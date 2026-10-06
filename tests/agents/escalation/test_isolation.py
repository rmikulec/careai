"""The escalation subagent must always run from a fresh, self-contained context.

These tests pin the guarantee that escalation never carries over the reporting
conversation: it has no ``messages`` channel, no checkpointer, and only ever
sends the model freshly built prompts derived from the report — even if a caller
tries to inject a prior conversation into its input. They also cover the notify
step draining the model's ``draft_notification`` calls into the queue.
"""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from CareAI.agents.escalation import assess_severity, build_escalation_agent
from CareAI.models import EscalationAssessment, IncidentReport, Notification


class _RecordingAssessor:
    """Structured-output runnable that records the messages it is invoked with."""

    def __init__(self, calls: list[list]) -> None:
        self._calls = calls

    async def ainvoke(self, messages: list) -> EscalationAssessment:
        self._calls.append(messages)
        return EscalationAssessment(severity="SEV-3", rationale="r", sources=[])


class _RecordingNotifier:
    """Tool-bound runnable that records its prompts and returns a canned reply."""

    def __init__(self, calls: list[list], reply: AIMessage) -> None:
        self._calls = calls
        self._reply = reply

    async def ainvoke(self, messages: list) -> AIMessage:
        self._calls.append(messages)
        return self._reply


class _FakeModel:
    """Chat model exposing the structured-output and tool-bound runnables."""

    def __init__(self, notify_reply: AIMessage | None = None) -> None:
        self.calls: list[list] = []
        self.notify_calls: list[list] = []
        self._notify_reply = notify_reply or AIMessage(content="", tool_calls=[])

    def with_structured_output(self, schema: type) -> _RecordingAssessor:
        assert schema is EscalationAssessment
        return _RecordingAssessor(self.calls)

    def bind_tools(self, tools: list) -> _RecordingNotifier:
        return _RecordingNotifier(self.notify_calls, self._notify_reply)


class _FakePolicyService:
    """Returns a single-chunk policy for any id, no database needed."""

    async def get(self, policy_id: str) -> dict:
        return {
            "policy_id": policy_id,
            "title": f"{policy_id} title",
            "chunks": [
                {
                    "chunk_index": 0,
                    "section": "Severity & Reporting",
                    "content": "SEV-1 catastrophic; SEV-2 major; SEV-3 minor.",
                }
            ],
        }


class _FakeNotificationService:
    """Records enqueued notifications without a database."""

    def __init__(self) -> None:
        self.enqueued: list[tuple[str, str | None, Notification]] = []

    async def enqueue(self, report_id, severity, notification):
        self.enqueued.append((report_id, severity, notification))

        class _Row:
            id = len(self.enqueued)
            recipient = notification.recipient
            channel = notification.channel
            subject = notification.subject

        return _Row()


def _report() -> IncidentReport:
    return IncidentReport(
        report_id="t1",
        reporter_id="u",
        reported_at="now",
        incident_type="fall",
        summary="unwitnessed fall",
        actions_taken=[
            {
                "description": "CT ordered late",
                "disposition": "omission",
                "related_policies": [{"policy_id": "POL-A", "chunk": 0, "reason": "r"}],
            }
        ],
    )


async def test_injected_conversation_never_reaches_the_model() -> None:
    """A conversation injected into the input must not reach any model call."""
    model = _FakeModel()
    agent = build_escalation_agent(
        model, _FakePolicyService(), _FakeNotificationService()
    )

    leaked = [
        HumanMessage("SECRET-PATIENT-CHATTER"),
        AIMessage("a prior assistant reply"),
    ]
    await agent.ainvoke(
        {"report": _report().model_dump(mode="json"), "messages": leaked}
    )

    # Both the assess and notify calls get exactly their two freshly built
    # messages — nothing from the injected "conversation".
    for sent in [*model.calls, *model.notify_calls]:
        assert [type(m).__name__ for m in sent] == ["SystemMessage", "HumanMessage"]
        assert all("SECRET-PATIENT-CHATTER" not in str(m.content) for m in sent)


async def test_result_state_has_no_messages_channel() -> None:
    """The agent's state carries no conversation — only report/policies/result."""
    agent = build_escalation_agent(
        _FakeModel(), _FakePolicyService(), _FakeNotificationService()
    )
    result = await agent.ainvoke({"report": _report().model_dump(mode="json")})
    assert "messages" not in result
    assert set(result) == {"report", "policies", "assessment", "notifications"}


async def test_prompt_is_grounded_only_in_report_and_policies() -> None:
    """The fresh assess prompt is built from the report brief and the policies."""
    model = _FakeModel()
    agent = build_escalation_agent(
        model, _FakePolicyService(), _FakeNotificationService()
    )
    await assess_severity(agent, _report())

    (sent,) = model.calls
    system = sent[0]
    assert isinstance(system, SystemMessage)
    assert "unwitnessed fall" in system.content  # report brief
    assert "SEV-2 major" in system.content  # fetched policy text


async def test_notify_queues_drafted_notifications() -> None:
    """draft_notification calls from the model are written to the queue."""
    reply = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "draft_notification",
                "args": {
                    "notification": {
                        "recipient": "Risk Management",
                        "channel": "email",
                        "subject": "SEV-3 fall",
                        "body": "An unwitnessed fall was reported.",
                        "related_policies": [
                            {"policy_id": "POL-A", "chunk": 0, "reason": "reporting"}
                        ],
                    }
                },
                "id": "call-1",
            }
        ],
    )
    notifications = _FakeNotificationService()
    agent = build_escalation_agent(
        _FakeModel(reply), _FakePolicyService(), notifications
    )

    result = await agent.ainvoke({"report": _report().model_dump(mode="json")})

    assert len(notifications.enqueued) == 1
    report_id, severity, notification = notifications.enqueued[0]
    assert report_id == "t1"
    assert severity == "SEV-3"
    assert notification.recipient == "Risk Management"
    assert result["notifications"][0]["recipient"] == "Risk Management"


async def test_no_notifications_when_model_drafts_none() -> None:
    """When the model calls no tool, nothing is queued."""
    notifications = _FakeNotificationService()
    agent = build_escalation_agent(_FakeModel(), _FakePolicyService(), notifications)
    result = await agent.ainvoke({"report": _report().model_dump(mode="json")})
    assert notifications.enqueued == []
    assert result["notifications"] == []


def test_agent_compiles_without_a_checkpointer() -> None:
    """No checkpointer means no cross-run persistence; every run starts cold."""
    agent = build_escalation_agent(
        _FakeModel(), _FakePolicyService(), _FakeNotificationService()
    )
    assert agent.checkpointer is None

"""The escalation subagent must always run from a fresh, self-contained context.

These tests pin the guarantee that escalation never carries over the reporting
conversation: it has no ``messages`` channel, no checkpointer, and only ever
sends the model a freshly built two-message prompt derived from the report — even
if a caller tries to inject a prior conversation into its input.
"""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from CareAI.agents.escalation import assess_severity, build_escalation_agent
from CareAI.models import EscalationAssessment, IncidentReport


class _RecordingAssessor:
    """Structured-output runnable that records the messages it is invoked with."""

    def __init__(self, calls: list[list]) -> None:
        self._calls = calls

    async def ainvoke(self, messages: list) -> EscalationAssessment:
        self._calls.append(messages)
        return EscalationAssessment(severity="SEV-3", rationale="r", sources=[])


class _FakeModel:
    """Chat model whose ``with_structured_output`` yields a recording assessor."""

    def __init__(self) -> None:
        self.calls: list[list] = []

    def with_structured_output(self, schema: type) -> _RecordingAssessor:
        assert schema is EscalationAssessment
        return _RecordingAssessor(self.calls)


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
    """A conversation injected into the input must not reach the model."""
    model = _FakeModel()
    agent = build_escalation_agent(model, _FakePolicyService())

    leaked = [
        HumanMessage("SECRET-PATIENT-CHATTER"),
        AIMessage("a prior assistant reply"),
    ]
    await agent.ainvoke(
        {"report": _report().model_dump(mode="json"), "messages": leaked}
    )

    (sent,) = model.calls
    # Exactly the two freshly built messages — nothing from the "conversation".
    assert [type(m).__name__ for m in sent] == ["SystemMessage", "HumanMessage"]
    assert all("SECRET-PATIENT-CHATTER" not in str(m.content) for m in sent)


async def test_result_state_has_no_messages_channel() -> None:
    """The agent's state carries no conversation — only report/policies/result."""
    agent = build_escalation_agent(_FakeModel(), _FakePolicyService())
    result = await agent.ainvoke({"report": _report().model_dump(mode="json")})
    assert "messages" not in result
    assert set(result) == {"report", "policies", "assessment"}


async def test_prompt_is_grounded_only_in_report_and_policies() -> None:
    """The fresh prompt is built from the report brief and the fetched policies."""
    model = _FakeModel()
    agent = build_escalation_agent(model, _FakePolicyService())
    await assess_severity(agent, _report())

    (sent,) = model.calls
    system = sent[0]
    assert isinstance(system, SystemMessage)
    assert "unwitnessed fall" in system.content  # report brief
    assert "SEV-2 major" in system.content  # fetched policy text


def test_agent_compiles_without_a_checkpointer() -> None:
    """No checkpointer means no cross-run persistence; every run starts cold."""
    agent = build_escalation_agent(_FakeModel(), _FakePolicyService())
    assert agent.checkpointer is None

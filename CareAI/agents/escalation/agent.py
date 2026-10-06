"""The escalation agent: a policy-grounded severity assessment step.

Runs once a report is finalized. It reads the incident report and the full text
of the policies already linked to it during intake, then reasons about the
incident's severity strictly from the severity/escalation criteria those policies
define. The scale is the facility's own (e.g. the SEV-1..SEV-3 / Near Miss scale
in POL-RM-013), never one imposed here. It returns the level with a grounded
rationale and chunk citations, or a null severity when the linked policies
specify no applicable criteria (leaving the report for human triage).

It is a **self-contained subagent that always starts from a fresh context**: its
state (``EscalationState``) has no ``messages`` channel and it compiles with no
checkpointer, so it never sees — and cannot be given — the reporting
conversation. It is handed only the finalized report dict (assembled from state
channels, not the message log) and builds each of its prompts from scratch on
every run.

The flow is deliberately small and linear:

1. ``gather`` — refetch the full text of every policy cited by the report, so the
   assessment sees complete policy text (including Severity & Reporting sections
   that intake may not have cited), not just the chunks that happened to ground
   an action or factor.
2. ``assess`` — one grounded, structured-output model call producing an
   :class:`CareAI.models.EscalationAssessment`.
3. ``notify`` — bind the ``draft_notification`` tool and, depending on the
   assessed severity, draft the notifications the policies require (who to notify,
   per their Severity & Reporting sections). Each drafted notification is written
   to the notifications queue (``CareAI.database.notification``), which nothing
   consumes yet in this demo.
"""

import logging

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from opentelemetry import trace

from CareAI.agents.escalation.prompts import ESCALATION_PROMPT, NOTIFY_PROMPT
from CareAI.agents.escalation.state import EscalationState
from CareAI.agents.escalation.tools import DRAFT_NOTIFICATION, build_escalation_tools
from CareAI.database.notification import NotificationService
from CareAI.database.policy import PolicyService
from CareAI.models import EscalationAssessment, IncidentReport, Notification

logger = logging.getLogger(__name__)

# Resolves to a no-op provider unless the app configures OpenTelemetry.
_tracer = trace.get_tracer(__name__)


def _cited_policy_ids(report: dict) -> list[str]:
    """Return the distinct policy ids cited by the report, in first-seen order.

    Args:
        report (dict): A finalized ``IncidentReport`` as a dict.

    Returns:
        list[str]: Every ``policy_id`` cited across the report's assessed actions
        and contributing factors, de-duplicated preserving order.
    """
    ids: list[str] = []
    seen: set[str] = set()
    items = (report.get("actions_taken") or []) + (
        report.get("contributing_factors") or []
    )
    for item in items:
        for link in item.get("related_policies") or []:
            pid = link.get("policy_id")
            if pid and pid not in seen:
                seen.add(pid)
                ids.append(pid)
    return ids


def _format_report(report: dict) -> str:
    """Render the incident report as a compact brief for the prompt."""
    lines = [
        f"- Type: {report.get('incident_type') or '—'}",
        f"- When: {report.get('occurred_at') or '—'}",
        f"- Where: {report.get('location') or '—'}",
        f"- Summary: {report.get('summary') or '—'}",
    ]
    factors = report.get("contributing_factors") or []
    if factors:
        lines.append("- Contributing factors:")
        lines += [f"  - {f.get('description', '')}" for f in factors]
    actions = report.get("actions_taken") or []
    if actions:
        lines.append("- Assessed actions (disposition):")
        lines += [
            f"  - [{a.get('disposition', '?')}] {a.get('description', '')}"
            for a in actions
        ]
    return "\n".join(lines)


def _format_policies(policies: list[dict]) -> str:
    """Render the linked policies' full chunk text with citable chunk indices."""
    if not policies:
        return "(no policies were linked to this report)"
    blocks = []
    for p in policies:
        chunks = "\n".join(
            f"  chunk {c['chunk_index']} [{c.get('section') or '-'}]: {c['content']}"
            for c in p.get("chunks", [])
        )
        blocks.append(f"[{p['policy_id']}] {p['title']}\n{chunks}")
    return "\n\n".join(blocks)


def build_escalation_agent(
    model: BaseChatModel,
    policy_service: PolicyService,
    notification_service: NotificationService,
) -> CompiledStateGraph:
    """Build and compile the escalation (severity + notifications) agent graph.

    Args:
        model (BaseChatModel): Chat model used for the grounded severity call and
            the notification-drafting step.
        policy_service (PolicyService): Retrieval service used to refetch the full
            text of the policies cited by the report.
        notification_service (NotificationService): Queue the ``draft_notification``
            tool writes drafted notifications to.

    Returns:
        CompiledStateGraph: The compiled agent. Invoke it with ``{"report": ...}``
        (a finalized ``IncidentReport`` as a dict); the result carries the
        ``EscalationAssessment`` under the ``assessment`` key, and any drafted
        notifications are queued as a side effect.
    """
    assessor = model.with_structured_output(EscalationAssessment)
    notifier = model.bind_tools(build_escalation_tools())

    async def gather(state: EscalationState) -> dict:
        """Refetch the full text of every policy cited by the report."""
        policies: list[dict] = []
        for pid in _cited_policy_ids(state["report"]):
            pol = await policy_service.get(pid)
            if pol is not None:
                policies.append(pol)
        return {"policies": policies}

    async def assess(state: EscalationState) -> dict:
        """Classify the incident's severity, grounded in the linked policies."""
        with _tracer.start_as_current_span("escalation.assess") as span:
            policies = state.get("policies", [])
            span.set_attribute("careai.policies", len(policies))
            system = SystemMessage(
                ESCALATION_PROMPT
                + f"\n\nIncident report:\n{_format_report(state['report'])}"
                + f"\n\nLinked policy text:\n{_format_policies(policies)}"
            )
            assessment: EscalationAssessment = await assessor.ainvoke(
                [system, HumanMessage("Assess this incident's severity now.")]
            )
            span.set_attribute("careai.severity", assessment.severity or "undetermined")
            return {"assessment": assessment.model_dump()}

    async def notify(state: EscalationState) -> dict:
        """Draft and queue the notifications the policies require at this severity.

        The model proposes ``draft_notification`` calls (zero or more, depending
        on the assessed severity); this node drains them, stamps each with the
        report id and severity from state, and writes it to the queue.
        """
        with _tracer.start_as_current_span("escalation.notify") as span:
            assessment = state.get("assessment") or {}
            severity = assessment.get("severity")
            span.set_attribute("careai.severity", severity or "undetermined")
            report = state["report"]
            report_brief = _format_report(report)
            policy_text = _format_policies(state.get("policies", []))
            system = SystemMessage(
                NOTIFY_PROMPT
                + "\n\nAssessed severity: "
                + (severity or "none (policies define no applicable criteria)")
                + f"\n\nSeverity rationale: {assessment.get('rationale', '')}"
                + f"\n\nIncident report:\n{report_brief}"
                + f"\n\nLinked policy text:\n{policy_text}"
            )
            response = await notifier.ainvoke(
                [system, HumanMessage("Draft any required notifications now.")]
            )

            queued: list[dict] = []
            report_id = report.get("report_id", "unknown")
            for call in getattr(response, "tool_calls", None) or []:
                if call.get("name") != DRAFT_NOTIFICATION:
                    continue
                try:
                    notification = Notification.model_validate(
                        call["args"]["notification"]
                    )
                except (KeyError, ValueError):
                    logger.warning("Discarding malformed draft_notification call")
                    continue
                record = await notification_service.enqueue(
                    report_id, severity, notification
                )
                queued.append(
                    {
                        "id": record.id,
                        "recipient": record.recipient,
                        "channel": record.channel,
                        "subject": record.subject,
                    }
                )
            span.set_attribute("careai.notifications", len(queued))
            return {"notifications": queued}

    builder = StateGraph(EscalationState)
    builder.add_node("gather", gather)
    builder.add_node("assess", assess)
    builder.add_node("notify", notify)
    builder.add_edge(START, "gather")
    builder.add_edge("gather", "assess")
    builder.add_edge("assess", "notify")
    builder.add_edge("notify", END)
    return builder.compile()


async def assess_severity(
    agent: CompiledStateGraph, report: IncidentReport
) -> EscalationAssessment:
    """Run the escalation agent over a finalized report and return its assessment.

    The agent is invoked with *only* the serialized report — never the reporting
    conversation — so the assessment always runs from a fresh context.

    Args:
        agent (CompiledStateGraph): A compiled escalation agent.
        report (IncidentReport): The finalized report to assess.

    Returns:
        EscalationAssessment: The policy-grounded severity assessment.
    """
    result = await agent.ainvoke({"report": report.model_dump(mode="json")})
    return EscalationAssessment.model_validate(result["assessment"])

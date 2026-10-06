"""Shared graph state for the escalation agent."""

from typing import TypedDict


class EscalationState(TypedDict, total=False):
    """State threaded through the escalation agent graph.

    The flow is linear (``gather`` -> ``assess`` -> ``notify``). Each channel is
    written once and the default last-value semantics suffice — no custom
    reducers, and deliberately **no ``messages`` channel**: the subagent never
    carries a conversation, so the reporting chat cannot leak in. Each node builds
    its own fresh prompt from the report and policies.

    Attributes:
        report: The finalized ``IncidentReport`` as a JSON-ready dict (the input).
        policies: Full text of the policies cited by the report, fetched for
            grounding; each ``{policy_id, title, chunks}`` as returned by
            ``PolicyService.get``.
        assessment: The resulting ``EscalationAssessment`` as a dict.
        notifications: Summaries of the notifications queued this run (one dict
            per drafted notification); empty when the severity warranted none.
    """

    report: dict
    policies: list[dict]
    assessment: dict
    notifications: list[dict]

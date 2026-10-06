"""Shared graph state for the escalation agent."""

from typing import TypedDict


class EscalationState(TypedDict, total=False):
    """State threaded through the escalation agent graph.

    The flow is linear (``gather`` -> ``assess``), so each channel is written
    once and the default last-value semantics suffice — no custom reducers.

    Attributes:
        report: The finalized ``IncidentReport`` as a JSON-ready dict (the input).
        policies: Full text of the policies cited by the report, fetched for
            grounding; each ``{policy_id, title, chunks}`` as returned by
            ``PolicyService.get``.
        assessment: The resulting ``EscalationAssessment`` as a dict (the output).
    """

    report: dict
    policies: list[dict]
    assessment: dict

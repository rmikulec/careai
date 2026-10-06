from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

Role = Literal["patient", "staff", "witness", "reporter"]

# Compliance disposition of a policy-required action, in the standard
# omission/commission framing used in clinical root-cause analysis:
#   - done_correctly: the required action was performed as the policy specifies.
#   - omission: a required action was not performed (it should have been).
#   - commission: an action was performed incorrectly, or one was performed that
#     should not have been.
ActionDisposition = Literal["done_correctly", "omission", "commission"]


class Person(BaseModel):
    """A person involved in the incident."""

    name: str = Field(description="Name or identifier of the person.")
    role: Role = Field(description="Their role in the incident.")


class ReportInfo(BaseModel):
    """Header details gathered from the practitioner during intake."""

    incident_type: str | None = Field(
        default=None, description="e.g. needlestick, fall, medication."
    )
    occurred_at: str | None = Field(
        default=None, description="When the incident happened."
    )
    location: str | None = Field(default=None, description="Ward, unit, or department.")
    summary: str | None = Field(
        default=None, description="One or two sentences on what happened."
    )
    people: list[Person] | None = Field(
        default=None, description="People involved, each with a role."
    )


class PolicyLink(BaseModel):
    """A citation linking a report item to the specific policy chunk that grounds it.

    Attributes:
        policy_id (str): Id of an added policy.
        chunk (int): Index of the chunk within that policy that grounds the item
            (a ``chunk`` value from a ``search_policies`` result).
        reason (str): Why this item satisfies or relates to that chunk.
    """

    policy_id: str = Field(description="Id of an added policy.")
    chunk: int = Field(description="Index of the policy chunk that grounds this item.")
    reason: str = Field(description="Why this item satisfies or relates to the chunk.")


class ActionTaken(BaseModel):
    """A policy-required action and whether it was carried out as required.

    Despite the name, this records the *assessed* action, not only actions that
    happened: an omitted action (required but not done) is recorded too, with its
    disposition set accordingly. Omissions and commissions are the procedure gaps
    the review step and manager view surface.

    Attributes:
        description (str): The action the policy called for and what actually
            happened (e.g. "Seen by Employee Health within 2h" or "Source-patient
            consent for testing was not obtained").
        disposition (ActionDisposition): Whether the action was done correctly,
            omitted, or a commission error.
        related_policies (list[PolicyLink]): Policy chunk citations grounding the
            action, each a policy id, chunk index, and reason.
    """

    description: str = Field(description="The required action and what happened.")
    disposition: ActionDisposition = Field(
        description="Whether it was done correctly, omitted, or a commission error."
    )
    related_policies: list[PolicyLink] = Field(
        description="Policy chunk citations grounding the action."
    )


class ContributingFactor(BaseModel):
    """A condition or cause that contributed to the incident."""

    description: str = Field(description="The contributing factor or cause.")
    related_policies: list[PolicyLink] = Field(
        default_factory=list,
        description=(
            "Optional citations, only when the factor is a deviation from a "
            "policy standard."
        ),
    )


class EscalationAssessment(BaseModel):
    """A policy-grounded severity assessment of a finalized incident.

    Produced by the escalation agent after intake finishes: it reads the report
    and the full text of the policies already linked to it, applies the
    severity/escalation criteria those policies define, and records the resulting
    level with its reasoning and citations. The severity *scale* is whatever the
    facility's policies specify (e.g. the SEV-1..SEV-3 / Near Miss scale in
    POL-RM-013) — never a scale imposed by this system.

    Attributes:
        severity (Optional[str]): The severity level using the policies' own
            labels (e.g. ``"SEV-2"``), or ``None`` when the linked policies
            define no applicable severity criteria — the report is then left for
            human triage rather than given an invented level.
        rationale (str): Why this level, grounded in the cited policy criteria.
        sources (list[PolicyLink]): Citations to the policy chunks the assessment
            relied on, each a policy id, chunk index, and reason.
    """

    severity: str | None = Field(
        default=None,
        description=(
            "Severity level using the facility policies' own labels (e.g. "
            "'SEV-2'), or null if the linked policies specify no applicable "
            "severity criteria. Never invent a scale."
        ),
    )
    rationale: str = Field(
        description="Why this level, grounded in the cited policy criteria."
    )
    sources: list[PolicyLink] = Field(
        default_factory=list,
        description="Citations to the policy chunks the assessment relied on.",
    )


class IncidentReport(BaseModel):
    """A structured incident report assembled from gathered info and recorded items."""

    report_id: str
    reporter_id: str
    reported_at: str
    status: Literal["collecting", "partial", "complete"] = "collecting"
    severity: str | None = None
    escalation: EscalationAssessment | None = None
    incident_type: str | None = None
    occurred_at: str | None = None
    location: str | None = None
    summary: str | None = None
    people: list[Person] = Field(default_factory=list)
    actions_taken: list[ActionTaken] = Field(default_factory=list)
    contributing_factors: list[ContributingFactor] = Field(default_factory=list)

    @classmethod
    def from_graph_state(
        cls,
        thread_id: str,
        state: dict[str, Any],
        reporter_id: str = "unknown",
    ) -> "IncidentReport":
        """Assemble a finalized report from the reporting agent's graph state.

        Maps the state channels the agent accumulates (``report_info``,
        ``people``, ``actions``, ``factors``) onto the report's fields. The
        recorded action/factor dicts carry enriched citation keys (``section``,
        ``content``) beyond :class:`PolicyLink`'s fields; those extras are
        ignored during validation.

        Args:
            thread_id (str): The reporting thread; used as the ``report_id``.
            state (dict[str, Any]): The agent's graph state for the thread.
            reporter_id (str): Identifier of the reporting practitioner; defaults
                to ``"unknown"`` where no identity is carried on the request.

        Returns:
            IncidentReport: The assembled report, marked ``complete``.
        """
        info = state.get("report_info", {}) or {}
        return cls(
            report_id=thread_id,
            reporter_id=reporter_id,
            reported_at=datetime.now(timezone.utc).isoformat(),
            status="complete",
            incident_type=info.get("incident_type"),
            occurred_at=info.get("occurred_at"),
            location=info.get("location"),
            summary=info.get("summary"),
            people=state.get("people", []) or [],
            actions_taken=state.get("actions", []) or [],
            contributing_factors=state.get("factors", []) or [],
        )

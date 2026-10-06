"""The intake plan: the lines of inquiry derived from the retrieved policies.

After policy discovery, the agent reads the full text of the added policies and
drafts an :class:`IntakePlan` — the concrete factor probes and action checks it
intends to work through. The plan is shown to the practitioner, stored in state,
and used to decide what to ask next (and, with policy coverage, when to stop).
"""

from typing import Literal

from pydantic import BaseModel, Field


class PlanItem(BaseModel):
    """One line of inquiry the agent intends to pursue during deep-dive intake.

    Attributes:
        policy_id (str): Id of the added policy this inquiry is grounded in.
        kind (Literal["factor", "action"]): Whether it probes a contributing
            factor or verifies an action the policy requires.
        topic (str): The question to ask or the detail to confirm.
        rationale (str): Why it matters, grounded in the policy.
    """

    policy_id: str = Field(description="Added policy id this inquiry grounds in.")
    kind: Literal["factor", "action"] = Field(
        description="Probe a contributing factor, or verify a required action."
    )
    topic: str = Field(description="The question to ask or detail to confirm.")
    rationale: str = Field(description="Why it matters, grounded in the policy.")


class IntakePlan(BaseModel):
    """The ordered set of inquiries to work through after policy discovery.

    Attributes:
        items (list[PlanItem]): Planned factor probes and action checks, roughly
            in the order the agent intends to pursue them.
    """

    items: list[PlanItem] = Field(
        default_factory=list, description="Planned factor probes and action checks."
    )

"""The intake plan: the lines of inquiry derived from the retrieved policies.

After policy discovery, the agent reads the full text of the added policies and
drafts an :class:`IntakePlan` — the concrete factor probes and action checks it
intends to work through, with requirements shared across policies consolidated
into a single item each. The plan is internal (not shown to the practitioner):
it is stored in state and used to decide what to ask next and, once every
``action`` item has been assessed, when to stop.
"""

from typing import Literal

from pydantic import BaseModel, Field


class PlanItem(BaseModel):
    """One line of inquiry the agent intends to pursue during deep-dive intake.

    A single item may consolidate a requirement shared by several policies, so it
    grounds in a *list* of policy ids rather than one. Each item carries a stable
    ``id`` (assigned in code after drafting) that the recording tools reference via
    their ``satisfies`` argument, so the deep-dive loops can drop an item once it
    has been addressed instead of re-asking it.

    Attributes:
        id (str): Stable identifier for the item (e.g. ``factor-1``, ``action-2``).
            Assigned by the agent after drafting; leave it empty when drafting.
        kind (Literal["factor", "action"]): Whether it probes a contributing
            factor or verifies an action the policies require.
        topic (str): The question to ask or the detail to confirm.
        rationale (str): Why it matters, grounded in the policies.
        policy_ids (list[str]): Added policy ids this inquiry grounds in. List more
            than one when the same requirement or factor recurs across policies —
            consolidate it into a single item rather than repeating it per policy.
    """

    id: str = Field(
        default="",
        description="Stable item id; assigned after drafting, leave empty.",
    )
    kind: Literal["factor", "action"] = Field(
        description="Probe a contributing factor, or verify a required action."
    )
    topic: str = Field(description="The question to ask or detail to confirm.")
    rationale: str = Field(description="Why it matters, grounded in the policies.")
    policy_ids: list[str] = Field(
        description=(
            "Added policy ids this inquiry grounds in; list all policies that "
            "share the requirement so it is asked once, not once per policy."
        )
    )


class IntakePlan(BaseModel):
    """The ordered set of inquiries to work through after policy discovery.

    Attributes:
        items (list[PlanItem]): Planned factor probes and action checks, roughly
            in the order the agent intends to pursue them.
    """

    items: list[PlanItem] = Field(
        default_factory=list, description="Planned factor probes and action checks."
    )

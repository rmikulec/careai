"""Shared graph state for the reporting agent."""

import operator
from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages

from CareAI.agents.reporting.reducers import (
    add_people,
    add_policies,
    merge_info,
    take_latest,
)


class ReportingState(TypedDict):
    """State threaded through the reporting agent graph.

    Attributes:
        messages: Conversation history (appended via ``add_messages``).
        report_info: Gathered header scalars (merged via ``merge_info``).
        people: People involved, de-duped by ``(name, role)``.
        policies: Added policies forming the grounding set, de-duped by id.
        actions: Recorded actions taken, each with policy citations.
        factors: Recorded contributing factors, each with optional citations.
        phase: Current stage of the semi-structured flow (``basics`` ->
            ``discover`` -> ``plan`` -> ``factors`` -> ``actions`` -> ``done``);
            the latest value set wins, so entry routing resumes the right stage
            next turn.
        discover_rounds: How many policy-discovery turns have run (summed); a
            cap on this keeps the autonomous discovery loop from running away.
        plan: The intake plan (``PlanItem`` dicts) drafted from the retrieved
            policies; guides what to ask in the factors and actions stages.
    """

    messages: Annotated[list, add_messages]
    report_info: Annotated[dict, merge_info]
    people: Annotated[list[dict], add_people]
    policies: Annotated[list[dict], add_policies]
    actions: Annotated[list[dict], operator.add]
    factors: Annotated[list[dict], operator.add]
    phase: Annotated[str, take_latest]
    discover_rounds: Annotated[int, operator.add]
    plan: Annotated[list[dict], take_latest]

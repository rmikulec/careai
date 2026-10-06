"""The reporting agent: a semi-structured, four-stage LangGraph.

The flow's *stages* are fixed by the graph; the *reasoning* within each stage is
the LLM's:

1. ``basics`` — ``extract_basics`` pulls header fields out of the conversation and
   ``ask_basics`` requests whatever is still missing in one markdown question.
2. ``discover`` — a reasoned policy loop (``discover`` <-> ``tools``) that
   searches the policy library and adds every relevant policy, following the
   threads between related policies and narrating its findings to the user.
3. ``plan`` — reads the full text of the added policies and drafts an
   ``IntakePlan`` (the factor probes and action checks to work through), shown to
   the practitioner and stored in state to steer the deep-dive stages.
4. ``factors`` — a grounded Q&A loop that digs into the confounding/contributing
   factors behind the incident, reasoning after each one about what to ask next,
   and (re)searching policy if a new facet appears. Ends by advancing to actions.
5. ``actions`` — a grounded Q&A loop that establishes, policy by policy, what
   action each required and its disposition (done correctly / omission /
   commission), reasoning after each about what to confirm next. Intake finishes
   only once every added policy has a recorded action.

The stage is tracked in ``ReportingState.phase`` so each new user message resumes
the correct loop, and so a tool loop returns to the loop it came from.
"""

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

from CareAI.agents.reporting.plan import IntakePlan
from CareAI.agents.reporting.prompts import (
    ACTIONS_PROMPT,
    BASIC_QUESTIONS,
    DISCOVER_PROMPT,
    FACTORS_PROMPT,
    INTAKE_INSTRUCTIONS,
    PHASE_ACTIONS,
    PHASE_BASICS,
    PHASE_DISCOVER,
    PHASE_DONE,
    PHASE_FACTORS,
    PHASE_PLAN,
    PLAN_PROMPT,
    REQUIRED_BASICS,
)
from CareAI.agents.reporting.state import ReportingState
from CareAI.agents.reporting.tools import build_reporting_tools, covered_policy_ids
from CareAI.database.policy import PolicyService
from CareAI.models import ReportInfo

_INTAKE_SYSTEM = SystemMessage(INTAKE_INSTRUCTIONS)

# Cap on autonomous policy-discovery turns. Each turn is one model call plus its
# tool round, so this also keeps us clear of the graph recursion limit.
_MAX_DISCOVER_ROUNDS = 8

# Which stage each phase resumes into when a new user message arrives.
_ENTRY_NODE: dict[str, str] = {
    PHASE_BASICS: "extract_basics",
    PHASE_DISCOVER: "discover",
    PHASE_FACTORS: "factors",
    PHASE_PLAN: "plan",
    PHASE_ACTIONS: "actions",
    PHASE_DONE: "actions",
}

# Which loop a tool round returns to, keyed by the phase the tools left in state.
_TOOLS_NODE: dict[str, str] = {
    PHASE_DISCOVER: "discover",
    PHASE_FACTORS: "factors",
    PHASE_ACTIONS: "actions",
    PHASE_DONE: "wrap_up",
}


def _basics_complete(state: ReportingState) -> bool:
    """Return ``True`` once every required header basic is present."""
    info = state.get("report_info", {})
    return all(info.get(k) for k in REQUIRED_BASICS)


def _format_info(info: dict) -> str:
    """Render the header basics as a bullet list for a system prompt."""
    return "\n".join(f"- {k}: {v}" for k, v in info.items()) or "(none)"


def _format_policies(policies: list[dict]) -> str:
    """Render the added grounding policies as a bullet list for a prompt."""
    if not policies:
        return "(none yet)"
    return "\n".join(f"- {p['id']}: {p['title']}" for p in policies)


def _format_plan(plan: list[dict], kind: str) -> str:
    """Render the plan items of one kind (``factor``/``action``) as bullets."""
    items = [i for i in plan if i.get("kind") == kind]
    if not items:
        return "(none)"
    return "\n".join(
        f"- ({i['policy_id']}) {i['topic']} — {i['rationale']}" for i in items
    )


def _deep_dive_context(state: ReportingState) -> str:
    """Build the shared context for the factors and actions loops.

    Surfaces the basics, the added policies, the intake plan split by kind, what
    has been recorded so far, and which policies still lack a recorded action —
    so the loop can reason about what to ask next and know when it is done.
    """
    info = state.get("report_info", {})
    policies = state.get("policies", [])
    plan = state.get("plan", [])
    factors = state.get("factors", [])
    actions = state.get("actions", [])
    uncovered = sorted({p["id"] for p in policies} - covered_policy_ids(actions))
    recorded_factors = "\n".join(f"- {f['description']}" for f in factors) or "(none)"
    recorded_actions = (
        "\n".join(
            f"- [{a.get('disposition', '?')}] {a['description']}" for a in actions
        )
        or "(none)"
    )
    return (
        f"\n\nIncident basics:\n{_format_info(info)}"
        f"\n\nPolicies on file:\n{_format_policies(policies)}"
        f"\n\nPlan — contributing factors to explore:\n{_format_plan(plan, 'factor')}"
        f"\n\nPlan — actions to verify:\n{_format_plan(plan, 'action')}"
        f"\n\nContributing factors recorded so far:\n{recorded_factors}"
        f"\n\nActions recorded so far:\n{recorded_actions}"
        f"\n\nAdded policies still without a recorded action: {uncovered or 'none'}"
    )


def _has_tool_calls(state: ReportingState) -> bool:
    """Return ``True`` if the last message carries tool calls to execute."""
    last = state["messages"][-1]
    return bool(getattr(last, "tool_calls", None))


def build_reporting_agent(
    model: BaseChatModel,
    policy_service: PolicyService,
    checkpointer: BaseCheckpointSaver | None = None,
) -> CompiledStateGraph:
    """Build and compile the reporting agent graph.

    Args:
        model (BaseChatModel): Chat model used for intake extraction and every
            policy/question loop. Tools are bound to per-stage copies internally.
        policy_service (PolicyService): Retrieval service the policy tools use.
        checkpointer (Optional[BaseCheckpointSaver]): Persistence for multi-turn
            conversations; an in-memory saver is used if omitted.

    Returns:
        CompiledStateGraph: The compiled, runnable agent. Invoke it with
        ``{"messages": [...]}`` and a ``thread_id`` in the config.
    """
    tools = build_reporting_tools(policy_service)
    by_name = {t.name: t for t in tools}

    # Each stage sees only the tools it should use; the shared ToolNode executes
    # whichever was called regardless of stage.
    discover_model = model.bind_tools(
        [by_name["search_policies"], by_name["add_policy"]]
    )
    factors_model = model.bind_tools(
        [
            by_name["search_policies"],
            by_name["add_policy"],
            by_name["search_incidents"],
            by_name["record_contributing_factor"],
            by_name["record_report_info"],
            by_name["advance_to_actions"],
        ]
    )
    actions_model = model.bind_tools(
        [
            by_name["search_policies"],
            by_name["add_policy"],
            by_name["search_incidents"],
            by_name["record_action"],
            by_name["record_report_info"],
            by_name["finish_report"],
        ]
    )

    async def extract_basics(state: ReportingState) -> dict:
        """Pull any stated header basics out of the conversation (phase 1)."""
        if _basics_complete(state):
            return {"phase": PHASE_DISCOVER}
        info = await model.with_structured_output(ReportInfo).ainvoke(
            [_INTAKE_SYSTEM, *state["messages"]]
        )
        data = info.model_dump()
        people = data.pop("people", None) or []
        scalars = {k: v for k, v in data.items() if v is not None}
        update: dict = {}
        if scalars:
            update["report_info"] = scalars
        if people:
            update["people"] = people
        merged = {**state.get("report_info", {}), **scalars}
        if all(merged.get(k) for k in REQUIRED_BASICS):
            update["phase"] = PHASE_DISCOVER
        return update

    def ask_basics(state: ReportingState) -> dict:
        """Ask for all still-missing basics in one markdown question."""
        info = state.get("report_info", {})
        missing = [BASIC_QUESTIONS[k] for k in REQUIRED_BASICS if not info.get(k)]
        bullets = "\n".join(f"- {q}" for q in missing)
        message = AIMessage(
            "Thanks for bringing this forward — reporting it helps protect future "
            "patients and colleagues. This is a blameless report: the goal is to "
            "understand what happened and why so we can improve the workflow, not "
            "to assign fault.\n\nTo file it correctly, I just need a few basics:\n\n"
            f"{bullets}\n\nYou can answer them all in one message."
        )
        return {"messages": [message]}

    async def discover(state: ReportingState) -> dict:
        """Run one autonomous turn of the reasoned policy-discovery loop."""
        if state.get("discover_rounds", 0) >= _MAX_DISCOVER_ROUNDS:
            # Hard stop: hand off to the factors stage with what we have.
            return {
                "messages": [AIMessage("Policy discovery capped; proceeding.")],
                "phase": PHASE_DISCOVER,
            }
        info = state.get("report_info", {})
        system = SystemMessage(
            DISCOVER_PROMPT + f"\n\nIncident basics:\n{_format_info(info)}"
        )
        response = await discover_model.ainvoke([system, *state["messages"]])
        return {
            "messages": [response],
            "phase": PHASE_DISCOVER,
            "discover_rounds": 1,
        }

    async def plan(state: ReportingState) -> dict:
        """Draft the intake plan from the full added-policy text (phase 2.5)."""
        info = state.get("report_info", {})
        policies = state.get("policies", [])
        corpus = (
            "\n\n".join(
                f"[{p['id']}] {p['title']}\n"
                + "\n".join(
                    f"  chunk {c['chunk_index']} "
                    f"[{c.get('section') or '-'}]: {c['content']}"
                    for c in p.get("chunks", [])
                )
                for p in policies
            )
            or "(no policies were added)"
        )
        system = SystemMessage(
            PLAN_PROMPT
            + f"\n\nIncident basics:\n{_format_info(info)}"
            + f"\n\nRetrieved policy text:\n{corpus}"
        )
        drafted = await model.with_structured_output(IntakePlan).ainvoke(
            [system, HumanMessage("Draft the intake plan now.")]
        )
        items = [item.model_dump() for item in drafted.items]
        # The plan stays internal — it steers the factors/actions prompts via
        # state and is never shown to the practitioner.
        return {"plan": items, "phase": PHASE_FACTORS}

    async def factors(state: ReportingState) -> dict:
        """Run one turn of the contributing-factors Q&A loop (phase 3a)."""
        system = SystemMessage(FACTORS_PROMPT + _deep_dive_context(state))
        response = await factors_model.ainvoke([system, *state["messages"]])
        return {"messages": [response], "phase": PHASE_FACTORS}

    async def actions(state: ReportingState) -> dict:
        """Run one turn of the actions-taken Q&A loop (phase 3b)."""
        system = SystemMessage(ACTIONS_PROMPT + _deep_dive_context(state))
        response = await actions_model.ainvoke([system, *state["messages"]])
        return {"messages": [response], "phase": PHASE_ACTIONS}

    def wrap_up(state: ReportingState) -> dict:
        """Emit a deterministic markdown summary of the collected report."""
        return {"messages": [AIMessage(_render_summary(state))], "phase": PHASE_DONE}

    def route_entry(state: ReportingState) -> str:
        """Resume the stage matching the stored phase for a new user message."""
        return _ENTRY_NODE.get(state.get("phase", PHASE_BASICS), "extract_basics")

    def route_after_extract(state: ReportingState) -> str:
        """Discover policies once basics are complete, else ask for them."""
        return "discover" if _basics_complete(state) else "ask_basics"

    def route_after_discover(state: ReportingState) -> str:
        """Keep searching while tools are called, else draft the intake plan."""
        return "tools" if _has_tool_calls(state) else "plan"

    def route_after_loop(state: ReportingState) -> str:
        """Run requested tools, else end the turn on a question to the user."""
        return "tools" if _has_tool_calls(state) else END

    def route_after_tools(state: ReportingState) -> str:
        """Return to the loop that called the tools (phase set in state)."""
        return _TOOLS_NODE.get(state.get("phase", PHASE_DISCOVER), "factors")

    builder = StateGraph(ReportingState)
    builder.add_node("extract_basics", extract_basics)
    builder.add_node("ask_basics", ask_basics)
    builder.add_node("discover", discover)
    builder.add_node("plan", plan)
    builder.add_node("factors", factors)
    builder.add_node("actions", actions)
    builder.add_node("tools", ToolNode(tools))
    builder.add_node("wrap_up", wrap_up)

    builder.add_conditional_edges(
        START,
        route_entry,
        {
            "extract_basics": "extract_basics",
            "discover": "discover",
            "plan": "plan",
            "factors": "factors",
            "actions": "actions",
        },
    )
    builder.add_conditional_edges(
        "extract_basics",
        route_after_extract,
        {"discover": "discover", "ask_basics": "ask_basics"},
    )
    builder.add_edge("ask_basics", END)
    builder.add_conditional_edges(
        "discover", route_after_discover, {"tools": "tools", "plan": "plan"}
    )
    builder.add_edge("plan", "factors")
    builder.add_conditional_edges(
        "factors", route_after_loop, {"tools": "tools", END: END}
    )
    builder.add_conditional_edges(
        "actions", route_after_loop, {"tools": "tools", END: END}
    )
    builder.add_conditional_edges(
        "tools",
        route_after_tools,
        {
            "discover": "discover",
            "factors": "factors",
            "actions": "actions",
            "wrap_up": "wrap_up",
        },
    )
    builder.add_edge("wrap_up", END)

    return builder.compile(checkpointer=checkpointer or InMemorySaver())


def _render_summary(state: ReportingState) -> str:
    """Render the collected report as a markdown summary for the practitioner."""
    info = state.get("report_info", {})
    lines = ["## Incident report summary", ""]
    lines.append(f"- **Type:** {info.get('incident_type', '—')}")
    lines.append(f"- **When:** {info.get('occurred_at', '—')}")
    lines.append(f"- **Where:** {info.get('location', '—')}")
    lines.append(f"- **What happened:** {info.get('summary', '—')}")

    people = state.get("people", [])
    if people:
        lines += ["", "**People involved**"]
        lines += [f"- {p['name']} — *{p['role']}*" for p in people]

    factors = state.get("factors", [])
    if factors:
        lines += ["", "**Contributing factors**"]
        lines += [f"- {f['description']}" for f in factors]

    actions = state.get("actions", [])
    if actions:
        lines += ["", "**Actions assessed**"]
        lines += [
            f"- {_DISPOSITION_LABEL.get(a.get('disposition'), '•')} {a['description']}"
            for a in actions
        ]
        gaps = [
            a for a in actions if a.get("disposition") in ("omission", "commission")
        ]
        if gaps:
            lines += ["", "**Opportunities to strengthen the system**"]
            lines += [
                f"- {_DISPOSITION_LABEL.get(a['disposition'])} {a['description']}"
                for a in gaps
            ]

    policies = state.get("policies", [])
    if policies:
        cited = ", ".join(f"`{p['id']}`" for p in policies)
        lines += ["", f"**Grounding policies:** {cited}"]

    lines += [
        "",
        "Thank you for reporting this — surfacing it helps protect future patients "
        "and colleagues. This report is ready for review.",
    ]
    return "\n".join(lines)


# Human-readable badges for an action's compliance disposition. Phrased in a
# Just Culture register: they describe what happened in the process, not who was
# at fault, so gaps read as system learning rather than individual blame.
_DISPOSITION_LABEL: dict[str, str] = {
    "done_correctly": "✅ followed as written —",
    "omission": "➖ step not completed —",
    "commission": "⚠️ step done differently than written —",
}

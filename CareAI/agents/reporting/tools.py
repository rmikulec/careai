"""Tools for the reporting agent.

The tools are the agent's only way to touch the world: search and select
policies, consult de-identified precedent, and record grounded report items.
Grounding is enforced here in code, not left to the prompt.
"""

from typing import Literal

from langchain.tools import ToolRuntime, tool
from langchain_core.messages import ToolMessage
from langchain_core.tools import BaseTool
from langgraph.types import Command

from CareAI.agents.reporting.prompts import PHASE_ACTIONS, PHASE_DONE
from CareAI.database.policy import PolicyService
from CareAI.models import ActionDisposition, PolicyLink, ReportInfo

# Mock precedent store. The real past-incident corpus is a separate RAG feature;
# this keeps the reporting agent runnable and deterministic in the meantime.
_INCIDENTS: list[dict] = [
    {
        "id": "INC-204",
        "incident_type": "needlestick",
        "created_at": "2026-08-11",
        "summary": (
            "Sharps injury during disposal; employee seen by Employee Health "
            "within the hour; source patient consented to testing."
        ),
    },
    {
        "id": "INC-187",
        "incident_type": "fall",
        "created_at": "2026-07-02",
        "summary": (
            "Unwitnessed fall in an anticoagulated patient; CT ordered; physician "
            "notified within 30 minutes."
        ),
    },
    {
        "id": "INC-233",
        "incident_type": "medication",
        "created_at": "2026-09-19",
        "summary": (
            "Double dose administered and reached the patient; patient monitored; "
            "no adverse outcome."
        ),
    },
]


def covered_policy_ids(actions: list[dict]) -> set[str]:
    """Return the set of policy ids cited by at least one recorded action.

    Args:
        actions (list[dict]): Recorded actions, each with ``related_policies``.

    Returns:
        set[str]: Every ``policy_id`` cited across the recorded actions. The
        actions stage is complete once this covers every added policy.
    """
    return {
        link["policy_id"]
        for action in actions
        for link in action.get("related_policies", [])
    }


def _validate_links(
    related_policies: list[PolicyLink], state: dict
) -> tuple[list[dict], str | None]:
    """Validate chunk citations against the added grounding set.

    Each citation must name an added policy and a chunk index that exists in it.
    Valid citations are enriched with the chunk's ``section`` and ``content`` so
    the stored report item carries the exact grounding text for review.

    Args:
        related_policies (list[PolicyLink]): Citations supplied by the model.
        state (dict): Current graph state (reads ``policies``).

    Returns:
        tuple[list[dict], Optional[str]]: The citations as dicts (enriched when
        valid), and a rejection message if any id is not an added policy or any
        chunk index does not exist in the cited policy; ``None`` when all valid.
    """
    links = [link.model_dump() for link in related_policies]
    added = {p["id"]: p for p in state.get("policies", [])}

    unknown = [lnk["policy_id"] for lnk in links if lnk["policy_id"] not in added]
    if unknown:
        return links, (
            f"Rejected: policy ids {unknown} have not been added via add_policy. "
            f"Add them first. Added ids so far: {sorted(added) or 'none'}."
        )

    enriched: list[dict] = []
    bad: list[str] = []
    for lnk in links:
        chunks = {
            c["chunk_index"]: c for c in added[lnk["policy_id"]].get("chunks", [])
        }
        chunk = chunks.get(lnk["chunk"])
        if chunk is None:
            valid = sorted(chunks) or "none"
            bad.append(f"{lnk['policy_id']} chunk {lnk['chunk']} (valid: {valid})")
            continue
        enriched.append(
            {**lnk, "section": chunk.get("section"), "content": chunk["content"]}
        )
    if bad:
        return links, (
            f"Rejected: these chunks do not exist in the cited policies: {bad}. "
            f"Cite a chunk index shown in a search_policies result."
        )
    return enriched, None


@tool
def record_report_info(info: ReportInfo, runtime: ToolRuntime) -> Command:
    """
    Record or update the report's header information (what happened, when, where, and who was
    involved). Call this during the initial information gather and whenever new header details
    emerge. Only set the fields you know; the rest stay unchanged.
    """
    data = info.model_dump()
    people = data.pop("people", None) or []
    scalars = {k: v for k, v in data.items() if v is not None}
    update: dict = {}
    if scalars:
        update["report_info"] = scalars
    if people:
        update["people"] = people
    update["messages"] = [
        ToolMessage(
            content=f"Report info updated: {scalars or 'no fields'}; people added: {len(people)}.",
            tool_call_id=runtime.tool_call_id,
        )
    ]
    return Command(update=update)


@tool
def search_incidents(
    query: str,
    incident_types: list[str],
    sort_by: Literal["created_at", "incident_type"],
) -> str:
    """
    Search through past relevant incidents to help guide the questioning. Incidents are all PII
    redacted, and should NEVER be surfaced to the user.
    """
    matches = [i for i in _INCIDENTS if i["incident_type"] in incident_types]
    matches.sort(key=lambda i: i[sort_by])
    if not matches:
        return "No relevant past incidents."
    lines = "\n".join(f"- [{i['incident_type']}] {i['summary']}" for i in matches)
    return (
        "De-identified precedent for question-shaping only; never repeat verbatim to the user:\n"
        + lines
    )


@tool
def record_action(
    action: str,
    disposition: ActionDisposition,
    related_policies: list[PolicyLink],
    runtime: ToolRuntime,
) -> Command:
    """
    Record a policy-required action and whether it was carried out as required. `action` describes
    what the policy called for and what actually happened. `disposition` is one of: "done_correctly"
    (performed as the policy specifies), "omission" (required but not done), or "commission" (done
    incorrectly, or done when it should not have been) — omissions and commissions are procedure
    gaps. Each related policy is a citation: the policy id, the chunk index that grounds it, and a
    reason it applies. Every policy id must have already been added via add_policy, and the chunk
    index must be one shown in a search_policies result for that policy.
    """
    links, error = _validate_links(related_policies, runtime.state)
    if error:
        return Command(
            update={
                "messages": [
                    ToolMessage(content=error, tool_call_id=runtime.tool_call_id)
                ]
            }
        )
    return Command(
        update={
            "actions": [
                {
                    "description": action,
                    "disposition": disposition,
                    "related_policies": links,
                }
            ],
            "messages": [
                ToolMessage(
                    content=f"Recorded action [{disposition}]: {action!r} (policies: {[lnk['policy_id'] for lnk in links]})",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )


@tool
def record_contributing_factor(
    factor: str,
    runtime: ToolRuntime,
    related_policies: list[PolicyLink] | None = None,
) -> Command:
    """
    Record a condition or cause that contributed to the incident (e.g. an overfilled sharps
    container, an interruption, understaffing). Policy citations are OPTIONAL: include a
    PolicyLink only when the factor is a deviation from a specific policy standard. Any cited
    policy must have been added via add_policy, and the cited chunk index must exist in it.
    """
    links, error = _validate_links(related_policies or [], runtime.state)
    if error:
        return Command(
            update={
                "messages": [
                    ToolMessage(content=error, tool_call_id=runtime.tool_call_id)
                ]
            }
        )
    return Command(
        update={
            "factors": [{"description": factor, "related_policies": links}],
            "messages": [
                ToolMessage(
                    content=f"Recorded contributing factor: {factor!r} (policies: {[lnk['policy_id'] for lnk in links]})",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )


@tool
def advance_to_actions(runtime: ToolRuntime) -> Command:
    """
    Signal that contributing-factor gathering is complete and move intake into the actions phase.
    Call this only once you have explored the confounding factors behind the incident. Afterwards
    you will ask, policy by policy, what action each one required and whether it was done.
    """
    return Command(
        update={
            "phase": PHASE_ACTIONS,
            "messages": [
                ToolMessage(
                    content=(
                        "Contributing factors complete. Now in the actions phase: for each added "
                        "policy, ask what action it required and whether it was done, then record "
                        "it with record_action."
                    ),
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )


@tool
def finish_report(runtime: ToolRuntime) -> Command:
    """
    Signal that intake is complete. This is only allowed once EVERY added policy has at least one
    recorded action with a disposition (done_correctly, omission, or commission) — that is the
    definition of a complete intake. If any added policy is still uncovered, this is rejected and
    names the gaps; ask about each and record_action before finishing. On success, a summary of
    the report is shown to the practitioner.
    """
    state = runtime.state
    added = {p["id"] for p in state.get("policies", [])}
    uncovered = sorted(added - covered_policy_ids(state.get("actions", [])))
    if uncovered:
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        content=(
                            f"Not finished: these added policies have no recorded action yet: "
                            f"{uncovered}. For each, ask what it required and whether it was done, "
                            f"then record_action with a disposition before calling finish_report."
                        ),
                        tool_call_id=runtime.tool_call_id,
                    )
                ]
            }
        )
    return Command(
        update={
            "phase": PHASE_DONE,
            "messages": [
                ToolMessage(
                    content="Intake complete.",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )


def build_reporting_tools(policy_service: PolicyService) -> list[BaseTool]:
    """Construct the reporting agent's tools, bound to a policy service.

    The policy search/selection tools close over ``policy_service``; the
    stateless recording tools are shared module-level objects.

    Args:
        policy_service (PolicyService): Retrieval service over the policy corpus.

    Returns:
        list[BaseTool]: Tools to bind to the model and the ``ToolNode``.
    """

    @tool
    async def search_policies(query: str) -> str:
        """
        Search the facility's policy library (vector retrieval) and return candidate policy
        chunks that may be relevant. Read-only: this does not add anything to the report. Each
        result is a specific chunk labelled with its policy id and chunk index — the chunk index
        is what record_action / record_contributing_factor cite. Review the candidates, reason
        about which policies apply, then call add_policy for those ids.
        """
        hits = await policy_service.search(query)
        if not hits:
            return "No candidate policies found."
        return (
            "Candidate policy chunks (cite a chunk as policy_id + chunk index; "
            "call add_policy for the policy ids that apply):\n"
            + "\n".join(
                f"{h['policy_id']} chunk {h['chunk_index']} — {h['title']} "
                f"[{h['section'] or '-'}]: {h['content']}"
                for h in hits
            )
        )

    @tool
    async def add_policy(policy_id: str, runtime: ToolRuntime) -> Command:
        """
        Mark one policy as relevant to this incident and add it to the report's grounding set.
        Only policies added here may be cited by record_action or record_contributing_factor.
        The id must come from a search_policies result. After adding, ask the action it requires.
        """
        pol = await policy_service.get(policy_id)
        if pol is None:
            return Command(
                update={
                    "messages": [
                        ToolMessage(
                            content=f"Rejected: {policy_id!r} is not a known policy id. Use an id from search_policies.",
                            tool_call_id=runtime.tool_call_id,
                        )
                    ]
                }
            )
        chunk_indices = [c["chunk_index"] for c in pol["chunks"]]
        return Command(
            update={
                "policies": [
                    {
                        "id": pol["policy_id"],
                        "title": pol["title"],
                        "chunks": pol["chunks"],
                    }
                ],
                "messages": [
                    ToolMessage(
                        content=(
                            f"Added {pol['policy_id']} — {pol['title']} "
                            f"(chunks {chunk_indices}). Ask the practitioner the "
                            f"action this policy requires, then record_action their answer "
                            f"linked to {pol['policy_id']} and the grounding chunk index."
                        ),
                        tool_call_id=runtime.tool_call_id,
                    )
                ],
            }
        )

    return [
        record_report_info,
        search_policies,
        add_policy,
        search_incidents,
        record_action,
        record_contributing_factor,
        advance_to_actions,
        finish_report,
    ]

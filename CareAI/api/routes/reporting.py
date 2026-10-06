"""HTTP routes for the reporting agent.

Thin endpoints: parse the request, drive the compiled agent by ``thread_id``,
and shape the response. All routes require a valid API key.
"""

import json
import logging
from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel, Field

from CareAI.agents.reporting.prompts import PHASE_DONE
from CareAI.api.dependencies import (
    get_incident_service,
    get_reporting_agent,
    require_api_key,
)
from CareAI.database import IncidentService
from CareAI.models import IncidentReport

logger = logging.getLogger(__name__)

# SSE responses must not be buffered by proxies or cached intermediaries.
_SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
}


def _sse(event: str, data: dict) -> str:
    """Format a single Server-Sent Event frame."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def _extract_messages(update: object) -> list:
    """Pull messages out of a LangGraph ``updates`` value.

    A node's update may be a ``{"messages": [...]}`` dict, or a list of
    ``Command`` objects / messages when its tools return ``Command`` (as the
    tools node does). This normalizes both shapes to a flat message list.
    """
    messages: list = []
    if isinstance(update, dict):
        messages.extend(update.get("messages") or [])
    elif isinstance(update, list):
        for item in update:
            if isinstance(item, dict):
                messages.extend(item.get("messages") or [])
            elif isinstance(getattr(item, "update", None), dict):
                messages.extend(item.update.get("messages") or [])
            elif hasattr(item, "text") or hasattr(item, "content"):
                messages.append(item)
    return messages


def _describe_tool_call(name: str, args: dict) -> str:
    """Render a tool call as a human-readable progress line.

    Args:
        name (str): The tool's name.
        args (dict): The arguments the model passed to the tool.

    Returns:
        str: A short present-tense status, e.g. "Searching policies for '...'".
    """
    if name == "search_policies":
        return f"Searching policies for {args.get('query', '')!r}"
    if name == "add_policy":
        return f"Adding policy {args.get('policy_id', '')}"
    if name == "search_incidents":
        types = ", ".join(args.get("incident_types") or [])
        return (
            f"Reviewing past {types} incidents" if types else "Reviewing past incidents"
        )
    if name == "record_report_info":
        return "Recording the incident details"
    if name == "record_action":
        return "Recording an action taken"
    if name == "record_contributing_factor":
        return "Recording a contributing factor"
    if name == "advance_to_actions":
        return "Moving on to actions taken"
    if name == "finish_report":
        return "Finishing the report"
    return f"Running {name}"


async def _persist_if_done(
    thread_id: str,
    state: dict,
    incident_service: IncidentService,
) -> None:
    """Assemble and store the finalized report once intake reaches ``done``.

    Called after each turn: when the agent has advanced the thread to the
    ``done`` phase, the collected state is assembled into an
    :class:`IncidentReport` and upserted into the incident store. A no-op for
    any earlier phase.

    Args:
        thread_id (str): The reporting thread.
        state (dict): The agent's graph state after the turn.
        incident_service (IncidentService): The finalized-incident store.
    """
    if state.get("phase") != PHASE_DONE:
        return
    report = IncidentReport.from_graph_state(thread_id, state)
    await incident_service.save(thread_id, report)


class MessageRequest(BaseModel):
    """A practitioner message sent to the reporting agent.

    Attributes:
        message (str): The practitioner's free-text message.
    """

    message: str = Field(description="The practitioner's message.")


class MessageResponse(BaseModel):
    """The agent's reply to a practitioner message.

    Attributes:
        thread_id (str): The conversation this reply belongs to.
        reply (str): The agent's plain-text response.
    """

    thread_id: str
    reply: str


class ReportStateResponse(BaseModel):
    """The report items collected so far for a thread.

    Attributes:
        report_info (dict): Gathered header fields.
        people (list[dict]): People involved, with roles.
        policies (list[dict]): Related policies, each with policy_id, title, summary.
        actions (list[dict]): Recorded actions with their citations.
        factors (list[dict]): Recorded contributing factors.
    """

    report_info: dict
    people: list[dict]
    policies: list[dict]
    actions: list[dict]
    factors: list[dict]


class ReportHistoryItem(BaseModel):
    """A finalized report in the history list.

    Attributes:
        thread_id (str): The thread it was assembled from; open it to view.
        report_id (str): The report's own identifier.
        status (str): Lifecycle status at write time.
        incident_type (Optional[str]): Incident type, if captured.
        summary (Optional[str]): One-line summary, if captured.
        updated_at (Optional[str]): ISO timestamp of the last write.
    """

    thread_id: str
    report_id: str
    status: str
    incident_type: str | None = None
    summary: str | None = None
    updated_at: str | None = None


class ChatMessage(BaseModel):
    """One turn of the visible transcript.

    Attributes:
        role (str): ``"user"`` or ``"assistant"``.
        content (str): The message text.
    """

    role: str
    content: str


class ThreadSummary(BaseModel):
    """A reporting thread for the history list (finalized or in progress).

    Attributes:
        thread_id (str): The thread id to resume.
        incident_type (Optional[str]): Incident type, if captured.
        summary (Optional[str]): One-line summary, if captured.
        phase (Optional[str]): Current stage (``basics`` … ``done``).
        updated_at (Optional[str]): ISO timestamp of the latest checkpoint.
    """

    thread_id: str
    incident_type: str | None = None
    summary: str | None = None
    phase: str | None = None
    updated_at: str | None = None


def _policy_summary(policy: dict, limit: int = 240) -> str:
    """Summarize an added policy from its first chunk (usually the purpose)."""
    chunks = policy.get("chunks") or []
    text = " ".join((chunks[0].get("content", "") if chunks else "").split())
    return text[: limit - 1].rstrip() + "…" if len(text) > limit else text


def build_reporting_router() -> APIRouter:
    """Construct the reporting agent's API router.

    Returns:
        APIRouter: Router exposing the intake conversation endpoints, guarded by
        the API-key dependency.
    """
    router = APIRouter(
        prefix="/reporting",
        tags=["reporting"],
        dependencies=[Depends(require_api_key)],
    )

    @router.post("/threads/{thread_id}/messages", response_model=MessageResponse)
    async def post_message(
        thread_id: str,
        body: MessageRequest,
        agent: CompiledStateGraph = Depends(get_reporting_agent),
        incident_service: IncidentService = Depends(get_incident_service),
    ) -> MessageResponse:
        """Send a practitioner message and return the agent's reply.

        If the turn completes intake (phase ``done``), the finalized report is
        assembled from state and stored before the reply is returned.
        """
        config = {"configurable": {"thread_id": thread_id}}
        result = await agent.ainvoke({"messages": [HumanMessage(body.message)]}, config)
        await _persist_if_done(thread_id, result, incident_service)
        return MessageResponse(thread_id=thread_id, reply=result["messages"][-1].text)

    @router.post("/threads/{thread_id}/stream")
    async def stream_message(
        thread_id: str,
        body: MessageRequest,
        agent: CompiledStateGraph = Depends(get_reporting_agent),
        incident_service: IncidentService = Depends(get_incident_service),
    ) -> StreamingResponse:
        """Stream the agent's turn as Server-Sent Events.

        Two kinds of event are emitted. ``status`` events are ephemeral progress
        (policy searches, additions, planning, mid-turn tool calls) meant to be
        shown transiently and replaced by the next — they are NOT part of the
        saved reply. ``token`` events are the actual assistant message (the
        question or summary) and are the only thing persisted client-side. A
        final ``done`` event closes the turn.

        Backstage stages are never voiced: the policy-discovery and plan-drafting
        prose stay internal (only their tool activity surfaces as status), and
        the intake-extraction call is silent.
        """
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [HumanMessage(body.message)]}

        # Stages whose streamed LLM text IS the assistant's reply to persist.
        answer_token_nodes = {"factors", "actions"}
        # Stages that emit a ready-made reply message (no token streaming).
        answer_message_nodes = {"ask_basics", "wrap_up"}
        # Stages whose tool calls surface as transient status lines.
        status_tool_nodes = {"discover", "factors", "actions"}

        async def events() -> AsyncIterator[str]:
            async for mode, chunk in agent.astream(
                inputs, config, stream_mode=["messages", "updates"]
            ):
                if mode == "messages":
                    message_chunk, meta = chunk
                    node = meta.get("langgraph_node")
                    if node in answer_token_nodes and message_chunk.text:
                        yield _sse("token", {"text": message_chunk.text})
                    continue
                for node, update in chunk.items():
                    messages = _extract_messages(update)
                    if node == "plan":
                        # The plan itself stays internal; show only that work is
                        # happening.
                        yield _sse(
                            "status",
                            {"text": "Reviewing the policies and planning what to ask"},
                        )
                    elif node in status_tool_nodes:
                        # Tool calls become transient status lines; the discovery
                        # narration prose is intentionally not surfaced.
                        for message in messages:
                            for call in getattr(message, "tool_calls", None) or []:
                                yield _sse(
                                    "status",
                                    {
                                        "text": _describe_tool_call(
                                            call["name"], call["args"]
                                        )
                                    },
                                )
                    elif node in answer_message_nodes and messages:
                        yield _sse("token", {"text": messages[-1].text})
            # Once the stream ends, persist the finalized report if the turn
            # completed intake. Read the settled state from the checkpointer.
            snapshot = await agent.aget_state(config)
            await _persist_if_done(thread_id, snapshot.values, incident_service)
            yield _sse("done", {"thread_id": thread_id})

        return StreamingResponse(
            events(), media_type="text/event-stream", headers=_SSE_HEADERS
        )

    @router.get("/threads/{thread_id}", response_model=ReportStateResponse)
    async def get_thread_state(
        thread_id: str,
        agent: CompiledStateGraph = Depends(get_reporting_agent),
    ) -> ReportStateResponse:
        """Return the report items collected so far for a thread.

        Raises:
            HTTPException: 404 if the thread has no stored state yet.
        """
        snapshot = await agent.aget_state({"configurable": {"thread_id": thread_id}})
        values = snapshot.values
        if not values:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No reporting thread {thread_id!r}",
            )
        return ReportStateResponse(
            report_info=values.get("report_info", {}),
            people=values.get("people", []),
            policies=[
                {
                    "policy_id": p["id"],
                    "title": p["title"],
                    "summary": _policy_summary(p),
                }
                for p in values.get("policies", [])
            ],
            actions=values.get("actions", []),
            factors=values.get("factors", []),
        )

    @router.get("/threads/{thread_id}/report", response_model=IncidentReport)
    async def get_thread_report(
        thread_id: str,
        incident_service: IncidentService = Depends(get_incident_service),
    ) -> IncidentReport:
        """Return the finalized incident report stored for a thread.

        The report is written automatically once a thread's intake reaches the
        ``done`` phase; until then this returns 404.

        Raises:
            HTTPException: 404 if the thread has no finalized report yet.
        """
        report = await incident_service.get(thread_id)
        if report is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No finalized report for thread {thread_id!r}",
            )
        return report

    @router.get("/reports", response_model=list[ReportHistoryItem])
    async def list_reports(
        incident_service: IncidentService = Depends(get_incident_service),
    ) -> list[ReportHistoryItem]:
        """List finalized incident reports, most recently updated first."""
        return [ReportHistoryItem(**item) for item in await incident_service.list()]

    @router.get("/threads", response_model=list[ThreadSummary])
    async def list_threads(
        agent: CompiledStateGraph = Depends(get_reporting_agent),
    ) -> list[ThreadSummary]:
        """List every reporting thread, newest first, finalized or in progress.

        Reads the LangGraph checkpointer (not just the finalized-report table) so
        any conversation can be resumed. The first checkpoint seen per thread is
        its latest, since the checkpointer lists newest-first.
        """
        latest: dict[str, ThreadSummary] = {}
        try:
            async for ct in agent.checkpointer.alist(None):
                thread_id = ct.config["configurable"]["thread_id"]
                if thread_id in latest:
                    continue
                values = ct.checkpoint.get("channel_values", {})
                info = values.get("report_info") or {}
                latest[thread_id] = ThreadSummary(
                    thread_id=thread_id,
                    incident_type=info.get("incident_type"),
                    summary=info.get("summary"),
                    phase=values.get("phase"),
                    updated_at=ct.checkpoint.get("ts"),
                )
        except Exception:
            logger.exception("Failed to list checkpointer threads")
        return list(latest.values())

    @router.get("/threads/{thread_id}/messages", response_model=list[ChatMessage])
    async def get_thread_messages(
        thread_id: str,
        agent: CompiledStateGraph = Depends(get_reporting_agent),
    ) -> list[ChatMessage]:
        """Return the visible transcript so a thread can be reopened and continued.

        Only user messages and the assistant's spoken replies are included; tool
        calls and tool results are filtered out.
        """
        snapshot = await agent.aget_state({"configurable": {"thread_id": thread_id}})
        transcript: list[ChatMessage] = []
        for message in snapshot.values.get("messages", []):
            kind = getattr(message, "type", "")
            text = (getattr(message, "text", "") or "").strip()
            if kind == "human" and text:
                transcript.append(ChatMessage(role="user", content=text))
            elif kind == "ai" and text:
                transcript.append(ChatMessage(role="assistant", content=text))
        return transcript

    return router

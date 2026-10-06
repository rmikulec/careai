"""Streamlit chat UI for the CareAI incident reporting agent.

A thin client: it POSTs practitioner messages to the API's reporting endpoints,
streams the agent's reply via Server-Sent Events, and renders the report items
collected so far alongside the conversation. Once a thread finalizes, it surfaces
the escalation agent's policy-grounded severity (level, rationale, and source
citations) as a banner above the report, followed by the notifications it drafted
(a collapsible list). It imports nothing from the agent or the database — all
state lives server-side, keyed by the ``thread_id`` held in the Streamlit
session.

Run with ``streamlit run CareAI/ui/streamlit_app.py`` (or ``uv run task ui``).
Configuration comes from the shared settings tree (:mod:`CareAI.config`):

- ``CAREAI_API_URL`` — base URL of the API (default ``http://localhost:8000``).
- ``CAREAI_API_KEY`` — value sent as the ``X-API-Key`` header.
"""

import json
import uuid
from collections.abc import Iterator

import httpx
import streamlit as st

from CareAI.config import get_settings

_settings = get_settings()
_API_URL = _settings.careai_api_url.rstrip("/")
_API_KEY = _settings.careai_api_key
_HEADERS = {"X-API-Key": _API_KEY}

# No read timeout: a single agent turn can take a while to stream. Connect/write
# stay bounded so a dead API surfaces quickly rather than hanging the UI.
_TIMEOUT = httpx.Timeout(connect=10.0, read=None, write=10.0, pool=10.0)

# Colored labels for an action's compliance disposition (Streamlit markdown
# color syntax), and a sort order that surfaces the procedure gaps first.
# Non-punitive badges: gaps are surfaced plainly (not hidden), but worded as
# process events rather than individual fault, in keeping with Just Culture.
_DISPOSITION_LABEL = {
    "done_correctly": ":green[Followed as written]",
    "omission": ":orange[Step not completed]",
    "commission": ":orange[Done differently than written]",
}
_DISPOSITION_ORDER = {"omission": 0, "commission": 1, "done_correctly": 2}


def _new_thread_id() -> str:
    """Return a fresh conversation id."""
    return f"ui-{uuid.uuid4().hex[:12]}"


def _reporting_url(thread_id: str, suffix: str = "") -> str:
    """Build a reporting endpoint URL for a thread."""
    return f"{_API_URL}/api/v1/reporting/threads/{thread_id}{suffix}"


def _iter_sse(response: httpx.Response) -> Iterator[tuple[str, dict]]:
    """Yield ``(event, data)`` pairs from an SSE response stream.

    Args:
        response (httpx.Response): An open streaming response whose body is a
            ``text/event-stream`` of ``event:``/``data:`` line pairs.

    Yields:
        tuple[str, dict]: The event name and its decoded JSON payload.
    """
    event = "message"
    for line in response.iter_lines():
        if not line:
            event = "message"  # blank line terminates a frame
            continue
        if line.startswith("event:"):
            event = line[len("event:") :].strip()
        elif line.startswith("data:"):
            yield event, json.loads(line[len("data:") :].strip())


def _stream_turn(thread_id: str, message: str, status_box, text_box) -> tuple[str, str]:
    """Send a message and stream the agent's turn into two placeholders.

    ``status`` events are transient progress (``Searching policies for '...'``,
    planning, mid-turn tools). Each replaces the previous in ``status_box`` and
    is cleared when the turn ends. ``token`` events are the actual reply and
    stream into ``text_box`` — they are the only thing worth persisting.

    Args:
        thread_id (str): The conversation to append to.
        message (str): The practitioner's message.
        status_box: A Streamlit container showing the latest transient status.
        text_box: A Streamlit container updated with the reply as it streams.

    Returns:
        tuple[str, str]: The full reply text and the last status line shown.

    Raises:
        httpx.HTTPStatusError: If the API returns a non-2xx status.
        httpx.RequestError: If the API is unreachable.
    """
    parts: list[str] = []
    latest_status = ""
    with httpx.Client(timeout=_TIMEOUT) as client:
        with client.stream(
            "POST",
            _reporting_url(thread_id, "/stream"),
            headers=_HEADERS,
            json={"message": message},
        ) as response:
            response.raise_for_status()
            for event, data in _iter_sse(response):
                if event == "token":
                    parts.append(data.get("text", ""))
                    text_box.markdown("".join(parts))
                elif event == "status":
                    line = data.get("text", "")
                    if line:
                        latest_status = line
                        status_box.markdown(f"_{line}…_")
    return "".join(parts), latest_status


def _fetch_report(thread_id: str) -> dict | None:
    """Fetch the report items collected so far, or ``None`` if none yet.

    Args:
        thread_id (str): The conversation to inspect.

    Returns:
        Optional[dict]: The report-state payload, or ``None`` if the thread has
        no stored state (HTTP 404) or the API is unreachable.
    """
    try:
        response = httpx.get(_reporting_url(thread_id), headers=_HEADERS, timeout=10.0)
    except httpx.RequestError:
        return None
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def _fetch_finalized_report(thread_id: str) -> dict | None:
    """Fetch the finalized report (with severity/escalation), or ``None``.

    The finalized :class:`IncidentReport` is written once intake reaches the
    ``done`` phase and then enriched with the escalation agent's severity
    assessment. Returns ``None`` while the thread is still in progress (HTTP 404)
    or the API is unreachable.

    Args:
        thread_id (str): The conversation to inspect.

    Returns:
        Optional[dict]: The finalized report payload, or ``None`` if not yet
        finalized / unreachable.
    """
    try:
        response = httpx.get(
            _reporting_url(thread_id, "/report"), headers=_HEADERS, timeout=10.0
        )
    except httpx.RequestError:
        return None
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def _fetch_notifications(thread_id: str) -> list[dict]:
    """Fetch the notifications drafted for a thread's finalized report.

    Args:
        thread_id (str): The conversation to inspect.

    Returns:
        list[dict]: Queued notification rows (newest first), or an empty list if
        none were drafted or the API is unreachable.
    """
    try:
        response = httpx.get(
            _reporting_url(thread_id, "/notifications"),
            headers=_HEADERS,
            timeout=10.0,
        )
    except httpx.RequestError:
        return []
    if response.status_code != 200:
        return []
    return response.json()


def _fetch_threads() -> list[dict]:
    """Fetch every reporting thread (finalized or in progress), newest first.

    Returns:
        list[dict]: Thread rows (``thread_id``, ``incident_type``, ``summary``,
        ``phase``, ``updated_at``), or an empty list if the API is unreachable.
    """
    try:
        response = httpx.get(
            f"{_API_URL}/api/v1/reporting/threads", headers=_HEADERS, timeout=10.0
        )
    except httpx.RequestError:
        return []
    if response.status_code != 200:
        return []
    return response.json()


def _fetch_messages(thread_id: str) -> list[dict]:
    """Fetch a thread's visible transcript so it can be reopened and continued.

    Args:
        thread_id (str): The conversation to restore.

    Returns:
        list[dict]: ``{role, content}`` turns, or an empty list if unavailable.
    """
    try:
        response = httpx.get(
            _reporting_url(thread_id, "/messages"), headers=_HEADERS, timeout=10.0
        )
    except httpx.RequestError:
        return []
    if response.status_code != 200:
        return []
    return response.json()


def _render_policy_links(links: list[dict]) -> None:
    """Render an item's policy chunk citations in a collapsed expander."""
    if not links:
        return
    label = f"{len(links)} policy citation" + ("" if len(links) == 1 else "s")
    with st.expander(label, expanded=False):
        for link in links:
            st.caption(
                f"**{link.get('policy_id', '?')}** · chunk {link.get('chunk', '?')} "
                f"— {link.get('reason', '')}"
            )
            content = link.get("content")
            if content:
                st.caption(f"> {content}")


def _severity_tone(severity: str | None) -> tuple[str, str]:
    """Pick a Streamlit alert tone + icon for a policy-defined severity label.

    Heuristic only: the severity *scale* belongs to the facility's policies, so
    this keys off common cues (sentinel/catastrophic/level-1 = most urgent) and
    degrades to an informational tone for anything it doesn't recognize. An
    unknown/undetermined severity is treated as "needs attention".

    Args:
        severity (Optional[str]): The policy's own severity label (e.g. "SEV-2"),
            or ``None`` when the policies defined no applicable criteria.

    Returns:
        tuple[str, str]: The alert tone (``error``/``warning``/``info``) and an
        icon to show beside it.
    """
    if not severity:
        return "warning", "⚠️"
    text = severity.lower()
    if any(k in text for k in ("sev-1", "sev 1", "catastroph", "sentinel", "death")):
        return "error", "🚨"
    if any(k in text for k in ("sev-2", "sev 2", "major", "severe")):
        return "warning", "⚠️"
    return "info", "ℹ️"


def _render_drafted_notifications(notifications: list[dict]) -> None:
    """Render the escalation agent's drafted notifications as a collapsible list.

    Shown within the severity section once a report is finalized and assessed.
    Each notification is its own expander (recipient + subject in the label); the
    channel, status, body, and policy citations are inside. A caption explains the
    empty case — the severity warranted no notification — so the absence reads as
    a decision, not a gap.

    Args:
        notifications (list[dict]): Queued notification rows for the report.
    """
    st.markdown("**Drafted notifications**")
    if not notifications:
        st.caption("No notifications were drafted at this severity.")
        return
    for note in notifications:
        recipient = note.get("recipient", "?")
        subject = note.get("subject", "")
        with st.expander(f"{recipient} · {subject}", expanded=False):
            meta = " · ".join(
                part for part in (note.get("channel"), note.get("status")) if part
            )
            if meta:
                st.caption(meta)
            body = note.get("body")
            if body:
                st.write(body)
            _render_policy_links(note.get("related_policies") or [])


def _render_severity(finalized: dict | None, notifications: list[dict]) -> None:
    """Render the policy-grounded severity banner for a finalized report.

    No-op until the thread is finalized and the escalation agent has run (so
    nothing shows mid-intake, and nothing shows if the assessment failed). When it
    has run, the drafted notifications are listed beneath the rationale/citations.

    Args:
        finalized (Optional[dict]): The finalized report payload (with
            ``escalation``), or ``None`` while the thread is in progress.
        notifications (list[dict]): Notifications drafted for the report.
    """
    escalation = (finalized or {}).get("escalation") or {}
    if not escalation:
        return
    severity = (finalized or {}).get("severity") or escalation.get("severity")
    tone, icon = _severity_tone(severity)
    banner = {"error": st.error, "warning": st.warning, "info": st.info}[tone]
    if severity:
        banner(f"Severity: {severity}", icon=icon)
    else:
        banner(
            "Severity not determined from the linked policies — flagged for "
            "human triage.",
            icon=icon,
        )

    rationale = escalation.get("rationale")
    if rationale:
        st.caption(rationale)

    sources = escalation.get("sources") or []
    if sources:
        label = f"{len(sources)} policy citation" + ("" if len(sources) == 1 else "s")
        with st.expander(f"Why this severity · {label}", expanded=False):
            for src in sources:
                st.caption(
                    f"**{src.get('policy_id', '?')}** · chunk "
                    f"{src.get('chunk', '?')} — {src.get('reason', '')}"
                )

    _render_drafted_notifications(notifications)
    st.divider()


def _render_report(report: dict | None) -> None:
    """Render the collected report as a full-width, structured view."""
    report = report or {}
    info = report.get("report_info") or {}
    people = report.get("people") or []
    actions = report.get("actions") or []
    factors = report.get("factors") or []
    policies = report.get("policies") or []

    if not any([info, people, actions, factors, policies]):
        st.info(
            "Nothing collected yet — start the conversation on the left. "
            "Share what happened in your own words; we'll work through it together."
        )
        return

    title = (info.get("incident_type") or "Incident").strip().capitalize()
    st.subheader(f"{title} report")
    if info.get("summary"):
        st.write(info["summary"])

    facts = st.columns(3)
    facts[0].markdown(f"**When**  \n{info.get('occurred_at') or '—'}")
    facts[1].markdown(f"**Where**  \n{info.get('location') or '—'}")
    facts[2].markdown(f"**Type**  \n{info.get('incident_type') or '—'}")

    gaps = sum(1 for a in actions if a.get("disposition") in ("omission", "commission"))
    metrics = st.columns(4)
    metrics[0].metric("Policies", len(policies))
    metrics[1].metric("Actions", len(actions))
    metrics[2].metric("Factors", len(factors))
    metrics[3].metric("To address", gaps)

    st.divider()

    if actions:
        st.markdown("#### Actions assessed")
        ordered = sorted(
            actions,
            key=lambda a: _DISPOSITION_ORDER.get(a.get("disposition"), 3),
        )
        for action in ordered:
            with st.container(border=True):
                label = _DISPOSITION_LABEL.get(action.get("disposition"), "")
                st.markdown(f"{label}  \n{action.get('description', '')}".strip())
                _render_policy_links(action.get("related_policies") or [])

    if factors:
        st.markdown("#### Contributing factors")
        for factor in factors:
            with st.container(border=True):
                st.markdown(factor.get("description", ""))
                _render_policy_links(factor.get("related_policies") or [])

    if people:
        st.markdown("#### People involved")
        for person in people:
            st.markdown(f"- {person.get('name', '?')} — *{person.get('role', '?')}*")

    if policies:
        st.markdown("#### Related policies")
        for policy in policies:
            label = f"{policy.get('policy_id', '?')} — {policy.get('title', '')}"
            with st.expander(label, expanded=False):
                st.write(policy.get("summary") or "No summary available.")

    st.divider()
    st.download_button(
        "Download report (JSON)",
        data=json.dumps(report, indent=2),
        file_name=f"{st.session_state.thread_id}.json",
        mime="application/json",
        use_container_width=True,
    )


def _open_thread(thread_id: str, restore: bool = True) -> None:
    """Switch the UI to a thread, restoring its transcript so it can continue.

    Args:
        thread_id (str): The thread to open.
        restore (bool): Reload the server-side transcript (``True`` for existing
            threads; ``False`` for a brand-new one).
    """
    st.session_state.thread_id = thread_id
    st.session_state.messages = _fetch_messages(thread_id) if restore else []
    st.rerun()


def _render_sidebar() -> None:
    """Render thread controls and the clickable, resumable report history."""
    with st.sidebar:
        if st.button("New report", use_container_width=True):
            _open_thread(_new_thread_id(), restore=False)
        st.caption(f"Current: `{st.session_state.thread_id}`")
        st.divider()

        st.subheader("Report history")
        threads = _fetch_threads()
        if not threads:
            st.caption("No reports yet.")
            return
        for item in threads:
            label = (item.get("incident_type") or "Incident").capitalize()
            phase = item.get("phase") or "new"
            stage = "done" if phase == "done" else "in progress"
            if st.button(
                f"{label} · {stage}",
                key=f"thread-{item['thread_id']}",
                use_container_width=True,
                help=item.get("summary") or None,
            ):
                _open_thread(item["thread_id"])


def _run_turn(prompt: str) -> None:
    """Append the user message, stream the assistant reply, and persist it."""
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status_box = st.empty()
        text_box = st.empty()
        try:
            reply, _ = _stream_turn(
                st.session_state.thread_id, prompt, status_box, text_box
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                text_box.error("Unauthorized — check CAREAI_API_KEY.")
            else:
                text_box.error(f"API error: {exc.response.status_code}")
            return
        except httpx.RequestError:
            text_box.error(f"Could not reach the API at {_API_URL}.")
            return
        # Progress lines were transient; the saved transcript keeps only the reply.
        status_box.empty()

    st.session_state.messages.append({"role": "assistant", "content": reply})


_PANEL_HEIGHT = 600


def main() -> None:
    """Chat and report as independent, side-by-side scrolling panels."""
    st.set_page_config(page_title="CareAI — Incident Reporting", layout="wide")
    # Trim the default top/side whitespace and tighten the gap between panels.
    st.markdown(
        "<style>.block-container{padding:1.5rem 1.5rem 2rem;}</style>",
        unsafe_allow_html=True,
    )

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = _new_thread_id()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_col, report_col = st.columns(2, gap="small")

    with chat_col:
        st.subheader("Conversation")
        # Establish psychological safety up front: set a blameless, non-punitive
        # tone before the practitioner types their first word.
        st.caption(
            "This is a blameless, non-punitive report. The goal is to understand "
            "what happened and why — to improve the workflow, not to assign blame."
        )
        # A bounded container is its own scroll region, so the chat scrolls
        # independently of the report and the input stays put beneath it.
        history = st.container(height=_PANEL_HEIGHT)
        with history:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            pending = st.session_state.pop("pending", None)
            if pending:
                _run_turn(pending)
        # Inline (not main-body) input: pinned under the chat column, full width
        # of that column only. Deferred via a rerun so the turn renders above it.
        if prompt := st.chat_input(
            "e.g. I got a needlestick while disposing of sharps"
        ):
            st.session_state.pending = prompt
            st.rerun()

    _render_sidebar()

    # Fetched after the turn so the right panel reflects this turn's items. The
    # finalized report (with the escalation agent's severity) exists only once
    # intake is done; until then it is None and the severity banner stays hidden.
    report = _fetch_report(st.session_state.thread_id)
    finalized = _fetch_finalized_report(st.session_state.thread_id)
    # Notifications exist only post-finalization; skip the call while in progress.
    notifications = (
        _fetch_notifications(st.session_state.thread_id) if finalized else []
    )

    with report_col:
        st.subheader("Report")
        with st.container(height=_PANEL_HEIGHT):
            _render_severity(finalized, notifications)
            _render_report(report)


if __name__ == "__main__":
    main()

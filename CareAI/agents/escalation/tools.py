"""Tools for the escalation agent.

``draft_notification`` is the model-facing contract for drafting a notification.
The escalation agent binds it so the model can propose, per recipient, the
message the policies require at the assessed severity. The ``notify`` node reads
those proposed calls and writes each to the notifications queue — stamping the
report id and severity from state — so the model never has to supply (or be
trusted with) those system-set values.
"""

from langchain.tools import tool
from langchain_core.tools import BaseTool

from CareAI.models import Notification

# The name the model calls and the node matches on when draining tool calls.
DRAFT_NOTIFICATION = "draft_notification"


def build_escalation_tools() -> list[BaseTool]:
    """Construct the escalation agent's tools.

    Returns:
        list[BaseTool]: Tools to bind to the model. The queue write itself is
        performed by the ``notify`` node (which holds the report id and
        severity), so the tool carries only the model-facing schema.
    """

    @tool
    async def draft_notification(notification: Notification) -> str:
        """
        Draft one notification and queue it for delivery. Call this once per recipient the policies
        require to be notified at the assessed severity (e.g. Risk Management for a sentinel event,
        the on-call Nursing Supervisor, Employee Health). `notification` carries the recipient (a
        role or team, never a named person), the channel, a subject, the message body, and the
        policy chunk citations that require the notification. The report id and severity are attached
        automatically from the assessment — do not include them. If the severity warrants no
        notification, do not call this tool.
        """
        return f"Drafted notification to {notification.recipient}."

    return [draft_notification]

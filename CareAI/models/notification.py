"""Wire model for a drafted escalation notification.

After the escalation agent assesses an incident's severity, it may draft one or
more notifications for the people the facility's policies say must be informed.
This model is what the ``draft_notification`` tool produces and what the
notifications queue stores alongside system-set fields (the report id, the
severity that drove the draft, and the queue status).
"""

from typing import Literal

from pydantic import BaseModel, Field

from CareAI.models.incident_report import PolicyLink

# How a drafted notification would be delivered. The queue is not wired to any
# real transport in this demo; the channel is recorded for the eventual sender.
NotificationChannel = Literal["email", "page", "sms", "in_app"]


class Notification(BaseModel):
    """A single notification drafted for a severity-assessed incident.

    Attributes:
        recipient (str): Who must be notified — a role or team as the policy
            names them (e.g. "Risk Management", "Nursing Supervisor", "Employee
            Health"), never an individual's identity.
        channel (NotificationChannel): How it would be delivered.
        subject (str): Short subject line.
        body (str): The notification message.
        related_policies (list[PolicyLink]): Citations to the policy chunk(s)
            that require this notification (typically a "Severity & Reporting"
            section naming who to notify and by when).
    """

    recipient: str = Field(
        description="Role or team to notify, as the policy names them."
    )
    channel: NotificationChannel = Field(
        description="How the notification would be delivered."
    )
    subject: str = Field(description="Short subject line.")
    body: str = Field(description="The notification message.")
    related_policies: list[PolicyLink] = Field(
        default_factory=list,
        description="Policy chunk citations that require this notification.",
    )

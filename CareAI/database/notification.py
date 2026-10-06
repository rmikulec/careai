"""Notifications queue: the ``notifications`` table and its service.

An append-only queue of notifications drafted by the escalation agent once a
report has been severity-assessed. In this demo nothing consumes the queue —
each row is written with status ``queued`` and left for a future delivery
worker. One row per drafted notification.
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column

from CareAI.database.base import Base
from CareAI.database.session import Session
from CareAI.models import Notification


class NotificationRecord(Base):
    """One queued notification drafted for a finalized incident.

    Attributes:
        id (int): Surrogate primary key.
        report_id (str): The incident report this notification concerns; indexed.
        severity (Optional[str]): The severity label that drove the draft, or
            ``None`` when the incident had no policy-defined severity.
        recipient (str): Role or team to notify.
        channel (str): Delivery channel (``email`` / ``page`` / ``sms`` /
            ``in_app``).
        subject (str): Subject line.
        body (str): Notification message.
        related_policies (list): Policy chunk citations grounding the
            notification (``PolicyLink`` dicts).
        status (str): Queue status; always ``queued`` in this demo (nothing
            consumes the queue yet).
        created_at (datetime): When the row was written.
    """

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_id: Mapped[str] = mapped_column(String, index=True)
    severity: Mapped[str | None] = mapped_column(String, nullable=True)
    recipient: Mapped[str] = mapped_column(String)
    channel: Mapped[str] = mapped_column(String)
    subject: Mapped[str] = mapped_column(String)
    body: Mapped[str] = mapped_column(Text)
    related_policies: Mapped[list] = mapped_column(JSONB, default=list)
    status: Mapped[str] = mapped_column(String, default="queued")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class NotificationService:
    """Append to and read from the notifications queue.

    Args:
        session_maker: Async session factory bound to the application database.
    """

    def __init__(self, session_maker: async_sessionmaker = Session) -> None:
        self._sessions = session_maker

    async def enqueue(
        self,
        report_id: str,
        severity: str | None,
        notification: Notification,
    ) -> NotificationRecord:
        """Queue one drafted notification for a report.

        Args:
            report_id (str): The incident report the notification concerns.
            severity (Optional[str]): The severity label that drove the draft.
            notification (Notification): The drafted notification to store.

        Returns:
            NotificationRecord: The stored row, with status ``queued``.
        """
        record = NotificationRecord(
            report_id=report_id,
            severity=severity,
            recipient=notification.recipient,
            channel=notification.channel,
            subject=notification.subject,
            body=notification.body,
            related_policies=[
                link.model_dump() for link in notification.related_policies
            ],
            status="queued",
        )
        async with self._sessions() as session:
            session.add(record)
            await session.commit()
            await session.refresh(record)
        return record

    async def list(self, report_id: str | None = None, limit: int = 100) -> list[dict]:
        """Return queued notifications, newest first.

        Args:
            report_id (Optional[str]): Restrict to one report when given.
            limit (int): Maximum number of rows to return.

        Returns:
            list[dict]: One dict per queued notification.
        """
        stmt = (
            select(NotificationRecord)
            .order_by(NotificationRecord.created_at.desc())
            .limit(limit)
        )
        if report_id is not None:
            stmt = stmt.where(NotificationRecord.report_id == report_id)
        async with self._sessions() as session:
            rows = (await session.execute(stmt)).scalars().all()
        return [
            {
                "id": r.id,
                "report_id": r.report_id,
                "severity": r.severity,
                "recipient": r.recipient,
                "channel": r.channel,
                "subject": r.subject,
                "body": r.body,
                "related_policies": r.related_policies,
                "status": r.status,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]

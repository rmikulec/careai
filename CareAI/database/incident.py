"""Finalized incident store: the ``incident_reports`` table and its service.

Where the reporting agent's *conversation* state lives in the LangGraph
checkpointer (``checkpoints*`` tables, keyed by ``thread_id``), this table holds
the *finalized* artifact — the assembled :class:`IncidentReport` as a single
JSONB document, written once a thread's intake reaches the ``done`` phase. One
row per thread, upserted so re-finalizing a thread overwrites in place.
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, func, select
from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column

from CareAI.database.base import Base
from CareAI.database.session import Session
from CareAI.models import IncidentReport


class IncidentRecord(Base):
    """One finalized incident report, stored as a JSONB document.

    Attributes:
        id (int): Surrogate primary key.
        thread_id (str): The reporting thread this report was assembled from;
            unique, so each thread has at most one finalized report.
        report_id (str): The report's own identifier (mirrors
            ``report["report_id"]`` for convenient lookup).
        status (str): The report's lifecycle status at write time
            (``collecting`` / ``partial`` / ``complete``).
        report (dict): The full :class:`IncidentReport` as a JSON document.
        created_at (datetime): When the row was first written.
        updated_at (datetime): When the row was last upserted.
    """

    __tablename__ = "incident_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    thread_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    report_id: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[str] = mapped_column(String)
    report: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class IncidentService:
    """Read/write access to finalized incident reports.

    Args:
        session_maker: Async session factory bound to the application database.
    """

    def __init__(self, session_maker: async_sessionmaker = Session) -> None:
        self._sessions = session_maker

    async def save(self, thread_id: str, report: IncidentReport) -> IncidentReport:
        """Upsert a finalized report for a thread.

        A single row per ``thread_id``: a subsequent save for the same thread
        overwrites the stored document and refreshes ``updated_at``.

        Args:
            thread_id (str): The reporting thread the report was assembled from.
            report (IncidentReport): The assembled report to persist.

        Returns:
            IncidentReport: The report as stored (returned unchanged for caller
            convenience).
        """
        payload = report.model_dump(mode="json")
        stmt = (
            insert(IncidentRecord)
            .values(
                thread_id=thread_id,
                report_id=report.report_id,
                status=report.status,
                report=payload,
            )
            .on_conflict_do_update(
                index_elements=[IncidentRecord.thread_id],
                set_={
                    "report_id": report.report_id,
                    "status": report.status,
                    "report": payload,
                    "updated_at": datetime.now(timezone.utc),
                },
            )
        )
        async with self._sessions() as session:
            await session.execute(stmt)
            await session.commit()
        return report

    async def list(self, limit: int = 100) -> list[dict]:
        """Return finalized reports as history rows, most recent first.

        Args:
            limit (int): Maximum number of rows to return.

        Returns:
            list[dict]: One dict per report with ``thread_id``, ``report_id``,
            ``status``, ``severity``, ``incident_type``, ``summary``, and
            ``updated_at`` (ISO string) — enough to list and open a past report.
        """
        stmt = (
            select(
                IncidentRecord.thread_id,
                IncidentRecord.report_id,
                IncidentRecord.status,
                IncidentRecord.report,
                IncidentRecord.updated_at,
            )
            .order_by(IncidentRecord.updated_at.desc())
            .limit(limit)
        )
        async with self._sessions() as session:
            rows = (await session.execute(stmt)).all()
        history: list[dict] = []
        for row in rows:
            report = row.report or {}
            history.append(
                {
                    "thread_id": row.thread_id,
                    "report_id": row.report_id,
                    "status": row.status,
                    "severity": report.get("severity"),
                    "incident_type": report.get("incident_type"),
                    "summary": report.get("summary"),
                    "updated_at": (
                        row.updated_at.isoformat() if row.updated_at else None
                    ),
                }
            )
        return history

    async def get(self, thread_id: str) -> IncidentReport | None:
        """Return the finalized report for a thread, if one has been written.

        Args:
            thread_id (str): The reporting thread to look up.

        Returns:
            Optional[IncidentReport]: The stored report, or ``None`` if the
            thread has no finalized report yet.
        """
        stmt = select(IncidentRecord.report).where(
            IncidentRecord.thread_id == thread_id
        )
        async with self._sessions() as session:
            row = (await session.execute(stmt)).scalar_one_or_none()
        if row is None:
            return None
        return IncidentReport.model_validate(row)

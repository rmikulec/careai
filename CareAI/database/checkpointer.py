"""Postgres-backed LangGraph checkpointer setup.

The reporting agent's multi-turn graph state (messages, phase, recorded items)
is persisted by LangGraph's ``AsyncPostgresSaver``, which runs over psycopg (v3)
— a connection pool separate from the asyncpg/SQLAlchemy pool used for the policy
and incident tables. This module owns converting the shared ``DATABASE_URL`` into
a psycopg DSN and opening/closing that pool over the application's lifespan.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

from CareAI.database.session import DATABASE_URL


def _psycopg_dsn(url: str = DATABASE_URL) -> str:
    """Convert a SQLAlchemy async URL to a psycopg DSN.

    SQLAlchemy addresses Postgres as ``postgresql+asyncpg://...``; psycopg wants
    the bare ``postgresql://...`` scheme, so any ``+<driver>`` suffix on the
    scheme is stripped.

    Args:
        url (str): The SQLAlchemy connection URL.

    Returns:
        str: The equivalent psycopg DSN.
    """
    scheme, sep, rest = url.partition("://")
    base = scheme.split("+", 1)[0]
    return f"{base}{sep}{rest}" if sep else url


@asynccontextmanager
async def open_checkpointer() -> AsyncIterator[AsyncPostgresSaver]:
    """Open a Postgres checkpointer and its connection pool for the app lifespan.

    The pool is opened on entry and closed on exit; ``setup()`` ensures the
    checkpoint tables exist (idempotent).

    Yields:
        AsyncPostgresSaver: A ready saver backed by an open connection pool.
    """
    # autocommit is required for the DDL that AsyncPostgresSaver.setup() issues.
    async with AsyncConnectionPool(
        conninfo=_psycopg_dsn(),
        max_size=10,
        open=False,
        kwargs={"autocommit": True},
    ) as pool:
        saver = AsyncPostgresSaver(pool)
        await saver.setup()
        yield saver

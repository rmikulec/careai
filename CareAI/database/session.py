"""Async database engine, session factory, and schema helper.

The connection URL comes from the typed settings tree (``Settings.database_url``,
sourced from ``DATABASE_URL``), with a fallback to the local docker-compose
Postgres so the package runs with no config. ``DATABASE_URL`` is re-exported here
for the psycopg checkpointer, which derives its DSN from the same value.

FUTURE: use Alembic instead of ``create_all`` for production migrations.
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from CareAI.config import get_settings

DATABASE_URL = get_settings().database_url

engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_all() -> None:
    """Enable the pgvector extension and create all ORM tables.

    A convenience for local/dev setup; production schema changes go through
    Alembic. Importing the models here ensures they are registered on the
    metadata before ``create_all`` runs.
    """
    from CareAI.database.base import Base
    from CareAI.database import policy  # noqa: F401  (registers PolicyChunk)
    from CareAI.database import incident  # noqa: F401  (registers IncidentRecord)
    from CareAI.database import notification  # noqa: F401 (registers Notification)

    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)

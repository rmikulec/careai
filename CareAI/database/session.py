"""Async database engine, session factory, and schema helper.

The connection URL is read from the ``DATABASE_URL`` environment variable, with a
fallback to the local docker-compose Postgres so the package runs with no config.
This is the one place that reads the environment; callers import ``Session``.

FUTURE: move ``DATABASE_URL`` into a typed ``pydantic-settings`` tree (tiered by
environment / DB backend) to match the rest of the stack, and use Alembic instead
of ``create_all`` for production migrations.
"""

import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://florence:florence@localhost:5432/florence",
)

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

    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)

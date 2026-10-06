"""Policy vector store: the ``policy_chunks`` table and its retrieval service.

Populated by the ingestion pipeline (PDF -> markdown -> chunks -> embeddings);
read by the reporting agent through :class:`PolicyService`.
"""

from langchain_openai import OpenAIEmbeddings
from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, String, Text, func, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column

from CareAI.database.base import Base
from CareAI.database.session import Session

EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536


class PolicyChunk(Base):
    """One embedded chunk of a facility policy document.

    Attributes:
        id (int): Surrogate primary key.
        policy_id (str): Policy identifier, e.g. ``POL-EH-001``.
        title (str): Policy title.
        section (Optional[str]): Header path of the chunk within the policy.
        chunk_index (int): Order of the chunk within its policy.
        content (str): The chunk text.
        meta (dict): Owner, dates, keywords, and header metadata.
        embedding (list[float]): Embedding vector of ``content``.
    """

    __tablename__ = "policy_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    policy_id: Mapped[str] = mapped_column(String, index=True)
    title: Mapped[str] = mapped_column(String)
    section: Mapped[str | None] = mapped_column(String, nullable=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)
    meta: Mapped[dict] = mapped_column(JSONB, default=dict)
    embedding: Mapped[list[float]] = mapped_column(Vector(EMBED_DIM))


class PolicyService:
    """Vector retrieval over the ``policy_chunks`` table.

    Args:
        session_maker: Async session factory bound to the policy database.
        embedder (Optional[OpenAIEmbeddings]): Embedding model for queries; a
            default ``text-embedding-3-small`` client is created if omitted.
    """

    def __init__(
        self,
        session_maker: async_sessionmaker = Session,
        embedder: OpenAIEmbeddings | None = None,
    ) -> None:
        self._sessions = session_maker
        self._embedder = embedder or OpenAIEmbeddings(model=EMBED_MODEL)

    async def search(self, query: str, k: int = 6) -> list[dict]:
        """Return the ``k`` policy chunks most similar to ``query``.

        Args:
            query (str): Natural-language search text.
            k (int): Maximum number of chunks to return.

        Returns:
            list[dict]: Chunks with ``policy_id``, ``title``, ``section``,
            ``chunk_index``, ``content``, and cosine ``distance``, nearest first.
        """
        qvec = await self._embedder.aembed_query(query)
        stmt = (
            select(
                PolicyChunk.policy_id,
                PolicyChunk.title,
                PolicyChunk.section,
                PolicyChunk.chunk_index,
                PolicyChunk.content,
                PolicyChunk.embedding.cosine_distance(qvec).label("distance"),
            )
            .order_by("distance")
            .limit(k)
        )
        async with self._sessions() as session:
            rows = (await session.execute(stmt)).all()
        return [
            {
                "policy_id": r.policy_id,
                "title": r.title,
                "section": r.section,
                "chunk_index": r.chunk_index,
                "content": r.content,
                "distance": float(r.distance),
            }
            for r in rows
        ]

    async def list_policies(self) -> list[dict]:
        """Return every ingested policy with its chunk count.

        Returns:
            list[dict]: ``{policy_id, title, chunks}`` per policy, ordered by id.
        """
        stmt = (
            select(
                PolicyChunk.policy_id,
                PolicyChunk.title,
                func.count().label("chunks"),
            )
            .group_by(PolicyChunk.policy_id, PolicyChunk.title)
            .order_by(PolicyChunk.policy_id)
        )
        async with self._sessions() as session:
            rows = (await session.execute(stmt)).all()
        return [
            {"policy_id": r.policy_id, "title": r.title, "chunks": r.chunks}
            for r in rows
        ]

    async def get(self, policy_id: str) -> dict | None:
        """Return a policy's title and its chunks in order.

        Args:
            policy_id (str): Policy identifier to fetch.

        Returns:
            Optional[dict]: ``{policy_id, title, chunks}`` where ``chunks`` is a
            list of ``{chunk_index, section, content}`` ordered by index, or
            ``None`` if no such policy exists. Chunk citations reference these
            ``chunk_index`` values.
        """
        stmt = (
            select(
                PolicyChunk.title,
                PolicyChunk.section,
                PolicyChunk.chunk_index,
                PolicyChunk.content,
            )
            .where(PolicyChunk.policy_id == policy_id)
            .order_by(PolicyChunk.chunk_index)
        )
        async with self._sessions() as session:
            rows = (await session.execute(stmt)).all()
        if not rows:
            return None
        return {
            "policy_id": policy_id,
            "title": rows[0].title,
            "chunks": [
                {
                    "chunk_index": r.chunk_index,
                    "section": r.section,
                    "content": r.content,
                }
                for r in rows
            ],
        }

"""Policy ingestion pipeline.

PDF -> text (``pypdf``) -> markdown + metadata (one structured LLM call) ->
markdown-aware chunks -> embeddings -> ``policy_chunks`` rows. Ingest is
idempotent per policy id: re-ingesting replaces that policy's existing rows.
"""

import io
import logging

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from pydantic import BaseModel, Field
from pypdf import PdfReader
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from CareAI.database.policy import EMBED_MODEL, PolicyChunk
from CareAI.database.session import Session

logger = logging.getLogger(__name__)

_HEADERS = [("#", "h1"), ("##", "h2"), ("###", "h3")]

_CONVERT_SYSTEM = SystemMessage(
    "You convert the extracted text of a hospital policy PDF into clean "
    "GitHub-flavored markdown and extract its metadata.\n"
    "- Use ## headers for numbered sections; preserve tables as markdown tables "
    "and keep lists.\n"
    "- Remove repeated page headers/footers, the 'CONFIDENTIAL / Uncontrolled "
    "when printed' boilerplate, and 'Page N' markers.\n"
    "- Keep the full policy content; do not summarize or drop clauses.\n"
    "- Extract policy_id, title, owner, effective/revised dates, and keywords."
)


class PolicyMarkdown(BaseModel):
    """A policy document converted to markdown with its metadata extracted.

    Attributes:
        policy_id (str): Policy number, e.g. ``POL-EH-001``.
        title (str): Policy title.
        owner (str): Owning department(s).
        effective (Optional[str]): Effective date, if present.
        revised (Optional[str]): Last revised date, if present.
        keywords (list[str]): Retrieval keywords.
        markdown (str): Full policy body as GitHub-flavored markdown.
    """

    policy_id: str = Field(description="Policy number, e.g. POL-EH-001.")
    title: str = Field(description="Policy title.")
    owner: str = Field(description="Owning department(s).")
    effective: str | None = Field(
        default=None, description="Effective date if present."
    )
    revised: str | None = Field(
        default=None, description="Last revised date if present."
    )
    keywords: list[str] = Field(default_factory=list, description="Retrieval keywords.")
    markdown: str = Field(description="Full policy body as clean markdown.")


class PolicyIngestor:
    """Convert policy PDFs into embedded ``policy_chunks`` rows.

    Args:
        model (BaseChatModel): Chat model for the PDF -> markdown conversion.
        embedder (Optional[OpenAIEmbeddings]): Embedding model for chunks.
        session_maker: Async session factory bound to the policy database.
        chunk_size (int): Target chunk size in characters.
        chunk_overlap (int): Overlap between adjacent chunks in characters.
    """

    def __init__(
        self,
        model: BaseChatModel,
        embedder: OpenAIEmbeddings | None = None,
        session_maker: async_sessionmaker = Session,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
    ) -> None:
        self._model = model
        self._embedder = embedder or OpenAIEmbeddings(model=EMBED_MODEL)
        self._sessions = session_maker
        self._header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=_HEADERS, strip_headers=False
        )
        self._char_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    @staticmethod
    def _extract_text(data: bytes) -> str:
        """Extract the text layer from PDF bytes."""
        reader = PdfReader(io.BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    @staticmethod
    def _section_path(meta: dict) -> str | None:
        """Join the header hierarchy of a chunk into a readable section path."""
        parts = [p for p in (meta.get("h1"), meta.get("h2"), meta.get("h3")) if p]
        return " > ".join(parts) or None

    async def ingest_pdf(self, data: bytes) -> dict:
        """Ingest one policy PDF and return a summary.

        Args:
            data (bytes): Raw PDF file content.

        Returns:
            dict: ``{policy_id, title, chunks}`` describing what was stored.
        """
        doc = await self._model.with_structured_output(PolicyMarkdown).ainvoke(
            [_CONVERT_SYSTEM, HumanMessage(self._extract_text(data))]
        )
        sections = self._header_splitter.split_text(doc.markdown)
        chunks = self._char_splitter.split_documents(sections)
        vectors = await self._embedder.aembed_documents(
            [c.page_content for c in chunks]
        )
        async with self._sessions() as session:
            await session.execute(
                delete(PolicyChunk).where(PolicyChunk.policy_id == doc.policy_id)
            )
            session.add_all(
                [
                    PolicyChunk(
                        policy_id=doc.policy_id,
                        title=doc.title,
                        section=self._section_path(chunk.metadata),
                        chunk_index=i,
                        content=chunk.page_content,
                        meta={
                            "owner": doc.owner,
                            "effective": doc.effective,
                            "revised": doc.revised,
                            "keywords": doc.keywords,
                        },
                        embedding=vector,
                    )
                    for i, (chunk, vector) in enumerate(zip(chunks, vectors))
                ]
            )
            await session.commit()
        logger.info("Ingested policy %s (%d chunks)", doc.policy_id, len(chunks))
        return {"policy_id": doc.policy_id, "title": doc.title, "chunks": len(chunks)}

"""HTTP routes for managing the policy corpus.

Upload policy PDFs (ingested into the pgvector store) and list what has been
ingested. All routes require a valid API key.
"""

import asyncio
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from CareAI.api.dependencies import (
    get_policy_ingestor,
    get_policy_service,
    require_api_key,
)
from CareAI.database import PolicyService
from CareAI.ingestion import PolicyIngestor

logger = logging.getLogger(__name__)


class PolicySummary(BaseModel):
    """A summary of one ingested policy.

    Attributes:
        policy_id (str): Policy identifier, e.g. ``POL-EH-001``.
        title (str): Policy title.
        chunks (int): Number of embedded chunks stored.
    """

    policy_id: str
    title: str
    chunks: int


class UploadResponse(BaseModel):
    """The result of an upload request.

    Attributes:
        ingested (list[PolicySummary]): One entry per successfully stored policy.
    """

    ingested: list[PolicySummary]


def _require_pdf(upload: UploadFile) -> None:
    """Reject non-PDF uploads.

    Raises:
        HTTPException: 415 if the file is not a PDF.
    """
    is_pdf = upload.content_type == "application/pdf" or (
        upload.filename or ""
    ).lower().endswith(".pdf")
    if not is_pdf:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"{upload.filename!r} is not a PDF",
        )


def build_policies_router() -> APIRouter:
    """Construct the policy-management API router.

    Returns:
        APIRouter: Router exposing upload and list endpoints, guarded by the
        API-key dependency.
    """
    router = APIRouter(
        prefix="/policies",
        tags=["policies"],
        dependencies=[Depends(require_api_key)],
    )

    @router.post(
        "/upload",
        response_model=UploadResponse,
        status_code=status.HTTP_201_CREATED,
    )
    async def upload_policies(
        files: list[UploadFile] = File(...),
        ingestor: PolicyIngestor = Depends(get_policy_ingestor),
    ) -> UploadResponse:
        """Upload one or more policy PDFs and ingest them concurrently.

        Raises:
            HTTPException: 415 for non-PDF files; 422 if any file cannot be
            ingested (unreadable PDF or extraction failure).
        """
        for upload in files:
            _require_pdf(upload)
        payloads = [(upload.filename, await upload.read()) for upload in files]

        results = await asyncio.gather(
            *(ingestor.ingest_pdf(data) for _, data in payloads),
            return_exceptions=True,
        )

        ingested: list[PolicySummary] = []
        failed: list[str] = []
        for (filename, _), result in zip(payloads, results):
            if isinstance(result, Exception):
                logger.error("Failed to ingest %r", filename, exc_info=result)
                failed.append(filename or "unnamed")
            else:
                ingested.append(PolicySummary(**result))

        if failed:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Could not ingest: {failed}",
            )
        return UploadResponse(ingested=ingested)

    @router.get("", response_model=list[PolicySummary])
    async def list_policies(
        policy_service: PolicyService = Depends(get_policy_service),
    ) -> list[PolicySummary]:
        """List every ingested policy with its chunk count."""
        return [PolicySummary(**p) for p in await policy_service.list_policies()]

    return router

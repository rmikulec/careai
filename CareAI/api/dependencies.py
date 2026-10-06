"""FastAPI dependencies: settings, services, the reporting agent, and auth.

Stateless singletons are cached with ``lru_cache`` so the policy and incident
services are built once and reused across requests. The reporting agent is
different: it is compiled once at startup against the Postgres-backed
checkpointer (see ``app.lifespan``) and stashed on ``app.state``, because its
checkpointer owns a connection pool whose lifecycle must span the app.
"""

from functools import lru_cache

from fastapi import Depends, Header, HTTPException, Request, status
from langchain.chat_models import init_chat_model
from langgraph.graph.state import CompiledStateGraph

from CareAI.config import Settings, get_settings
from CareAI.database import IncidentService, PolicyService
from CareAI.ingestion import PolicyIngestor

# Re-exported so routes and the app factory can depend on the one cached
# accessor; the canonical definition lives in CareAI.config.
__all__ = ["get_settings"]


@lru_cache
def get_policy_service() -> PolicyService:
    """Return the cached policy retrieval service (singleton)."""
    return PolicyService()


@lru_cache
def get_incident_service() -> IncidentService:
    """Return the cached finalized-incident store (singleton)."""
    return IncidentService()


@lru_cache
def get_policy_ingestor() -> PolicyIngestor:
    """Return the cached policy ingestion pipeline (singleton)."""
    settings = get_settings()
    model = init_chat_model(
        settings.openai_model, use_responses_api=True, reasoning_effort="low"
    )
    return PolicyIngestor(model)


def get_reporting_agent(request: Request) -> CompiledStateGraph:
    """Return the shared reporting agent compiled at startup.

    The agent is built in the app lifespan against the Postgres-backed
    checkpointer and stored on ``app.state`` so every request reuses it and a
    ``thread_id`` resumes the same persisted conversation.

    Args:
        request (Request): The incoming request, used to reach ``app.state``.

    Returns:
        CompiledStateGraph: The compiled reporting agent.
    """
    return request.app.state.reporting_agent


def get_escalation_agent(request: Request) -> CompiledStateGraph:
    """Return the shared escalation agent compiled at startup.

    Built once in the app lifespan and stored on ``app.state``; used after a
    report is finalized to assess its severity grounded in the linked policies.

    Args:
        request (Request): The incoming request, used to reach ``app.state``.

    Returns:
        CompiledStateGraph: The compiled escalation agent.
    """
    return request.app.state.escalation_agent


def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    settings: Settings = Depends(get_settings),
) -> None:
    """Validate the ``X-API-Key`` header against the configured keys.

    Args:
        x_api_key (Optional[str]): Value of the ``X-API-Key`` request header.
        settings (Settings): Injected application settings.

    Raises:
        HTTPException: 401 if the key is missing or not recognised.
    """
    if not x_api_key or x_api_key not in settings.api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

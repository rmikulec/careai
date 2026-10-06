"""FastAPI application factory and ASGI entrypoint.

``create_app`` wires CORS, opens shared resources over a lifespan (the ORM
schema, the Postgres-backed graph-state checkpointer, and the reporting agent
compiled against it), and mounts every router under ``/api/v1``; module-level
``app`` is the ASGI target (``uvicorn CareAI.api.app:app``).
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.chat_models import init_chat_model

from CareAI.agents.escalation import build_escalation_agent
from CareAI.agents.reporting import build_reporting_agent
from CareAI.api.dependencies import (
    get_notification_service,
    get_policy_service,
    get_settings,
)
from CareAI.api.routes.policies import build_policies_router
from CareAI.api.routes.reporting import build_reporting_router
from CareAI.database import create_all
from CareAI.database.checkpointer import open_checkpointer
from CareAI.telemetry import configure_telemetry


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Open shared resources for the application's lifetime.

    Ensures the ORM schema exists, opens the Postgres-backed graph-state
    checkpointer, and compiles the reporting agent against it once so every
    request shares one agent whose conversations survive restarts. The
    escalation agent (stateless severity assessment) is compiled here too. The
    checkpointer's connection pool is closed on shutdown.
    """
    settings = get_settings()
    model = init_chat_model(
        settings.openai_model, use_responses_api=True, reasoning_effort="low"
    )
    policy_service = get_policy_service()
    await create_all()
    async with open_checkpointer() as checkpointer:
        app.state.reporting_agent = build_reporting_agent(
            model, policy_service, checkpointer=checkpointer
        )
        app.state.escalation_agent = build_escalation_agent(
            model, policy_service, get_notification_service()
        )
        yield


def create_app() -> FastAPI:
    """Create and configure the CareAI FastAPI application.

    Returns:
        FastAPI: The app with CORS middleware, a resource lifespan, and all
        routers mounted.
    """
    settings = get_settings()
    app = FastAPI(title="CareAI", version="0.1.0", lifespan=lifespan)

    # Trace requests, the agent, and DB calls to the configured OTLP endpoint
    # (a no-op unless OTEL_ENABLED is set); instrument before routers are added.
    configure_telemetry(app, settings)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"])
    async def health() -> dict:
        """Unauthenticated liveness probe."""
        return {"status": "ok"}

    app.include_router(build_reporting_router(), prefix="/api/v1")
    app.include_router(build_policies_router(), prefix="/api/v1")
    return app


app = create_app()

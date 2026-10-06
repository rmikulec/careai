"""Application settings, loaded once from the environment / ``.env``.

A single typed ``pydantic-settings`` object so configuration is not read ad hoc
across the codebase. Field names map case-insensitively to the env vars used by
docker-compose (``DATABASE_URL``, ``API_KEYS``, ``CORS_ORIGINS``,
``OPENAI_MODEL``, ``OTEL_*``). Import :func:`get_settings` for the cached,
process-wide instance rather than constructing ``Settings`` directly.
"""

from functools import lru_cache
from typing import Annotated, Literal

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

# Make .env values (e.g. OPENAI_API_KEY) visible to this process and to the
# libraries that read os.environ directly (langchain).
load_dotenv()


class Settings(BaseSettings):
    """Runtime configuration.

    Attributes:
        environment (str): Deployment environment label (``development`` …).
        api_keys (list[str]): Accepted ``X-API-Key`` values; comma-separated in
            the environment.
        cors_origins (list[str]): Allowed CORS origins; comma-separated in the
            environment.
        openai_model (str): Chat model id used by the reporting agent.
        llm_reasoning_effort (Literal): Reasoning effort passed to the chat model
            ("minimal", "low", "medium", or "high"); higher trades latency/cost
            for deeper reasoning.
        llm_max_retries (int): Times the chat model retries a failed request
            (transient HTTP errors / rate limits) before giving up.
        agent_recursion_limit (int): Maximum LangGraph super-steps allowed for a
            single agent turn before a ``GraphRecursionError`` is raised.
        database_url (str): SQLAlchemy async connection URL for Postgres; the
            local docker-compose DB is the default so the app runs unconfigured.
        otel_enabled (bool): Whether to export OpenTelemetry traces. Off by
            default so local runs and tests don't reach for an exporter.
        otel_exporter_otlp_endpoint (str): OTLP gRPC endpoint spans are sent to.
        otel_service_name (str): ``service.name`` reported on exported spans.
        careai_api_url (str): Base URL the Streamlit UI calls the API on.
        careai_api_key (str): ``X-API-Key`` the Streamlit UI sends.
    """

    model_config = SettingsConfigDict(extra="ignore", case_sensitive=False)

    environment: str = "development"

    # Auth & CORS
    api_keys: Annotated[list[str], NoDecode] = ["dev-local-key"]
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:3000"]

    # LLM
    openai_model: str = "gpt-5.6-luna"
    llm_reasoning_effort: Literal["minimal", "low", "medium", "high"] = "medium"
    llm_max_retries: int = 2
    agent_recursion_limit: int = 25

    # Database
    database_url: str = "postgresql+asyncpg://florence:florence@localhost:5432/florence"

    # Observability (self-hosted OTEL; no PHI leaves the boundary)
    otel_enabled: bool = False
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    otel_service_name: str = "careai-api"

    # Streamlit UI client
    careai_api_url: str = "http://localhost:8000"
    careai_api_key: str = "dev-local-key"

    @field_validator("api_keys", "cors_origins", mode="before")
    @classmethod
    def _split_csv(cls, value: object) -> object:
        """Parse a comma-separated env string into a list of trimmed values."""
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Return the cached, process-wide application settings.

    Returns:
        Settings: The settings parsed once from the environment and reused.
    """
    return Settings()

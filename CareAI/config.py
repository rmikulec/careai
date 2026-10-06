"""Application settings, loaded once from the environment / ``.env``.

A single typed settings object so configuration is not read ad hoc across the
codebase. Field names map case-insensitively to the env vars used by
docker-compose (``API_KEYS``, ``CORS_ORIGINS``, ``OPENAI_MODEL``).
"""

from typing import Annotated

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

# Make .env values (e.g. OPENAI_API_KEY) visible to this process and to the
# libraries that read os.environ directly (langchain, the DB session).
load_dotenv()


class Settings(BaseSettings):
    """Runtime configuration.

    Attributes:
        api_keys (list[str]): Accepted ``X-API-Key`` values; comma-separated in
            the environment.
        cors_origins (list[str]): Allowed CORS origins; comma-separated in the
            environment.
        openai_model (str): Chat model id used by the reporting agent.
    """

    model_config = SettingsConfigDict(extra="ignore", case_sensitive=False)

    api_keys: Annotated[list[str], NoDecode] = ["dev-local-key"]
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:3000"]
    openai_model: str = "gpt-5.6-luna"

    @field_validator("api_keys", "cors_origins", mode="before")
    @classmethod
    def _split_csv(cls, value: object) -> object:
        """Parse a comma-separated env string into a list of trimmed values."""
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

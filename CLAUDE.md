# Coding Standards

A FastAPI backend API. These standards are carried over from `pyagentic`. Follow them
exactly.

## Language & Tooling

- **Python 3.13+**. Use modern builtin generics (`list[str]`, `dict[str, int]`,
  `X | None` is acceptable, but the existing code favors `Optional[X]` / `Union[X, Y]`
  from `typing` — match that).
- **Dependency management & packaging** via `uv` + `pyproject.toml`.
- **Formatting**: `black` (default 88-col line length). Format before committing.
- **Linting**: `flake8`. Where a line genuinely can't fit (e.g. a long URL or message),
  suppress with a trailing `# noqa: E501` rather than contorting the code.
- **Tasks**: expose common commands via `taskipy` (`[tool.taskipy.tasks]`).

## Typing

- **Fully type-annotated.** Every function signature has parameter and return types,
  including `-> None`. No untyped public surface.
- Use `Optional[X]`, `Union[X, Y]`, `Any`, `Literal[...]` from `typing`.

## Docstrings

- **Private functions / methods** (`_private_func`): a brief one-line description is
  enough.
- **Public functions / methods**: [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
  **with types**, including `Args`, `Returns`, and `Raises` sections where applicable:
  ```python
  def example(name: str, count: int = 0) -> bool:
      """Short summary.

      Args:
          name (str): Description.
          count (int): Description.

      Returns:
          bool: Description.

      Raises:
          ValueError: Description.
      """
  ```
- **Modules**: start each module with a docstring explaining what it holds and why it
  exists.
- **Pydantic models**: document fields in an `Attributes:` section of the class
  docstring (name, type, meaning).
- **Comments explain *why*, not *what*.** Reserve inline comments for non-obvious
  rationale, edge cases, and invariants — not restating the code.

## Module & Package Layout

- **Implementation modules are underscore-prefixed** (`_app.py`, `_config.py`,
  `_models.py`, `_routes.py`, `_sessions.py`). The leading `_` marks them private to the
  package.
- **The public API is re-exported from `__init__.py`** with an explicit `__all__`.
  Callers import from the package, not the private modules.
- Group related concerns into subpackages, each with its own `__init__.py`
  (e.g. a feature folder with `_models.py`, `_routes.py`, and a `_service`/`store`
  layer underneath).
- **Constants** are module-level `UPPER_SNAKE_CASE`; prefix with `_` when private to the
  module (`_SSE_HEADERS`, `_TAIL_POLL_SECONDS`).

## Pydantic (v2)

- Models subclass `BaseModel`. Use `Field(default_factory=...)` for mutable defaults
  (never a bare `[]`/`{}`).
- Validators are `@field_validator("name")` + `@classmethod`, named `_validate_*`.
- Enums subclass `(str, Enum)` so they serialize cleanly.
- Use `ConfigDict` for model config (e.g. `populate_by_name=True`).
- Keep **wire models** (request/response) distinct from internal/domain models.

## FastAPI Conventions

- Define routes on an `APIRouter`; prefer **builder functions** that construct and return
  a configured router (`def build_xxx_router(...) -> APIRouter:`).
- **Endpoints are `async def`.** Declare `response_model=` and, for non-200 success,
  `status_code=` on the decorator.
- Signal errors with `raise HTTPException(status_code=..., detail="...")`. Map domain
  exceptions to status codes at the route boundary:
  - `404` not found, `409` conflict / illegal state transition, `202` accepted-async.
- Validate request bodies and query params through typed Pydantic models / typed
  parameters — don't reach into raw request data unless necessary.
- Keep business logic in a service/store layer; routes stay thin (parse → delegate →
  shape response).

## Configuration

- Load config from a typed Pydantic model tree, with sensible defaults so the app runs
  with no config file. Parse env / files (`tomllib`, env vars) into those models; never
  scatter `os.environ` reads through the codebase.

## Logging

- Per-module logger: `logger = logging.getLogger(__name__)`. Never use `print`.
- Centralize logging configuration in one module (a `LOGGING_CONFIG` dict + a
  `configure_logging()` that runs once). Default level `WARNING`.

## Exceptions

- Define custom exception classes for domain errors. Each has a docstring (with `Args:`
  for its constructor params) and builds a descriptive message in `__init__`.
- Keep deprecated names as aliases with a comment when renaming, for backwards
  compatibility.

## Testing

- `pytest` + `pytest-asyncio`. The `tests/` tree **mirrors the package layout**.
- Shared fixtures in `conftest.py`; reusable fakes under a `mocks/` package.
- Test behavior through the public API where possible.

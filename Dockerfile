# Runtime image for the CareAI API. uv-managed, matching the project's uv + uv.lock
# workflow. Single-stage keeps it simple for the local/dev stack; deps are cached
# in their own layer so source edits don't trigger a full reinstall.
FROM python:3.13-slim

# uv binary from its official distroless image (pinned major for reproducibility).
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

WORKDIR /app

# UV_COMPILE_BYTECODE: faster cold starts. UV_LINK_MODE=copy: silence the cache
# hardlink warning across the layer boundary. UV_PYTHON_DOWNLOADS=0: use the
# base image's interpreter rather than fetching another.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

# Install dependencies first, without the project itself, so this layer is reused
# whenever only application source changes.
COPY pyproject.toml uv.lock README.md ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Now install the project (builds the CareAI wheel via hatchling).
COPY CareAI ./CareAI
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Put the venv on PATH so `uvicorn`/`alembic`/`python` resolve without `uv run`.
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Single process on purpose: the reporting agent's conversation checkpointer is
# in-memory (see api/dependencies.py), so a thread_id must always hit the same
# worker. Scale horizontally only after moving to a shared checkpointer.
CMD ["uvicorn", "CareAI.api.app:app", "--host", "0.0.0.0", "--port", "8000"]

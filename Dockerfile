# First, build the application in the `/app` directory.
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
WORKDIR /app

# Explicitly create the virtual environment
RUN python -m venv .venv

# Install uv into the venv (uv is needed for sync)
RUN .venv/bin/pip install uv

# Install dependencies into the created venv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    .venv/bin/uv sync --frozen --no-install-project --no-dev

ADD . /app
# Re-sync after adding app code (if needed, but might not be necessary with explicit venv creation)
RUN --mount=type=cache,target=/root/.cache/uv \
    .venv/bin/uv sync --frozen --no-dev

# Then, use a final image with uv for development convenience
FROM python:3.12-slim-bookworm

# Copy uv from the builder stage for development use
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy the virtual environment explicitly from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the rest of the application code
COPY --from=builder /app /app

WORKDIR /app

# Set environment variables for proper Python environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/.venv/lib/python3.12/site-packages"
ENV VIRTUAL_ENV="/app/.venv"

# Expose port 8000
EXPOSE 8000

# Use gunicorn on port 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
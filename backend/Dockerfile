FROM python:3.13-slim AS builder

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy UV dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
RUN uv sync --frozen --no-install-project

# Copy application code and blocked_sites.txt
COPY app/ app/
COPY app/blocked_sites.txt app/blocked

# Stage 2: Runtime
FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy virtual environment and application files from builder
COPY --from=builder /app /app

# Create a non-root user for security
RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["uv","run","uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
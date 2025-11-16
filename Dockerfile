FROM mcr.microsoft.com/playwright/python:v1.56.0-jammy-amd64

WORKDIR /app

# Install build dependencies for Python packages (pandas, numpy, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy dependency files and install dependencies
COPY pyproject.toml uv.lock README.md ./

# Use cache mount for uv cache to speed up subsequent builds
# This will cache downloaded packages and compiled wheels
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

# Create necessary directories
RUN mkdir -p data logs

# Default entrypoint (can be overridden in docker-compose)
ENTRYPOINT ["uv", "run", "python", "main.py", "guest", "stable", "--max-tweets", "20"]

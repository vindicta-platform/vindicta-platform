FROM mcr.microsoft.com/devcontainers/python:1-3.13-bullseye

# Install uv for high-performance dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install basic development utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

USER vscode
WORKDIR /workspace

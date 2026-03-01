# Quick Start

Get Vindicta running in 5 minutes.

---

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended)
- Docker & Docker Compose (for full platform)
- A terminal

## Option 1: Devcontainer (Recommended)

The fastest path. Requires Docker Desktop and a devcontainer-capable IDE (VS Code, Antigravity, etc.).

```bash
git clone https://github.com/vindicta-platform/vindicta-foundation.git
cd vindicta-foundation
# Open in IDE → "Reopen in Container"
# Or from CLI:
npx -y @devcontainers/cli up --workspace-folder .
```

Everything is installed automatically: Python 3.12, `uv`, and all project dependencies.

## Option 2: The Engine (Simulation)

The `vindicta-engine` handles all mechanics, dice resolution, and physics.

```bash
# Clone the Engine repository
git clone https://github.com/vindicta-platform/vindicta-engine.git
cd vindicta-engine

# Install with uv
uv sync
source .venv/bin/activate
# or `uv run pytest` directly
```

## Option 3: Full Platform (Docker)

Run the entire suite (Portal, Engine, Oracle) locally using Docker.

```bash
# Clone the Orchestrator / Platform Root
git clone https://github.com/vindicta-platform/vindicta-platform.git
cd vindicta-platform

# Start all services
docker-compose up -d

# Access the Portal
# Open http://localhost:3000
```

## Option 4: Interface Only (Platform Web)

If you only want to work on the frontend portals:

```bash
git clone https://github.com/vindicta-platform/vindicta-platform.git
cd vindicta-platform
# Add typical JS/frontend commands here via the web workspaces
npm install
npm run dev

# Open http://localhost:3000
```

---

## Next Steps

- [Installation Guide](installation.md) — Detailed setup instructions for each meso-repository.
- [WARScribe System](../features/army-management.md) — Learn the notation format.
- [Architecture](../architecture/overview.md) — Understand how the modules connect.

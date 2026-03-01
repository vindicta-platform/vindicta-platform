# Installation

Detailed installation instructions for each platform component.

---

## Core Requirements

All Vindicta components require:

- **Python 3.10+** (for backend components)
- **Node.js 18+** (for UI components)
- **uv** (recommended package manager)

### Installing uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Devcontainer (Recommended)

The simplest way to get started. Requires Docker Desktop.

```bash
git clone https://github.com/vindicta-platform/vindicta-foundation.git
cd vindicta-foundation
# Open in your IDE and select "Reopen in Container"
# Or use the CLI:
npx -y @devcontainers/cli up --workspace-folder .
```

This installs Python 3.12, `uv`, and all project dependencies automatically.

## Component Installation

### The Engine (Physics & Simulation)

The simulation engine and back-end logic layer:

```bash
git clone https://github.com/vindicta-platform/vindicta-engine.git
cd vindicta-engine
uv sync
```

### The Platform (Web & Identity)

The unified web interface and user entry point:

```bash
git clone https://github.com/vindicta-platform/vindicta-platform.git
cd vindicta-platform
npm install
```

### Individual Modules

Each module can be installed independently:

```bash
# Core Platform
uv pip install git+https://github.com/vindicta-platform/vindicta-foundation.git
uv pip install git+https://github.com/vindicta-platform/vindicta-engine.git

# Logic & Data
uv pip install git+https://github.com/vindicta-platform/warscribe-system.git
uv pip install git+https://github.com/vindicta-platform/vindicta-economy.git
uv pip install git+https://github.com/vindicta-platform/vindicta-oracle.git
```

---

## Verification

Verify your installation:

```bash
# Check CLI equivalent (if installed)
# vindicta --version

# Run tests
pytest tests/ -v
```

---

## Troubleshooting

### uv lock file issues

```bash
uv cache clean
rm uv.lock
uv sync
```

### Port already in use

```bash
# Find process on port 8000
lsof -i :8000
# or on Windows
netstat -ano | findstr :8000
```

### Devcontainer hangs or `uv sync` permission denied

A stale `.venv` directory owned by root from a previous Docker run can block `uv sync`:

```bash
# Remove the stale .venv using Docker (runs as root)
docker run --rm -v ${PWD}:/ws -w /ws python:3.12-bookworm rm -rf .venv
# Then rebuild the devcontainer
```

If the devcontainer appears to hang with no output, use the open-source CLI to surface the real error:

```bash
npx -y @devcontainers/cli up --workspace-folder .
```


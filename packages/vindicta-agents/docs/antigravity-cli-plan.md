# Implementation Plan: Antigravity CLI

This document outlines the design and implementation plan for the `antigravity` CLI tool, which facilitates the installation of agent configurations and workflows into target repositories.

## 1. Objective
Enable developers to quickly bootstrap a repository with standardized AI agent personas (SM, SSE, etc.) and their associated workflows (Check-in, PR review, etc.).

## 2. CLI Command Interface

The CLI will be named `antigravity` (alias `ag`).

### Commands

#### `antigravity init`
Initializes a repository for Antigravity workflows.
- Creates `.agent/workflows/` directory.
- Creates `agents/` directory if needed.
- Generates a `.antigravity.yaml` config file.

#### `antigravity agent list`
Lists all available agent types bundled with the CLI.
- Output: `senior-manager`, `senior-software-engineer`, `agile-delivery-lead`, etc.

#### `antigravity agent install <type>`
Installs a specific agent persona and its dependent workflows.
- **Arguments**: `<type>` (e.g., `sm`, `senior-manager`)
- **Flags**: `--force` (overwrite existing), `--path <repo-path>`
- **Behavior**:
    1. Copies `library/agents/<type>/AGENT.md` to `agents/<type>/AGENT.md`.
    2. Parses `AGENT.md` (or metadata) for workflow links.
    3. Copies the required `.md` files from `library/workflows/` to `.agent/workflows/`.

#### `antigravity workflow install <name>`
Installs a specific workflow independently.
- **Arguments**: `<name>` (e.g., `adl-standup`)

---

## 3. Package & Setup

### Repository Structure
```text
antigravity-cli/
├── pyproject.toml        # Build system and dependencies (typer, rich, pyyaml)
├── src/
│   └── antigravity/
│       ├── __init__.py
│       ├── cli.py        # Main entry point using Typer
│       ├── registry.py   # Registry of available agents/workflows
│       ├── installer.py  # Logic for copying files and templating
│       └── library/       # Source of truth for files
│           ├── agents/
│           │   └── senior-manager/
│           │       └── AGENT.md
│           └── workflows/
│               └── sm-check-in.md
└── tests/
    └── test_cli.py
```

### Setup (`pyproject.toml`)
```toml
[project]
name = "antigravity-cli"
version = "0.1.0"
dependencies = [
    "typer[all]",
    "rich",
    "pyyaml",
]

[project.scripts]
antigravity = "antigravity.cli:app"
ag = "antigravity.cli:app"
```

---

## 4. Metadata Strategy
To avoid fragile parsing of markdown files, each agent directory in the `library/` will include a `metadata.yaml`:

```yaml
# library/agents/senior-manager/metadata.yaml
name: "Senior Manager"
id: "senior-manager"
description: "Strategic orchestrator"
workflows:
  - "sm-check-in"
  - "sm-start-work"
  - "sm-end-day"
```

## 5. Future Enhancements
- **Global Config**: Support for a global `~/.antigravity/` registry.
- **Remote Registry**: `antigravity install --from github.com/owner/repo`.
- **Custom Templates**: Use Jinja2 to allow variable injection into `AGENT.md` (e.g., project name).

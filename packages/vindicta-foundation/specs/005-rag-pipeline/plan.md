# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

This feature implements a Retrieval-Augmented Generation (RAG) pipeline to ingest rules from Warhammer 40k sites (Wahapedia and 40k.app) and serve them to Vindicta agents. Per user constraints, it strictly relies on local models and tooling (ChromaDB and Ollama) to function as a fully offline, cost-free MVP. A Local Model Context Protocol (MCP) server enables agents to query this indexed knowledge seamlessly.

## Technical Context

**Technical Setup & Integration**:
- **Foundation**: Integrates directly with `vindicta-foundation` schemas, ensuring all models inherit `VindictaModel` for strict structural integrity across the ecosystem.
- **GitHub Actions (`.github`)**: The pipeline utilizes the centralized `ci-python-template.yml` and `ci-precommit-template.yml` inherited from the `vindicta-platform/.github` repository. All tests (Python 3.11/3.12 matrix, `pytest`, `ruff`, `mypy`) must pass this workflow. If the workflow fails during a Pull Request, the PR will be automatically converted to Draft status.
- **Documentation (`docs/`)**: Architecture changes (e.g., ADRs) will be placed in `vindicta-oracle/docs/adr/`. Changes to systemic layouts must update `docs/index.md` and be verifiable via `uv run mkdocs build --strict`. The `vindicta-platform.github.io` repo acts as the static frontend host for these compiled docs.

**Language/Version**: Python 3.12+ (uv workspace)
**Primary Dependencies**: mcp (Model Context Protocol SDK), crawl4ai, chromadb, ollama (for local Python client embeddings)
**Storage**: Embedded ChromaDB (vector database) + SQLite metadata (persisted locally on disk)
**Testing**: pytest (with 90% coverage mandate), pre-commit
**Target Platform**: Local Developer Workstations (Windows, macOS, Linux)
**Project Type**: RAG Pipeline + Local Agent Tool Server (MCP Web Service)
**Performance Goals**: < 1.5 seconds retrieval latency locally for agent requests
**Constraints**: MUST use strictly local models and tooling for the MVP. No external APIs (other than scraping targets) can be utilized. All inference and vector lookups must happen on localhost.
**Scale/Scope**: Designed for tens of thousands of markdown chunks. Local scale MVP for one human/agent user concurrently.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[x] **Model Integrity**: `RulesSegment` and `AgentQuery` will explicitly inherit from `VindictaModel` in `vindicta_foundation.models.base`. (Constitution II).
[x] **Quality Mandate**: `pytest` requires 90% coverage, `mypy` strict type checking will be enforced, and `ruff` linting applies. (Constitution V).
[x] **Environment**: `pyproject.toml` uses `pythonpath = ["src"]`. (Constitution Constraints).

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
vindicta-oracle/
├── src/
│   ├── vindicta_oracle/
│   │   ├── rag_pipeline/
│   │   │   ├── scraper.py       # crawl4ai integrations
│   │   │   └── storage.py       # ChromaDB + SQLite logic
│   │   ├── mcp_server/
│   │   │   └── server.py        # MCP server exposing search_40k_rules
│   │   └── models/
│   │       ├── __init__.py      # Exports
│   │       └── rag.py           # Inherits from VindictaModel
├── tests/
│   ├── unit/
│   │   ├── test_scraper.py
│   │   └── test_storage.py
│   └── integration/
│       └── test_mcp_server.py
├── pyproject.toml
```

**Structure Decision**: A new `rag_pipeline` and `mcp_server` under `vindicta-oracle` (Option 1 equivalent). The oracle handles memory and intelligent lookups. Models belong in `models/` mapping standard Vindicta standards.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected. Strict adherence to Foundation axioms and local model execution per user requests.*

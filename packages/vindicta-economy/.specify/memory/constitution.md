# Vindicta Economy Constitution

## Core Principles

### I. MCP-First Mandate
All filesystem, git, and external operations must use the provided MCP tools. Manually constructing commands is forbidden if an MCP tool exists.

### II. Spec-Driven Development (SDD)
No code is written without a prior specification (`spec.md`) and implementation plan (`plan.md`).

### III. Zero-Issue Stability
The `main` branch must always pass all linting and test suites. PRs that break CI will not be merged.

### IV. Python-Full Standards
- **Linting**: All code must pass `ruff` and `mypy` checks.
- **Testing**: Minimum 90% coverage with `pytest`.
- **BDD**: Core behaviors must be defined in Gherkin and verified with `behave`.

### V. Domain Isolation
This domain (`vindicta-economy`) must not import from other domain realms. Coordination happens via the swarm orchestrator only.

# TODO: Consolidate and update GEMINI.md
# Vindicta Platform Workspace Rules

This file defines the foundational mandates for the entire Vindicta Platform workspace. These rules take precedence over general defaults.

## 1. Project Constitution & Requirements
- All architectural models, specification generation, implementation rules, and agent workflows MUST adhere to the requirements defined in `docs/constitution.md` and `.specify/memory/constitution.md`.

## 2. Structural Integrity & Core Models
- Every domain model in the platform SHOULD align with the architectural patterns established in `packages/vindicta-foundation`.
- Models within the foundation package MUST inherit from `VindictaModel` in `src/vindicta_foundation/models/base.py`.

## 3. Meso-Repo Consolidation
- Follow the consolidation tactics in `docs/architecture/adr/0006-consolidation-tactics.md` when porting code from other repositories.
- Legacy code must be audited against the project requirements before integration.

## 4. Architecture Documentation
- Update the **C4 Model** in `docs/architecture/c4-model.md` when changing container boundaries.
- Standardize new ADRs using the `docs/architecture/adr/_0000-template.md` and follow the `XXXX-title.md` naming convention.
- Always verify documentation with `uv run mkdocs build --strict` after any change to the `docs/` directory.

## 5. Quality Mandates
- **Coverage:** Minimum 90% test coverage required for all new logic. Verify with `pytest`.
- **Types:** Strict type checking with `mypy` is mandatory across all packages.
- **Linting & Formatting:** All code must pass `ruff check .` AND `ruff format --check .`.

## 6. Speckit Integration & Workflows
- Utilize the IDE slash commands defined in `.agent/workflows/` (e.g., `/speckit-plan`, `/speckit-tasks`) for complex tasks like task extraction, planning, and implementation.
- The `speckit-` prefix in `.agent/workflows/` is a **strict namespace** reserved exclusively for Speckit configurations. Other workflows must either be namespace-free or use appropriate custom namespaces.

## 7. Pull Request & Git Standards
- **PR Formatting:** NEVER use inline `--body` flags with `gh pr create` or `gh pr edit`.
- **Body Files:** ALWAYS generate a properly formatted markdown file (e.g., `PR_BODY.md`) and use the `--body-file` flag to ensure high-quality documentation.
- **Cleanup:** Delete temporary PR body files immediately after the PR is created or updated.

## 8. Devcontainer Standards
- **Minimalism (YAGNI):** `.devcontainer/devcontainer.json` MUST remain minimal. Use the Microsoft Python base image (`mcr.microsoft.com/devcontainers/python:1-3.12-bookworm`) unless a concrete, immediate need for a custom Dockerfile exists.
- **Debugging:** If the devcontainer appears to "hang," use `npx -y @devcontainers/cli up --workspace-folder .` to surface real errors.

## 9. Strategic AI Mandates
- **Direct Action:** Assume all requests are directives unless explicitly phrased as inquiries.
- **Surgical Changes:** Focus modifications strictly on requested areas. Avoid unrelated refactoring.
- **Validation:** Never assume success; always confirm outcomes with shell commands, build checks, or test runs.

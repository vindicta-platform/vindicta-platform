### Vindicta Foundation Workspace Rules

1. **Dual Constitution Hierarchy**:
    - **Tier 1 (Foundation Law)**: All architectural models and universal definitions must adhere to the **Zero-Order Axioms** defined in `docs/constitution.md`.
    - **Tier 2 (Builder Law)**: Specification generation, implementation rules, and agent workflows strictly rely on `# Project Constitution` in `.specify/memory/constitution.md`, which inherently adheres to Tier 1.
2. **Structural Integrity**:
    - Every domain model MUST inherit from `VindictaModel` in `src/vindicta_foundation/models/base.py`.
    - New models must be explicitly exported in `src/vindicta_foundation/models/__init__.py`.
3. **Meso-Repo Consolidation**:
    - Follow the consolidation tactics in `docs/architecture/adr/0006-consolidation-tactics.md` when porting code from other repositories.
    - Legacy code must be audited against the **Vindicta Axioms** before integration.
4. **Architecture Documentation**:
    - Update the **C4 Model** in `docs/architecture/c4-model.md` when changing container boundaries.
    - Standardize new ADRs using the `docs/architecture/adr/_0000-template.md` and follow the `XXXX-title.md` naming convention.
    - Always verify documentation with `uv run mkdocs build --strict` after any change to the `docs/` directory.
5. **Quality Mandates**:
    - **Coverage**: Minimum 90% test coverage required. Verify with `uv run pytest`.
    - **Types**: Strict type checking with `mypy` is mandatory.
    - **Linting & Formatting**: All code must pass `ruff check .` AND `ruff format --check .`. Verify explicitly during pre-flight checks if `just prepush` fails.
6. **Speckit Integration & Workflows**: Utilize the IDE slash commands defined in `.agent/workflows/` (e.g., `/speckit-plan`, `/speckit-tasks`) for complex tasks like task extraction, planning, and implementation. Do not attempt to manually reference or run `.gemini/commands/*.toml` configuration files.
7. **Workflow Namespacing**: The `speckit-` prefix in `.agent/workflows/` is a **strict namespace** reserved exclusively for Speckit configurations. Other workflows must either be namespace-free (e.g., `pr.md`) or use appropriate custom namespaces for logical grouping.
8. **Pull Request Formatting**: You must NEVER use inline `--body` flags with `gh pr create` or `gh pr edit`. You MUST ALWAYS generate a properly formatted markdown file (e.g., `PR_BODY.md`) and use the `--body-file` flag to ensure high-quality, template-driven documentation. Clean up the body file immediately after execution.
9. **Devcontainer Minimalism (YAGNI)**: The `.devcontainer/devcontainer.json` MUST remain minimal — no custom `Dockerfile`, no `init.sh`, no extra features unless a concrete, immediate need exists. The Microsoft Python base image (`mcr.microsoft.com/devcontainers/python:1-3.12-bookworm`) already provides `pipx`, `git`, `gh`, and the `vscode` user. Only add complexity when the default image provably cannot satisfy a requirement.
10. **Devcontainer Debugging**: When the Antigravity devcontainer appears to "hang," use `npx -y @devcontainers/cli up --workspace-folder .` to surface the real error. Antigravity's CLI does not stream `postCreateCommand` output, making failures look like hangs. Always check for stale `.venv` directories owned by root before rebuilding.

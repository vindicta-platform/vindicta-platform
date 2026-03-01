<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- List of modified principles:
  - VI. Speckit Integration: Updated tool reference from .gemini/commands/ to .agent/workflows/
- Added sections:
  - VII. Specification Directory Convention
- Templates requiring updates:
  - None (templates already aligned with NNN-short-name convention)
- Follow-up TODOs:
  - None
-->

# Vindicta Foundation Constitution

## Core Principles

### I. Foundation Adherence (NON-NEGOTIABLE)
All technical decisions, specs, and tasks generated under this constitution MUST adhere to the **Zero-Order Axioms** defined in the [Platform Foundation Constitution](../../docs/constitution.md). This document (Tier 2) strictly governs the *implementation and generation* process, while the Foundation Constitution (Tier 1) governs the *universal mechanics and truth*.

### II. Model Integrity (Structural Integrity)
Every domain model MUST inherit from `VindictaModel` in `src/vindicta_foundation/models/base.py`. New models must be explicitly exported in `src/vindicta_foundation/models/__init__.py`. This ensures consistent validation, metadata, and serialization across the entire Vindicta ecosystem.

### III. Meso-Repo Consolidation
Implementation must follow the consolidation tactics defined in `docs/architecture/adr/0006-consolidation-tactics.md`. Legacy code ported from other repositories must be audited against the **Vindicta Axioms** before integration into the shared kernel. We prioritize a clean, unified codebase over rapid, unverified migration.

### IV. Documentation Discipline
Architecture documentation is a living asset. Update the **C4 Model** in `docs/architecture/c4-model.md` immediately when changing container or component boundaries. New architectural decisions must be documented as ADRs using the standard template and naming convention. All documentation changes must be verified with `uv run mkdocs build --strict`.

### V. Quality Mandates (NON-NEGOTIABLE)
We maintain a zero-compromise policy on quality.
- **Coverage**: Minimum 90% test coverage required for all new code. Verify with `uv run pytest`.
- **Types**: Strict type checking with `mypy` is mandatory.
- **Linting**: All code must pass `ruff check .` AND `ruff format --check .`.

### VI. Speckit Integration
Utilize the IDE slash commands defined in `.agent/workflows/` (e.g., `/speckit-plan`, `/speckit-tasks`, `/speckit-specify`) for task decomposition, planning, and implementation. The `speckit-` prefix is a **strict namespace** reserved exclusively for Speckit workflows. Ensure cross-artifact consistency by running `/speckit-analyze` regularly. The "Builder Law" is enforced by these tools to maintain systemic integrity.

### VII. Specification Directory Convention (NON-NEGOTIABLE)
All feature specifications MUST reside in `specs/NNN-short-name/` where:
- **NNN**: A 3-digit zero-padded sequential number (e.g., `001`, `002`, `003`).
- **short-name**: A 2-4 word kebab-case descriptor (e.g., `ocr-parser`, `dice-core`).
- The `create-new-feature.ps1` script auto-assigns the next available number.
- Never nest spec directories (e.g., `specs/feat/name/` is **forbidden**).

Each feature directory MUST contain at minimum:
- `spec.md` — Functional specification (created by `/speckit-specify`)
- `plan.md` — Implementation plan (created by `/speckit-plan`)
- `tasks.md` — Task breakdown (created by `/speckit-tasks`)

Optional artifacts per feature:
- `research.md` — Technical research decisions
- `data-model.md` — Entity and data model definitions
- `quickstart.md` — Usage examples
- `contracts/` — Interface contracts (APIs, grammars, schemas)
- `checklists/` — Quality validation checklists

## Additional Constraints

- **Python Environment**: `pyproject.toml` must include `pythonpath = ["src"]` to prevent `ModuleNotFoundError` during test collection.
- **Git Hygiene**: Ensure `**/__pycache__/` is added to `.gitignore` to recursively ignore Python cache directories.
- **Encoding Awareness**: If standard tools fail to read a file, be prepared to handle non-UTF-8 encodings (e.g., UTF-16LE) manually.

## Development Workflow

1. **Clarify**: Use `/speckit-clarify` to resolve requirements or technical unknowns.
2. **Specify**: Use `/speckit-specify` to create detailed functional specifications.
3. **Plan**: Use `/speckit-plan` to develop technical implementation plans.
4. **Tasks**: Use `/speckit-tasks` to decompose plans into actionable, dependency-ordered tasks.
5. **Implement**: Use `/speckit-implement` to execute code implementation following the approved plan.

## Governance
This constitution is governed by the Vindicta Platform's systemic logic and requires validation against Zero-Order Axioms. Evolution of these principles occurs via the Amendment Mechanism. All pull requests and architectural reviews must verify compliance with these Tier 2 laws.

**Version**: 1.1.0 | **Ratified**: 2026-02-21 | **Last Amended**: 2026-02-22

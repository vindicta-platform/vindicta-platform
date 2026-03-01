# Implementation Plan: Rules Validation Parser

**Branch**: `006-rules-validation-parser` | **Date**: 2026-02-23 | **Spec**: [spec.md](file:///c:/Users/bfoxt/vindicta-playground/vindicta-foundation/specs/006-rules-validation-parser/spec.md)
**Input**: Feature specification from `/specs/006-rules-validation-parser/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

This feature implements a rules validation engine that cross-references parsed game transcript actions against the RAG rules database (005-rag-pipeline). It accepts pre-parsed, typed action objects from upstream parsers, queries the RAG storage module directly (in-process, not via MCP), and produces structured validation verdicts (legal/illegal/hallucination). Legal actions are augmented with the exact rules text for downstream consumers (Debate Engine, Analytics). Batch validation of entire transcripts produces a consolidated integrity report with a simple ratio score.

## Technical Context

**Technical Setup & Integration**:
- **Foundation**: Integrates directly with `vindicta-foundation` schemas. All models inherit `VindictaModel` from `src/vindicta_foundation/models/base.py`.
- **RAG Dependency**: Imports `RulesStorage.search()` from `vindicta_foundation.rag_pipeline.storage` for in-process rules lookups. The MCP server is reserved for external agent consumers.
- **GitHub Actions (`.github`)**: Uses `ci-python-template.yml` and `ci-precommit-template.yml`. Tests run on Python 3.11/3.12 matrix with `pytest`, `ruff`, `mypy`.
- **Documentation (`docs/`)**: ADRs placed in `docs/adr/`. Changes verified via `uv run mkdocs build --strict`.

**Language/Version**: Python 3.12+ (uv workspace)
**Primary Dependencies**: pydantic (models), vindicta_foundation.rag_pipeline.storage (RAG queries), logging (observability)
**Storage**: N/A (reads from RAG storage via `RulesStorage`; no new persistence layer)
**Testing**: pytest (90% coverage mandate), pytest-mock, pytest-cov
**Target Platform**: Local Developer Workstations (Windows, macOS, Linux)
**Project Type**: Library (validation engine consumed by downstream services)
**Performance Goals**: < 10 seconds for batch validation of a 50-action transcript (SC-003)
**Constraints**: Must use the shared `RulesStorage` module directly. Must fail gracefully when RAG is unavailable (FR-007). All inference local.
**Scale/Scope**: Single transcripts of up to ~100 actions per batch. One concurrent user for MVP.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[x] **Model Integrity**: `ValidationRequest`, `ValidationVerdict`, `ViolationReport`, `AugmentedAction`, and `TranscriptIntegrityReport` will explicitly inherit from `VindictaModel` in `vindicta_foundation.models.base`. (Constitution II).
[x] **Quality Mandate**: `pytest` requires 90% coverage, `mypy` strict type checking will be enforced, and `ruff` linting applies. (Constitution V).
[x] **Environment**: `pyproject.toml` uses `pythonpath = ["src"]`. (Constitution Constraints).
[x] **Spec Directory**: Feature resides in `specs/006-rules-validation-parser/` following `NNN-short-name` convention. (Constitution VII).

## Project Structure

### Documentation (this feature)

```text
specs/006-rules-validation-parser/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── vindicta_foundation/
│   ├── models/
│   │   ├── __init__.py          # Updated: export new validation models
│   │   └── validation.py        # NEW: ValidationRequest, ValidationVerdict,
│   │                            #       ViolationReport, AugmentedAction,
│   │                            #       TranscriptIntegrityReport
│   └── validation/
│       ├── __init__.py          # Package init
│       ├── engine.py            # NEW: RulesValidator class (single + batch validation)
│       └── types.py             # NEW: ViolationType enum, verdict enums

tests/
├── unit/
│   ├── test_validation_models.py   # Model validation tests
│   └── test_validation_engine.py   # Engine logic tests with mocked RAG
└── integration/
    └── test_validation_pipeline.py # End-to-end with real storage (if available)
```

**Structure Decision**: The validation engine lives as a new `validation/` subpackage under `vindicta_foundation`, co-located with the existing `rag_pipeline/` and `models/`. Models are placed in `models/validation.py` following the existing convention (`models/economy.py`, `models/entropy.py`). The engine imports `RulesStorage` directly for in-process RAG queries.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected. Strict adherence to Foundation axioms.*

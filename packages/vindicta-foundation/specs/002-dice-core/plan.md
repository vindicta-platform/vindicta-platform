# Implementation Plan: dice-core

**Spec ID**: `002-dice-core` | **Branch**: `feat/dice-core` | **Date**: 2026-02-22 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/002-dice-core/spec.md`

## Summary

Implement a CSPRNG-backed dice engine with HMAC-SHA256 verifiable entropy proofs as a pure Python library module within `vindicta_foundation`. The engine uses Python's `secrets` module for cryptographic randomness (satisfying AX-03 and FR-001), provides commit-reveal style proofs for every roll (FR-002), and supports deterministic seeding strictly for CI/testing environments (FR-004). No external dependencies beyond stdlib + Pydantic.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: `pydantic>=2.10.0` (existing), `secrets`/`hmac`/`hashlib` (stdlib)  
**Storage**: N/A — pure in-memory library  
**Testing**: `pytest` with `pytest-cov`, `pytest-mock`  
**Target Platform**: Cross-platform (Linux, macOS, Windows)  
**Project Type**: Library module within `vindicta-foundation`  
**Performance Goals**: < 1ms per roll+proof generation (SC-003)  
**Constraints**: No external services, no `random` module in production paths, stdlib-only cryptography  
**Scale/Scope**: Single module, 4 source files, ~200-300 LOC

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate                                                  | Status | Notes                                                            |
| ----------------------------------------------------- | ------ | ---------------------------------------------------------------- |
| **AX-03 (Probability Source)**: Equal probability 1/N | ✅ PASS | `secrets.randbelow(N)` guarantees uniform distribution           |
| **Model Integrity**: Inherits VindictaModel           | ✅ PASS | `RollEntropy` and `RandomResult` inherit from `VindictaModel`    |
| **Quality Mandates**: 90% coverage, mypy, ruff        | ✅ PASS | Enforced by existing `pyproject.toml` config                     |
| **FR-003**: No predictable sources                    | ✅ PASS | `secrets` module only; `random` gated behind `TESTING` mode enum |
| **FR-005**: Pure Python, no external services         | ✅ PASS | All stdlib + Pydantic                                            |

**Post-Phase 1 Re-check**: All gates still passing. No violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/002-dice-core/
├── spec.md              # Feature specification (input)
├── plan.md              # This file
├── research.md          # Phase 0: Technical decisions
├── data-model.md        # Phase 1: Entity definitions
├── quickstart.md        # Phase 1: Usage examples
├── contracts/
│   └── api.md           # Phase 1: Public API contract
└── tasks.md             # Phase 2: Task breakdown (next step)
```

### Source Code (repository root)

```text
src/vindicta_foundation/
├── models/
│   ├── base.py          # VindictaModel (existing)
│   ├── entropy.py       # EntropyProof (existing - audit model)
│   └── __init__.py      # Exports (update needed)
├── dice/                # NEW module
│   ├── __init__.py      # Public re-exports (create_engine, RngMode, etc.)
│   ├── types.py         # RollEntropy, RandomResult, RngMode
│   ├── engine.py        # DiceEngine class, create_engine factory
│   └── errors.py        # SecurityError

tests/
├── test_models.py       # Existing model tests
├── test_dice_types.py   # NEW: RollEntropy, RandomResult validation
├── test_dice_engine.py  # NEW: DiceEngine roll + verify logic
└── test_dice_security.py # NEW: Mode guards, deterministic seeding
```

**Structure Decision**: Single project layout — new `dice/` submodule under existing `src/vindicta_foundation/`. No new top-level directories needed. The `dice/` module sits alongside `models/` as a sibling package within the foundation.

## Generated Artifacts

| Artifact         | Path                                   | Status     |
| ---------------- | -------------------------------------- | ---------- |
| research.md      | `specs/002-dice-core/research.md`      | ✅ Complete |
| data-model.md    | `specs/002-dice-core/data-model.md`    | ✅ Complete |
| contracts/api.md | `specs/002-dice-core/contracts/api.md` | ✅ Complete |
| quickstart.md    | `specs/002-dice-core/quickstart.md`    | ✅ Complete |

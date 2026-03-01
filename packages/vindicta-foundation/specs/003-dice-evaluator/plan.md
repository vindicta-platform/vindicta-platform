# Implementation Plan: dice-evaluator

**Spec ID**: `003-dice-evaluator` | **Branch**: `feat/dice-evaluator` | **Date**: 2026-02-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-dice-evaluator/spec.md`

## Summary

The dice-evaluator is an AST tree-walking evaluator that accepts strongly typed AST nodes (produced by `dice-parser`) and executes dice and arithmetic operations using `dice-core` for all randomness. It produces an `EvaluationResult` containing the final integer total, a step-by-step `ExecutionTrace`, and the cryptographic entropy proofs from `dice-core`. This is a pure Python library with no external service dependencies.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: Pydantic >=2.10.0 (via `VindictaModel`), internal `dice-core` module (CSPRNG + entropy), internal `dice-parser` module (AST nodes)
**Storage**: N/A (stateless computation)
**Testing**: pytest >=8.0.0, pytest-cov, pytest-mock (for deterministic seed injection)
**Target Platform**: Cross-platform Python library
**Project Type**: Library (internal module within `vindicta_foundation`)
**Performance Goals**: Standard attack expression resolves in <2ms (SC-003)
**Constraints**: Must use `dice-core` exclusively for RNG (FR-003, AX-03); no external service calls (FR-005 from dice-core)
**Scale/Scope**: Handles all standard tabletop mechanics: Keep Highest, Drop Lowest, Reroll, Exploding dice (FR-004)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate                                                                                          | Status | Notes                                                                                      |
| --------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| **AX-03 (Probability Source)**: Outcomes determined by N-faced die with equal probability 1/N | ✅ PASS | Evaluator delegates all RNG to `dice-core` CSPRNG; never generates randomness itself       |
| **II. Model Integrity**: All models inherit `VindictaModel`, exported in `__init__.py`        | ✅ PASS | `EvaluationResult`, `ExecutionTrace`, `TraceStep` will inherit `VindictaModel`             |
| **V. Quality Mandates**: 90% coverage, mypy strict, ruff                                      | ✅ PASS | pytest + mypy + ruff enforced via pyproject.toml and CI                                    |
| **FR-003**: Must rely exclusively on `dice-core` for RNG                                      | ✅ PASS | Evaluator accepts a `DiceRoller` protocol/interface from dice-core, never imports `random` |

## Project Structure

### Documentation (this feature)

```text
specs/003-dice-evaluator/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── evaluator-api.md
└── tasks.md             # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
src/vindicta_foundation/
├── models/
│   ├── base.py              # VindictaModel (existing)
│   ├── entropy.py           # EntropyProof (existing, from dice-core)
│   ├── evaluation.py        # EvaluationResult, ExecutionTrace, TraceStep [NEW]
│   └── __init__.py          # Updated exports
├── evaluator/
│   ├── __init__.py          # Public API re-exports
│   ├── protocols.py         # DiceRoller protocol, ASTNode protocol [NEW]
│   ├── engine.py            # Evaluator tree-walker [NEW]
│   └── errors.py            # EvaluationError hierarchy [NEW]
└── __init__.py

tests/
├── unit/
│   ├── test_evaluation_models.py   [NEW]
│   └── test_evaluator_engine.py    [NEW]
└── test_models.py                  (existing)
```

**Structure Decision**: Single project layout. The evaluator is added as a new `evaluator/` subpackage under `vindicta_foundation`, following the existing pattern of `models/` at the same level.

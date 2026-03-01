# Implementation Plan: dice-parser

**Spec ID**: `004-dice-parser` | **Branch**: `feat/dice-parser` | **Date**: 2026-02-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-dice-parser/spec.md`

## Summary

Implement a dice notation parser that translates standard wargaming dice expressions (e.g., `"2d6 + 3"`, `"4d6dl1"`, `"1d10e10"`) into a typed Abstract Syntax Tree (AST). The parser uses Lark's LALR(1) algorithm with a formal EBNF grammar, producing Pydantic V2 models that inherit from `VindictaModel`. The AST is designed for downstream consumption by a dice evaluator, with clean serialization and sub-millisecond parsing performance.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: Pydantic ≥2.10.0, Lark ≥1.2.0
**Storage**: N/A (pure computational library, no persistence)
**Testing**: pytest ≥8.0.0, pytest-cov
**Target Platform**: Cross-platform Python library (Linux, macOS, Windows)
**Project Type**: Library (in-tree module within `vindicta_foundation`)
**Performance Goals**: < 1ms parsing for typical expressions (< 50 chars) per SC-003
**Constraints**: Zero external runtime state; deterministic string→AST; all models frozen after parse
**Scale/Scope**: ~10 AST node types, ~15 grammar rules, single-module parser

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate                           | Requirement                                 | Status                                                                                            |
| ------------------------------ | ------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **II. Model Integrity**        | All models inherit from `VindictaModel`     | ✅ PASS — All AST nodes will inherit from `VindictaModel`                                          |
| **II. Model Integrity**        | New models exported in `models/__init__.py` | ✅ PASS — Will add all AST node exports                                                            |
| **V. Quality Mandates**        | 90% test coverage                           | ✅ PASS — Target 95%+ coverage via parametrized tests                                              |
| **V. Quality Mandates**        | `mypy` strict                               | ✅ PASS — All models fully typed, Lark Transformer typed                                           |
| **V. Quality Mandates**        | `ruff` clean                                | ✅ PASS — Will verify before commit                                                                |
| **AX-03 (Probability Source)** | Die defined as N-faced, equal probability   | ✅ PASS — Parser produces `DicePoolNode(count, sides)` matching the axiom; no randomness in parser |
| **IV. Documentation**          | Update C4 if boundaries change              | ✅ N/A — No container boundary changes; parser is a sub-module                                     |

## Project Structure

### Documentation (this feature)

```text
specs/004-dice-parser/
├── plan.md              # This file
├── research.md          # Phase 0 output — library research
├── data-model.md        # Phase 1 output — AST node schema
├── quickstart.md        # Phase 1 output — usage examples
├── contracts/
│   └── grammar.ebnf     # Phase 1 output — formal dice notation grammar
└── tasks.md             # Phase 2 output (/speckit-tasks command)
```

### Source Code (repository root)

```text
src/vindicta_foundation/
├── models/
│   ├── base.py              # VindictaModel (existing)
│   ├── dice_ast.py          # NEW — AST node models (DicePoolNode, BinaryOpNode, etc.)
│   └── __init__.py          # Updated — export new AST models
├── parser/
│   ├── __init__.py          # NEW — public API: parse_dice(expression: str) -> ASTNode
│   ├── grammar.py           # NEW — embedded Lark grammar string
│   ├── transformer.py       # NEW — Lark Transformer → AST node conversion
│   └── errors.py            # NEW — ParseError, InvalidDiceNotationError
└── __init__.py              # Existing

tests/
├── test_models.py           # Existing
├── test_dice_ast.py         # NEW — AST node serialization / validation tests
├── test_parser.py           # NEW — parse_dice() parametrized tests
└── test_parser_errors.py    # NEW — error path / malformed input tests
```

**Structure Decision**: Single project, library module. The parser lives under `src/vindicta_foundation/parser/` as a new sub-package alongside the existing `models/` package. AST models live in `models/dice_ast.py` to comply with the constitution's model integrity rules (all models in `models/`).

## Complexity Tracking

> No constitution violations. No complexity justification required.

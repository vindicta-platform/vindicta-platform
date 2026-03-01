# Research: dice-parser

**Feature**: dice-parser | **Date**: 2026-02-22

## Decision 1: Parsing Library

**Decision**: Use **Lark** (≥1.2.0) with the LALR(1) parsing algorithm.

**Rationale**:
- LALR(1) provides O(n) time complexity, comfortably meeting SC-003 (< 1ms for typical expressions).
- Declarative EBNF grammar keeps the grammar definition separate from transformation logic, improving maintainability.
- Automatic parse tree generation simplifies AST construction via Lark's `Transformer` class.
- Active development (v1.3.0 in Oct 2025), strong community, and well-documented.
- Zero-dependency (pure Python), aligning with the project's minimal dependency philosophy.

**Alternatives Considered**:

| Library                            | Rejected Because                                                                                                                                                      |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **pyparsing**                      | PEG-based, potentially exponential worst-case. Grammar defined inline in Python (less readable for a growing grammar). Slower for complex expressions per benchmarks. |
| **Hand-written recursive descent** | More boilerplate, harder to maintain as grammar evolves. No grammar validation tooling. Higher risk of bugs in operator precedence handling.                          |
| **PLY (Python Lex-Yacc)**          | Dated API, intrusive use of docstrings for rules, less ergonomic than Lark's EBNF format.                                                                             |

## Decision 2: AST Design Strategy

**Decision**: Typed discriminated union using Pydantic V2 models inheriting from `VindictaModel`.

**Rationale**:
- FR-003 mandates Pydantic models inheriting from `VindictaModel`.
- Pydantic V2's discriminated unions (via `Literal` type fields) enable clean JSON serialization with `model_validate_json()` and `model_dump_json()`, satisfying SC-004.
- Each AST node type is a concrete model (not generic) for full `mypy` strict compatibility.
- Using a `node_type` discriminator field enables downstream evaluators to pattern-match on the AST without `isinstance` chains.

**Alternatives Considered**:

| Approach                  | Rejected Because                                                                                        |
| ------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Python dataclasses**    | Constitution mandates `VindictaModel` inheritance; dataclasses would break model integrity.             |
| **Generic Tree[T]**       | Over-generic; loses type safety on node-specific fields. `mypy` strict would require excessive casting. |
| **Enum-based node types** | Requires separate payload classes anyway; discriminated unions are more idiomatic in Pydantic V2.       |

## Decision 3: Modifier Representation

**Decision**: Modifiers are represented as wrapper nodes that contain their base `DicePoolNode`, not as properties of `DicePoolNode`.

**Rationale**:
- Modifiers can be chained (e.g., keep highest then explode).
- Wrapper pattern keeps `DicePoolNode` simple and composable.
- Lark grammar naturally nests modifiers as outer rules wrapping the dice pool.
- Matches how wargaming rule engines think about modifiers: operations applied to a pool result.

## Decision 4: Error Strategy

**Decision**: Custom `ParseError` hierarchy with structured error context (position, expected tokens, input fragment).

**Rationale**:
- FR-004 mandates "descriptive, typed error messages."
- Lark raises `UnexpectedInput` with position info; wrapping it in a custom `ParseError` provides a stable API surface for downstream consumers.
- Error classes inherit from a base `DiceParserError` (which is a standard `Exception`, not a `VindictaModel` — errors are not domain entities).

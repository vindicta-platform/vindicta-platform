# Research: dice-evaluator

**Feature**: dice-evaluator | **Date**: 2026-02-22

## R1: AST Evaluation Strategy

**Decision**: Recursive tree-walking interpreter using the Visitor pattern

**Rationale**: The dice AST is a simple expression tree (arithmetic ops, dice pools, modifiers). A tree-walker is the simplest correct approach—no compilation step needed. The Visitor pattern cleanly separates node types from evaluation logic, making it easy to add new node types (e.g., new modifiers) without modifying the core traversal.

**Alternatives considered**:
- **Stack-based VM**: Overkill for expression evaluation. Adds compilation step with no performance benefit at this scale (<2ms target).
- **Direct recursive `evaluate()` methods on AST nodes**: Couples evaluation logic into the parser's domain. Violates separation of concerns; parser shouldn't know about `dice-core`.

---

## R2: Dependency Injection for dice-core

**Decision**: Define a `DiceRoller` Protocol (PEP 544) that the evaluator depends on. The `dice-core` module will provide the concrete implementation.

**Rationale**: Using a Protocol decouples the evaluator from the concrete `dice-core` implementation, enabling:
1. Deterministic testing via mock rollers with fixed seed sequences
2. Independent development of evaluator and dice-core
3. Clean constitutional compliance: the evaluator *structurally* cannot bypass `dice-core`

**Alternatives considered**:
- **Direct import of dice-core**: Creates tight coupling. Testing requires monkeypatching. Rejected.
- **Abstract base class (ABC)**: More ceremonial than Protocol for this use case. Protocol is idiomatic Pydantic/modern Python.

---

## R3: Execution Trace Design

**Decision**: Append-only list of `TraceStep` value objects, each recording one atomic operation with its inputs and outputs.

**Rationale**: Players need transparency ("show your work"). The trace must capture:
- Raw dice rolls before any modifier (SC-002)
- Which dice were kept/dropped and why
- Arithmetic operations with intermediate totals
- Final result derivation

An append-only list is simple, serializable (Pydantic), and matches the user-facing display order.

**Alternatives considered**:
- **Tree-structured trace mirroring the AST**: More complex to serialize and display. Flat list with labels is sufficient for the "combat log" use case.
- **Logging-based trace**: Not structured data; can't be programmatically consumed or serialized.

---

## R4: Error Handling Strategy

**Decision**: Custom `EvaluationError` hierarchy with strictly typed error variants.

**Rationale**: SC-004 requires strictly typed errors for malformed/invalid ASTs. A hierarchy enables callers to catch specific error types (e.g., `DivisionByZeroError`, `InvalidASTError`, `UnsupportedModifierError`).

**Alternatives considered**:
- **Generic ValueError/TypeError**: Insufficient specificity for SC-004 compliance.
- **Result monad pattern**: Adds complexity without clear benefit; Python convention favors exceptions for truly exceptional cases like invalid ASTs.

---

## R5: Modifier Implementation Pattern

**Decision**: Each modifier (Keep Highest, Drop Lowest, Reroll, Exploding) is a standalone function that transforms a `list[int]` → `list[int]` with trace metadata.

**Rationale**: Modifiers are pure transformations on rolled dice pools. Standalone functions are testable in isolation and compose cleanly. Each modifier receives the pool, applies its rule, and returns the filtered pool plus a `TraceStep` describing what was done.

**Alternatives considered**:
- **Modifier class hierarchy**: Over-engineered for stateless transformations. Functions are simpler.
- **Chained pipeline**: Modifiers don't typically chain in standard notation (you apply one modifier to a dice pool, not a pipeline). If chaining is needed later, functions compose naturally.

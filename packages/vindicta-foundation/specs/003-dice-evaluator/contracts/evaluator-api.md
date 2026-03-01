# Evaluator API Contract

**Feature**: dice-evaluator | **Date**: 2026-02-22
**Type**: Internal Python Library API

## Overview

The dice-evaluator exposes a single primary interface: the `Evaluator` class, which accepts AST nodes and produces `EvaluationResult` objects. All randomness is delegated via the injected `DiceRoller` protocol.

## Public API Surface

### `Evaluator` class

**Module**: `vindicta_foundation.evaluator.engine`

```python
class Evaluator:
    def __init__(self, roller: DiceRoller) -> None: ...
    def evaluate(self, ast: ASTNode) -> EvaluationResult: ...
```

| Method     | Input                             | Output             | Raises                                                                            |
| ---------- | --------------------------------- | ------------------ | --------------------------------------------------------------------------------- |
| `__init__` | `roller: DiceRoller`              | `None`             | —                                                                                 |
| `evaluate` | `ast: ASTNode` (from dice-parser) | `EvaluationResult` | `InvalidASTError`, `DivisionByZeroError`, `UnsupportedNodeError`, `ModifierError` |

### `DiceRoller` protocol

**Module**: `vindicta_foundation.evaluator.protocols`

```python
class DiceRoller(Protocol):
    def roll(self, sides: int, count: int = 1) -> RollResult: ...
```

### `RollResult` named tuple

**Module**: `vindicta_foundation.evaluator.protocols`

```python
class RollResult(NamedTuple):
    values: list[int]
    proof: EntropyProof
```

## Contract Guarantees

1. **Determinism**: Given the same AST and the same `DiceRoller` implementation producing the same values, `evaluate()` will always return the same `EvaluationResult`.
2. **Entropy completeness**: `EvaluationResult.entropy_proofs` contains exactly one `EntropyProof` per `roll()` call made during evaluation.
3. **Trace fidelity**: Every dice roll appears in the trace with `raw_values` populated before any modifier application (SC-002).
4. **Error specificity**: All error conditions raise from the `EvaluationError` hierarchy; no generic exceptions escape (SC-004).

## Supported AST Node Types

The evaluator must handle the following node types from `dice-parser`:

| Node Type            | Example Notation | Evaluation Behavior                              |
| -------------------- | ---------------- | ------------------------------------------------ |
| `DicePoolNode`       | `2d6`            | Call `roller.roll(sides=6, count=2)`             |
| `BinaryOpNode` (add) | `2d6 + 3`        | Evaluate left, evaluate right, sum               |
| `BinaryOpNode` (sub) | `2d6 - 1`        | Evaluate left, evaluate right, subtract          |
| `BinaryOpNode` (mul) | `2d6 * 2`        | Evaluate left, evaluate right, multiply          |
| `BinaryOpNode` (div) | `2d6 / 2`        | Evaluate left, evaluate right, integer divide    |
| `UnaryOpNode` (neg)  | `-3`             | Evaluate operand, negate result                  |
| `IntegerNode`        | `3`              | Return literal value                             |
| `ModifierNode` (kh)  | `2d20kh1`        | Roll pool, keep N highest                        |
| `ModifierNode` (kl)  | `4d6kl1`         | Roll pool, keep N lowest                         |
| `ModifierNode` (dh)  | `4d6dh1`         | Roll pool, drop N highest                        |
| `ModifierNode` (dl)  | `4d6dl1`         | Roll pool, drop N lowest                         |
| `ModifierNode` (r)   | `1d6r1`          | Roll, reroll if matching condition               |
| `ModifierNode` (e)   | `1d6e6`          | Roll, add extra roll on matching value (explode) |

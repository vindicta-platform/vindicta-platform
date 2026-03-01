# Quickstart: dice-evaluator

**Feature**: dice-evaluator | **Date**: 2026-02-22

## Prerequisites

- Python 3.12+
- `uv` package manager
- `vindicta-foundation` installed in dev mode

## Setup

```bash
cd .worktrees/dice-evaluator
uv sync --all-extras
```

## Quick Validation Scenarios

### Scenario 1: Evaluate a simple roll (US1)

```python
from vindicta_foundation.evaluator.engine import Evaluator
from vindicta_foundation.evaluator.protocols import DiceRoller

# Create a mock roller for testing (deterministic)
class MockRoller:
    def __init__(self, values: list[list[int]]):
        self._values = iter(values)
    
    def roll(self, sides: int, count: int = 1) -> "RollResult":
        from vindicta_foundation.evaluator.protocols import RollResult
        from vindicta_foundation.models.entropy import EntropyProof
        vals = next(self._values)
        proof = EntropyProof(seed_hash="a" * 64)
        return RollResult(values=vals[:count], proof=proof)

# Build a "2d6 + 3" AST manually
# (In production, dice-parser produces this)
roller = MockRoller(values=[[3, 5]])
evaluator = Evaluator(roller=roller)

# result = evaluator.evaluate(ast_node)
# assert result.total == 11  # 3 + 5 + 3
# assert len(result.trace.steps) >= 2  # roll step + arithmetic step
# assert len(result.entropy_proofs) == 1
```

### Scenario 2: Verify execution trace (US2)

```python
# Using the same result from Scenario 1:
# assert result.trace.steps[0].kind == "roll"
# assert result.trace.steps[0].raw_values == [3, 5]
# assert result.trace.summary == "[3, 5] + 3 = 11"
```

### Scenario 3: Keep Highest modifier (US1 - FR-004)

```python
# Build a "2d20kh1" AST manually
roller = MockRoller(values=[[7, 18]])
evaluator = Evaluator(roller=roller)

# result = evaluator.evaluate(kh_ast_node)
# assert result.total == 18
# assert result.trace.steps[1].kept_values == [18]
# assert result.trace.steps[1].dropped_values == [7]
```

## Running Tests

```bash
uv run pytest tests/ -v
```

## Type Checking

```bash
uv run mypy src/vindicta_foundation/evaluator/ --strict
```

# Contract: DiceEngine API

**Feature**: dice-core  
**Type**: Python Library (Pure API)  
**Date**: 2026-02-22

---

## Overview

The `dice-core` module exposes a pure Python API for generating cryptographically secure random dice rolls with verifiable entropy proofs. It has no external service dependencies (FR-005).

---

## Public API Surface

### Module: `vindicta_foundation.dice.engine`

#### `create_engine(mode: RngMode = RngMode.PRODUCTION, seed: int | None = None) -> DiceEngine`

Factory function to create a dice engine instance.

**Parameters**:
| Parameter | Type          | Required | Default      | Description                                     |
| --------- | ------------- | -------- | ------------ | ----------------------------------------------- |
| `mode`    | `RngMode`     | No       | `PRODUCTION` | Runtime mode selector                           |
| `seed`    | `int \| None` | No       | `None`       | Deterministic seed (only valid in TESTING mode) |

**Returns**: `DiceEngine` instance

**Raises**:
- `SecurityError`: If `seed` is provided with `mode=PRODUCTION`

**Example**:
```python
from vindicta_foundation.dice.engine import create_engine
from vindicta_foundation.dice.types import RngMode

# Production usage
engine = create_engine()

# Test usage
engine = create_engine(mode=RngMode.TESTING, seed=42)
```

---

#### `DiceEngine.roll(lower: int, upper: int, count: int = 1, context: str = "") -> RandomResult`

Generate random integers within a range with a cryptographic proof.

**Parameters**:
| Parameter | Type  | Required | Default | Description                                           |
| --------- | ----- | -------- | ------- | ----------------------------------------------------- |
| `lower`   | `int` | Yes      | —       | Minimum value (inclusive), must be >= 1               |
| `upper`   | `int` | Yes      | —       | Maximum value (inclusive), must be > lower            |
| `count`   | `int` | No       | `1`     | Number of values to generate                          |
| `context` | `str` | No       | `""`    | Contextual binding for the HMAC (game ID, turn, etc.) |

**Returns**: `RandomResult` with `.values`, `.entropy`

**Raises**:
- `ValueError`: If `lower < 1`, `upper <= lower`, or `count < 1`

**Example**:
```python
result = engine.roll(lower=1, upper=6, count=2, context="game-123:turn-5")
print(result.values)        # e.g., [3, 5]
print(result.entropy.commitment)  # HMAC-SHA256 hex digest
```

---

#### `RandomResult.verify() -> bool`

Verify the cryptographic proof that binds the result to its entropy source.

**Returns**: `True` if the commitment matches the seed; `False` otherwise.

**Example**:
```python
result = engine.roll(1, 6)
assert result.verify()  # Always True for untampered results
```

---

#### `RollEntropy.reveal() -> str`

Expose the raw seed as a hex string for external auditing.

**Returns**: Hex-encoded seed bytes.

**Example**:
```python
seed_hex = result.entropy.reveal()
# Auditor can recompute: hmac_sha256(bytes.fromhex(seed_hex), context) == commitment
```

---

## Error Types

| Error           | Module                            | When Raised                           |
| --------------- | --------------------------------- | ------------------------------------- |
| `SecurityError` | `vindicta_foundation.dice.errors` | Deterministic seed in PRODUCTION mode |
| `ValueError`    | builtin                           | Invalid roll parameters               |

---

## Module Layout

```
src/vindicta_foundation/dice/
├── __init__.py          # Public re-exports
├── engine.py            # DiceEngine implementation + create_engine factory
├── types.py             # RngMode enum, RollEntropy, RandomResult models
└── errors.py            # SecurityError
```

# Quickstart: dice-core

**Feature**: Dice Core — CSPRNG with Verifiable Entropy Proofs  
**Date**: 2026-02-22

---

## Prerequisites

- Python 3.12+
- `vindicta-foundation` package installed (`uv sync`)

---

## Basic Usage

### 1. Generate a Secure Dice Roll

```python
from vindicta_foundation.dice.engine import create_engine

engine = create_engine()
result = engine.roll(lower=1, upper=6)

print(f"Rolled: {result.values[0]}")
print(f"Proof: {result.entropy.commitment}")
```

### 2. Roll Multiple Dice

```python
result = engine.roll(lower=1, upper=6, count=3, context="battle-round-1")
print(f"Dice: {result.values}")  # e.g., [4, 2, 6]
```

### 3. Verify a Roll

```python
result = engine.roll(1, 20)
assert result.verify()  # Proof is valid
```

### 4. Audit a Roll (External Verifier)

```python
import hmac, hashlib

# Get the proof components
seed_hex = result.entropy.reveal()
commitment = result.entropy.commitment
context = result.entropy.context

# Recompute independently
seed_bytes = bytes.fromhex(seed_hex)
expected = hmac.new(seed_bytes, context.encode(), hashlib.sha256).hexdigest()
assert expected == commitment  # ✓ Fair roll confirmed
```

---

## Test Mode (CI/Automated Testing)

```python
from vindicta_foundation.dice.engine import create_engine
from vindicta_foundation.dice.types import RngMode

# Deterministic, reproducible rolls for testing
engine = create_engine(mode=RngMode.TESTING, seed=42)
result = engine.roll(1, 6)
# Same seed always produces same result
```

⚠️ **Warning**: `RngMode.TESTING` with a seed will raise `SecurityError` if `mode=PRODUCTION`.

---

## Validation Scenarios

| Scenario                | Expected Outcome                 | How to Verify                       |
| ----------------------- | -------------------------------- | ----------------------------------- |
| Single d6 roll          | `result.values[0]` in [1, 6]     | `assert 1 <= result.values[0] <= 6` |
| Proof verification      | `result.verify()` returns `True` | `assert result.verify()`            |
| Deterministic test mode | Same seed → same result          | Run twice with `seed=42`, compare   |
| Production + seed       | Raises `SecurityError`           | `pytest.raises(SecurityError)`      |
| 1000 d6 rolls           | Uniform distribution             | Chi-square p-value > 0.01           |

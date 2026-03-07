# TDD Workflow Reference

## The Red-Green-Refactor Cycle

```
┌──────────┐     ┌──────────┐     ┌──────────────┐
│   RED    │ ──→ │  GREEN   │ ──→ │   REFACTOR   │
│Write test│     │Make pass │     │ Clean up     │
│  (FAIL)  │     │(minimal) │     │(keep passing)│
└──────────┘     └──────────┘     └──────────────┘
      ↑                                   │
      └───────────────────────────────────┘
```

## Pytest Quick Reference

| Goal                          | Command                                           |
| :---------------------------- | :------------------------------------------------ |
| Run all tests                 | `uv run pytest`                                   |
| Run specific file             | `uv run pytest tests/test_foo.py`                 |
| Run specific test             | `uv run pytest tests/test_foo.py::test_bar`       |
| Run with coverage             | `uv run pytest --cov --cov-report=term-missing`   |
| Coverage with threshold       | `uv run pytest --cov --cov-fail-under=90`         |
| Verbose output                | `uv run pytest -v`                                |
| Stop on first failure         | `uv run pytest -x`                                |
| Run last failed               | `uv run pytest --lf`                              |
| Show local variables on fail  | `uv run pytest -l`                                |

## Test Organization

```text
packages/<package>/
├── src/<package_name>/
│   ├── __init__.py
│   └── module.py
└── tests/
    ├── __init__.py
    ├── conftest.py        # Shared fixtures
    ├── unit/
    │   └── test_module.py
    ├── integration/
    │   └── test_flows.py
    └── contract/
        └── test_api.py
```

## Writing Good Tests

### Naming Convention
```python
def test_<unit>_<scenario>_<expected_behavior>():
    """Test that <unit> does <expected> when <scenario>."""
```

### AAA Pattern (Arrange-Act-Assert)
```python
def test_dice_roll_within_bounds():
    # Arrange
    engine = DiceEngine(sides=6)

    # Act
    result = engine.roll()

    # Assert
    assert 1 <= result <= 6
```

### Fixtures
```python
import pytest

@pytest.fixture
def engine():
    """Provide a standard 6-sided dice engine."""
    return DiceEngine(sides=6)

def test_roll_returns_int(engine):
    assert isinstance(engine.roll(), int)
```

## Quality Gate Checklist

- [ ] Tests written BEFORE implementation code
- [ ] Tests fail for the correct reason (RED confirmed)
- [ ] Minimal code written to pass (GREEN confirmed)
- [ ] Coverage >= 90% for new logic
- [ ] No `Any` types without explicit justification
- [ ] No commented-out tests

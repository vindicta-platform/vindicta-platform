# Quickstart: Rules Validation Parser

**Feature Branch**: `006-rules-validation-parser`

## Prerequisites

- Python 3.12+
- `vindicta-foundation` installed with dev dependencies: `uv sync --all-extras`
- RAG storage populated (005-rag-pipeline must have ingested rules data)

## Single Action Validation

```python
from vindicta_foundation.models.validation import ValidationRequest
from vindicta_foundation.validation.engine import RulesValidator
from vindicta_foundation.rag_pipeline.storage import RulesStorage

# Assumes RulesStorage is already initialized with VectorStore + EmbeddingProvider
storage = RulesStorage(store=my_vector_store, embedder=my_embedder)
validator = RulesValidator(storage=storage)

# Create a validation request
request = ValidationRequest(
    unit_id="TAC-01",
    action_type="SHOOT",
    target="Enemy-01",
    weapon="Lascannon",
)

# Validate
verdict = validator.validate_action(request)

if verdict.status == "legal":
    print(f"Legal! Rules: {verdict.augmented_action.rules_text}")
elif verdict.status in ("illegal", "hallucination"):
    print(f"Violation: {verdict.violation.violation_type}")
    print(f"Expected: {verdict.violation.expected_values}")
elif verdict.status == "error":
    print(f"Error: {verdict.error_message}")
```

## Batch Transcript Validation

```python
actions = [
    ValidationRequest(unit_id="TAC-01", action_type="SHOOT", target="Enemy-01", weapon="Lascannon"),
    ValidationRequest(unit_id="CPT-01", action_type="ABILITY", ability="Oath of Moment"),
    ValidationRequest(unit_id="TAC-02", action_type="SHOOT", target="Enemy-02", weapon="Plasma Obliterator"),
]

report = validator.validate_transcript(actions)

print(f"Integrity: {report.integrity_pct:.1f}%")
print(f"Legal: {report.legal_count}, Illegal: {report.illegal_count}, Errors: {report.error_count}")

for v in report.violations_summary:
    print(f"  - {v.violation_type}: {v.offending_element}")
```

## Testing

```bash
# Run all validation tests
uv run pytest tests/unit/test_validation_models.py tests/unit/test_validation_engine.py -v

# Run with coverage
uv run pytest --cov=vindicta_foundation.validation --cov-report=term-missing
```

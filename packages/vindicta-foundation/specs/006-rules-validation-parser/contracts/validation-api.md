# Contract: Rules Validation Engine API

**Feature Branch**: `006-rules-validation-parser`
**Date**: 2026-02-23

## Python API Contract

The `RulesValidator` class exposes two public methods. All inputs and outputs are typed Pydantic models inheriting `VindictaModel`.

### `validate_action(request: ValidationRequest) -> ValidationVerdict`

Validates a single game action against the RAG rules database.

**Input**: `ValidationRequest` — a pre-parsed action object with `unit_id`, `action_type`, `target`, `weapon`, `ability` fields.

**Output**: `ValidationVerdict` with:
- `status`: One of `legal`, `illegal`, `hallucination`, `error`
- `augmented_action`: Present only when `status == legal` — includes full rules text, source URL, version
- `violation`: Present only when `status == illegal` or `hallucination` — includes violation type, offending element, expected values
- `error_message`: Present only when `status == error` — RAG unavailable

**Error handling**:
- RAG unavailable → returns `ValidationVerdict(status=ERROR, error_message="...")` (never raises)
- No results for query → returns `ValidationVerdict(status=ILLEGAL, violation=ViolationReport(violation_type=RULES_NOT_FOUND, ...))`

---

### `validate_transcript(requests: list[ValidationRequest]) -> TranscriptIntegrityReport`

Batch validates a list of actions and returns an aggregate report.

**Input**: `list[ValidationRequest]` — ordered list of pre-parsed actions.

**Output**: `TranscriptIntegrityReport` with:
- `verdicts`: One `ValidationVerdict` per input action (same order)
- `total_actions`, `legal_count`, `illegal_count`, `error_count`: Counts
- `integrity_pct`: `(legal_count / total_actions) * 100`
- `violations_summary`: Flattened list of all `ViolationReport` objects

**Invariants**:
- `len(verdicts) == len(requests) == total_actions`
- `legal_count + illegal_count + error_count == total_actions`
- If `total_actions == 0`, `integrity_pct == 100.0`

---

### Constructor

```python
class RulesValidator:
    def __init__(self, storage: RulesStorage) -> None:
        """Initialize validator with a RulesStorage dependency.

        Args:
            storage: The RAG storage module for rules lookups.
        """
```

The `RulesStorage` dependency uses protocol-based DI (see 005-rag-pipeline), making it mockable for testing.

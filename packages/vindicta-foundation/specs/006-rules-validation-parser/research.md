# Research: Rules Validation Parser

**Feature Branch**: `006-rules-validation-parser`
**Date**: 2026-02-23

## Research Decisions

### RD-001: Integration Pattern with RAG Storage

**Decision**: Import `RulesStorage` directly as a Python module dependency (in-process) rather than calling the MCP server as an HTTP/MCP client.

**Rationale**: The validator runs in the same Python process context as the RAG pipeline. Direct import avoids serialization overhead, eliminates network round-trip latency, and simplifies testing (mock `RulesStorage` protocols instead of standing up an MCP server). The MCP server remains the external interface for AI agents.

**Alternatives considered**:
- MCP client calls: Adds unnecessary latency (~50-100ms per query) and requires MCP client dependency. Rejected for in-process use.
- Abstract protocol that can back either: Over-engineered for MVP. The `RulesStorage` class already uses protocol-based DI (`VectorStore`, `EmbeddingProvider`), so it's inherently testable.

### RD-002: Input Contract Design

**Decision**: Accept pre-parsed, typed `ValidationRequest` dataclass objects. This feature does not parse WARScribe notation strings.

**Rationale**: Clean separation of concerns. The upstream parser (001-ocr-parser or future WARScribe parser) owns text-to-struct transformation. This feature focuses solely on validation logic — mapping structured actions to rules and producing verdicts.

**Alternatives considered**:
- Accept raw WARScribe strings: Conflates parsing and validation responsibilities. Rejected.
- Support both: Adds complexity with negligible benefit; upstream parser is already planned.

### RD-003: Violation Type Taxonomy

**Decision**: Use a Python `StrEnum` for violation types with the following members: `weapon_not_found`, `ability_not_found`, `illegal_action`, `rules_not_found`, `loadout_ambiguous`, `version_mismatch`.

**Rationale**: `StrEnum` (Python 3.11+) provides type safety, serialization to JSON strings, and exhaustive match support. The taxonomy covers all edge cases identified in the spec — from missing database entries to version conflicts.

**Alternatives considered**:
- Plain string literals: No type safety, easy to typo. Rejected.
- Integer enum: Not human-readable in logs and reports. Rejected.

### RD-004: Integrity Score Calculation

**Decision**: Simple ratio: `integrity_pct = (legal_actions / total_actions) * 100`. No weighting by violation severity.

**Rationale**: Keeps the MVP testable and deterministic. Weighted scoring introduces subjective severity assignments that require real-world calibration data we don't have yet. Can be evolved post-MVP.

**Alternatives considered**:
- Weighted ratio by violation severity: Requires severity calibration. Deferred.
- Binary pass/fail threshold: Too coarse; loses granular information.

### RD-005: Validation Engine Pattern

**Decision**: Implement `RulesValidator` class with protocol-based dependency injection for `RulesStorage`, following the same pattern used in `storage.py` for `VectorStore`/`EmbeddingProvider`.

**Rationale**: Consistent with existing codebase patterns. The `RulesStorage` dependency can be mocked in tests using the existing protocol pattern, enabling unit tests without ChromaDB or Ollama running.

**Alternatives considered**:
- Functional approach (pure functions): Loses the DI benefits and makes mocking harder. Rejected.
- Factory pattern: Over-engineered for a single dependency. Rejected.

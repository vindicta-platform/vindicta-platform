# Tasks: Rules Validation Parser

**Input**: Design documents from `/specs/006-rules-validation-parser/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for the validation engine

- [ ] T001 Create validation package directory structure: `src/vindicta_foundation/validation/__init__.py`, `src/vindicta_foundation/validation/types.py`, `src/vindicta_foundation/validation/engine.py`
- [ ] T002 [P] Create test directory structure: `tests/unit/test_validation_models.py`, `tests/unit/test_validation_engine.py`, `tests/integration/test_validation_pipeline.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core type definitions and domain models that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 [P] Implement `ViolationType` and `VerdictStatus` StrEnum types in `src/vindicta_foundation/validation/types.py` per data-model.md (6 violation types + 4 verdict statuses)
- [ ] T004 Implement `ValidationRequest` model extending `VindictaModel` in `src/vindicta_foundation/models/validation.py` with fields: `unit_id` (str), `action_type` (str), `target` (str | None), `weapon` (str | None), `ability` (str | None)
- [ ] T005 Implement `ViolationReport` model extending `VindictaModel` in `src/vindicta_foundation/models/validation.py` with fields: `violation_type` (ViolationType), `offending_element` (str), `expected_values` (list[str]), `rules_text` (str | None), `source_url` (str | None), `rules_version` (int | None)
- [ ] T006 Implement `AugmentedAction` model extending `VindictaModel` in `src/vindicta_foundation/models/validation.py` with fields: `request` (ValidationRequest), `rules_text` (str), `source_url` (str), `rules_version` (int)
- [ ] T007 Implement `ValidationVerdict` model extending `VindictaModel` in `src/vindicta_foundation/models/validation.py` with fields: `request` (ValidationRequest), `status` (VerdictStatus), `augmented_action` (AugmentedAction | None), `violation` (ViolationReport | None), `error_message` (str | None). Add model validators: `augmented_action` MUST be None when status is not LEGAL; `violation` MUST be None when status is LEGAL (depends on T004-T006)
- [ ] T008 Implement `TranscriptIntegrityReport` model extending `VindictaModel` in `src/vindicta_foundation/models/validation.py` with fields: `verdicts` (list[ValidationVerdict]), `total_actions` (int), `legal_count` (int), `illegal_count` (int), `error_count` (int), `integrity_pct` (float), `violations_summary` (list[ViolationReport]). Add computed validator: `integrity_pct` MUST equal `(legal_count / total_actions) * 100` (depends on T007)
- [ ] T009 Update `src/vindicta_foundation/models/__init__.py` to export all new validation models: `ValidationRequest`, `ValidationVerdict`, `ViolationReport`, `AugmentedAction`, `TranscriptIntegrityReport` (depends on T004-T008)
- [ ] T010 Write unit tests for all validation models in `tests/unit/test_validation_models.py` covering: field validation, VindictaModel inheritance (id/created_at), model validators (augmented_action/violation exclusivity), integrity_pct computation, ViolationType/VerdictStatus enum members (depends on T003-T009)

**Checkpoint**: Foundation ready — all models validated, all enums defined, exports verified

---

## Phase 3: User Story 1 — Validate Transcribed Actions Against Rules (Priority: P1) 🎯 MVP

**Goal**: Accept a single `ValidationRequest` and return a `ValidationVerdict` (legal/illegal/hallucination/error) by querying `RulesStorage.search()`

**Independent Test**: Submit a single annotated action (e.g., `ValidationRequest(unit_id="TAC-01", action_type="SHOOT", weapon="Lascannon")`) and verify the system returns the correct verdict with supporting evidence

### Implementation for User Story 1

- [ ] T011 [US1] Implement `RulesValidator.__init__(self, storage: RulesStorage)` constructor in `src/vindicta_foundation/validation/engine.py` with protocol-based DI for `RulesStorage` dependency and `logging.getLogger(__name__)` setup (FR-008)
- [ ] T012 [US1] Implement `RulesValidator.validate_action(request: ValidationRequest) -> ValidationVerdict` in `src/vindicta_foundation/validation/engine.py`: query `self._storage.search()` with constructed search string from request fields, parse results to match weapon/ability, produce LEGAL verdict with `AugmentedAction` or ILLEGAL/HALLUCINATION verdict with `ViolationReport` (FR-001, FR-002, FR-003, FR-004)
- [ ] T013 [US1] Implement graceful error handling in `validate_action`: wrap `storage.search()` in try/except, return `ValidationVerdict(status=ERROR, error_message=...)` when RAG is unavailable — never raise exceptions (FR-007, SC-004)
- [ ] T014 [US1] Implement version mismatch detection in `validate_action`: compare result metadata version against latest, flag `version_mismatch` if transcript references deprecated wording (FR-006)
- [ ] T015 [US1] Implement `loadout_ambiguous` advisory: when multiple results match with similar confidence, return closest match with `loadout_ambiguous` violation type instead of hard failure (spec edge case L68)
- [ ] T016 [US1] Add structured logging for all validation operations in `src/vindicta_foundation/validation/engine.py`: log query, verdict, violation details, and timing per FR-008
- [ ] T017 [US1] Write unit tests for `validate_action` in `tests/unit/test_validation_engine.py` covering: legal weapon match, weapon_not_found, ability_not_found, rules_not_found (empty RAG), hallucination detection, error state when storage raises, version_mismatch, loadout_ambiguous — mock `RulesStorage` using protocol pattern (SC-001)

**Checkpoint**: Single action validation fully functional and tested independently

---

## Phase 4: User Story 2 — Augment Game State with Rules Text (Priority: P2)

**Goal**: Enriched legal actions include full rules text, weapon profiles, ability descriptions, source URL, and rules version

**Independent Test**: Submit a valid action, confirm it passes validation, and inspect the returned `AugmentedAction` to verify full rules text and source citation are attached

### Implementation for User Story 2

- [ ] T018 [US2] Enhance `AugmentedAction` population in `validate_action` to include: full weapon profile text (Range, Attacks, BS, S, AP, D), full ability text with conditions, source URL from RAG metadata, and rules version from metadata version field in `src/vindicta_foundation/validation/engine.py`
- [ ] T019 [US2] Write unit tests for augmented action completeness in `tests/unit/test_validation_engine.py` covering: weapon profile fields present (SC-002), ability text with conditions present, source_url populated from RAG metadata, rules_version populated from RAG metadata version

**Checkpoint**: Legal actions return fully augmented state with rules text — downstream consumers (Debate Engine) can consume without additional RAG queries (SC-005)

---

## Phase 5: User Story 3 — Batch Validate a Full Transcript (Priority: P3)

**Goal**: Process a list of `ValidationRequest` objects and produce a `TranscriptIntegrityReport` with per-action verdicts and overall integrity percentage

**Independent Test**: Submit a multi-action transcript fixture (40 actions, 3 planted violations) and verify the report contains correct per-action verdicts and `integrity_pct = (37/40) * 100 = 92.5`

### Implementation for User Story 3

- [ ] T020 [US3] Implement `RulesValidator.validate_transcript(requests: list[ValidationRequest]) -> TranscriptIntegrityReport` in `src/vindicta_foundation/validation/engine.py`: iterate requests calling `validate_action` per-item, aggregate counts, compute `integrity_pct = (legal_count / total_actions) * 100`, flatten violations into `violations_summary` (FR-005)
- [ ] T021 [US3] Handle empty transcript edge case in `validate_transcript`: if `total_actions == 0`, return `integrity_pct = 100.0` per contract invariant
- [ ] T022 [US3] Add batch-level logging in `validate_transcript`: log total actions, legal/illegal/error counts, integrity percentage, and total elapsed time (FR-008, SC-003)
- [ ] T023 [US3] Write unit tests for `validate_transcript` in `tests/unit/test_validation_engine.py` covering: batch with all legal, batch with mixed verdicts (verify integrity_pct), batch with errors (RAG down), empty transcript edge case, verify len(verdicts) == total_actions invariant, verify violations_summary contains all violations

**Checkpoint**: Full transcript validation works end-to-end with correct integrity scoring

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Quality gates, documentation, and integration readiness

- [ ] T024 [P] Export `RulesValidator` from `src/vindicta_foundation/validation/__init__.py` and add module docstring
- [ ] T025 [P] Write integration test in `tests/integration/test_validation_pipeline.py` exercising `RulesValidator` with a real `RulesStorage` (mocked `VectorStore` + `EmbeddingProvider`) to verify end-to-end latency under 10s for 50 actions (SC-003)
- [ ] T026 Validate 90% test coverage using `uv run pytest --cov=vindicta_foundation.validation --cov-report=term-missing`
- [ ] T027 [P] Run `ruff check .` and `ruff format --check .` to ensure linting compliance (Constitution V)
- [ ] T028 [P] Run `mypy --strict` across `src/vindicta_foundation/validation/` and `src/vindicta_foundation/models/validation.py` (Constitution V)
- [ ] T029 Run `specs/006-rules-validation-parser/quickstart.md` examples manually to validate correctness

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 (Phase 3) → US2 (Phase 4) → US3 (Phase 5): Sequential dependency chain (US2 enhances US1's augmentation, US3 wraps US1's single-action method)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — core validation engine
- **User Story 2 (P2)**: Depends on US1 (enriches the `AugmentedAction` produced by `validate_action`)
- **User Story 3 (P3)**: Depends on US1 (calls `validate_action` per-item in batch)

### Within Each User Story

- Models before engine methods
- Core implementation before edge cases
- Engine logic before logging
- Implementation before tests

### Parallel Opportunities

- T001 + T002: Setup directories in parallel
- T003 (types.py) is parallel with T004-T006 (validation.py), but T004-T006 are sequential (same file)
- T024 + T025 + T027 + T028: All polish tasks in parallel

---

## Parallel Example: Phase 2 (Foundation)

```bash
# T003 is parallel with T004 (different files):
Task T003: "ViolationType + VerdictStatus enums in validation/types.py"
Task T004: "ValidationRequest model in models/validation.py"  # T005-T006 follow sequentially in same file
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1 (single action validation)
4. **STOP and VALIDATE**: Test `validate_action` independently with mocked storage
5. Deliver core validation capability

### Incremental Delivery

1. Complete Setup + Foundational → Models + enums ready
2. Add User Story 1 → Single action validation → Test independently (MVP!)
3. Add User Story 2 → Full rules text augmentation → Test independently
4. Add User Story 3 → Batch transcript validation → Test independently
5. Polish → Coverage, linting, integration test

### Sequential Rationale

Unlike some features where user stories are independent, this feature's stories build on each other:
- US2 enriches the output of US1's `validate_action`
- US3 wraps US1's `validate_action` in a batch loop
- Therefore, the stories should be implemented sequentially (P1 → P2 → P3)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- All models MUST inherit VindictaModel (Constitution II)
- Mock `RulesStorage` using protocol pattern from 005-rag-pipeline for unit tests
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently

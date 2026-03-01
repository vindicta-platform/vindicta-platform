# Tasks: dice-evaluator

**Input**: Design documents from `/specs/003-dice-evaluator/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/evaluator-api.md ✅

**Tests**: Not explicitly requested in the feature specification. Test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and evaluator module scaffolding

- [ ] T001 Create evaluator package directory structure at `src/vindicta_foundation/evaluator/__init__.py`
- [ ] T002 [P] Create error hierarchy in `src/vindicta_foundation/evaluator/errors.py` with `EvaluationError`, `InvalidASTError`, `DivisionByZeroError`, `UnsupportedNodeError`, `ModifierError`
- [ ] T003 [P] Create protocols module in `src/vindicta_foundation/evaluator/protocols.py` with `DiceRoller` protocol and `RollResult` named tuple

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain models that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create `TraceStep` model with `kind`, `description`, `raw_values`, `kept_values`, `dropped_values`, `intermediate_total` fields in `src/vindicta_foundation/models/evaluation.py`
- [ ] T005 Create `ExecutionTrace` model with `steps` list and `summary` field plus `add_step()` method in `src/vindicta_foundation/models/evaluation.py`
- [ ] T006 Create `EvaluationResult` model with `total`, `trace`, `entropy_proofs`, `expression_repr` fields in `src/vindicta_foundation/models/evaluation.py`
- [ ] T007 Export `EvaluationResult`, `ExecutionTrace`, `TraceStep` in `src/vindicta_foundation/models/__init__.py`

**Checkpoint**: Foundation ready — evaluator engine implementation can now begin

---

## Phase 3: User Story 1 — Evaluating Standard Dice Rolls (Priority: P1) 🎯 MVP

**Goal**: Evaluate complex mathematical and dice expressions via AST tree-walking, producing numeric results using `dice-core` for all RNG.

**Independent Test**: Provide handcrafted ASTs directly to the evaluator and verify numeric outputs against known values using a deterministic mock `DiceRoller`.

### Implementation for User Story 1

- [ ] T008 [US1] Implement core `Evaluator` class with `__init__(roller: DiceRoller)` and `evaluate(ast: ASTNode) -> EvaluationResult` skeleton in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T009 [US1] Implement `_evaluate_integer_node()` handler for literal integer AST nodes in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T010 [US1] Implement `_evaluate_dice_pool_node()` handler that calls `roller.roll()` and records a `TraceStep` in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T011 [US1] Implement `_evaluate_binary_op_node()` handler for `+`, `-`, `*`, `/` with `DivisionByZeroError` guard in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T012 [US1] Implement `_apply_keep_highest()` modifier function that filters a dice pool and records kept/dropped values in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T013 [US1] Implement `_apply_keep_lowest()` modifier function in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T014 [US1] Implement `_apply_drop_highest()` modifier function in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T015 [US1] Implement `_apply_drop_lowest()` modifier function in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T016 [US1] Implement `_apply_reroll()` modifier function that re-invokes `roller.roll()` for matching values in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T017 [US1] Implement `_apply_exploding()` modifier function that adds bonus rolls when values match threshold in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T018 [US1] Implement `_evaluate_modified_dice_node()` handler that dispatches to the correct modifier function in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T019 [US1] Wire all node handlers into the main `evaluate()` dispatch and assemble `EvaluationResult` with entropy proofs in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T020 [US1] Export `Evaluator` from `src/vindicta_foundation/evaluator/__init__.py`

**Checkpoint**: Evaluator can process any valid AST and return correct numeric totals with entropy proofs

---

## Phase 4: User Story 2 — Execution Trace Generation (Priority: P2)

**Goal**: Produce a structured step-by-step resolution trace showing intermediate values, dropped dice, and modifiers for combat log display.

**Independent Test**: Assert that the evaluator's `EvaluationResult` includes a complete `ExecutionTrace` with correct `TraceStep` entries matching the requested operations and a human-readable `summary` string.

### Implementation for User Story 2

- [ ] T021 [US2] Enhance `_evaluate_dice_pool_node()` to populate `TraceStep.raw_values` with the full unmodified roll results in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T022 [US2] Enhance all modifier functions to populate `TraceStep.kept_values`, `TraceStep.dropped_values`, and `TraceStep.description` with human-readable detail in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T023 [US2] Enhance `_evaluate_binary_op_node()` to record arithmetic `TraceStep` entries with `intermediate_total` in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T024 [US2] Implement `ExecutionTrace.summary` generation that composes a human-readable string from all steps (e.g., `"[3, 5] + 3 = 11"`) in `src/vindicta_foundation/evaluator/engine.py`
- [ ] T025 [US2] Add validation that `entropy_proofs` count matches the number of `"roll"` kind `TraceStep` entries in `src/vindicta_foundation/models/evaluation.py`

**Checkpoint**: Evaluator returns full execution traces with human-readable summaries suitable for combat log display

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Quality improvements, documentation, and cross-cutting validation

- [ ] T026 [P] Add type annotations and ensure `mypy --strict` passes for `src/vindicta_foundation/evaluator/` directory
- [ ] T027 [P] Ensure `ruff check .` and `ruff format --check .` pass for all new files
- [ ] T028 [P] Update `src/vindicta_foundation/__init__.py` to expose evaluator public API if appropriate
- [ ] T029 Run quickstart.md validation scenarios end-to-end
- [ ] T030 Verify 90% test coverage for evaluator module with `uv run pytest --cov=vindicta_foundation.evaluator`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on User Story 1 (enhances existing handlers)
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on other stories
- **User Story 2 (P2)**: Enhances US1 implementation — REQUIRES US1 complete first (trace detail builds on existing handlers)

### Within Each User Story

- Models before services
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T002 and T003 (errors + protocols) can run in parallel within Phase 1
- T026, T027, T028 can run in parallel within Phase 5
- Within US1: T012–T017 (modifier functions) could be parallelized if split into separate files

---

## Parallel Example: Phase 1

```bash
# Launch all Setup tasks in parallel:
Task: "Create error hierarchy in src/vindicta_foundation/evaluator/errors.py"
Task: "Create protocols module in src/vindicta_foundation/evaluator/protocols.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test evaluator with mock roller and handcrafted ASTs
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP!)
3. Add User Story 2 → Test independently → Demo
4. Each story adds value without breaking previous stories

---

## Summary

| Metric                     | Value                     |
| -------------------------- | ------------------------- |
| **Total tasks**            | 30                        |
| **Phase 1 (Setup)**        | 3 tasks                   |
| **Phase 2 (Foundational)** | 4 tasks                   |
| **Phase 3 (US1 — MVP)**    | 13 tasks                  |
| **Phase 4 (US2)**          | 5 tasks                   |
| **Phase 5 (Polish)**       | 5 tasks                   |
| **Parallel opportunities** | T002∥T003, T026∥T027∥T028 |
| **MVP scope**              | Phases 1–3 (20 tasks)     |
| **US2 dependency**         | Requires US1 complete     |

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

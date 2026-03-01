# Tasks: dice-core

**Input**: Design documents from `/specs/01-dice-core/`  
**Prerequisites**: plan.md ✅, spec.md ✅, data-model.md ✅, contracts/api.md ✅, research.md ✅, quickstart.md ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Includes exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, module scaffolding, and error types

- [ ] T001 Create dice module package at `src/vindicta_foundation/dice/__init__.py` with public re-exports
- [ ] T002 [P] Create error types in `src/vindicta_foundation/dice/errors.py` (SecurityError)
- [ ] T003 [P] Create `RngMode` enum in `src/vindicta_foundation/dice/types.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models that both user stories depend on — MUST complete before user story work

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Implement `RollEntropy` model in `src/vindicta_foundation/dice/types.py` inheriting from `VindictaModel` with seed, commitment, algorithm, context fields, `verify()` and `reveal()` methods
- [ ] T005 Implement `RandomResult` model in `src/vindicta_foundation/dice/types.py` inheriting from `VindictaModel` with values, lower_bound, upper_bound, entropy fields, `verify()` method, and field validators
- [ ] T006 Update `src/vindicta_foundation/dice/__init__.py` to export `RollEntropy`, `RandomResult`, `RngMode`, `SecurityError`
- [ ] T007 Update `src/vindicta_foundation/models/__init__.py` to add `RollEntropy` and `RandomResult` to `__all__` exports

**Checkpoint**: Foundation models ready — DiceEngine implementation can begin

---

## Phase 3: User Story 1 — Secure Randomness Generation (Priority: P1) 🎯 MVP

**Goal**: Implement the CSPRNG-backed dice engine that generates cryptographically secure random integers using `secrets.randbelow()`

**Independent Test**: Generate 10,000 d6 rolls and verify chi-square goodness-of-fit test passes with p > 0.01

### Implementation for User Story 1

- [ ] T008 [US1] Implement `CsprngEngine` class in `src/vindicta_foundation/dice/engine.py` with `roll(lower, upper, count, context)` method using `secrets.randbelow()` for random generation and HMAC-SHA256 for commitment
- [ ] T009 [US1] Implement `DeterministicEngine` class in `src/vindicta_foundation/dice/engine.py` using `random.Random(seed)` for reproducible testing
- [ ] T010 [US1] Implement `create_engine(mode, seed)` factory function in `src/vindicta_foundation/dice/engine.py` with production/testing mode guard (raises `SecurityError` if seed provided in PRODUCTION mode)
- [ ] T011 [US1] Update `src/vindicta_foundation/dice/__init__.py` to export `create_engine`
- [ ] T012 [US1] Write unit tests in `tests/test_dice_engine.py`: roll returns values in range, roll count matches, deterministic engine with same seed produces same results, production mode rejects seed, roll with count=1 and count=N
- [ ] T013 [US1] Write statistical validation test in `tests/test_dice_engine.py`: chi-square uniformity test over 10,000 d6 rolls with p > 0.01

**Checkpoint**: At this point, `create_engine().roll(1, 6)` produces cryptographically secure random results. User Story 1 is fully functional and independently testable.

---

## Phase 4: User Story 2 — Verifiable Entropy Proofs (Priority: P1)

**Goal**: Ensure every roll includes a cryptographic proof (HMAC-SHA256 commitment) that an external auditor can independently verify

**Independent Test**: Generate a roll, extract the proof components, and recompute the HMAC independently to confirm the result was derived fairly

### Implementation for User Story 2

- [ ] T014 [US2] Write verification tests in `tests/test_dice_verification.py`: `result.verify()` returns True for untampered results, `result.verify()` returns False when commitment is altered, `RollEntropy.reveal()` returns hex-encoded seed, independent HMAC recomputation matches commitment
- [ ] T015 [US2] Write auditor integration test in `tests/test_dice_verification.py`: full commit-reveal-verify cycle — generate roll, extract seed via `reveal()`, recompute HMAC with `hmac.new(seed_bytes, context, sha256)`, assert matches `entropy.commitment`

**Checkpoint**: At this point, every roll is cryptographically verifiable. An external auditor can independently confirm roll fairness using only the seed, context, and commitment.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Type checking, linting, coverage, and documentation

- [ ] T016 [P] Run `mypy` strict type checking on `src/vindicta_foundation/dice/` and fix any type errors
- [ ] T017 [P] Run `ruff check .` and `ruff format --check .` to verify linting and formatting compliance
- [ ] T018 Verify test coverage meets 90% minimum with `uv run pytest --cov=vindicta_foundation --cov-report=term-missing`
- [ ] T019 [P] Run quickstart.md validation: execute all code examples from `specs/01-dice-core/quickstart.md` in a Python REPL to confirm correctness
- [ ] T020 Update `src/vindicta_foundation/dice/__init__.py` module docstring with constitutional compliance notes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) — implements the engine
- **User Story 2 (Phase 4)**: Depends on User Story 1 (Phase 3) — tests the proof mechanism that US1 builds
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — core engine implementation
- **User Story 2 (P1)**: Depends on US1 completion — US2 verifies the proofs that US1 generates. Cannot test verification without a working engine.

### Within Each User Story

- Models → Services/Engine → Tests
- Core implementation before integration tests

### Parallel Opportunities

- T002 + T003 can run in parallel (different files, Phase 1)
- T016 + T017 + T019 can run in parallel (different concerns, Phase 5)
- Within US1: T008 + T009 are sequential (same file) but T012 + T013 can be parallelized

---

## Parallel Example: Phase 1 Setup

```bash
# Launch all Phase 1 tasks together:
Task: "Create dice module package at src/vindicta_foundation/dice/__init__.py"
Task: "Create error types in src/vindicta_foundation/dice/errors.py"
Task: "Create RngMode enum in src/vindicta_foundation/dice/types.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (module structure)
2. Complete Phase 2: Foundational (RollEntropy + RandomResult models)
3. Complete Phase 3: User Story 1 (DiceEngine + create_engine)
4. **STOP and VALIDATE**: `engine.roll(1, 6)` returns valid RandomResult with proof
5. Chi-square test passes

### Incremental Delivery

1. Setup + Foundational → Models ready
2. Add User Story 1 → Engine works → Roll generates secure random values (MVP!)
3. Add User Story 2 → Proofs are externally auditable
4. Polish → Type-safe, linted, 90%+ coverage

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US2 depends on US1 (verification needs a working engine to test against)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently

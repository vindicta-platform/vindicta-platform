# Tasks: Simulation Stat Retrieval

**Input**: Design documents from `specs/001-simulation-stat-retrieval/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), quickstart.md (✓)

**Tests**: Tests included — the constitution mandates 90% coverage and `uv run pytest`.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Engine Subsystem**: `src/vindicta_engine/` at repository root (`vindicta-engine/`)
- **Tests**: `tests/` at repository root (`vindicta-engine/`)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the `retrieval` subpackage scaffold and install dependencies

- [ ] T001 Create retrieval subpackage directory with `__init__.py` at src/vindicta_engine/retrieval/__init__.py
- [ ] T002 Add `mcp` SDK dependency to vindicta-engine/pyproject.toml
- [ ] T003 [P] Create test directory structure at tests/retrieval/__init__.py
- [ ] T004 [P] Add `pytest-asyncio` to dev dependencies in vindicta-engine/pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared data models and base types that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Create `StatModifier` Pydantic model (type, value, condition fields) inheriting from VindictaModel in src/vindicta_engine/retrieval/models.py
- [ ] T006 [P] Create `WeaponStatLine` Pydantic model (weapon_name, range, attacks, hit_on, strength, ap, damage, modifiers fields) inheriting from VindictaModel in src/vindicta_engine/retrieval/models.py
- [ ] T007 Create `UnitProfile` Pydantic model (unit_name, rules_version, movement, toughness, save, wounds, leadership, oc, weapons fields) inheriting from VindictaModel in src/vindicta_engine/retrieval/models.py
- [ ] T008 [P] Create `CacheMetrics` dataclass (hits, misses, parse_errors, total_query_latency_ms counters) in src/vindicta_engine/retrieval/metrics.py
- [ ] T009 [P] Create `RAGQueryError` and `StatParseError` exception classes in src/vindicta_engine/retrieval/exceptions.py
- [ ] T010 Write unit tests for all foundational models (construction, validation, serialization) in tests/retrieval/test_models.py

**Checkpoint**: Foundation ready — all data models validated and exportable. User story implementation can now begin.

---

## Phase 3: User Story 1 — Load Unit Stats for Combat Simulation (Priority: P1) 🎯 MVP

**Goal**: The simulation engine queries the RAG MCP server for a unit's profile and weapon stats and receives a fully populated `UnitProfile` object.

**Independent Test**: Request "Intercessor Squad" from the RAG server and verify the returned `UnitProfile` has correct combat parameters matching the canonical source.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Unit test for `RAGClient.query_unit_stats()` with mocked MCP responses in tests/retrieval/test_mcp_client.py
- [ ] T012 [P] [US1] Unit test for `RAGClient` retry logic — verify exactly 1 retry after ~500ms on failure, then raises `RAGQueryError` in tests/retrieval/test_mcp_client.py
- [ ] T013 [P] [US1] Integration test for full stat retrieval flow: query → parse → return `UnitProfile` in tests/retrieval/test_integration.py

### Implementation for User Story 1

- [ ] T014 [US1] Implement `RAGClient` class with async `query_unit_stats(unit_name: str, version: str)` method using `mcp` SDK in src/vindicta_engine/retrieval/mcp_client.py
- [ ] T015 [US1] Implement retry logic in `RAGClient` — catch connection errors, wait ~500ms, retry once, then raise `RAGQueryError` with context in src/vindicta_engine/retrieval/mcp_client.py
- [ ] T016 [US1] Implement timeout handling — ensure total query time (including retry) stays within 3-second budget per SC-004 in src/vindicta_engine/retrieval/mcp_client.py
- [ ] T017 [US1] Export `RAGClient` and all retrieval models from src/vindicta_engine/retrieval/__init__.py

**Checkpoint**: `RAGClient` can query the RAG server and return raw markdown. Retry logic verified. US1 is independently testable.

---

## Phase 4: User Story 3 — Parse RAG Markdown into Structured Stat Objects (Priority: P1)

**Goal**: A parser converts raw markdown from the RAG server into populated `UnitProfile` objects with all weapon stat lines and recognized modifiers.

**Independent Test**: Feed the parser a representative Wahapedia-style markdown chunk and verify the output `UnitProfile` has correctly typed fields and all weapons parsed.

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T018 [P] [US3] Unit test for parsing a standard unit datasheet (M, T, Sv, W, Ld, OC extraction) in tests/retrieval/test_parser.py
- [ ] T019 [P] [US3] Unit test for parsing weapon profile tables (Range, A, BS/WS, S, AP, D) into `WeaponStatLine` objects in tests/retrieval/test_parser.py
- [ ] T020 [P] [US3] Unit test for parsing variable stat values ("D6", "2D6", "D3+1") kept as strings for dice-engine resolution in tests/retrieval/test_parser.py
- [ ] T021 [P] [US3] Unit test for parsing MVP keyword abilities (Lethal Hits, Sustained Hits, Devastating Wounds, Anti-X, Lance, Heavy, Rapid Fire, Assault, Pistol, Blast, Torrent) into `StatModifier` objects in tests/retrieval/test_parser.py
- [ ] T022 [P] [US3] Unit test for malformed/incomplete markdown — returns partial result with flagged missing fields in tests/retrieval/test_parser.py
- [ ] T023 [P] [US3] Unit test for unrecognized abilities — preserved as raw text and flagged per FR-007 in tests/retrieval/test_parser.py

### Implementation for User Story 3

- [ ] T024 [US3] Implement `MarkdownStatParser` class with `parse_unit_profile(markdown: str) -> UnitProfile` method in src/vindicta_engine/retrieval/parser.py
- [ ] T025 [US3] Implement datasheet stat extraction (regex-based parsing of M, T, Sv, W, Ld, OC from markdown tables/lists) in src/vindicta_engine/retrieval/parser.py
- [ ] T026 [US3] Implement weapon profile table parser — extract each weapon row into a `WeaponStatLine`, handling variable damage/attacks as raw strings in src/vindicta_engine/retrieval/parser.py
- [ ] T027 [US3] Implement MVP keyword ability parser — match the 12 enumerated keywords (re-rolls, Lethal Hits, Sustained Hits, Devastating Wounds, Anti-X, Lance, Heavy, Rapid Fire, Assault, Pistol, Blast, Torrent) into `StatModifier` objects in src/vindicta_engine/retrieval/parser.py
- [ ] T028 [US3] Implement partial result handling — return `UnitProfile` with `None` or sentinel values for missing fields and a list of parse warnings in src/vindicta_engine/retrieval/parser.py

**Checkpoint**: Parser converts raw markdown to typed `UnitProfile` objects. All 12 MVP keywords recognized. Malformed input handled gracefully. US3 is independently testable.

---

## Phase 5: User Story 2 — Cache Stats During Heavy Simulation Runs (Priority: P2)

**Goal**: An async-safe LRU cache eliminates redundant RAG queries during Monte Carlo batches, keyed by `(unit_name, weapon_name, rules_version)`.

**Independent Test**: Run a 1,000-iteration batch and verify via `CacheMetrics` that the RAG server is queried at most once per unique unit-weapon-version combination.

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T029 [P] [US2] Unit test for cache hit — second lookup for same key returns cached result in <1ms in tests/retrieval/test_stat_cache.py
- [ ] T030 [P] [US2] Unit test for cache miss — new key triggers RAG query and stores result in tests/retrieval/test_stat_cache.py
- [ ] T031 [P] [US2] Unit test for LRU eviction — when max_size exceeded, least-recently-used entry is evicted in tests/retrieval/test_stat_cache.py
- [ ] T032 [P] [US2] Unit test for async-safety — concurrent async tasks requesting the same uncached key trigger only one RAG query (no thundering herd) in tests/retrieval/test_stat_cache.py
- [ ] T033 [P] [US2] Unit test for version-keyed cache miss — same unit+weapon but different version triggers fresh retrieval in tests/retrieval/test_stat_cache.py
- [ ] T034 [P] [US2] Unit test for cache invalidation — `invalidate()` clears all entries; `refresh(key)` forces re-fetch in tests/retrieval/test_stat_cache.py
- [ ] T035 [P] [US2] Unit test for `CacheMetrics` counters — hits, misses, and parse_errors increment correctly in tests/retrieval/test_stat_cache.py

### Implementation for User Story 2

- [ ] T036 [US2] Implement `StatCacheKey` named tuple `(unit_name, weapon_name, rules_version)` in src/vindicta_engine/retrieval/stat_cache.py
- [ ] T037 [US2] Implement `StatCache` class with async-safe `get()` method using `asyncio.Lock` per-key double-checked locking pattern in src/vindicta_engine/retrieval/stat_cache.py
- [ ] T038 [US2] Implement LRU eviction — track insertion/access timestamps, evict least-recently-used when `max_size` exceeded in src/vindicta_engine/retrieval/stat_cache.py
- [ ] T039 [US2] Implement `invalidate()` (clear all) and `refresh(key)` (force re-fetch for specific key) methods in src/vindicta_engine/retrieval/stat_cache.py
- [ ] T040 [US2] Integrate `CacheMetrics` counters — increment hits/misses/parse_errors on each operation in src/vindicta_engine/retrieval/stat_cache.py
- [ ] T041 [US2] Implement `StatRetriever` facade combining `RAGClient` + `MarkdownStatParser` + `StatCache` in src/vindicta_engine/retrieval/stat_cache.py

**Checkpoint**: Cache eliminates redundant queries. Async-safe under concurrent load. LRU eviction bounds memory. Metrics observable. US2 is independently testable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Integration, documentation, and quality improvements across all stories

- [ ] T042 [P] Export full public API from src/vindicta_engine/retrieval/__init__.py (StatRetriever, UnitProfile, WeaponStatLine, StatModifier, CacheMetrics, RAGQueryError)
- [ ] T043 [P] Add structured logging (Python `logging` module) for cache hits/misses, RAG query latency, and parse errors in src/vindicta_engine/retrieval/stat_cache.py and src/vindicta_engine/retrieval/mcp_client.py
- [ ] T044 [P] Add docstrings to all public classes and methods across src/vindicta_engine/retrieval/
- [ ] T045 Run `ruff check .` and `ruff format --check .` across vindicta-engine and fix any violations
- [ ] T046 Run `mypy --strict` across vindicta-engine and fix any type errors
- [ ] T047 Validate `quickstart.md` code example runs correctly against the implemented API
- [ ] T048 Run full test suite `uv run pytest` and verify ≥90% coverage
- [ ] T049 Add memory benchmark test validating SC-005: cache memory for a 20-unit matchup stays under 10 MB in tests/retrieval/test_stat_cache.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational — RAG client needs models
- **US3 (Phase 4)**: Depends on Foundational — parser needs models. **Can run in parallel with US1**
- **US2 (Phase 5)**: Depends on US1 + US3 — cache wraps client + parser
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — no dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational — no dependencies on other stories. **Can run in parallel with US1.**
- **User Story 2 (P2)**: Depends on US1 (RAGClient) and US3 (Parser) — composes both into the cached `StatRetriever`

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T003/T004 (Setup) can run in parallel
- T005/T006/T008/T009 (Foundational models) can run in parallel
- T011/T012/T013 (US1 tests) can run in parallel
- T018–T023 (US3 tests) can all run in parallel
- T029–T035 (US2 tests) can all run in parallel
- **US1 and US3 can execute in parallel** after Foundational completes
- T042/T043/T044 (Polish) can run in parallel

---

## Parallel Example: User Stories 1 & 3

```bash
# After Foundational completes, launch both P1 stories in parallel:

# Stream 1: User Story 1 (RAG Client)
Task: "Unit test for RAGClient.query_unit_stats() in tests/retrieval/test_mcp_client.py"
Task: "Implement RAGClient class in src/vindicta_engine/retrieval/mcp_client.py"

# Stream 2: User Story 3 (Parser) — runs simultaneously
Task: "Unit test for parsing a standard unit datasheet in tests/retrieval/test_parser.py"
Task: "Implement MarkdownStatParser class in src/vindicta_engine/retrieval/parser.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational models
3. Complete Phase 3: User Story 1 (RAG Client)
4. **STOP and VALIDATE**: Verify RAGClient returns raw markdown from real MCP server
5. Demo stat retrieval independently

### Incremental Delivery

1. Complete Setup + Foundational → Models ready
2. Add US1 (RAG Client) + US3 (Parser) **in parallel** → Full stat loading pipeline → Demo
3. Add US2 (Cache) → Wraps US1+US3 → Performant for Monte Carlo batches → Demo
4. Polish → Production-quality code with logging, docs, full coverage

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (RAG Client)
   - Developer B: User Story 3 (Parser)
3. Both complete → Developer A or B: User Story 2 (Cache Integration)
4. Polish phase

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US3 (parsing) is ordered before US2 (caching) despite being labeled US3 in the spec, because the cache depends on the parser

## Deferred Items

- **Conditional/phase-dependent stats** (spec.md edge case L72): Units whose stats change between melee and ranged phases are not handled by the MVP parser. This will be addressed in a future iteration once the core parsing pipeline is validated.
- **SC-001 end-to-end benchmark** and **SC-003 accuracy benchmark**: Covered by unit tests; formal benchmark tasks deferred to post-MVP.

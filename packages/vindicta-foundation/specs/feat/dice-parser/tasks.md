# Tasks: dice-parser

**Input**: Design documents from `/specs/feat/dice-parser/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependency installation, and skeleton creation

- [X] T001 Add `lark>=1.2.0` dependency to `pyproject.toml` and run `uv lock`
- [X] T002 Create parser package skeleton at `src/vindicta_foundation/parser/__init__.py`
- [X] T003 [P] Create error module at `src/vindicta_foundation/parser/errors.py` with `DiceParserError`, `ParseError`, and `InvalidDiceNotationError`
- [X] T004 [P] Create grammar module at `src/vindicta_foundation/parser/grammar.py` with the Lark EBNF grammar string from `contracts/grammar.ebnf`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: AST node models and supporting enums that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create AST node models and enums in `src/vindicta_foundation/models/dice_ast.py`: `BinaryOperator`, `UnaryOperator`, `ModifierType` enums; `IntegerNode`, `DicePoolNode`, `BinaryOpNode`, `UnaryOpNode`, `ModifierNode` Pydantic models inheriting from `VindictaModel`; and `ASTNodeType` discriminated union
- [X] T006 Update `src/vindicta_foundation/models/__init__.py` to export all new AST models and enums
- [X] T007 Create AST model unit tests in `tests/test_dice_ast.py`: construction, validation (count≥1, sides≥1, value≥1), serialization round-trip via `model_dump_json()`/`model_validate_json()`, and discriminated union deserialization

**Checkpoint**: AST models are fully defined, exported, tested, and serialize/deserialize correctly

---

## Phase 3: User Story 1 — Parsing Standard Notation (Priority: P1) 🎯 MVP

**Goal**: Parse basic dice notation strings (e.g., `"3d6"`, `"2d6 + 4"`) into typed AST nodes with correct arithmetic precedence

**Independent Test**: Verify string→AST translation for all basic notation patterns without any modifier support

### Implementation for User Story 1

- [X] T008 [US1] Implement Lark Transformer in `src/vindicta_foundation/parser/transformer.py`: convert parse tree to AST nodes for rules `integer`, `dice`, `add`, `sub`, `mul`, `div`, `neg`, `pos`
- [X] T009 [US1] Implement public `parse_dice()` function in `src/vindicta_foundation/parser/__init__.py`: instantiate Lark parser with grammar, apply Transformer, wrap Lark exceptions in `ParseError`
- [X] T010 [P] [US1] Create parser tests in `tests/test_parser.py`: parametrized tests for `"3d6"`, `"2d6 + 4"`, `"1d20"`, `"2d6 + 1d4 * 3"` (precedence), `"(2d6 + 3) * 2"` (grouping), `"-3"` (unary), integer-only expressions
- [X] T011 [P] [US1] Create error tests in `tests/test_parser_errors.py`: parametrized tests for empty string, `"abc"`, `"2d"`, `"d6"`, `"++"`, `"2d6 +"` (trailing operator), and other malformed inputs asserting `ParseError` with descriptive messages

**Checkpoint**: Parser handles all basic dice + arithmetic expressions, rejects malformed input with typed errors

---

## Phase 4: User Story 2 — Mechanics Modifiers Support (Priority: P2)

**Goal**: Extend parser to understand standard wargaming modifiers (keep highest/lowest, drop highest/lowest, explode)

**Independent Test**: Verify modifier expressions produce correct `ModifierNode` AST wrapping the `DicePoolNode`, independently testable on top of US1

### Implementation for User Story 2

- [X] T012 [US2] Extend Transformer in `src/vindicta_foundation/parser/transformer.py` with modifier rules: `keep_highest`, `keep_lowest`, `drop_highest`, `drop_lowest`, `explode`, and `modified_dice` handler
- [X] T013 [P] [US2] Add modifier parser tests in `tests/test_parser.py`: parametrized tests for `"4d6dl1"`, `"4d6kh3"`, `"2d20kl1"`, `"4d6dh1"`, `"1d10e10"`, and modifier combined with arithmetic (e.g., `"4d6dl1 + 2"`)
- [X] T014 [P] [US2] Add modifier error tests in `tests/test_parser_errors.py`: `"4d6kh"` (missing value), `"kh3"` (modifier without dice), and other malformed modifier inputs

**Checkpoint**: Full modifier support working; all 6 modifiers (kh, kl, dh, dl, e) parse correctly

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Quality gates, performance validation, and documentation

- [X] T015 [P] Run `uv run pytest --cov=vindicta_foundation --cov-report=term-missing` and verify ≥90% coverage on `parser/` and `models/dice_ast.py`
- [X] T016 [P] Run `uv run mypy src/vindicta_foundation/parser/ src/vindicta_foundation/models/dice_ast.py --strict` and fix any type errors
- [X] T017 [P] Run `ruff check .` and `ruff format --check .` to verify linting and formatting
- [X] T018 Add performance smoke test in `tests/test_parser.py`: parse 1000 iterations of `"4d6dl1 + 2d8kh1 * 3"` and assert average < 1ms per SC-003
- [X] T019 Run quickstart.md validation: execute all code examples from `quickstart.md` in a test or script to confirm accuracy

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2)
- **User Story 2 (Phase 4)**: Depends on User Story 1 (Phase 3) — extends the Transformer
- **Polish (Phase 5)**: Depends on all user stories being complete

### Within Each User Story

- Models before Transformer (already done in Foundational)
- Transformer before public API
- Implementation and tests can proceed in parallel (tests for separate files)

### Parallel Opportunities

- T003 and T004 can run in parallel (different files, no dependencies)
- T010 and T011 can run in parallel (different test files)
- T013 and T014 can run in parallel (different test concerns)
- T015, T016, T017 can run in parallel (different validation tools)

---

## Parallel Example: User Story 1

```text
# After T008 and T009 complete, launch tests in parallel:
Task T010: "Parser tests in tests/test_parser.py"
Task T011: "Error tests in tests/test_parser_errors.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T004)
2. Complete Phase 2: Foundational (T005–T007)
3. Complete Phase 3: User Story 1 (T008–T011)
4. **STOP and VALIDATE**: All basic dice parsing works, errors are typed
5. Can demo: `parse_dice("2d6 + 3")`

### Incremental Delivery

1. Setup + Foundational → AST models ready
2. Add User Story 1 → Basic parsing works → MVP!
3. Add User Story 2 → Modifier support → Feature complete
4. Polish → Quality gates pass → Ready for merge

---

## Summary

| Metric                        | Value                                               |
| ----------------------------- | --------------------------------------------------- |
| **Total tasks**               | 19                                                  |
| **Phase 1 (Setup)**           | 4 tasks                                             |
| **Phase 2 (Foundational)**    | 3 tasks                                             |
| **Phase 3 (US1 — Parsing)**   | 4 tasks                                             |
| **Phase 4 (US2 — Modifiers)** | 3 tasks                                             |
| **Phase 5 (Polish)**          | 5 tasks                                             |
| **Parallel opportunities**    | 7 (T003∥T004, T010∥T011, T013∥T014, T015∥T016∥T017) |
| **MVP scope**                 | Phases 1–3 (11 tasks)                               |
| **Suggested first milestone** | `parse_dice("2d6 + 3")` → typed AST                 |

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently

# Tasks: WARScribe OCR Parser

**Feature**: WARScribe OCR Parser
**Branch**: `001-ocr-parser`
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Implementation Strategy

We will build the OCR Parser starting with the structural core (Pydantic models) and the lowest-level OpenCV pipelines, before moving up to the text parsing heuristics and CLI assembly.

## Phase 1: Setup

The foundation of the Python library environments.
- [ ] T001 Define `pyproject.toml` with `pytesseract`, `opencv-python`, `Pillow`, `pydantic`, `click`, and `pytest` dependencies.
- [ ] T002 Initialize the project structure: `src/warscribe_parser/ocr/` and `tests/`.
- [ ] T003 [P] Create `.gitignore` and `README.md` boilerplate.

## Phase 2: Foundational Data Models

Implementing the axiomatic VindictaModel structures.
- [ ] T004 [P] Implement `ObjectiveScore` model in `src/warscribe_parser/ocr/models.py`.
- [ ] T005 [P] Implement `PlayerResult` model in `src/warscribe_parser/ocr/models.py`.
- [ ] T006 Implement `GameResult` model in `src/warscribe_parser/ocr/models.py`.

## Phase 3: User Story 1 - Process Warscribe Screenshots to JSON (P1)

**Goal**: Extract structured JSON from a single WARScribe screenshot image.
**Independent Test**: Provide an image to the CLI and receive validated JSON matching the `GameResult` schema perfectly.

- [ ] T007 [US1] Implement `preprocess()` function utilizing OpenCV adaptive thresholding and grayscale conversion in `src/warscribe_parser/ocr/preprocessor.py`.
- [ ] T008 [US1] Create the Tesseract OCR wrapper functions (`extract_words`, `extract_text_lines`) in `src/warscribe_parser/ocr/ocr_engine.py`.
- [ ] T009 [US1] Build header and footer regex parsing logic in `src/warscribe_parser/ocr/parser.py`.
- [ ] T010 [US1] Build player-block extraction logic (handling Primary/Secondary rules) in `src/warscribe_parser/ocr/parser.py`.
- [ ] T011 [US1] Write test fixtures and comprehensive parser unit tests in `tests/test_ocr_parser.py`.
- [ ] T012 [US1] Wire up `src/warscribe_parser/ocr/cli.py` to connect preprocessor → ocr_engine → parser using `click`.

## Phase 4: Polish & Integration

- [ ] T013 Update `README.md` with final installation guidelines (`winget install UB-Mannheim.TesseractOCR`).
- [ ] T014 Run `uv run pytest --cov` to ensure 90%+ coverage.
- [ ] T015 Verify `mypy` strict type checking across the module.

---

## Dependencies

- Phase 2 (Data Models) depends on Phase 1.
- Phase 3 (US1 Core Logic) depends heavily on Phase 2 to map the data.
- Phase 4 depends on all previous phases.

## Parallel Execution

- T003 can run in parallel with T001.
- T004 and T005 can be implemented concurrently by independent agents.

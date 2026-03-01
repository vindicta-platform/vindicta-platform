# Implementation Plan: WARScribe OCR Parser

**Branch**: `001-ocr-parser` | **Date**: 2026-02-22 | **Spec**: [specs/001-ocr-parser/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-ocr-parser/spec.md`

## Summary

Build a local, non-cloud OCR parser using OpenCV and Tesseract to ingest WARScribe 10e screenshots into structured JSON mapping to `VindictaModel` entities.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `pytesseract`, `opencv-python`, `Pillow`, `pydantic`, `click`
**Storage**: N/A (stateless pipeline)
**Testing**: `pytest`
**Target Platform**: Any environment with Tesseract installed (Windows dev, Linux containers)
**Project Type**: CLI / Library (internal package in the `WARScribe-Parser` module)
**Performance Goals**: <5.0 seconds per image
**Constraints**: Must run locally without external API calls
**Scale/Scope**: Handles single 40k 10e match scorecard images

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Model Integrity (II)**: The output domain models must inherit from `VindictaModel` in `src/vindicta_foundation/models/base.py`. (PASSED)
- **Meso-Repo Consolidation (III)**: Code will live in the appropriate Meso-repo (`vindicta-foundation` or designated WARScribe component). (PASSED)
- **Quality Mandates (V)**: Code must hit 90% test coverage and use strict `mypy` typing. (PASSED)

## Project Structure

### Documentation (this feature)

```text
specs/001-ocr-parser/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/warscribe_parser/ocr/
├── __init__.py
├── models.py            # VindictaModel implementations
├── preprocessor.py      # OpenCV logic
├── ocr_engine.py        # Tesseract wrapper
├── parser.py            # Regex/Text to Model logic
└── cli.py               # Click CLI

tests/
└── test_ocr_parser.py   # Pytest suite
```

**Structure Decision**: A single library package inside `src/warscribe_parser/ocr` alongside existing parser code, with tests in the root `tests/` folder.

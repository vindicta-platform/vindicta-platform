# Feature Specification: WARScribe OCR Parser

**Feature Branch**: `001-ocr-parser`  
**Created**: 2026-02-22  
**Status**: Draft  
**Input**: User description: "create an OCR parser to take images and parse them into formatting ready for consumption for Warscribe, Primordia and other Platform tasks"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Process Warscribe Screenshots to JSON (Priority: P1)

Users (specifically the WARScribe ingestion pipeline) need to supply a screenshot of a completed Warhammer 40k match from the Warscribe app and receive structured, machine-readable data (JSON) containing all scores, objectives, and metadata.

**Why this priority**: This is the core capability that enables automated ingestion of physical/app scorecards into the overarching Vindicta platform (Primordia, Oracle, etc.), bypassing manual data entry.

**Independent Test**: Can be fully tested by providing a standard 40k 10e Warscribe app scorecard screenshot, running the CLI/function, and asserting the output JSON matches the visual data perfectly.

**Acceptance Scenarios**:

1. **Given** a clear screenshot of a 2-player Warscribe match scorecard, **When** the image is processed by the OCR parser, **Then** it produces a JSON document with the correct date, players, final scores, and winner.
2. **Given** a scorecard containing specific secondary objective names and per-round scores, **When** processed, **Then** the JSON contains an array of those exact objectives, matched to the correct player, with the correct round-by-round point values (treating empty round slots as null/not scored).
3. **Given** an image with a dark UI background, **When** processed, **Then** the system successfully thresholds the image and reads the light text with an accuracy sufficient for correct JSON construction.

---

### Edge Cases

- What happens when an image is slightly blurry or has low resolution? (Should reject or provide partial data with low confidence warnings).
- How does system handle non-standard scorecard layouts (e.g. from a different app or a physical paper sheet)? (For this MVP, it should explicitly fail/error if the "Warscribe" structure isn't detected).
- What happens if the OCR misreads a player name? (The platform will eventually need fuzz-matching against registered users).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept standard image formats (JPEG, PNG).
- **FR-002**: System MUST output structured JSON conforming to the canonical platform score model (`GameResult`, `PlayerResult`, `ObjectiveScore`).
- **FR-003**: System MUST accurately extract the overarching match metadata (Date, Ruleset, Mission Deck, Match Type, Final Scores, Winner).
- **FR-004**: System MUST accurately partition data by Player, extracting Faction, Detachment, and "Went First" status.
- **FR-005**: System MUST extract both the Primary (Terraform) and Secondary objectives, capturing point values *per round* (Rounds 1-5).
- **FR-006**: System MUST extract summary mechanics (Battle Ready points, CP Remaining per round).
- **FR-007**: System MUST run locally without depending on external/cloud vision APIs to maintain the platform's free-tier viability mandate.

### Key Entities

- **GameResult**: The root document containing match metadata and two PlayerResult objects.
- **PlayerResult**: Contains player-specific context (name, faction) and a collection of ObjectiveScores.
- **ObjectiveScore**: A specific scored mechanic, tracked across 5 rounds, with a final total.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The parser achieves 100% data extraction accuracy on high-quality, uncropped baseline screenshots of the Warscribe 10e app.
- **SC-002**: Image processing and JSON generation completes in under 5.0 seconds per image on standard consumer hardware.
- **SC-003**: The resulting JSON schema maps 1:1 with the `VindictaModel` definitions required by downstream services (Primordia).
- **SC-004**: The package successfully installs and runs locally in a standalone Python environment with no cloud dependencies.

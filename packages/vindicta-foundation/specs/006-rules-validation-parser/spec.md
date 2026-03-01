# Feature Specification: Rules Validation Parser

**Feature Branch**: `006-rules-validation-parser`  
**Created**: 2026-02-23  
**Status**: Draft  
**Input**: User description: "Defines an integration point where parsed chat logs are cross-referenced with the RAG rules database. Validates transcribed actions against the active rules database to flag illegal moves or hallucinations in transcripts. Augments the resulting game state with exact rules text for downstream processing."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Validate Transcribed Actions Against Rules (Priority: P1)

When a game transcript is generated (via WARScribe notation or chat-log parsing), each recorded action (e.g., a unit shooting a weapon, using an ability, or making a charge) must be cross-referenced against the currently active rules in the RAG database. Any action that references a non-existent ability, uses a weapon profile incorrectly, or violates a game rule should be flagged as an **illegal move** or a **transcription hallucination**.

**Why this priority**: Without validation, downstream consumers (Oracle debate engine, Primordia analytics) inherit errors silently. This is the core value proposition — turning raw transcripts into *trustworthy* game state.

**Independent Test**: Can be fully tested by submitting a single annotated action (e.g., `[SHOOT: TAC-01 -> Enemy-01]` with weapon "Lascannon") and verifying that the system either confirms the action as legal or returns a structured violation report citing the relevant rule.

**Acceptance Scenarios**:

1. **Given** a transcript action `[SHOOT: TAC-01 -> Enemy-01]` where TAC-01 is a Tactical Squad equipped with a Lascannon, **When** the validator checks this action, **Then** it confirms the action as legal and returns the matched weapon profile from the rules database.
2. **Given** a transcript action referencing a weapon that does not exist on the unit's datasheet (e.g., a Tactical Marine using a "Plasma Obliterator"), **When** the validator checks this action, **Then** it flags the action as an illegal move with a violation type of "weapon_not_found" and includes the unit's actual available wargear.
3. **Given** a transcript action claiming a unit used an ability it does not possess, **When** the validator checks this action, **Then** it flags the action as a hallucination with a violation type of "ability_not_found" and includes the unit's actual abilities list.

---

### User Story 2 - Augment Game State with Rules Text (Priority: P2)

After validation, each confirmed-legal action in the game state should be enriched with the exact rules text (weapon profiles, ability descriptions, stratagem wording) retrieved from the RAG database. This augmented state becomes the canonical artifact for downstream systems.

**Why this priority**: Downstream consumers (e.g., the Debate Engine) need exact rules text attached to each action to perform accurate tactical analysis without making their own separate RAG queries. This reduces latency and ensures a single source of truth for the game record.

**Independent Test**: Can be independently tested by submitting a valid action, confirming it passes validation, and then inspecting the returned game state to verify that the matching rules text, source URL, and rules version are attached.

**Acceptance Scenarios**:

1. **Given** a validated legal action `[SHOOT: CPT-01 -> Enemy-HQ]` with weapon "Master-crafted Bolt Rifle", **When** the game state is augmented, **Then** the action record includes the full weapon profile (Range, Attacks, BS, Strength, AP, Damage) and the source citation from the rules database.
2. **Given** a validated legal action using a faction-specific ability (e.g., "Oath of Moment"), **When** the game state is augmented, **Then** the action record includes the full ability text, any conditions or restrictions, and the rules version identifier.

---

### User Story 3 - Batch Validate a Full Transcript (Priority: P3)

A complete game transcript containing dozens of actions across multiple game rounds should be validatable in a single batch operation. The system produces a consolidated validation report listing all legal actions, all flagged violations, and an overall confidence score for the transcript's integrity.

**Why this priority**: Real-world use requires processing entire games, not individual actions. Batch validation enables integration into automated pipelines and post-game analysis workflows.

**Independent Test**: Can be independently tested by submitting a multi-round transcript fixture and verifying the report contains per-action verdicts, an aggregate violation summary, and an overall integrity score.

**Acceptance Scenarios**:

1. **Given** a full 5-round game transcript with 40 actions, **When** batch validation is run, **Then** the system returns a structured report with a verdict (legal/illegal/hallucination) for each action and an overall transcript integrity percentage.
2. **Given** a transcript where 3 out of 40 actions are flagged, **When** the report is reviewed, **Then** each violation includes the action reference, the violation type, the offending element, and the corrective rules text.

---

### Edge Cases

- What happens when the RAG database returns no results for a unit or weapon query? (System should flag as "rules_not_found" rather than silently pass or fail, indicating a gap in the database rather than a player error.)
- How does the system handle actions referencing outdated rules or errata that have been superseded? (System should validate against the most recent version and note the version mismatch if the transcript references deprecated wording.)
- What happens when a unit's datasheet exists but its specific loadout variant is ambiguous? (System should return the closest match with a confidence indicator and a "loadout_ambiguous" advisory rather than a hard failure.)
- How does the system behave when the RAG server is unreachable? (Validation should fail gracefully with a clear connectivity error, never silently marking actions as valid.)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a structured game action (conforming to WARScribe canonical notation) and return a validation verdict (legal, illegal, or hallucination) with supporting evidence.
- **FR-002**: System MUST query the RAG rules database to retrieve the relevant unit datasheet, weapon profiles, and ability descriptions for cross-referencing against each transcribed action.
- **FR-003**: System MUST categorize validation failures into distinct violation types: `weapon_not_found`, `ability_not_found`, `illegal_action`, `rules_not_found`, `loadout_ambiguous`, and `version_mismatch`.
- **FR-004**: System MUST augment each validated legal action with the exact rules text, source citation (URL), and rules version identifier retrieved from the database.
- **FR-005**: System MUST support batch validation of a full game transcript, producing a consolidated report with per-action verdicts, violation summaries, and an overall transcript integrity score.
- **FR-006**: System MUST validate actions against the most recent version of the rules and flag any version discrepancies when older rules wording is detected in the transcript.
- **FR-007**: System MUST fail gracefully when the rules database is unavailable, returning a clear error state rather than producing silent false-positives.
- **FR-008**: System MUST log all validation operations with sufficient detail to support auditability and debugging of false-positive or false-negative rulings.

### Key Entities

- **Validation Request**: A single game action (unit, action type, target, weapon/ability) submitted for cross-referencing against the rules database.
- **Validation Verdict**: The result of a single validation: legal (with augmented rules text), illegal (with violation details and corrective text), or hallucination (action references non-existent game element).
- **Violation Report**: A structured record containing the violation type, the offending element, the expected/actual values from the rules database, and the source citation.
- **Augmented Action**: A validated game action enriched with the full rules text, weapon profile, ability description, source URL, and rules version used for validation.
- **Transcript Integrity Report**: An aggregate report for a batch-validated transcript, containing all individual verdicts, violation summaries, and an overall confidence/integrity percentage.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The system correctly identifies 95% or more of deliberately planted illegal actions in a curated test transcript within the top-1 violation result.
- **SC-002**: Validated legal actions include the full, unmodified rules text from the database with a correct source citation in 100% of cases.
- **SC-003**: Batch validation of a 50-action transcript completes in under 10 seconds under typical local workload.
- **SC-004**: The system produces zero false-positive "legal" verdicts when the RAG server is unreachable (all actions must return an error state).
- **SC-005**: Downstream consumers (Debate Engine, Analytics) can consume the augmented game state without performing additional rules lookups for the validated actions.

## Assumptions

- The upstream RAG pipeline (005-rag-pipeline) is operational and serving rules via MCP, providing unit datasheets, weapon profiles, and ability descriptions as markdown chunks.
- Transcripts conform to WARScribe canonical notation format as defined in the WARScribe v1 Scope & Notation Standards (unit registration with unique IDs, `[ACTION: UnitID -> Target]` format).
- The rules database is maintained with versioned content, allowing the system to distinguish between current and superseded rules.
- This feature addresses the "List Validation Gap" explicitly accepted in the WARScribe v1 scope decision, serving as the separate validation layer referenced in that architecture note.

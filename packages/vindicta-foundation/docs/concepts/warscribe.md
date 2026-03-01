# WARScribe Technical Manual (The Language)

**Function:** Language-Agnostic Game State Notation
**Pattern:** Subject-Action-Target-Outcome (SATO)

## I. The Syntax Schema

WARScribe records state changes using a **Coordinate-Action Syntax**, similar to Algebraic Chess Notation.

`[Subject_ID] [Action_Code] [Target/Coord] [Formation_Tag] ([Resolution])`

## II. Opcode Library

- **`M` (Move):** `U1 M (22,30) F:FF` — Unit 1 moves to centroid (22,30) in Fang Formation.
- **`C` (Charge):** `U1 C U2 (!8)` — Unit 1 attempts a charge on Unit 2, result is a successful 8.
- **`A` (Attack):** `U1 A U2 [W:1] (!H3 ?W1)` — Unit 1 attacks Unit 2 with weapon index 1; results in 3 hits and 1 failed wound.
- **`R` (Reaction):** Nested logic for 11th Edition: `U1 M (x,y) {U2 R:A}`.

## III. Formation & Geometry Tags

To handle multi-model units, WARScribe uses **Centroid Anchoring**:

- **`F:CC` (Centroid Cluster):** Minimum footprint.
- **`F:FF` (Fang Formation):** Line formation with 3-model "triangle" end-caps to satisfy 7+ model coherency rules.
- **`F:OW` (Objective Wrap):** Radial distribution 2.9" from an objective center for denial.

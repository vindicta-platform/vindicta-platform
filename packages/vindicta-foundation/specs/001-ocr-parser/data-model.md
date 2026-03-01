# Data Model: WARScribe OCR Parser

The WARScribe OCR Parser leverages the base `VindictaModel` to serialize data extracted from game screenshots into predictable JSON payloads.

## Core Entities

### ObjectiveScore
A granular record representing points scored linearly across 5 distinct game rounds. 
**Fields**:
- `name` (str): Label of the objective (e.g. "Area Denial").
- `rounds` (list[int | None]): Values scored per round. `None` implies dash/unavailable.
- `total` (int | None): Explicit right-hand column total, if detected.
- `max_total` (int | None): Denominator (e.g. 40 in "15/40").

### PlayerResult
Records all metrics specific to one of the two players in a match.
**Fields**:
- `name` (str): Player's registered identity or screen name.
- `faction` (str): Faction played (e.g. "T'au").
- `detachment` (str): Detachment used (e.g. "Mont'Ka").
- `went_first` (bool): True if this player had the first turn.
- `terraform` (ObjectiveScore): Tracked specifically as it is primary in competitive formats.
- `secondary_objectives` (list[ObjectiveScore]): Dynamic list of chosen secondaries.
- `battle_ready` (int | None): Painting score metric (typically 10).
- `cp_remaining` (list[int | None]): Command points available per round.
- `total_score` (int): Player's final cumulative match score.

### GameResult
The root container holding the full state of the parsed image.
**Fields**:
- `date` (str): ISO 8601 formatting of the match date.
- `ruleset` (str | None): e.g. "Warhammer 40k 10e".
- `mission_deck` (str | None): e.g. "Chapter Approved 2025-26".
- `mission_type` (str | None): e.g. "Crucible Of Battle".
- `game_size` (str | None): e.g. "Strike Force".
- `result` (str | None): "VICTORY", "DEFEAT", or "DRAW".
- `player1` (PlayerResult): Object representing player 1.
- `player2` (PlayerResult): Object representing player 2.
- `winner` (str | None): Parsed winner's name.
- `raw_scores` (dict[str, int]): Dictionary mapping player name to score explicitly.
- `num_rounds` (int): Hardcoded integer denoting round count (5).

# WARScribe System

The Universal Wargaming Notation System.

---

## Overview

**WARScribe** is a formal, language-agnostic, and edition-independent notation system for recording wargaming states and actions. It serves as the "source of truth" for the Vindicta Platform, enabling:

- **Universal Transcripts**: A standard format for sharing battle reports.
- **Machine Readability**: Parsable by engines for simulation and analysis.
- **Cross-System Support**: Designed to handle various game systems (40k 10th, etc.) through adapters.

## Core Capabilities

| Feature                | Description                                                                                      |
| :--------------------- | :----------------------------------------------------------------------------------------------- |
| **Unit Identity**      | Maps arbitrary unit strings (e.g., "Space Marine Captain") to unique, persistent IDs (`CPT-01`). |
| **Coordinate System**  | Uses a standardized coordinate reference system (CRS) for board positioning.                     |
| **Action Logging**     | Records moves, attacks, and state changes with formal syntax.                                    |
| **Modification Logic** | Tracks buffs, debuffs, and lasting effects on units.                                             |

## The Notation

WARScribe uses a structured format to capture game events.

### Unit Definition

```text
DEFINE UNIT: "Captain in Terminator Armour" AS [U-001]
PROPERTIES: { Faction: "Adeptus Astartes", Points: 95 }
```

### Action Record

```text
[TURN 1: PLAYER A]
MOVE [U-001] FROM (12, 4) TO (12, 10)
ATTACK [U-001] -> [E-005] USING "Storm Bolter"
  > HITS: 3
  > WOUNDS: 2
  > SAVES: 1
  > DAMAGE: 1
```

## Tools and Ecosystem

- **WARScribe-CLI**: Command line tool for validating notation and generating reports.
  - `warscribe parse <file.ws>`
  - `warscribe export --format json`
- **WARScribe-Parser**: The core library for programmatic access to WARScribe data.
- **Vindicta Portal**: Visualizes WARScribe transcripts as interactive battle reports.

## Integration

WARScribe feeds directly into **Project Primordia** to drive post-game analysis and "What-If" simulations.

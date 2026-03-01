# Feature Specification: Simulation Stat Retrieval

**Feature Branch**: `001-simulation-stat-retrieval`  
**Created**: 2026-02-23  
**Status**: Draft  
**Input**: User description: "How the Monte Carlo simulation engine queries the RAG server to load unit profiles and weapon stats before running combat simulations, including caching strategies and markdown-to-struct parsing."

## Clarifications

### Session 2026-02-23

- Q: What uniquely identifies a cached stat entry — unit name + weapon name alone, or should the rules version also be part of the cache key? → A: Unit name + weapon name + rules version (version is part of the key, so new versions auto-miss the cache).
- Q: Should the engine retry failed RAG queries, and if so, how many attempts before surfacing the error? → A: 1 retry after a short delay (~500ms), then fail if still unavailable.
- Q: Should the engine emit observable signals for monitoring and debugging? → A: Structured logging with in-memory counters (cache hits/misses, query latency, parse errors) accessible via API or log output.
- Q: Should the stat cache support thread-safe concurrent access, or is single-threaded sequential access sufficient? → A: Thread-safe and async-safe — cache must support concurrent access from async simulation tasks.
- Q: Should the MVP parser handle all known ability types, or a curated core subset? → A: Core modifiers + common keywords (re-rolls, Lethal Hits, Sustained Hits, Devastating Wounds, Anti-X, Lance, Heavy, Rapid Fire, Assault, Pistol, Blast, Torrent).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Load Unit Stats for Combat Simulation (Priority: P1)

As the simulation engine, before executing a Monte Carlo combat run, I need to retrieve the complete unit profile and weapon stats for each participating unit from the RAG rules server so that all combat parameters (attacks, hit threshold, wound threshold, save, damage, special rules) are accurate and rules-authoritative.

**Why this priority**: Without accurate stat retrieval, the simulation produces meaningless results. This is the foundational data path that enables all downstream physics calculations.

**Independent Test**: Can be fully tested by requesting a known unit's profile (e.g., "Intercessor Squad") from the RAG server and verifying the returned data is correctly parsed into the engine's structured combat parameters — `attacks`, `hit_on`, `wound_on`, `save`, `damage` — matching the canonical rules source.

**Acceptance Scenarios**:

1. **Given** the simulation engine is initialized and the RAG server is available, **When** the engine requests the profile for "Intercessor Squad with Bolt Rifle", **Then** it receives and parses a structured stats object containing all required combat parameters (attacks, ballistic skill, strength, AP, damage) within 2 seconds.
2. **Given** a unit has multiple weapon options (e.g., heavy, rapid fire, melee), **When** the engine requests the unit profile, **Then** it receives all weapon profiles as distinct structured objects, each with their own stat line.
3. **Given** the RAG server returns rules text that includes special abilities or modifiers (e.g., "re-roll hit rolls of 1"), **When** the engine parses the response, **Then** the modifier is identified and encoded as a structured flag or parameter alongside the base stats.

---

### User Story 2 - Cache Stats During Heavy Simulation Runs (Priority: P2)

As the simulation engine during a batch Monte Carlo run (e.g., evaluating 10,000 iterations of a matchup), I need frequently requested unit stats to be served from a local cache to avoid redundant RAG server queries, so that simulation throughput is not bottlenecked by repeated network round-trips.

**Why this priority**: A single Monte Carlo batch may reference the same unit stat line thousands of times. Without caching, the system would send thousands of identical requests to the RAG server, creating unacceptable latency and wasted resources.

**Independent Test**: Can be tested by running a 1,000-iteration Monte Carlo batch for a known matchup (e.g., 10 Intercessors vs. 10 Ork Boyz) and verifying via instrumented counters that the RAG server is queried at most once per unique unit/weapon combination, with all subsequent lookups served from cache.

**Acceptance Scenarios**:

1. **Given** a Monte Carlo batch of N iterations for the same two-unit matchup, **When** the batch executes, **Then** the RAG server receives at most one query per unique unit-weapon combination, regardless of the iteration count.
2. **Given** a cached stat entry exists for a unit, **When** a new simulation iteration requests that unit's stats, **Then** the cached result is returned in under 1 millisecond.
3. **Given** the simulation engine is configured with a maximum cache size, **When** the cache reaches capacity, **Then** least-recently-used entries are evicted first to make room for new queries.

---

### User Story 3 - Parse RAG Markdown into Structured Stat Objects (Priority: P1)

As the simulation engine, when the RAG server returns rule chunks as markdown text, I need a reliable parser that converts those free-form markdown chunks into strongly typed statistical objects that the physics engine can consume, so that combat calculations are driven by precise numeric values rather than raw text.

**Why this priority**: The RAG pipeline (005) stores and serves rules as markdown chunks. The simulation engine's physics layer expects structured numeric data (integers, floats, booleans). This translation layer is critical for correctness.

**Independent Test**: Can be tested by feeding the parser a representative markdown rules chunk (containing a unit's stat block, weapon profiles, and special rules) and verifying the output is a correctly populated structured object with all numeric fields extracted and typed.

**Acceptance Scenarios**:

1. **Given** a markdown chunk containing a standard Warhammer 40k unit datasheet (Movement, Toughness, Save, Wounds, Leadership, OC), **When** the parser processes it, **Then** each stat is extracted into its corresponding typed field with correct values.
2. **Given** a markdown chunk containing a weapon profile table (Range, A, BS/WS, S, AP, D), **When** the parser processes it, **Then** each weapon is parsed into a distinct stat object with all fields correctly typed (including variable damage like "D3" encoded as a range or roll type).
3. **Given** a markdown chunk that includes an ability or aura rule (e.g., "Each time this model makes a ranged attack, re-roll a wound roll of 1"), **When** the parser processes it, **Then** the ability is identified by keyword and encoded as a structured modifier applicable to the combat roll parameters.
4. **Given** a malformed or incomplete markdown chunk (missing columns, unexpected formatting), **When** the parser processes it, **Then** it returns a partial result with clearly flagged missing fields rather than failing silently or producing incorrect values.

---

### Edge Cases

- What happens when the RAG server is unreachable or returns an empty result set for a valid unit query?
- How does the system handle units with conditional or phase-dependent stat profiles (e.g., stats change in melee vs. ranged)?
- What happens when the RAG server returns multiple versioned rule chunks for the same unit (e.g., pre-errata and post-errata) and the engine must select the correct one?
- How does the parser handle non-standard stat values like "2D6", "D3+1", or "N/A" for damage or attacks?
- What happens if a cached stat entry becomes stale because the RAG server has ingested updated rules between simulation batches?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST query the RAG rules server via its published interface to retrieve unit profiles and weapon stat lines by unit name or identifier before initiating any combat simulation.
- **FR-002**: System MUST parse returned markdown text chunks into strongly typed statistical objects with discrete numeric fields (e.g., attacks, ballistic skill, strength, armour penetration, damage).
- **FR-003**: System MUST support parsing variable stat values (e.g., "D6", "2D6", "D3+1") into a representation that the dice engine can resolve at simulation time.
- **FR-004**: System MUST maintain a local stat cache keyed by the composite of unit name, weapon name, and rules version, eliminating redundant queries for the same unit-weapon-version combination within a single simulation session or batch run. A new rules version for the same unit-weapon pair MUST result in a cache miss and fresh retrieval.
- **FR-005**: System MUST implement a cache eviction strategy (e.g., least-recently-used) to bound memory usage during heavy simulation runs.
- **FR-006**: System MUST attempt exactly one retry after a short delay (~500ms) when a RAG server query fails, then return a meaningful error or partial result to the caller if the retry also fails, rather than silently proceeding with default or zero values.
- **FR-007**: System MUST support retrieving and parsing the following ability categories for the MVP: core combat modifiers (re-roll hits, re-roll wounds, Lethal Hits, Sustained Hits, Devastating Wounds) and common weapon keywords (Anti-X, Lance, Heavy, Rapid Fire, Assault, Pistol, Blast, Torrent). Unrecognized abilities MUST be preserved as raw text and flagged for future parser expansion.
- **FR-008**: System MUST version-stamp cached entries using the rules segment version from the RAG pipeline so that stale data can be detected and refreshed.
- **FR-009**: System MUST allow cache invalidation or refresh on demand (e.g., between successive batch runs or when the user triggers a rules update).
- **FR-010**: System MUST expose structured logging and in-memory counters for key operational signals — cache hit/miss counts, RAG query latency, and parse error counts — accessible via programmatic API or log output for debugging and validation.
- **FR-011**: System MUST ensure the stat cache is async-safe, supporting concurrent reads and writes from multiple async simulation tasks without data corruption or race conditions.

### Key Entities

- **Unit Profile**: A structured representation of a unit's core statistics (Movement, Toughness, Save, Wounds, Leadership, Objective Control), uniquely identified by unit name and rules version.
- **Weapon Stat Line**: A structured representation of a single weapon's combat parameters (Range, Attacks, Skill, Strength, AP, Damage, Keywords/Abilities), linked to a parent Unit Profile.
- **Stat Modifier**: A structured encoding of a conditional rule or ability that alters base combat parameters (e.g., re-roll type, bonus attacks, conditional hit/wound modifiers), linked to either a Unit Profile or Weapon Stat Line.
- **Stat Cache Entry**: A cached unit-weapon stat bundle keyed by the composite of (unit name, weapon name, rules version). Includes insertion timestamp and last-access timestamp for LRU eviction. A new rules version naturally creates a distinct cache entry, ensuring stale data is never served.

## Assumptions

- The RAG rules server (005-rag-pipeline) is operational and serves rules as markdown text chunks via the Model Context Protocol (MCP) interface.
- The markdown format returned by the RAG pipeline follows a consistent structure (e.g., Wahapedia/40k.app style datasheet layouts) that can be reliably parsed.
- The simulation engine runs locally on the same machine as the RAG server, so network latency is negligible (localhost communication).
- Cache sizes will be bounded by available system memory; typical simulation batches involve fewer than 100 unique unit-weapon combinations.
- The stat cache will be accessed concurrently by async simulation tasks and must be designed for async-safe operation from the outset.
- Variable damage values (e.g., "D6") will be resolved at dice-roll time by the existing `DiceEngine`, not at parse time.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The simulation engine can load all required stats for a two-army matchup (up to 20 unique units) from the RAG server and begin simulation within 5 seconds.
- **SC-002**: During a 10,000-iteration Monte Carlo batch, cached stat lookups account for ≥99% of all stat retrievals, with at most one RAG query per unique unit-weapon combination.
- **SC-003**: 95% of parsed stat objects from RAG markdown chunks match the canonical source values with zero field errors.
- **SC-004**: When the RAG server is unavailable, the system reports the failure to the caller within 3 seconds rather than hanging or producing silently incorrect results.
- **SC-005**: Cache memory usage for a typical 20-unit matchup remains under 10 MB.

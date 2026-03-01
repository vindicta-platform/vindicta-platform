# Data Model: Simulation Stat Retrieval

These models will reside in `src/vindicta_engine/physics/models.py` or their own domain models file logically associated with the simulation. All inherit from `vindicta_foundation.models.base.VindictaModel`.

## `StatModifier` (Entity)
Represents a specific ability or keyword altering combat.
- `type`: str (e.g., "re_roll_hits", "lethal_hits", "anti")
- `value`: Optional[int] (e.g., The '4' in Anti-Vehicle 4+)
- `condition`: Optional[str] (e.g., "vehicle")

## `WeaponStatLine` (Entity)
Strongly typed combat parameters for a weapon instance.
- `weapon_name`: str
- `range`: int (0 for melee)
- `attacks`: str (e.g., "3", "D6") - kept as string to pass to the dice roller.
- `hit_on`: int (Target BS/WS)
- `strength`: int
- `ap`: int (Formatted to positive absolute integer internally if preferred)
- `damage`: str (e.g., "2", "D3")
- `modifiers`: List[StatModifier]

## `UnitProfile` (Entity)
Structured core statistics.
- `unit_name`: str
- `rules_version`: str
- `movement`: int
- `toughness`: int
- `save`: int
- `wounds`: int
- `leadership`: int
- `oc`: int
- `weapons`: List[WeaponStatLine]

## `StatCacheEntry` (Entity)
Internal caching wrapper.
- `profile`: UnitProfile
- `insertion_time`: float (Unix timestamp)
- `last_access`: float (Unix timestamp)
- `query_count`: int (Observability counter)

## State Transitions
**Cache Retrieval Workflow**:
1. Request for `(unit, weapon, version)` is received by `StatRetriever`.
2. Check `StatCache` dict. 
    - **HIT**: Update `last_access` and `query_count`, return immediately.
    - **MISS**: 
        a. Acquire async lock for this specific key to prevent thundering herds from parallel simulations.
        b. Check cache again inside lock (double-checked locking).
        c. Issue MCP query to RAG server. (Retry exactly once after 500ms on failure).
        d. Parse returned markdown into `UnitProfile`.
        e. Insert into `StatCache` with current timestamp.
        f. Enforce LRU eviction if cache size > limit (e.g., 500 entries).
        g. Release lock, return result.

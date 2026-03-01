# Research & Technical Decisions: Simulation Stat Retrieval

## 1. Async-Safe State Cache
- **Decision**: Use `asyncio.Lock` coupled with a standard `dict` for the cache store, or leverage an `asyncio` primitive like a bounded `LRU` cache implementation using `OrderedDict`. Since Python's dictionary is thread-safe for simple operations but async operations involving I/O (like an MCP query on a cache miss) need to prevent "thundering herd" query duplication, a per-key `asyncio.Event` or a unified `asyncio.Lock` is necessary during the retrieval phase.
- **Rationale**: The Monte Carlo simulator will trigger thousands of async lookup requests simultaneously. A simple lock prevents redundant network queries for the same unit while waiting for the RAG server to respond (FR-011).
- **Alternatives considered**: External caching like Redis (rejected: local-first MVP constraint), `functools.lru_cache` (rejected: doesn't handle shared async waiting cleanly without wrappers).

## 2. Markdown Parsing
- **Decision**: Utilize standard Python string processing and regex combined with Pydantic validation for the extraction of core combat modifiers and common keywords (FR-007). Unrecognized abilities will be captured as raw strings.
- **Rationale**: The RAG server returns Wahapedia/40k.app style structured markdown (tables, lists). Regex and basic table-parsing utilities are sufficient for the MVP "core" keywords, and Pydantic will ensure proper typed casting (e.g., extracting "3" from "WS 3+").
- **Alternatives considered**: LLM-based parsing at runtime (rejected: too slow for large simulation batches, parser needs to be deterministic and fast).

## 3. RAG Server MCP Communications
- **Decision**: Implement a lightweight asynchronous MCP client using the standard `mcp` SDK to query the rule segments. Implement a wrapper around the client request that catches `mcp` timeouts, waits ~500ms, and retries exactly once before raising an exception (FR-006).
- **Rationale**: Aligns with the platform's standard for MCP communication while fulfilling the robust error-handling requirement from the clarification session.
- **Alternatives considered**: Direct database queries to ChromaDB (rejected: violates the architectural container boundary by bypassing the RAG MCP server interface).

## 4. Cache Identity Key
- **Decision**: The cache key will be a formatted string or a named tuple: `(unit_name, weapon_name, rules_version)`. 
- **Rationale**: Directly aligns with the clarification for Q1. By embedding the version inside the key itself, cache invalidation for newly versioned data is handled inherently by a cache miss, preventing stale reads.
- **Alternatives considered**: Hashing the values (rejected: unnecessary overhead, the tuple/string is clean and unique).

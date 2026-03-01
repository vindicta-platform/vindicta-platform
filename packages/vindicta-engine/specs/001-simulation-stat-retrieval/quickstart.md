# Quickstart: Simulation Stat Retrieval

## Overview
This subsystem abstracts the heavy network calls to the local RAG rules server when loading Unit data for the Monte Carlo simulation engine. It parses the raw markdown output into structured Pydantic `UnitProfile` entities.

## Prerequisites
- The RAG MCP Server (setup in `005-rag-pipeline`) must be running locally.
- Engine execution must be wrapped in an `asyncio` event loop.

## Usage Example

```python
import asyncio
from vindicta_engine.retrieval.stat_cache import StatCache
from vindicta_engine.retrieval.mcp_client import RAGClient

async def run_simulation_batch():
    # Initialize the retrieval system
    rag_client = RAGClient(endpoint="http://localhost:8000/mcp") # Standard MCP config
    cache = StatCache(max_size=100)
    
    # Example request for a single unit profile
    unit_name = "Intercessor Squad"
    version = "1.0.0"
    
    # Retrieve the parsed stats (hits MCP on first call, then caches)
    try:
        profile = await cache.get_unit_stats(
            client=rag_client, 
            unit_name=unit_name, 
            version=version
        )
        print(f"Loaded {unit_name} with Toughness {profile.toughness}")
        
    except RAGQueryError as e:
        print(f"Failed to load stats after retry: {e}")

if __name__ == "__main__":
    asyncio.run(run_simulation_batch())
```

## Observability
Check the built-in tracking variables on the `StatCache` instance to verify metrics matching the specification:
```python
print(f"Cache Hits: {cache.metrics.hits}, Misses: {cache.metrics.misses}")
print(f"Parse Errors: {cache.metrics.parse_errors}")
```

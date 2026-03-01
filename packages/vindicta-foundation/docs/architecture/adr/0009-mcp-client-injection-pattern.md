# ADR-0009: MCP Client Injection Pattern

**Status**: Proposed
**Date**: 2026-02-23
**Decision Makers**: Brandon Fox

## Context

The `010-mcp-client-integration` spec (Vindicta-Agents) introduces an `MCPRulesClient` — an async client that agents use to query the local RAG MCP server for game rules. The platform must decide how this client is provided to individual agent nodes within the LangGraph swarm.

Two established injection patterns exist in the codebase:

1. **`RunnableConfig["configurable"]` injection** — used today by `NexusClient` (`nexus/client.py`). The client is instantiated once at graph startup and threaded through every node via LangGraph's `configurable` dict. Agents access it via `config["configurable"]["nexus_client"]`.
2. **Constructor injection** — each agent node class receives the client as a constructor argument, stored as an instance attribute.

The choice affects testability, concurrency safety, and how cleanly new tool clients can be added as the platform grows.

## Decision

Adopt the existing `RunnableConfig["configurable"]` injection pattern for `MCPRulesClient`, keyed as `mcp_client`.

Agents will access the client via:

```python
mcp_client: MCPRulesClient = config["configurable"]["mcp_client"]
result = await mcp_client.search_rules("toughness Space Marine")
```

The `swarm_startup.py` module will be responsible for instantiating and injecting the client into `RunnableConfig` at graph boot, alongside the existing `NexusClient`.

## Consequences

### Positive

- Consistent with the `NexusClient` precedent — zero new patterns for developers to learn
- LangGraph-native: `configurable` dict is the idiomatic way to pass shared resources through graph execution
- Easily mockable in tests: override the `configurable` key with a stub
- Supports concurrent graph invocations: each invocation can carry its own client instance if needed

### Negative

- Type safety relies on convention (string key `"mcp_client"`) rather than compile-time guarantees — a typo in the key silently returns `None`
- Adding many clients to `configurable` may eventually warrant a typed registry or dependency container

### Neutral

- The `MCPRulesClient` must be async-compatible, same as `NexusClient`
- This decision does not preclude wrapping the injection in a typed helper (e.g., `get_mcp_client(config)`) for safer access

## Alternatives Considered

1. **Constructor injection**: More explicit, but breaks the LangGraph functional node pattern where nodes are plain functions operating on `(state, config)`. Would require refactoring all nodes to classes.
2. **Global singleton**: Simplest, but untestable, not concurrency-safe across multiple graph invocations, and violates the platform's explicit-dependency principles.
3. **LangGraph `InjectedToolArg`**: Newer LangGraph feature for injecting runtime values into tool arguments. Could work for the `search_rules` tool specifically, but doesn't solve non-tool access patterns and adds coupling to a less-stable API.

## References

- [NexusClient injection](file:///c:/Users/bfoxt/vindicta-playground/Vindicta-Agents/src/vindicta_agents/nexus/client.py)
- [Swarm startup](file:///c:/Users/bfoxt/vindicta-playground/Vindicta-Agents/src/vindicta_agents/swarm_startup.py)
- [LangGraph RunnableConfig docs](https://langchain-ai.github.io/langgraph/concepts/low_level/#runnableconfig)
- [010-mcp-client-integration spec](file:///c:/Users/bfoxt/vindicta-playground/Vindicta-Agents/specs/010-mcp-client-integration/spec.md)

# ADR-0011: Adopt Model Context Protocol (MCP)

**Status**: Accepted
**Date**: 2026-02-23
**Decision Makers**: Brandon Fox

## Context

The Vindicta platform's AI swarm relies heavily on accessing external systems, specifically the `vindicta-foundation`'s RAG Pipeline for Warhammer 40k rules data. As the agent swarm scales out across different responsibilities (Meta-Oracle debates, Scribe rules verification, Arbitration predictions), creating tightly-coupled, proprietary APIs for every new tool becomes an unmaintainable architectural anti-pattern. Moreso, as new LLMs (from different providers) are implemented, integrating bespoke tooling configurations is inefficient.

## Decision

Adopt the **Model Context Protocol (MCP)** as the standard integration layer for all agent tools within the Vindicta ecosystem. 

All external tool interfaces—starting with the RAG Pipeline's `search_40k_rules` logic—MUST be exposed as an MCP Server. The `vindicta-agents` SDK MUST consume these services via an MCP Client interface.

## Consequences

### Positive

- **Interoperability**: Any MCP-compliant agent (Claude Desktop, local LangGraph agents, future LLM architectures) can discover and utilize Vindicta's tools without writing custom integration bridges.
- **Decoupled Architecture**: The server (e.g., Python FastAPI/MCP SDK) handles the complex backend (ChromaDB, Ollama), while the agent SDK remains lightweight, only needing an MCP network client.
- **Standardized Definitions**: Tool schemas (input/output) are strictly defined by the MCP specification, reducing hallucination caused by poorly described custom JSON-RPC schemas.
- **Centralized Security**: We can govern agent tool access via the MCP server Gateway rather than auditing every individual agent's REST client implementations.

### Negative

- Adds an abstraction networking layer (JSON-RPC over STDIO or HTTP/SSE) that slightly increases latency compared to direct in-process function execution.
- Small learning curve for developers unfamiliar with the MCP methodology.

### Neutral

- Requires the Vindicta system to implement an MCP Server boundary in addition to (or eventually replacing) traditional REST endpoints for agent-specific tasks.

## Alternatives Considered

1. **Direct REST/FastAPI Integrations**: Rejected. Requires every agent to understand the specific HTTP semantics, error handling, and JSON schema of each tool endpoint manually. Doesn't scale cleanly to an arbitrary number of dynamically injected tools.
2. **In-Process Python Functions (LangChain `@tool`)**: Rejected. While fast, it couples the Agent's runtime environment to the Tool's dependencies (e.g., requiring the agent docker container to also run Chrome for scraping, or house the ChromaDB vector logic).

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [005-rag-pipeline spec](file:///c:/Users/bfoxt/vindicta-playground/vindicta-foundation/specs/005-rag-pipeline/spec.md)

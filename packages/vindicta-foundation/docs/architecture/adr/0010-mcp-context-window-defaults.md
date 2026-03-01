# ADR-0010: MCP Client Context Window Defaults

**Status**: Proposed
**Date**: 2026-02-23
**Decision Makers**: Brandon Fox

## Context

The `MCPRulesClient` (spec `010-mcp-client-integration`) retrieves rule markdown chunks from the RAG MCP server. A single broad query can return 10–20 chunks totalling 10,000–15,000+ tokens. Agents operate within finite LLM context windows (Gemini 1.5 Flash: 1M tokens theoretical, but practical prompt budgets are much smaller for cost and latency reasons). Without a client-side cap, agents risk:

1. **Context pollution** — low-relevance chunks dilute the signal for the LLM.
2. **Latency bloat** — more tokens = slower inference, violating the <1.5s retrieval target.
3. **Silent truncation** — if the LLM or framework truncates input silently, critical rules may be lost unpredictably.

A default token budget must be chosen. The trade-off is between comprehensiveness (more context = more rules coverage) and precision (less context = faster, more focused reasoning).

## Decision

Set the default `max_context_tokens` to **8,192 tokens** with the following truncation strategy:

1. Chunks are returned in descending relevance order (highest `score` first).
2. Chunks are accumulated until adding the next chunk would exceed the budget.
3. **No mid-chunk splitting** — a chunk is either fully included or fully excluded.
4. If any chunks are dropped, the `RulesQueryResult.truncated` flag is set to `true` and a `structlog` warning is emitted.

Token estimation uses a simple heuristic: `len(content) // 4` (roughly 4 characters per token for English text). This avoids a tokenizer dependency while being accurate enough for budget enforcement.

### Rationale for 8,192

- Gemini 1.5 Flash handles 8K retrieval context comfortably alongside a system prompt and conversation history.
- The RAG pipeline's average chunk size is ~500 tokens, so 8,192 tokens ≈ 16 chunks — enough to cover most focused queries without overloading.
- Agents with specialized needs (e.g., full-army analysis) can override to higher values explicitly.
- The value is a power of two, aligning with common LLM context window conventions.

## Consequences

### Positive

- Predictable agent behaviour: retrieved context size is bounded and documented
- Agents always receive the most relevant chunks first
- No silent data loss — truncation is explicit via `truncated` flag and logging
- Zero external tokenizer dependency (no `tiktoken`, no model-specific encoders)

### Negative

- The `len // 4` heuristic is approximate — actual token counts may vary ±15% for non-English text, code blocks, or special characters in rules markdown
- 8,192 may be too conservative for agents doing cross-faction comparisons that legitimately need 20+ chunks
- Overriding the default requires the caller to know and set `max_context_tokens`, which is a configuration detail leaked to the agent layer

### Neutral

- The default can be adjusted in `MCPClientConfig` without breaking changes
- A future ADR could introduce model-aware tokenization if the heuristic proves insufficient

## Alternatives Considered

1. **No default cap (unlimited)**: Risks context pollution, unpredictable latency, and silent truncation at the LLM level. Rejected.
2. **4,096 tokens**: Too restrictive for queries spanning multiple units or complex interactions. Would frequently trigger truncation on routine queries.
3. **16,384 tokens**: Generous but risks latency degradation and wastes context budget that agents need for conversation history and system prompts.
4. **Exact tokenizer (tiktoken / SentencePiece)**: Accurate but adds a heavy dependency, couples the client to a specific model family, and is overkill for a budget enforcement heuristic.

## References

- [010-mcp-client-integration spec](file:///c:/Users/bfoxt/vindicta-playground/Vindicta-Agents/specs/010-mcp-client-integration/spec.md)
- [005-rag-pipeline spec](file:///c:/Users/bfoxt/vindicta-playground/vindicta-foundation/specs/005-rag-pipeline/spec.md) — defines chunk structure and scoring
- [Gemini 1.5 Flash context window](https://ai.google.dev/gemini-api/docs/models#gemini-1.5-flash)

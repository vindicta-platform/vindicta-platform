# ADR-0012: Local-First Offline RAG Pipeline

**Status**: Accepted
**Date**: 2026-02-23
**Decision Makers**: Brandon Fox

## Context

The `vindicta-platform` requires a Retrieval-Augmented Generation (RAG) subsystem (the `vindicta-oracle`) capable of storing and searching the complex, hierarchical rulesets of Warhammer 40k. 

A traditional GenAI application would typically deploy an external cloud-hosted Vector Database (Pinecone, Weaviate) and rely on commercial embedding models (OpenAI `text-embedding-3-large`). However, the Vindicta Platform architecture enforces a strict **Local-First MVP Constraint** for all underlying primitives (as defined in the Zero-Order Axioms surrounding deterministic play and cost efficiency).

## Decision

The RAG pipeline MUST be implemented using purely local, embedded, and "cost-free" infrastructure during the platform's MVP and Gen-Zero phases.

1. **Storage**: The pipeline will utilize `ChromaDB` running in `PersistentClient` mode (embedded directly into the local filesystem) backed by SQLite for metadata persistence. 
2. **Embeddings**: The pipeline will exclusively use the `ollama` unified Python client calling locally hosted embedding models (e.g., `nomic-embed-text` or `llama3.2`).

## Consequences

### Positive

- **Zero Operational Cost**: The RAG subsystem incurs zero API charges for computing embeddings or storing vectors, aligning with the `Economy-Engine`'s stringent cost limits.
- **Offline Capability**: Developers and agents can run full test suites, integration layers, and queries entirely offline, removing network latency bottlenecks during rapid iterations.
- **Privacy and Sovereignty**: Proprietary wargaming lists, transcripts, and potential future private strategies are kept strictly local, upholding data sovereignty for players.

### Negative

- **Resource Constraint**: Local embedding generation and ChromaDB lookups consume significant local RAM/CPU, meaning development machines (and eventually production agents) require sufficient hardware to host the models.
- **Scaling Complexity**: An embedded local SQLite/Chroma setup is not horizontally scalable. As the platform moves beyond the MVP into concurrent multi-tenant usage, an externalized service will be required. 

### Neutral

- Dependency Injection Protocols (e.g., `EmbeddingProvider` and `VectorStore`) MUST be strictly utilized to ensure that the core logic can seamlessly swap from the local Ollama/Chroma implementation to cloud equivalents without rewriting the subsystem.

## Alternatives Considered

1. **OpenAI / Pinecone**: Rejected due to high ongoing costs and violation of the local-first MVP mandate.
2. **PostgreSQL + pgvector**: Rejected. While open-source, it requires a dedicated background database daemon running (or a heavy Docker compose setup), violating the simplistic install-and-run requirement for the MVP architecture compared to embedded ChromaDB.

## References

- [005-rag-pipeline spec](file:///c:/Users/bfoxt/vindicta-playground/vindicta-foundation/specs/005-rag-pipeline/spec.md)

# ADR-0013: Idempotent Markdown Hashing for Ingestion

**Status**: Accepted
**Date**: 2026-02-23
**Decision Makers**: Brandon Fox

## Context

The Vindicta Oracle's RAG Pipeline handles large volumes of scraped web text and data transformations (e.g., Wahapedia rules) converted to optimized Markdown for the Agent Swarm. 

Because sources frequently update—and because scraping runs may overlap or crash—the Storage Layer cannot simply perform unstructured `INSERT` commands. Without a deterministic identification schema for knowledge chunks, the Vector DB (`ChromaDB`) would balloon with duplicated embeddings of identical rules, causing retrieval degradation, unnecessary compute costs, and a polluted context window.

## Decision

All ingested content MUST enforce idempotency through the cryptographic hashing of its Markdown payload strings before storage.

1. **The Hash Algorithm:** The pipeline will use a deterministic `SHA-256` digest constructed directly from the cleaned Markdown string of any given `RulesSegment`.
2. **Identification:** This hash strictly becomes the chunk's primary key (ID) inside the Vector database and the SQLite metadata store.
3. **Upsert Logic:** Before embedding a chunk, the system must query via the computed hash.
   - If the hash exists, `SKIP` entirely (avoiding the expensive LLM embedding call).
   - If a chunk exists with the *same URL* but a *different hash*, treat it as an update, increment the `version_id`, and `UPSERT`.

## Consequences

### Positive

- **Compute Efficiency**: Embedding operations (which are slow and computationally heavy) are only ever performed on purely novel or changed rules text. Identical re-scrapes cost almost zero compute.
- **Database Purity**: Duplicate results are mathematically eliminated from the Vector DB results, ensuring Agents receive the highest density of unique, relevant context without repeated paragraphs.
- **Traceability**: Given a specific markdown string, its location and history in the database can be determined globally without executing a fuzzy vector search.

### Negative

- Small compute overhead in calculating SHA-256 digests for every scraped element during the ingest loop.
- Vulnerability to formatting flux: If the scraper parser changes slightly (e.g., adding an extra space or altering header depth), the hash changes, triggering a full re-embedding of the corpus even if the semantic meaning is identical.

### Neutral

- The hashing mechanism requires strict sanitation (trimming whitespace, standardizing precise line endings) *before* the digest is generated to maximize cache hits.

## Alternatives Considered

1. **Semantic Deduplication**: Running an embedding pass first and rejecting chunks if cosine similarity is `> 0.999`. Rejected. This forces the system to perform the expensive embedding task *before* deciding if the data is useless, defeating the efficiency goal.
2. **URL + Section Header Primary Keys**: Rejected. While human readable, structural header names change, and URLs do not guarantee content stability when FAQs or errata drop.

## References

- [005-rag-pipeline spec](file:///c:/Users/bfoxt/vindicta-playground/vindicta-foundation/specs/005-rag-pipeline/spec.md)

# Technical Research: RAG Pipeline

**Feature Branch**: `005-rag-pipeline`
**Date**: 2026-02-23

## Research Objectives
Resolve unknowns regarding the local tooling and tech stack for the MVP RAG Pipeline, aligning with the user constraint: "Use local models and local tooling for MVP".

### 1. Vector Storage Database
- **Decision**: **ChromaDB**
- **Rationale**: ChromaDB is exceptionally well-suited for local, entirely strictly-offline MVPs. It runs embedded natively in Python without requiring any external docker containers for the database itself, perfectly adhering to the "local tooling" requirement. It also seamlessly integrates with local embedding providers.
- **Alternatives considered**: 
  - *LanceDB*: Also excellent for embedded usage, but Chroma provides a somewhat gentler learning curve for rapid MVP integration.
  - *Pinecone / Milvus*: Rejected because they are cloud-first or require complex infrastructure deployment, violating the local MVP constraint.

### 2. Local AI Model Tooling
- **Decision**: **Ollama** (for both Embeddings and LLM Generation)
- **Rationale**: The user specifically requested "local models and local tooling for MVP". Ollama allows us to run models like `mxbai-embed-large` or `nomic-embed-text` locally for generating vector embeddings of the rule chunks, and models like `llama3` or `phi3` for generation via the MCP server, completely offline and at zero cost.
- **Alternatives considered**:
  - *OpenAI / Gemini APIs*: Rejected due to the explicit constraint to use local models for the MVP.
  - *HuggingFace sentence-transformers*: Viable for embeddings, but Ollama provides a unified API for both the embedding model and the generation model, simplifying the architecture.

### 3. Scraping Strategy
- **Decision**: **crawl4ai**
- **Rationale**: As previously established, Wahapedia and 40k.app use dynamic JS rendering. `crawl4ai` provides a streamlined way to extract purely markdown text from dynamic elements, minimizing token usage for local models compared to raw HTML.
- **Alternatives considered**: *Playwright* (too much boilerplate), *BeautifulSoup* (cannot render JS).

## Further Research on Modern Tooling
- **Model Context Protocol (MCP)**: MCP is rapidly emerging as the industry standard for connecting AI agents to external tools and data sources. Utilizing the Python MCP SDK allows the RAG pipeline to be exposed as a standard server. Any MCP-compliant client can instantly understand the `search_40k_rules` tool signature without custom integration logic.
- **Embedded Database viability**: While production systems use external highly-available Vector DBs (Milvus/Pinecone), the SQLite+Parquet backend of ChromaDB embedded mode is robust enough for tens of thousands of vectors. This matches the scope of Wahapedia entirely while remaining strictly local.
- **Crawling Dynamic Web Apps**: Wahapedia and 40k.app heavily rely on client-side state. `crawl4ai` integrates LLM-based extraction if needed, but its pure DOM-to-Markdown feature strips out headers, footers, and noise automatically, dramatically lowering the semantic noise in the RAG chunks.

## Proposed Decisions for ADRs
To ensure platform alignment across the `vindicta-foundation`, the following ADRs should be drafted:
- **ADR-TODO: Adopt Model Context Protocol (MCP)**: Formalize MCP as the standard integration layer for all agent tools within the Vindicta ecosystem, starting with the RAG Pipeline.
- **ADR-TODO: Local-First Offline RAG**: Mandate that all core rule lookups must function in an air-gapped environment using local Ollama embeddings and embedded ChromaDB, adhering to the Zero-Order Axioms.
- **ADR-TODO: Idempotent Markdown Hashing**: Establish the standard of using SHA-256 cryptographic hashes of markdown content as the idempotency key for all ingested data, preventing database bloat and staleness.

## Platform Alignment Assessment
- Models like `RulesSegment` and `AgentQuery` must inherit from `VindictaModel` located in `src/vindicta_foundation/models/base.py` and must be explicitly exported in `src/vindicta_foundation/models/__init__.py` (per Tier 2 Builder Law). The current `plan.md` indicates placing models in `vindicta_oracle`. This needs reconciling to ensure strict structural integrity.

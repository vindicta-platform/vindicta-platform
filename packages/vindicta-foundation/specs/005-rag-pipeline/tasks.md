# Implementation Tasks: RAG Pipeline

**Feature Branch**: `005-rag-pipeline`

## Phase 1: Foundation Models

- [X] Create `src/vindicta_foundation/models/rag.py`
  - [X] Implement `RulesSegment` model extending `VindictaModel` (include embedding vector, URL, hash, timestamp, version id).
  - [X] Implement `AgentQuery` model extending `VindictaModel`.
  - [X] Update `src/vindicta_foundation/models/__init__.py` to export the new models.
- [X] Ensure strict type hinting (`mypy`) is applied to new models.

## Phase 2: Ingest & Scraping Pipeline (`scraper.py`)

- [X] Create `src/vindicta_foundation/rag_pipeline/scraper.py`.
- [X] Integrate `crawl4ai` to scrape dynamic JS-rendered websites (FR-001).
- [X] Implement DOM element extraction to clean markdown optimized for LLMs (FR-002).
- [X] Implement SHA-256 chunk hashing to identify unique content changes.
- [X] Ensure the ingest pipeline ignores completely duplicate/unchanged content (FR-003, SC-003).
- [X] Write unit tests in `tests/unit/test_scraper.py` covering DOM extraction and hashing.

## Phase 3: Storage Layer (`storage.py`)

- [X] Create `src/vindicta_foundation/rag_pipeline/storage.py`.
- [X] Initialize embedded ChromaDB local database with SQLite metadata persistence (FR-004).
- [X] Integrate local `ollama` client for generating text embeddings.
- [X] Implement save/upsert logic for `RulesSegment` ensuring newest chunks shadow or version older segments (FR-006).
- [X] Write unit tests in `tests/unit/test_storage.py` covering chunk saving and querying.

## Phase 4: MCP Server (`server.py`)

- [X] Create `src/vindicta_foundation/mcp_server/server.py`.
- [X] Implement the standard Model Context Protocol (MCP) server interface (FR-005).
- [X] Expose `search_40k_rules` tool to allow Vindicta agents to query rules.
- [X] Connect the MCP tool to `storage.py` querying logic for retrieving relevant markdown rules excerpts.
- [X] Write integration test `tests/integration/test_mcp_server.py` verifying end-to-end local latency expectations (< 1.5 seconds) and context retrieval (SC-001, SC-002).

## Phase 5: CI & Validation

- [X] Validate 90% test coverage using `uv run pytest`.
- [X] Run `ruff check .` and `ruff format --check .` to ensure compliance.
- [X] Run `mypy` strict type checking across the entire `vindicta_foundation` module.

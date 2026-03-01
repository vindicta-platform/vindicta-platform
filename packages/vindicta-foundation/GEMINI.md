# vindicta-foundation Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-22

## Active Technologies
- Python 3.12+ (uv workspace) + mcp (Model Context Protocol SDK), crawl4ai, chromadb, ollama (for local Python client embeddings) (005-rag-pipeline)
- Embedded ChromaDB (vector database) + SQLite metadata (persisted locally on disk) (005-rag-pipeline)

- Python 3.11+ + `pytesseract`, `opencv-python`, `Pillow`, `pydantic`, `click` (001-ocr-parser)

## Project Structure

```text
src/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.11+: Follow standard conventions

## Recent Changes
- 005-rag-pipeline: Added Python 3.12+ (uv workspace) + mcp (Model Context Protocol SDK), crawl4ai, chromadb, ollama (for local Python client embeddings)

- 001-ocr-parser: Added Python 3.11+ + `pytesseract`, `opencv-python`, `Pillow`, `pydantic`, `click`

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->

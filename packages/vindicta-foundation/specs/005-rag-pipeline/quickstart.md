# Quickstart: RAG Pipeline

This quickstart guides you through running the local MVP of the RAG Pipeline for Vindicta Agents. 

## Prerequisites
- Ollama installed locally (`ollama pull llama3`, `ollama pull nomic-embed-text`)
- Start the Ollama local daemon.
- `uv` for python dependencies.

## 1. Environment Setup

```bash
# From the repository root
uv sync
```

## 2. Running the Scraper

```bash
uv run python src/vindicta_oracle/rag_pipeline/scraper.py --target "https://www.40k.app/"
```
This command spins up `crawl4ai`, converts complex targets to markdown, generates embeddings via Ollama, and persists them into the local ChromaDB.

## 3. Starting the MCP Server

```bash
uv run python src/vindicta_oracle/mcp_server/server.py
```
This runs the local JSON-RPC MCP server. Connect your agent utilizing the `search_40k_rules` tool to issue semantic search queries locally, resolving against Ollama and the Vector database.

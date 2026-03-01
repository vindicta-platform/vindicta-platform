"""Integration-style tests for the MCP server tool handler."""

from __future__ import annotations

from typing import Any

import pytest

from vindicta_foundation.mcp_server.server import McpToolHandler
from vindicta_foundation.rag_pipeline.scraper import ScrapedChunk, compute_content_hash
from vindicta_foundation.rag_pipeline.storage import RulesStorage


class MockEmbedder:
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


class MockVectorStore:
    def __init__(self) -> None:
        self._documents: dict[str, dict[str, Any]] = {}

    def upsert(
        self,
        ids: list[str],
        documents: list[str],
        metadatas: list[dict[str, Any]],
        embeddings: list[list[float]],
    ) -> None:
        for doc_id, doc, meta, emb in zip(ids, documents, metadatas, embeddings):
            self._documents[doc_id] = {
                "document": doc,
                "metadata": meta,
                "embedding": emb,
            }

    def query(
        self,
        query_embeddings: list[list[float]],
        n_results: int = 5,
    ) -> dict[str, Any]:
        all_docs = list(self._documents.values())[:n_results]
        return {
            "documents": [[d["document"] for d in all_docs]],
            "metadatas": [[d["metadata"] for d in all_docs]],
            "distances": [[0.05] * len(all_docs)],
        }

    def get(
        self,
        ids: list[str] | None = None,
        where: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        results: list[dict[str, Any]] = []
        for entry in self._documents.values():
            if where:
                meta = entry["metadata"]
                if all(meta.get(k) == v for k, v in where.items()):
                    results.append(entry)
        return {
            "documents": [r["document"] for r in results],
            "metadatas": [r["metadata"] for r in results],
        }


@pytest.fixture
def handler() -> McpToolHandler:
    store = MockVectorStore()
    embedder = MockEmbedder()
    storage = RulesStorage(store=store, embedder=embedder)

    # Seed some data
    content = "Space Marines have Toughness 4 and Save 3+."
    chunk = ScrapedChunk(
        url="https://wahapedia.ru/space-marines",
        content_markdown=content,
        content_hash=compute_content_hash(content),
    )
    storage.store_chunk(chunk)

    return McpToolHandler(storage=storage)


class TestMcpToolHandler:
    def test_search_returns_results(self, handler: McpToolHandler) -> None:
        result = handler.search_40k_rules("What is the toughness of a Space Marine?")
        assert result["count"] > 0
        assert len(result["results"]) > 0
        assert "content" in result["results"][0]

    def test_query_metadata_included(self, handler: McpToolHandler) -> None:
        result = handler.search_40k_rules("Space Marine stats", agent_id="test-agent")
        assert result["query"]["agent_id"] == "test-agent"
        assert result["query"]["text"] == "Space Marine stats"

    def test_invalid_query_raises(self, handler: McpToolHandler) -> None:
        with pytest.raises(Exception):
            handler.search_40k_rules("ab")  # Too short

    def test_tool_definitions(self, handler: McpToolHandler) -> None:
        defs = handler.get_tool_definitions()
        assert len(defs) == 1
        assert defs[0]["name"] == "search_40k_rules"
        assert "inputSchema" in defs[0]
        assert "query_text" in defs[0]["inputSchema"]["properties"]

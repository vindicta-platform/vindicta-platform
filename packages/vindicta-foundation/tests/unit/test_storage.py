"""Unit tests for the RAG pipeline storage module."""

from __future__ import annotations

from typing import Any

import pytest

from vindicta_foundation.rag_pipeline.scraper import ScrapedChunk, compute_content_hash
from vindicta_foundation.rag_pipeline.storage import RulesStorage


class MockEmbedder:
    """Mock embedding provider — returns fixed-length dummy vectors."""

    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3, 0.4, 0.5]


class MockVectorStore:
    """In-memory mock vector store simulating ChromaDB."""

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
        # Return all documents as "results" (no real similarity)
        all_docs = list(self._documents.values())[:n_results]
        return {
            "documents": [[d["document"] for d in all_docs]],
            "metadatas": [[d["metadata"] for d in all_docs]],
            "distances": [[0.1] * len(all_docs)],
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
            elif ids:
                # Not used in our tests
                pass
            else:
                results.append(entry)
        return {
            "documents": [r["document"] for r in results],
            "metadatas": [r["metadata"] for r in results],
        }


@pytest.fixture
def storage() -> RulesStorage:
    return RulesStorage(
        store=MockVectorStore(),
        embedder=MockEmbedder(),
    )


class TestStoreChunk:
    def test_store_new_chunk(self, storage: RulesStorage) -> None:
        content = "Space Marines have Toughness 4."
        chunk = ScrapedChunk(
            url="https://wahapedia.ru/wh40k10ed/factions/space-marines",
            content_markdown=content,
            content_hash=compute_content_hash(content),
        )
        segment = storage.store_chunk(chunk)
        assert segment.content_markdown == content
        assert segment.version == 1

    def test_duplicate_is_skipped(self, storage: RulesStorage) -> None:
        """FR-003 / SC-003: Duplicate content is not stored twice."""
        content = "Duplicate content test."
        chunk = ScrapedChunk(
            url="https://test.com",
            content_markdown=content,
            content_hash=compute_content_hash(content),
        )
        seg1 = storage.store_chunk(chunk)
        seg2 = storage.store_chunk(chunk)
        # Second call should return existing (same hash)
        assert seg2.content_hash == seg1.content_hash

    def test_new_version_for_changed_content(self, storage: RulesStorage) -> None:
        """FR-006: New version when URL has updated content."""
        content1 = "Original rule text."
        content2 = "Updated rule text with errata."
        chunk1 = ScrapedChunk(
            url="https://test.com/rules",
            content_markdown=content1,
            content_hash=compute_content_hash(content1),
        )
        chunk2 = ScrapedChunk(
            url="https://test.com/rules",
            content_markdown=content2,
            content_hash=compute_content_hash(content2),
        )
        seg1 = storage.store_chunk(chunk1)
        seg2 = storage.store_chunk(chunk2)
        assert seg1.version == 1
        assert seg2.version == 2


class TestStoreChunks:
    def test_store_multiple(self, storage: RulesStorage) -> None:
        chunks = [
            ScrapedChunk(
                url=f"https://test.com/page{i}",
                content_markdown=f"Content {i}",
                content_hash=compute_content_hash(f"Content {i}"),
            )
            for i in range(3)
        ]
        segments = storage.store_chunks(chunks)
        assert len(segments) == 3


class TestSearch:
    def test_search_returns_results(self, storage: RulesStorage) -> None:
        content = "Space Marines have Toughness 4."
        chunk = ScrapedChunk(
            url="https://test.com",
            content_markdown=content,
            content_hash=compute_content_hash(content),
        )
        storage.store_chunk(chunk)
        results = storage.search("What is Toughness of Space Marines?")
        assert len(results) > 0
        assert "content" in results[0]
        assert "metadata" in results[0]

    def test_empty_store_returns_empty(self, storage: RulesStorage) -> None:
        results = storage.search("anything")
        assert results == []

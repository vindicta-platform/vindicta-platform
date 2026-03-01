"""Unit tests for the RAG pipeline scraper module."""

from __future__ import annotations

import asyncio

from vindicta_foundation.rag_pipeline.scraper import (
    ScrapeResult,
    compute_content_hash,
    extract_markdown_chunks,
    scrape_url,
    scrape_urls,
)


class TestContentHash:
    def test_deterministic(self) -> None:
        h1 = compute_content_hash("hello world")
        h2 = compute_content_hash("hello world")
        assert h1 == h2

    def test_different_content_different_hash(self) -> None:
        h1 = compute_content_hash("hello")
        h2 = compute_content_hash("world")
        assert h1 != h2

    def test_sha256_length(self) -> None:
        h = compute_content_hash("test")
        assert len(h) == 64

    def test_empty_string(self) -> None:
        h = compute_content_hash("")
        assert len(h) == 64


class TestExtractMarkdownChunks:
    def test_empty_content_returns_empty(self) -> None:
        chunks = extract_markdown_chunks("", "https://example.com")
        assert chunks == []

    def test_whitespace_only_returns_empty(self) -> None:
        chunks = extract_markdown_chunks("   \n\n  ", "https://example.com")
        assert chunks == []

    def test_single_paragraph(self) -> None:
        text = "This is a test paragraph."
        chunks = extract_markdown_chunks(text, "https://example.com")
        assert len(chunks) == 1
        assert chunks[0].url == "https://example.com"
        assert chunks[0].content_markdown == text
        assert len(chunks[0].content_hash) == 64

    def test_multiple_paragraphs_under_limit(self) -> None:
        text = "Para 1\n\nPara 2\n\nPara 3"
        chunks = extract_markdown_chunks(text, "https://test.com", chunk_size=5000)
        assert len(chunks) == 1

    def test_large_content_splits_into_chunks(self) -> None:
        text = "\n\n".join(f"Paragraph {i} with some content" for i in range(50))
        chunks = extract_markdown_chunks(text, "https://test.com", chunk_size=200)
        assert len(chunks) > 1

    def test_all_chunks_have_hashes(self) -> None:
        text = "\n\n".join(f"Paragraph {i}" for i in range(10))
        chunks = extract_markdown_chunks(text, "https://test.com", chunk_size=50)
        for chunk in chunks:
            assert len(chunk.content_hash) == 64
            assert chunk.url == "https://test.com"


class MockCrawler:
    """Mock crawler for testing."""

    def __init__(self, responses: dict[str, str]) -> None:
        self._responses = responses

    async def fetch_markdown(self, url: str) -> str:
        if url in self._responses:
            return self._responses[url]
        raise ConnectionError(f"Failed to fetch {url}")


class TestScrapeUrl:
    def test_scrape_with_mock_crawler(self) -> None:
        crawler = MockCrawler({"https://test.com": "# Test Rules\n\nSome rules."})
        chunks = asyncio.run(scrape_url("https://test.com", crawler=crawler))
        assert len(chunks) > 0
        assert chunks[0].url == "https://test.com"

    def test_scrape_failure_returns_empty(self) -> None:
        crawler = MockCrawler({})
        chunks = asyncio.run(scrape_url("https://missing.com", crawler=crawler))
        assert chunks == []


class TestScrapeUrls:
    def test_resilient_scraping(self) -> None:
        """FR-007: Failed pages are skipped, remaining continue."""
        crawler = MockCrawler(
            {
                "https://ok.com": "# OK\n\nContent here.",
                # https://fail.com is missing → scrape_url handles gracefully
            }
        )
        result = asyncio.run(
            scrape_urls(
                ["https://ok.com", "https://fail.com"],
                crawler=crawler,
            )
        )
        assert isinstance(result, ScrapeResult)
        # ok.com produces chunks; fail.com silently returns 0 chunks
        assert result.success_count > 0

    def test_all_success(self) -> None:
        crawler = MockCrawler(
            {
                "https://a.com": "Content A",
                "https://b.com": "Content B",
            }
        )
        result = asyncio.run(
            scrape_urls(["https://a.com", "https://b.com"], crawler=crawler)
        )
        assert result.error_count == 0
        assert result.success_count >= 2

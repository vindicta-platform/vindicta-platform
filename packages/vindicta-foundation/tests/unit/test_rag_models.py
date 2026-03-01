"""Tests for RAG domain models — RulesSegment and AgentQuery."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from vindicta_foundation.models.rag import AgentQuery, RulesSegment


class TestRulesSegment:
    def test_valid_construction(self) -> None:
        content = "Space Marines have BS 3+."
        segment = RulesSegment(
            url="https://wahapedia.ru/wh40k10ed/factions/space-marines",  # type: ignore[arg-type]
            content_markdown=content,
            content_hash=RulesSegment.compute_hash(content),
        )
        assert segment.content_markdown == content
        assert segment.version == 1
        assert len(segment.content_hash) == 64

    def test_empty_content_rejected(self) -> None:
        with pytest.raises(ValidationError, match="content_markdown"):
            RulesSegment(
                url="https://test.com",  # type: ignore[arg-type]
                content_markdown="",
                content_hash="a" * 64,
            )

    def test_invalid_hash_length(self) -> None:
        with pytest.raises(ValidationError, match="64 hex characters"):
            RulesSegment(
                url="https://test.com",  # type: ignore[arg-type]
                content_markdown="Some content",
                content_hash="tooshort",
            )

    def test_compute_hash_static(self) -> None:
        h = RulesSegment.compute_hash("test")
        assert len(h) == 64
        assert h == RulesSegment.compute_hash("test")

    def test_serialization_round_trip(self) -> None:
        content = "Test rules content."
        segment = RulesSegment(
            url="https://test.com",  # type: ignore[arg-type]
            content_markdown=content,
            content_hash=RulesSegment.compute_hash(content),
        )
        json_str = segment.model_dump_json()
        restored = RulesSegment.model_validate_json(json_str)
        assert restored.content_markdown == content
        assert restored.content_hash == segment.content_hash


class TestAgentQuery:
    def test_valid_query(self) -> None:
        query = AgentQuery(query_text="What is Toughness?")
        assert query.query_text == "What is Toughness?"
        assert query.agent_id == "unknown"

    def test_short_query_rejected(self) -> None:
        with pytest.raises(ValidationError, match="4 characters"):
            AgentQuery(query_text="ab")

    def test_long_query_rejected(self) -> None:
        with pytest.raises(ValidationError, match="4096 characters"):
            AgentQuery(query_text="x" * 4097)

    def test_boundary_4_chars(self) -> None:
        query = AgentQuery(query_text="test")
        assert query.query_text == "test"

"""Unit tests for Phase 2: State Model & Spec Queue.

Tests cover:
- SpecQueueItem and DeclineRecord dataclasses
- SpecQueue (add, pop, full, slots, peek)
- DeclineMemory (add, count, latest, history, format_for_prompt)
- VindictaState has all expected SDD lifecycle fields
"""

from __future__ import annotations

import pytest

from vindicta_agents.swarm.spec_queue import (
    DeclineMemory,
    DeclineRecord,
    SpecQueue,
    SpecQueueItem,
)
from vindicta_agents.swarm.state import VindictaState


# ──────────────────────────────────────────────
# SpecQueueItem
# ──────────────────────────────────────────────


class TestSpecQueueItem:
    def test_creation(self) -> None:
        item = SpecQueueItem(feature_name="auth", content="spec text")
        assert item.feature_name == "auth"
        assert item.content == "spec text"
        assert item.status == "pending"
        assert item.timestamp is not None

    def test_frozen(self) -> None:
        item = SpecQueueItem(feature_name="x", content="y")
        with pytest.raises(AttributeError):
            item.feature_name = "z"  # type: ignore[misc]


# ──────────────────────────────────────────────
# DeclineRecord
# ──────────────────────────────────────────────


class TestDeclineRecord:
    def test_creation(self) -> None:
        r = DeclineRecord(feature_name="bad-spec", reason="Too vague")
        assert r.feature_name == "bad-spec"
        assert r.reason == "Too vague"
        assert r.spec_content == ""

    def test_with_content(self) -> None:
        r = DeclineRecord(feature_name="x", reason="y", spec_content="full spec")
        assert r.spec_content == "full spec"


# ──────────────────────────────────────────────
# SpecQueue
# ──────────────────────────────────────────────


class TestSpecQueue:
    def test_starts_empty(self) -> None:
        q = SpecQueue(target_size=5)
        assert q.size == 0
        assert not q.is_full
        assert q.slots_available == 5

    def test_add(self) -> None:
        q = SpecQueue(target_size=5)
        item = q.add("auth", "Auth spec")
        assert item.feature_name == "auth"
        assert q.size == 1

    def test_add_multiple(self) -> None:
        q = SpecQueue(target_size=3)
        q.add("a", "A")
        q.add("b", "B")
        q.add("c", "C")
        assert q.size == 3
        assert q.is_full
        assert q.slots_available == 0

    def test_pop_fifo_order(self) -> None:
        q = SpecQueue()
        q.add("first", "1")
        q.add("second", "2")
        item = q.pop()
        assert item is not None
        assert item.feature_name == "first"
        assert q.size == 1

    def test_pop_empty(self) -> None:
        q = SpecQueue()
        assert q.pop() is None

    def test_peek(self) -> None:
        q = SpecQueue()
        q.add("alpha", "A")
        assert q.peek() is not None
        assert q.peek().feature_name == "alpha"  # type: ignore[union-attr]
        assert q.size == 1  # peek doesn't remove

    def test_peek_empty(self) -> None:
        q = SpecQueue()
        assert q.peek() is None

    def test_list_items(self) -> None:
        q = SpecQueue()
        q.add("x", "X")
        q.add("y", "Y")
        items = q.list_items()
        assert len(items) == 2
        assert items[0].feature_name == "x"

    def test_is_full_at_target(self) -> None:
        q = SpecQueue(target_size=2)
        q.add("a", "A")
        assert not q.is_full
        q.add("b", "B")
        assert q.is_full


# ──────────────────────────────────────────────
# DeclineMemory
# ──────────────────────────────────────────────


class TestDeclineMemory:
    def test_starts_empty(self) -> None:
        m = DeclineMemory()
        assert m.count == 0
        assert m.latest is None

    def test_add(self) -> None:
        m = DeclineMemory()
        r = m.add("bad-spec", "Too vague")
        assert r.feature_name == "bad-spec"
        assert m.count == 1

    def test_latest(self) -> None:
        m = DeclineMemory()
        m.add("a", "reason-a")
        m.add("b", "reason-b")
        assert m.latest is not None
        assert m.latest.reason == "reason-b"

    def test_get_history(self) -> None:
        m = DeclineMemory()
        m.add("x", "r1")
        m.add("y", "r2")
        history = m.get_history()
        assert len(history) == 2
        assert history[0].feature_name == "x"
        assert history[1].feature_name == "y"

    def test_format_for_prompt_empty(self) -> None:
        m = DeclineMemory()
        assert m.format_for_prompt() == "No previous rejections."

    def test_format_for_prompt(self) -> None:
        m = DeclineMemory()
        m.add("auth", "Missing acceptance criteria")
        m.add("cache", "Scope too broad")
        text = m.format_for_prompt()
        assert "Missing acceptance criteria" in text
        assert "Scope too broad" in text
        assert text.startswith("1.")


# ──────────────────────────────────────────────
# VindictaState field presence
# ──────────────────────────────────────────────


class TestVindictaState:
    """Verify that the TypedDict has all expected SDD lifecycle keys."""

    EXPECTED_FIELDS = [
        "intent",
        "sdd_stage",
        "feature_name",
        "branch_name",
        "spec_dir",
        "spec_content",
        "plan_content",
        "tasks_content",
        "tasks",
        "pr_url",
        "issue_urls",
        "spec_queue",
        "decline_memory",
        "current_phase",
        "error_log",
        "execution_log",
    ]

    def test_all_fields_present(self) -> None:
        annotations = VindictaState.__annotations__
        for f in self.EXPECTED_FIELDS:
            assert f in annotations, f"Missing field: {f}"

    def test_backward_compat(self) -> None:
        """Original fields from the old state are still present."""
        annotations = VindictaState.__annotations__
        for f in [
            "intent",
            "spec_content",
            "plan_content",
            "tasks",
            "current_phase",
            "error_log",
            "execution_log",
        ]:
            assert f in annotations

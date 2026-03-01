"""Unit tests for Phase 4: Review Gates.

Tests cover:
- ReviewDecision (approve/decline, reason)
- ReviewGate with AutoApproveBackend
- ReviewGate with AutoDeclineBackend
- ReviewGate with CallbackBackend
- Decline capture flow (decline → store reason in memory)
"""

from __future__ import annotations

import asyncio
import pytest

from vindicta_agents.swarm.review_gates import (
    AutoApproveBackend,
    AutoDeclineBackend,
    CallbackBackend,
    ReviewAction,
    ReviewDecision,
    ReviewGate,
)
from vindicta_agents.swarm.spec_queue import DeclineMemory


# ── ReviewDecision ───────────────────────────────────────────────────


class TestReviewDecision:
    def test_approve(self):
        d = ReviewDecision(action=ReviewAction.APPROVE)
        assert d.approved is True
        assert d.reason == ""

    def test_decline(self):
        d = ReviewDecision(action=ReviewAction.DECLINE, reason="Bad spec")
        assert d.approved is False
        assert d.reason == "Bad spec"

    def test_frozen(self):
        d = ReviewDecision(action=ReviewAction.APPROVE)
        with pytest.raises(AttributeError):
            d.action = ReviewAction.DECLINE  # type: ignore[misc]


# ── AutoApproveBackend ───────────────────────────────────────────────


class TestAutoApproveBackend:
    def test_always_approves(self):
        backend = AutoApproveBackend()
        decision = asyncio.get_event_loop().run_until_complete(
            backend.ask_decision("Test", "content", "spec_review")
        )
        assert decision.approved is True
        assert decision.reviewer == "auto"


# ── AutoDeclineBackend ───────────────────────────────────────────────


class TestAutoDeclineBackend:
    def test_declines_with_reason(self):
        backend = AutoDeclineBackend(reason="Missing tests")
        decision = asyncio.get_event_loop().run_until_complete(
            backend.ask_decision("Test", "content", "plan_review")
        )
        assert decision.approved is False
        assert decision.reason == "Missing tests"

    def test_default_reason(self):
        backend = AutoDeclineBackend()
        decision = asyncio.get_event_loop().run_until_complete(
            backend.ask_decision("Test", "content", "generic")
        )
        assert "Auto-declined" in decision.reason


# ── CallbackBackend ──────────────────────────────────────────────────


class TestCallbackBackend:
    def test_delegates_to_callback(self):
        def my_callback(title, content, gate_type):
            return ReviewDecision(
                action=ReviewAction.APPROVE
                if "good" in content
                else ReviewAction.DECLINE,
                reason="" if "good" in content else "Bad content",
            )

        backend = CallbackBackend(my_callback)

        good = asyncio.get_event_loop().run_until_complete(
            backend.ask_decision("Review", "this is good", "spec_review")
        )
        assert good.approved is True

        bad = asyncio.get_event_loop().run_until_complete(
            backend.ask_decision("Review", "this is terrible", "spec_review")
        )
        assert bad.approved is False
        assert bad.reason == "Bad content"


# ── ReviewGate ───────────────────────────────────────────────────────


class TestReviewGate:
    def test_approve_gate(self):
        gate = ReviewGate(backend=AutoApproveBackend(), gate_type="spec_review")
        decision = asyncio.get_event_loop().run_until_complete(
            gate.review("Spec: auth", "Auth spec content")
        )
        assert decision.approved is True

    def test_decline_gate(self):
        gate = ReviewGate(
            backend=AutoDeclineBackend("Needs AC"), gate_type="spec_review"
        )
        decision = asyncio.get_event_loop().run_until_complete(
            gate.review("Spec: auth", "Auth spec content")
        )
        assert decision.approved is False
        assert decision.reason == "Needs AC"

    def test_gate_type_preserved(self):
        gate = ReviewGate(backend=AutoApproveBackend(), gate_type="pr_merge")
        assert gate.gate_type == "pr_merge"


# ── Decline Capture Integration ──────────────────────────────────────


class TestDeclineCaptureFlow:
    def test_decline_stores_in_memory(self):
        """Simulate the full decline → store in memory flow."""
        gate = ReviewGate(
            backend=AutoDeclineBackend("Too vague"),
            gate_type="spec_review",
        )
        decision = asyncio.get_event_loop().run_until_complete(
            gate.review("Spec: auth", "Auth spec content")
        )

        # Store in decline memory (what nexus.py would do)
        memory = DeclineMemory()
        if not decision.approved:
            memory.add(
                feature_name="auth",
                reason=decision.reason,
                spec_content="Auth spec content",
            )

        assert memory.count == 1
        assert memory.latest is not None
        assert memory.latest.reason == "Too vague"
        assert "Too vague" in memory.format_for_prompt()

    def test_approve_does_not_store(self):
        gate = ReviewGate(
            backend=AutoApproveBackend(),
            gate_type="spec_review",
        )
        decision = asyncio.get_event_loop().run_until_complete(
            gate.review("Spec: auth", "Auth spec content")
        )

        memory = DeclineMemory()
        if not decision.approved:
            memory.add("auth", decision.reason)

        assert memory.count == 0

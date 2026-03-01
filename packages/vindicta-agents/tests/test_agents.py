"""Tests for vindicta-agents SDK models."""

from uuid import UUID, uuid4
from datetime import datetime

from vindicta_agents.sdk import (
    RequestPriority,
    AITask,
    TaskResult,
    QuotaBudget,
    TierLimits,
)
from vindicta_foundation.models.base import VindictaModel


def test_ai_task_inherits_vindicta_model():
    task = AITask(
        name="Test Analysis",
        prompt="Analyze this army list",
        priority=RequestPriority.NORMAL,
    )
    assert isinstance(task, VindictaModel)
    assert isinstance(task.id, UUID)
    assert task.model == "gemini-1.5-flash"


def test_ai_task_priority_ordering():
    assert RequestPriority.HUMAN < RequestPriority.CRITICAL
    assert RequestPriority.CRITICAL < RequestPriority.HIGH
    assert RequestPriority.HIGH < RequestPriority.NORMAL
    assert RequestPriority.NORMAL < RequestPriority.LOW
    assert RequestPriority.LOW < RequestPriority.BACKGROUND


def test_task_result_inherits_vindicta_model():
    result = TaskResult(
        task_id=uuid4(),
        status="success",
        response="Analysis complete.",
        tokens_used=150,
        latency_ms=320,
    )
    assert isinstance(result, VindictaModel)
    assert result.tokens_used == 150


def test_quota_budget():
    budget = QuotaBudget(
        requests_available=100,
        tokens_available=50000,
        window_end=datetime.utcnow(),
    )
    assert budget.human_reserve_percent == 20
    assert budget.confidence == 0.8


def test_tier_limits_defaults():
    limits = TierLimits()
    assert limits.tier_name == "free"
    assert limits.requests_per_minute == 15
    assert limits.requests_per_day == 1500

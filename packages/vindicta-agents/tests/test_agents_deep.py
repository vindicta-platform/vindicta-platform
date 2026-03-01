"""Phase 12: Deep tests for Agent SDK models (T183-T190)."""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from vindicta_agents.sdk.models import (
    RequestPriority,
    AITask,
    TaskResult,
    QuotaBudget,
    UsageEntry,
)


def test_aitask_estimated_tokens() -> None:
    """T183: AITask with estimated_tokens set and readable."""
    task = AITask(name="Test", prompt="Hello", estimated_tokens=500)
    assert task.estimated_tokens == 500

    task_no_tokens = AITask(name="No tokens", prompt="Hi")
    assert task_no_tokens.estimated_tokens is None


def test_aitask_history_conversation() -> None:
    """T184: AITask with history list containing multiple turns."""
    history = [
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": "4"},
        {"role": "user", "content": "And 3+3?"},
    ]
    task = AITask(name="Math", prompt="Answer", history=history)
    assert len(task.history) == 3
    assert task.history[0]["role"] == "user"
    assert task.history[1]["role"] == "assistant"


def test_task_result_failed() -> None:
    """T185: TaskResult with status 'failed' and error message."""
    result = TaskResult(
        task_id=uuid4(),
        status="failed",
        error="API rate limit exceeded",
    )
    assert result.status == "failed"
    assert result.error == "API rate limit exceeded"
    assert result.response is None


def test_task_result_cancelled() -> None:
    """T186: TaskResult with status 'cancelled' (valid Literal)."""
    result = TaskResult(
        task_id=uuid4(),
        status="cancelled",
    )
    assert result.status == "cancelled"


def test_task_result_invalid_status() -> None:
    """T187: TaskResult with invalid status string raises validation error."""
    with pytest.raises(ValueError):
        TaskResult(
            task_id=uuid4(),
            status="invalid_status",
        )


def test_quota_budget_negative_requests() -> None:
    """T188: QuotaBudget with negative requests_available raises error (ge=0)."""
    with pytest.raises(ValueError):
        QuotaBudget(
            requests_available=-1,
            tokens_available=1000,
            window_end=datetime.utcnow() + timedelta(hours=1),
        )


def test_quota_budget_confidence_over_one() -> None:
    """T189: QuotaBudget with confidence > 1.0 raises error (le=1.0)."""
    with pytest.raises(ValueError):
        QuotaBudget(
            requests_available=100,
            tokens_available=1000,
            window_end=datetime.utcnow() + timedelta(hours=1),
            confidence=1.5,
        )


def test_usage_entry_all_fields() -> None:
    """T190: UsageEntry dataclass construction with all fields."""
    entry = UsageEntry(
        timestamp=datetime.utcnow(),
        task_id="task-abc-123",
        request_type="human",
        priority=RequestPriority.HUMAN,
        tokens_used=100,
        requests_used=1,
        success=True,
        latency_ms=250,
        error=None,
        task_name="test_query",
    )
    assert entry.task_id == "task-abc-123"
    assert entry.request_type == "human"
    assert entry.priority == RequestPriority.HUMAN
    assert entry.success is True
    assert entry.error is None
    assert entry.task_name == "test_query"


def test_usage_entry_with_error() -> None:
    """T190b: UsageEntry with error field populated."""
    entry = UsageEntry(
        timestamp=datetime.utcnow(),
        task_id="task-err-456",
        request_type="background",
        priority=RequestPriority.LOW,
        tokens_used=0,
        requests_used=1,
        success=False,
        latency_ms=5000,
        error="Timeout after 5000ms",
    )
    assert entry.success is False
    assert entry.error == "Timeout after 5000ms"

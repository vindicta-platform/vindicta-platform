"""
Core data models for the Agent Auditor SDK.

Ported from Agent-Auditor-SDK. Entity models inherit VindictaModel.
Value objects (TierLimits, UsageEntry) remain as plain types.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field
from vindicta_foundation.models.base import VindictaModel


class RequestPriority(IntEnum):
    """Priority levels for task scheduling.

    Lower values = higher priority.
    P0 (HUMAN) always preempts all other priorities.
    """

    HUMAN = 0
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5


class AITask(VindictaModel):
    """A task to be executed against an AI API.

    Tasks are queued and executed based on priority and available quota.
    """

    name: str = Field(..., description="Human-readable task name")
    system: Optional[str] = Field(
        default=None, description="System prompt for the task"
    )
    prompt: str = Field(..., description="The prompt/payload to send")
    model: str = Field(default="gemini-1.5-flash", description="Target model")
    priority: RequestPriority = Field(
        default=RequestPriority.NORMAL,
        description="Task priority level",
    )

    history: List[Dict[str, str]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    estimated_tokens: Optional[int] = Field(
        default=None,
        description="Estimated token count for proactive rate limiting",
    )

    def execute(self, provider: Optional[Any] = None) -> str:
        """Executes the task using an LLM backend (MOCKED for now)."""
        if provider:
            return provider.execute(self.system, self.prompt)
        # Fallback to current mock
        return f"[MOCKED EXECUTION] System: {self.system} | User: {self.prompt}"

    def execute_json(self, provider: Optional[Any] = None) -> List[Dict[str, Any]]:
        """Executes the task and returns JSON output (MOCKED for now)."""
        if provider:
            return provider.execute_json(self.system, self.prompt)

        # Mocking a list of tasks for the ADL usage pattern
        return [
            {
                "id": "task-1",
                "description": "Implement core engine logic",
                "target_realm": "vindicta-engine",
                "status": "pending",
            },
            {
                "id": "task-2",
                "description": "Implement warscribe parsing",
                "target_realm": "warscribe-system",
                "status": "pending",
            },
            {
                "id": "task-3",
                "description": "Implement economy features",
                "target_realm": "vindicta-economy",
                "status": "pending",
            },
        ]


class TaskResult(VindictaModel):
    """Result of an executed AI task."""

    task_id: UUID
    status: Literal["success", "failed", "queued", "cancelled"]
    response: Optional[str] = None
    error: Optional[str] = None
    tokens_used: int = 0
    latency_ms: int = 0


class QuotaBudget(BaseModel):
    """Available quota budget for a time window (value object)."""

    requests_available: int = Field(ge=0)
    tokens_available: int = Field(ge=0)
    window_end: datetime
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)
    human_reserve_percent: int = Field(default=20, ge=0, le=100)


@dataclass
class UsageEntry:
    """A single API usage log entry (value object).

    IMPORTANT: Never log API keys or sensitive payloads.
    """

    timestamp: datetime
    task_id: str
    request_type: Literal["human", "background"]
    priority: RequestPriority
    tokens_used: int
    requests_used: int
    success: bool
    latency_ms: int
    error: Optional[str] = None
    task_name: str = ""


@dataclass
class TierLimits:
    """API tier rate limits (defaults to Gemini Free Tier)."""

    requests_per_minute: int = 15
    tokens_per_minute: int = 1_000_000
    requests_per_day: int = 1500
    tier_name: str = "free"


__all__ = [
    "RequestPriority",
    "AITask",
    "TaskResult",
    "QuotaBudget",
    "UsageEntry",
    "TierLimits",
]

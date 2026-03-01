"""Review gates for human-in-the-loop approval.

This module provides a ``ReviewGate`` abstraction that works with both
Chainlit (interactive) and programmatic (test/CLI) backends.

The gate pattern:
1. Present the artifact (spec, plan, PR) to the reviewer
2. Collect a decision: ``approve`` or ``decline``
3. If declined, collect a reason string
4. Return a ``ReviewDecision`` dataclass

Chainlit integration is in ``chainlit_app.py`` — this module stays
framework-agnostic so it can be unit-tested without Chainlit.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Protocol


class ReviewAction(str, Enum):
    """Possible reviewer actions."""

    APPROVE = "approve"
    DECLINE = "decline"


@dataclass(frozen=True)
class ReviewDecision:
    """Result of a human review gate."""

    action: ReviewAction
    reason: str = ""
    reviewer: str = ""

    @property
    def approved(self) -> bool:
        return self.action == ReviewAction.APPROVE


class ReviewBackend(Protocol):
    """Protocol for review UI backends.

    Implementations:
    - ``ChainlitReviewBackend``: uses ``cl.AskActionMessage``
    - ``AutoApproveBackend``: approves everything (tests)
    - ``CLIReviewBackend``: stdin-based (CLI mode)
    """

    async def ask_decision(
        self,
        title: str,
        content: str,
        gate_type: str,
    ) -> ReviewDecision: ...


class AutoApproveBackend:
    """Test backend that auto-approves everything."""

    async def ask_decision(
        self, title: str, content: str, gate_type: str
    ) -> ReviewDecision:
        return ReviewDecision(action=ReviewAction.APPROVE, reviewer="auto")


class AutoDeclineBackend:
    """Test backend that auto-declines with a fixed reason."""

    def __init__(self, reason: str = "Auto-declined for testing") -> None:
        self._reason = reason

    async def ask_decision(
        self, title: str, content: str, gate_type: str
    ) -> ReviewDecision:
        return ReviewDecision(
            action=ReviewAction.DECLINE,
            reason=self._reason,
            reviewer="auto",
        )


class CallbackBackend:
    """Backend that delegates to a sync callback (for programmatic control)."""

    def __init__(self, callback: Callable[[str, str, str], ReviewDecision]) -> None:
        self._callback = callback

    async def ask_decision(
        self, title: str, content: str, gate_type: str
    ) -> ReviewDecision:
        return self._callback(title, content, gate_type)


class ReviewGate:
    """Orchestrates a human review checkpoint.

    Parameters
    ----------
    backend:
        The UI backend to use for collecting decisions.
    gate_type:
        Identifies this gate (``spec_review``, ``plan_review``, ``pr_merge``).
    """

    def __init__(
        self,
        backend: ReviewBackend,
        gate_type: str = "generic",
    ) -> None:
        self.backend = backend
        self.gate_type = gate_type

    async def review(self, title: str, content: str) -> ReviewDecision:
        """Present the artifact and collect a decision."""
        return await self.backend.ask_decision(title, content, self.gate_type)

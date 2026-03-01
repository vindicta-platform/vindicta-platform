"""Spec Queue and Decline Memory for the autonomous PO loop.

The PO continuously generates specs, filling a queue of up to
``target_size`` items (default 5).  When a human declines a spec, the
reason is recorded in ``DeclineMemory`` so the PO can learn from past
rejections.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class SpecQueueItem:
    """A spec waiting for human review."""

    feature_name: str
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "pending"  # pending | approved | declined


@dataclass(frozen=True)
class DeclineRecord:
    """A record of a spec that was declined with a reason."""

    feature_name: str
    reason: str
    spec_content: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class SpecQueue:
    """FIFO queue of specs awaiting review.

    Parameters
    ----------
    target_size:
        Maximum number of specs the PO should keep ready.
    """

    def __init__(self, target_size: int = 5) -> None:
        self.target_size = target_size
        self._items: list[SpecQueueItem] = []

    # ---- queue operations ----

    def add(self, feature_name: str, content: str) -> SpecQueueItem:
        """Add a new spec to the back of the queue.

        Returns the created ``SpecQueueItem``.
        """
        item = SpecQueueItem(feature_name=feature_name, content=content)
        self._items.append(item)
        return item

    def pop(self) -> Optional[SpecQueueItem]:
        """Remove and return the oldest spec, or ``None`` if empty."""
        if not self._items:
            return None
        return self._items.pop(0)

    @property
    def size(self) -> int:
        """Number of specs currently in the queue."""
        return len(self._items)

    @property
    def is_full(self) -> bool:
        """``True`` if queue has reached ``target_size``."""
        return self.size >= self.target_size

    @property
    def slots_available(self) -> int:
        """Number of slots the PO should fill."""
        return max(0, self.target_size - self.size)

    def peek(self) -> Optional[SpecQueueItem]:
        """Return the oldest spec without removing it."""
        return self._items[0] if self._items else None

    def list_items(self) -> list[SpecQueueItem]:
        """Return a copy of all queued items."""
        return list(self._items)


class DeclineMemory:
    """Stores decline reasons so the PO can avoid repeating mistakes."""

    def __init__(self) -> None:
        self._records: list[DeclineRecord] = []

    def add(
        self,
        feature_name: str,
        reason: str,
        spec_content: str = "",
    ) -> DeclineRecord:
        """Record a declined spec and the reason."""
        record = DeclineRecord(
            feature_name=feature_name,
            reason=reason,
            spec_content=spec_content,
        )
        self._records.append(record)
        return record

    @property
    def count(self) -> int:
        """Number of decline records."""
        return len(self._records)

    @property
    def latest(self) -> Optional[DeclineRecord]:
        """Most recent decline record, or ``None``."""
        return self._records[-1] if self._records else None

    def get_history(self) -> list[DeclineRecord]:
        """Return all decline records (oldest first)."""
        return list(self._records)

    def format_for_prompt(self) -> str:
        """Format decline history as context for LLM prompts.

        Returns a newline-separated summary of past rejections.
        """
        if not self._records:
            return "No previous rejections."
        lines = []
        for i, r in enumerate(self._records, 1):
            lines.append(f"{i}. Feature '{r.feature_name}' was rejected: {r.reason}")
        return "\n".join(lines)

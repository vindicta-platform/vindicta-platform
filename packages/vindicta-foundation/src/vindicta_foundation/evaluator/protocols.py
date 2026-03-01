"""Protocols and result types for dice-evaluator dependency injection.

The ``DiceRoller`` protocol decouples the evaluator from the concrete
``dice-core`` implementation, enabling deterministic mock testing (R2).
"""

from __future__ import annotations

from typing import NamedTuple, Protocol

from vindicta_foundation.models.entropy import EntropyProof


class RollResult(NamedTuple):
    """Result of a single dice roll operation."""

    values: list[int]
    proof: EntropyProof


class DiceRoller(Protocol):
    """Protocol for dice rolling — implemented by dice-core.

    The evaluator depends on this protocol, never on the concrete
    dice-core implementation directly (R2).
    """

    def roll(self, sides: int, count: int = 1) -> RollResult: ...

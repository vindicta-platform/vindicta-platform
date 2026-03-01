"""Dice engine implementations and factory function.

Provides ``CsprngEngine`` for production use (``secrets.randbelow``)
and ``DeterministicEngine`` for reproducible CI testing. The
``create_engine`` factory selects the correct implementation based
on ``RngMode``.
"""

from __future__ import annotations

import hashlib
import hmac
import random
import secrets

from vindicta_foundation.dice.errors import SecurityError
from vindicta_foundation.dice.types import (
    RandomResult,
    RngMode,
    RollEntropy,
)


class CsprngEngine:
    """CSPRNG-backed dice engine using ``secrets.randbelow()``.

    Every roll generates a fresh 32-byte seed and produces an
    HMAC-SHA256 commitment for external verification.

    Constitutional Compliance:
        - AX-03: Uses ``secrets.randbelow(N)`` for uniform distribution.
        - FR-001: Cryptographically secure random generation.
        - FR-003: No predictable sources.
    """

    def roll(
        self,
        lower: int,
        upper: int,
        count: int = 1,
        context: str = "",
    ) -> RandomResult:
        """Generate cryptographically secure random integers.

        Args:
            lower: Minimum value (inclusive), must be >= 1.
            upper: Maximum value (inclusive), must be > lower.
            count: Number of values to generate, must be >= 1.
            context: Contextual binding string for the HMAC.

        Returns:
            A ``RandomResult`` containing the values and entropy proof.

        Raises:
            ValueError: If parameters are out of valid range.
        """
        self._validate_params(lower, upper, count)

        seed = secrets.token_bytes(32)
        commitment = hmac.new(seed, context.encode(), hashlib.sha256).hexdigest()

        range_size = upper - lower + 1
        values = [secrets.randbelow(range_size) + lower for _ in range(count)]

        entropy = RollEntropy(
            seed=seed,
            commitment=commitment,
            algorithm="hmac-sha256",
            context=context,
        )

        return RandomResult(
            values=values,
            lower_bound=lower,
            upper_bound=upper,
            entropy=entropy,
        )

    @staticmethod
    def _validate_params(lower: int, upper: int, count: int) -> None:
        """Validate roll parameters."""
        if lower < 1:
            raise ValueError(f"lower must be >= 1, got {lower}")
        if upper <= lower:
            raise ValueError(f"upper ({upper}) must be > lower ({lower})")
        if count < 1:
            raise ValueError(f"count must be >= 1, got {count}")


class DeterministicEngine:
    """Deterministic dice engine for reproducible CI testing.

    Uses ``random.Random(seed)`` to produce repeatable sequences.
    **Must never be used in production** — gated by ``RngMode.TESTING``.
    """

    def __init__(self, seed: int) -> None:
        """Initialize with a deterministic seed.

        Args:
            seed: Integer seed for reproducible output.
        """
        self._rng = random.Random(seed)  # noqa: S311
        self._seed_int = seed

    def roll(
        self,
        lower: int,
        upper: int,
        count: int = 1,
        context: str = "",
    ) -> RandomResult:
        """Generate deterministic random integers.

        Args:
            lower: Minimum value (inclusive), must be >= 1.
            upper: Maximum value (inclusive), must be > lower.
            count: Number of values to generate, must be >= 1.
            context: Contextual binding string for the HMAC.

        Returns:
            A ``RandomResult`` containing the values and entropy proof.

        Raises:
            ValueError: If parameters are out of valid range.
        """
        CsprngEngine._validate_params(lower, upper, count)

        # Generate a deterministic 32-byte seed from the RNG state
        seed_bytes = bytes(self._rng.getrandbits(8) for _ in range(32))
        commitment = hmac.new(seed_bytes, context.encode(), hashlib.sha256).hexdigest()

        values = [self._rng.randint(lower, upper) for _ in range(count)]

        entropy = RollEntropy(
            seed=seed_bytes,
            commitment=commitment,
            algorithm="hmac-sha256",
            context=context,
        )

        return RandomResult(
            values=values,
            lower_bound=lower,
            upper_bound=upper,
            entropy=entropy,
        )


def create_engine(
    mode: RngMode = RngMode.PRODUCTION,
    seed: int | None = None,
) -> CsprngEngine | DeterministicEngine:
    """Factory function to create a dice engine instance.

    Args:
        mode: Runtime mode selector (PRODUCTION or TESTING).
        seed: Deterministic seed, only valid in TESTING mode.

    Returns:
        A ``CsprngEngine`` for production or ``DeterministicEngine``
        for testing.

    Raises:
        SecurityError: If ``seed`` is provided with
            ``mode=RngMode.PRODUCTION``.
    """
    if mode == RngMode.PRODUCTION and seed is not None:
        raise SecurityError(
            "Deterministic seeding is not allowed in PRODUCTION mode. "
            "Use RngMode.TESTING for reproducible test runs."
        )

    if mode == RngMode.TESTING:
        return DeterministicEngine(seed=seed if seed is not None else 0)

    return CsprngEngine()

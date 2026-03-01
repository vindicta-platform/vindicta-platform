"""Core types for the dice-core module.

Contains the ``RngMode`` enum, ``RollEntropy`` model, and
``RandomResult`` model as specified in the data-model.md.
"""

from __future__ import annotations

import hashlib
import hmac
from enum import Enum

from pydantic import Field, field_validator

from vindicta_foundation.models.base import VindictaModel


class RngMode(str, Enum):
    """Runtime mode selector for the dice engine.

    Attributes:
        PRODUCTION: Uses ``secrets`` module CSPRNG.
            Deterministic seeding raises ``SecurityError``.
        TESTING: Allows deterministic seeding via
            ``random.Random(seed)`` for reproducible CI.
    """

    PRODUCTION = "production"
    TESTING = "testing"


class RollEntropy(VindictaModel):
    """Encapsulates seed material and HMAC commitment for a roll.

    Contains the raw 32-byte CSPRNG seed, the HMAC-SHA256 commitment,
    and verification/reveal methods for external auditing.

    Constitutional Compliance:
        - FR-002: Cryptographic proof via HMAC-SHA256 commitment.
        - AX-03: Seed is generated from a true CSPRNG source.
    """

    seed: bytes = Field(..., description="Raw 32-byte CSPRNG seed")
    commitment: str = Field(..., description="HMAC-SHA256 hex digest of seed + context")
    algorithm: str = Field(
        default="hmac-sha256",
        description="Algorithm used for the commitment",
    )
    context: str = Field(
        default="",
        description="Contextual binding string (e.g. game ID, turn number)",
    )

    @field_validator("seed")
    @classmethod
    def validate_seed_length(cls, v: bytes) -> bytes:
        """Validate that the seed is exactly 32 bytes."""
        if len(v) != 32:
            raise ValueError(f"Seed must be exactly 32 bytes, got {len(v)}")
        return v

    @field_validator("commitment")
    @classmethod
    def validate_commitment_hex(cls, v: str) -> str:
        """Validate that the commitment is a valid 64-char hex string."""
        if len(v) != 64:
            raise ValueError(
                f"Commitment must be a 64-character hex string, got length {len(v)}"
            )
        try:
            bytes.fromhex(v)
        except ValueError as exc:
            raise ValueError("Commitment must be a valid hex string") from exc
        return v

    @field_validator("algorithm")
    @classmethod
    def validate_algorithm(cls, v: str) -> str:
        """Validate the algorithm is a supported commitment scheme."""
        allowed = {"hmac-sha256"}
        if v not in allowed:
            raise ValueError(f"Algorithm must be one of {allowed}, got '{v}'")
        return v

    def verify(self, revealed_seed: bytes | None = None) -> bool:
        """Verify the commitment against the seed.

        Args:
            revealed_seed: Optional external seed to verify against.
                If ``None``, uses ``self.seed``.

        Returns:
            ``True`` if the recomputed HMAC matches the commitment.
        """
        seed = revealed_seed if revealed_seed is not None else self.seed
        expected = hmac.new(seed, self.context.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, self.commitment)

    def reveal(self) -> str:
        """Return the hex-encoded seed for external auditing.

        Returns:
            Hex string of the raw seed bytes.
        """
        return self.seed.hex()


class RandomResult(VindictaModel):
    """Contains generated random integers with cryptographic proof.

    Holds the dice roll values, the valid range, and the
    ``RollEntropy`` proof binding for external verification.

    Constitutional Compliance:
        - AX-03: Values are uniformly distributed in [lower_bound, upper_bound].
        - FR-002: Every result includes an entropy proof.
    """

    values: list[int] = Field(..., description="The generated random integers")
    lower_bound: int = Field(
        ..., description="Minimum value (inclusive) of the roll range"
    )
    upper_bound: int = Field(
        ..., description="Maximum value (inclusive) of the roll range"
    )
    entropy: RollEntropy = Field(
        ..., description="Cryptographic proof binding for this result"
    )

    @field_validator("values")
    @classmethod
    def validate_values_not_empty(cls, v: list[int]) -> list[int]:
        """Validate that at least one value was generated."""
        if not v:
            raise ValueError("Values list must not be empty")
        return v

    @field_validator("lower_bound")
    @classmethod
    def validate_lower_bound(cls, v: int) -> int:
        """Validate that lower_bound >= 1 (dice faces are positive)."""
        if v < 1:
            raise ValueError(f"lower_bound must be >= 1, got {v}")
        return v

    @field_validator("upper_bound")
    @classmethod
    def validate_upper_bound(cls, v: int, info: object) -> int:
        """Validate that upper_bound > lower_bound."""
        # Access the already-validated lower_bound from info.data
        data = getattr(info, "data", {})
        lower = data.get("lower_bound")
        if lower is not None and v <= lower:
            raise ValueError(f"upper_bound ({v}) must be > lower_bound ({lower})")
        return v

    @field_validator("values")
    @classmethod
    def validate_values_in_range(cls, v: list[int], info: object) -> list[int]:
        """Validate that all values are within [lower_bound, upper_bound]."""
        data = getattr(info, "data", {})
        lower = data.get("lower_bound")
        upper = data.get("upper_bound")
        if lower is not None and upper is not None:
            for val in v:
                if val < lower or val > upper:
                    raise ValueError(f"Value {val} out of range [{lower}, {upper}]")
        return v

    def verify(self) -> bool:
        """Verify the cryptographic proof binding.

        Delegates to ``self.entropy.verify()`` for proof validation.

        Returns:
            ``True`` if the entropy proof is valid.
        """
        return self.entropy.verify()

"""Dice Core — CSPRNG with Verifiable Entropy Proofs.

Provides cryptographically secure random dice rolls with HMAC-SHA256
verifiable entropy proofs. Uses Python's ``secrets`` module for
production randomness and supports deterministic seeding for CI/testing.

Constitutional Compliance:
    - AX-03: Equal probability 1/N via ``secrets.randbelow(N)``.
    - FR-001: CSPRNG-backed generation.
    - FR-002: Every roll includes a cryptographic proof.
    - FR-003: No predictable sources in production mode.
    - FR-005: Pure Python, no external services.
"""

from vindicta_foundation.dice.engine import create_engine
from vindicta_foundation.dice.errors import SecurityError
from vindicta_foundation.dice.types import RandomResult, RngMode, RollEntropy

__all__ = [
    "create_engine",
    "RandomResult",
    "RngMode",
    "RollEntropy",
    "SecurityError",
]

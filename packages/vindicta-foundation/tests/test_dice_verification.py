"""Tests for entropy verification — US2: Verifiable Entropy Proofs.

Covers commit-reveal-verify cycle, tamper detection, and
independent HMAC recomputation by an external auditor.
"""

from __future__ import annotations

import hashlib
import hmac

from vindicta_foundation.dice.engine import CsprngEngine, create_engine
from vindicta_foundation.dice.types import RngMode


class TestVerifyUntampered:
    """Verify that untampered results pass verification."""

    def test_verify_returns_true(self) -> None:
        engine = CsprngEngine()
        result = engine.roll(1, 6)
        assert result.verify() is True

    def test_verify_on_multiple_rolls(self) -> None:
        engine = CsprngEngine()
        for _ in range(20):
            result = engine.roll(1, 20, count=3)
            assert result.verify() is True

    def test_verify_with_context(self) -> None:
        engine = CsprngEngine()
        result = engine.roll(1, 6, context="game-42:round-3")
        assert result.verify() is True


class TestVerifyTampered:
    """Verify that tampered results fail verification."""

    def test_altered_commitment_fails(self) -> None:
        engine = CsprngEngine()
        result = engine.roll(1, 6)

        # Tamper with the commitment
        original = result.entropy.commitment
        tampered = "0" * 64
        if tampered == original:
            tampered = "f" * 64

        # Create a new RollEntropy with tampered commitment
        # (model is not frozen by default in VindictaModel)
        result.entropy.commitment = tampered
        assert result.verify() is False

    def test_altered_seed_fails(self) -> None:
        engine = CsprngEngine()
        result = engine.roll(1, 6)

        # Replace seed with different bytes
        result.entropy.seed = b"\x00" * 32
        assert result.verify() is False


class TestRevealAndAudit:
    """Full commit-reveal-verify cycle for external auditor (T015)."""

    def test_reveal_returns_hex_seed(self) -> None:
        engine = CsprngEngine()
        result = engine.roll(1, 6)
        seed_hex = result.entropy.reveal()
        assert isinstance(seed_hex, str)
        assert len(seed_hex) == 64  # 32 bytes = 64 hex chars

    def test_independent_hmac_recomputation(self) -> None:
        """Full auditor flow: extract seed, recompute HMAC, verify."""
        engine = CsprngEngine()
        result = engine.roll(1, 6, context="audit-test")

        # Step 1: Extract proof components
        seed_hex = result.entropy.reveal()
        commitment = result.entropy.commitment
        context = result.entropy.context

        # Step 2: Independently recompute HMAC
        seed_bytes = bytes.fromhex(seed_hex)
        expected = hmac.new(seed_bytes, context.encode(), hashlib.sha256).hexdigest()

        # Step 3: Verify match
        assert expected == commitment, (
            f"Independent HMAC recomputation failed: "
            f"expected={expected}, commitment={commitment}"
        )

    def test_deterministic_engine_also_verifiable(self) -> None:
        """Verify that even the testing engine produces valid proofs."""
        engine = create_engine(mode=RngMode.TESTING, seed=42)
        result = engine.roll(1, 6, context="test-context")
        assert result.verify() is True

        # Also verify via independent recomputation
        seed_hex = result.entropy.reveal()
        seed_bytes = bytes.fromhex(seed_hex)
        expected = hmac.new(
            seed_bytes, "test-context".encode(), hashlib.sha256
        ).hexdigest()
        assert expected == result.entropy.commitment

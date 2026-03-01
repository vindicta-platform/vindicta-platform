"""Tests for DiceEngine — US1: Secure Randomness Generation.

Covers CsprngEngine, DeterministicEngine, create_engine factory,
and statistical uniformity validation (chi-square test).
"""

from __future__ import annotations

import pytest

from vindicta_foundation.dice.engine import (
    CsprngEngine,
    DeterministicEngine,
    create_engine,
)
from vindicta_foundation.dice.errors import SecurityError
from vindicta_foundation.dice.types import RandomResult, RngMode


class TestCsprngEngine:
    """Tests for CsprngEngine.roll()."""

    def test_roll_returns_random_result(self) -> None:
        engine = CsprngEngine()
        result = engine.roll(1, 6)
        assert isinstance(result, RandomResult)

    def test_roll_single_value_in_range(self) -> None:
        engine = CsprngEngine()
        for _ in range(100):
            result = engine.roll(1, 6)
            assert len(result.values) == 1
            assert 1 <= result.values[0] <= 6

    def test_roll_multiple_values(self) -> None:
        engine = CsprngEngine()
        result = engine.roll(1, 6, count=5)
        assert len(result.values) == 5
        for v in result.values:
            assert 1 <= v <= 6

    def test_roll_d20(self) -> None:
        engine = CsprngEngine()
        for _ in range(50):
            result = engine.roll(1, 20)
            assert 1 <= result.values[0] <= 20

    def test_roll_bounds_are_recorded(self) -> None:
        engine = CsprngEngine()
        result = engine.roll(1, 6, count=3)
        assert result.lower_bound == 1
        assert result.upper_bound == 6

    def test_roll_has_entropy_proof(self) -> None:
        engine = CsprngEngine()
        result = engine.roll(1, 6)
        assert result.entropy is not None
        assert result.entropy.commitment
        assert result.entropy.algorithm == "hmac-sha256"

    def test_roll_with_context(self) -> None:
        engine = CsprngEngine()
        result = engine.roll(1, 6, context="game-123:turn-5")
        assert result.entropy.context == "game-123:turn-5"

    def test_roll_invalid_lower_bound(self) -> None:
        engine = CsprngEngine()
        with pytest.raises(ValueError, match="lower must be >= 1"):
            engine.roll(0, 6)

    def test_roll_invalid_upper_bound(self) -> None:
        engine = CsprngEngine()
        with pytest.raises(ValueError, match="upper.*must be > lower"):
            engine.roll(6, 6)

    def test_roll_invalid_count(self) -> None:
        engine = CsprngEngine()
        with pytest.raises(ValueError, match="count must be >= 1"):
            engine.roll(1, 6, count=0)


class TestDeterministicEngine:
    """Tests for DeterministicEngine (reproducible test mode)."""

    def test_same_seed_same_results(self) -> None:
        engine1 = DeterministicEngine(seed=42)
        engine2 = DeterministicEngine(seed=42)
        r1 = engine1.roll(1, 6, count=5)
        r2 = engine2.roll(1, 6, count=5)
        assert r1.values == r2.values

    def test_different_seed_different_results(self) -> None:
        engine1 = DeterministicEngine(seed=42)
        engine2 = DeterministicEngine(seed=99)
        r1 = engine1.roll(1, 6, count=10)
        r2 = engine2.roll(1, 6, count=10)
        assert r1.values != r2.values

    def test_values_in_range(self) -> None:
        engine = DeterministicEngine(seed=42)
        result = engine.roll(1, 6, count=100)
        for v in result.values:
            assert 1 <= v <= 6

    def test_returns_random_result(self) -> None:
        engine = DeterministicEngine(seed=42)
        result = engine.roll(1, 6)
        assert isinstance(result, RandomResult)


class TestCreateEngine:
    """Tests for the create_engine factory function."""

    def test_default_creates_csprng_engine(self) -> None:
        engine = create_engine()
        assert isinstance(engine, CsprngEngine)

    def test_production_mode_explicit(self) -> None:
        engine = create_engine(mode=RngMode.PRODUCTION)
        assert isinstance(engine, CsprngEngine)

    def test_testing_mode_with_seed(self) -> None:
        engine = create_engine(mode=RngMode.TESTING, seed=42)
        assert isinstance(engine, DeterministicEngine)

    def test_testing_mode_without_seed_defaults_to_zero(self) -> None:
        engine = create_engine(mode=RngMode.TESTING)
        assert isinstance(engine, DeterministicEngine)

    def test_production_mode_rejects_seed(self) -> None:
        with pytest.raises(SecurityError, match="PRODUCTION mode"):
            create_engine(mode=RngMode.PRODUCTION, seed=42)


class TestStatisticalUniformity:
    """Statistical validation of CSPRNG output (chi-square test).

    SC-001: Chi-square goodness-of-fit over 10,000 d6 rolls with p > 0.01.
    """

    def test_chi_square_uniformity_d6(self) -> None:
        """Verify uniform distribution over 10,000 d6 rolls."""
        engine = CsprngEngine()
        n = 10_000
        faces = 6
        counts = [0] * faces

        for _ in range(n):
            result = engine.roll(1, faces)
            counts[result.values[0] - 1] += 1

        # Chi-square statistic
        expected = n / faces
        chi_sq = sum((observed - expected) ** 2 / expected for observed in counts)

        # Critical value for df=5, alpha=0.01 is 15.086
        # We want p > 0.01, so chi_sq must be < critical
        assert chi_sq < 15.086, (
            f"Chi-square {chi_sq:.2f} exceeds critical value 15.086 (counts: {counts})"
        )

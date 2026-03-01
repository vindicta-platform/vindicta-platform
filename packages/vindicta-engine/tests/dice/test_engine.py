"""Unit tests for Dice-Engine."""

from dice_engine import DiceEngine, DiceRoll


class TestDiceRoll:
    """Tests for DiceRoll model."""

    def test_dice_roll_creation(self):
        """DiceRoll should be creatable."""
        roll = DiceRoll(value=4, sides=6, entropy_proof="abc123")

        assert roll.value == 4
        assert roll.sides == 6

    def test_dice_roll_str(self):
        """str() should show die type and value."""
        roll = DiceRoll(value=3, sides=6, entropy_proof="x")

        assert "D6" in str(roll)
        assert "3" in str(roll)


class TestDiceEngine:
    """Tests for DiceEngine."""

    def test_roll_d6_range(self):
        """D6 should produce values 1-6."""
        engine = DiceEngine()

        for _ in range(100):
            roll = engine.roll_d6()
            assert 1 <= roll.value <= 6

    def test_roll_d3_range(self):
        """D3 should produce values 1-3."""
        engine = DiceEngine()

        for _ in range(100):
            roll = engine.roll_d3()
            assert 1 <= roll.value <= 3

    def test_roll_has_entropy_proof(self):
        """Rolls should include entropy proof."""
        engine = DiceEngine()
        roll = engine.roll_d6()

        assert roll.entropy_proof
        assert len(roll.entropy_proof) == 16

    def test_deterministic_with_seed(self):
        """Same seed should produce same rolls."""
        seed = b"test_seed_12345"

        engine1 = DiceEngine(seed=seed)
        engine2 = DiceEngine(seed=seed)

        rolls1 = [engine1.roll_d6().value for _ in range(10)]
        rolls2 = [engine2.roll_d6().value for _ in range(10)]

        assert rolls1 == rolls2

    def test_roll_batch(self):
        """Batch rolling should work."""
        engine = DiceEngine()

        result = engine.roll_batch(10, sides=6)

        assert len(result.rolls) == 10
        assert result.total == sum(r.value for r in result.rolls)

    def test_roll_2d6(self):
        """2D6 should return two rolls."""
        engine = DiceEngine()

        r1, r2 = engine.roll_2d6()

        assert 1 <= r1.value <= 6
        assert 1 <= r2.value <= 6


class TestCombatRoll:
    """Tests for combat roll sequences."""

    def test_combat_roll_basic(self):
        """Combat roll should process hits, wounds, saves."""
        engine = DiceEngine(seed=b"combat_test")

        result = engine.combat_roll(attacks=10, hit_on=3, wound_on=4, save=5, damage=1)

        assert result.attacks == 10
        assert 0 <= result.hits <= 10
        assert 0 <= result.wounds <= result.hits
        assert 0 <= result.saves_failed <= result.wounds

    def test_combat_result_damage(self):
        """Damage should equal saves_failed * damage."""
        engine = DiceEngine(seed=b"damage_test")

        result = engine.combat_roll(
            attacks=10,
            hit_on=2,  # Very likely to hit
            wound_on=2,  # Very likely to wound
            save=6,  # Poor save
            damage=3,
        )

        assert result.damage_dealt == result.saves_failed * 3

    def test_combat_result_str(self):
        """CombatResult str should show sequence."""
        engine = DiceEngine(seed=b"str_test")

        result = engine.combat_roll(attacks=5, hit_on=3, wound_on=4, save=5, damage=1)

        s = str(result)
        assert "5A" in s  # 5 attacks


class TestEntropyProofs:
    """Tests for entropy proof system."""

    def test_unique_proofs(self):
        """Each roll should have unique proof."""
        engine = DiceEngine()

        proofs = set()
        for _ in range(100):
            roll = engine.roll_d6()
            proofs.add(roll.entropy_proof)

        # All proofs should be unique
        assert len(proofs) == 100

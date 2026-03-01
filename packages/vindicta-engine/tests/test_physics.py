from vindicta_engine.physics.engine import DiceEngine
from vindicta_engine.physics.models import DiceRoll, CombatResult


def test_dice_roll_defaults() -> None:
    engine = DiceEngine()
    roll = engine.roll_d6()

    assert isinstance(roll, DiceRoll)
    assert 1 <= roll.value <= 6
    assert roll.sides == 6
    assert roll.id is not None  # Inherited from VindictaModel
    assert roll.created_at is not None  # Inherited from VindictaModel


def test_deterministic_seed() -> None:
    seed = b"test_seed_123"
    engine1 = DiceEngine(seed)
    engine2 = DiceEngine(seed)

    roll1 = engine1.roll_d6()
    roll2 = engine2.roll_d6()

    assert roll1.value == roll2.value
    assert roll1.entropy_proof == roll2.entropy_proof


def test_combat_roll_logic() -> None:
    # Deterministic engine to ensure hits
    # We can't easily force specific values without mocking internals,
    # but we can check constraints.
    engine = DiceEngine()

    result = engine.combat_roll(
        attacks=10,
        hit_on=2,
        wound_on=2,
        save=6,  # Hard save
        damage=1,
    )

    assert isinstance(result, CombatResult)
    assert result.attacks == 10
    assert (
        len(result.hit_rolls) >= 10
    )  # Could be more if rerolls implemented logic was slightly different, here it's appended
    assert result.hits <= 10 + len(result.hit_rolls) - 10  # Rerolls add to list
    assert result.damage_dealt >= 0


def test_batch_roll() -> None:
    engine = DiceEngine()
    batch = engine.roll_batch(count=10, sides=6)

    assert len(batch.rolls) == 10
    assert batch.total == sum(r.value for r in batch.rolls)

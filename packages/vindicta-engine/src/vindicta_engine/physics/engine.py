import hashlib
import secrets
from typing import Optional, List
from vindicta_engine.physics.models import DiceRoll, CombatResult, BatchRollResult


class DiceEngine:
    """Cryptographically secure dice rolling engine.

    All rolls are CSPRNG-backed and include entropy proofs
    for verification and audit purposes.
    """

    def __init__(self, seed: Optional[bytes] = None) -> None:
        """Initialize the dice engine.

        Args:
            seed: Optional seed for testing (uses CSPRNG by default).
        """
        self._seed = seed
        self._roll_count = 0

    def _generate_entropy(self) -> bytes:
        """Generate cryptographically secure entropy."""
        if self._seed:
            # Deterministic for testing
            # We use a simple counter to ensure subsequent rolls differ
            combined = self._seed + self._roll_count.to_bytes(8, "big")
            self._roll_count += 1
            return hashlib.sha256(combined).digest()
        else:
            return secrets.token_bytes(32)

    def _create_proof(self, entropy: bytes) -> str:
        """Create entropy proof hash."""
        return hashlib.sha256(entropy).hexdigest()[:16]

    def roll(self, sides: int = 6) -> DiceRoll:
        """Roll a die with the specified number of sides.

        Args:
            sides: Number of sides (e.g., 6 for D6).

        Returns:
            DiceRoll with value and entropy proof.
        """
        entropy = self._generate_entropy()
        # Modulo bias is negligible for 32 bytes of entropy vs small N
        value = (int.from_bytes(entropy[:4], "big") % sides) + 1
        proof = self._create_proof(entropy)

        return DiceRoll(value=value, sides=sides, entropy_proof=proof)

    def roll_d6(self) -> DiceRoll:
        """Roll a D6."""
        return self.roll(6)

    def roll_d3(self) -> DiceRoll:
        """Roll a D3 (1-3)."""
        return self.roll(3)

    def roll_2d6(self) -> List[DiceRoll]:
        """Roll 2D6."""
        return [self.roll_d6(), self.roll_d6()]

    def roll_batch(self, count: int, sides: int = 6) -> BatchRollResult:
        """Roll multiple dice.

        Args:
            count: Number of dice to roll.
            sides: Number of sides per die.

        Returns:
            BatchRollResult with all rolls and statistics.
        """
        rolls = [self.roll(sides) for _ in range(count)]
        total = sum(r.value for r in rolls)
        average = total / count if count > 0 else 0.0

        return BatchRollResult(rolls=rolls, total=total, average=average)

    def combat_roll(
        self,
        attacks: int,
        hit_on: int,
        wound_on: int,
        save: int,
        damage: int,
        hit_reroll: bool = False,
        wound_reroll: bool = False,
    ) -> CombatResult:
        """Perform a complete combat roll sequence.

        Args:
            attacks: Number of attacks.
            hit_on: Target number to hit (e.g., 3 means 3+).
            wound_on: Target number to wound.
            save: Target save (e.g., 5 means 5+).
            damage: Damage per failed save.
            hit_reroll: Reroll failed hits.
            wound_reroll: Reroll failed wounds.

        Returns:
            CombatResult with all rolls and damage dealt.
        """
        result = CombatResult(
            attacks=attacks, hit_on=hit_on, wound_on=wound_on, save=save, damage=damage
        )

        # Hit rolls
        for _ in range(attacks):
            roll = self.roll_d6()
            result.hit_rolls.append(roll)
            if roll.value >= hit_on:
                result.hits += 1
            elif hit_reroll:
                reroll = self.roll_d6()
                result.hit_rolls.append(reroll)
                # Note: This logic assumes reroll replaces the miss but we keep both in log
                if reroll.value >= hit_on:
                    result.hits += 1

        # Wound rolls
        for _ in range(result.hits):
            roll = self.roll_d6()
            result.wound_rolls.append(roll)
            if roll.value >= wound_on:
                result.wounds += 1
            elif wound_reroll:
                reroll = self.roll_d6()
                result.wound_rolls.append(reroll)
                if reroll.value >= wound_on:
                    result.wounds += 1

        # Save rolls
        for _ in range(result.wounds):
            roll = self.roll_d6()
            result.save_rolls.append(roll)
            if roll.value < save:
                result.saves_failed += 1

        # Damage
        result.damage_dealt = result.saves_failed * damage

        return result

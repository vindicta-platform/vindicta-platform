"""Data models for Dice-Engine."""

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class DiceRoll:
    """A single dice roll with entropy proof."""

    value: int
    sides: int
    entropy_proof: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    roll_id: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return f"D{self.sides}: {self.value}"

    def verify(self, entropy_bytes: bytes) -> bool:
        """Verify this roll was generated from given entropy."""
        expected_proof = hashlib.sha256(entropy_bytes).hexdigest()[:16]
        return self.entropy_proof == expected_proof


@dataclass
class CombatResult:
    """Result of a combat roll sequence."""

    # Input parameters
    attacks: int
    hit_on: int
    wound_on: int
    save: int
    damage: int

    # Roll results
    hit_rolls: list[DiceRoll] = field(default_factory=list)
    wound_rolls: list[DiceRoll] = field(default_factory=list)
    save_rolls: list[DiceRoll] = field(default_factory=list)

    # Computed results
    hits: int = 0
    wounds: int = 0
    saves_failed: int = 0
    damage_dealt: int = 0

    def __str__(self) -> str:
        return f"{self.attacks}A → {self.hits}H → {self.wounds}W → {self.damage_dealt}D"


@dataclass
class BatchRollResult:
    """Result of a batch dice roll."""

    rolls: list[DiceRoll]
    total: int
    average: float

    @property
    def values(self) -> list[int]:
        return [r.value for r in self.rolls]

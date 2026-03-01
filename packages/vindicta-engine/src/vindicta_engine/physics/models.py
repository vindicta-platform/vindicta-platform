from typing import List
from pydantic import Field
from vindicta_foundation.models.base import VindictaModel


class DiceRoll(VindictaModel):
    """A single dice roll with entropy proof.

    Inherits from VindictaModel for standard ID/Timestamp/Serialization.
    """

    value: int = Field(..., description="The result of the roll (e.g., 1-6)")
    sides: int = Field(..., description="Number of sides on the die")
    entropy_proof: str = Field(
        ..., description="SHA-256 hash fragment of the entropy used"
    )

    def __str__(self) -> str:
        return f"D{self.sides}: {self.value}"


class BatchRollResult(VindictaModel):
    """Result of a batch dice roll."""

    rolls: List[DiceRoll] = Field(..., description="List of individual dice rolls")
    total: int = Field(..., description="Sum of all roll values")
    average: float = Field(..., description="Average value of the rolls")

    @property
    def values(self) -> List[int]:
        return [r.value for r in self.rolls]


class CombatResult(VindictaModel):
    """Result of a combat roll sequence."""

    # Input parameters
    attacks: int = Field(..., description="Number of attacks")
    hit_on: int = Field(..., description="Target number to hit")
    wound_on: int = Field(..., description="Target number to wound")
    save: int = Field(..., description="Target save")
    damage: int = Field(..., description="Damage description or value")

    # Computed results
    hits: int = Field(0, description="Total successful hits")
    wounds: int = Field(0, description="Total successful wounds")
    saves_failed: int = Field(0, description="Total failed saves")
    damage_dealt: int = Field(0, description="Total damage dealt")

    # Detailed rolls
    hit_rolls: List[DiceRoll] = Field(
        default_factory=list, description="Individual hit rolls"
    )
    wound_rolls: List[DiceRoll] = Field(
        default_factory=list, description="Individual wound rolls"
    )
    save_rolls: List[DiceRoll] = Field(
        default_factory=list, description="Individual save rolls"
    )

    def __str__(self) -> str:
        return (
            f"{self.attacks}A -> {self.hits}H -> {self.wounds}W -> {self.damage_dealt}D"
        )

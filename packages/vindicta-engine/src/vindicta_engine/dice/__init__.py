"""Dice-Engine: Cryptographically secure dice rolling.

Provides CSPRNG-backed dice rolling with entropy proofs
for fair gameplay in the Vindicta Platform.
"""

from dice_engine.engine import DiceEngine
from dice_engine.models import DiceRoll, CombatResult

__version__ = "1.0.0"

__all__ = [
    "DiceEngine",
    "DiceRoll",
    "CombatResult",
]

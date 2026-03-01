"""
Economy models for the Vindicta Platform.

Ported from Economy-Engine. All entity models inherit VindictaModel.
Sub-component value objects (Currency, enums) use BaseModel.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from vindicta_foundation.models.base import VindictaModel
from vindicta_foundation.models.economy import GasTankState  # Re-export


class CurrencyType(str, Enum):
    """Types of virtual currency."""

    VINDICTA_CREDITS = "vindicta_credits"
    PREMIUM = "premium"


class TransactionType(str, Enum):
    """Types of transactions."""

    EARN = "earn"
    SPEND = "spend"
    TRANSFER = "transfer"
    REFUND = "refund"


class Currency(BaseModel):
    """Virtual currency definition (value object, no ID needed)."""

    type: CurrencyType
    name: str
    symbol: str = "VC"
    decimals: int = 0


class Transaction(VindictaModel):
    """A currency transaction with full audit trail."""

    user_id: str
    currency: CurrencyType = CurrencyType.VINDICTA_CREDITS
    transaction_type: TransactionType
    amount: int
    reason: str = ""
    metadata: dict = Field(default_factory=dict)


class Balance(VindictaModel):
    """A user's currency balance."""

    user_id: str
    currency: CurrencyType = CurrencyType.VINDICTA_CREDITS
    amount: int = 0


class AchievementType(str, Enum):
    """Types of achievements."""

    GAMES_PLAYED = "games_played"
    WINS = "wins"
    STREAK = "streak"
    COLLECTION = "collection"


class Achievement(VindictaModel):
    """An unlockable achievement."""

    name: str
    description: str
    achievement_type: AchievementType
    threshold: int
    reward_amount: int = 0
    badge_icon: Optional[str] = None
    user_progress: int = 0
    unlocked: bool = False
    unlocked_at: Optional[datetime] = None


__all__ = [
    "GasTankState",
    "CurrencyType",
    "TransactionType",
    "Currency",
    "Transaction",
    "Balance",
    "AchievementType",
    "Achievement",
]

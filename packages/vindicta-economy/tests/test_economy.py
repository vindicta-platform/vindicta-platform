"""Unit tests for vindicta-economy models."""

from uuid import UUID
from vindicta_economy.models import (
    GasTankState,
    Transaction,
    TransactionType,
    Balance,
    Achievement,
    AchievementType,
)
from vindicta_foundation.models.base import VindictaModel


def test_gas_tank_state_from_foundation():
    """GasTankState is re-exported from foundation."""
    tank = GasTankState(balance_usd=5.0, limit_usd=10.0)
    assert isinstance(tank, VindictaModel)
    assert tank.balance_usd == 5.0
    assert not tank.is_empty


def test_transaction_model():
    tx = Transaction(
        user_id="user_123",
        transaction_type=TransactionType.EARN,
        amount=100,
        reason="Game completion bonus",
    )
    assert isinstance(tx, VindictaModel)
    assert isinstance(tx.id, UUID)
    assert tx.amount == 100


def test_balance_model():
    balance = Balance(user_id="user_123", amount=500)
    assert isinstance(balance, VindictaModel)
    assert balance.amount == 500


def test_achievement_model():
    achievement = Achievement(
        name="First Blood",
        description="Win your first game",
        achievement_type=AchievementType.WINS,
        threshold=1,
        reward_amount=50,
    )
    assert isinstance(achievement, VindictaModel)
    assert not achievement.unlocked

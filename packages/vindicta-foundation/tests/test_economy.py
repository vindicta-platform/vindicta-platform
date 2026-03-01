import pytest
from vindicta_foundation.models.economy import GasTankState


def test_gas_tank_state_logic() -> None:
    """Test empty, full, and low tank logic."""
    # Empty tank
    empty = GasTankState(balance_usd=0.0, limit_usd=10.0, is_active=True)
    assert empty.is_empty is True
    assert empty.is_low is True

    # Full tank
    full = GasTankState(balance_usd=10.0, limit_usd=10.0, is_active=True)
    assert full.is_empty is False
    assert full.is_low is False

    # Low tank (below 10%)
    low = GasTankState(balance_usd=0.9, limit_usd=10.0, is_active=True)
    assert low.is_low is True


def test_gas_tank_defaults() -> None:
    """Test the default instantiation of GasTankState."""
    tank = GasTankState(balance_usd=0.0, limit_usd=0.0, is_active=True)
    assert tank.balance_usd == 0.0
    assert tank.limit_usd == 0.0
    assert tank.is_active is True
    assert tank.is_empty is True
    assert tank.is_low is True


def test_gas_tank_edge_cases() -> None:
    """Test edge case scenarios for gas tank construction."""
    with pytest.raises(ValueError):
        GasTankState(balance_usd=-1.0, limit_usd=10.0, is_active=True)

    with pytest.raises(ValueError):
        GasTankState(balance_usd=1.0, limit_usd=-5.0, is_active=True)

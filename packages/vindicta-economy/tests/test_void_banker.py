import asyncio
import os
import pytest
from vindicta_economy.ledger.manager import VoidBankerManager
from vindicta_economy.governor.quotas import OperationType, MockHardwareState
from vindicta_economy.governor.policy import (
    ResourcePolicy,
    PriorityLevel,
    ResourceExhaustionHalt,
)

DB_PATH = "test_compute_ledger.db"


DB_PATH = "test_compute_ledger.db"


async def setup_banker():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except PermissionError:
            pass

    # Initialize Manager
    manager = await VoidBankerManager.get_instance(db_path=DB_PATH)
    # Reset schema for test isolation
    manager.ledger.db_path = DB_PATH
    manager.ledger._init_db()
    return manager


async def teardown_banker():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except PermissionError:
            pass


async def _test_ledger_basics():
    banker = await setup_banker()
    try:
        agent_id = "agent_007"

        # Check initial balance
        balance = await banker.ledger.get_balance(agent_id)
        assert balance == 0.0

        # Grant credits
        await banker.grant_credits(agent_id, 100.0)
        balance = await banker.ledger.get_balance(agent_id)
        assert balance == 100.0

        # Check solvency
        assert await banker.check_solvency(agent_id, required_cc=50.0)
        assert not await banker.check_solvency(agent_id, required_cc=150.0)
    finally:
        await teardown_banker()


async def _test_purchase_operation():
    banker = await setup_banker()
    try:
        agent_id = "agent_008"
        await banker.grant_credits(agent_id, 10.0)

        # Purchase BSH (Cost 1.0)
        success = await banker.purchase_operation(
            agent_id, OperationType.BSH_GENERATION
        )
        assert success
        balance = await banker.ledger.get_balance(agent_id)
        assert balance == 9.0

        # Purchase DMF (Cost 5.0)
        success = await banker.purchase_operation(
            agent_id, OperationType.DMF_EVALUATION
        )
        assert success
        balance = await banker.ledger.get_balance(agent_id)
        assert balance == 4.0

        # Fail purchase (Cost 5.0 > Balance 4.0)
        success = await banker.purchase_operation(
            agent_id, OperationType.DMF_EVALUATION
        )
        assert not success
        balance = await banker.ledger.get_balance(agent_id)
        assert balance == 4.0
    finally:
        await teardown_banker()


async def _test_policy_enforcement():
    banker = await setup_banker()
    try:
        policy = ResourcePolicy(manager=banker)
        agent_id = "agent_policy"
        await banker.grant_credits(agent_id, 100.0)

        # Normal operation
        assert await policy.enforce_policy(
            agent_id, PriorityLevel.STANDARD_OPERATION, estimated_cost=5.0
        )

        # Trigger Thermal Guard
        overheated_state = MockHardwareState()
        # MockHardwareState attributes are cpu_temp, gpu_temp
        overheated_state.cpu_temp = 90.0  # > 85.0 limit
        banker.update_hardware_state(overheated_state)

        with pytest.raises(ResourceExhaustionHalt) as excinfo:
            await policy.enforce_policy(
                agent_id, PriorityLevel.STANDARD_OPERATION, estimated_cost=5.0
            )
        assert "THERMAL GUARD" in str(excinfo.value)

        # Trigger Load Shedding
        loaded_state = MockHardwareState()
        loaded_state.cpu_load = 95.0  # > 90.0 limit
        banker.update_hardware_state(loaded_state)

        # Low priority rejected
        with pytest.raises(ResourceExhaustionHalt) as excinfo:
            await policy.enforce_policy(
                agent_id, PriorityLevel.BACKGROUND_SIMULATION, estimated_cost=5.0
            )
        assert "LOAD SHEDDING" in str(excinfo.value)

        # High priority allowed
        assert await policy.enforce_policy(
            agent_id, PriorityLevel.LIVE_GAME_STATE, estimated_cost=5.0
        )
    finally:
        await teardown_banker()


def test_ledger_basics():
    asyncio.run(_test_ledger_basics())


def test_purchase_operation():
    asyncio.run(_test_purchase_operation())


def test_policy_enforcement():
    asyncio.run(_test_policy_enforcement())

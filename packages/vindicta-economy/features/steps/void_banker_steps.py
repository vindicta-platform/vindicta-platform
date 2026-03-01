import asyncio
import os
from behave import given, when, then
from vindicta_economy.ledger.manager import VoidBankerManager
from vindicta_economy.governor.quotas import OperationType, MockHardwareState
from vindicta_economy.governor.policy import (
    ResourcePolicy,
    PriorityLevel,
    ResourceExhaustionHalt,
)

# Testing DB Path
TEST_DB = "bdd_compute_ledger.db"


def run_async(coro):
    return asyncio.run(coro)


@given("the Void Banker is initialized with a clean ledger")
def step_init_banker(context):
    if os.path.exists(TEST_DB):
        import sqlite3

        with sqlite3.connect(TEST_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions")
            cursor.execute("DELETE FROM accounts")
            conn.commit()

    context.banker = run_async(VoidBankerManager.get_instance(db_path=TEST_DB))
    context.banker.ledger.db_path = TEST_DB
    context.banker.ledger._init_db()
    context.policy = ResourcePolicy(manager=context.banker)
    context.last_error = None
    context.starting_balances = {}


@when('when "{agent_id}" attempts a "{priority}" task')
def step_attempt_task_aliased(context, agent_id, priority):
    # This matches the 'But when' step which Behave thinks is 'Then when'
    step_attempt_task(context, agent_id, priority)


@given('an agent "{agent_id}" exists with a balance of {balance} CC')
def step_agent_exists(context, agent_id, balance):
    run_async(context.banker.grant_credits(agent_id, float(balance)))
    context.starting_balances[agent_id] = float(balance)


@given('the agent "{agent_id}" has a balance of {balance} CC')
def step_set_balance(context, agent_id, balance):
    # Use simple sync sqlite here as we are in a step
    import sqlite3

    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET balance = ? WHERE agent_id = ?",
            (float(balance), agent_id),
        )
        conn.commit()


@then('when "{agent_id}" attempts a "{priority}" task')
def step_attempt_task_aliased_then(context, agent_id, priority):
    # Behave maps 'But' to the previous step type, which was 'Then' in the feature
    step_attempt_task(context, agent_id, priority)


@given("the system temperature is {temp} degrees")
def step_set_temp(context, temp):
    hw_state = MockHardwareState()
    hw_state.cpu_temp = float(temp)
    hw_state.gpu_temp = float(temp)
    context.banker.update_hardware_state(hw_state)


@given("the system load is {load} percent")
def step_set_load(context, load):
    hw_state = MockHardwareState()
    hw_state.cpu_load = float(load)
    hw_state.gpu_load = float(load)
    context.banker.update_hardware_state(hw_state)


@when('"{agent_id}" performs a "{op_name}" operation')
def step_perform_op(context, agent_id, op_name):
    op_type = getattr(OperationType, op_name.upper())
    context.success = run_async(context.banker.purchase_operation(agent_id, op_type))


@when('"{agent_id}" performs an "alpha_beta_search" at depth {depth}')
def step_perform_search(context, agent_id, depth):
    context.success = run_async(
        context.banker.purchase_operation(
            agent_id, OperationType.ALPHA_BETA_SEARCH, depth=int(depth)
        )
    )


@when('"{agent_id}" attempts a "{op_name}" operation')
def step_attempt_op(context, agent_id, op_name):
    op_type = getattr(OperationType, op_name.upper())
    # This specifically checks for success/failure via purchase_operation
    context.success = run_async(context.banker.purchase_operation(agent_id, op_type))


@when('"{agent_id}" attempts any operation')
def step_attempt_any(context, agent_id):
    try:
        # Explicitly check policy
        run_async(
            context.policy.enforce_policy(
                agent_id, PriorityLevel.STANDARD_OPERATION, estimated_cost=1.0
            )
        )
        context.success = True
    except ResourceExhaustionHalt as e:
        context.last_error = e
        context.success = False


@when('"{agent_id}" attempts a "{priority}" task')
def step_attempt_task(context, agent_id, priority):
    try:
        p_level = getattr(PriorityLevel, priority.upper())
        run_async(context.policy.enforce_policy(agent_id, p_level, estimated_cost=1.0))
        context.success = True
    except ResourceExhaustionHalt as e:
        context.last_error = e
        context.success = False


@then("their balance should be {balance} CC")
def step_check_balance(context, balance):
    # Hardcoded "tech_priest" check or use last agent_id?
    current_balance = run_async(context.banker.ledger.get_balance("tech_priest"))
    assert current_balance == float(balance)


@then("the transaction should be logged in the ledger")
def step_check_logs(context):
    import sqlite3

    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM transactions")
        count = cursor.fetchone()[0]
        assert count > 0


@then("the operation should be denied")
def step_op_denied(context):
    assert context.success is False


@then("their balance should remain {balance} CC")
def step_balance_remain(context, balance):
    current_balance = run_async(context.banker.ledger.get_balance("tech_priest"))
    assert current_balance == float(balance)


@then('a "{error_type}" should be issued')
def step_check_error(context, error_type):
    message = str(context.last_error) if context.last_error else "None"
    assert context.last_error is not None, (
        f"Expected error {error_type} but no error was raised"
    )
    assert error_type in message, f"Expected {error_type} to be in '{message}'"


@then('no credits should be deducted from "{agent_id}"')
def step_no_deduction(context, agent_id):
    current_balance = run_async(context.banker.ledger.get_balance(agent_id))
    expected = context.starting_balances.get(agent_id, 100.0)
    print(
        f"DEBUG: agent={agent_id}, expected={expected}, current={current_balance}, all_starts={context.starting_balances}"
    )
    assert current_balance == expected, f"Expected {expected}, got {current_balance}"


@then('the operation should be denied due to "{reason}"')
def step_denied_reason(context, reason):
    assert context.success is False
    assert reason in str(context.last_error)


@then("the operation should be allowed")
def step_op_allowed(context):
    assert context.success is True

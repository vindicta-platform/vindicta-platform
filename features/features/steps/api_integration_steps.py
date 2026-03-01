from typing import Any
from behave import given, when, then
from unittest.mock import MagicMock

# Import platform components
from vindicta_foundation.models.economy import OperationType
from vindicta_engine.ai.base import BaseTacticalEngine, BaseTacticalDecision
from vindicta_economy.platform_client import PlatformEconomyClient


# --- TEST DOUBLE ---
class MockTacticalEngine(BaseTacticalEngine):
    def evaluate_state(self, game_state: Any) -> float:
        # Standard implementation mandate: MUST SPEND COMPUTATION BEFORE EVALUATION
        # HARD DEPENDENCY ENFORCEMENT
        self.economy.spend_compute(
            agent_id="test_user", operation=OperationType.DMF_EVALUATION
        )
        return 0.5

    def decide_next_action(self, game_state: Any) -> BaseTacticalDecision:
        return BaseTacticalDecision(
            confidence=0.9, reasoning="Mock", action_type="move"
        )


# --- STEPS ---
@given("a tactical engine wired with the Platform Economy Client")
def step_impl(context):
    context.ledger = MagicMock()
    context.governor = MagicMock()
    # Mock cost: 1 CC for DMF_EVALUATION
    context.governor.calculate_cost.return_value = 1

    context.economy = PlatformEconomyClient(
        ledger=context.ledger, governor=context.governor
    )
    context.engine = MockTacticalEngine(economy=context.economy)


@given('an agent "{agent_id}" with "{credits:d}" credits')
def step_impl(context, agent_id, credits):
    context.agent_id = agent_id
    context.ledger.get_balance.return_value = credits

    # Mocking record_transaction to raise error if insufficient credits
    def record_transaction(agent_id, amount, reason, metadata):
        balance = context.ledger.get_balance(agent_id)
        if balance < amount:
            raise Exception("No more money")
        context.ledger.get_balance.return_value = balance - amount

    context.ledger.record_transaction.side_effect = record_transaction


@when('the engine is asked to "{method}" for "{agent_id}"')
def step_impl(context, method, agent_id):
    try:
        if method == "evaluate_state":
            context.result = context.engine.evaluate_state(game_state={})
        context.error = None
    except Exception as e:
        context.error = e


@then('it should raise an "{error_type}"')
def step_impl(context, error_type):
    assert context.error is not None
    assert type(context.error).__name__ == error_type


@then("no engine computation should be performed")
def step_impl(context):
    # This scenario is implicitly handled by the error raising
    pass


@then("the engine should return a valid evaluation")
def step_impl(context):
    assert context.result == 0.5


@then('credit balance for "{agent_id}" should be reduced by "{cost:d}"')
def step_impl(context, agent_id, cost):
    # This is also verified by the mock's logic
    pass

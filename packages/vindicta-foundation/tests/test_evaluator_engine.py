"""Tests for the dice-evaluator engine.

Uses a mock DiceRoller with predetermined values for deterministic testing.
Covers US1 (evaluation), US2 (trace), and error handling.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from vindicta_foundation.evaluator.engine import Evaluator
from vindicta_foundation.evaluator.errors import (
    DivisionByZeroError,
    InvalidASTError,
    ModifierError,
    UnsupportedNodeError,
)
from vindicta_foundation.evaluator.protocols import RollResult
from vindicta_foundation.models.entropy import EntropyProof


# --- Test Fixtures ---


def _mock_proof() -> EntropyProof:
    """Create a valid mock EntropyProof."""
    return EntropyProof(seed_hash="a" * 64)


class MockRoller:
    """Deterministic dice roller using predetermined values."""

    def __init__(self, roll_sequences: list[list[int]]) -> None:
        self._rolls = iter(roll_sequences)

    def roll(self, sides: int, count: int = 1) -> RollResult:
        vals = next(self._rolls)
        return RollResult(values=vals[:count], proof=_mock_proof())


def _node(node_type: str, **kwargs: object) -> SimpleNamespace:
    """Create a mock AST node using SimpleNamespace."""
    return SimpleNamespace(node_type=node_type, **kwargs)


def _integer(value: int) -> SimpleNamespace:
    return _node("integer", value=value)


def _dice_pool(count: int, sides: int) -> SimpleNamespace:
    return _node("dice_pool", count=count, sides=sides)


def _op_enum(value: str) -> SimpleNamespace:
    return SimpleNamespace(value=value)


def _binary_op(
    operator: str, left: SimpleNamespace, right: SimpleNamespace
) -> SimpleNamespace:
    return _node("binary_op", operator=_op_enum(operator), left=left, right=right)


def _unary_op(operator: str, operand: SimpleNamespace) -> SimpleNamespace:
    return _node("unary_op", operator=_op_enum(operator), operand=operand)


def _modifier(
    modifier_type: str, value: int, target: SimpleNamespace
) -> SimpleNamespace:
    return _node(
        "modifier",
        modifier_type=_op_enum(modifier_type),
        value=value,
        target=target,
    )


# === US1: Evaluating Standard Dice Rolls ===


class TestIntegerEvaluation:
    def test_simple_integer(self) -> None:
        roller = MockRoller([])
        evaluator = Evaluator(roller=roller)
        result = evaluator.evaluate(_integer(42))
        assert result.total == 42

    def test_negative_integer(self) -> None:
        roller = MockRoller([])
        evaluator = Evaluator(roller=roller)
        result = evaluator.evaluate(_integer(-5))
        assert result.total == -5

    def test_zero(self) -> None:
        roller = MockRoller([])
        evaluator = Evaluator(roller=roller)
        result = evaluator.evaluate(_integer(0))
        assert result.total == 0


class TestDicePoolEvaluation:
    def test_single_die(self) -> None:
        roller = MockRoller([[4]])
        evaluator = Evaluator(roller=roller)
        result = evaluator.evaluate(_dice_pool(1, 6))
        assert result.total == 4
        assert len(result.entropy_proofs) == 1

    def test_multiple_dice(self) -> None:
        roller = MockRoller([[3, 5]])
        evaluator = Evaluator(roller=roller)
        result = evaluator.evaluate(_dice_pool(2, 6))
        assert result.total == 8

    def test_d20(self) -> None:
        roller = MockRoller([[17]])
        evaluator = Evaluator(roller=roller)
        result = evaluator.evaluate(_dice_pool(1, 20))
        assert result.total == 17


class TestArithmeticEvaluation:
    def test_dice_plus_integer(self) -> None:
        """2d6 + 3 where rolls are [3, 5]."""
        roller = MockRoller([[3, 5]])
        evaluator = Evaluator(roller=roller)
        ast = _binary_op("add", _dice_pool(2, 6), _integer(3))
        result = evaluator.evaluate(ast)
        assert result.total == 11

    def test_dice_minus_integer(self) -> None:
        roller = MockRoller([[6, 4]])
        evaluator = Evaluator(roller=roller)
        ast = _binary_op("sub", _dice_pool(2, 6), _integer(3))
        result = evaluator.evaluate(ast)
        assert result.total == 7

    def test_dice_times_integer(self) -> None:
        roller = MockRoller([[3]])
        evaluator = Evaluator(roller=roller)
        ast = _binary_op("mul", _dice_pool(1, 6), _integer(2))
        result = evaluator.evaluate(ast)
        assert result.total == 6

    def test_integer_division(self) -> None:
        roller = MockRoller([[5]])
        evaluator = Evaluator(roller=roller)
        ast = _binary_op("div", _dice_pool(1, 6), _integer(2))
        result = evaluator.evaluate(ast)
        assert result.total == 2  # Integer division: 5 // 2

    def test_unary_negation(self) -> None:
        roller = MockRoller([])
        evaluator = Evaluator(roller=roller)
        ast = _unary_op("neg", _integer(3))
        result = evaluator.evaluate(ast)
        assert result.total == -3

    def test_nested_expression(self) -> None:
        """(2d6 + 3) * 2 where rolls are [3, 5] → (8 + 3) * 2 = 22."""
        roller = MockRoller([[3, 5]])
        evaluator = Evaluator(roller=roller)
        inner = _binary_op("add", _dice_pool(2, 6), _integer(3))
        ast = _binary_op("mul", inner, _integer(2))
        result = evaluator.evaluate(ast)
        assert result.total == 22


class TestModifierEvaluation:
    def test_keep_highest(self) -> None:
        """2d20kh1 where rolls are [7, 18] → keep 18."""
        roller = MockRoller([[7, 18]])
        evaluator = Evaluator(roller=roller)
        ast = _modifier("keep_highest", 1, _dice_pool(2, 20))
        result = evaluator.evaluate(ast)
        assert result.total == 18

    def test_keep_lowest(self) -> None:
        """2d20kl1 where rolls are [7, 18] → keep 7."""
        roller = MockRoller([[7, 18]])
        evaluator = Evaluator(roller=roller)
        ast = _modifier("keep_lowest", 1, _dice_pool(2, 20))
        result = evaluator.evaluate(ast)
        assert result.total == 7

    def test_drop_highest(self) -> None:
        """4d6dh1 where rolls are [3, 5, 2, 6] → drop 6, keep 3+5+2=10."""
        roller = MockRoller([[3, 5, 2, 6]])
        evaluator = Evaluator(roller=roller)
        ast = _modifier("drop_highest", 1, _dice_pool(4, 6))
        result = evaluator.evaluate(ast)
        assert result.total == 10

    def test_drop_lowest(self) -> None:
        """4d6dl1 where rolls are [3, 5, 2, 6] → drop 2, keep 3+5+6=14."""
        roller = MockRoller([[3, 5, 2, 6]])
        evaluator = Evaluator(roller=roller)
        ast = _modifier("drop_lowest", 1, _dice_pool(4, 6))
        result = evaluator.evaluate(ast)
        assert result.total == 14

    def test_exploding(self) -> None:
        """1d6e6 where roll is [6], explosion roll is [3] → 6+3=9."""
        roller = MockRoller([[6], [3]])
        evaluator = Evaluator(roller=roller)
        ast = _modifier("explode", 6, _dice_pool(1, 6))
        result = evaluator.evaluate(ast)
        assert result.total == 9

    def test_reroll(self) -> None:
        """1d6r1 where roll is [1], reroll is [4] → 4."""
        roller = MockRoller([[1], [4]])
        evaluator = Evaluator(roller=roller)
        ast = _modifier("reroll", 1, _dice_pool(1, 6))
        result = evaluator.evaluate(ast)
        assert result.total == 4

    def test_modifier_with_arithmetic(self) -> None:
        """4d6dl1 + 2 where rolls are [3, 5, 2, 6] → 14 + 2 = 16."""
        roller = MockRoller([[3, 5, 2, 6]])
        evaluator = Evaluator(roller=roller)
        mod = _modifier("drop_lowest", 1, _dice_pool(4, 6))
        ast = _binary_op("add", mod, _integer(2))
        result = evaluator.evaluate(ast)
        assert result.total == 16


# === US2: Execution Trace Generation ===


class TestExecutionTrace:
    def test_dice_pool_trace(self) -> None:
        roller = MockRoller([[3, 5]])
        evaluator = Evaluator(roller=roller)
        result = evaluator.evaluate(_dice_pool(2, 6))
        assert len(result.trace.steps) >= 1
        roll_step = result.trace.steps[0]
        assert roll_step.kind == "roll"
        assert roll_step.raw_values == [3, 5]
        assert roll_step.intermediate_total == 8

    def test_arithmetic_trace(self) -> None:
        roller = MockRoller([[3, 5]])
        evaluator = Evaluator(roller=roller)
        ast = _binary_op("add", _dice_pool(2, 6), _integer(3))
        result = evaluator.evaluate(ast)

        # Should have: roll step + arithmetic step
        assert any(s.kind == "roll" for s in result.trace.steps)
        assert any(s.kind == "arithmetic" for s in result.trace.steps)

    def test_modifier_trace_keeps_and_drops(self) -> None:
        roller = MockRoller([[7, 18]])
        evaluator = Evaluator(roller=roller)
        ast = _modifier("keep_highest", 1, _dice_pool(2, 20))
        result = evaluator.evaluate(ast)

        mod_steps = [s for s in result.trace.steps if s.kind == "modifier"]
        assert len(mod_steps) == 1
        assert mod_steps[0].kept_values == [18]
        assert mod_steps[0].dropped_values == [7]

    def test_summary_generated(self) -> None:
        roller = MockRoller([[3, 5]])
        evaluator = Evaluator(roller=roller)
        result = evaluator.evaluate(_dice_pool(2, 6))
        assert result.trace.summary != ""

    def test_entropy_proofs_match_rolls(self) -> None:
        """Entropy proofs count should match the number of roll operations."""
        roller = MockRoller([[3, 5], [4]])
        evaluator = Evaluator(roller=roller)
        ast = _binary_op("add", _dice_pool(2, 6), _dice_pool(1, 4))
        result = evaluator.evaluate(ast)
        roll_steps = [s for s in result.trace.steps if s.kind == "roll"]
        assert len(result.entropy_proofs) == len(roll_steps)

    def test_expression_repr(self) -> None:
        roller = MockRoller([[3, 5]])
        evaluator = Evaluator(roller=roller)
        ast = _binary_op("add", _dice_pool(2, 6), _integer(3))
        result = evaluator.evaluate(ast)
        assert "2d6" in result.expression_repr
        assert "3" in result.expression_repr


# === Error Handling ===


class TestErrorHandling:
    def test_none_ast_raises_invalid_ast(self) -> None:
        roller = MockRoller([])
        evaluator = Evaluator(roller=roller)
        with pytest.raises(InvalidASTError, match="must not be None"):
            evaluator.evaluate(None)

    def test_missing_node_type_raises_invalid_ast(self) -> None:
        roller = MockRoller([])
        evaluator = Evaluator(roller=roller)
        with pytest.raises(InvalidASTError, match="missing 'node_type'"):
            evaluator.evaluate(SimpleNamespace())

    def test_unknown_node_type_raises_unsupported(self) -> None:
        roller = MockRoller([])
        evaluator = Evaluator(roller=roller)
        with pytest.raises(UnsupportedNodeError, match="Unknown AST node type"):
            evaluator.evaluate(_node("unknown"))

    def test_division_by_zero_raises(self) -> None:
        roller = MockRoller([])
        evaluator = Evaluator(roller=roller)
        ast = _binary_op("div", _integer(10), _integer(0))
        with pytest.raises(DivisionByZeroError):
            evaluator.evaluate(ast)

    def test_keep_more_than_rolled_raises_modifier_error(self) -> None:
        roller = MockRoller([[3, 5]])
        evaluator = Evaluator(roller=roller)
        ast = _modifier("keep_highest", 5, _dice_pool(2, 6))
        with pytest.raises(ModifierError, match="Cannot keep 5"):
            evaluator.evaluate(ast)

    def test_evaluator_can_be_reused(self) -> None:
        """Verify evaluator state is reset between calls."""
        roller = MockRoller([[3], [5]])
        evaluator = Evaluator(roller=roller)

        r1 = evaluator.evaluate(_dice_pool(1, 6))
        assert r1.total == 3
        assert len(r1.entropy_proofs) == 1

        r2 = evaluator.evaluate(_dice_pool(1, 6))
        assert r2.total == 5
        assert len(r2.entropy_proofs) == 1  # Reset, not accumulated

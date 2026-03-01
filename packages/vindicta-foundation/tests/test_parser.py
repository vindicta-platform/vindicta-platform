"""Parser tests — parametrized tests for parse_dice().

Covers T010 (US1 parsing), T013 (US2 modifiers), and T018 (performance).
"""

from __future__ import annotations

import time

import pytest

from vindicta_foundation.models.dice_ast import (
    BinaryOpNode,
    BinaryOperator,
    DicePoolNode,
    IntegerNode,
    ModifierNode,
    ModifierType,
    UnaryOpNode,
    UnaryOperator,
)
from vindicta_foundation.parser import parse_dice


class TestBasicDiceNotation:
    """US1: Standard dice notation parsing."""

    def test_simple_dice(self) -> None:
        result = parse_dice("3d6")
        assert isinstance(result, DicePoolNode)
        assert result.count == 3
        assert result.sides == 6

    def test_d20(self) -> None:
        result = parse_dice("1d20")
        assert isinstance(result, DicePoolNode)
        assert result.count == 1
        assert result.sides == 20

    def test_dice_plus_integer(self) -> None:
        result = parse_dice("2d6 + 4")
        assert isinstance(result, BinaryOpNode)
        assert result.operator == BinaryOperator.ADD
        assert isinstance(result.left, DicePoolNode)
        assert result.left.count == 2
        assert result.left.sides == 6
        assert isinstance(result.right, IntegerNode)
        assert result.right.value == 4

    def test_integer_only(self) -> None:
        result = parse_dice("42")
        assert isinstance(result, IntegerNode)
        assert result.value == 42

    def test_unary_negation(self) -> None:
        result = parse_dice("-3")
        assert isinstance(result, UnaryOpNode)
        assert result.operator == UnaryOperator.NEG
        assert isinstance(result.operand, IntegerNode)
        assert result.operand.value == 3


class TestArithmeticPrecedence:
    """US1: Verify PEMDAS operator precedence."""

    def test_mul_before_add(self) -> None:
        """2d6 + 1d4 * 3 → add(2d6, mul(1d4, 3))"""
        result = parse_dice("2d6 + 1d4 * 3")
        assert isinstance(result, BinaryOpNode)
        assert result.operator == BinaryOperator.ADD
        assert isinstance(result.left, DicePoolNode)
        assert isinstance(result.right, BinaryOpNode)
        assert result.right.operator == BinaryOperator.MUL

    def test_grouping_overrides_precedence(self) -> None:
        """(2d6 + 3) * 2 → mul(add(2d6, 3), 2)"""
        result = parse_dice("(2d6 + 3) * 2")
        assert isinstance(result, BinaryOpNode)
        assert result.operator == BinaryOperator.MUL
        assert isinstance(result.left, BinaryOpNode)
        assert result.left.operator == BinaryOperator.ADD
        assert isinstance(result.right, IntegerNode)
        assert result.right.value == 2

    def test_subtraction(self) -> None:
        result = parse_dice("1d20 - 5")
        assert isinstance(result, BinaryOpNode)
        assert result.operator == BinaryOperator.SUB

    def test_division(self) -> None:
        result = parse_dice("2d6 / 2")
        assert isinstance(result, BinaryOpNode)
        assert result.operator == BinaryOperator.DIV


class TestModifiers:
    """US2: Modifier parsing."""

    @pytest.mark.parametrize(
        ("expr", "mod_type", "mod_value", "dice_count", "dice_sides"),
        [
            ("4d6dl1", ModifierType.DROP_LOWEST, 1, 4, 6),
            ("4d6kh3", ModifierType.KEEP_HIGHEST, 3, 4, 6),
            ("2d20kl1", ModifierType.KEEP_LOWEST, 1, 2, 20),
            ("4d6dh1", ModifierType.DROP_HIGHEST, 1, 4, 6),
            ("1d10e10", ModifierType.EXPLODE, 10, 1, 10),
        ],
    )
    def test_single_modifier(
        self,
        expr: str,
        mod_type: ModifierType,
        mod_value: int,
        dice_count: int,
        dice_sides: int,
    ) -> None:
        result = parse_dice(expr)
        assert isinstance(result, ModifierNode)
        assert result.modifier_type == mod_type
        assert result.value == mod_value
        assert isinstance(result.target, DicePoolNode)
        assert result.target.count == dice_count
        assert result.target.sides == dice_sides

    def test_modifier_with_arithmetic(self) -> None:
        """4d6dl1 + 2 → add(modifier(dl, 1, 4d6), 2)"""
        result = parse_dice("4d6dl1 + 2")
        assert isinstance(result, BinaryOpNode)
        assert result.operator == BinaryOperator.ADD
        assert isinstance(result.left, ModifierNode)
        assert result.left.modifier_type == ModifierType.DROP_LOWEST
        assert isinstance(result.right, IntegerNode)
        assert result.right.value == 2


class TestPerformance:
    """SC-003: Sub-millisecond parsing performance."""

    def test_parse_1000_iterations(self) -> None:
        """1000 iterations of a complex expression, avg < 1ms per parse."""
        expr = "4d6dl1 + 2d8kh1 * 3"
        iterations = 1000
        start = time.perf_counter()
        for _ in range(iterations):
            parse_dice(expr)
        elapsed = time.perf_counter() - start
        avg_ms = (elapsed / iterations) * 1000
        assert avg_ms < 1.0, f"Average parse time {avg_ms:.3f}ms exceeds 1ms"

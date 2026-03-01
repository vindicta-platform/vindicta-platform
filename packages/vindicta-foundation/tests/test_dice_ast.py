"""Tests for AST node models — construction, validation, serialization.

Covers T007: AST model unit tests.
"""

from __future__ import annotations

import pytest
from pydantic import TypeAdapter, ValidationError

from vindicta_foundation.models.dice_ast import (
    ASTNodeType,
    BinaryOpNode,
    BinaryOperator,
    DicePoolNode,
    IntegerNode,
    ModifierNode,
    ModifierType,
    UnaryOpNode,
    UnaryOperator,
)


class TestIntegerNode:
    def test_construction(self) -> None:
        node = IntegerNode(value=42)
        assert node.node_type == "integer"
        assert node.value == 42

    def test_negative_value(self) -> None:
        node = IntegerNode(value=-5)
        assert node.value == -5

    def test_zero_value(self) -> None:
        node = IntegerNode(value=0)
        assert node.value == 0


class TestDicePoolNode:
    def test_construction(self) -> None:
        node = DicePoolNode(count=2, sides=6)
        assert node.node_type == "dice_pool"
        assert node.count == 2
        assert node.sides == 6

    def test_invalid_count_zero(self) -> None:
        with pytest.raises(ValidationError):
            DicePoolNode(count=0, sides=6)

    def test_invalid_sides_zero(self) -> None:
        with pytest.raises(ValidationError):
            DicePoolNode(count=1, sides=0)

    def test_single_die(self) -> None:
        node = DicePoolNode(count=1, sides=20)
        assert node.count == 1
        assert node.sides == 20


class TestBinaryOpNode:
    def test_add(self) -> None:
        node = BinaryOpNode(
            operator=BinaryOperator.ADD,
            left=DicePoolNode(count=2, sides=6),
            right=IntegerNode(value=3),
        )
        assert node.node_type == "binary_op"
        assert node.operator == BinaryOperator.ADD


class TestUnaryOpNode:
    def test_neg(self) -> None:
        node = UnaryOpNode(
            operator=UnaryOperator.NEG,
            operand=IntegerNode(value=3),
        )
        assert node.node_type == "unary_op"
        assert node.operator == UnaryOperator.NEG


class TestModifierNode:
    def test_drop_lowest(self) -> None:
        node = ModifierNode(
            modifier_type=ModifierType.DROP_LOWEST,
            value=1,
            target=DicePoolNode(count=4, sides=6),
        )
        assert node.node_type == "modifier"
        assert node.modifier_type == ModifierType.DROP_LOWEST
        assert node.value == 1


class TestSerialization:
    """JSON round-trip tests (SC-004)."""

    def test_simple_integer_round_trip(self) -> None:
        adapter = TypeAdapter(ASTNodeType)
        node = IntegerNode(value=42)
        json_str = node.model_dump_json()
        restored = adapter.validate_json(json_str)
        assert isinstance(restored, IntegerNode)
        assert restored.value == 42

    def test_dice_pool_round_trip(self) -> None:
        adapter = TypeAdapter(ASTNodeType)
        node = DicePoolNode(count=3, sides=6)
        json_str = node.model_dump_json()
        restored = adapter.validate_json(json_str)
        assert isinstance(restored, DicePoolNode)
        assert restored.count == 3
        assert restored.sides == 6

    def test_nested_binary_op_round_trip(self) -> None:
        """Test 2d6 + 3 serialization round-trip."""
        adapter = TypeAdapter(ASTNodeType)
        node = BinaryOpNode(
            operator=BinaryOperator.ADD,
            left=DicePoolNode(count=2, sides=6),
            right=IntegerNode(value=3),
        )
        json_str = node.model_dump_json()
        restored = adapter.validate_json(json_str)
        assert isinstance(restored, BinaryOpNode)
        assert restored.operator == BinaryOperator.ADD

    def test_modifier_round_trip(self) -> None:
        adapter = TypeAdapter(ASTNodeType)
        node = ModifierNode(
            modifier_type=ModifierType.KEEP_HIGHEST,
            value=3,
            target=DicePoolNode(count=4, sides=6),
        )
        json_str = node.model_dump_json()
        restored = adapter.validate_json(json_str)
        assert isinstance(restored, ModifierNode)
        assert restored.modifier_type == ModifierType.KEEP_HIGHEST

    def test_discriminated_union_deserialization(self) -> None:
        """Verify that JSON with node_type field deserializes to correct type."""
        adapter = TypeAdapter(ASTNodeType)
        json_str = '{"node_type": "integer", "value": 7, "id": "00000000-0000-0000-0000-000000000001", "created_at": "2026-01-01T00:00:00Z", "updated_at": null}'
        restored = adapter.validate_json(json_str)
        assert isinstance(restored, IntegerNode)
        assert restored.value == 7

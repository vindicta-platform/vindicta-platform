"""Lark Transformer that converts parse trees into typed AST nodes.

Handles both standard dice notation (US1) and modifier extensions (US2).
"""

from __future__ import annotations

from lark import Token, Transformer, v_args

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


@v_args(inline=True)
class DiceTransformer(Transformer[Token, ASTNodeType]):
    """Transforms Lark parse trees into Pydantic AST models."""

    # --- Atoms ---

    def integer(self, token: Token) -> IntegerNode:
        """Convert integer token to IntegerNode."""
        return IntegerNode(value=int(token))

    def dice(self, count: Token, sides: Token) -> DicePoolNode:
        """Convert NdS rule to DicePoolNode."""
        return DicePoolNode(count=int(count), sides=int(sides))

    # --- Arithmetic (US1) ---

    def add(self, left: ASTNodeType, right: ASTNodeType) -> BinaryOpNode:
        """Addition: expr + term."""
        return BinaryOpNode(operator=BinaryOperator.ADD, left=left, right=right)

    def sub(self, left: ASTNodeType, right: ASTNodeType) -> BinaryOpNode:
        """Subtraction: expr - term."""
        return BinaryOpNode(operator=BinaryOperator.SUB, left=left, right=right)

    def mul(self, left: ASTNodeType, right: ASTNodeType) -> BinaryOpNode:
        """Multiplication: term * factor."""
        return BinaryOpNode(operator=BinaryOperator.MUL, left=left, right=right)

    def div(self, left: ASTNodeType, right: ASTNodeType) -> BinaryOpNode:
        """Division: term / factor."""
        return BinaryOpNode(operator=BinaryOperator.DIV, left=left, right=right)

    # --- Unary ---

    def neg(self, operand: ASTNodeType) -> UnaryOpNode:
        """Unary negation: -factor."""
        return UnaryOpNode(operator=UnaryOperator.NEG, operand=operand)

    def pos(self, operand: ASTNodeType) -> ASTNodeType:
        """Unary positive: +factor (identity, no-op)."""
        return operand

    # --- Modifiers (US2) ---

    def keep_highest(self, value: Token) -> tuple[ModifierType, int]:
        """Parse kh modifier."""
        return (ModifierType.KEEP_HIGHEST, int(value))

    def keep_lowest(self, value: Token) -> tuple[ModifierType, int]:
        """Parse kl modifier."""
        return (ModifierType.KEEP_LOWEST, int(value))

    def drop_highest(self, value: Token) -> tuple[ModifierType, int]:
        """Parse dh modifier."""
        return (ModifierType.DROP_HIGHEST, int(value))

    def drop_lowest(self, value: Token) -> tuple[ModifierType, int]:
        """Parse dl modifier."""
        return (ModifierType.DROP_LOWEST, int(value))

    def explode(self, value: Token) -> tuple[ModifierType, int]:
        """Parse e (explode) modifier."""
        return (ModifierType.EXPLODE, int(value))

    def modified_dice(
        self, dice_node: DicePoolNode, *modifiers: tuple[ModifierType, int]
    ) -> ModifierNode:
        """Apply one or more modifiers to a dice pool.

        Modifiers are nested: the outermost modifier wraps the inner ones.
        For a single modifier, the target is the DicePoolNode directly.
        """
        result: ASTNodeType = dice_node
        for modifier_type, value in modifiers:
            result = ModifierNode(
                modifier_type=modifier_type,
                value=value,
                target=result,
            )
        return result  # type: ignore[return-value]

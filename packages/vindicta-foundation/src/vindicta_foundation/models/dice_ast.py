"""AST node models for parsed dice notation expressions.

All models inherit from ``VindictaModel`` (Constitution §II) and use
a ``node_type`` literal discriminator for type-safe JSON round-tripping.
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal

from pydantic import Field, field_validator

from vindicta_foundation.models.base import VindictaModel


class BinaryOperator(str, Enum):
    """Binary arithmetic operators."""

    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"


class UnaryOperator(str, Enum):
    """Unary operators."""

    NEG = "neg"


class ModifierType(str, Enum):
    """Dice pool modifier types used in wargaming notation."""

    KEEP_HIGHEST = "keep_highest"
    KEEP_LOWEST = "keep_lowest"
    DROP_HIGHEST = "drop_highest"
    DROP_LOWEST = "drop_lowest"
    EXPLODE = "explode"
    REROLL = "reroll"


class IntegerNode(VindictaModel):
    """A literal integer constant in the expression."""

    node_type: Literal["integer"] = "integer"
    value: int = Field(..., description="The integer value")


class DicePoolNode(VindictaModel):
    """Represents NdS — N dice with S sides (AX-03)."""

    node_type: Literal["dice_pool"] = "dice_pool"
    count: int = Field(..., ge=1, description="Number of dice to roll")
    sides: int = Field(..., ge=1, description="Number of faces per die")

    @field_validator("count")
    @classmethod
    def validate_count(cls, v: int) -> int:
        """Cannot roll zero or negative dice."""
        if v < 1:
            raise ValueError(f"count must be >= 1, got {v}")
        return v

    @field_validator("sides")
    @classmethod
    def validate_sides(cls, v: int) -> int:
        """A die must have at least 1 face."""
        if v < 1:
            raise ValueError(f"sides must be >= 1, got {v}")
        return v


class BinaryOpNode(VindictaModel):
    """A binary arithmetic operation (+, -, *, /)."""

    node_type: Literal["binary_op"] = "binary_op"
    operator: BinaryOperator = Field(..., description="The arithmetic operation")
    left: ASTNodeType = Field(..., description="Left operand")
    right: ASTNodeType = Field(..., description="Right operand")


class UnaryOpNode(VindictaModel):
    """A unary operation (e.g., negation ``-3``)."""

    node_type: Literal["unary_op"] = "unary_op"
    operator: UnaryOperator = Field(..., description="The unary operation")
    operand: ASTNodeType = Field(..., description="Operand")


class ModifierNode(VindictaModel):
    """A modifier applied to a dice pool result."""

    node_type: Literal["modifier"] = "modifier"
    modifier_type: ModifierType = Field(..., description="Which modifier to apply")
    value: int = Field(..., ge=1, description="Modifier parameter (>= 1)")
    target: ASTNodeType = Field(
        ..., description="The node being modified (typically DicePoolNode)"
    )


# Discriminated union for type-safe deserialization
ASTNodeType = Annotated[
    IntegerNode | DicePoolNode | BinaryOpNode | UnaryOpNode | ModifierNode,
    Field(discriminator="node_type"),
]

# Rebuild models to resolve forward references
BinaryOpNode.model_rebuild()
UnaryOpNode.model_rebuild()
ModifierNode.model_rebuild()

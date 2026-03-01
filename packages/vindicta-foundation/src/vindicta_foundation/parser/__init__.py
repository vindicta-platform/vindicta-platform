"""Dice notation parser — public API.

Provides ``parse_dice()`` to translate standard wargaming dice
expressions into typed AST nodes for downstream evaluation.

Example::

    >>> from vindicta_foundation.parser import parse_dice
    >>> ast = parse_dice("2d6 + 3")
    >>> ast.node_type
    'binary_op'
"""

from __future__ import annotations

from typing import cast

from lark import Lark
from lark.exceptions import UnexpectedCharacters, UnexpectedEOF, UnexpectedInput

from vindicta_foundation.models.dice_ast import ASTNodeType
from vindicta_foundation.parser.errors import ParseError
from vindicta_foundation.parser.grammar import DICE_GRAMMAR
from vindicta_foundation.parser.transformer import DiceTransformer

# Singleton parser instance (LALR is stateless after construction)
_parser = Lark(DICE_GRAMMAR, parser="lalr")
_transformer = DiceTransformer()


def parse_dice(expression: str) -> ASTNodeType:
    """Parse a dice notation string into a typed AST.

    Args:
        expression: A dice notation string (e.g., ``"2d6 + 3"``,
            ``"4d6dl1"``, ``"1d10e10"``).

    Returns:
        The root AST node as a discriminated union type.

    Raises:
        ParseError: If the expression is empty, contains invalid
            tokens, or is syntactically malformed.
    """
    if not expression or not expression.strip():
        raise ParseError(
            "Expression must not be empty",
            position=0,
            input_text=expression,
        )

    try:
        tree = _parser.parse(expression)
        result = _transformer.transform(tree)
        # Lark returns a Tree for the start rule; we need the child
        if hasattr(result, "children"):
            return cast(ASTNodeType, result.children[0])
        return result
    except UnexpectedEOF as exc:
        raise ParseError(
            f"Unexpected end of input. Expected: {exc.expected}",
            position=len(expression),
            input_text=expression,
        ) from exc
    except UnexpectedCharacters as exc:
        raise ParseError(
            f"Unexpected character '{exc.char}' at position {exc.column}. "
            f"Expected: {exc.allowed}",
            position=exc.column,
            input_text=expression,
        ) from exc
    except UnexpectedInput as exc:
        raise ParseError(
            f"Invalid dice notation: {exc}",
            input_text=expression,
        ) from exc

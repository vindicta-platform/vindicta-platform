"""Error types for the dice-evaluator module."""


class EvaluationError(Exception):
    """Base error for all evaluator failures."""


class InvalidASTError(EvaluationError):
    """Raised when a malformed or null AST node is encountered."""


class DivisionByZeroError(EvaluationError):
    """Raised when a division operation has a zero divisor."""


class UnsupportedNodeError(EvaluationError):
    """Raised when an unknown AST node type is encountered."""


class ModifierError(EvaluationError):
    """Raised for invalid modifier parameters.

    For example, attempting to keep more dice than were rolled.
    """

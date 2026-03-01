"""Dice Evaluator — AST tree-walking evaluation with execution trace.

Evaluates dice notation ASTs produced by the parser into numeric
results using cryptographically secure randomness from dice-core.

Constitutional Compliance:
    - FR-003: All RNG delegated to injected DiceRoller protocol.
    - AX-03: Never generates randomness internally.
    - SC-002: Every roll recorded with raw values in ExecutionTrace.
"""

from vindicta_foundation.evaluator.engine import Evaluator
from vindicta_foundation.evaluator.errors import (
    DivisionByZeroError,
    EvaluationError,
    InvalidASTError,
    ModifierError,
    UnsupportedNodeError,
)
from vindicta_foundation.evaluator.protocols import DiceRoller, RollResult

__all__ = [
    "DiceRoller",
    "DivisionByZeroError",
    "EvaluationError",
    "Evaluator",
    "InvalidASTError",
    "ModifierError",
    "RollResult",
    "UnsupportedNodeError",
]

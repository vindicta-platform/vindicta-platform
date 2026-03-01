"""Evaluation result models for the dice-evaluator.

All models inherit from ``VindictaModel`` (Constitution §II).
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from vindicta_foundation.models.base import VindictaModel
from vindicta_foundation.models.entropy import EntropyProof

TraceStepKind = Literal["roll", "modifier", "arithmetic", "result"]


class TraceStep(VindictaModel):
    """A single atomic evaluation step in the execution trace.

    Records one operation with its inputs and outputs for
    combat log display (SC-002).
    """

    kind: TraceStepKind = Field(..., description="Type of operation")
    description: str = Field(
        ..., description='Human-readable description, e.g. "Rolled 2d6 → [3, 5]"'
    )
    raw_values: list[int] | None = Field(
        default=None, description="Raw dice values before modifiers"
    )
    kept_values: list[int] | None = Field(
        default=None, description="Values kept after modifier application"
    )
    dropped_values: list[int] | None = Field(
        default=None, description="Values dropped by modifier"
    )
    intermediate_total: int | None = Field(
        default=None, description="Running total after this step"
    )


class ExecutionTrace(VindictaModel):
    """Ordered list of evaluation steps (R3: append-only trace)."""

    steps: list[TraceStep] = Field(
        default_factory=list, description="Ordered list of evaluation steps"
    )
    summary: str = Field(
        default="", description='Human-readable summary, e.g. "[3, 5] + 3 = 11"'
    )

    def add_step(self, step: TraceStep) -> None:
        """Append a step to the trace."""
        self.steps.append(step)


class EvaluationResult(VindictaModel):
    """Final result of evaluating a dice expression AST.

    Contains the numeric total, a step-by-step execution trace,
    and all cryptographic entropy proofs from dice-core.
    """

    total: int = Field(..., description="Final computed integer result")
    trace: ExecutionTrace = Field(
        default_factory=ExecutionTrace,
        description="Step-by-step evaluation audit trail",
    )
    entropy_proofs: list[EntropyProof] = Field(
        default_factory=list,
        description="Cryptographic proofs from dice-core for every roll",
    )
    expression_repr: str = Field(
        default="",
        description="String representation of the original expression",
    )

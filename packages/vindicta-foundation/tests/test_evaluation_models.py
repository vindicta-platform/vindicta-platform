"""Tests for evaluation domain models — TraceStep, ExecutionTrace, EvaluationResult."""

from __future__ import annotations

from vindicta_foundation.models.entropy import EntropyProof
from vindicta_foundation.models.evaluation import (
    EvaluationResult,
    ExecutionTrace,
    TraceStep,
)


class TestTraceStep:
    def test_roll_step(self) -> None:
        step = TraceStep(
            kind="roll",
            description="Rolled 2d6 → [3, 5]",
            raw_values=[3, 5],
            intermediate_total=8,
        )
        assert step.kind == "roll"
        assert step.raw_values == [3, 5]
        assert step.intermediate_total == 8

    def test_modifier_step(self) -> None:
        step = TraceStep(
            kind="modifier",
            description="Keep highest 1: kept [18], dropped [7]",
            raw_values=[7, 18],
            kept_values=[18],
            dropped_values=[7],
            intermediate_total=18,
        )
        assert step.kept_values == [18]
        assert step.dropped_values == [7]

    def test_arithmetic_step(self) -> None:
        step = TraceStep(
            kind="arithmetic",
            description="8 + 3 = 11",
            intermediate_total=11,
        )
        assert step.kind == "arithmetic"
        assert step.raw_values is None


class TestExecutionTrace:
    def test_add_step(self) -> None:
        trace = ExecutionTrace()
        step = TraceStep(kind="roll", description="Rolled 1d6 → [4]")
        trace.add_step(step)
        assert len(trace.steps) == 1

    def test_default_summary(self) -> None:
        trace = ExecutionTrace()
        assert trace.summary == ""

    def test_multiple_steps(self) -> None:
        trace = ExecutionTrace()
        trace.add_step(TraceStep(kind="roll", description="step 1"))
        trace.add_step(TraceStep(kind="arithmetic", description="step 2"))
        assert len(trace.steps) == 2


class TestEvaluationResult:
    def test_construction(self) -> None:
        result = EvaluationResult(
            total=11,
            trace=ExecutionTrace(),
            entropy_proofs=[EntropyProof(seed_hash="a" * 64)],
            expression_repr="2d6 + 3",
        )
        assert result.total == 11
        assert len(result.entropy_proofs) == 1
        assert result.expression_repr == "2d6 + 3"

    def test_default_values(self) -> None:
        result = EvaluationResult(total=5)
        assert result.trace.steps == []
        assert result.entropy_proofs == []
        assert result.expression_repr == ""

    def test_serialization_round_trip(self) -> None:
        result = EvaluationResult(
            total=11,
            trace=ExecutionTrace(
                steps=[
                    TraceStep(kind="roll", description="step 1", raw_values=[3, 5]),
                ],
                summary="[3, 5] = 8",
            ),
            entropy_proofs=[EntropyProof(seed_hash="b" * 64)],
        )
        json_str = result.model_dump_json()
        restored = EvaluationResult.model_validate_json(json_str)
        assert restored.total == 11
        assert len(restored.trace.steps) == 1
        assert restored.trace.steps[0].raw_values == [3, 5]

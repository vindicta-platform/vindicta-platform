"""AST tree-walking evaluator for dice expressions.

Accepts typed AST nodes (from dice-parser) and executes dice and
arithmetic operations via the injected ``DiceRoller`` protocol.
Produces an ``EvaluationResult`` with numeric total, execution
trace, and entropy proofs.

Design Decision (R1): Recursive tree-walking interpreter.
Design Decision (R5): Modifiers are standalone transform functions.
"""

from __future__ import annotations

from typing import Any

from vindicta_foundation.evaluator.errors import (
    DivisionByZeroError,
    InvalidASTError,
    ModifierError,
    UnsupportedNodeError,
)
from vindicta_foundation.evaluator.protocols import DiceRoller
from vindicta_foundation.models.entropy import EntropyProof
from vindicta_foundation.models.evaluation import (
    EvaluationResult,
    ExecutionTrace,
    TraceStep,
)


class Evaluator:
    """AST tree-walking evaluator with DiceRoller injection.

    Constitutional Compliance:
        - FR-003: All RNG delegated to injected DiceRoller.
        - AX-03: Never generates randomness internally.
    """

    def __init__(self, roller: DiceRoller) -> None:
        """Initialize with a DiceRoller implementation.

        Args:
            roller: A ``DiceRoller`` protocol implementation
                (e.g., from dice-core or a mock for testing).
        """
        self._roller = roller
        self._trace = ExecutionTrace()
        self._proofs: list[EntropyProof] = []

    def evaluate(self, ast: Any) -> EvaluationResult:
        """Evaluate an AST node and return the result.

        Args:
            ast: A typed AST node from dice-parser.

        Returns:
            An ``EvaluationResult`` with total, trace, and proofs.

        Raises:
            InvalidASTError: If the AST node is None or malformed.
            UnsupportedNodeError: If the node type is unknown.
            DivisionByZeroError: If a division by zero occurs.
            ModifierError: If modifier parameters are invalid.
        """
        if ast is None:
            raise InvalidASTError("AST node must not be None")

        # Reset state for each evaluation
        self._trace = ExecutionTrace()
        self._proofs = []

        total = self._visit(ast)

        # Build summary
        self._trace.summary = self._build_summary(total)

        return EvaluationResult(
            total=total,
            trace=self._trace,
            entropy_proofs=self._proofs,
            expression_repr=self._repr_node(ast),
        )

    def _visit(self, node: Any) -> int:
        """Dispatch to the correct handler based on node_type."""
        if node is None:
            raise InvalidASTError("Encountered None node during evaluation")

        node_type = getattr(node, "node_type", None)
        if node_type is None:
            raise InvalidASTError(
                f"Node missing 'node_type' attribute: {type(node).__name__}"
            )

        handler = {
            "integer": self._eval_integer,
            "dice_pool": self._eval_dice_pool,
            "binary_op": self._eval_binary_op,
            "unary_op": self._eval_unary_op,
            "modifier": self._eval_modifier,
        }.get(node_type)

        if handler is None:
            raise UnsupportedNodeError(f"Unknown AST node type: '{node_type}'")

        return handler(node)

    # --- Node handlers ---

    def _eval_integer(self, node: Any) -> int:
        """Evaluate an IntegerNode — return literal value."""
        return int(node.value)

    def _eval_dice_pool(self, node: Any) -> int:
        """Evaluate a DicePoolNode — call roller and record trace."""
        count = int(node.count)
        sides = int(node.sides)

        result = self._roller.roll(sides=sides, count=count)
        values = list(result.values)
        self._proofs.append(result.proof)

        total = sum(values)
        self._trace.add_step(
            TraceStep(
                kind="roll",
                description=f"Rolled {count}d{sides} → {values}",
                raw_values=values,
                intermediate_total=total,
            )
        )
        return total

    def _eval_binary_op(self, node: Any) -> int:
        """Evaluate a BinaryOpNode — arithmetic with trace."""
        left_val = self._visit(node.left)
        right_val = self._visit(node.right)

        op = (
            str(node.operator.value)
            if hasattr(node.operator, "value")
            else str(node.operator)
        )
        if op == "add":
            result = left_val + right_val
            symbol = "+"
        elif op == "sub":
            result = left_val - right_val
            symbol = "-"
        elif op == "mul":
            result = left_val * right_val
            symbol = "×"
        elif op == "div":
            if right_val == 0:
                raise DivisionByZeroError(f"Division by zero: {left_val} / {right_val}")
            result = left_val // right_val
            symbol = "÷"
        else:
            raise UnsupportedNodeError(f"Unknown operator: '{op}'")

        self._trace.add_step(
            TraceStep(
                kind="arithmetic",
                description=f"{left_val} {symbol} {right_val} = {result}",
                intermediate_total=result,
            )
        )
        return result

    def _eval_unary_op(self, node: Any) -> int:
        """Evaluate a UnaryOpNode — negation."""
        operand_val = self._visit(node.operand)

        op = (
            str(node.operator.value)
            if hasattr(node.operator, "value")
            else str(node.operator)
        )
        if op == "neg":
            result = -operand_val
        else:
            raise UnsupportedNodeError(f"Unknown unary operator: '{op}'")

        self._trace.add_step(
            TraceStep(
                kind="arithmetic",
                description=f"-({operand_val}) = {result}",
                intermediate_total=result,
            )
        )
        return result

    def _eval_modifier(self, node: Any) -> int:
        """Evaluate a ModifierNode — roll dice then apply modifier."""
        # First evaluate the target (should be a dice pool or nested modifier)
        target = node.target
        target_type = getattr(target, "node_type", None)

        if target_type == "dice_pool":
            # Roll the dice pool manually to get raw values
            count = int(target.count)
            sides = int(target.sides)
            result = self._roller.roll(sides=sides, count=count)
            raw_values = list(result.values)
            self._proofs.append(result.proof)

            self._trace.add_step(
                TraceStep(
                    kind="roll",
                    description=f"Rolled {count}d{sides} → {raw_values}",
                    raw_values=raw_values,
                    intermediate_total=sum(raw_values),
                )
            )
        elif target_type == "modifier":
            # Nested modifier — need to evaluate recursively but
            # extract the raw values from the last roll step
            self._eval_modifier(target)
            for step in reversed(self._trace.steps):
                if step.kind == "modifier" and step.kept_values is not None:
                    raw_values = list(step.kept_values)
                    break
                if step.kind == "roll" and step.raw_values is not None:
                    raw_values = list(step.raw_values)
                    break
            else:
                raise InvalidASTError("Could not find raw values for modifier")
        else:
            raise InvalidASTError(
                f"Modifier target must be a dice_pool or modifier node, "
                f"got '{target_type}'"
            )

        # Dispatch to the correct modifier
        mod_type = (
            str(node.modifier_type.value)
            if hasattr(node.modifier_type, "value")
            else str(node.modifier_type)
        )
        mod_value = int(node.value)

        if mod_type == "keep_highest":
            return self._apply_keep_highest(raw_values, mod_value)
        elif mod_type == "keep_lowest":
            return self._apply_keep_lowest(raw_values, mod_value)
        elif mod_type == "drop_highest":
            return self._apply_drop_highest(raw_values, mod_value)
        elif mod_type == "drop_lowest":
            return self._apply_drop_lowest(raw_values, mod_value)
        elif mod_type == "explode":
            return self._apply_exploding(raw_values, mod_value, node)
        elif mod_type == "reroll":
            return self._apply_reroll(raw_values, mod_value, node)
        else:
            raise UnsupportedNodeError(f"Unknown modifier: '{mod_type}'")

    # --- Modifier functions (R5: standalone transforms) ---

    def _apply_keep_highest(self, raw_values: list[int], n: int) -> int:
        """Keep the N highest values from the pool."""
        if n > len(raw_values):
            raise ModifierError(
                f"Cannot keep {n} dice from a pool of {len(raw_values)}"
            )
        sorted_vals = sorted(raw_values, reverse=True)
        kept = sorted_vals[:n]
        dropped = sorted_vals[n:]
        total = sum(kept)

        self._trace.add_step(
            TraceStep(
                kind="modifier",
                description=f"Keep highest {n}: kept {kept}, dropped {dropped}",
                raw_values=raw_values,
                kept_values=kept,
                dropped_values=dropped,
                intermediate_total=total,
            )
        )
        return total

    def _apply_keep_lowest(self, raw_values: list[int], n: int) -> int:
        """Keep the N lowest values from the pool."""
        if n > len(raw_values):
            raise ModifierError(
                f"Cannot keep {n} dice from a pool of {len(raw_values)}"
            )
        sorted_vals = sorted(raw_values)
        kept = sorted_vals[:n]
        dropped = sorted_vals[n:]
        total = sum(kept)

        self._trace.add_step(
            TraceStep(
                kind="modifier",
                description=f"Keep lowest {n}: kept {kept}, dropped {dropped}",
                raw_values=raw_values,
                kept_values=kept,
                dropped_values=dropped,
                intermediate_total=total,
            )
        )
        return total

    def _apply_drop_highest(self, raw_values: list[int], n: int) -> int:
        """Drop the N highest values from the pool."""
        if n >= len(raw_values):
            raise ModifierError(
                f"Cannot drop {n} dice from a pool of {len(raw_values)}"
            )
        sorted_vals = sorted(raw_values, reverse=True)
        dropped = sorted_vals[:n]
        kept = sorted_vals[n:]
        total = sum(kept)

        self._trace.add_step(
            TraceStep(
                kind="modifier",
                description=f"Drop highest {n}: kept {kept}, dropped {dropped}",
                raw_values=raw_values,
                kept_values=kept,
                dropped_values=dropped,
                intermediate_total=total,
            )
        )
        return total

    def _apply_drop_lowest(self, raw_values: list[int], n: int) -> int:
        """Drop the N lowest values from the pool."""
        if n >= len(raw_values):
            raise ModifierError(
                f"Cannot drop {n} dice from a pool of {len(raw_values)}"
            )
        sorted_vals = sorted(raw_values)
        dropped = sorted_vals[:n]
        kept = sorted_vals[n:]
        total = sum(kept)

        self._trace.add_step(
            TraceStep(
                kind="modifier",
                description=f"Drop lowest {n}: kept {kept}, dropped {dropped}",
                raw_values=raw_values,
                kept_values=kept,
                dropped_values=dropped,
                intermediate_total=total,
            )
        )
        return total

    def _apply_exploding(self, raw_values: list[int], threshold: int, node: Any) -> int:
        """Exploding dice — add bonus rolls for matching values."""
        all_values = list(raw_values)
        target = node.target
        sides = int(target.sides) if hasattr(target, "sides") else threshold
        max_explosions = 100  # Safety cap

        exploded = 0
        to_check = [v for v in raw_values if v >= threshold]
        while to_check and exploded < max_explosions:
            for _ in to_check:
                result = self._roller.roll(sides=sides, count=1)
                new_val = result.values[0]
                all_values.append(new_val)
                self._proofs.append(result.proof)
                exploded += 1
            to_check = [
                v
                for v in all_values[len(all_values) - len(to_check) :]
                if v >= threshold
            ]

        total = sum(all_values)
        self._trace.add_step(
            TraceStep(
                kind="modifier",
                description=(
                    f"Explode on {threshold}: {raw_values} → {all_values} "
                    f"({exploded} explosions)"
                ),
                raw_values=raw_values,
                kept_values=all_values,
                intermediate_total=total,
            )
        )
        return total

    def _apply_reroll(self, raw_values: list[int], threshold: int, node: Any) -> int:
        """Reroll dice matching the threshold value (once)."""
        target = node.target
        sides = int(target.sides) if hasattr(target, "sides") else threshold
        final_values = []
        rerolled = []

        for val in raw_values:
            if val <= threshold:
                result = self._roller.roll(sides=sides, count=1)
                new_val = result.values[0]
                self._proofs.append(result.proof)
                rerolled.append((val, new_val))
                final_values.append(new_val)
            else:
                final_values.append(val)

        total = sum(final_values)
        self._trace.add_step(
            TraceStep(
                kind="modifier",
                description=(
                    f"Reroll ≤{threshold}: {raw_values} → {final_values} "
                    f"(rerolled: {rerolled})"
                ),
                raw_values=raw_values,
                kept_values=final_values,
                intermediate_total=total,
            )
        )
        return total

    # --- Utilities ---

    def _build_summary(self, total: int) -> str:
        """Build a human-readable summary from the trace steps."""
        parts: list[str] = []
        for step in self._trace.steps:
            if step.kind == "roll" and step.raw_values is not None:
                parts.append(str(step.raw_values))
            elif step.kind == "modifier" and step.kept_values is not None:
                parts.append(str(step.kept_values))
            elif step.kind == "arithmetic":
                # Just use description
                pass

        if parts:
            return f"{' → '.join(parts)} = {total}"
        return str(total)

    @staticmethod
    def _repr_node(node: Any) -> str:
        """Build a string representation of an AST node."""
        node_type = getattr(node, "node_type", "unknown")
        if node_type == "integer":
            return str(node.value)
        if node_type == "dice_pool":
            return f"{node.count}d{node.sides}"
        if node_type == "binary_op":
            op_map = {"add": "+", "sub": "-", "mul": "*", "div": "/"}
            op_str = (
                str(node.operator.value)
                if hasattr(node.operator, "value")
                else str(node.operator)
            )
            symbol = op_map.get(op_str, op_str)
            left = Evaluator._repr_node(node.left)
            right = Evaluator._repr_node(node.right)
            return f"({left} {symbol} {right})"
        if node_type == "unary_op":
            return f"-{Evaluator._repr_node(node.operand)}"
        if node_type == "modifier":
            mod = (
                str(node.modifier_type.value)
                if hasattr(node.modifier_type, "value")
                else str(node.modifier_type)
            )
            return f"{Evaluator._repr_node(node.target)}[{mod}({node.value})]"
        return f"<{node_type}>"

# Feature Specification: dice-evaluator

**Spec ID**: `003-dice-evaluator` | **Branch**: `feat/dice-evaluator`  
**Created**: 2026-02-22  
**Status**: Draft  
**Input**: User description: "Dice Engine: Implement evaluator for parsed dice AST relying on dice-core (dice-evaluator)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Evaluating Standard Dice Rolls (Priority: P1)

As a game mechanics engine, I need to evaluate complex mathematical and dice expressions so that I can compute the final outcome of an attack or event.

**Why this priority**: Without evaluation, the parsed notation is useless. This is the core execution step bridging input to output.

**Independent Test**: Can be tested by providing handcrafted Abstract Syntax Trees (ASTs) directly to the evaluator and checking the numeric outputs.

**Acceptance Scenarios**:

1. **Given** an AST representing "2d6 + 3", **When** evaluated, **Then** it generates two random numbers between 1 and 6 using `dice-core`, adds them, adds 3, and returns the total.
2. **Given** an AST representing "1d20kh1", **When** evaluated, **Then** it rolls two 20-sided dice, keeps the highest, and returns that result.

---

### User Story 2 - Execution Trace Generation (Priority: P2)

As a player viewing a combat log, I want to see exactly how a final number was calculated (e.g., "[4, 6] + 3 = 13") so that I understand the mechanics behind the result.

**Why this priority**: Transparency in tabletop gaming is critical. A black-box calculation causes player friction.

**Independent Test**: Can be tested by asserting that the evaluator's return object includes a step-by-step resolution path matching the requested operations.

**Acceptance Scenarios**:

1. **Given** a complex AST evaluation, **When** requested, **Then** the evaluator outputs a structured trace showing intermediate values, dropped dice, and added modifiers before presenting the final result.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a strongly typed Abstract Syntax Tree (AST) representing a dice expression.
- **FR-002**: System MUST traverse the AST and execute the corresponding mathematical and dice operations.
- **FR-003**: System MUST rely exclusively on `dice-core` for all random number generation during evaluation.
- **FR-004**: System MUST handle standard tabletop dice mechanics including: Keep Highest, Drop Lowest, Reroll, and Exploding dice.
- **FR-005**: System MUST produce a standardized `EvaluationResult` containing the final integer total and an auditable `ExecutionTrace`.

### Key Entities

- **EvaluationResult**: The final container holding the calculated total, the trace, and the associated entropy proofs from `dice-core`.
- **ExecutionTrace**: A structured list of evaluation steps detailing each operation (e.g., "Rolled 2d6 -> [3, 5]").

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Evaluator successfully processes 100% of valid ASTs representing known tabletop mechanics correctly.
- **SC-002**: Evaluation result includes 100% of the raw, unadulterated dice rolls before modifiers were applied.
- **SC-003**: A standard attack expression resolves in under 2 milliseconds.
- **SC-004**: Evaluator throws strictly typed errors upon receiving malformed or mathematically invalid ASTs (e.g., divide by zero).

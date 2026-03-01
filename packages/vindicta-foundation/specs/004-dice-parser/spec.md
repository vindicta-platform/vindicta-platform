# Feature Specification: dice-parser

**Spec ID**: `004-dice-parser` | **Branch**: `feat/dice-parser`  
**Created**: 2026-02-22  
**Status**: Draft  
**Input**: User description: "Dice Engine: Implement parser for dice notation strings into typed AST (dice-parser)"

> [!NOTE]
> This spec was retroactively created during the specs folder refactoring (2026-02-22). The feature was originally planned without running `/speckit-specify` first.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Parse Standard Dice Notation (Priority: P1)

As a game mechanics engine, I need to convert human-readable dice notation strings (e.g., `"2d6 + 3"`, `"4d6dl1"`) into a structured Abstract Syntax Tree so that the evaluator can execute them.

**Why this priority**: Parsing is the entry point for all dice operations. Without it, no notation can be evaluated.

**Independent Test**: Can be fully tested by passing dice notation strings to the parser and asserting the returned AST structure matches expected node types and values.

**Acceptance Scenarios**:

1. **Given** a valid dice notation string `"2d6 + 3"`, **When** parsed, **Then** it produces a BinaryOpNode containing a DicePoolNode(count=2, sides=6) and a LiteralNode(value=3) with operator ADD.
2. **Given** a notation with modifiers `"4d6dl1"`, **When** parsed, **Then** it produces a DropLowestNode wrapping a DicePoolNode(count=4, sides=6) with drop_count=1.
3. **Given** a notation with exploding dice `"1d10e10"`, **When** parsed, **Then** it produces an ExplodingNode wrapping a DicePoolNode(count=1, sides=10) with threshold=10.

---

### User Story 2 - Reject Invalid Notation (Priority: P2)

As a consumer of the parser API, I need clear, typed errors when invalid dice notation is provided so that I can provide meaningful feedback to users.

**Why this priority**: Robust error handling is essential for downstream consumers to differentiate between user input errors and system failures.

**Independent Test**: Can be tested by passing malformed strings and asserting that specific, typed ParseError exceptions are raised with position and context information.

**Acceptance Scenarios**:

1. **Given** an invalid notation `"d"`, **When** parsed, **Then** it raises a ParseError with descriptive context about the missing dice count.
2. **Given** an empty string, **When** parsed, **Then** it raises a ParseError indicating no expression was provided.

---

### Edge Cases

- What happens with extremely large dice counts (e.g., `"999999d6"`)? (Parser should accept; evaluation limits are the evaluator's concern.)
- How does the parser handle nested parentheses `"(2d6 + 3) * 2"`? (Must support arbitrary nesting via grammar.)
- What happens with whitespace variations (e.g., `"2d6+3"` vs `"2d6 + 3"`)? (Parser must handle both.)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST parse standard tabletop dice notation into a typed Abstract Syntax Tree.
- **FR-002**: System MUST support dice pool notation (`NdS` where N is count, S is sides).
- **FR-003**: All AST node models MUST inherit from `VindictaModel`.
- **FR-004**: System MUST provide descriptive, typed error messages for invalid input with position information.
- **FR-005**: System MUST support modifiers: Keep Highest (`kh`), Drop Lowest (`dl`), Reroll (`r`), Exploding (`e`).
- **FR-006**: System MUST support arithmetic operators (`+`, `-`, `*`, `/`) and grouping with parentheses.
- **FR-007**: System MUST produce deterministic AST output for identical input strings.

### Key Entities

- **ASTNode**: Base discriminated union type for all parse tree nodes.
- **DicePoolNode**: Represents `NdS` notation with count and sides.
- **BinaryOpNode**: Represents arithmetic operations between two sub-expressions.
- **LiteralNode**: Represents a constant integer value.
- **ModifierNode** (variants): KeepHighestNode, DropLowestNode, RerollNode, ExplodingNode.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Parser correctly handles 100% of valid standard wargaming dice notation expressions.
- **SC-002**: All AST nodes correctly serialize to and deserialize from JSON via Pydantic.
- **SC-003**: Typical expressions (< 50 characters) parse in under 1 millisecond.
- **SC-004**: Parser achieves ≥95% test coverage with parametrized test cases.

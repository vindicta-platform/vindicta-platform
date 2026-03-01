# Quickstart: dice-parser

**Feature**: dice-parser | **Date**: 2026-02-22

## Installation

The parser is an in-tree module. No extra installation beyond `vindicta-foundation` is required, except for the new `lark` dependency:

```bash
uv add lark
```

## Usage

```python
from vindicta_foundation.parser import parse_dice

# Basic dice notation
result = parse_dice("2d6")
# → DicePoolNode(count=2, sides=6)

# Arithmetic
result = parse_dice("2d6 + 3")
# → BinaryOpNode(operator="add", left=DicePoolNode(2, 6), right=IntegerNode(3))

# Modifiers
result = parse_dice("4d6dl1")
# → ModifierNode(modifier_type="drop_lowest", value=1, target=DicePoolNode(4, 6))

# Complex expression
result = parse_dice("2d6 + 1d8kh1 * 2")
# → BinaryOpNode(
#     operator="add",
#     left=DicePoolNode(2, 6),
#     right=BinaryOpNode(
#       operator="mul",
#       left=ModifierNode(modifier_type="keep_highest", value=1, target=DicePoolNode(1, 8)),
#       right=IntegerNode(2)
#     )
#   )
```

## Serialization

```python
from vindicta_foundation.parser import parse_dice

ast = parse_dice("3d6 + 2")

# To JSON
json_str = ast.model_dump_json(indent=2)

# From JSON — requires the discriminated union wrapper
from vindicta_foundation.models.dice_ast import ASTNodeType
from pydantic import TypeAdapter

adapter = TypeAdapter(ASTNodeType)
restored = adapter.validate_json(json_str)
assert restored == ast
```

## Error Handling

```python
from vindicta_foundation.parser import parse_dice
from vindicta_foundation.parser.errors import ParseError

try:
    parse_dice("2d")  # Missing sides
except ParseError as e:
    print(e)
    # → ParseError: Unexpected end of input at position 2.
    #   Expected: INTEGER
    #   Input: "2d"
```

## Validation Scenarios

| Input             | Expected AST Root                                        | Notes                      |
| ----------------- | -------------------------------------------------------- | -------------------------- |
| `"3d6"`           | `DicePoolNode(3, 6)`                                     | Basic pool                 |
| `"2d6 + 4"`       | `BinaryOpNode(add, DicePoolNode, IntegerNode)`           | Arithmetic                 |
| `"4d6dl1"`        | `ModifierNode(drop_lowest, 1, DicePoolNode)`             | Modifier                   |
| `"1d10e10"`       | `ModifierNode(explode, 10, DicePoolNode)`                | Exploding                  |
| `"2d6 + 1d4 * 3"` | `BinaryOpNode(add, ..., BinaryOpNode(mul, ...))`         | Precedence                 |
| `"(2d6 + 3) * 2"` | `BinaryOpNode(mul, BinaryOpNode(add, ...), IntegerNode)` | Grouping                   |
| `""`              | `ParseError`                                             | Empty input                |
| `"abc"`           | `ParseError`                                             | Invalid tokens             |
| `"2d"`            | `ParseError`                                             | Incomplete dice expression |

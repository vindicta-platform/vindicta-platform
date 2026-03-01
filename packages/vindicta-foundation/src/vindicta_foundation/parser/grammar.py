"""Lark EBNF grammar for dice notation parsing.

Grammar sourced from ``specs/004-dice-parser/contracts/grammar.ebnf``.
Supports basic dice (NdS), arithmetic (+, -, *, /), modifiers
(kh, kl, dh, dl, e), grouping, and unary negation.
"""

DICE_GRAMMAR = r"""
start: expr

// Arithmetic — standard PEMDAS via precedence climbing
?expr: term
     | expr "+" term   -> add
     | expr "-" term   -> sub

?term: factor
     | term "*" factor -> mul
     | term "/" factor -> div

?factor: "+" factor    -> pos
       | "-" factor    -> neg
       | atom

?atom: modified_dice
     | dice
     | INTEGER         -> integer
     | "(" expr ")"

// Dice pool: NdS
dice: INTEGER "d" INTEGER

// Modifiers applied to a dice pool
modified_dice: dice modifier+

?modifier: "kh" INTEGER  -> keep_highest
         | "kl" INTEGER  -> keep_lowest
         | "dh" INTEGER  -> drop_highest
         | "dl" INTEGER  -> drop_lowest
         | "e" INTEGER   -> explode

// Terminals
INTEGER: /[0-9]+/

// Whitespace handling
%import common.WS
%ignore WS
"""

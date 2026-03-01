"""Error types for the dice-parser module."""


class DiceParserError(Exception):
    """Base error for all dice parser failures."""


class ParseError(DiceParserError):
    """Raised when a dice notation string cannot be parsed.

    Wraps Lark's ``UnexpectedInput`` with a stable API surface
    and structured error context (FR-004).
    """

    def __init__(
        self,
        message: str,
        position: int | None = None,
        input_text: str | None = None,
    ) -> None:
        self.position = position
        self.input_text = input_text
        super().__init__(message)


class InvalidDiceNotationError(DiceParserError):
    """Raised when dice notation is syntactically valid but semantically invalid.

    For example, zero-sided dice or negative dice counts.
    """

"""Parser error tests — malformed input handling.

Covers T011 (US1 errors) and T014 (US2 modifier errors).
"""

from __future__ import annotations

import pytest

from vindicta_foundation.parser import parse_dice
from vindicta_foundation.parser.errors import ParseError


class TestMalformedInput:
    """US1: Error cases for standard notation."""

    @pytest.mark.parametrize(
        ("expr", "description"),
        [
            ("", "empty string"),
            ("   ", "whitespace only"),
            ("abc", "non-numeric characters"),
            ("2d", "missing sides"),
            ("d6", "missing count (d6 shorthand not supported)"),
            ("++", "double operator"),
            ("2d6 +", "trailing operator"),
        ],
    )
    def test_parse_error_raised(self, expr: str, description: str) -> None:
        with pytest.raises(ParseError):
            parse_dice(expr)

    def test_error_has_input_text(self) -> None:
        with pytest.raises(ParseError) as exc_info:
            parse_dice("abc")
        assert exc_info.value.input_text == "abc"

    def test_empty_string_has_position(self) -> None:
        with pytest.raises(ParseError) as exc_info:
            parse_dice("")
        assert exc_info.value.position == 0


class TestModifierErrors:
    """US2: Error cases for modifier notation."""

    @pytest.mark.parametrize(
        ("expr", "description"),
        [
            ("4d6kh", "missing modifier value"),
            ("kh3", "modifier without dice"),
        ],
    )
    def test_modifier_error_raised(self, expr: str, description: str) -> None:
        with pytest.raises(ParseError):
            parse_dice(expr)

from decimal import Decimal

import pytest

from toolkit.calculator import calculate, evaluate, tokenize, validate
from toolkit.errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidNumberError,
    InvalidSymbolError,
    MissingOperandError,
    OperatorsInARowError,
    UnexpectedNumberError,
)

Token = Decimal | str


class TestTokenize:
    @pytest.mark.parametrize(
        ("expression", "expected"),
        [
            ("2+3", [Decimal("2.0"), "+", Decimal("3.0")]),
            ("-5+2", [Decimal("-5.0"), "+", Decimal("2.0")]),
            ("2+-3", [Decimal("2.0"), "+", Decimal("-3.0")]),
            ("2.5 * 4", [Decimal("2.5"), "*", Decimal("4.0")]),
        ],
    )
    def test_tokenize(self, expression: str, expected: list[Token]):
        assert tokenize(expression) == expected

    @pytest.mark.parametrize(
        ("expression", "error"),
        [
            ("2+a", InvalidSymbolError),
            ("2#3", InvalidSymbolError),
            (".", InvalidNumberError),
            ("1.2.3", InvalidNumberError),
        ],
    )
    def test_invalid_number_or_symbol(self, expression: str, error: type[Exception]):
        with pytest.raises(error):
            tokenize(expression)

    @pytest.mark.parametrize(
        ("expression"),
        [("2  3 + 1"), ("2 3*5"), ("2 . 5 * 1"), (". 5"), ("+. 5"), ("-. 5")],
    )
    def test_unexpected_number(self, expression: str):
        with pytest.raises(UnexpectedNumberError):
            tokenize(expression)


class TestValidate:
    def test_empty_expression(self):
        with pytest.raises(EmptyExpressionError):
            validate([])

    @pytest.mark.parametrize(
        "tokens",
        [
            ["+", Decimal("2.0")],
            [Decimal("2.0"), "+"],
        ],
    )
    def test_missing_operand(self, tokens: list[Token]):
        with pytest.raises(MissingOperandError):
            validate(tokens)

    @pytest.mark.parametrize(
        "tokens",
        [
            [Decimal("2.0"), "+", "*", Decimal("3.0")],
            [Decimal("2.0"), "/", "-", Decimal("3.0")],
        ],
    )
    def test_two_operators(self, tokens: list[Token]):
        with pytest.raises(OperatorsInARowError):
            validate(tokens)

    @pytest.mark.parametrize(
        "tokens",
        [
            [Decimal("2.0"), Decimal("3.0")],
            [Decimal("2.0"), "+", Decimal("3.0"), Decimal("4.0")],
        ],
    )
    def test_two_numbers(self, tokens: list[Token]):
        with pytest.raises(UnexpectedNumberError):
            validate(tokens)


class TestCalculate:
    @pytest.mark.parametrize(
        ("tokens", "expected"),
        [
            ([Decimal("2.0"), "+", Decimal("3.0")], Decimal("5.0")),
            (
                [Decimal("2.0"), "+", Decimal("3.0"), "*", Decimal("4.0")],
                Decimal("14.0"),
            ),
        ],
    )
    def test_calculate(self, tokens: list[Token], expected: Decimal):
        assert calculate(tokens) == expected

    def test_division_by_zero(self):
        with pytest.raises(DivisionByZeroError):
            calculate([Decimal("10.0"), "/", Decimal("0.0")])


class TestEvaluate:
    @pytest.mark.parametrize(
        ("expression", "expected"),
        [
            ("2+3", Decimal("5.0")),
            ("10-4", Decimal("6.0")),
            ("3*4", Decimal("12.0")),
            ("8/2", Decimal("4.0")),
            # operator precedence
            ("2+3*4", Decimal("14.0")),
            ("2*3+4", Decimal("10.0")),
            ("10-6/2", Decimal("7.0")),
            # multiple operations
            ("2+3*4-8/2", Decimal("10.0")),
            # negative numbers
            ("-5+2", Decimal("-3.0")),
            ("5+-2", Decimal("3.0")),
            ("5--2", Decimal("7.0")),
            ("-2*-3", Decimal("6.0")),
            # fractional numbers
            ("2.5+1.5", Decimal("4.0")),
            ("2.5*2", Decimal("5.0")),
            # spaces
            (" 2 + 3 * 4 ", Decimal("14.0")),
            # one number
            ("42", Decimal("42.0")),
        ],
    )
    def test_evaluate(self, expression: str, expected: float):
        assert evaluate(expression) == expected

    @pytest.mark.parametrize(
        ("expression", "error"),
        [
            ("", EmptyExpressionError),
            (" ", EmptyExpressionError),
            ("2+", MissingOperandError),
            ("*2", MissingOperandError),
            ("2+*3", OperatorsInARowError),
            ("hello", InvalidSymbolError),
        ],
    )
    def test_invalid_expression(self, expression: str, error: type[Exception]):
        with pytest.raises(error):
            evaluate(expression)

    def test_division_by_zero(self):
        with pytest.raises(DivisionByZeroError):
            evaluate("10/0")

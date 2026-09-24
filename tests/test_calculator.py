from decimal import Decimal

import pytest

from toolkit.calculator import calculate, evaluate, tokenize, validate

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
        "expression",
        [
            "2+a",
            "2#3",
            ".",
            "1.2.3",
        ],
    )
    def test_invalid_number_or_symbol(self, expression: str):
        with pytest.raises(ValueError):
            tokenize(expression)


class TestValidate:
    def test_empty_expression(self):
        with pytest.raises(ValueError, match="Empty expression"):
            validate([])

    @pytest.mark.parametrize(
        "tokens",
        [
            ["+", Decimal("2.0")],
            [Decimal("2.0"), "+"],
        ],
    )
    def test_missing_operand(self, tokens: list[Token]):
        with pytest.raises(ValueError, match="Missing operand"):
            validate(tokens)

    @pytest.mark.parametrize(
        "tokens",
        [
            [Decimal("2.0"), "+", "*", Decimal("3.0")],
            [Decimal("2.0"), "/", "-", Decimal("3.0")],
        ],
    )
    def test_two_operators(self, tokens: list[Token]):
        with pytest.raises(ValueError, match="Two operators in a row"):
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
        with pytest.raises(ZeroDivisionError, match="Division by zero"):
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
        "expression",
        [
            "",
            " ",
            "2+",
            "*2",
            "2+*3",
            "hello",
        ],
    )
    def test_invalid_expression(self, expression: str):
        with pytest.raises(ValueError):
            evaluate(expression)

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError, match="Division by zero"):
            evaluate("10/0")

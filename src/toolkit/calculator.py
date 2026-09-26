from decimal import ROUND_HALF_UP, Decimal, InvalidOperation, localcontext

from .constants import OPERATORS
from .errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidNumberError,
    InvalidSymbolError,
    MissingOperandError,
    OperatorsInARowError,
    UnexpectedNumberError,
)

PRECISION = 28
ROUNDING = ROUND_HALF_UP

Token = Decimal | str


def _parse_number(number: str) -> Decimal:
    """Parse a number string into a Decimal."""
    if number in "+-":
        raise MissingOperandError()
    try:
        return Decimal(number)
    except InvalidOperation:
        raise InvalidNumberError(number)


def tokenize(expression: str) -> list[Token]:
    """Split an expression into numbers and operators."""
    tokens: list[Token] = []
    number = ""

    for char in expression:
        if char.isspace():
            if number not in ("", "+", "-"):
                if any(digit.isdigit() for digit in number):
                    tokens.append(_parse_number(number))
                    number = ""
                else:
                    raise UnexpectedNumberError()
            continue

        unary = (
            char in "+-" and not number and (not tokens or isinstance(tokens[-1], str))
        )
        if unary:
            number = char
            continue

        if (
            (char.isdigit() or char == ".")
            and not number
            and tokens
            and isinstance(tokens[-1], Decimal)
        ):
            raise UnexpectedNumberError()

        if char.isdigit() or char == ".":
            number += char
        elif char in OPERATORS:
            if number:
                tokens.append(_parse_number(number))
                number = ""
            tokens.append(char)
        else:
            raise InvalidSymbolError(char)

    if number:
        tokens.append(_parse_number(number))

    return tokens


def _is_operator(token: Token) -> bool:
    """Return whether a token is an arithmetic operator."""
    return isinstance(token, str) and token in OPERATORS


def validate(tokens: list[Token]) -> None:
    """Reject a token list that is not a valid expression."""
    if not tokens:
        raise EmptyExpressionError()

    if _is_operator(tokens[0]):
        raise MissingOperandError()

    if _is_operator(tokens[-1]):
        raise MissingOperandError()

    for i in range(len(tokens) - 1):
        if _is_operator(tokens[i]) and _is_operator(tokens[i + 1]):
            raise OperatorsInARowError()
        if isinstance(tokens[i], Decimal) and isinstance(tokens[i + 1], Decimal):
            raise UnexpectedNumberError()


def _number(token: Token) -> Decimal:
    """Return the token when it is a Decimal."""
    if isinstance(token, Decimal):
        return token
    raise TypeError(f"Expected a number, got {token!r}")


def calculate(tokens: list[Token]) -> Decimal:
    """Calculate the value of a token list."""
    with localcontext() as context:
        context.prec = PRECISION
        context.rounding = ROUNDING

        new_tokens: list[Token] = [_number(tokens[0])]

        i = 1
        while i < len(tokens):
            operator = tokens[i]
            number = _number(tokens[i + 1])

            if operator == "*":
                new_tokens[-1] = _number(new_tokens[-1]) * number

            elif operator == "/":
                if number == 0:
                    raise DivisionByZeroError()
                new_tokens[-1] = _number(new_tokens[-1]) / number

            else:
                new_tokens.append(operator)
                new_tokens.append(number)

            i += 2

        result = _number(new_tokens[0])

        i = 1
        while i < len(new_tokens):
            operator = new_tokens[i]
            number = _number(new_tokens[i + 1])

            if operator == "+":
                result += number
            elif operator == "-":
                result -= number

            i += 2

        return result


def evaluate(expression: str) -> Decimal:
    """Evaluate an arithmetic expression."""
    tokens = tokenize(expression)
    validate(tokens)
    return calculate(tokens)

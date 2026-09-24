from decimal import ROUND_HALF_UP, Decimal, InvalidOperation, localcontext

from .constants import OPERATORS

PRECISION = 28
ROUNDING = ROUND_HALF_UP

Token = Decimal | str


def _parse_number(number: str) -> Decimal:
    if number in "+-":
        raise ValueError("Missing operand")
    try:
        return Decimal(number)
    except InvalidOperation:
        raise ValueError(f"Invalid number: {number}")


def tokenize(expression: str) -> list[Token]:
    tokens: list[Token] = []
    number = ""

    for char in expression:
        if char.isspace():
            continue

        unary = (
            char in "+-" and not number and (not tokens or isinstance(tokens[-1], str))
        )
        if unary:
            number = char
            continue

        if char.isdigit() or char == ".":
            number += char
        elif char in OPERATORS:
            if number:
                tokens.append(_parse_number(number))
                number = ""
            tokens.append(char)
        else:
            raise ValueError(f"Invalid symbol: {char}")

    if number:
        tokens.append(_parse_number(number))

    return tokens


def _is_operator(token: Token) -> bool:
    return isinstance(token, str) and token in OPERATORS


def validate(tokens: list[Token]) -> None:
    if not tokens:
        raise ValueError("Empty expression")

    if _is_operator(tokens[0]):
        raise ValueError("Missing operand")

    if _is_operator(tokens[-1]):
        raise ValueError("Missing operand")

    for i in range(len(tokens) - 1):
        if _is_operator(tokens[i]) and _is_operator(tokens[i + 1]):
            raise ValueError("Two operators in a row")


def _number(token: Token) -> Decimal:
    if isinstance(token, Decimal):
        return token
    raise TypeError(f"Expected a number, got {token!r}")


def calculate(tokens: list[Token]) -> Decimal:
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
                    raise ZeroDivisionError("Division by zero")
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
    tokens = tokenize(expression)
    validate(tokens)
    return calculate(tokens)

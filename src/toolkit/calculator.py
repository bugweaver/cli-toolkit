from .constants import OPERATORS


def tokenize(expression: str) -> list[float | str]:
    tokens: list[float | str] = []
    number = ""

    for char in expression:
        if char.isspace():
            continue
        if char.isdigit() or char == ".":
            number += char
        elif char in OPERATORS:
            if number:
                tokens.append(float(number))
                number = ""
            tokens.append(char)
        else:
            raise ValueError(f"Invalid symbol: {char}")

    if number:
        tokens.append(float(number))

    return tokens


def _is_operator(token: float | str) -> bool:
    return isinstance(token, str) and token in OPERATORS


def validate(tokens: list[float | str]) -> None:
    if not tokens:
        raise ValueError("Empty expression")

    if _is_operator(tokens[-1]):
        raise ValueError("Missing operand")

    for i in range(len(tokens) - 1):
        if _is_operator(tokens[i]) and _is_operator(tokens[i + 1]):
            raise ValueError("Two operators in a row")


def _number(token: float | str) -> float:
    if isinstance(token, float):
        return token
    raise TypeError(f"Expected a number, got {token!r}")


def calculate(tokens: list[float | str]) -> float:
    new_tokens: list[float | str] = [_number(tokens[0])]

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


def evaluate(expression: str) -> float:
    tokens = tokenize(expression)
    return calculate(tokens)

class ToolkitError(Exception):
    """Base error for toolkit commands."""


class CalculatorError(ToolkitError, ValueError):
    """Invalid expression or calculation."""


class EmptyExpressionError(CalculatorError):
    """The expression is empty."""

    def __init__(self) -> None:
        super().__init__("Empty expression")


class MissingOperandError(CalculatorError):
    """An operand is missing."""

    def __init__(self) -> None:
        super().__init__("Missing operand")


class InvalidNumberError(CalculatorError):
    """A number cannot be parsed."""

    def __init__(self, number: str) -> None:
        super().__init__(f"Invalid number: {number}")


class InvalidSymbolError(CalculatorError):
    """The expression contains an unsupported symbol."""

    def __init__(self, symbol: str) -> None:
        super().__init__(f"Invalid symbol: {symbol}")


class OperatorsInARowError(CalculatorError):
    """Two operators appear in a row."""

    def __init__(self) -> None:
        super().__init__("Two operators in a row")


class UnexpectedNumberError(CalculatorError):
    """A number follows another number without an operator."""

    def __init__(self) -> None:
        super().__init__("Unexpected number")


class DivisionByZeroError(ToolkitError, ZeroDivisionError):
    """Division by zero."""

    def __init__(self) -> None:
        super().__init__("Division by zero")


class ConverterError(ToolkitError, ValueError):
    """Unit conversion failed."""


class UnknownUnitError(ConverterError):
    """The unit is not recognized."""

    def __init__(self, unit: str) -> None:
        super().__init__(f"Unknown unit: {unit}")


class IncompatibleUnitsError(ConverterError):
    """The units belong to different groups."""

    def __init__(self, source: str, target: str) -> None:
        super().__init__(f"Incompatible units: {source} and {target}")


class TemperatureBelowAbsoluteZeroError(ConverterError):
    """The temperature is below absolute zero."""

    def __init__(self) -> None:
        super().__init__("Temperature below absolute zero")

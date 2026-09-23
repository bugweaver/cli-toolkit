OPERATORS: str = "+-*/"

LENGTH_TO_METERS: dict[str, float] = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

MASS_TO_GRAMS: dict[str, float] = {
    "g": 1.0,
    "kg": 1000.0,
}

TEMPERATURE_UNITS: set[str] = {"c", "f", "k"}

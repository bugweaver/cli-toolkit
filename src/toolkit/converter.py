from .constants import LENGTH_TO_METERS, MASS_TO_GRAMS, TEMPERATURE_UNITS
from .errors import (
    IncompatibleUnitsError,
    TemperatureBelowAbsoluteZeroError,
    UnknownUnitError,
)


def _to_kelvin(value: float, unit: str) -> float:
    """Convert a temperature to kelvin."""
    if unit == "c":
        return value + 273.15
    if unit == "f":
        return (value - 32) * 5 / 9 + 273.15

    return value


def _from_kelvin(value: float, unit: str) -> float:
    """Convert a kelvin value to the given unit."""
    if unit == "c":
        return value - 273.15

    if unit == "f":
        return (value - 273.15) * 9 / 5 + 32

    return value


def _group(unit: str) -> str:
    """Return the group that contains the unit."""
    if unit in LENGTH_TO_METERS:
        return "length"
    if unit in MASS_TO_GRAMS:
        return "mass"
    if unit in TEMPERATURE_UNITS:
        return "temperature"
    raise UnknownUnitError(unit)


def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a value between units of the same group."""
    source = from_unit.lower()
    target = to_unit.lower()
    source_group = _group(source)
    target_group = _group(target)

    if source_group != target_group:
        raise IncompatibleUnitsError(source, target)

    if source_group == "length":
        meters = value * LENGTH_TO_METERS[source]
        return meters / LENGTH_TO_METERS[target]

    if source_group == "mass":
        grams = value * MASS_TO_GRAMS[source]
        return grams / MASS_TO_GRAMS[target]

    kelvin = _to_kelvin(value, source)
    if kelvin < 0:
        raise TemperatureBelowAbsoluteZeroError()

    return _from_kelvin(kelvin, target)

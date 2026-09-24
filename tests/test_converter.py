import pytest

from toolkit.converter import convert_units


class TestConvertUnits:
    @pytest.mark.parametrize(
        ("value", "from_unit", "to_unit", "expected"),
        [
            # length
            (1000.0, "mm", "m", 1.0),
            (250, "cm", "m", 2.5),
            (2.0, "km", "m", 2000.0),
            # mass
            (1000, "g", "kg", 1.0),
            (2.5, "kg", "g", 2500.0),
            # temperature
            (0.0, "c", "f", 32.0),
            (100, "c", "k", 373.15),
            (32.0, "f", "c", 0.0),
            (273.15, "k", "c", 0.0),
        ],
    )
    def test_convert_units(
        self, value: float, from_unit: str, to_unit: str, expected: float
    ):
        # может использовать math.isclose?
        assert convert_units(value, from_unit, to_unit) == pytest.approx(expected)  # pyright: ignore

    def test_ignores_unit_case(self):
        assert convert_units(1, "KM", "M") == 1000.0

    def test_rejects_unknown_unit(self):
        with pytest.raises(ValueError, match="Unknown unit"):
            convert_units(1, "unknown", "m")

    def test_rejects_incompatible_units(self):
        with pytest.raises(ValueError, match="Incompatible units"):
            convert_units(1, "m", "kg")

    @pytest.mark.parametrize(
        ("value", "unit"),
        [
            (-273.16, "c"),
            (-500.0, "f"),
            (-1.0, "k"),
        ],
    )
    def test_rejects_temperature_below_absolute_zero(
        self,
        value: float,
        unit: str,
    ):
        with pytest.raises(ValueError, match="Temperature below absolute zero"):
            convert_units(value, unit, "k")

    def test_allows_absolute_zero(self):
        assert convert_units(-273.15, "c", "k") == pytest.approx(0.0) # pyright: ignore

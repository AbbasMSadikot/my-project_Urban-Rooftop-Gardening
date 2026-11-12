"""Property-based fuzz tests for all three solar estimate input parsers."""

from hypothesis import given, settings, strategies as st

from solar_panel_estimate_parser import (
    clean_site_name,
    panels_for_roof,
    parse_monthly_units,
)


FUZZ_SETTINGS = settings(max_examples=200, deadline=None)


@FUZZ_SETTINGS
@given(st.one_of(st.text(), st.none()))
def test_clean_site_name_handles_arbitrary_input(value):
    try:
        clean_site_name(value)
    except Exception as error:
        raise AssertionError(f"clean_site_name crashed for {value!r}: {error}") from error


@FUZZ_SETTINGS
@given(st.one_of(st.text(), st.none()))
def test_parse_monthly_units_handles_arbitrary_input(value):
    try:
        parse_monthly_units(value)
    except Exception as error:
        raise AssertionError(f"parse_monthly_units crashed for {value!r}: {error}") from error


@FUZZ_SETTINGS
@given(st.one_of(st.text(), st.none()))
def test_panels_for_roof_handles_arbitrary_input(value):
    try:
        panels_for_roof(value)
    except Exception as error:
        raise AssertionError(f"panels_for_roof crashed for {value!r}: {error}") from error


@FUZZ_SETTINGS
@given(st.text())
def test_clean_site_name_returns_a_string(value):
    result = clean_site_name(value)
    assert isinstance(result, str)
    assert result == result.strip()
    assert "#" not in result
    assert "@" not in result


@FUZZ_SETTINGS
@given(st.integers(min_value=0, max_value=10**12))
def test_monthly_units_parse_valid_kwh_readings(units):
    assert parse_monthly_units(f"{units} kWh") == units


@FUZZ_SETTINGS
@given(
    st.integers(min_value=1, max_value=10000),
    st.integers(min_value=1, max_value=10000),
)
def test_roof_panel_count_is_area_divided_by_panel_area(length, width):
    assert panels_for_roof(f"{length}ft x {width}ft") == (length * width) // 18

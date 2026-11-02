"""Code coverage tests for the assigned solar panel estimate application."""

import pytest

from solar_panel_estimate import install_cost, panels_needed, payback_years


def test_panels_needed_exact_calculation_and_panel_types():
    assert panels_needed(300, "mono", 5) == 5
    assert panels_needed(300, "poly", 5) == 7


def test_panels_needed_rounding_and_minimum_system_size():
    assert panels_needed(1, "mono", 5) == 2
    assert panels_needed(60, "mono", 5) == 2


def test_panels_needed_rejects_unknown_type_and_invalid_inputs():
    with pytest.raises(ValueError, match="unknown panel type"):
        panels_needed(300, "thin-film", 5)
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(0, "mono", 5)
    with pytest.raises(ValueError, match="invalid input"):
        panels_needed(300, "mono", 0)


def test_install_cost_for_each_roof_type_and_battery():
    assert install_cost(4, "tin", False) == 108000
    assert install_cost(4, "tiled", True) == 168000
    assert install_cost(4, "concrete", False) == 100000


def test_install_cost_discount_and_validation():
    assert install_cost(10, "concrete", True) == 279000
    with pytest.raises(ValueError, match="invalid panel count"):
        install_cost(0, "concrete", False)
    with pytest.raises(ValueError, match="unknown roof type"):
        install_cost(4, "wood", False)


def test_payback_for_nonpositive_savings_and_capped_subsidy():
    assert payback_years(100000, 20, 0) == -1
    assert payback_years(100000, 50, 500) == 10


def test_payback_rounds_up_and_handles_exact_year():
    assert payback_years(1200, 20, 100) == 1
    assert payback_years(1200, 0, 100) == 1

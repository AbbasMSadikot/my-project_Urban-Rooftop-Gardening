"""Branch coverage tests for alternate solar estimate decision paths."""

from CodeCoverageTest_solar_panel_estimate import *  # noqa: F401,F403

from solar_panel_estimate import install_cost, panels_needed, payback_years


def test_each_panel_validation_branch():
    for monthly_units, sun_hours in ((0, 5), (300, 0)):
        try:
            panels_needed(monthly_units, "mono", sun_hours)
        except ValueError as error:
            assert str(error) == "invalid input"
        else:
            raise AssertionError("invalid sizing input should fail")


def test_cost_discount_threshold_and_battery_branches():
    assert install_cost(9, "concrete", False) == 225000
    assert install_cost(10, "concrete", False) == 225000


def test_payback_subsidy_cap_and_saving_branches():
    assert payback_years(1200, 40, 100) == 1
    assert payback_years(1200, 41, 100) == 1
    assert payback_years(1200, 0, -1) == -1

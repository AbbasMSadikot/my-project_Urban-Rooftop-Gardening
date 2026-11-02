# Lab 6: Code and Branch Coverage

This Lab 6 submission tests the Solar Panel Estimate application assigned in [SETAPESU26/L6_L7_65_solar_panel_estimate](https://github.com/SETAPESU26/L6_L7_65_solar_panel_estimate). A copy of `solar_panel_estimate.py` is included here so the tests and reports are self-contained; the assigned repository was not modified.

## Setup

Use Python 3.10 or newer. From `Lab-6/solar-panel-estimate/`:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

## Code coverage

```sh
coverage erase
coverage run --source=solar_panel_estimate -m pytest -q CodeCoverageTest_solar_panel_estimate.py
coverage report -m
```

Result: **100% code coverage**, 7 tests passed.

## Branch coverage

```sh
coverage erase
coverage run --branch --source=solar_panel_estimate -m pytest -q BranchCoverageTest_solar_panel_estimate.py
coverage report -m
```

Result: **100% branch coverage**, 10 tests passed (26 of 26 branches).

The terminal output is saved in `reports/`; the corresponding PNG evidence is in `screenshots/`.

# Lab 7: Fuzzing for Input Validation Bugs

This submission completes the Solar Panel Estimate parser exercise assigned in [`SETAPESU26/L6_L7_65_solar_panel_estimate`](https://github.com/SETAPESU26/L6_L7_65_solar_panel_estimate/tree/main/LAB7).

## What changed

- Added Hypothesis tests for arbitrary inputs to all three parser functions and properties for valid inputs.
- Hardened site-name cleanup, monthly kWh parsing, and roof panel calculations against malformed values.
- Recorded the buggy run, failing fuzz tests, fixed run, and passing tests in `AbbasMSadikot_LAB7.pdf`.

## Run

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python solar_panel_estimate_parser.py
python -m pytest -q test_solar_panel_estimate_parser.py
```

The test suite uses 200 Hypothesis examples per property test. All six tests pass on the fixed module. The PDF contains four command-output screenshots and answers to the handout reflection questions.

The four PNG output captures are also available in `screenshots/` for separate review.

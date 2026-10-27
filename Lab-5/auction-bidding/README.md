# Lab 5: Static Code Analysis

This folder contains the auction bidding program, the issue table, reflection, and reports captured before and after the fixes.

## Run the program

Python 3.10 or newer is recommended.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python auction_system.py
```

## Reproduce the analysis

Install the analysis tools in the active environment:

```sh
python -m pip install pylint bandit flake8
```

Run each tool from this directory:

```sh
python -m pylint auction_system.py > reports/pylint_report.txt
python -m bandit -r auction_system.py > reports/bandit_report.txt
python -m flake8 auction_system.py > reports/flake8_report.txt
```

The captured reports are separated into `reports/before/` and `reports/after/`. Tool versions used: Pylint 3.3.9, Bandit 1.8.6, Flake8 7.3.0.

## Results

- Pylint: 5.75/10 before; 10.00/10 after.
- Bandit: two high and one medium finding before; no findings after.
- Flake8: formatting findings before; no findings after.

See `issues.md` for the findings and fixes. The attached handout refers to four reflection answers but does not provide the question prompts; `reflection.md` answers four questions based on the handout's stated learning outcomes.

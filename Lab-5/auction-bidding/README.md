# Lab 5: Static Code Analysis

This folder contains the auction program from the assigned starter repository and the original demo and static-analysis output captured before fixes.

## Setup and run

Use Python 3.10 or newer. The starter imports Jinja2.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python auction_system.py
```

## Analyze

Install the tools and run them from this directory:

```sh
python -m pip install pylint bandit flake8
python -m pylint auction_system.py > reports/pylint_report.txt
python -m bandit -r auction_system.py > reports/bandit_report.txt
python -m flake8 auction_system.py > reports/flake8_report.txt
```

Initial analyzer reports and demo output are preserved in `reports/before/`. The fixed version and after reports are added in the following commits.

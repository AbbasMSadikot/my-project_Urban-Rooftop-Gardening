# Lab 6: Code and Branch Coverage

Coverage tests for the Snake application already in `Lab-4/snake-game/`. The tests target the app's `main.py` and the `game/` modules without copying or modifying the Lab 4 application.

## Setup

Run these commands from the repository root with Python 3.10 or newer:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r Lab-6/snake-game/requirements.txt
```

The tests set SDL's dummy video and audio drivers so Pygame can run headlessly.

## Code coverage

```sh
coverage erase
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy coverage run --source=game,main -m pytest -q Lab-6/snake-game/CodeCoverageTest_snake_application.py
coverage report -m
```

## Branch coverage

```sh
coverage erase
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy coverage run --branch --source=game,main -m pytest -q Lab-6/snake-game/BranchCoverageTest_snake_application.py
coverage report -m
```

## Results

- Code coverage: **99%** overall (8 tests passed).
- Branch coverage: **99%** overall (11 tests passed).
- Terminal output images and text reports are in `snake-game/screenshots/` and `snake-game/reports/`.

The main entry point's `if __name__ == "__main__"` guard is not executed when the test suite imports the application, so it remains outside the measured lines. Overall coverage is above the handout's 90% target.

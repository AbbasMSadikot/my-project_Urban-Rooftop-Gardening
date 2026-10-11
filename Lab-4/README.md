# Lab 4 — Vibe Coding Submission

**Student:** Abbas M Sadikot  
**Project:** Snake Game (Pygame)  
**Source Repo:** [SETAPESU26/45_snake](https://github.com/SETAPESU26/45_snake)

---

## Submission Checklist

- [x] **Before video** — `submission/before vibe coding.mov` (~10s) showing the original broken behavior (instant death on reverse key, no game-over screen)
- [x] **After video** — `submission/after vibe coding.mov` (~10s) showing all fixes and new features working
- [x] **LLM Chat link** — Antigravity (Google DeepMind) used as AI pair-programming assistant

---

## Changes Made (Tasks Completed)

### Task 1 — Collision Detection Fix (`snake-game/game/snake.py`)
- `set_direction()` now blocks 180° direction reversals — pressing the opposite direction key no longer instantly kills the snake.

### Task 2 — Game Over Screen (`snake-game/game/game_engine.py`)
- A semi-transparent overlay is displayed on game over showing **"GAME OVER"** and the **Final Score** instead of just printing to the console.

### Task 3 — Replay with Difficulty Selection (`snake-game/game/game_engine.py`)
- After Game Over, press **R / Enter** to reach the difficulty menu.
- Choose **Easy**, **Medium**, or **Hard** speed with arrow keys, then press Enter to restart.
- Press **Esc / Q** to quit.

### Task 4 — Sound Feedback (`snake-game/game/game_engine.py`)
- Programmatically generated beep sounds using `numpy` — no audio files needed.
- 🎵 High-pitched beep on food eaten.
- 💀 Low drone on game over.

---

## Folder Structure

```
Lab-4/
├── README.md                     ← this file
├── snake-game/                   ← full game source code
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   └── game/
│       ├── snake.py
│       ├── food.py
│       └── game_engine.py
└── submission/
    ├── before vibe coding.mov    ← 10s video BEFORE changes
    └── after vibe coding.mov     ← 10s video AFTER changes
```

---

## How to Run

```bash
cd snake-game
pip install -r requirements.txt
python main.py
```

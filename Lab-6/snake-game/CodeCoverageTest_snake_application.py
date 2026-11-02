"""Line-coverage tests for the existing Snake game application."""

import os
from pathlib import Path
import sys
from unittest.mock import Mock

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

APP_ROOT = Path(__file__).resolve().parents[2] / "Lab-4" / "snake-game"
sys.path.insert(0, str(APP_ROOT))

import pygame
import pytest

import main
from game.food import Food
from game.game_engine import DIFFICULTIES, GameEngine
from game.snake import Snake


@pytest.fixture(scope="session", autouse=True)
def pygame_session():
    """Initialize SDL with dummy drivers for headless test execution."""
    pygame.init()
    pygame.display.set_mode((600, 600))
    yield
    pygame.quit()


def make_engine(moves_per_second=9):
    """Return an initialized engine and a drawing surface."""
    return GameEngine(200, 200, moves_per_second), pygame.Surface((200, 200))


def test_snake_direction_movement_growth_and_collision():
    snake = Snake(5, 5, 20)
    original = snake.direction
    snake.set_direction(-1, 0)
    assert snake.direction == original
    snake.set_direction(0, -1)
    assert snake.direction == (0, -1)
    snake.move()
    assert snake.body[0] == (5, 4)
    assert not snake.grow_pending
    snake.grow()
    before = len(snake.body)
    snake.move()
    assert len(snake.body) == before + 1
    assert not snake.grow_pending
    assert snake.head_rect().topleft == (100, 60)
    assert len(snake.segment_rects()) == len(snake.body)
    assert not snake.collides_with_self()
    snake.body.insert(1, snake.body[0])
    assert snake.collides_with_self()
    assert not snake.collides_with_wall(10, 10)
    snake.body[0] = (-1, 5)
    assert snake.collides_with_wall(10, 10)
    snake.body = [(1, 1)]
    snake.set_direction(0, 1)
    assert snake.direction == (0, 1)


def test_food_respawns_away_from_occupied_cells(monkeypatch):
    values = iter((1, 1, 2, 2, 3, 3))
    monkeypatch.setattr("game.food.random.randint", lambda _low, _high: next(values))
    food = Food(8, 8, 20)
    assert (food.x, food.y) == (1, 1)
    food.respawn([(2, 2)])
    assert (food.x, food.y) == (3, 3)
    assert food.rect().topleft == (60, 60)


def test_engine_initialization_key_controls_and_noop_input():
    engine, _ = make_engine()
    engine.handle_keydown(pygame.K_UP)
    assert engine.snake.direction == (0, -1)
    engine.handle_keydown(pygame.K_a)
    assert engine.snake.direction == (-1, 0)
    engine.handle_keydown(pygame.K_s)
    assert engine.snake.direction == (0, 1)
    engine.handle_keydown(pygame.K_RIGHT)
    assert engine.snake.direction == (1, 0)
    engine.handle_keydown(pygame.K_x)
    engine.handle_input()
    assert engine.state == "playing"
    assert engine.score == 0
    assert DIFFICULTIES == {"Easy": 5, "Medium": 9, "Hard": 15}


def test_engine_game_over_and_menu_keys(monkeypatch):
    engine, _ = make_engine()
    engine.state = "game_over"
    engine.handle_keydown(pygame.K_x)
    assert engine.state == "game_over"
    engine.handle_keydown(pygame.K_r)
    assert engine.state == "menu"
    engine.handle_keydown(pygame.K_UP)
    assert engine._menu_cursor == 0
    engine.handle_keydown(pygame.K_DOWN)
    assert engine._menu_cursor == 1
    engine.handle_keydown(pygame.K_s)
    assert engine._menu_cursor == 2
    engine.handle_keydown(pygame.K_w)
    assert engine._menu_cursor == 1
    engine.handle_keydown(pygame.K_x)
    assert engine._menu_cursor == 1
    engine.handle_keydown(pygame.K_RETURN)
    assert engine.moves_per_second == DIFFICULTIES["Medium"]
    assert engine.state == "playing"
    engine.state = "menu"
    engine._menu_cursor = 0
    engine.handle_keydown(pygame.K_SPACE)
    assert engine.moves_per_second == DIFFICULTIES["Easy"]
    engine.state = "menu"
    engine._menu_cursor = 2
    engine.handle_keydown(pygame.K_RETURN)
    assert engine.moves_per_second == DIFFICULTIES["Hard"]
    post = Mock()
    monkeypatch.setattr(pygame.event, "post", post)
    engine.state = "menu"
    engine.handle_keydown(pygame.K_ESCAPE)
    post.assert_called_once()
    engine.state = "menu"
    engine.handle_keydown(pygame.K_q)
    assert post.call_count == 2


def test_engine_update_waits_moves_and_handles_food(monkeypatch):
    engine, _ = make_engine(moves_per_second=60)
    engine.state = "menu"
    engine.update()
    assert engine._frame_counter == 0
    engine.state = "playing"
    engine._frame_counter = 0
    original_move = engine.snake.move
    moves = Mock(wraps=original_move)
    monkeypatch.setattr(engine.snake, "move", moves)
    engine.update()
    moves.assert_called_once()
    assert engine._frame_counter == 0

    engine, _ = make_engine(moves_per_second=60)
    engine.food.rect = lambda: engine.snake.head_rect()
    eat_sound = Mock()
    engine._sound_eat = eat_sound
    engine._sound_gameover = Mock()
    engine.update()
    assert engine.score == 1
    assert engine.snake.grow_pending
    eat_sound.play.assert_called_once()


def test_engine_update_handles_wall_and_self_collisions():
    engine, _ = make_engine(moves_per_second=60)
    engine._sound_gameover = Mock()
    engine.snake.move = lambda: engine.snake.body.__setitem__(0, (-1, 2))
    engine.update()
    assert engine.state == "game_over"
    engine._sound_gameover.play.assert_called_once()

    engine, _ = make_engine(moves_per_second=60)
    engine._sound_gameover = Mock()
    engine.snake.move = lambda: engine.snake.body.__setitem__(0, engine.snake.body[1])
    engine.update()
    assert engine.state == "game_over"
    engine._sound_gameover.play.assert_called_once()


def test_engine_render_states_and_empty_snake():
    engine, surface = make_engine()
    engine.render(surface)
    engine.state = "game_over"
    engine.render(surface)
    engine.state = "menu"
    engine.render(surface)
    engine.state = "playing"
    engine.snake.body = []
    engine.render(surface)


def test_main_loop_handles_key_and_quit_events(monkeypatch):
    key_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
    quit_event = pygame.event.Event(pygame.QUIT)
    monkeypatch.setattr(pygame.event, "get", lambda: [key_event, quit_event])
    screen = Mock()
    engine = Mock()
    clock = Mock()
    monkeypatch.setattr(main, "SCREEN", screen)
    monkeypatch.setattr(main, "engine", engine)
    monkeypatch.setattr(main, "clock", clock)
    monkeypatch.setattr(pygame.display, "flip", Mock())
    quit_game = Mock()
    monkeypatch.setattr(pygame, "quit", quit_game)
    main.main()
    engine.handle_keydown.assert_called_once_with(pygame.K_UP)
    engine.handle_input.assert_called_once()
    engine.update.assert_called_once()
    engine.render.assert_called_once_with(screen)
    quit_game.assert_called_once()

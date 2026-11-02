"""Branch-coverage tests built on the line-coverage suite plus edge paths."""

from CodeCoverageTest_snake_application import *  # noqa: F401,F403


def test_engine_update_waiting_and_noncollision_paths():
    engine, _ = make_engine(moves_per_second=9)
    engine.update()
    assert engine._frame_counter == 1
    assert engine.score == 0

    engine.moves_per_second = 120
    engine.food.rect = lambda: pygame.Rect(0, 0, 20, 20)
    engine.update()
    assert engine._frame_counter == 0
    assert engine.score == 0
    assert engine.state == "playing"


def test_each_wall_boundary_is_a_game_over_path():
    for position in ((-1, 3), (3, -1), (10, 3), (3, 10)):
        snake = Snake(*position, 20)
        assert snake.collides_with_wall(10, 10)


def test_return_and_space_replay_from_game_over():
    for key in (pygame.K_RETURN, pygame.K_SPACE):
        engine, _ = make_engine()
        engine.state = "game_over"
        engine.handle_keydown(key)
        assert engine.state == "menu"

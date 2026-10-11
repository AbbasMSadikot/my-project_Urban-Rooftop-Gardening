import pygame
import numpy
from .snake import Snake
from .food import Food

# Game Engine

WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
GREEN      = (0,   200, 0  )
DARK_GREEN = (0,   140, 0  )
RED        = (220, 60,  60 )
YELLOW     = (255, 220, 0  )
GREY       = (180, 180, 180)
DARK_GREY  = (50,  50,  50 )

# Difficulty presets: name -> moves per second
DIFFICULTIES = {
    "Easy":   5,
    "Medium": 9,
    "Hard":   15,
}


def _make_beep(frequency: int, duration_ms: int, volume: float = 0.4) -> pygame.mixer.Sound:
    """Generate a simple sine-wave beep as a pygame Sound object."""
    sample_rate = 44100
    n_samples   = int(sample_rate * duration_ms / 1000)
    t           = numpy.linspace(0, duration_ms / 1000, n_samples, endpoint=False)
    wave        = (numpy.sin(2 * numpy.pi * frequency * t) * volume * 32767).astype(numpy.int16)
    # pygame Sound expects stereo (two channels) by default when mixer is stereo
    stereo      = numpy.column_stack((wave, wave))
    sound       = pygame.sndarray.make_sound(stereo)
    return sound


class GameEngine:
    def __init__(self, width, height, moves_per_second: int = 9):
        self.width       = width
        self.height      = height
        self.cell_size   = 20
        self.grid_width  = width  // self.cell_size
        self.grid_height = height // self.cell_size

        self.moves_per_second = moves_per_second
        self._frame_counter   = 0

        self.score     = 0
        self.font      = pygame.font.SysFont("Arial", 30)
        self.big_font  = pygame.font.SysFont("Arial", 52, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 34)

        # States: "playing", "game_over", "menu"
        self.state = "playing"

        # Task 4: sounds (generated programmatically — no audio files needed)
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self._sound_eat      = _make_beep(880,  80,  volume=0.4)
        self._sound_gameover = _make_beep(220, 500,  volume=0.5)

        self._init_round()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _init_round(self):
        """Reset snake and food for a fresh round."""
        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food  = Food(self.grid_width, self.grid_height, self.cell_size)
        self.score = 0
        self._frame_counter = 0
        self.state = "playing"

        # Menu cursor: 0=Easy, 1=Medium, 2=Hard
        self._menu_cursor = 1  # default Medium

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def handle_keydown(self, key):
        if self.state == "playing":
            # Direction input
            if key in (pygame.K_UP, pygame.K_w):
                self.snake.set_direction(0, -1)
            elif key in (pygame.K_DOWN, pygame.K_s):
                self.snake.set_direction(0, 1)
            elif key in (pygame.K_LEFT, pygame.K_a):
                self.snake.set_direction(-1, 0)
            elif key in (pygame.K_RIGHT, pygame.K_d):
                self.snake.set_direction(1, 0)

        elif self.state == "game_over":
            # Any key takes us to the difficulty menu
            if key == pygame.K_RETURN or key == pygame.K_SPACE or key == pygame.K_r:
                self.state = "menu"

        elif self.state == "menu":
            difficulty_names = list(DIFFICULTIES.keys())
            if key in (pygame.K_UP, pygame.K_w):
                self._menu_cursor = (self._menu_cursor - 1) % len(difficulty_names)
            elif key in (pygame.K_DOWN, pygame.K_s):
                self._menu_cursor = (self._menu_cursor + 1) % len(difficulty_names)
            elif key == pygame.K_RETURN or key == pygame.K_SPACE:
                # Start a new round with the selected difficulty
                chosen = difficulty_names[self._menu_cursor]
                self.moves_per_second = DIFFICULTIES[chosen]
                self._init_round()
            elif key == pygame.K_ESCAPE or key == pygame.K_q:
                # Signal the main loop to quit
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_input(self):
        # Reserved for continuously-held-key input (not used for a
        # grid-based snake, but kept here to mirror the engine's shape).
        pass

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self):
        if self.state != "playing":
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)
        if self._frame_counter < frames_per_move:
            return
        self._frame_counter = 0

        self.snake.move()

        # Task 2: proper game-over state (wall collision)
        if self.snake.collides_with_wall(self.grid_width, self.grid_height):
            self._sound_gameover.play()   # Task 4
            self.state = "game_over"
            return

        # Task 2: proper game-over state (self collision)
        if self.snake.collides_with_self():
            self._sound_gameover.play()   # Task 4
            self.state = "game_over"
            return

        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
            self._sound_eat.play()        # Task 4
            self.food.respawn(self.snake.body)

    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------

    def render(self, screen):
        if self.state == "playing":
            self._render_game(screen)
        elif self.state == "game_over":
            self._render_game(screen)
            self._render_game_over_overlay(screen)
        elif self.state == "menu":
            self._render_difficulty_menu(screen)

    def _render_game(self, screen):
        # Draw food
        pygame.draw.rect(screen, RED, self.food.rect())

        # Draw snake body segments (slightly darker)
        for rect in self.snake.segment_rects()[1:]:
            pygame.draw.rect(screen, GREEN, rect)

        # Draw snake head (brighter highlight)
        if self.snake.segment_rects():
            pygame.draw.rect(screen, (0, 255, 0), self.snake.segment_rects()[0])

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    def _render_game_over_overlay(self, screen):
        """Task 2 & 3: Semi-transparent game-over overlay with final score and replay hint."""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # "GAME OVER" title
        title = self.big_font.render("GAME OVER", True, RED)
        screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 2 - 60)))

        # Final score
        score_surf = self.font.render(f"Final Score: {self.score}", True, YELLOW)
        screen.blit(score_surf, score_surf.get_rect(center=(self.width // 2, self.height // 2 + 10)))

        # Prompt
        prompt = self.menu_font.render("Press R / Enter to play again   Q to quit", True, GREY)
        screen.blit(prompt, prompt.get_rect(center=(self.width // 2, self.height // 2 + 65)))

    def _render_difficulty_menu(self, screen):
        """Task 3: Difficulty selection screen."""
        screen.fill(BLACK)

        title = self.big_font.render("SELECT DIFFICULTY", True, WHITE)
        screen.blit(title, title.get_rect(center=(self.width // 2, 140)))

        difficulty_names = list(DIFFICULTIES.keys())
        for i, name in enumerate(difficulty_names):
            is_selected = (i == self._menu_cursor)
            color  = YELLOW if is_selected else GREY
            prefix = "> " if is_selected else "  "
            label  = self.menu_font.render(f"{prefix}{name}", True, color)
            y_pos  = 260 + i * 60
            screen.blit(label, label.get_rect(center=(self.width // 2, y_pos)))

        hint = self.font.render("↑ ↓  to choose   Enter to start   Esc to quit", True, DARK_GREY)
        screen.blit(hint, hint.get_rect(center=(self.width // 2, self.height - 40)))

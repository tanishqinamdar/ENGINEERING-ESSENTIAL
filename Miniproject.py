# snake_levels.py
import pygame 
import random
import sys

# --- Configuration ---
CELL = 20              # size of a cell
COLS = 30
ROWS = 20
WIDTH = CELL * COLS
HEIGHT = CELL * ROWS
SNAKE_COLOR = (17, 168, 79)
FOOD_COLOR = (219, 50, 54)
BG_COLOR = (30, 30, 30)
GRID_COLOR = (40, 40, 40)
TEXT_COLOR = (240, 240, 240)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        x = COLS // 2
        y = ROWS // 2
        self.body = [(x, y), (x-1, y), (x-2, y)]
        self.dir = RIGHT
        self.grow = False

    def head(self):
        return self.body[0]

    def move(self):
        hx, hy = self.head()
        dx, dy = self.dir
        new_head = (hx + dx, hy + dy)   # no wrap-around
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_dir(self, new_dir):
        opposite = (-self.dir[0], -self.dir[1])
        if new_dir != opposite:
            self.dir = new_dir


class Food:
    def __init__(self, snake_body):
        self.position = self.random_pos(snake_body)

    def random_pos(self, snake_body):
        choices = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in snake_body]
        return random.choice(choices) if choices else None

    def respawn(self, snake_body):
        self.position = self.random_pos(snake_body)


def draw_grid(surface):
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))


def draw_rect(surface, pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
    pygame.draw.rect(surface, color, rect)


def draw_text_center(surface, text, size, y_offset=0):
    font = pygame.font.SysFont("consolas", size, bold=True)
    text_surf = font.render(text, True, TEXT_COLOR)
    rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    surface.blit(text_surf, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake — Levels")
    clock = pygame.time.Clock()
    font_small = pygame.font.SysFont("consolas", 20)

    # --- Level Selection ---
    level = None
    while level is None:
        screen.fill(BG_COLOR)
        draw_text_center(screen, "Select Level", 40, -60)
        draw_text_center(screen, "1. Easy   2. Medium   3. Hard", 28, 0)
        draw_text_center(screen, "Press 1 / 2 / 3", 22, 60)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = 1
                    FPS = 8
                elif event.key == pygame.K_2:
                    level = 2
                    FPS = 12
                elif event.key == pygame.K_3:
                    level = 3
                    FPS = 18

    snake = Snake()
    food = Food(snake.body)
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    snake.change_dir(UP)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    snake.change_dir(DOWN)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    snake.change_dir(LEFT)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    snake.change_dir(RIGHT)
                elif event.key == pygame.K_r and game_over:
                    # restart
                    snake = Snake()
                    food = Food(snake.body)
                    score = 0
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if not running:
            break

        if not game_over:
            snake.move()

            hx, hy = snake.head()

            # --- Rule 1: Collision with wall ---
            if hx < 0 or hx >= COLS or hy < 0 or hy >= ROWS:
                game_over = True

            # --- Rule 2: Collision with self ---
            elif snake.head() in snake.body[1:]:
                game_over = True

            # Food eaten?
            if food.position is not None and snake.head() == food.position:
                snake.grow = True
                score += 1
                food.respawn(snake.body)

        # Draw
        screen.fill(BG_COLOR)
        draw_grid(screen)

        if food.position:
            draw_rect(screen, food.position, FOOD_COLOR)

        for i, segment in enumerate(snake.body):
            draw_rect(screen, segment, SNAKE_COLOR)

        score_surf = font_small.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_surf, (8, 8))

        if game_over:
            draw_text_center(screen, "GAME OVER", 48, -20)
            draw_text_center(screen, "Press R to restart or Esc to quit", 22, 30)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

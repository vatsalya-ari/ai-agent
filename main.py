import pygame
import sys
import random

pygame.init()

# --- Game Window ---
WIDTH, HEIGHT = 600, 600
CELL = 30
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 32)

# --- Colors ---
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# -----------------------------
#     Helper Functions
# -----------------------------

def draw_grid():
    for x in range(0, WIDTH, CELL):
        for y in range(0, HEIGHT, CELL):
            pygame.draw.rect(window, (40, 40, 40), (x, y, CELL, CELL), 1)


def random_position():
    return random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL)


# -----------------------------
#     Main Game Loop
# -----------------------------

def game_loop():
    # Snake starting position
    snake = [(300, 300), (270, 300), (240, 300)]
    direction = "RIGHT"

    food = random_position()
    score = 0
    running = True

    while running:
        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # --- Move Snake ---
        x, y = snake[0]
        if direction == "UP":
            y -= CELL
        elif direction == "DOWN":
            y += CELL
        elif direction == "LEFT":
            x -= CELL
        elif direction == "RIGHT":
            x += CELL

        new_head = (x, y)
        snake.insert(0, new_head)

        # --- Check food collision ---
        if new_head == food:
            score += 1
            food = random_position()  # spawn new food
        else:
            snake.pop()  # remove tail

        # --- Check wall collision ---
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return score

        # --- Check self collision ---
        if new_head in snake[1:]:
            return score

        # --- Draw everything ---
        window.fill(BLACK)
        draw_grid()

        # Draw snake
        for block in snake:
            pygame.draw.rect(window, GREEN, (block[0], block[1], CELL, CELL))

        # Draw food
        pygame.draw.rect(window, RED, (food[0], food[1], CELL, CELL))

        # Draw score
        score_surf = font.render(f"Score: {score}", True, WHITE)
        window.blit(score_surf, (10, 10))

        pygame.display.update()
        clock.tick(10)  # control speed


# -----------------------------
#     Game Over Screen
# -----------------------------

def game_over_screen(score):
    while True:
        window.fill(BLACK)
        text = font.render(f"Game Over! Score: {score}", True, WHITE)
        restart = font.render("Press R to Restart", True, WHITE)

        window.blit(text, (150, 250))
        window.blit(restart, (150, 320))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return


# -----------------------------
#     Game Loop Controller
# -----------------------------

while True:
    final_score = game_loop()
    game_over_screen(final_score)

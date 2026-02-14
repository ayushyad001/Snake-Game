import pygame
import random
import sys

# ---------- Config ----------
CELL = 20
GRID_W, GRID_H = 30, 20
WIDTH, HEIGHT = GRID_W * CELL, GRID_H * CELL
FPS = 12

BLACK = (0, 0, 0)
WHITE = (240, 240, 240)
GREEN = (0, 200, 0)
RED = (220, 40, 40)
GRAY = (35, 35, 35)

# ---------- Helpers ----------
def rand_food(snake):
    while True:
        pos = (random.randrange(GRID_W), random.randrange(GRID_H))
        if pos not in snake:
            return pos

def draw_cell(screen, pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x * CELL, y * CELL, CELL, CELL), border_radius=4)

# ---------- Main ----------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    snake = [(GRID_W // 2, GRID_H // 2)]
    direction = (1, 0)   # start moving right
    pending_dir = direction

    food = rand_food(snake)
    score = 0
    game_over = False

    while True:
        clock.tick(FPS)

        # --- Events / Input ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if not game_over:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        pending_dir = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        pending_dir = (0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        pending_dir = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        pending_dir = (1, 0)
                else:
                    if event.key == pygame.K_r:
                        return main()

        if not game_over:
            # Prevent 180-degree turns
            if (pending_dir[0] != -direction[0]) or (pending_dir[1] != -direction[1]):
                direction = pending_dir

            # --- Update (Game Loop Mechanics) ---
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # Wall collision
            if not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
                game_over = True
            # Self collision
            elif new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)

                # Eat food
                if new_head == food:
                    score += 1
                    food = rand_food(snake)
                else:
                    snake.pop()

        # --- Draw ---
        screen.fill(BLACK)

        # Optional subtle grid
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        # Food
        draw_cell(screen, food, RED)

        # Snake (head brighter)
        for i, segment in enumerate(snake):
            draw_cell(screen, segment, (0, 255, 0) if i == 0 else GREEN)

        # Score
        score_surf = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        if game_over:
            msg = font.render("Game Over! Press R to restart", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 16))

        pygame.display.flip()

if __name__ == "__main__":
    main()

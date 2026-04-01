import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Shooter Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5

# Exploitable variables (for learning purposes)
player_health = 100  # Can be modified in memory
score = 0  # Can be modified

# Bullet
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Enemy
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []

# Clock
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.SysFont(None, 36)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def create_enemy():
    x = random.randint(0, SCREEN_WIDTH - enemy_width)
    y = -enemy_height
    enemies.append([x, y])

def main():
    global player_x, player_health, score
    running = True
    enemy_spawn_timer = 0

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Shoot bullet
                    bullet_x = player_x + player_width // 2 - bullet_width // 2
                    bullet_y = player_y
                    bullets.append([bullet_x, bullet_y])

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        # Update bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Spawn enemies
        enemy_spawn_timer += 1
        if enemy_spawn_timer > 60:  # Spawn every second
            create_enemy()
            enemy_spawn_timer = 0

        # Update enemies
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            if enemy[1] > SCREEN_HEIGHT:
                enemies.remove(enemy)
                player_health -= 10  # Damage when enemy reaches bottom
                if player_health <= 0:
                    running = False  # Game over

        # Check collisions between player and enemies
        for enemy in enemies[:]:
            if (player_x < enemy[0] + enemy_width and
                player_x + player_width > enemy[0] and
                player_y < enemy[1] + enemy_height and
                player_y + player_height > enemy[1]):
                enemies.remove(enemy)
                player_health -= 10
                if player_health <= 0:
                    running = False
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (bullet[0] < enemy[0] + enemy_width and
                    bullet[0] + bullet_width > enemy[0] and
                    bullet[1] < enemy[1] + enemy_height and
                    bullet[1] + bullet_height > enemy[1]):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    break

        # Draw player
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))

        # Draw UI
        draw_text(f"Health: {player_health}", font, WHITE, 10, 10)
        draw_text(f"Score: {score}", font, WHITE, 10, 50)

        pygame.display.flip()
        clock.tick(FPS)

    # Game over
    screen.fill(BLACK)
    draw_text("Game Over", font, RED, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
    draw_text(f"Final Score: {score}", font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()
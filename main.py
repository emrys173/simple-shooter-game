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
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5

# Exploitable variables (for learning purposes)
player_health = 100  # Can be modified in memory
score = 0  # Can be modified
level = 1
spawn_rate = 60
paused = False

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

# Power-up
power_up_width = 30
power_up_height = 30
power_up_speed = 2
power_ups = []

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
    enemy_type = random.choice([0, 1, 2])  # 0: normal, 1: fast, 2: tough
    health = 1
    if enemy_type == 2:
        health = 2
    enemies.append([x, y, health, enemy_type])

def create_power_up():
    x = random.randint(0, SCREEN_WIDTH - power_up_width)
    y = -power_up_height
    power_ups.append([x, y])

def main():
    global player_x, player_health, score, level, enemy_speed, spawn_rate, enemies, bullets, power_ups, paused
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
                if event.key == pygame.K_p:
                    paused = not paused

        if paused:
            continue

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
        if enemy_spawn_timer > spawn_rate:  # Spawn every spawn_rate frames
            create_enemy()
            enemy_spawn_timer = 0
            if random.randint(1, 10) == 1:  # 10% chance
                create_power_up()

        # Update enemies
        for enemy in enemies[:]:
            speed = enemy_speed
            if enemy[3] == 1:  # fast enemy
                speed *= 1.5
            enemy[1] += speed
            if enemy[1] > SCREEN_HEIGHT:
                enemies.remove(enemy)
                player_health -= 10  # Damage when enemy reaches bottom
                if player_health <= 0:
                    running = False

        # Update power-ups
        for power_up in power_ups[:]:
            power_up[1] += power_up_speed
            if power_up[1] > SCREEN_HEIGHT:
                power_ups.remove(power_up)

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
        # Check collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (bullet[0] < enemy[0] + enemy_width and
                    bullet[0] + bullet_width > enemy[0] and
                    bullet[1] < enemy[1] + enemy_height and
                    bullet[1] + bullet_height > enemy[1]):
                    enemy[2] -= 1  # decrease health
                    bullets.remove(bullet)
                    if enemy[2] <= 0:
                        enemies.remove(enemy)
                        score += 10
                        if score > level * 100:
                            level += 1
                            enemy_speed += 0.5
                            spawn_rate = max(20, spawn_rate - 10)
                    break

        # Check collisions between player and power-ups
        for power_up in power_ups[:]:
            if (player_x < power_up[0] + power_up_width and
                player_x + player_width > power_up[0] and
                player_y < power_up[1] + power_up_height and
                player_y + player_height > power_up[1]):
                power_ups.remove(power_up)
                player_health = min(100, player_health + 20)

        # Draw player
        pygame.draw.rect(screen, GREEN, (player_x, player_y, player_width, player_height))

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))

        # Draw enemies
        for enemy in enemies:
            color = RED if enemy[3] == 0 else GREEN if enemy[3] == 1 else BLUE
            pygame.draw.rect(screen, color, (enemy[0], enemy[1], enemy_width, enemy_height))

        # Draw power-ups
        for power_up in power_ups:
            pygame.draw.rect(screen, YELLOW, (power_up[0], power_up[1], power_up_width, power_up_height))

        # Draw UI
        draw_text(f"Health: {player_health}", font, WHITE, 10, 10)
        draw_text(f"Score: {score}", font, WHITE, 10, 50)
        draw_text(f"Level: {level}", font, WHITE, 10, 90)

        pygame.display.flip()
        clock.tick(FPS)

    # Game over
    screen.fill(BLACK)
    draw_text("Game Over", font, RED, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
    draw_text(f"Final Score: {score}", font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
    draw_text("Press R to Restart", font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Reset game
                player_x = SCREEN_WIDTH // 2 - player_width // 2
                player_health = 100
                score = 0
                level = 1
                enemy_speed = 3
                spawn_rate = 60
                enemies = []
                bullets = []
                power_ups = []
                paused = False
                main()  # Restart
    pygame.quit()

if __name__ == "__main__":
    main()
import os
import pygame
import sys
from collections import deque
import random
import sys

def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Initialize Pygame
pygame.init()

# Initialize Mixer
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
except pygame.error as e:
    print(f"Could not initialize mixer: {e}")
    sys.exit(1)

# Screen settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echoes of Time")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 120, 215)
RED = (220, 20, 60)
DARK_RED = (139, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
TINT_COLOR = (0, 0, 0, 180)  # Semi-transparent black

# Player settings
PLAYER_SIZE = 50
PLAYER_SPEED = 300  # pixels per second

# Echo settings
ECHO_DURATION = 2  # seconds
FPS = 60

# Minimum spawn distance for enemies
MIN_SPAWN_DISTANCE = 100  # Adjusted to balance spawning

# Fragment velocity decay factor
FRAGMENT_VELOCITY_DECAY = 0.95
MIN_FRAGMENT_VELOCITY = 5  # Minimum threshold velocity below which fragments stop moving

# Font
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

clock = pygame.time.Clock()

# Game states
PLAYING = 'playing'
PAUSED = 'paused'
DEAD = 'dead'

def render_text_with_shadow(text, font, main_color, shadow_color, shadow_offset=(2, 2)):
    text_surface = font.render(text, True, main_color)
    shadow_surface = font.render(text, True, shadow_color)
    combined_surface = pygame.Surface(
        (text_surface.get_width() + shadow_offset[0], text_surface.get_height() + shadow_offset[1]),
        pygame.SRCALPHA
    )
    combined_surface.blit(shadow_surface, shadow_offset)
    combined_surface.blit(text_surface, (0, 0))
    return combined_surface

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def generate_enemy_position(player_pos, obstacles, enemies, min_distance, enemy_size):
    attempts = 0
    buffer = 50
    max_attempts = 500  # Reduce maximum attempts to prevent excessive looping
    max_time = 1.0  # Maximum time in seconds for finding a position
    start_time = pygame.time.get_ticks()

    while attempts < max_attempts and (pygame.time.get_ticks() - start_time) / 1000 < max_time:
        x = random.randint(buffer, WIDTH - enemy_size - buffer)
        y = random.randint(buffer, HEIGHT - enemy_size - buffer)
        enemy_rect = pygame.Rect(x, y, enemy_size, enemy_size)

        player_center = pygame.Vector2(player_pos.x + PLAYER_SIZE / 2, player_pos.y + PLAYER_SIZE / 2)
        enemy_center = pygame.Vector2(x + enemy_size / 2, y + enemy_size / 2)
        distance = player_center.distance_to(enemy_center)
        if distance < min_distance + (enemy_size / 2):
            attempts += 1
            continue

        overlap = any(enemy_rect.colliderect(obstacle.rect) for obstacle in obstacles)
        if overlap:
            attempts += 1
            continue

        overlap_with_enemy = any(enemy_center.distance_to(pygame.Vector2(enemy.rect.x + enemy.size / 2, enemy.rect.y + enemy.size / 2)) < (enemy_size + enemy.size) / 2 for enemy in enemies)
        if overlap_with_enemy:
            attempts += 1
            continue

        if not SCREEN.get_rect().contains(enemy_rect):
            attempts += 1
            continue

        return (x, y)
    return None

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.num_enemies = 3 + level_number
        self.enemy_speed = 120 + (level_number * 20)

class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.size = PLAYER_SIZE
        self.color = BLUE
        self.speed = PLAYER_SPEED
        self.history = deque(maxlen=int(ECHO_DURATION * FPS))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        self.visible = True

    def handle_movement(self, keys_pressed, obstacles, shattered_enemies, dt):
        original_pos = self.pos.copy()
        movement = self.get_movement_vector(keys_pressed, dt)
        self.apply_movement(movement, obstacles, shattered_enemies, original_pos)
        self.clamp_position()

    def get_movement_vector(self, keys_pressed, dt):
        movement = pygame.Vector2(0, 0)
        if keys_pressed[pygame.K_LEFT]:
            movement.x -= 1
        if keys_pressed[pygame.K_RIGHT]:
            movement.x += 1
        if keys_pressed[pygame.K_UP]:
            movement.y -= 1
        if keys_pressed[pygame.K_DOWN]:
            movement.y += 1

        if movement.length_squared() > 0:
            movement = movement.normalize() * self.speed * dt
        return movement

    def apply_movement(self, movement, obstacles, shattered_enemies, original_pos):
        self.pos += movement
        self.rect.topleft = self.pos
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.handle_collision(movement, obstacle, original_pos)

        for shattered_enemy in shattered_enemies:
            for fragment in shattered_enemy.fragments:
                if self.rect.colliderect(fragment['rect']):
                    fragment_center = pygame.Vector2(fragment['rect'].center)
                    player_center = pygame.Vector2(self.rect.center)
                    push_direction = fragment_center - player_center
                    if push_direction.length() != 0:
                        push_direction = push_direction.normalize()
                        fragment['velocity'] += push_direction * 100  # Increased push velocity

    def handle_collision(self, movement, obstacle, original_pos):
        self.pos = original_pos
        self.rect.topleft = self.pos

        if movement.x != 0:
            self.pos.x += movement.x
            self.rect.x = self.pos.x
            if self.rect.colliderect(obstacle.rect):
                if movement.x > 0:
                    self.pos.x = obstacle.rect.left - self.size
                elif movement.x < 0:
                    self.pos.x = obstacle.rect.right
            self.rect.x = self.pos.x

        if movement.y != 0:
            self.pos.y += movement.y
            self.rect.y = self.pos.y
            if self.rect.colliderect(obstacle.rect):
                if movement.y > 0:
                    self.pos.y = obstacle.rect.top - self.size
                elif movement.y < 0:
                    self.pos.y = obstacle.rect.bottom
            self.rect.y = self.pos.y

    def clamp_position(self):
        self.pos.x = max(0, min(WIDTH - self.size, self.pos.x))
        self.pos.y = max(0, min(HEIGHT - self.size, self.pos.y))
        self.rect.topleft = self.pos

    def update_history(self):
        self.history.append(self.pos.copy())

    def draw(self, surface, color=None):
        if self.visible:
            if color is None:
                color = self.color
            pygame.draw.rect(surface, color, self.rect)

class Echo:
    def __init__(self, history):
        self.history = list(history)
        self.current_step = 0
        self.size = PLAYER_SIZE
        self.color = DARK_RED
        self.rect = pygame.Rect(0, 0, self.size, self.size)

    def update(self):
        if self.current_step < len(self.history):
            pos = self.history[-self.current_step - 1]
            self.rect.topleft = pos
            self.current_step += 1
            return pos
        return None

    def draw(self, surface):
        pos = self.update()
        if pos:
            pygame.draw.rect(surface, self.color, self.rect)
            return True
        return False

MAX_COLLISIONS_BEFORE_RANDOM_DIRECTION = 3

class Enemy:
    def __init__(self, x, y, speed):
        self.pos = pygame.Vector2(x, y)
        self.size = 40
        self.color = GREEN
        self.speed = speed
        angle = random.uniform(0, 360)
        self.direction = pygame.Vector2(1, 0).rotate(angle).normalize()
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        self.stuck_timer = 0
        self.last_pos = pygame.Vector2(self.pos)
        self.collision_count = 0

    def move(self, dt, obstacles, shattered_player):
        adjusted_dt = self.get_adjusted_dt(dt)
        self.update_position(adjusted_dt)
        self.handle_bounds_collision()
        self.handle_obstacle_collision(obstacles)
        self.update_stuck_timer(adjusted_dt)
        self.handle_shattered_player_collision(shattered_player)

    def get_adjusted_dt(self, dt):
        return min(dt, 1 / FPS) if dt > 1 / FPS else dt

    def update_position(self, adjusted_dt):
        adjusted_speed = self.speed * adjusted_dt
        self.pos += self.direction * adjusted_speed
        self.rect.topleft = self.pos

    def handle_bounds_collision(self):
        stuck = False

        if self.pos.x < 0:
            self.pos.x = 0
            self.direction.x *= -1
            stuck = True
        elif self.pos.x > WIDTH - self.size:
            self.pos.x = WIDTH - self.size
            self.direction.x *= -1
            stuck = True

        if self.pos.y < 0:
            self.pos.y = 0
            self.direction.y *= -1
            stuck = True
        elif self.pos.y > HEIGHT - self.size:
            self.pos.y = HEIGHT - self.size
            self.direction.y *= -1
            stuck = True

        self.rect.topleft = self.pos
        return stuck

    def handle_obstacle_collision(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                self.collision_count += 1
                overlap_x, overlap_y = self.calculate_overlap(obstacle)
                self.resolve_obstacle_collision(overlap_x, overlap_y, obstacle)
                self.rect.topleft = self.pos

                if self.collision_count > MAX_COLLISIONS_BEFORE_RANDOM_DIRECTION:
                    self.randomize_direction()
                    self.collision_count = 0

    def handle_shattered_player_collision(self, shattered_player):
        if shattered_player:
            for fragment in shattered_player.fragments:
                if self.rect.colliderect(fragment['rect']):
                    fragment_center = pygame.Vector2(fragment['rect'].center)
                    enemy_center = pygame.Vector2(self.rect.center)
                    push_direction = fragment_center - enemy_center
                    if push_direction.length() != 0:
                        push_direction = push_direction.normalize()
                        fragment['velocity'] += push_direction * 100  # Increased push velocity

    def calculate_overlap(self, obstacle):
        overlap_x = min(self.rect.right, obstacle.rect.right) - max(self.rect.left, obstacle.rect.left)
        overlap_y = min(self.rect.bottom, obstacle.rect.bottom) - max(self.rect.top, obstacle.rect.top)
        return overlap_x, overlap_y

    def resolve_obstacle_collision(self, overlap_x, overlap_y, obstacle):
        if overlap_x < overlap_y:
            if self.direction.x > 0:
                self.pos.x = obstacle.rect.left - self.size
            else:
                self.pos.x = obstacle.rect.right
            self.direction.x *= -1
        else:
            if self.direction.y > 0:
                self.pos.y = obstacle.rect.top - self.size
            else:
                self.pos.y = obstacle.rect.bottom
            self.direction.y *= -1
        self.direction = self.direction.normalize()

    def randomize_direction(self):
        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

    def update_stuck_timer(self, adjusted_dt):
        if self.last_pos.distance_to(self.pos) < 1:
            self.stuck_timer += adjusted_dt
        else:
            self.stuck_timer = 0

        if self.stuck_timer > 1.0:
            self.adjust_direction()
            self.stuck_timer = 0

        self.last_pos.update(self.pos)

    def adjust_direction(self):
        self.direction.rotate_ip(random.uniform(-45, 45))
        self.direction = self.direction.normalize()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLACK

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class ShatteredEntity:
    def __init__(self, x, y, size, color, num_fragments=15, velocity_range=(50, 150), fade=False):
        self.fragments = []
        self.size = size
        self.color = color
        self.fade = fade
        fragment_size = size // 5
        for _ in range(num_fragments):
            offset_x = random.randint(-size//2, size//2)
            offset_y = random.randint(-size//2, size//2)
            fragment_rect = pygame.Rect(x + offset_x, y + offset_y, fragment_size, fragment_size)
            angle = random.uniform(0, 360)
            speed = random.uniform(*velocity_range)
            velocity = pygame.Vector2(speed, 0).rotate(angle)
            fragment = {
                'rect': fragment_rect,
                'velocity': velocity,
                'alpha': 255 if fade else None,
                'fade_timer': pygame.time.get_ticks() if fade else None
            }
            self.fragments.append(fragment)
        self.fade_delay = 1000 if fade else None

    def update(self, dt, obstacles):
        current_time = pygame.time.get_ticks()
        for fragment in self.fragments:
            fragment['rect'].x += fragment['velocity'].x * dt
            fragment['rect'].y += fragment['velocity'].y * dt

            # Apply decay to velocity, but stop if below minimum threshold
            if fragment['velocity'].length() > MIN_FRAGMENT_VELOCITY:
                fragment['velocity'] *= FRAGMENT_VELOCITY_DECAY
            else:
                fragment['velocity'] = pygame.Vector2(0, 0)

            if fragment['rect'].left <= 0 or fragment['rect'].right >= WIDTH:
                fragment['velocity'].x = 0
                fragment['rect'].x = max(0, min(fragment['rect'].x, WIDTH - fragment['rect'].width))
            if fragment['rect'].top <= 0 or fragment['rect'].bottom >= HEIGHT:
                fragment['velocity'].y = 0
                fragment['rect'].y = max(0, min(fragment['rect'].y, HEIGHT - fragment['rect'].height))

            for obstacle in obstacles:
                if fragment['rect'].colliderect(obstacle.rect):
                    fragment['velocity'] = pygame.Vector2(0, 0)
                    if fragment['rect'].centerx < obstacle.rect.centerx:
                        fragment['rect'].right = obstacle.rect.left
                    else:
                        fragment['rect'].left = obstacle.rect.right
                    if fragment['rect'].centery < obstacle.rect.centery:
                        fragment['rect'].bottom = obstacle.rect.top
                    else:
                        fragment['rect'].top = obstacle.rect.bottom

            if self.fade and current_time - fragment['fade_timer'] >= self.fade_delay:
                fragment['alpha'] -= 10  # Increased fade rate
                fragment['alpha'] = max(fragment['alpha'], 0)

    def draw(self, surface):
        for fragment in self.fragments:
            if self.fade and fragment['alpha'] > 0:
                fragment_surface = pygame.Surface((fragment['rect'].width, fragment['rect'].height), pygame.SRCALPHA)
                fragment_color = (*self.color, fragment['alpha'])
                pygame.draw.rect(fragment_surface, fragment_color, (0, 0, fragment['rect'].width, fragment['rect'].height))
                surface.blit(fragment_surface, fragment['rect'].topleft)
            elif not self.fade:
                pygame.draw.rect(surface, self.color, fragment['rect'])

    def handle_push(self, entities):
        # Optimize by limiting collision checks to nearby entities only
        nearby_entities = [entity for entity in entities if self.is_near(entity)]
        for fragment in self.fragments:
            fragment_rect = fragment['rect']
            for entity in nearby_entities:
                if fragment_rect.colliderect(entity.rect):
                    fragment_center = pygame.Vector2(fragment_rect.center)
                    entity_center = pygame.Vector2(entity.rect.center)
                    push_direction = fragment_center - entity_center
                    if push_direction.length() != 0:
                        push_direction = push_direction.normalize()
                        fragment['velocity'] += push_direction * 100  # Increased push velocity

    def is_near(self, entity):
        # Consider entities within a 200-pixel radius as "near"
        return self.fragments[0]['rect'].centerx - 200 < entity.rect.centerx < self.fragments[0]['rect'].centerx + 200 and \
               self.fragments[0]['rect'].centery - 200 < entity.rect.centery < self.fragments[0]['rect'].centery + 200

class ShatteredPlayer(ShatteredEntity):
    def __init__(self, x, y, size, color, num_fragments=15):
        super().__init__(x, y, size, color, num_fragments=num_fragments, velocity_range=(50, 150), fade=False)

class ShatteredEnemy(ShatteredEntity):
    def __init__(self, x, y, size, color, num_fragments=15):
        super().__init__(x, y, size, color, num_fragments=num_fragments, velocity_range=(100, 300), fade=True)

try:
    SOUND_ECHO = pygame.mixer.Sound(resource_path('sounds/echo.wav'))
    SOUND_DEATH = pygame.mixer.Sound(resource_path('sounds/death.wav'))
    SOUND_SHATTER = pygame.mixer.Sound(resource_path('sounds/shatter.wav'))
    SOUND_LEVEL_UP = pygame.mixer.Sound(resource_path('sounds/level_up.wav'))
    SOUND_PAUSE = pygame.mixer.Sound(resource_path('sounds/pause.wav'))
except pygame.error as e:
    print(f"Error loading sound: {e}")
    sys.exit(1)

# Set sound volumes
SOUND_ECHO.set_volume(0.5)
SOUND_DEATH.set_volume(0.9)  # Increased death sound volume
SOUND_SHATTER.set_volume(0.8)  # Increased shatter sound volume
SOUND_LEVEL_UP.set_volume(0.8)
SOUND_PAUSE.set_volume(0.3)

def run_game():
    player = Player(50, 50)
    echoes = []
    shattered_enemies = []
    shattered_player = None

    obstacles = [
        Obstacle(200, 150, 100, 300),
        Obstacle(500, 100, 50, 400),
        Obstacle(350, 250, 100, 100)
    ]

    current_level_number = 1
    level = Level(current_level_number)

    enemies = []
    for _ in range(level.num_enemies):
        pos = generate_enemy_position(player.pos, obstacles, enemies, MIN_SPAWN_DISTANCE, 50)
        if pos:
            enemies.append(Enemy(pos[0], pos[1], level.enemy_speed))

    score = 0
    game_state = PLAYING
    death_time = None
    death_text_surface = None

    while True:
        dt = clock.tick(FPS) / 1000
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if game_state == PLAYING:
                        game_state = PAUSED
                        SOUND_PAUSE.play()
                    elif game_state == PAUSED:
                        game_state = PLAYING
                        SOUND_PAUSE.play()
                if game_state == PLAYING and event.key == pygame.K_e:
                    if len(player.history) > 0:
                        echo = Echo(player.history)
                        echoes.append(echo)
                        SOUND_ECHO.play()
                if game_state == DEAD:
                    if death_time and (current_time - death_time >= 500):
                        if event.key not in [pygame.K_LCTRL, pygame.K_RCTRL,
                                             pygame.K_LALT, pygame.K_RALT,
                                             pygame.K_LSHIFT, pygame.K_RSHIFT]:
                            enemies.clear()
                            return

        keys = pygame.key.get_pressed()

        if game_state == PLAYING:
            player.visible = True
            player.handle_movement(keys, obstacles, shattered_enemies, dt)
            player.update_history()
            
            # Broad-phase collision detection to reduce unnecessary fine checks
            potential_colliders = [enemy for enemy in enemies if player.rect.colliderect(enemy.rect.inflate(50, 50))]

            # Check collisions and handle game logic
            player_rect = player.rect
            for enemy in potential_colliders:
                enemy_rect = enemy.rect
                if check_collision(player_rect, enemy_rect):
                    shattered_player = ShatteredPlayer(
                        player.pos.x,
                        player.pos.y,
                        player.size,
                        player.color,
                        num_fragments=25  # Increased number of fragments
                    )
                    game_state = DEAD
                    player.visible = False
                    death_time = current_time
                    death_text_surface = render_text_with_shadow("YOU ARE DEAD", large_font, DARK_RED, GRAY, shadow_offset=(5,5))
                    SOUND_DEATH.play()
                    break

            for echo in echoes[:]:
                active = echo.draw(SCREEN)
                echo_pos = echo.update()
                if echo_pos:
                    echo_rect = echo.rect
                    for enemy in enemies[:]:
                        enemy_rect = enemy.rect
                        if check_collision(echo_rect, enemy_rect):
                            shattered_enemy = ShatteredEnemy(
                                enemy.pos.x,
                                enemy.pos.y,
                                enemy.size,
                                enemy.color,
                                num_fragments=25  # Increased number of fragments
                            )
                            shattered_enemies.append(shattered_enemy)
                            enemies.remove(enemy)
                            echoes.remove(echo)
                            score += 10
                            SOUND_SHATTER.play()
                            break
                else:
                    echoes.remove(echo)

            if shattered_player:
                shattered_player.handle_push([player] + enemies)
            for shattered_enemy in shattered_enemies:
                shattered_enemy.handle_push(enemies)

            if not enemies:
                current_level_number += 1
                level = Level(current_level_number)

                for i in range(level.num_enemies):
                    pos = generate_enemy_position(player.pos, obstacles, enemies, MIN_SPAWN_DISTANCE, enemy_size=40)
                    if pos:
                        enemies.append(Enemy(pos[0], pos[1], level.enemy_speed))

                echoes.clear()
                SOUND_LEVEL_UP.play()

        elif game_state == PAUSED:
            pause_text = render_text_with_shadow("Paused", large_font, WHITE, GRAY, shadow_offset=(3, 3))
            pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            SCREEN.blit(pause_text, pause_rect)
            pygame.display.flip()
            continue

        elif game_state == DEAD:
            if shattered_player:
                shattered_player.update(dt, obstacles)
            player.visible = False

        # Keep enemies and shattered entities moving even when DEAD
        if game_state != PAUSED:
            for enemy in enemies:
                enemy.move(dt, obstacles, shattered_player)

        for shattered_enemy in shattered_enemies[:]:
            shattered_enemy.update(dt, obstacles)
            if all(fragment['alpha'] == 0 for fragment in shattered_enemy.fragments):
                shattered_enemies.remove(shattered_enemy)

        SCREEN.fill(WHITE)

        for obstacle in obstacles:
            obstacle.draw(SCREEN)

        for echo in echoes[:]:
            active = echo.draw(SCREEN)
            if not active:
                echoes.remove(echo)

        for shattered_enemy in shattered_enemies:
            shattered_enemy.draw(SCREEN)

        for enemy in enemies:
            enemy.draw(SCREEN)

        if shattered_player:
            shattered_player.draw(SCREEN)

        player.draw(SCREEN)

        # Display Score
        score_text = font.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (WIDTH - 150, 20))

        # Display Number of Enemies
        enemy_text = font.render(f"Enemies: {len(enemies)}", True, BLACK)
        SCREEN.blit(enemy_text, (WIDTH // 2 - enemy_text.get_width() // 2, 60))

        # Display Current Level
        level_text = font.render(f"Level: {current_level_number}", True, BLACK)
        SCREEN.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 20))

        # Display Instructions
        if game_state == PLAYING:
            instructions = [
                "Move: Arrow Keys",
                "Echo: 'E'",
                "Pause: 'P'"
            ]
            for i, line in enumerate(instructions):
                instr_surface = render_text_with_shadow(line, font, BLACK, GRAY, shadow_offset=(1,1))
                SCREEN.blit(instr_surface, (20, 20 + i * 30))

        # Display Death Overlay
        if game_state == DEAD and death_text_surface:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(TINT_COLOR)
            SCREEN.blit(overlay, (0, 0))
            SCREEN.blit(death_text_surface, death_text_surface.get_rect(center=(WIDTH//2, HEIGHT//2)))

        pygame.display.flip()

def main():
    while True:
        run_game()

if __name__ == "__main__":
    main()
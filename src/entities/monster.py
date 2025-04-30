import pygame
import math
import random
from src.utils.constants import *

class Monster:
    def __init__(self, x, y, monster_type, level):
        self.x = x
        self.y = y
        self.type = monster_type
        self.level = level
        self.health = MONSTER_HEALTH[monster_type] * (1 + (level - 1) * 0.2)  # 20% increase per level
        self.max_health = self.health
        self.speed = MONSTER_SPEED[monster_type]
        self.damage = MONSTER_DAMAGE[monster_type] * (1 + (level - 1) * 0.1)  # 10% increase per level
        self.experience = MONSTER_EXP[monster_type] * level
        self.attack_cooldown = 0
        self.attack_range = MONSTER_ATTACK_RANGE[monster_type]
        self.detection_range = MONSTER_DETECTION_RANGE[monster_type]
        self.color = MONSTER_COLORS[monster_type]
        self.size = MONSTER_SIZE[monster_type]
        self.is_boss = monster_type == 'boss'
        self.special_ability_cooldown = 0
        self.special_ability_active = False
        self.special_ability_timer = 0

    def update(self, dt, player, maze):
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # Update special ability
        if self.special_ability_cooldown > 0:
            self.special_ability_cooldown -= dt
        if self.special_ability_active:
            self.special_ability_timer -= dt
            if self.special_ability_timer <= 0:
                self.special_ability_active = False

        # Calculate distance to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        # If player is within detection range, move towards them
        if distance <= self.detection_range:
            # Normalize direction vector
            if distance > 0:
                dx /= distance
                dy /= distance

            # Calculate new position
            new_x = self.x + dx * self.speed * dt
            new_y = self.y + dy * self.speed * dt

            # Check if the new position is within the maze boundaries and not in a wall
            cell_x = int(new_x / CELL_SIZE)
            cell_y = int(new_y / CELL_SIZE)
            if (0 <= cell_x < len(maze[0]) and 0 <= cell_y < len(maze) and
                maze[cell_y][cell_x] == 0):
                self.x = new_x
                self.y = new_y

            # Attack if in range
            if distance <= self.attack_range and self.attack_cooldown <= 0:
                self.attack(player)

        # Boss special ability
        if self.is_boss and not self.special_ability_active and self.special_ability_cooldown <= 0:
            if random.random() < 0.01:  # 1% chance per frame
                self.activate_special_ability()

    def attack(self, player):
        if player.take_damage(self.damage):
            self.attack_cooldown = MONSTER_ATTACK_COOLDOWN

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        return self.health <= 0

    def activate_special_ability(self):
        self.special_ability_active = True
        self.special_ability_timer = BOSS_SPECIAL_ABILITY_DURATION
        self.special_ability_cooldown = BOSS_SPECIAL_ABILITY_COOLDOWN
        # Apply special ability effects (e.g., increased speed, damage, etc.)
        self.speed *= 1.5
        self.damage *= 1.5

    def draw(self, screen, player_x, player_y):
        # Calculate screen position based on player's view
        screen_x = WIDTH // 2 + (self.x - player_x)
        screen_y = HEIGHT // 2 + (self.y - player_y)

        # Only draw if monster is on screen
        if (0 <= screen_x <= WIDTH and 0 <= screen_y <= HEIGHT):
            # Draw monster
            pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.size)

            # Draw health bar
            health_width = self.size * 2
            health_height = 5
            health_x = screen_x - health_width // 2
            health_y = screen_y - self.size - 10

            # Background
            pygame.draw.rect(screen, (50, 50, 50), (health_x, health_y, health_width, health_height))
            # Health
            health_percentage = self.health / self.max_health
            pygame.draw.rect(screen, (255, 0, 0), (health_x, health_y, health_width * health_percentage, health_height))

            # Draw special ability indicator for boss
            if self.is_boss and self.special_ability_active:
                pygame.draw.circle(screen, (255, 255, 0), (int(screen_x), int(screen_y)), self.size + 5, 2) 
import pygame
import math
from src.utils.constants import *

class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.health = 100
        self.max_health = 100
        self.experience = 0
        self.level = 1
        self.invulnerable = False
        self.invulnerability_timer = 0
        self.special_abilities = SPECIAL_ABILITIES.copy()
        self.ability_cooldowns = {ability: 0 for ability in SPECIAL_ABILITIES}
        self.ability_active = {ability: False for ability in SPECIAL_ABILITIES}
        self.ability_timers = {ability: 0 for ability in SPECIAL_ABILITIES}

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check if the new position is within the maze boundaries
        if 0 <= new_x < len(maze[0]) * CELL_SIZE and 0 <= new_y < len(maze) * CELL_SIZE:
            # Check if the new position is not in a wall
            cell_x = int(new_x / CELL_SIZE)
            cell_y = int(new_y / CELL_SIZE)
            if maze[cell_y][cell_x] == 0:
                self.x = new_x
                self.y = new_y

    def rotate(self, angle):
        self.angle += angle
        # Keep angle between 0 and 2π
        self.angle %= 2 * math.pi

    def take_damage(self, amount):
        if not self.invulnerable:
            self.health = max(0, self.health - amount)
            self.invulnerable = True
            self.invulnerability_timer = INVULNERABILITY_TIME
            return True
        return False

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def gain_experience(self, amount):
        self.experience += amount
        # Level up every 100 experience points
        new_level = self.experience // 100 + 1
        if new_level > self.level:
            self.level = new_level
            self.max_health += 20
            self.health = self.max_health
            return True
        return False

    def update(self, dt):
        # Update invulnerability timer
        if self.invulnerable:
            self.invulnerability_timer -= dt
            if self.invulnerability_timer <= 0:
                self.invulnerable = False

        # Update ability cooldowns and timers
        for ability in self.special_abilities:
            if self.ability_cooldowns[ability] > 0:
                self.ability_cooldowns[ability] -= dt
            if self.ability_active[ability]:
                self.ability_timers[ability] -= dt
                if self.ability_timers[ability] <= 0:
                    self.ability_active[ability] = False

        # Apply health regeneration if active
        if self.special_abilities['health_regen'] and self.ability_active['health_regen']:
            self.heal(HEALTH_REGEN_RATE * dt)

    def activate_ability(self, ability):
        if (self.special_abilities[ability] and 
            self.ability_cooldowns[ability] <= 0 and 
            not self.ability_active[ability]):
            self.ability_active[ability] = True
            self.ability_timers[ability] = SLOW_TIME_DURATION if ability == 'slow_time' else float('inf')
            self.ability_cooldowns[ability] = ABILITY_COOLDOWN
            return True
        return False

    def draw(self, screen):
        # Draw health bar
        health_width = 200
        health_height = 20
        health_x = 20
        health_y = HEIGHT - 40
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (health_x, health_y, health_width, health_height))
        # Health
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (health_x, health_y, health_width * health_percentage, health_height))
        
        # Draw experience bar
        exp_width = 200
        exp_height = 10
        exp_x = 20
        exp_y = HEIGHT - 60
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (exp_x, exp_y, exp_width, exp_height))
        # Experience
        exp_percentage = (self.experience % 100) / 100
        pygame.draw.rect(screen, (0, 255, 0), (exp_x, exp_y, exp_width * exp_percentage, exp_height))
        
        # Draw level
        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(level_text, (20, HEIGHT - 100))
        
        # Draw ability cooldowns
        ability_y = HEIGHT - 150
        for ability, active in self.ability_active.items():
            if self.special_abilities[ability]:
                color = (0, 255, 0) if active else (255, 0, 0)
                cooldown = self.ability_cooldowns[ability]
                if cooldown > 0:
                    cooldown_text = font.render(f"{ability}: {cooldown:.1f}s", True, color)
                else:
                    cooldown_text = font.render(f"{ability}: Ready", True, color)
                screen.blit(cooldown_text, (20, ability_y))
                ability_y -= 30 
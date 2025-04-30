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
        self.health = MONSTER_HEALTH[monster_type] * level
        self.speed = MONSTER_SPEED[monster_type]
        self.damage = MONSTER_DAMAGE[monster_type] * level
        self.attack_range = MONSTER_ATTACK_RANGE[monster_type]
        self.attack_cooldown = 0
        self.size = MONSTER_SIZE[monster_type]
        self.color = MONSTER_COLORS[monster_type]
        
        # Load monster image if available
        try:
            self.image = pygame.image.load(f'Images/{monster_type}.png')
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        except:
            self.image = None

    def update(self, dt, player, current_map):
        """Update monster state"""
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            
        # Move towards player
        dx = player['x'] - self.x
        dy = player['y'] - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 0:
            dx /= distance
            dy /= distance
            
            # Check for walls
            new_x = self.x + dx * self.speed * dt
            new_y = self.y + dy * self.speed * dt
            
            cell_x = int(new_x / CELL_SIZE)
            cell_y = int(new_y / CELL_SIZE)
            
            if 0 <= cell_x < len(current_map[0]) and 0 <= cell_y < len(current_map):
                if current_map[cell_y][cell_x] == 0:  # Free space
                    self.x = new_x
                    self.y = new_y

    def draw(self, screen, player_x, player_y):
        """Draw monster on screen"""
        if self.image:
            screen.blit(self.image, (self.x - self.size/2, self.y - self.size/2))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    def attack(self, player):
        """Attempt to attack the player"""
        if self.attack_cooldown <= 0:
            self.attack_cooldown = MONSTER_ATTACK_COOLDOWN
            return True
        return False

    def take_damage(self, damage):
        """Handle monster taking damage"""
        self.health -= damage
        return self.health <= 0 
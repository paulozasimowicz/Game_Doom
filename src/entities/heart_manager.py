import pygame
import random
import math
from src.utils.constants import *

class HeartManager:
    def __init__(self, maze):
        self.maze = maze
        self.hearts = []
        try:
            # Load the heart image and convert it for better performance
            self.heart_image = pygame.image.load("Images/heart.png").convert_alpha()
            self.heart_image = pygame.transform.scale(self.heart_image, (HEART_SIZE, HEART_SIZE))
        except Exception as e:
            print(f"Error loading heart image: {e}")
            # Create a fallback heart surface if image loading fails
            self.heart_image = pygame.Surface((HEART_SIZE, HEART_SIZE), pygame.SRCALPHA)
            pygame.draw.polygon(self.heart_image, (255, 0, 0), [
                (HEART_SIZE//2, 0),
                (HEART_SIZE, HEART_SIZE//3),
                (HEART_SIZE, HEART_SIZE),
                (HEART_SIZE//2, HEART_SIZE*2//3),
                (0, HEART_SIZE),
                (0, HEART_SIZE//3)
            ])
        self.spawn_positions = self._generate_spawn_positions()
        
    def _generate_spawn_positions(self):
        positions = []
        # Try to find valid spawn positions
        for _ in range(MAX_HEART_SPAWN_ATTEMPTS):
            # Get a random cell that's not a wall
            cell_x = random.randint(0, len(self.maze[0]) - 1)
            cell_y = random.randint(0, len(self.maze) - 1)
            
            if self.maze[cell_y][cell_x] == 1:  # Skip walls
                continue
                
            # Convert cell coordinates to world coordinates
            x = cell_x * CELL_SIZE + CELL_SIZE // 2
            y = cell_y * CELL_SIZE + CELL_SIZE // 2
            
            # Check if position is too close to other hearts
            if self._is_too_close_to_other_hearts(x, y, positions):
                continue
                
            positions.append((x, y))
            
            # Stop if we have enough positions
            if len(positions) >= MAX_HEARTS:
                break
                
        return positions
        
    def _is_too_close_to_other_hearts(self, x, y, positions):
        for pos in positions:
            dx = pos[0] - x
            dy = pos[1] - y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < MIN_HEART_DISTANCE:
                return True
        return False
        
    def spawn_hearts(self):
        for pos in self.spawn_positions:
            self.hearts.append({
                'x': pos[0],
                'y': pos[1],
                'collected': False,
                'pulse_scale': 1.0,
                'pulse_speed': 0.1,
                'pulse_time': 0
            })
            
    def check_collision(self, player_x, player_y):
        for heart in self.hearts:
            if heart['collected']:
                continue
                
            dx = heart['x'] - player_x
            dy = heart['y'] - player_y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < HEART_COLLISION_DISTANCE:
                heart['collected'] = True
                return True
        return False
        
    def update(self):
        # Update heart animations
        for heart in self.hearts:
            if not heart['collected']:
                heart['pulse_time'] += heart['pulse_speed']
                heart['pulse_scale'] = 1.0 + math.sin(heart['pulse_time']) * 0.2
        
    def draw(self, screen):
        for heart in self.hearts:
            if not heart['collected']:
                # Calculate scaled size
                scaled_size = int(HEART_SIZE * heart['pulse_scale'])
                scaled_image = pygame.transform.scale(self.heart_image, (scaled_size, scaled_size))
                
                # Calculate position to keep heart centered
                x = heart['x'] - scaled_size // 2
                y = heart['y'] - scaled_size // 2
                
                screen.blit(scaled_image, (x, y)) 
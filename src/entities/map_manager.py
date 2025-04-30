import pygame
import time
import random
from src.utils.constants import *
from src.entities.monster_manager import MonsterManager
from src.entities.heart_manager import HeartManager

class MapManager:
    def __init__(self):
        self.current_level = 1
        self.current_map = MAPS[0]
        self.monster_manager = None
        self.heart_manager = None
        self.level_start_time = time.time()
        self.level_completed = False
        self.visited_cells = set()
        self.level_time_limit = LEVEL_TIME_LIMIT
        self.kill_count = 0
        self.player_health = 10
        self.last_hit_time = 0
        self.invulnerability_time = INVULNERABILITY_TIME

    def reset_level(self):
        """Reset the current level state"""
        self.current_map = MAPS[self.current_level - 1]
        self.level_start_time = time.time()
        self.level_completed = False
        self.visited_cells.clear()
        self.kill_count = 0
        
        # Initialize or reset managers
        if self.monster_manager:
            self.monster_manager.reset()
        else:
            self.monster_manager = MonsterManager(self.current_map)
            
        if self.heart_manager:
            self.heart_manager.reset()
        else:
            self.heart_manager = HeartManager(self.current_map)

    def next_level(self):
        """Advance to the next level"""
        if self.current_level < MAX_LEVEL:
            self.current_level += 1
            self.reset_level()
            return True
        return False

    def update_visited_cells(self, player_x, player_y):
        """Update the set of visited cells based on player position"""
        cell_x = int(player_x / CELL_SIZE)
        cell_y = int(player_y / CELL_SIZE)
        self.visited_cells.add((cell_x, cell_y))

    def update(self, dt, player):
        """Update game state"""
        # Update visited cells
        self.update_visited_cells(player['x'], player['y'])
        
        # Update managers
        if self.monster_manager:
            if not self.monster_manager.update(dt, player):
                return False
                
        if self.heart_manager:
            self.heart_manager.update()
        
        # Check if level is completed
        if self.check_level_completion():
            self.level_completed = True
        
        return True

    def draw(self, screen, player_x, player_y):
        """Draw game elements"""
        if self.monster_manager:
            self.monster_manager.draw(screen, player_x, player_y)
        
        if self.heart_manager:
            self.heart_manager.draw(screen)

    def check_special_area(self, x, y):
        """Check if player is in a special area"""
        cell_x = int(x / CELL_SIZE)
        cell_y = int(y / CELL_SIZE)
        
        if 0 <= cell_x < len(self.current_map[0]) and 0 <= cell_y < len(self.current_map):
            return self.current_map[cell_y][cell_x] in SPECIAL_AREAS.values()
        return False

    def handle_special_area(self, x, y):
        """Handle special area effects"""
        cell_x = int(x / CELL_SIZE)
        cell_y = int(y / CELL_SIZE)
        
        if 0 <= cell_x < len(self.current_map[0]) and 0 <= cell_y < len(self.current_map):
            cell_value = self.current_map[cell_y][cell_x]
            
            if cell_value == SPECIAL_AREAS['treasure']:
                if self.heart_manager:
                    self.heart_manager.spawn_hearts()
            
            elif cell_value == SPECIAL_AREAS['trap']:
                if self.monster_manager:
                    self.monster_manager.spawn_wave()
            
            elif cell_value == SPECIAL_AREAS['boss']:
                if self.monster_manager:
                    self.monster_manager.spawn_boss()
            
            elif cell_value == SPECIAL_AREAS['exit']:
                return self.next_level()
        
        return False

    def check_level_completion(self):
        """Check if level is completed"""
        # Check if time limit is reached
        if time.time() - self.level_start_time > self.level_time_limit:
            return True
            
        # Check if all monsters are defeated
        if self.monster_manager and len(self.monster_manager.monsters) == 0:
            return True
            
        return False

    def take_damage(self, amount):
        """Handle player taking damage"""
        current_time = time.time()
        if current_time - self.last_hit_time >= self.invulnerability_time:
            self.player_health -= amount
            self.last_hit_time = current_time
            return True
        return False

    def add_kill(self):
        """Increment kill count"""
        self.kill_count += 1

    def get_level_info(self):
        """Get current level information"""
        return {
            'level': self.current_level,
            'time_remaining': max(0, self.level_time_limit - (time.time() - self.level_start_time)),
            'kills': self.kill_count,
            'health': self.player_health
        } 
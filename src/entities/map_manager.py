import pygame
import time
import random
import math
from src.utils.constants import *
from src.entities.monster import Monster
from src.entities.heart_manager import HeartManager

class MapManager:
    def __init__(self):
        self.current_level = 1
        self.current_map = MAPS[0]
        self.monsters = []
        self.heart_manager = None
        self.last_spawn_time = time.time()
        self.last_wave_time = time.time()
        self.boss_spawned = False
        self.level_start_time = time.time()
        self.level_completed = False
        self.visited_cells = set()

    def reset_level(self):
        """Reset the current level state"""
        self.current_map = MAPS[self.current_level - 1]
        self.monsters.clear()
        self.heart_manager = HeartManager(self.current_map)
        self.heart_manager.spawn_hearts()
        self.last_spawn_time = time.time()
        self.last_wave_time = time.time()
        self.boss_spawned = False
        self.level_start_time = time.time()
        self.level_completed = False
        self.visited_cells.clear()

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

    def spawn_monsters(self, player_x, player_y):
        """Spawn monsters according to level limits and timing"""
        current_time = time.time()
        
        # Check if we've reached the monster limit for this level
        if len(self.monsters) >= MAX_MONSTERS_PER_LEVEL[self.current_level]:
            return

        # Regular monster spawn
        if current_time - self.last_spawn_time >= SPAWN_INTERVAL:
            self._try_spawn_monster(player_x, player_y)
            self.last_spawn_time = current_time

        # Wave spawn
        if current_time - self.last_wave_time >= WAVE_INTERVAL:
            self._spawn_wave(player_x, player_y)
            self.last_wave_time = current_time

    def _try_spawn_monster(self, player_x, player_y):
        """Attempt to spawn a single monster"""
        for _ in range(MAX_SPAWN_ATTEMPTS):
            # Get random position
            cell_x = random.randint(1, len(self.current_map[0]) - 2)
            cell_y = random.randint(1, len(self.current_map) - 2)
            
            if self.current_map[cell_y][cell_x] != 0:  # Skip walls
                continue
                
            # Convert to world coordinates
            x = cell_x * CELL_SIZE + CELL_SIZE // 2
            y = cell_y * CELL_SIZE + CELL_SIZE // 2
            
            # Check distance from player
            dx = x - player_x
            dy = y - player_y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < MIN_SPAWN_DISTANCE:
                continue
                
            # Check distance from other monsters
            if self._is_too_close_to_other_monsters(x, y):
                continue
                
            # Create and add monster
            monster_type = 'normal' if random.random() < 0.8 else 'elite'
            monster = Monster(x, y, monster_type, self.current_level)
            self.monsters.append(monster)
            break

    def _spawn_wave(self, player_x, player_y):
        """Spawn a wave of monsters"""
        # Spawn regular monsters
        for _ in range(WAVE_SIZE - 1):
            self._try_spawn_monster(player_x, player_y)
            
        # Try to spawn boss if not already spawned
        if not self.boss_spawned and self.current_level > 1:
            self._try_spawn_boss(player_x, player_y)

    def _try_spawn_boss(self, player_x, player_y):
        """Attempt to spawn a boss monster"""
        for _ in range(MAX_SPAWN_ATTEMPTS):
            # Get random position
            cell_x = random.randint(1, len(self.current_map[0]) - 2)
            cell_y = random.randint(1, len(self.current_map) - 2)
            
            if self.current_map[cell_y][cell_x] != 0:  # Skip walls
                continue
                
            # Convert to world coordinates
            x = cell_x * CELL_SIZE + CELL_SIZE // 2
            y = cell_y * CELL_SIZE + CELL_SIZE // 2
            
            # Check distance from player
            dx = x - player_x
            dy = y - player_y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < MIN_SPAWN_DISTANCE * 2:  # Boss needs more space
                continue
                
            # Check distance from other monsters
            if self._is_too_close_to_other_monsters(x, y):
                continue
                
            # Create and add boss
            boss = Monster(x, y, 'boss', self.current_level)
            self.monsters.append(boss)
            self.boss_spawned = True
            break

    def _is_too_close_to_other_monsters(self, x, y):
        """Check if a position is too close to other monsters"""
        for monster in self.monsters:
            dx = monster.x - x
            dy = monster.y - y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < MIN_SPAWN_DISTANCE:
                return True
        return False

    def update(self, dt, player):
        """Update game state"""
        # Update visited cells
        self.update_visited_cells(player['x'], player['y'])
        
        # Spawn monsters
        self.spawn_monsters(player['x'], player['y'])
        
        # Update monsters
        for monster in self.monsters[:]:
            monster.update(dt, player, self.current_map)
            
            # Check for player damage
            dx = monster.x - player['x']
            dy = monster.y - player['y']
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < monster.attack_range and monster.attack_cooldown <= 0:
                if monster.attack(player):
                    player['health'] -= monster.damage
                    if player['health'] <= 0:
                        return False
        
        # Update heart manager
        if self.heart_manager:
            self.heart_manager.update()
            if self.heart_manager.check_collision(player['x'], player['y']):
                player['health'] = min(10, player['health'] + HEART_HEAL_AMOUNT)
        
        return True

    def draw(self, screen, player_x, player_y):
        """Draw game elements"""
        # Draw monsters
        for monster in self.monsters:
            monster.draw(screen, player_x, player_y)
        
        # Draw hearts
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
                # Spawn extra hearts
                if self.heart_manager:
                    self.heart_manager.spawn_hearts()
            
            elif cell_value == SPECIAL_AREAS['trap']:
                # Spawn extra monsters
                for _ in range(3):
                    self._try_spawn_monster(x, y)
            
            elif cell_value == SPECIAL_AREAS['boss']:
                # Spawn boss if not already spawned
                if not self.boss_spawned:
                    self._try_spawn_boss(x, y)
            
            elif cell_value == SPECIAL_AREAS['exit']:
                # Advance to next level
                return self.next_level()
        
        return False 
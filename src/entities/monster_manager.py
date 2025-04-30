import random
import math
import time
from src.utils.constants import *
from src.entities.monster import Monster

class MonsterManager:
    def __init__(self, maze):
        self.maze = maze
        self.monsters = []
        self.last_spawn_time = time.time()
        self.last_wave_time = time.time()
        self.boss_spawned = False

    def reset(self):
        """Reset the monster manager state"""
        self.monsters.clear()
        self.last_spawn_time = time.time()
        self.last_wave_time = time.time()
        self.boss_spawned = False

    def update(self, dt, player):
        """Update all monsters and handle player interactions"""
        current_time = time.time()
        
        # Spawn monsters if needed
        if current_time - self.last_spawn_time >= SPAWN_INTERVAL:
            self._try_spawn_monster(player['x'], player['y'])
            self.last_spawn_time = current_time

        # Spawn wave if needed
        if current_time - self.last_wave_time >= WAVE_INTERVAL:
            self.spawn_wave(player['x'], player['y'])
            self.last_wave_time = current_time

        # Update existing monsters
        for monster in self.monsters[:]:
            monster.update(dt, player, self.maze)
            
            # Check for player damage
            dx = monster.x - player['x']
            dy = monster.y - player['y']
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < monster.attack_range and monster.attack_cooldown <= 0:
                if monster.attack(player):
                    player['health'] -= monster.damage
                    if player['health'] <= 0:
                        return False

        return True

    def draw(self, screen, player_x, player_y):
        """Draw all monsters"""
        for monster in self.monsters:
            monster.draw(screen, player_x, player_y)

    def _try_spawn_monster(self, player_x, player_y):
        """Attempt to spawn a single monster"""
        for _ in range(MAX_SPAWN_ATTEMPTS):
            # Get random position
            cell_x = random.randint(1, len(self.maze[0]) - 2)
            cell_y = random.randint(1, len(self.maze) - 2)
            
            if self.maze[cell_y][cell_x] != 0:  # Skip walls
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
            monster = Monster(x, y, monster_type)
            self.monsters.append(monster)
            break

    def spawn_wave(self, player_x, player_y):
        """Spawn a wave of monsters"""
        # Spawn regular monsters
        for _ in range(WAVE_SIZE - 1):
            self._try_spawn_monster(player_x, player_y)
            
        # Try to spawn boss if not already spawned
        if not self.boss_spawned:
            self.spawn_boss(player_x, player_y)

    def spawn_boss(self, player_x, player_y):
        """Spawn a boss monster"""
        for _ in range(MAX_SPAWN_ATTEMPTS):
            # Get random position
            cell_x = random.randint(1, len(self.maze[0]) - 2)
            cell_y = random.randint(1, len(self.maze) - 2)
            
            if self.maze[cell_y][cell_x] != 0:  # Skip walls
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
            boss = Monster(x, y, 'boss')
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
import random
import math
from src.entities.monster import Monster
from src.utils.constants import *

class MonsterSpawner:
    def __init__(self, maze):
        self.maze = maze
        self.monsters = []
        self.spawn_timer = 0
        self.spawn_cooldown = 5.0  # Seconds between spawn attempts
        self.max_monsters = 20
        self.boss_spawned = False
        self.elite_chance = 0.2  # 20% chance for elite monster
        self.boss_chance = 0.05  # 5% chance for boss (if not already spawned)

    def update(self, dt, player):
        # Update spawn timer
        self.spawn_timer -= dt

        # Update all monsters
        for monster in self.monsters[:]:
            monster.update(dt, player, self.maze)
            if monster.health <= 0:
                self.monsters.remove(monster)
                if monster.type == 'boss':
                    self.boss_spawned = False

        # Try to spawn new monsters
        if self.spawn_timer <= 0 and len(self.monsters) < self.max_monsters:
            self.spawn_timer = self.spawn_cooldown
            self._try_spawn_monster(player)

    def _try_spawn_monster(self, player):
        # Find valid spawn position
        spawn_pos = self._find_valid_spawn_position(player)
        if not spawn_pos:
            return

        x, y = spawn_pos

        # Determine monster type
        monster_type = self._determine_monster_type()

        # Create and add monster
        monster = Monster(x, y, monster_type, player.level)
        self.monsters.append(monster)

    def _find_valid_spawn_position(self, player):
        # Try to find a valid spawn position
        for _ in range(10):  # Try 10 times
            # Random position in maze
            cell_x = random.randint(0, len(self.maze[0]) - 1)
            cell_y = random.randint(0, len(self.maze) - 1)

            # Check if cell is empty
            if self.maze[cell_y][cell_x] != 0:
                continue

            # Convert to world coordinates
            x = (cell_x + 0.5) * CELL_SIZE
            y = (cell_y + 0.5) * CELL_SIZE

            # Check distance from player
            dx = x - player.x
            dy = y - player.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < MIN_SPAWN_DISTANCE:
                continue

            # Check distance from other monsters
            too_close = False
            for monster in self.monsters:
                dx = x - monster.x
                dy = y - monster.y
                if math.sqrt(dx * dx + dy * dy) < CELL_SIZE:
                    too_close = True
                    break

            if not too_close:
                return (x, y)

        return None

    def _determine_monster_type(self):
        if not self.boss_spawned and random.random() < self.boss_chance:
            self.boss_spawned = True
            return 'boss'
        elif random.random() < self.elite_chance:
            return 'elite'
        else:
            return 'normal'

    def draw(self, screen, player_x, player_y):
        for monster in self.monsters:
            monster.draw(screen, player_x, player_y)

    def get_monsters_in_range(self, x, y, range):
        monsters_in_range = []
        for monster in self.monsters:
            dx = monster.x - x
            dy = monster.y - y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance <= range:
                monsters_in_range.append(monster)
        return monsters_in_range

    def clear(self):
        self.monsters.clear()
        self.boss_spawned = False 
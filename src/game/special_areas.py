from enum import Enum
import random
from src.entities.monster import Monster
from src.utils.constants import *

class SpecialAreaType(Enum):
    TREASURE = 2
    TRAP = 3
    BOSS = 4
    EXIT = 5

class SpecialAreaManager:
    def __init__(self, maze, player_state):
        self.maze = maze
        self.player_state = player_state
        self.special_areas = {
            SpecialAreaType.TREASURE: self._handle_treasure,
            SpecialAreaType.TRAP: self._handle_trap,
            SpecialAreaType.BOSS: self._handle_boss,
            SpecialAreaType.EXIT: self._handle_exit
        }

    def check_special_area(self, x, y):
        map_x = int(x / CELL_SIZE)
        map_y = int(y / CELL_SIZE)
        if 0 <= map_x < len(self.maze) and 0 <= map_y < len(self.maze[0]):
            cell_value = self.maze[map_x][map_y]
            try:
                return SpecialAreaType(cell_value)
            except ValueError:
                return None
        return None

    def handle_special_area(self, x, y, monsters, current_level, max_level):
        area_type = self.check_special_area(x, y)
        if area_type and area_type in self.special_areas:
            return self.special_areas[area_type](x, y, monsters, current_level, max_level)
        return False

    def _handle_treasure(self, x, y, monsters, current_level, max_level):
        # Update player health through the player state
        self.player_state['health'] = min(5, self.player_state['health'] + 1)
        return True

    def _handle_trap(self, x, y, monsters, current_level, max_level):
        # Spawn extra monsters in trap room
        for _ in range(3):
            monsters.append(Monster(
                x + random.randint(-CELL_SIZE, CELL_SIZE),
                y + random.randint(-CELL_SIZE, CELL_SIZE)
            ))
        return True

    def _handle_boss(self, x, y, monsters, current_level, max_level):
        # Spawn boss monster
        monsters.append(Monster(x, y, is_boss=True))
        return True

    def _handle_exit(self, x, y, monsters, current_level, max_level):
        if current_level < max_level:
            return True
        return False 
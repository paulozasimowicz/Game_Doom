import random
import math

class MonsterManager:
    def __init__(self, maze, player):
        self.maze = maze
        self.player = player
        self.monsters = []
        self.last_spawn_time = 0

    def _spawn_monster(self, current_time):
        if len(self.monsters) >= MAX_MONSTERS_PER_LEVEL:
            return
            
        # Find a valid spawn position
        spawn_pos = self._find_valid_spawn_position()
        if not spawn_pos:
            return
            
        # Create monster
        monster_type = random.choices(
            ['normal', 'boss'],
            weights=[1 - BOSS_SPAWN_CHANCE, BOSS_SPAWN_CHANCE]
        )[0]
        
        if monster_type == 'boss':
            monster = BossMonster(spawn_pos[0], spawn_pos[1])
        else:
            monster = Monster(spawn_pos[0], spawn_pos[1])
            
        self.monsters.append(monster)
        self.last_spawn_time = current_time
        
    def _find_valid_spawn_position(self):
        # Try to find a valid spawn position
        for _ in range(MAX_SPAWN_ATTEMPTS):
            # Get a random cell that's not a wall
            cell_x = random.randint(0, len(self.maze[0]) - 1)
            cell_y = random.randint(0, len(self.maze) - 1)
            
            if self.maze[cell_y][cell_x] == 1:  # Skip walls
                continue
                
            # Convert cell coordinates to world coordinates
            x = cell_x * CELL_SIZE + CELL_SIZE // 2
            y = cell_y * CELL_SIZE + CELL_SIZE // 2
            
            # Check distance from player
            if self._get_distance_to_player(x, y) < MIN_SPAWN_DISTANCE:
                continue
                
            # Check distance from other monsters
            if self._is_too_close_to_other_monsters(x, y):
                continue
                
            return (x, y)
            
        return None
        
    def _is_too_close_to_other_monsters(self, x, y):
        for monster in self.monsters:
            dx = monster.x - x
            dy = monster.y - y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < MIN_MONSTER_DISTANCE:
                return True
        return False
        
    def _get_distance_to_player(self, x, y):
        dx = self.player.x - x
        dy = self.player.y - y
        return math.sqrt(dx * dx + dy * dy)
        
    def update(self, current_time):
        # Update existing monsters
        for monster in self.monsters[:]:
            monster.update()
            
            # Check if monster is too far from player
            if self._get_distance_to_player(monster.x, monster.y) > MAX_MONSTER_DISTANCE:
                self.monsters.remove(monster)
                continue
                
            # Check for collisions with other monsters
            for other in self.monsters:
                if monster != other and self._is_too_close_to_other_monsters(monster.x, monster.y):
                    # Move monster away from collision
                    dx = monster.x - other.x
                    dy = monster.y - other.y
                    distance = math.sqrt(dx * dx + dy * dy)
                    if distance < MIN_MONSTER_DISTANCE:
                        move_x = (MIN_MONSTER_DISTANCE - distance) * dx / distance
                        move_y = (MIN_MONSTER_DISTANCE - distance) * dy / distance
                        monster.x += move_x
                        monster.y += move_y
                        
        # Spawn new monsters if needed
        if current_time - self.last_spawn_time >= MONSTER_SPAWN_INTERVAL:
            self._spawn_monster(current_time) 
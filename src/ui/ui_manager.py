import pygame
import math
from src.utils.constants import *

class UIManager:
    def __init__(self, maze):
        self.maze = maze
        self.visited_cells = set()
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.boss_warning_font = pygame.font.Font(None, BOSS_WARNING_SIZE)
        
        # Create surfaces for UI elements
        self.status_surface = pygame.Surface((STATUS_WIDTH, STATUS_HEIGHT), pygame.SRCALPHA)
        self.minimap_surface = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE), pygame.SRCALPHA)
        self.compass_surface = pygame.Surface((COMPASS_SIZE, COMPASS_SIZE), pygame.SRCALPHA)
        self.quest_surface = pygame.Surface((QUEST_WIDTH, QUEST_HEIGHT), pygame.SRCALPHA)
        
        # Calculate minimap scale
        self.minimap_scale = MINIMAP_SIZE / (max(len(maze[0]), len(maze)) * CELL_SIZE)
        
        # Boss warning
        self.boss_warning_timer = 0
        self.boss_warning_text = None

    def update(self, player_info, monsters):
        # Update visited cells
        cell_x = int(player_info['position'][0] / CELL_SIZE)
        cell_y = int(player_info['position'][1] / CELL_SIZE)
        self.visited_cells.add((cell_x, cell_y))
        
        # Update all UI elements
        self._update_status(player_info)
        self._update_minimap(player_info, monsters)
        self._update_compass(player_info)
        
        # Check for boss warning
        for monster in monsters:
            if hasattr(monster, 'is_boss') and monster.is_boss:
                self.show_boss_warning("BOSS")
                break

    def _update_status(self, player_info):
        # Clear status surface
        self.status_surface.fill(UI_BACKGROUND_COLOR)
        
        # Draw status information
        texts = [
            f"Level: {player_info['level']}",
            f"Health: {player_info['health']}/10",
            f"Kills: {player_info['kill_count']}",
            f"Position: ({int(player_info['position'][0])}, {int(player_info['position'][1])})",
            f"FPS: {int(pygame.time.Clock().get_fps())}"
        ]
        
        for i, text in enumerate(texts):
            text_surface = self.font.render(text, True, UI_FONT_COLOR)
            self.status_surface.blit(text_surface, (10, 10 + i * 30))

    def _update_minimap(self, player_info, monsters):
        # Clear minimap surface
        self.minimap_surface.fill((0, 0, 0, 0))
        
        # Calculate scale factors
        map_width = len(self.maze[0])
        map_height = len(self.maze)
        scale_x = MINIMAP_SIZE / (map_width * CELL_SIZE)
        scale_y = MINIMAP_SIZE / (map_height * CELL_SIZE)
        
        # Draw maze
        for y in range(map_height):
            for x in range(map_width):
                # Only draw visited cells
                if (x, y) in self.visited_cells:
                    cell_color = MINIMAP_VISITED_COLOR if self.maze[y][x] == 0 else MINIMAP_WALL_COLOR
                else:
                    cell_color = MINIMAP_UNVISITED_COLOR
                
                # Draw cell with proper scaling
                cell_rect = pygame.Rect(
                    x * MINIMAP_CELL_SIZE,
                    y * MINIMAP_CELL_SIZE,
                    MINIMAP_CELL_SIZE,
                    MINIMAP_CELL_SIZE
                )
                pygame.draw.rect(self.minimap_surface, cell_color, cell_rect)
        
        # Draw monsters
        for monster in monsters:
            # Convert monster position to cell coordinates
            monster_cell_x = int(monster.x / CELL_SIZE)
            monster_cell_y = int(monster.y / CELL_SIZE)
            
            # Only draw monsters in visited cells
            if (monster_cell_x, monster_cell_y) in self.visited_cells:
                # Convert monster position to minimap coordinates
                monster_x = monster_cell_x * MINIMAP_CELL_SIZE + MINIMAP_CELL_SIZE // 2
                monster_y = monster_cell_y * MINIMAP_CELL_SIZE + MINIMAP_CELL_SIZE // 2
                
                # Determine monster color based on type
                color = MINIMAP_MONSTER_COLORS['boss'] if hasattr(monster, 'is_boss') and monster.is_boss else MINIMAP_MONSTER_COLORS['normal']
                
                # Draw monster with proper scaling
                monster_size = MINIMAP_CELL_SIZE // 2
                pygame.draw.circle(
                    self.minimap_surface,
                    color,
                    (monster_x, monster_y),
                    monster_size
                )
        
        # Draw player
        player_cell_x = int(player_info['position'][0] / CELL_SIZE)
        player_cell_y = int(player_info['position'][1] / CELL_SIZE)
        
        # Ensure player stays within minimap bounds
        player_cell_x = max(0, min(player_cell_x, map_width - 1))
        player_cell_y = max(0, min(player_cell_y, map_height - 1))
        
        # Convert player position to minimap coordinates
        player_x = player_cell_x * MINIMAP_CELL_SIZE + MINIMAP_CELL_SIZE // 2
        player_y = player_cell_y * MINIMAP_CELL_SIZE + MINIMAP_CELL_SIZE // 2
        
        # Draw player
        pygame.draw.circle(
            self.minimap_surface,
            MINIMAP_PLAYER_COLOR,
            (player_x, player_y),
            MINIMAP_CELL_SIZE // 2
        )
        
        # Draw player direction indicator
        angle = player_info['angle']
        indicator_length = MINIMAP_CELL_SIZE
        indicator_x = player_x + math.cos(angle) * indicator_length
        indicator_y = player_y - math.sin(angle) * indicator_length
        pygame.draw.line(
            self.minimap_surface,
            MINIMAP_PLAYER_COLOR,
            (player_x, player_y),
            (indicator_x, indicator_y),
            2
        )

    def _update_compass(self, player_info):
        # Clear compass surface
        self.compass_surface.fill((0, 0, 0, 0))
        
        # Draw compass circle
        pygame.draw.circle(self.compass_surface, UI_FONT_COLOR, 
                         (COMPASS_SIZE//2, COMPASS_SIZE//2), COMPASS_SIZE//2, 2)
        
        # Draw cardinal directions
        directions = ['N', 'E', 'S', 'W']
        for i, direction in enumerate(directions):
            angle = math.pi/2 * i
            x = COMPASS_SIZE//2 + math.cos(angle) * (COMPASS_SIZE//2 - 10)
            y = COMPASS_SIZE//2 - math.sin(angle) * (COMPASS_SIZE//2 - 10)
            
            # Draw direction text
            text = self.font.render(direction, True, COMPASS_COLORS[direction])
            text_rect = text.get_rect(center=(x, y))
            self.compass_surface.blit(text, text_rect)
        
        # Draw player direction indicator
        player_angle = player_info['angle']
        indicator_x = COMPASS_SIZE//2 + math.cos(player_angle) * (COMPASS_SIZE//2 - 20)
        indicator_y = COMPASS_SIZE//2 - math.sin(player_angle) * (COMPASS_SIZE//2 - 20)
        pygame.draw.line(self.compass_surface, UI_FONT_COLOR,
                        (COMPASS_SIZE//2, COMPASS_SIZE//2),
                        (indicator_x, indicator_y), 2)

    def show_boss_warning(self, boss_name):
        self.boss_warning_timer = BOSS_WARNING_DURATION
        self.boss_warning_text = self.boss_warning_font.render(
            f"WARNING: {boss_name} APPROACHING!", True, BOSS_WARNING_COLOR)

    def draw(self, screen):
        # Draw all UI elements
        screen.blit(self.status_surface, STATUS_POSITION)
        screen.blit(self.minimap_surface, MINIMAP_POSITION)
        screen.blit(self.compass_surface, COMPASS_POSITION)
        
        # Draw minimap border
        pygame.draw.rect(
            screen,
            UI_FONT_COLOR,
            (*MINIMAP_POSITION, MINIMAP_SIZE, MINIMAP_SIZE),
            2
        )
        
        # Draw boss warning if active
        if self.boss_warning_timer > 0 and self.boss_warning_text:
            text_rect = self.boss_warning_text.get_rect(center=(WIDTH//2, HEIGHT//4))
            screen.blit(self.boss_warning_text, text_rect)
            self.boss_warning_timer -= 1/60  # Assuming 60 FPS 
import pygame
import math
import os
import random
import time
import sys

# Set SDL to use the macOS Cocoa video driver before any pygame initialization
os.environ['SDL_VIDEODRIVER'] = 'cocoa'

# Initialize Pygame with all modules
pygame.init()
if not pygame.display.get_init():
    pygame.display.init()

# Default window size
WIDTH = 1024
HEIGHT = 720

# Initialize the display
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Doom-style Raycaster")
except pygame.error as e:
    print(f"Failed to initialize display: {e}")
    sys.exit(1)

# Try to switch to fullscreen after initial display is set up
try:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
except:
    print("Failed to switch to fullscreen, using windowed mode")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

FOV = math.pi / 3  # 60-degree field of view
NUM_RAYS = WIDTH  # Match the number of rays to screen width
MAX_DEPTH = 800

# Player settings
CELL_SIZE = 64  # Size of each maze cell in pixels
player_x = CELL_SIZE * 1.5  # Start in the middle of the first empty cell
player_y = CELL_SIZE * 1.5  # Start in the middle of the first empty cell
player_angle = 0
player_speed = 7  # Reduced speed for better control
rotation_speed = 0.1
MOUSE_SENSITIVITY = 0.002  # New mouse sensitivity setting
player_health = 10  # Player starts with 10 health
last_hit_time = 0  # For invulnerability frames
INVULNERABILITY_TIME = 1.0  # Seconds of invulnerability after being hit
kill_count = 0  # Track number of monsters killed

# Weapon settings
WEAPON_SCALE = 0.5
is_shooting = False
shoot_frame = 0
MAX_SHOOT_FRAMES = 3  # Reduced from 5 to 3 for faster shooting
SHOOT_COOLDOWN = 0.1  # Reduced from 0.2 to 0.1 for 10 shots per second
last_shot_time = 0  # Track last shot time

# Colors
SKY_COLOR = (20, 20, 30)  # Darker blue for dungeon atmosphere
FLOOR_COLOR = (40, 35, 30)  # Dark brown for dungeon floor
WALL_COLOR = (60, 55, 50)  # Dark gray for walls
WALL_HIGHLIGHT = (80, 75, 70)  # Lighter gray for wall highlights
WALL_SHADOW = (40, 35, 30)  # Darker gray for wall shadows
BLOOD_COLOR = (200, 0, 0, 128)  # Semi-transparent red

# Add after the player settings
current_level = 1
MAX_LEVEL = 5
level_completed = False
level_start_time = time.time()
LEVEL_TIME_LIMIT = 300  # 5 minutes per level

# Special areas in the maze
SPECIAL_AREAS = {
    'treasure': 2,  # Treasure room with extra health
    'trap': 3,      # Trap room with more monsters
    'boss': 4,      # Boss room
    'exit': 5       # Level exit
}

# Complex maze variations
MAPS = [
    # Level 1 - Basic maze
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # Level 2 - Larger maze with treasure room
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 2, 2, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 2, 2, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # Level 3 - Maze with trap rooms
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 3, 3, 3, 3, 3, 3, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 3, 3, 3, 3, 3, 3, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 3, 3, 3, 3, 3, 3, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 3, 3, 3, 3, 3, 3, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 3, 3, 3, 3, 3, 3, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # Level 4 - Maze with boss room
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 4, 4, 4, 4, 4, 4, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 4, 4, 4, 4, 4, 4, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 4, 4, 4, 4, 4, 4, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 4, 4, 4, 4, 4, 4, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 4, 4, 4, 4, 4, 4, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # Level 5 - Final maze with exit
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 5, 5, 5, 5, 5, 5, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 5, 5, 5, 5, 5, 5, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 5, 5, 5, 5, 5, 5, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 5, 5, 5, 5, 5, 5, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 5, 5, 5, 5, 5, 5, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
]

# Initialize the current map
MAP = MAPS[0]  # Start with level 1 map

# Function to get the current level map
def get_level_map(level):
    return MAPS[level - 1]  # Level 1 uses index 0

# Function to check special areas
def check_special_area(x, y):
    map_x = int(x / CELL_SIZE)
    map_y = int(y / CELL_SIZE)
    if 0 <= map_x < len(MAP) and 0 <= map_y < len(MAP[0]):
        cell_value = MAP[map_x][map_y]
        if cell_value in SPECIAL_AREAS.values():
            return cell_value
    return 0

# Function to handle special area effects
def handle_special_area(x, y):
    area_type = check_special_area(x, y)
    if area_type == SPECIAL_AREAS['treasure']:
        global player_health
        player_health = min(5, player_health + 1)  # Restore 1 health
    elif area_type == SPECIAL_AREAS['trap']:
        global monsters
        # Spawn extra monsters in trap room
        for _ in range(3):
            monsters.append(Monster(x + random.randint(-CELL_SIZE, CELL_SIZE),
                                  y + random.randint(-CELL_SIZE, CELL_SIZE)))
    elif area_type == SPECIAL_AREAS['boss']:
        # Spawn boss monster
        monsters.append(Monster(x, y, is_boss=True))
    elif area_type == SPECIAL_AREAS['exit']:
        global level_completed, current_level
        if current_level < MAX_LEVEL:
            level_completed = True
            current_level += 1
            reset_level()

# Function to reset level
def reset_level():
    global MAP, player_x, player_y, player_angle, monsters, health_hearts, last_spawn_time, last_heart_spawn_time, level_start_time, level_completed
    MAP = get_level_map(current_level)
    player_x = CELL_SIZE * 1.5
    player_y = CELL_SIZE * 1.5
    player_angle = 0
    monsters = []
    health_hearts = []
    last_spawn_time = time.time()
    last_heart_spawn_time = time.time()
    level_start_time = time.time()
    level_completed = False

# Wall texture patterns
WALL_TEXTURES = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

# Color map (RGB values for each wall)
COLORS = [
    [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)],
    [(255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0)],
    [(255, 0, 0), (0, 0, 0), (0, 255, 0), (0, 0, 0), (0, 0, 0), (0, 255, 0), (0, 0, 0), (255, 0, 0)],
    [(255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0)],
    [(255, 0, 0), (0, 0, 0), (0, 0, 255), (0, 0, 0), (0, 0, 0), (0, 0, 255), (0, 0, 0), (255, 0, 0)],
    [(255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0)],
    [(255, 0, 0), (0, 0, 0), (255, 255, 0), (0, 0, 0), (0, 0, 0), (255, 255, 0), (0, 0, 0), (255, 0, 0)],
    [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)]
]

# Game state
class GameState:
    RUNNING = 0
    PAUSED = 1
    GAME_OVER = 2
    TITLE = 3  # New state for title screen
    UPGRADE = 4  # New state for upgrade menu

# Monster settings
class Monster:
    def __init__(self, x, y, is_boss=False):
        self.x = x
        self.y = y
        self.health = 9 if is_boss else 3  # Boss has triple health
        self.size = CELL_SIZE if is_boss else CELL_SIZE // 2  # Boss is bigger
        self.color = (200, 0, 0) if is_boss else (150, 0, 0)  # Boss is darker red
        self.is_hit = False
        self.hit_timer = 0
        self.speed = 1.0 if is_boss else 1.5  # Boss is slower
        self.damage = 3 if is_boss else 1  # Boss deals triple damage
        self.last_attack_time = 0
        self.attack_cooldown = 1.0
        self.animation_time = 0
        self.animation_speed = 0.1
        self.visible = True
        self.images = []
        self.current_frame = 0
        self.is_boss = is_boss
        self.exp_value = EXP_PER_MONSTER['boss'] if is_boss else EXP_PER_MONSTER['normal']
        self.load_images()

    def load_images(self):
        try:
            # Create Images folder if it doesn't exist
            if not os.path.exists('Images'):
                os.makedirs('Images')
                print("Created Images folder. Please add monster animation images.")
            
            # Try to load 8 frames first
            frame_count = 8
            while frame_count > 0:
                image_path = os.path.join('Images', f'slime{frame_count}.png')
                if os.path.exists(image_path):
                    break
                frame_count -= 1
            
            if frame_count == 0:
                print("No monster images found. Using fallback monster graphics.")
                return
            
            # Load all available frames
            for i in range(1, frame_count + 1):
                image_path = os.path.join('Images', f'slime{i}.png')
                if os.path.exists(image_path):
                    image = pygame.image.load(image_path)
                    image = image.convert_alpha()
                    image = pygame.transform.scale(image, (self.size, self.size))
                    self.images.append(image)
            
            print(f"Loaded {len(self.images)} monster animation frames from Images folder")
            
        except Exception as e:
            print(f"Error loading monster images: {e}")
            self.images = []

    def draw(self, screen, x, y, size):
        if not self.visible:
            return
            
        # Update animation
        self.animation_time += self.animation_speed
        if self.animation_time >= 0.2 and self.images:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)
        
        if self.images:
            # Draw the current animation frame
            scaled_size = int(size)
            scaled_image = pygame.transform.scale(self.images[self.current_frame], 
                                               (scaled_size, scaled_size))
            
            # Apply hit effect
            if self.is_hit:
                hit_surface = pygame.Surface(scaled_image.get_size(), pygame.SRCALPHA)
                hit_surface.fill((255, 0, 0, 128))
                scaled_image.blit(hit_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Draw the image
            screen.blit(scaled_image, (x - scaled_size//2, y - scaled_size//2))
        else:
            # Fallback to drawn monster
            color = (255, 100, 100) if self.is_hit else self.color
            pygame.draw.circle(screen, color, (int(x), int(y)), int(size))
            
            # Draw eyes
            eye_color = (255, 0, 0) if self.is_hit else (255, 200, 0)
            left_eye = (x - size/3, y - size/4)
            right_eye = (x + size/3, y - size/4)
            
            for eye_pos in [left_eye, right_eye]:
                pygame.draw.circle(screen, eye_color, 
                                 (int(eye_pos[0]), int(eye_pos[1])), 
                                 int(size/4))
                pygame.draw.circle(screen, (0, 0, 0), 
                                 (int(eye_pos[0]), int(eye_pos[1])), 
                                 int(size/8))
        
        # Draw health bar
        health_width = size * (self.health / (9 if self.is_boss else 3))
        health_height = 5
        health_y = y + size + 5
        
        pygame.draw.rect(screen, (100, 0, 0),
                        (x - size/2, health_y, size, health_height))
        pygame.draw.rect(screen, (0, 255, 0),
                        (x - size/2, health_y, health_width, health_height))

# Health heart settings
class HealthHeart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = CELL_SIZE // 2
        self.color = (255, 0, 0)  # Red color for heart
        self.pulse_scale = 1.0
        self.pulse_speed = 0.1
        self.pulse_time = 0
        self.images = []
        self.current_frame = 0
        self.animation_time = 0
        self.animation_speed = 0.1
        self.load_images()

    def load_images(self):
        try:
            # Load the GIF file from the Images folder
            gif_path = os.path.join('Images', 'Pixel Heart Animation 32x32.gif')
            if os.path.exists(gif_path):
                # Load the GIF and convert it to a list of surfaces
                gif = pygame.image.load(gif_path)
                # Get the number of frames from the GIF
                frame_count = getattr(gif, 'n_frames', 1)
                
                # Extract each frame
                for i in range(frame_count):
                    gif.seek(i)
                    frame = gif.convert_alpha()
                    frame = pygame.transform.scale(frame, (self.size, self.size))
                    self.images.append(frame)
                
                print(f"Loaded {len(self.images)} heart animation frames from {gif_path}")
            else:
                print(f"Heart GIF not found at {gif_path}. Using fallback heart graphics.")
        except Exception as e:
            print(f"Error loading heart images: {e}")
            self.images = []

    def draw(self, screen, x, y, size):
        # Update pulse animation
        self.pulse_time += self.pulse_speed
        self.pulse_scale = 1.0 + math.sin(self.pulse_time) * 0.2
        
        if self.images:
            # Update animation
            self.animation_time += self.animation_speed
            if self.animation_time >= 0.2:
                self.animation_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.images)
            
            # Draw the current frame
            scaled_size = int(size * self.pulse_scale)
            scaled_image = pygame.transform.scale(self.images[self.current_frame], 
                                               (scaled_size, scaled_size))
            screen.blit(scaled_image, (x - scaled_size//2, y - scaled_size//2))
        else:
            # Fallback to drawn heart
            heart_color = (255, 0, 0)
            scaled_size = size * self.pulse_scale
            
            # Draw heart shape using rectangles and circles
            center_x = x
            center_y = y
            
            # Draw the two circles for the top of the heart
            pygame.draw.circle(screen, heart_color, 
                             (int(center_x - scaled_size/4), int(center_y - scaled_size/4)), 
                             int(scaled_size/4))
            pygame.draw.circle(screen, heart_color, 
                             (int(center_x + scaled_size/4), int(center_y - scaled_size/4)), 
                             int(scaled_size/4))
            
            # Draw the triangle for the bottom of the heart
            points = [
                (center_x, center_y + scaled_size/4),
                (center_x - scaled_size/4, center_y - scaled_size/4),
                (center_x + scaled_size/4, center_y - scaled_size/4)
            ]
            pygame.draw.polygon(screen, heart_color, points)

# Add after the player settings
# Progression system
player_level = 1
player_exp = 0
exp_to_next_level = 100
base_damage = 1
base_health = 5
base_speed = 7
upgrade_points = 0

# Monster settings per level
MONSTERS_PER_LEVEL = {
    1: 10,  # Level 1: 10 monsters
    2: 15,  # Level 2: 15 monsters
    3: 20,  # Level 3: 20 monsters
    4: 25,  # Level 4: 25 monsters
    5: 30   # Level 5: 30 monsters
}

# Experience points per monster type
EXP_PER_MONSTER = {
    'normal': 10,
    'boss': 30
}

# Function to handle level up
def level_up():
    global player_level, player_exp, exp_to_next_level, upgrade_points
    player_level += 1
    player_exp = 0
    exp_to_next_level = int(exp_to_next_level * 1.5)  # Increase exp needed for next level
    upgrade_points += 2  # Give 2 upgrade points per level
    show_upgrade_menu()

# Function to show upgrade menu
def show_upgrade_menu():
    global game_state
    game_state = GameState.UPGRADE
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)

# Function to draw upgrade menu
def draw_upgrade_menu():
    # Create a dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Title
    title_font = pygame.font.Font(None, 74)
    title_text = title_font.render("LEVEL UP!", True, (255, 255, 0))
    title_rect = title_text.get_rect(center=(WIDTH/2, HEIGHT/4))
    screen.blit(title_text, title_rect)
    
    # Available points
    points_font = pygame.font.Font(None, 48)
    points_text = points_font.render(f"Upgrade Points: {upgrade_points}", True, (255, 255, 255))
    points_rect = points_text.get_rect(center=(WIDTH/2, HEIGHT/3))
    screen.blit(points_text, points_rect)
    
    # Current stats
    stats_font = pygame.font.Font(None, 36)
    stats = [
        f"Damage: {base_damage}",
        f"Health: {base_health}",
        f"Speed: {base_speed}"
    ]
    
    for i, stat in enumerate(stats):
        stat_text = stats_font.render(stat, True, (200, 200, 200))
        stat_rect = stat_text.get_rect(center=(WIDTH/2, HEIGHT/2 + i * 40))
        screen.blit(stat_text, stat_rect)
    
    # Special abilities
    abilities_font = pygame.font.Font(None, 32)
    abilities = [
        ("4 - Double Shot (3 points)", "double_shot"),
        ("5 - Health Regeneration (2 points)", "health_regen"),
        ("6 - Slow Time (4 points)", "slow_time"),
        ("7 - Explosive Shot (3 points)", "explosive_shot")
    ]
    
    for i, (text, ability_name) in enumerate(abilities):
        color = (200, 200, 200) if not SPECIAL_ABILITIES[ability_name] else (0, 255, 0)
        ability_text = abilities_font.render(text, True, color)
        ability_rect = ability_text.get_rect(center=(WIDTH/2, HEIGHT * 2/3 + 120 + i * 40))
        screen.blit(ability_text, ability_rect)
    
    # Upgrade buttons
    button_font = pygame.font.Font(None, 32)
    buttons = [
        ("1 - Increase Damage", (WIDTH/2, HEIGHT * 2/3)),
        ("2 - Increase Health", (WIDTH/2, HEIGHT * 2/3 + 40)),
        ("3 - Increase Speed", (WIDTH/2, HEIGHT * 2/3 + 80)),
        ("Enter - Continue (You can save points for later)", (WIDTH/2, HEIGHT * 3/4 + 280))
    ]
    
    for text, pos in buttons:
        button_text = button_font.render(text, True, (200, 200, 200))
        button_rect = button_text.get_rect(center=pos)
        screen.blit(button_text, button_rect)

# Function to handle upgrades
def handle_upgrade(key):
    global base_damage, base_health, base_speed, upgrade_points, game_state, SPECIAL_ABILITIES
    
    if key == pygame.K_1 and upgrade_points > 0:  # Increase damage
        base_damage += 1
        upgrade_points -= 1
    elif key == pygame.K_2 and upgrade_points > 0:  # Increase health
        base_health += 1
        upgrade_points -= 1
    elif key == pygame.K_3 and upgrade_points > 0:  # Increase speed
        base_speed += 0.5
        upgrade_points -= 1
    elif key == pygame.K_4 and upgrade_points >= 3 and not SPECIAL_ABILITIES['double_shot']:
        SPECIAL_ABILITIES['double_shot'] = True
        upgrade_points -= 3
    elif key == pygame.K_5 and upgrade_points >= 2 and not SPECIAL_ABILITIES['health_regen']:
        SPECIAL_ABILITIES['health_regen'] = True
        upgrade_points -= 2
    elif key == pygame.K_6 and upgrade_points >= 4 and not SPECIAL_ABILITIES['slow_time']:
        SPECIAL_ABILITIES['slow_time'] = True
        upgrade_points -= 4
    elif key == pygame.K_7 and upgrade_points >= 3 and not SPECIAL_ABILITIES['explosive_shot']:
        SPECIAL_ABILITIES['explosive_shot'] = True
        upgrade_points -= 3
    elif key == pygame.K_RETURN:  # Continue
        game_state = GameState.RUNNING
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

# Add after the player settings
NUM_MONSTERS = float('inf')  # Remove monster limit
monsters = []
last_spawn_time = time.time()
last_wave_time = time.time()
SPAWN_INTERVAL = 1.0  # Spawn new monsters every 1 second
WAVE_INTERVAL = 5.0  # Spawn wave every 5 seconds
WAVE_SIZE = 5  # Number of monsters in each wave

# Add after monster settings
health_hearts = []
last_heart_spawn_time = time.time()
HEART_SPAWN_INTERVAL = 5.0  # Spawn new heart every 5 seconds

# Add after the player settings
# Special abilities
SPECIAL_ABILITIES = {
    'double_shot': False,  # Shoot two projectiles at once
    'health_regen': False,  # Regenerate health over time
    'slow_time': False,    # Slow down time temporarily
    'explosive_shot': False  # Shots explode on impact
}

# Ability cooldowns and timers
ability_cooldowns = {
    'double_shot': 0,
    'health_regen': 0,
    'slow_time': 0,
    'explosive_shot': 0
}

ABILITY_COOLDOWN = 30  # 30 seconds cooldown
SLOW_TIME_DURATION = 5  # 5 seconds duration
HEALTH_REGEN_RATE = 0.1  # Health per second
MIN_SPAWN_DISTANCE = 200  # Minimum distance from player for monster spawns

def spawn_monsters():
    global monsters, last_spawn_time, last_wave_time, game_state
    current_time = time.time()
    
    # Determine spawn interval based on game state
    spawn_interval = SPAWN_INTERVAL / 5 if game_state == GameState.PAUSED else SPAWN_INTERVAL
    
    # Regular monster spawn
    if current_time - last_spawn_time >= spawn_interval:
        max_attempts = 10  # Limit spawn attempts
        for _ in range(max_attempts):
            x = random.randint(1, len(MAP)-2) * CELL_SIZE + CELL_SIZE//2
            y = random.randint(1, len(MAP[0])-2) * CELL_SIZE + CELL_SIZE//2
            
            # Check distance from player
            dx = x - player_x
            dy = y - player_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance >= MIN_SPAWN_DISTANCE:
                map_x = int(x / CELL_SIZE)
                map_y = int(y / CELL_SIZE)
                if MAP[map_x][map_y] == 0:
                    monsters.append(Monster(x, y))
                    last_spawn_time = current_time
                    break
    
    # Wave spawn
    if current_time - last_wave_time >= WAVE_INTERVAL:
        # Spawn wave of monsters
        for _ in range(WAVE_SIZE - 1):  # Spawn regular monsters
            max_attempts = 10
            for _ in range(max_attempts):
                x = random.randint(1, len(MAP)-2) * CELL_SIZE + CELL_SIZE//2
                y = random.randint(1, len(MAP[0])-2) * CELL_SIZE + CELL_SIZE//2
                
                # Check distance from player
                dx = x - player_x
                dy = y - player_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance >= MIN_SPAWN_DISTANCE:
                    map_x = int(x / CELL_SIZE)
                    map_y = int(y / CELL_SIZE)
                    if MAP[map_x][map_y] == 0:
                        monsters.append(Monster(x, y))
                        break
        
        # Spawn boss monster
        max_attempts = 10
        for _ in range(max_attempts):
            x = random.randint(1, len(MAP)-2) * CELL_SIZE + CELL_SIZE//2
            y = random.randint(1, len(MAP[0])-2) * CELL_SIZE + CELL_SIZE//2
            
            # Check distance from player
            dx = x - player_x
            dy = y - player_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance >= MIN_SPAWN_DISTANCE:
                map_x = int(x / CELL_SIZE)
                map_y = int(y / CELL_SIZE)
                if MAP[map_x][map_y] == 0:
                    monsters.append(Monster(x, y, is_boss=True))
                    break
        
        last_wave_time = current_time

def spawn_health_heart():
    global health_hearts, last_heart_spawn_time
    current_time = time.time()
    
    # Only spawn if enough time has passed and we're under the heart limit
    if current_time - last_heart_spawn_time >= HEART_SPAWN_INTERVAL:
        # Random position in the map
        while True:
            x = random.randint(1, len(MAP)-2) * CELL_SIZE + CELL_SIZE//2
            y = random.randint(1, len(MAP[0])-2) * CELL_SIZE + CELL_SIZE//2
            map_x = int(x / CELL_SIZE)
            map_y = int(y / CELL_SIZE)
            if MAP[map_x][map_y] == 0:
                health_hearts.append(HealthHeart(x, y))
                last_heart_spawn_time = current_time
                break

def update_monsters():
    global player_health, last_hit_time, monsters
    current_time = time.time()
    
    # Remove dead monsters
    monsters = [monster for monster in monsters if monster.health > 0]
    
    for monster in monsters:
        # Calculate direction to player
        dx = player_x - monster.x
        dy = player_y - monster.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:  # Prevent division by zero
            # Normalize direction
            dx = dx / distance
            dy = dy / distance
            
            # Move monster towards player
            new_x = monster.x + dx * monster.speed
            new_y = monster.y + dy * monster.speed
            
            # Check if new position is valid (not in a wall)
            map_x = int(new_x / CELL_SIZE)
            map_y = int(new_y / CELL_SIZE)
            
            if (0 <= map_x < len(MAP) and 
                0 <= map_y < len(MAP[0]) and 
                MAP[map_x][map_y] == 0):
                monster.x = new_x
                monster.y = new_y
            
            # Check for collision with player
            if distance < CELL_SIZE * 0.5:  # Close enough to attack
                if current_time - monster.last_attack_time >= monster.attack_cooldown:
                    if current_time - last_hit_time >= INVULNERABILITY_TIME:
                        player_health -= monster.damage
                        last_hit_time = current_time
                        monster.last_attack_time = current_time

def update_health_hearts():
    global player_health, health_hearts
    current_time = time.time()
    
    for heart in health_hearts[:]:  # Use slice copy to allow removal during iteration
        # Update heart animation
        heart.pulse_time += heart.pulse_speed
        heart.pulse_scale = 1.0 + math.sin(heart.pulse_time) * 0.2
        
        # Calculate distance to player
        dx = player_x - heart.x
        dy = player_y - heart.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Check for collection
        if distance < CELL_SIZE * 0.5:  # Close enough to collect
            player_health = 5  # Restore full health
            health_hearts.remove(heart)

def draw_weapon(shooting=False, frame=0):
    weapon_color = (70, 70, 70)  # Gun metal gray
    
    # Base weapon dimensions
    weapon_width = 100
    weapon_height = 150
    
    # Position at the bottom center of the screen
    weapon_x = WIDTH // 2 - weapon_width // 2
    weapon_y = HEIGHT - weapon_height
    
    if shooting:
        # Modify position for recoil animation
        recoil = math.sin(frame * math.pi / MAX_SHOOT_FRAMES) * 20
        weapon_y += recoil
    
    # Draw the weapon
    # Main body
    pygame.draw.rect(screen, weapon_color, (weapon_x, weapon_y, weapon_width, weapon_height))
    
    # Barrel
    barrel_width = 30
    barrel_height = 60
    barrel_x = weapon_x + (weapon_width - barrel_width) // 2
    barrel_y = weapon_y - barrel_height // 2
    pygame.draw.rect(screen, (50, 50, 50), (barrel_x, barrel_y, barrel_width, barrel_height))
    
    # Muzzle flash when shooting
    if shooting and frame < MAX_SHOOT_FRAMES // 2:
        flash_color = (255, 200, 0)
        flash_points = [
            (barrel_x + barrel_width // 2, barrel_y - 30),
            (barrel_x - 20, barrel_y),
            (barrel_x + barrel_width + 20, barrel_y)
        ]
        pygame.draw.polygon(screen, flash_color, flash_points)

def draw_kill_counter():
    font = pygame.font.Font(None, 36)
    text = font.render(f'Kills: {kill_count}', True, (255, 255, 255))
    screen.blit(text, (WIDTH - 150, 20))

def draw_blood_overlay():
    if player_health < 5:
        # Create a surface for the blood effect
        blood_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # Calculate opacity based on health
        opacity = int((1 - player_health/5) * 128)  # Max opacity of 128
        blood_color = (*BLOOD_COLOR[:3], opacity)
        blood_surface.fill(blood_color)
        screen.blit(blood_surface, (0, 0))

def cast_rays():
    # Draw sky and floor with gradient effect
    for y in range(HEIGHT):
        if y < HEIGHT // 2:
            factor = y / (HEIGHT // 2)
            color = tuple(int(c * (1 - factor * 0.5)) for c in SKY_COLOR)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))
        else:
            factor = (y - HEIGHT // 2) / (HEIGHT // 2)
            color = tuple(int(c * (1 + factor * 0.3)) for c in FLOOR_COLOR)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))
    
    depth_buffer = [float('inf')] * WIDTH
    
    for i in range(NUM_RAYS):
        angle = player_angle + (i - NUM_RAYS // 2) * (FOV / NUM_RAYS)
        
        ray_x = player_x
        ray_y = player_y
        ray_length = 0
        hit_wall = False
        wall_color = WALL_COLOR
        wall_highlight = WALL_HIGHLIGHT
        wall_shadow = WALL_SHADOW
        
        while not hit_wall and ray_length < MAX_DEPTH:
            ray_length += 1
            ray_x = player_x + ray_length * math.cos(angle)
            ray_y = player_y + ray_length * math.sin(angle)
            
            map_x = int(ray_x / CELL_SIZE)
            map_y = int(ray_y / CELL_SIZE)
            
            if map_x < 0 or map_x >= len(MAP) or map_y < 0 or map_y >= len(MAP[0]):
                hit_wall = True
            elif MAP[map_x][map_y] == 1:
                hit_wall = True
                # Get texture coordinates
                hit_x = ray_x % CELL_SIZE
                hit_y = ray_y % CELL_SIZE
                
                # Determine wall texture based on hit position
                texture_x = int(hit_x / CELL_SIZE * 8)
                texture_y = int(hit_y / CELL_SIZE * 8)
                
                if WALL_TEXTURES[texture_x][texture_y] == 1:
                    wall_color = WALL_SHADOW
                else:
                    wall_color = WALL_COLOR
        
        depth_buffer[i] = ray_length
        
        distance = ray_length * math.cos(angle - player_angle)
        wall_height = min(HEIGHT, (HEIGHT / distance) * 64)
        wall_top = (HEIGHT - wall_height) // 2
        wall_bottom = wall_top + wall_height
        
        # Apply distance-based shading and lighting
        shade_factor = max(0.2, min(1.0, 1.0 - distance * 0.001))
        shaded_color = tuple(int(c * shade_factor) for c in wall_color)
        
        # Draw wall slice with texture
        pygame.draw.rect(screen, shaded_color, (i, wall_top, 1, wall_bottom - wall_top))
        
        # Add wall highlights and shadows
        if i % 4 == 0:
            highlight_height = wall_height // 8
            pygame.draw.rect(screen, wall_highlight, 
                           (i, wall_top, 1, highlight_height))
            pygame.draw.rect(screen, wall_shadow, 
                           (i, wall_bottom - highlight_height, 1, highlight_height))
    
    # Render monsters and health hearts with visibility check
    visible_objects = []
    
    # Add monsters to visible objects
    for monster in monsters:
        dx = monster.x - player_x
        dy = monster.y - player_y
        monster_angle = math.atan2(dy, dx)
        relative_angle = monster_angle - player_angle
        
        if relative_angle < -math.pi:
            relative_angle += 2 * math.pi
        elif relative_angle > math.pi:
            relative_angle -= 2 * math.pi
            
        if abs(relative_angle) < FOV / 2:
            distance = math.sqrt(dx*dx + dy*dy)
            monster_screen_x = int((0.5 + relative_angle / FOV) * WIDTH)
            monster_size = min(HEIGHT, (HEIGHT / distance) * 64)
            
            # Check if monster is in front of wall and within reasonable distance
            if distance < depth_buffer[monster_screen_x] and distance < MAX_DEPTH * 0.8:
                monster.visible = True
                monster_top = (HEIGHT - monster_size) // 2
                visible_objects.append((distance, monster, monster_screen_x, monster_top + monster_size//2, monster_size//2))
            else:
                monster.visible = False
    
    # Add health hearts to visible objects
    for heart in health_hearts:
        dx = heart.x - player_x
        dy = heart.y - player_y
        heart_angle = math.atan2(dy, dx)
        relative_angle = heart_angle - player_angle
        
        if relative_angle < -math.pi:
            relative_angle += 2 * math.pi
        elif relative_angle > math.pi:
            relative_angle -= 2 * math.pi
            
        if abs(relative_angle) < FOV / 2:
            distance = math.sqrt(dx*dx + dy*dy)
            heart_screen_x = int((0.5 + relative_angle / FOV) * WIDTH)
            heart_size = min(HEIGHT, (HEIGHT / distance) * 64)
            
            # Check if heart is in front of wall and within reasonable distance
            if distance < depth_buffer[heart_screen_x] and distance < MAX_DEPTH * 0.8:
                heart_top = (HEIGHT - heart_size) // 2
                visible_objects.append((distance, heart, heart_screen_x, heart_top + heart_size//2, heart_size//2))
    
    # Sort objects by distance (back to front) using the first element of each tuple (distance)
    visible_objects.sort(key=lambda x: x[0], reverse=True)
    
    # Draw all visible objects
    for _, obj, screen_x, screen_y, size in visible_objects:
        if isinstance(obj, Monster):
            obj.draw(screen, screen_x, screen_y, size)
        else:  # HealthHeart
            obj.draw(screen, screen_x, screen_y, size)

def handle_shooting():
    global monsters, kill_count, is_shooting, shoot_frame, last_shot_time, player_exp, player_level, exp_to_next_level, ability_cooldowns
    
    current_time = time.time()
    if current_time - last_shot_time < SHOOT_COOLDOWN:
        return
    
    # Handle double shot
    if SPECIAL_ABILITIES['double_shot'] and current_time - ability_cooldowns['double_shot'] >= ABILITY_COOLDOWN:
        # Shoot two projectiles at slightly different angles
        angles = [player_angle - 0.1, player_angle + 0.1]
        for angle in angles:
            shoot_projectile(angle, explosive=SPECIAL_ABILITIES['explosive_shot'])
        ability_cooldowns['double_shot'] = current_time
    else:
        # Normal shot
        shoot_projectile(player_angle, explosive=SPECIAL_ABILITIES['explosive_shot'])
    
    is_shooting = True
    shoot_frame = 0
    last_shot_time = current_time

def shoot_projectile(angle, explosive=False):
    global monsters, kill_count, player_exp, player_level, exp_to_next_level
    
    ray_x = player_x
    ray_y = player_y
    ray_length = 0
    hit_monster = False
    
    while not hit_monster and ray_length < MAX_DEPTH:
        ray_length += 1
        ray_x = player_x + ray_length * math.cos(angle)
        ray_y = player_y + ray_length * math.sin(angle)
        
        for monster in monsters:
            dx = ray_x - monster.x
            dy = ray_y - monster.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < monster.size:
                monster.health -= base_damage
                monster.is_hit = True
                monster.hit_timer = 10
                
                # Handle explosive shot
                if explosive:
                    for nearby_monster in monsters:
                        if nearby_monster != monster:
                            nx = nearby_monster.x - monster.x
                            ny = nearby_monster.y - monster.y
                            dist = math.sqrt(nx*nx + ny*ny)
                            if dist < 100:  # Explosion radius
                                nearby_monster.health -= base_damage // 2
                                nearby_monster.is_hit = True
                                nearby_monster.hit_timer = 10
                
                if monster.health <= 0:
                    monsters.remove(monster)
                    kill_count += 1
                    player_exp += monster.exp_value
                    if player_exp >= exp_to_next_level:
                        level_up()
                hit_monster = True
                break

def handle_input():
    global player_x, player_y, player_angle, is_shooting, shoot_frame
    
    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    
    # Handle mouse movement for camera rotation
    mouse_rel_x, _ = pygame.mouse.get_rel()
    player_angle += mouse_rel_x * MOUSE_SENSITIVITY
    
    # Handle shooting
    if mouse_buttons[0] and not is_shooting:  # Left mouse button
        handle_shooting()
    
    # Update shooting animation
    if is_shooting:
        shoot_frame += 1
        if shoot_frame >= MAX_SHOOT_FRAMES:
            is_shooting = False
            shoot_frame = 0
    
    # Update monster hit effects
    for monster in monsters:
        if monster.is_hit:
            monster.hit_timer -= 1
            if monster.hit_timer <= 0:
                monster.is_hit = False
    
    # Movement
    next_x = player_x
    next_y = player_y
    
    if keys[pygame.K_w]:
        next_x += player_speed * math.cos(player_angle)
        next_y += player_speed * math.sin(player_angle)
    if keys[pygame.K_s]:
        next_x -= player_speed * math.cos(player_angle)
        next_y -= player_speed * math.sin(player_angle)
    if keys[pygame.K_a]:
        next_x += player_speed * math.cos(player_angle - math.pi/2)
        next_y += player_speed * math.sin(player_angle - math.pi/2)
    if keys[pygame.K_d]:
        next_x += player_speed * math.cos(player_angle + math.pi/2)
        next_y += player_speed * math.sin(player_angle + math.pi/2)
    
    # Check if the next position is valid (not inside a wall)
    next_map_x = int(next_x / CELL_SIZE)
    next_map_y = int(next_y / CELL_SIZE)
    
    if (0 <= next_map_x < len(MAP) and 
        0 <= next_map_y < len(MAP[0]) and 
        MAP[next_map_x][next_map_y] == 0):
        player_x = next_x
        player_y = next_y
        # Check for special areas
        handle_special_area(player_x, player_y)

def draw_player_health():
    health_width = 200
    health_height = 20
    x = 20
    y = 20
    
    # Draw background (red)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, health_width, health_height))
    # Draw current health (green)
    current_health_width = (health_width * player_health) / 5
    pygame.draw.rect(screen, (0, 255, 0), (x, y, current_health_width, health_height))

def draw_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render('Game Over - Press R to Restart', True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)

def draw_health_heart(heart, screen_x, screen_y, size):
    heart.draw(screen, screen_x, screen_y, size)

def reset_game():
    global player_health, player_x, player_y, player_angle, monsters, health_hearts, last_spawn_time, last_heart_spawn_time, kill_count, current_level, MAP, player_level, player_exp, exp_to_next_level, upgrade_points
    player_health = base_health
    player_x = CELL_SIZE * 1.5
    player_y = CELL_SIZE * 1.5
    player_angle = 0
    monsters = []
    health_hearts = []
    last_spawn_time = time.time()
    last_heart_spawn_time = time.time()
    kill_count = 0
    current_level = 1
    player_level = 1
    player_exp = 0
    exp_to_next_level = 100
    upgrade_points = 0
    MAP = get_level_map(current_level)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

def draw_pause_screen():
    # Create a dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Load horror font or use default
    try:
        font = pygame.font.Font('horror.ttf', 48)
    except:
        font = pygame.font.Font(None, 48)
    
    # Render creepy message
    messages = [
        "ONLY WEAKS NEED PAUSE",
        "YOU WILL WISH THAT YOU DIDN'T DO IT",
        "THEY ARE COMING..."
    ]
    
    for i, message in enumerate(messages):
        text = font.render(message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50 + i * 60))
        screen.blit(text, text_rect)
    
    # Add "Press P to continue" message
    continue_font = pygame.font.Font(None, 36)
    continue_text = continue_font.render("Press P to continue", True, (200, 0, 0))
    continue_rect = continue_text.get_rect(center=(WIDTH/2, HEIGHT - 50))
    screen.blit(continue_text, continue_rect)

def draw_title_screen():
    # Create a dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Title text
    title_font = pygame.font.Font(None, 100)
    title_text = title_font.render("SHADOW MAZE", True, (255, 0, 0))
    title_rect = title_text.get_rect(center=(WIDTH/2, HEIGHT/3))
    screen.blit(title_text, title_rect)
    
    # Subtitle text
    subtitle_font = pygame.font.Font(None, 50)
    subtitle_text = subtitle_font.render("A Raycasting Nightmare", True, (200, 0, 0))
    subtitle_rect = subtitle_text.get_rect(center=(WIDTH/2, HEIGHT/3 + 70))
    screen.blit(subtitle_text, subtitle_rect)
    
    # Start prompt
    prompt_font = pygame.font.Font(None, 36)
    prompt_text = prompt_font.render("Press any key to start", True, (255, 255, 255))
    prompt_rect = prompt_text.get_rect(center=(WIDTH/2, HEIGHT * 2/3))
    screen.blit(prompt_text, prompt_rect)
    
    # Controls info
    controls_font = pygame.font.Font(None, 24)
    controls = [
        "WASD - Move",
        "Mouse - Look around",
        "Left Click - Shoot",
        "P - Pause",
        "F - Toggle Fullscreen",
        "ESC - Quit"
    ]
    
    for i, control in enumerate(controls):
        control_text = controls_font.render(control, True, (200, 200, 200))
        control_rect = control_text.get_rect(center=(WIDTH/2, HEIGHT * 3/4 + i * 30))
        screen.blit(control_text, control_rect)

def initialize_game():
    global screen, clock, player_health, player_x, player_y, player_angle, monsters, health_hearts, last_spawn_time, last_heart_spawn_time, kill_count, game_state
    
    try:
        # Initialize game variables
        clock = pygame.time.Clock()
        player_health = 5
        player_x = CELL_SIZE * 1.5
        player_y = CELL_SIZE * 1.5
        player_angle = 0
        monsters = []
        health_hearts = []
        last_spawn_time = time.time()
        last_heart_spawn_time = time.time()
        kill_count = 0
        game_state = GameState.RUNNING
        
        # Initial monster spawn
        spawn_monsters()
        
        return True
    except Exception as e:
        print(f"Error initializing game: {e}")
        return False

def draw_level_info():
    font = pygame.font.Font(None, 36)
    level_text = font.render(f'Level: {player_level} ({player_exp}/{exp_to_next_level} EXP)', True, (255, 255, 255))
    time_left = max(0, LEVEL_TIME_LIMIT - (time.time() - level_start_time))
    time_text = font.render(f'Time: {int(time_left)}', True, (255, 255, 255))
    screen.blit(level_text, (20, 60))
    screen.blit(time_text, (20, 100))

def main():
    global game_state, current_level, level_completed, player_health, player_speed, ability_cooldowns
    
    if not initialize_game():
        print("Failed to initialize game. Exiting...")
        pygame.quit()
        sys.exit(1)
    
    running = True
    game_state = GameState.TITLE
    last_health_regen = time.time()
    slow_time_active = False
    slow_time_end = 0
    
    while running:
        current_time = time.time()
        
        # Handle health regeneration
        if SPECIAL_ABILITIES['health_regen'] and current_time - last_health_regen >= 1.0:
            player_health = min(base_health, player_health + HEALTH_REGEN_RATE)
            last_health_regen = current_time
        
        # Handle slow time
        if SPECIAL_ABILITIES['slow_time'] and pygame.key.get_pressed()[pygame.K_SPACE]:
            if current_time - ability_cooldowns['slow_time'] >= ABILITY_COOLDOWN:
                slow_time_active = True
                slow_time_end = current_time + SLOW_TIME_DURATION
                ability_cooldowns['slow_time'] = current_time
        
        if slow_time_active and current_time >= slow_time_end:
            slow_time_active = False
        
        # Rest of the main game loop...
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == GameState.TITLE:
                        running = False
                    else:
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
                        running = False
                elif event.key == pygame.K_f:
                    current_flags = pygame.display.get_window_flags()
                    if current_flags & pygame.FULLSCREEN:
                        pygame.display.set_mode((1024, 720))
                    else:
                        pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                elif event.key == pygame.K_r and game_state == GameState.GAME_OVER:
                    reset_game()
                    game_state = GameState.RUNNING
                elif event.key == pygame.K_p:
                    if game_state == GameState.RUNNING:
                        game_state = GameState.PAUSED
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
                    elif game_state == GameState.PAUSED:
                        game_state = GameState.RUNNING
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                elif game_state == GameState.TITLE:
                    game_state = GameState.RUNNING
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                elif game_state == GameState.UPGRADE:
                    handle_upgrade(event.key)
        
        # Apply slow time effect
        if slow_time_active:
            pygame.time.delay(50)  # Slow down the game
        
        # Rest of the game loop...
        screen.fill((0, 0, 0))
        
        if game_state == GameState.TITLE:
            draw_title_screen()
        elif game_state == GameState.RUNNING:
            handle_input()
            spawn_monsters()
            spawn_health_heart()
            update_monsters()
            update_health_hearts()
            
            if player_health <= 0:
                game_state = GameState.GAME_OVER
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
            
            cast_rays()
            draw_weapon(is_shooting, shoot_frame)
            draw_player_health()
            draw_kill_counter()
            draw_blood_overlay()
            draw_level_info()
            
            # Check for level completion
            if level_completed:
                reset_level()
            
            # Check for time limit
            if time.time() - level_start_time > LEVEL_TIME_LIMIT:
                game_state = GameState.GAME_OVER
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
        elif game_state == GameState.PAUSED:
            cast_rays()
            draw_weapon(is_shooting, shoot_frame)
            draw_player_health()
            draw_kill_counter()
            draw_blood_overlay()
            draw_level_info()
            draw_pause_screen()
        elif game_state == GameState.GAME_OVER:
            cast_rays()
            draw_weapon(is_shooting, shoot_frame)
            draw_player_health()
            draw_kill_counter()
            draw_blood_overlay()
            draw_level_info()
            draw_game_over()
        elif game_state == GameState.UPGRADE:
            draw_upgrade_menu()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    pygame.quit()

if __name__ == "__main__":
    main() 
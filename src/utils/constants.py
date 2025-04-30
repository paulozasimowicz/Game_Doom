import math

# Window settings
WIDTH = 1024
HEIGHT = 720
FOV = math.pi / 3  # 60-degree field of view
NUM_RAYS = WIDTH  # Match the number of rays to screen width
MAX_DEPTH = 800

# Player settings
CELL_SIZE = 64  # Size of each maze cell in pixels
player_speed = 7  # Reduced speed for better control
rotation_speed = 0.1
MOUSE_SENSITIVITY = 0.002  # Mouse sensitivity setting
INVULNERABILITY_TIME = 1.0  # Seconds of invulnerability after being hit

# Weapon settings
WEAPON_SCALE = 0.5
MAX_SHOOT_FRAMES = 3  # Reduced from 5 to 3 for faster shooting
SHOOT_COOLDOWN = 0.1  # Reduced from 0.2 to 0.1 for 10 shots per second

# Game maps
MAPS = [
    # Level 1
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    # Level 2
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
]

# Colors
SKY_COLOR = (20, 20, 30)  # Darker blue for dungeon atmosphere
FLOOR_COLOR = (40, 35, 30)  # Dark brown for dungeon floor
WALL_COLOR = (60, 55, 50)  # Dark gray for walls
WALL_HIGHLIGHT = (80, 75, 70)  # Lighter gray for wall highlights
WALL_SHADOW = (40, 35, 30)  # Darker gray for wall shadows
BLOOD_COLOR = (200, 0, 0, 128)  # Semi-transparent red

# Game settings
MAX_LEVEL = 5
LEVEL_TIME_LIMIT = 300  # 5 minutes per level
MIN_SPAWN_DISTANCE = 200  # Minimum distance from player for monster spawns

# Special areas
SPECIAL_AREAS = {
    'treasure': 2,  # Treasure room with extra health
    'trap': 3,      # Trap room with more monsters
    'boss': 4,      # Boss room
    'exit': 5       # Level exit
}

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

# Special abilities
SPECIAL_ABILITIES = {
    'double_shot': False,  # Shoot two projectiles at once
    'health_regen': False,  # Regenerate health over time
    'slow_time': False,    # Slow down time temporarily
    'explosive_shot': False  # Shots explode on impact
}

# Ability cooldowns and timers
ABILITY_COOLDOWN = 30  # 30 seconds cooldown
SLOW_TIME_DURATION = 5  # 5 seconds duration
HEALTH_REGEN_RATE = 0.1  # Health per second

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

# Door texture
DOOR_TEXTURE = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

# Monster settings
MONSTER_HEALTH = {
    'normal': 50,
    'elite': 100,
    'boss': 200
}

MONSTER_SPEED = {
    'normal': 2.0,
    'elite': 2.5,
    'boss': 1.8
}

MONSTER_DAMAGE = {
    'normal': 10,
    'elite': 20,
    'boss': 30
}

MONSTER_EXP = {
    'normal': 10,
    'elite': 25,
    'boss': 50
}

MONSTER_ATTACK_RANGE = {
    'normal': 1.5,
    'elite': 2.0,
    'boss': 2.5
}

MONSTER_DETECTION_RANGE = {
    'normal': 10.0,
    'elite': 12.0,
    'boss': 15.0
}

MONSTER_COLORS = {
    'normal': (255, 0, 0),    # Red
    'elite': (255, 165, 0),   # Orange
    'boss': (128, 0, 128)     # Purple
}

MONSTER_SIZE = {
    'normal': 20,
    'elite': 30,    # 1.5x normal size
    'boss': 45      # 2.25x normal size
}

MONSTER_SIZE_SCALE = {
    'normal': 1.0,
    'elite': 1.5,
    'boss': 2.25
}

MONSTER_ATTACK_COOLDOWN = 1.0  # Seconds between attacks
BOSS_SPECIAL_ABILITY_DURATION = 5.0  # Seconds
BOSS_SPECIAL_ABILITY_COOLDOWN = 30.0  # Seconds

# UI Settings
UI_PADDING = 20
UI_FONT_SIZE = 24
UI_FONT_COLOR = (255, 255, 255)
UI_BACKGROUND_COLOR = (0, 0, 0, 128)  # Semi-transparent black

# Status Display
STATUS_WIDTH = 250
STATUS_HEIGHT = 250  # Increased for additional info
STATUS_POSITION = (WIDTH - STATUS_WIDTH - UI_PADDING, UI_PADDING)

# Ability Display
ABILITY_ICON_SIZE = 32
ABILITY_COOLDOWN_COLOR = (255, 0, 0, 128)  # Semi-transparent red
ABILITY_READY_COLOR = (0, 255, 0, 128)      # Semi-transparent green
ABILITY_POSITION = (WIDTH - STATUS_WIDTH - UI_PADDING, STATUS_HEIGHT + UI_PADDING * 2)

# Compass Settings
COMPASS_SIZE = 100
COMPASS_POSITION = (WIDTH - COMPASS_SIZE - UI_PADDING, HEIGHT - COMPASS_SIZE - UI_PADDING)
COMPASS_COLORS = {
    'N': (255, 0, 0),    # Red for North
    'E': (0, 255, 0),    # Green for East
    'S': (0, 0, 255),    # Blue for South
    'W': (255, 255, 0)   # Yellow for West
}

# Quest Display
QUEST_WIDTH = 300
QUEST_HEIGHT = 100
QUEST_POSITION = (UI_PADDING, UI_PADDING)
QUEST_COLORS = {
    'active': (255, 255, 0),    # Yellow for active quests
    'completed': (0, 255, 0),   # Green for completed quests
    'failed': (255, 0, 0)       # Red for failed quests
}

# Boss Warning
BOSS_WARNING_DURATION = 3.0  # Seconds
BOSS_WARNING_COLOR = (255, 0, 0, 200)  # Semi-transparent red
BOSS_WARNING_SIZE = 48

# Minimap Settings
MINIMAP_CELL_SIZE = 8  # Size of each cell in the minimap
MINIMAP_SIZE = 200  # Size of the minimap in pixels
MINIMAP_PADDING = 20  # Padding around the minimap
MINIMAP_POSITION = (MINIMAP_PADDING, HEIGHT - MINIMAP_SIZE - MINIMAP_PADDING)

# Minimap colors
MINIMAP_VISITED_COLOR = (100, 100, 100)  # Gray for visited cells
MINIMAP_UNVISITED_COLOR = (50, 50, 50)   # Dark gray for unvisited cells
MINIMAP_WALL_COLOR = (0, 0, 0)           # Black for walls
MINIMAP_PLAYER_COLOR = (0, 255, 0)       # Green for player
MINIMAP_MONSTER_COLORS = {
    'normal': (255, 0, 0),    # Red for normal monsters
    'boss': (255, 165, 0)     # Orange for boss monsters
}

# Map dimensions
MAP_WIDTH = 16  # Number of cells wide
MAP_HEIGHT = 16  # Number of cells tall

# Monster spawning settings
MAX_MONSTERS_PER_LEVEL = {
    1: 15,  # Level 1: 15 monsters total
    2: 20,  # Level 2: 20 monsters total
    3: 25,  # Level 3: 25 monsters total
    4: 30,  # Level 4: 30 monsters total
    5: 40   # Level 5: 40 monsters total (including boss)
}

SPAWN_INTERVAL = 5.0  # Time between regular monster spawns
WAVE_INTERVAL = 30.0  # Time between monster waves
WAVE_SIZE = 3  # Number of monsters per wave
MAX_SPAWN_ATTEMPTS = 50  # Maximum attempts to find valid spawn position

# Monster attributes
MONSTER_SPEED = {
    'normal': 3.0,
    'elite': 4.0,
    'boss': 2.5
}

MONSTER_DAMAGE = {
    'normal': 10,
    'elite': 15,
    'boss': 25
}

MONSTER_ATTACK_RANGE = {
    'normal': 40,
    'elite': 50,
    'boss': 60
}

MONSTER_DETECTION_RANGE = {
    'normal': 200,
    'elite': 250,
    'boss': 300
}

MONSTER_SIZE = {
    'normal': 15,
    'elite': 20,
    'boss': 30
}

MONSTER_COLORS = {
    'normal': (255, 0, 0),
    'elite': (255, 128, 0),
    'boss': (255, 0, 128)
}

MONSTER_ATTACK_COOLDOWN = 1.0  # Time between monster attacks
BOSS_SPECIAL_ABILITY_DURATION = 5.0  # Duration of boss special ability
BOSS_SPECIAL_ABILITY_COOLDOWN = 15.0  # Time between boss special abilities

# Heart settings
HEART_SIZE = 32  # Size of heart image in pixels
MAX_HEARTS = 5  # Maximum number of hearts in the level
MIN_HEART_DISTANCE = 100  # Minimum distance between hearts
MAX_HEART_SPAWN_ATTEMPTS = 50  # Maximum attempts to find valid heart positions
HEART_COLLISION_DISTANCE = 20  # Distance for heart collection
HEART_HEAL_AMOUNT = 20  # Amount of health restored by collecting a heart

# ... existing code ... 
# Doom-Style Game

A Python-based first-person shooter game inspired by the classic Doom series, featuring raycasting for 3D rendering and a maze-based level design.

## Implemented Features

### Core Game Engine
- Raycasting-based 3D rendering system
- Player movement and rotation mechanics
- Collision detection with walls
- Maze generation and navigation

### Player System
- Health and experience management
- Level progression system
- Special abilities with cooldowns
- Movement and rotation controls
- Damage and healing mechanics

### Monster System
- Monster spawning and management
- Different monster types (normal and boss)
- Monster movement and pathfinding
- Collision avoidance between monsters
- Distance-based spawning rules

### UI System
- Minimap with player and monster tracking
- Health and experience bars
- Level display
- Ability cooldown indicators
- Compass for navigation
- Boss warning system

## Key Components

### Player Class (`src/entities/player.py`)
- `__init__`: Initializes player attributes (health, experience, abilities)
- `move`: Handles player movement with wall collision detection
- `rotate`: Manages player rotation
- `take_damage`: Processes damage taken with invulnerability periods
- `heal`: Restores player health
- `gain_experience`: Handles experience gain and leveling up
- `update`: Manages timers and state updates
- `activate_ability`: Handles special ability activation
- `draw`: Renders player-related UI elements

### Monster Manager (`src/entities/monster_manager.py`)
- `__init__`: Initializes monster management system
- `_spawn_monster`: Handles monster spawning with type selection
- `_find_valid_spawn_position`: Finds suitable spawn locations
- `_is_too_close_to_other_monsters`: Prevents monster overlap
- `_get_distance_to_player`: Calculates distance to player
- `update`: Manages monster updates and collisions

### UI Manager (`src/ui/ui_manager.py`)
- `__init__`: Sets up UI elements and surfaces
- `update`: Updates all UI components
- `_update_status`: Updates player status display
- `_update_minimap`: Renders the minimap with player and monster positions
- `_update_compass`: Updates the compass display
- `show_boss_warning`: Displays boss encounter warnings
- `draw`: Renders all UI elements to the screen

## How It Works

The game uses a raycasting technique to create a 3D environment from a 2D maze. The player navigates through the maze, encountering monsters and collecting experience. The UI provides essential information about the player's status and surroundings.

### Rendering System
- Uses raycasting to create a pseudo-3D environment
- Calculates wall distances and heights
- Applies shading and textures for depth perception

### Gameplay Mechanics
- Player moves through the maze using WASD keys
- Mouse controls player rotation and aiming
- Monsters spawn at appropriate distances from the player
- Experience is gained by defeating monsters
- Special abilities can be activated with cooldown periods

### UI Features
- Minimap shows visited areas and nearby monsters
- Health and experience bars track player progress
- Compass helps with navigation
- Boss warnings alert the player to dangerous encounters

## Development Status
- Core game engine implemented
- Player system complete
- Monster system functional
- UI system operational
- Basic gameplay mechanics working

## Next Steps
- Implement weapon system
- Add sound effects
- Create more monster types
- Design additional levels
- Add power-ups and collectibles



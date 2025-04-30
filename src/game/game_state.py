from enum import Enum

class GameState(Enum):
    RUNNING = 0
    PAUSED = 1
    GAME_OVER = 2
    TITLE = 3
    UPGRADE = 4

class GameStateManager:
    def __init__(self):
        self.current_state = GameState.TITLE
        self.previous_state = None
        self.state_changed = False

    def change_state(self, new_state):
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            self.state_changed = True

    def is_state(self, state):
        return self.current_state == state

    def was_state(self, state):
        return self.previous_state == state

    def get_state(self):
        return self.current_state

    def get_previous_state(self):
        return self.previous_state

    def has_state_changed(self):
        return self.state_changed

    def reset_state_changed(self):
        self.state_changed = False 
from enum import Enum

class GameState(Enum):
    START_SCREEN = 0
    SETTINGS = 1
    CREDITS = 2
    GAME = 3
    PAUSE_MENU = 4
    QUIT = 5
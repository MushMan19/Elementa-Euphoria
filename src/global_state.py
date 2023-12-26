import pygame
from src.components.game_state import GameState
from src.constants import Constants

class GlobalState:
    GameStatus = GameState.START_SCREEN
    SCREEN = None
    
    @staticmethod
    def load_main_screen():
        screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        screen.fill(Constants.PRIMARY)
        GlobalState.SCREEN = screen
        
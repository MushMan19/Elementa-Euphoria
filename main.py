import pygame
from src.components.game_state import GameState
from src.game_phases import *
from src.constants import Constants
from src.global_state import GlobalState
from src.services.database import create_database

class Main:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.phases = {
            GameState.START_SCREEN: None,
            GameState.GAME: None,
            GameState.SETTINGS: None,
            GameState.CREDITS: None,
            GameState.PAUSE_MENU: None,
            GameState.QUIT: None
        }
        create_database()
        
        
    def run(self): 
        while True:
            Visuals.draw_game_background(GlobalState.SCREEN)
            current_state = GlobalState.GameStatus
            if current_state in self.phases:
                current_phase = self.phases[current_state]
                if current_phase is None:
                    self.reset_other_phases()
                    self.phases[current_state] = self.create_phase(current_state)
                self.phases[current_state].run()
            self.update()


    def create_phase(self, state):
        match state:
            case GameState.START_SCREEN:
                return StartScreen()
            case GameState.GAME:
                return GamePhase()
            case GameState.SETTINGS:
                return SettingsMenu()  
            case GameState.CREDITS:
                return CreditsMenu()
            case GameState.PAUSE_MENU:
                return pause_menu()
            case GameState.QUIT:
                exit_game()

    def update(self):
        pygame.display.update()
        self.clock.tick(Constants.FPS)
        
    def reset_other_phases(self):
        for state, phase in self.phases.items():
            if phase is not None:
                del phase
                self.phases[state] = None
            
if __name__ == "__main__":
    main = Main()
    main.run()

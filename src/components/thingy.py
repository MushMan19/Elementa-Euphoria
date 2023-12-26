import pygame
from src.constants import Constants
from src.services.sound import Sounds
from src.services.settings import Settings

class Slider:
    def __init__(self, pos:tuple, size, initial_value, increments, min, max) -> None:
        self.pos = pos
        self.size = size
        self.increment = increments
        self.min = min
        self.max = max
        self.current = initial_value
        self.value = Settings.get_volume()
        self.slider_rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.button_rect = pygame.rect.Rect((self.pos[0] + (self.current*(self.size[0]-self.size[1])/100)), self.pos[1], self.size[1], self.size[1])
        
    def handle_events(self, event_key):
        if (event_key == pygame.K_RIGHT or event_key == pygame.K_d) and self.current < 100:
            Sounds.play_change_sound()
            self.current += self.increment
        
        elif (event_key == pygame.K_LEFT or event_key == pygame.K_a) and self.current > 0:
            Sounds.play_change_sound()
            self.current -= self.increment
            
    def render(self, screen, selected):
        pygame.draw.rect(screen, Constants.RED, self.slider_rect, self.size[1])
        if selected:
            pygame.draw.rect(screen, Constants.BLUE, self.button_rect, self.size[1])
        else:
            pygame.draw.rect(screen, Constants.BLACK, self.button_rect, self.size[1])
            
    def update(self):
        self.value = Settings.update_volume(self.current)
        self.button_rect.x = self.pos[0] + self.current*(self.size[0]-self.size[1])/100
        
    def get_current_value(self):
        return self.current
    


import pygame
from src.constants import Constants
from src.services.visuals import Visuals
from src.services.sound import Sounds
from src.services.settings import Settings

class GuessTimer:
    def __init__(self):
        self.clock_image = Visuals.get_clock_image()
        self.guess_time = Settings.get_guess_time()
        self.guess_timer_start = None
        self.start_time = pygame.time.get_ticks()
        self.remaining_time = Settings.get_guess_time()
        self.timer_over = False
        self.e_2 = self.remaining_time
        
    def timer(self):
        if self.guess_timer_start == None:
            self.guess_timer_start = pygame.time.get_ticks()
            
        if self.e_2 != self.remaining_time:
            Sounds.play_clock_sound()
            self.e_2 = self.remaining_time
            
        elapsed_time = (pygame.time.get_ticks() - self.guess_timer_start) // 1000
        self.remaining_time = self.guess_time - elapsed_time
        if self.remaining_time <= 0:
            self.timer_over = True
    
    def display(self, screen):
        screen.blit(self.clock_image, (Constants.T_PAD_X, Constants.T_PAD_Y))
        # minutes, seconds = divmod(self.remaining_time, 60)
        # time_str = f"{int(minutes):01}:{int(seconds):02}"
        Visuals.draw_text(screen, Visuals.load_font(30), f'{self.remaining_time}', None, Constants.BLACK, (self.clock_image.get_width() // 2 + Constants.T_PAD_X, self.clock_image.get_height() // 2 + Constants.T_PAD_Y), rect_pos='center')
    
    def restart_timer(self):
        self.timer_over = False
        self.remaining_time = Settings.get_guess_time()
        self.guess_timer_start = pygame.time.get_ticks()
    
    def update(self):
        self.timer()
    
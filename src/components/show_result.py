import pygame
from src.services.visuals import Visuals
from src.constants import Constants
from src.tools.tools import sine

class ShowResult:
    def __init__(self, state) -> None:
        self.state = state
        self.font_size = 35
    
    def display_win_text(self, screen):
        res_text_font = Visuals.load_font_bold(self.font_size)
        if self.state != -1:
            Visuals.draw_text(screen, res_text_font, Constants.RES_TEXT[self.state], None,Constants.BLACK, (Constants.T_PAD_X + Visuals.get_textbox_image().get_width()/2, Constants.SCREEN_HEIGHT/2))
        else:
            Visuals.draw_text(screen, res_text_font, Constants.RES_TEXT[-2], None, Constants.BLACK, (Constants.T_PAD_X + Visuals.get_textbox_image().get_width()/2, Constants.SCREEN_HEIGHT/2 - 10), 'midbottom')
            Visuals.draw_text(screen, Visuals.load_font_bold(self.font_size-18), Constants.RES_TEXT[-1], None, Constants.BLACK, (Constants.T_PAD_X + Visuals.get_textbox_image().get_width()/2, Constants.SCREEN_HEIGHT/2 + 10), 'midtop')
        pygame.display.flip()
    
    def bloom(self):
        if sine(200, 550, 6, 35) % 5 == 0:
            self.font_size = sine(200, 550, 6, 35)
    
    def display(self, screen):
        self.display_win_text(screen)
        
        
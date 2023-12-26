import pygame
from src.constants import Constants
from src.services.visuals import Visuals
from src.services.sound import Sounds
from src.constants import Constants

class Textbox():
    def __init__(self):
        self.textbox = Visuals.get_textbox_image()
        self.text_color = Constants.BLACK
        self.input_text = ""
        self.entered_text = ""
        self.cursor_visible = True
        self.font = Visuals.load_font(Constants.TEXTBOX_FONT_SIZE)
        pygame.time.set_timer(pygame.USEREVENT + 1, Constants.CURSOR_BLINK_TIME)
    
    def display(self,screen):
        screen.blit(self.textbox, (Constants.T_PAD_X, (Constants.SCREEN_HEIGHT - self.textbox.get_height() - Constants.T_PAD_Y)))    
        
        text_surface = self.font.render(self.input_text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.midleft = ((Constants.T_PAD_X + Constants.TEXT_PAD_X), (Constants.SCREEN_HEIGHT - (self.textbox.get_height()/2) - Constants.T_PAD_Y))
        screen.blit(text_surface, text_rect)

        if self.cursor_visible:
            cursor_rect = pygame.Rect(text_rect.right + 2, text_rect.y-1, 2, text_rect.height + 2)
            pygame.draw.rect(screen, self.text_color, cursor_rect)

    def handle_input(self, text):
        match text:
            case pygame.K_RETURN:
                self.entered_text = self.input_text
                self.reset_text_input()
                
            case pygame.K_BACKSPACE:
                Sounds.play_type_sound()
                self.input_text = self.input_text[:-1]
            
            case _:
                Sounds.play_type_sound()
                if Visuals.get_text_width(self.input_text, self.font, Constants.TEXTBOX_FONT_SIZE) < (self.textbox.get_width() - Constants.T_PAD_X - 2*Constants.TEXT_PAD_X):
                    self.input_text += text
        
    def reset_text_input(self):
        self.input_text = ""

        
        
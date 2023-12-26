import pygame
from src.constants import Constants
from src.tools.tools import sine
from paths import IMAGE_DIR, FONT_DIR

class Visuals:
    @staticmethod
    def load_font_bold(size):
        return pygame.font.Font(FONT_DIR/ "dogica/dogicapixelbold.ttf", size)
    
    @staticmethod
    def load_font(size):
        return pygame.font.Font(FONT_DIR/ "dogica/dogicapixel.ttf", size)

    @staticmethod
    def load_countdown_font(size):
        return pygame.font.Font(FONT_DIR/ "04b_30/04B_30__.TTF", size)
    
    @staticmethod
    def load_display_settings():
        pygame.display.set_caption(Constants.GAME_TITLE)
        pygame.display.set_icon(Visuals.get_game_icon_image())
        
    @staticmethod
    def get_flashcard_image():
        return pygame.image.load(IMAGE_DIR/"flashcard.png").convert_alpha()

    @staticmethod
    def get_textbox_image():
        return pygame.image.load(IMAGE_DIR/"text_box.png").convert_alpha()

    @staticmethod
    def get_question_mark_image():
        return pygame.image.load(IMAGE_DIR/"question_mark.png").convert_alpha()

    @staticmethod
    def get_game_background_image():
        return pygame.image.load(IMAGE_DIR/"game_background.png").convert_alpha()
    
    @staticmethod
    def get_game_icon_image():
        return pygame.image.load(IMAGE_DIR/"icon.png").convert_alpha()

    @staticmethod
    def get_clock_image():
        clock = pygame.image.load(IMAGE_DIR/"clock2.png").convert_alpha()
        clock = pygame.transform.smoothscale_by(clock, Constants.CLOCK_SCALE_FACTOR)
        return clock
    
    @staticmethod
    def get_scoreboard_image():
        scoreboard = pygame.image.load(IMAGE_DIR/"scoreboard.png").convert_alpha()
        scoreboard = pygame.transform.smoothscale_by(scoreboard, 0.6)
        return scoreboard
    
    @staticmethod
    def load_and_scale_image(image_path, scale_factor):
        og = pygame.image.load(IMAGE_DIR/ image_path).convert_alpha()
        rescaled = pygame.transform.smoothscale_by(og, scale_factor)
        return rescaled

    @staticmethod
    def get_game_title_image():
        return pygame.image.load(IMAGE_DIR/"title.png").convert_alpha()

    @staticmethod
    def get_start_button_image():
        return Visuals.load_and_scale_image("start_button.png", Constants.BUTTON_SCALE_FACTOR)

    @staticmethod
    def get_start_selected_button_image():
        return Visuals.load_and_scale_image("start_button_selected.png", Constants.BUTTON_SCALE_FACTOR)

    @staticmethod
    def get_settings_button_image():
        return Visuals.load_and_scale_image("settings_button.png", Constants.BUTTON_SCALE_FACTOR)

    @staticmethod
    def get_settings_selected_button_image():
        return Visuals.load_and_scale_image("settings_button_selected.png", Constants.BUTTON_SCALE_FACTOR)

    @staticmethod
    def get_credits_button_image():
        return Visuals.load_and_scale_image("credits_button.png", Constants.BUTTON_SCALE_FACTOR)

    @staticmethod
    def get_credits_selected_button_image():
        return Visuals.load_and_scale_image("credits_button_selected.png", Constants.BUTTON_SCALE_FACTOR)
       
    @staticmethod
    def draw_text(screen, font, text, size, color, pos, rect_pos=None):
        if font == None:
            font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if rect_pos is not None:
            setattr(text_rect, rect_pos, (pos[0], pos[1]))
        else:
            text_rect.center = (pos[0], pos[1])
        screen.blit(text_surface,text_rect)
      
    @staticmethod  
    def get_text_width(text, font, size):
        if font == None:
            font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        return text_rect.width
        
    @staticmethod
    def draw_game_background(screen):
        background = Visuals.get_game_background_image()
        screen.blit(background, (0, 0))
     
    @staticmethod
    def draw_game_title(screen):
        y = sine(200.0, 1280, 5.0, 15)
        title = Visuals.get_game_title_image()
        title = pygame.transform.smoothscale_by(title, 1.3)
        screen.blit(title, ((Constants.SCREEN_WIDTH - title.get_width()) // 2, y))
      
    @staticmethod 
    def draw_game_buttons(screen, selected_button):
        buttons = {
            "game": {
                "selected": Visuals.get_start_selected_button_image(),
                "not_selected": Visuals.get_start_button_image(),
                'y_pos': 320
            },
            "settings": {
                "selected": Visuals.get_settings_selected_button_image(),
                "not_selected": Visuals.get_settings_button_image(),
                "y_pos": 390
            },
            "credits": {
                "selected": Visuals.get_credits_selected_button_image(),
                "not_selected": Visuals.get_credits_button_image(),
                "y_pos": 460
            }
        }

        for button_name, button_info in buttons.items():
            selected_image = button_info["selected"]
            not_selected_image = button_info["not_selected"]
            x_pos = (Constants.SCREEN_WIDTH - selected_image.get_width())//2
            y_pos = button_info["y_pos"]

            if selected_button == button_name:
                screen.blit(selected_image, (x_pos, y_pos))
            else:
                screen.blit(not_selected_image, (x_pos, y_pos))
        
    @staticmethod
    def draw_best_score(screen, max_score):
        score_font = Visuals.load_font_bold(Constants.SCORE_FONT_SIZE_MENU)
        best_score = score_font.render(f"Best: {max_score}", True, (0, 0, 0))
        best_score_rect = best_score.get_rect(center=(Constants.SCREEN_WIDTH/ 2, 200))
        screen.blit(best_score, best_score_rect)
        
    @staticmethod
    def draw_main_menu(screen, selected_button, max_score):
        Visuals.draw_best_score(screen, max_score)
        Visuals.draw_game_title(screen)
        Visuals.draw_game_buttons(screen, selected_button)
        
    @staticmethod
    def draw_credits_menu(screen):
        name_font = Visuals.load_font(30)
        title_font = Visuals.load_font_bold(25)
        pad = 340
        pad_y = 20
        Visuals.draw_text(screen, Visuals.load_font_bold(45), 'Developer', None, Constants.BLACK, (Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT/2 + 80 +pad_y))
        # Visuals.draw_text(screen, title_font, 'Programer', None, Constants.BLACK, (Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT - 175.5 + pad_y), 'midbottom')
        Visuals.draw_text(screen, name_font, 'Shubhanyu Jain', None, Constants.BLACK, (Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT - 163 + pad_y), 'midtop')
       
        Visuals.draw_text(screen, title_font, 'Class XI', None, Constants.BLACK, (Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT - 40), 'midbottom')
        
        Visuals.draw_game_title(screen)
        text_y = 210
        game_description = (
            "Embark on an exciting journey of chemical discovery! Guess the",
            "element based on the given properties within a limited time.",
            "Test your knowledge of the periodic table and take part in this",
            "race against time to identify all the elements and become the", 
            "ultimate chemist? PLAY NOW!"
        )

        description_font = Visuals.load_font(15)
        for line in game_description:
            Visuals.draw_text(screen, description_font, line, None, Constants.BLACK, (Constants.SCREEN_WIDTH // 2, text_y))
            text_y += 30

    
    @staticmethod
    def draw_countdown(screen, count):
        Visuals.draw_game_background(screen)
        Visuals.draw_text(screen, Visuals.load_font_bold(Constants.COUNTDOWN_TIMER_FONT_SIZE), count, None, Constants.BLACK, (Constants.SCREEN_WIDTH/2, Constants.SCREEN_HEIGHT/2))
        pygame.display.flip()
        
    @staticmethod
    def draw_settings_menu(screen, vol_y_pos):
        Visuals.draw_text(screen, Visuals.load_font_bold(Constants.SETTINGS_TEXT_FONT_SIZE), 'SETTINGS', None, Constants.BLACK, (Constants.SCREEN_WIDTH/2, Constants.SETTINGS_PAD_Y), 'midtop')
        font = Visuals.load_font(Constants.SETTINGS_FONT_SIZE)
        Visuals.draw_text(screen, font, 'Volume', None, Constants.BLACK, (Constants.SETTINGS_PAD_X, vol_y_pos), 'topleft')

        Visuals.draw_text(screen, font, 'Guess Timer Duration', None, Constants.BLACK, (Constants.SETTINGS_PAD_X, vol_y_pos + Constants.SETTINGS_INTERSPACE_PAD_Y), 'topleft')
        screen.blit(Visuals.get_scoreboard_image(), (Constants.SETTINGS_PAD_X + Visuals.get_text_width('Guess Timer Duration', font, None) + Constants.SETTINGS_INTERSPACE_PAD_X, vol_y_pos + Constants.SETTINGS_INTERSPACE_PAD_Y + Constants.SETTINGS_FONT_SIZE/2 - Visuals.get_scoreboard_image().get_height()/2 + 4))
        
        Visuals.draw_text(screen, font, 'Guesses', None, Constants.BLACK, (Constants.SETTINGS_PAD_X, vol_y_pos + 2*Constants.SETTINGS_INTERSPACE_PAD_Y), 'topleft')
        screen.blit(Visuals.get_scoreboard_image(), (Constants.SETTINGS_PAD_X + Visuals.get_text_width('Guesses', font, None) + Constants.SETTINGS_INTERSPACE_PAD_X, vol_y_pos + 2*Constants.SETTINGS_INTERSPACE_PAD_Y + Constants.SETTINGS_FONT_SIZE/2 - Visuals.get_scoreboard_image().get_height()/2 + 4))

        Visuals.draw_text(screen, font, 'Difficulty', None, Constants.BLACK, (Constants.SETTINGS_PAD_X, vol_y_pos + 3*Constants.SETTINGS_INTERSPACE_PAD_Y), 'topleft')
        screen.blit(Visuals.get_scoreboard_image(), (Constants.SETTINGS_PAD_X + Visuals.get_text_width('Difficulty', font, None) + Constants.SETTINGS_INTERSPACE_PAD_X, vol_y_pos + 3*Constants.SETTINGS_INTERSPACE_PAD_Y + Constants.SETTINGS_FONT_SIZE/2 - Visuals.get_scoreboard_image().get_height()/2 + 4))
        

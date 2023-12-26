import sys
import pygame
import random
from src.global_state import GlobalState
from src.constants import Constants
from src.components.game_state import GameState
from src.components.flashcard import Flashcard
from src.components.textbox import Textbox
from src.components.show_result import ShowResult
from src.components.guess_timer import GuessTimer
from src.components.scoreboard import Scoreboard
from src.components.thingy import Slider
from src.services.database import *
from src.services.visuals import Visuals
from src.services.sound import Sounds
from src.services.settings import Settings
from src.services.result_timer import wait_for_time, create_threading_event, end_threads
from src.tools.tools import *

GlobalState.load_main_screen()
Visuals.load_display_settings()
score = Scoreboard()
volume = 100

class StartScreen:
    current_menu = 'game'
    def __init__(self):
        self.buttons = {'game': 0, 'settings': 1, 'credits': 2}
        score.reset_current_score()
        Sounds.start_background_music()
        
    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if is_close_app_event(event):
                GlobalState.GameStatus = GameState.QUIT
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    StartScreen.current_menu = self.get_next_button()
                    Sounds.play_button_sound()
                elif event.key == pygame.K_UP:
                    StartScreen.current_menu = self.get_previous_button()
                    Sounds.play_button_sound()
                    
                elif event.key == pygame.K_RETURN:
                    selected_button_menu = getattr(GameState, StartScreen.current_menu.upper())
                    GlobalState.GameStatus = selected_button_menu
                    if StartScreen.current_menu != 'game':
                        Sounds.play_button_enter_sound()
                    else:
                        pygame.mixer.music.stop()
                        Sounds.play_coutdown_sound()
            
    def run(self):
        self.handle_events()
        self.render(GlobalState.SCREEN, StartScreen.current_menu, score.get_max_score())
        
    def render(self, screen, selected_button, max_score):
        Visuals.draw_main_menu(screen, selected_button, max_score)
    
    def get_next_button(self):
        current_index = self.buttons[StartScreen.current_menu]
        next_index = (current_index + 1) % len(self.buttons)
        return list(self.buttons.keys())[next_index]

    def get_previous_button(self):
        current_index = self.buttons[StartScreen.current_menu]
        previous_index = (current_index - 1) % len(self.buttons)
        return list(self.buttons.keys())[previous_index]       
        
            
class GamePhase:
    def __init__(self):
        self.textbox = Textbox()
        self.guess_timer = GuessTimer()
        self.guesses = Settings.get_guesses()
        self.difficulty = Settings.get_difficulty()
        self.countdown_timer = 3
        self.threads = []
        self.recently_generated_elements = []
        self.create_new_flashcard()
        
        self.flag1 = create_threading_event()
        self.flag2 = create_threading_event()
        self.reset_called = False
        self.state = None


    def create_new_flashcard(self):
        while True:
            if self.difficulty == 1:
                random_num = random.randint(0, 56)
            elif self.difficulty == 2:
                random_num = random.randint(0, 71)
            elif self.difficulty == 3:
                random_num = random.randint(0, get_database_size())

            if random_num not in self.recently_generated_elements:
                break

        self.recently_generated_elements.append(random_num)

        if len(self.recently_generated_elements) > 5:
            self.recently_generated_elements.pop(0)

        self.element_data = retrieve_data(row=random_num)
        self.flashcard = Flashcard(
            self.element_data[1], str(self.element_data[0]),
            self.element_data[2], str(self.element_data[3])[:4],
            self.element_data[4], self.element_data[5],
            self.element_data[6], self.element_data[7]
        )
        
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if is_close_app_event(event):
                end_threads(self.threads)
                GlobalState.GameStatus = GameState.QUIT
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.state == None:
                    self.textbox.handle_input(pygame.K_RETURN)
                    self._check_answer()
                elif event.key == pygame.K_BACKSPACE:
                    self.textbox.handle_input(pygame.K_BACKSPACE)
                elif event.key == pygame.K_ESCAPE:
                    GlobalState.GameStatus = GameState.START_SCREEN
                    Sounds.play_button_enter_sound()
                    end_threads(self.threads)
                elif event.unicode.isprintable():
                    self.textbox.handle_input(event.unicode)
            

            elif event.type == pygame.USEREVENT + 1:
                self.textbox.cursor_visible = not self.textbox.cursor_visible

    def update(self):
        global s
        self.flashcard.update()
        if self.guess_timer.timer_over and not self.reset_called:
            self._check_answer()
        if self.state == None:
            # print(f'reset called: {self.reset_called}, guess timer over: {self.guess_timer.timer_over}, game state: {self.state}')
            self.guess_timer.update()
        elif self.state != None:
            try:
                s.bloom()
            except: pass
            
    def render(self, screen):
        screen.blit(Visuals.get_game_background_image(), (0,0))
        self.flashcard.display(screen)
        self.textbox.display(screen)
        self.guess_timer.display(screen)
        score.draw(screen)
        if self.state != None:
            s.display(screen)
    
    def run(self):
        start_time = pygame.time.get_ticks()
        while self.countdown_timer >= 0:
            time = pygame.time.get_ticks()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    GlobalState.GameStatus = GameState.QUIT
                    return
            if self.countdown_timer > 0:
                Visuals.draw_countdown(GlobalState.SCREEN, str(self.countdown_timer))
            
            elif self.countdown_timer == 0:
                Visuals.draw_countdown(GlobalState.SCREEN, 'Go!')
            
            else:
                pygame.event.clear()
                break
            
            if time - start_time > 1000:
                self.countdown_timer -= 1
                start_time = pygame.time.get_ticks()
        
        self._run_game()
    
    def reset_round_phase(self, state):
        self.reset_called = True
        if state == 1:
            score.increase_current_score()
            score.update_max_score()
        self.threads.append(wait_for_time(self._reset_round_func, self.flag1, state))
        self.threads.append(wait_for_time(self._reveal_properties_func, self.flag2))
        
    def _reset_round_func(self, state):
        global s
        # pygame.time.wait(int(0.5*1000))
        self.state = state
        self.guesses = Settings.get_guesses()
        s = ShowResult(self.state)
        self.textbox.reset_text_input()
        pygame.time.wait(int(Constants.NEW_ROUND_WAIT_TIME*1000))
        self.guess_timer.restart_timer()
        self.create_new_flashcard()
        self.flashcard.showing_answer = False
        self.flag1['stop_flag'].clear()
        self.threads.pop()
        self.reset_called = False  
        self.state = None
        del s
    
    
    def _reveal_properties_func(self):
        pygame.time.wait(int(0.5*1000))
        score.cheer()
        self.flashcard.showing_answer = True
        self.flag2['stop_flag'].clear()
        self.threads.pop()
        
    def _check_answer(self):
        if self.guess_timer.timer_over:
            Sounds.play_timer_over_sound()
            self.reset_round_phase(-1)
        
        elif is_correct_guess(self.textbox.entered_text, self.flashcard.element_name)  and self.guesses >= 0:
            # print('yes')
            Sounds.play_correct_sound()
            self.reset_round_phase(1)
        
        else:
            if self.guesses > 1:
                # print('no f')
                Sounds.play_wrong_sound()
                self.guesses -= 1
            
            else:
                # print('no')
                Sounds.play_cancel_sound()
                self.reset_round_phase(0)
   
    def _run_game(self):
        self.handle_events()
        self.update()
        self.render(GlobalState.SCREEN)


class SettingsMenu:
    def __init__(self):
        self.vol_y_pos = Constants.SETTINGS_PAD_Y + Constants.SETTINGS_INTERSPACE_PAD_Y + 20
        self.vol_x_pos = Constants.SETTINGS_PAD_X + Visuals.get_text_width('Volume', Visuals.load_font(Constants.SETTINGS_FONT_SIZE), None) + Constants.SETTINGS_INTERSPACE_PAD_X
        
        self.buttons = {'volume': 0, 'guess_timer': 1, 'max_guess': 2, 'difficulty': 3, 'reset':4}
        self.current_button = 'volume'
        self.volume_slider = Slider((self.vol_x_pos, self.vol_y_pos), (((Constants.SCREEN_WIDTH/2-(self.vol_x_pos))*2), Constants.SETTINGS_FONT_SIZE), Settings.get_volume(), 10, 10, 200)

        self._entered_times = 0

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                GlobalState.GameStatus = GameState.QUIT
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.current_button = self.get_next_button()
                    Sounds.play_button_sound()
                
                elif event.key == pygame.K_UP:
                    self.current_button = self.get_previous_button()
                    Sounds.play_button_sound()
                
                elif event.key == pygame.K_ESCAPE:
                    Sounds.play_button_enter_sound()
                    GlobalState.GameStatus = GameState.START_SCREEN
                
                match self.current_button:
                    case 'volume':
                        self.volume_slider.handle_events(event.key)
                        volume = self.volume_slider.get_current_value()
                        Sounds.set_volume(volume/100)

                    case 'guess_timer':
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            Sounds.play_change_sound()
                            Settings.update_guess_time((Settings.get_guess_time() % 999) + 1)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            Sounds.play_change_sound()
                            Settings.update_guess_time((Settings.get_guess_time() - 2) % 999 + 1)
                        try:
                            if self._entered_times == 0:
                                Settings.update_guess_time(int(event.unicode))
                            elif 1 <= self._entered_times < 3:
                                Settings.update_guess_time(int(Settings.get_guess_time())*10 + int(event.unicode))
                            else:
                                Settings.update_guess_time(int(event.unicode))
                                self._entered_times = 0
                    
                            if int(Settings.get_guess_time()) != 0:
                                self._entered_times += 1
                        except: pass
                    
                    case 'max_guess':
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            Sounds.play_change_sound()
                            Settings.update_guesses((Settings.get_guesses() % 9) + 1)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            Sounds.play_change_sound()
                            Settings.update_guesses((Settings.get_guesses() - 2) % 9 + 1)
                        try:
                            Settings.update_guesses(int(event.unicode) if int(event.unicode) != 0 else Settings.get_guesses())
                        except: pass
                        
                    case 'difficulty':
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            Sounds.play_change_sound()
                            Settings.update_difficulty((Settings.get_difficulty() % 3) + 1)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            Sounds.play_change_sound()
                            Settings.update_difficulty((Settings.get_difficulty() - 2) % 3 + 1)

                        try:
                            Settings.update_difficulty(int(event.unicode) if 0 < int(event.unicode) <= 3 else Settings.get_difficulty())
                        
                        except:pass
                        
                    case 'reset':
                        if event.key == pygame.K_RETURN:
                            Sounds.play_change_sound()
                            score.reset_max_score()

                # print(self.current_button)
    
    def render(self, screen):
        Visuals.draw_settings_menu(screen, self.vol_y_pos)
        self.volume_slider.render(screen, (self.current_button=='volume'))
        Visuals.draw_text(screen, Visuals.load_font(Constants.SCORE_FONT_SIZE_SETTINGS), str(Settings.get_guess_time()), None, (Constants.BLACK if self.current_button != 'guess_timer' else Constants.BLUE), (Constants.SETTINGS_PAD_X + Visuals.get_text_width('Guess Timer Duration', Visuals.load_font(Constants.SETTINGS_FONT_SIZE), None) + Constants.SETTINGS_INTERSPACE_PAD_X + Visuals.get_scoreboard_image().get_width()/2, self.vol_y_pos + Constants.SETTINGS_INTERSPACE_PAD_Y + Constants.SETTINGS_FONT_SIZE/2 + 4 - 1.5))
        Visuals.draw_text(screen, Visuals.load_font(Constants.SCORE_FONT_SIZE_SETTINGS), str(Settings.get_guesses()), None, (Constants.BLACK if self.current_button != 'max_guess' else Constants.BLUE), (Constants.SETTINGS_PAD_X + Visuals.get_text_width('Guesses', Visuals.load_font(Constants.SETTINGS_FONT_SIZE), None) + Constants.SETTINGS_INTERSPACE_PAD_X + Visuals.get_scoreboard_image().get_width()/2, self.vol_y_pos + 2*Constants.SETTINGS_INTERSPACE_PAD_Y + Constants.SETTINGS_FONT_SIZE/2 + 4 - 1.5))
        Visuals.draw_text(screen, Visuals.load_font(Constants.SCORE_FONT_SIZE_SETTINGS), str(Settings.get_difficulty()), None, (Constants.BLACK if self.current_button != 'difficulty' else Constants.BLUE), (Constants.SETTINGS_PAD_X + Visuals.get_text_width('Difficulty', Visuals.load_font(Constants.SETTINGS_FONT_SIZE), None) + Constants.SETTINGS_INTERSPACE_PAD_X + Visuals.get_scoreboard_image().get_width()/2, self.vol_y_pos + 3*Constants.SETTINGS_INTERSPACE_PAD_Y + Constants.SETTINGS_FONT_SIZE/2 + 4 - 1.5))
        Visuals.draw_text(screen, Visuals.load_font(Constants.SETTINGS_FONT_SIZE), 'Reset Best Score', None, (Constants.BLACK if self.current_button != 'reset' else Constants.BLUE), (Constants.SCREEN_WIDTH/2, self.vol_y_pos + 5*Constants.SETTINGS_INTERSPACE_PAD_Y), 'midtop')
        pygame.display.flip()

    def update(self):
        # print(self.volume_slider.get_current_value(), self.volume_slider.value)
        self.volume_slider.update()

    def run(self):
        self.handle_events()
        self.update()
        self.render(GlobalState.SCREEN)

    def get_next_button(self):
        current_index = self.buttons[self.current_button]
        next_index = (current_index + 1) % len(self.buttons)
        return list(self.buttons.keys())[next_index]

    def get_previous_button(self):
        current_index = self.buttons[self.current_button]
        previous_index = (current_index - 1) % len(self.buttons)
        return list(self.buttons.keys())[previous_index]   

def pause_menu():
    pass
    
class CreditsMenu:
    def __init__(self) -> None:
        # print('in_credits')
        pass
        
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                GlobalState.GameStatus = GameState.QUIT
                break
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                Sounds.play_button_enter_sound()
                GlobalState.GameStatus = GameState.START_SCREEN
    
    def run(self):
        self.handle_events()
        self.render(GlobalState.SCREEN)
    
    def render(self, screen):
        Visuals.draw_credits_menu(screen)
    
def exit_game():
    pygame.mixer.stop()
    pygame.quit()
    sys.exit()

from src.constants import Constants
from src.services.score import Score
from src.services.visuals import Visuals
from src.services.sound import Sounds

class Scoreboard:
    def __init__(self):
        self._current_score = 0
        self._max_score = Score.get_max_score()

    def reset_current_score(self):
        self._current_score = 0

    def reset_max_score(self):
        Score.update_max_score(0)
        self._max_score = Score.get_max_score()

    def increase_current_score(self):
        self._current_score += 1

    def get_max_score(self):
        return self._max_score

    def get_current_score(self):
        return self._current_score

    def update_max_score(self):
        if self._current_score > self._max_score:
            Score.update_max_score(self._current_score)
            self._max_score = self._current_score
            
    def draw(self, screen):
        scoreboard_image = Visuals.get_scoreboard_image()
        scoreboard_x = Constants.T_PAD_X + 200
        screen.blit(scoreboard_image, (scoreboard_x, Constants.T_PAD_Y))
        Visuals.draw_text(screen, Visuals.load_font(Constants.SCORE_FONT_SIZE_GAME), str(self._current_score), None, Constants.BLACK, (scoreboard_x + (scoreboard_image.get_width()/2) + 1, (Constants.T_PAD_Y + scoreboard_image.get_height()/2 -1)))
        
    def cheer(self):
        if self._current_score % 5 == 0 and self._current_score != 0:
            Sounds.play_cheer_sound()
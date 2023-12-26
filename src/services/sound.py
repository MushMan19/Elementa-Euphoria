import random
import pygame
from paths import SOUND_DIR
from src.services.settings import Settings


class Sounds:
    @staticmethod
    def set_volume(volume):
        pygame.mixer.music.set_volume(volume)
    
    @staticmethod
    def get_background_musics():
        return [
            SOUND_DIR / "background.ogg"
        ]

    @staticmethod
    def get_cheer_musics():
        return [
            SOUND_DIR / "cheer.wav",
            SOUND_DIR / "cheer_2.wav",
            SOUND_DIR / "cheer_3.wav",
            SOUND_DIR / "cheer_4.wav"
        ]

    @staticmethod
    def start_background_music():
        if pygame.mixer.music.get_busy():
            return

        musics = Sounds.get_background_musics()
        filename = random.choice(musics)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(Settings.get_volume()/100)
        pygame.mixer.music.play()
        

    @staticmethod
    def play_button_sound():
        button_sfx = pygame.mixer.Sound(SOUND_DIR / "button.wav")
        pygame.mixer.Sound.play(button_sfx)

    @staticmethod
    def play_button_enter_sound():
        enter_button_sfx = pygame.mixer.Sound(SOUND_DIR / "enter.wav")
        pygame.mixer.Sound.play(enter_button_sfx)

    @staticmethod
    def play_change_sound():
        change_sfx = pygame.mixer.Sound(SOUND_DIR / "change.wav")
        pygame.mixer.Sound.play(change_sfx)

    @staticmethod
    def play_coutdown_sound():
        countdown_sfx = pygame.mixer.Sound(SOUND_DIR / "countdown.wav")
        pygame.mixer.Sound.play(countdown_sfx)

    @staticmethod
    def play_clock_sound():
        clock_tick_sfx = pygame.mixer.Sound(SOUND_DIR / "tick.wav")
        clock_tick_sfx.set_volume(0.25)
        pygame.mixer.Sound.play(clock_tick_sfx)

    @staticmethod
    def play_timer_over_sound():
        time_over_sfx = pygame.mixer.Sound(SOUND_DIR / "time_over.wav")
        time_over_sfx.set_volume(0.25)
        pygame.mixer.Sound.play(time_over_sfx)

    @staticmethod
    def play_wrong_sound():
        wrong_sfx = pygame.mixer.Sound(SOUND_DIR / "wrong.wav")
        wrong_sfx.set_volume(0.2)
        pygame.mixer.Sound.play(wrong_sfx)

    @staticmethod
    def play_cancel_sound():
        cancel_sfx = pygame.mixer.Sound(SOUND_DIR / "cancel.wav")
        cancel_sfx.set_volume(0.2)
        pygame.mixer.Sound.play(cancel_sfx)

    @staticmethod
    def play_correct_sound():
        correct_sfx = pygame.mixer.Sound(SOUND_DIR / "correct.wav")
        correct_sfx.set_volume(0.3)
        pygame.mixer.Sound.play(correct_sfx)
    
    @staticmethod
    def play_type_sound():
        type_sfx = pygame.mixer.Sound(SOUND_DIR / "type.wav")
        type_sfx.set_volume(0.2)
        pygame.mixer.Sound.play(type_sfx)

    @staticmethod
    def play_cheer_sound():
        musics = Sounds.get_cheer_musics()
        filename = random.choice(musics)
        cheer = pygame.mixer.Sound(filename)
        pygame.mixer.Sound.play(cheer)

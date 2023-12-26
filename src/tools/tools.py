import pygame
import math
import random


def is_close_app_event(event):
    return (event.type == pygame.QUIT)

def is_correct_guess(guess:str, answer:str):
    return (guess.lower() == answer.lower())

def sine(speed: float, time: int, how_far: float, overall_y: int) -> int:
    t = pygame.time.get_ticks() / 2 % time
    y = math.sin(t / speed) * how_far + overall_y
    return int(y)

def generate_visible_colors():
    random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    complementary_color = (255 - random_color[0], 255 - random_color[1], 255 - random_color[2])
    return random_color, complementary_color
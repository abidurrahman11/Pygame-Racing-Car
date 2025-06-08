import pygame

# load car images for player and enemy's cars
def load_car_image(path):
    return pygame.image.load(path)

# load sound effects
def load_crash_sound(path):
    return pygame.mixer.Sound(path)

# load font
def load_font(path, size):
    return pygame.font.Font(path, size)

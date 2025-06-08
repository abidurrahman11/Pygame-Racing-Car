import pygame

# load car images for player and enemy's cars
def load_car_image(path, width, height):
    original = pygame.image.load(path)
    return pygame.transform.scale(
        original,
        (
            int(original.get_width() * (width / 800)),
            int(original.get_height() * (height / 600)),
        )
    )

# load sound effects
def load_crash_sound(path):
    return pygame.mixer.Sound(path)

# load font
def load_font(path, size):
    return pygame.font.Font(path, size)

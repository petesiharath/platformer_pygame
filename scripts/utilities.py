import pygame

BASE_IMAGE_PATH = "data/images/"

def load_image(path):

    image = pygame.image.load(BASE_IMAGE_PATH + path).convert()
    image.set_colorkey((0, 0, 0))

    return image
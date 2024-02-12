import pygame

BASE_IMAGE_PATH = "data/images/"

def load_image(path):
    
    image = pygame.load_image(BASE_IMAGE_PATH + path).convert()
    image.set_colorkey((0, 0, 0))

    return image
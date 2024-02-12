import pygame
import os

BASE_IMAGE_PATH = "data/images/"

def load_image(path):

    image = pygame.image.load(BASE_IMAGE_PATH + path).convert()
    image.set_colorkey((0, 0, 0))

    return image

def load_images(path):
    images = []
    for imageName in os.listdir(BASE_IMAGE_PATH + path):
        images.append(load_image(path + "/" + imageName))
    
    return images
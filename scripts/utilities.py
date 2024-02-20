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

class Animation:

    def __init__(self, images, image_duration=5, loop=True):

        self.images = images
        self.loop = loop
        self.image_duration = image_duration
        self.done = False
        self.frame = 0
        

    def copy(self):

        return Animation(self.images, self.image_duration, self.loop)
    

    def update(self):

        if self.loop:
            self.frame = (self.frame + 1) % (self.image_duration * len(self.images))

        else:
            self.frame = min(self.frame + 1, self.image_duration * len(self.images) - 1)
            if self.frame >= self.image_duration * len(self.images) - 1:
                self.done = True
    

    def image(self):

        return self.images[int(self.frame / self.image_duration)]
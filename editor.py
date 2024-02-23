import pygame
import sys


from scripts.utilities import load_image, load_images, Animation
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:

    def __init__(self):

        pygame.init()

        pygame.display.set_caption("Editor")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {
            "decor": load_images("tiles/decor"),
            "largeDecor": load_images("tiles/large_decor"),
            "grass": load_images("tiles/grass"),
            "stone": load_images("tiles/stone")
        }

        self.cameraMovement = [0, 0, 0, 0]

        self.tilemap = Tilemap(self, tile_size=16)

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False


    def run(self):

        while True:
            
            self.display.fill((0, 0, 0))

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_image = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_image.set_alpha(100)

            self.display.blit(current_tile_image, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
            
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        self.clicking = True
                    if event.button == 3:
                        self.right_clicking = True

                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])

                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_a:
                        self.cameraMovement[0] = 1
                    if event.key == pygame.K_d:
                        self.cameraMovement[1] = 1
                    if event.key == pygame.K_w:
                        self.cameraMovement[2] = 1
                    if event.key == pygame.K_s:
                        self.cameraMovement[3] = 1
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_a:
                        self.cameraMovement[0] = 0
                    if event.key == pygame.K_d:
                        self.cameraMovement[1] = 0
                    if event.key == pygame.K_w:
                        self.cameraMovement[2] = 0
                    if event.key == pygame.K_s:
                        self.cameraMovement[3] = 0
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Editor().run()
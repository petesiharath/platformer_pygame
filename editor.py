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

        self.camera_movement = [0, 0, 0, 0]

        self.tilemap = Tilemap(self, tile_size=16)

        try:
            self.tilemap.load("map.json")
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True


    def run(self):

        while True:
            
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.camera_movement[1] - self.camera_movement[0]) * 2
            self.scroll[1] += (self.camera_movement[3] - self.camera_movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_image = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_image.set_alpha(100)

            mouse_position = pygame.mouse.get_pos()
            mouse_position = (mouse_position[0] / RENDER_SCALE, mouse_position[1] / RENDER_SCALE)
            tile_position = (int((mouse_position[0] + self.scroll[0]) // self.tilemap.tile_size), int((mouse_position[1] + self.scroll[1]) // self.tilemap.tile_size))

            if self.ongrid:
                self.display.blit(current_tile_image, (tile_position[0] * self.tilemap.tile_size - self.scroll[0], tile_position[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_image, mouse_position)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_position[0]) + ";" + str(tile_position[1])] = {"type": self.tile_list[self.tile_group], "variant": self.tile_variant, "position": (tile_position)}

            if self.right_clicking:
                tile_location = str(tile_position[0]) + ";" + str(tile_position[1])
                if tile_location in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_location]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_image = self.assets[tile["type"]][tile["variant"]]
                    tile_rect = pygame.Rect(tile["position"][0] - self.scroll[0], tile["position"][1] - self.scroll[1], tile_image.get_width(), tile_image.get_height())
                    if tile_rect.collidepoint(mouse_position):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_image, (5, 5))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
            
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({"type": self.tile_list[self.tile_group], "variant": self.tile_variant, "position": (mouse_position[0] + self.scroll[0], mouse_position[1] + self.scroll[1])})
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

                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.camera_movement[0] = 1
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.camera_movement[1] = 1
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.camera_movement[2] = 1
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.camera_movement[3] = 1
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.tilemap.save("map.json")
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.camera_movement[0] = 0
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.camera_movement[1] = 0
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.camera_movement[2] = 0
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.camera_movement[3] = 0
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Editor().run()
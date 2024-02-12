import pygame

NEIGHBOUR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {"grass", "stone"}

class Tilemap:
    def __init__(self, game, tile_size=16):

        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ";10"] = {"type": "grass", "variant": 1, "position": (3 + i, 10)}
            self.tilemap["10;" + str(5 + i)] = {"type": "stone", "variant": 1, "position": (10, 5 + i)}

    def tiles_around(self, position):

        tiles = []
        tile_location = (int(position[0] // self.tile_size), int(position[1] // self.tile_size))

        for offset in NEIGHBOUR_OFFSETS:
            check_location = str(tile_location[0] + offset[0]) + ";" + str(tile_location[1] + offset[1])

            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])

        return tiles
    
    def physics_rects_around(self, position):

        rects = []
        for tile in self.tiles_around(position):
            if tile["type"] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile["position"][0] * self.tile_size, tile["position"][1] * self.tile_size, self.tile_size, self.tile_size))
        
        return rects
    
    def render(self, surface):

        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], tile["position"])

        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["position"][0] * self.tile_size, tile["position"][1] * self.tile_size))


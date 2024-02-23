import pygame
import json

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

NEIGHBOUR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {"grass", "stone"}
AUTOTILE_TYPES = {"grass", "stone"}


class Tilemap:
    
    def __init__(self, game, tile_size=16):

        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []


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
    

    def autotile(self):

        for location in self.tilemap:
            tile = self.tilemap[location]
            neighbours = set()

            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_location = str(tile["position"][0] + shift[0]) + ";" + str(tile["position"][1] + shift[1])
                if check_location in self.tilemap:
                    if self.tilemap[check_location]["type"] == tile["type"]:
                        neighbours.add(shift)

            neighbours = tuple(sorted(neighbours))
            if (tile["type"] in AUTOTILE_TYPES) and (neighbours in AUTOTILE_MAP):
                tile["variant"] = AUTOTILE_MAP[neighbours]
    

    def render(self, surface, offset=[0, 0]):

        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["position"][0] - offset[0], tile["position"][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                location = str(x) + ";" + str(y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    surface.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["position"][0] * self.tile_size - offset[0], tile["position"][1] * self.tile_size - offset[1]))


    def save(self, path):

        file = open(path, "w")
        json.dump({"tilemap": self.tilemap, "tile_size": self.tile_size, "offgrid": self.offgrid_tiles}, file)

    
    def load(self, path):

        file = open(path, "r")
        map_data = json.load(file)

        self.tilemap = map_data["tilemap"]
        self.tile_size = map_data["tile_size"]
        self.offgrid_tiles = map_data["offgrid"]
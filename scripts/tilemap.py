class Tilemap:
    def __init__(self, game, tileSize=16):

        self.game = game
        self.tileSize = tileSize
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ";10"] = {"type": "grass", "variant": 1, "position": (3 + i, 10)}
            self.tilemap["10;" + str(5 + i)] = {"type": "stone", "variant": 1, "position": (10, 5 + i)}
    
    def render(self, surface):

        for tile in self.offgrid_tiles:
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], tile["position"])

        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["position"][0] * self.tileSize, tile["position"][1] * self.tileSize))

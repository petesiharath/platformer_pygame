import pygame
import sys

from scripts.entities import PhysicsEntity
from scripts.utilities import load_image

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Platformer")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {
            "player": load_image("entities/player.png")
        }

        self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))
        self.playerMovement = [0, 0]

    def run(self):
        while True:
            
            self.display.fill((14, 219, 248))

            self.player.update((self.playerMovement[1] - self.playerMovement[0], 0))
            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
            
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.playerMovement[0] = 1
                    if event.key == pygame.K_d:
                        self.playerMovement[1] = 1
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.playerMovement[0] = 0
                    if event.key == pygame.K_d:
                        self.playerMovement[1] = 0

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Platformer = Game()
Platformer.run()
import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Platformer")
        self.screen = pygame.display.set_mode((640, 480))

        self.clock = pygame.time.Clock()

        self.playerImage = pygame.image.load("data/images/player.png")
        self.playerImagePosition = [160, 260]
        self.playerMovement = [0, 0]

        self.collisionArea = pygame.Rect(50, 50, 300, 50)

    def run(self):
        while True:
            
            self.screen.fill((14, 219, 248))

            img_r = pygame.Rect(self.playerImagePosition[0], self.playerImagePosition[1], self.playerImage.get_width(), self.playerImage.get_height())

            if img_r.colliderect(self.collisionArea):
                pygame.draw.rect(self.screen, (0, 100, 255), self.collisionArea)
            else:
                pygame.draw.rect(self.screen, (0, 255, 255), self.collisionArea)

            self.playerImagePosition[1] += self.playerMovement[1] - self.playerMovement[0]
            self.screen.blit(self.playerImage, self.playerImagePosition)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
            
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.playerMovement[0] = 1
                    if event.key == pygame.K_s:
                        self.playerMovement[1] = 1
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.playerMovement[0] = 0
                    if event.key == pygame.K_s:
                        self.playerMovement[1] = 0

            pygame.display.update()
            self.clock.tick(60)

Platformer = Game()
Platformer.run()
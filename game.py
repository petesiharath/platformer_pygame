import pygame
import sys
import random
import math

from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.utilities import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle


class Game:

    def __init__(self):

        pygame.init()

        pygame.display.set_caption("Platformer")
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {
            "decor": load_images("tiles/decor"),
            "large_decor": load_images("tiles/large_decor"),
            "grass": load_images("tiles/grass"),
            "stone": load_images("tiles/stone"),
            "player": load_image("entities/player.png"),
            "background": load_image("background.png"),
            "clouds": load_images("clouds"),
            "enemy/idle": Animation(load_images("entities/enemy/idle"), image_duration=6),
            "enemy/run": Animation(load_images("entities/enemy/run"), image_duration=4),
            "player/idle": Animation(load_images("entities/player/idle"), image_duration=6),
            "player/run": Animation(load_images("entities/player/run"), image_duration=4),
            "player/jump": Animation(load_images("entities/player/jump")),
            "player/slide": Animation(load_images("entities/player/slide")),
            "player/wall_slide": Animation(load_images("entities/player/wall_slide")),
            "particle/leaf": Animation(load_images("particles/leaf"), image_duration=20, loop=False),
            "particle/particle": Animation(load_images("particles/particle"), image_duration=6, loop=False),
            "gun": load_image("gun.png"),
            "projectile": load_image("projectile.png"),
        }

        self.clouds = Clouds(self.assets["clouds"], count=16)

        self.player = Player(self, (50, 50), (8, 15))
        self.player_movement = [0, 0]

        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load("map.json")

        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree["position"][0], 4 + tree["position"][1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract([("spawners", 0), ("spawners", 1)]):
            if spawner["variant"] == 0:
                self.player.position = spawner["position"]
            else:
                self.enemies.append(Enemy(self, spawner["position"], (8, 15)))
        
        self.projectiles = []
        self.particles = []

        self.scroll = [0, 0]


    def run(self):

        while True:
            
            self.display.blit(self.assets["background"], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    position = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, "leaf", position, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            for enemy in self.enemies.copy():
                enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.player_movement[1] - self.player_movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                image = self.assets["projectile"]
                self.display.blit(image, (projectile[0][0] - image.get_width() / 2 - render_scroll[0], projectile[0][1] - image.get_height() / 2 - render_scroll[1]))
                
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == "leaf":
                    particle.position[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
            
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.player_movement[0] = 1
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.player_movement[1] = 1
                    if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.player.dash()

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.player_movement[0] = 0
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.player_movement[1] = 0

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Platformer = Game()
Platformer.run()
import pygame
import math
import random

from scripts.particle import Particle
from scripts.spark import Spark


class PhysicsEntity:

    def __init__(self, game, entity_type, position, size):

        self.game = game
        self.type = entity_type
        self.position = list(position)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "left": False, "right": False}

        self.action = ""
        self.animation_offset = (-3, -3)
        self.flip = False
        self.set_action("idle")

        self.last_movement = [0, 0]


    def rect(self):

        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    

    def set_action(self, action):
        
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()


    def update(self, tilemap, movement=(0, 0)):

        self.collisions = {"up": False, "down": False, "left": False, "right": False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.position[0] += frame_movement[0]
        entity_rect = self.rect()

        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):

                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True

                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True

                self.position[0] = entity_rect.x

        self.position[1] += frame_movement[1]
        entity_rect = self.rect()

        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):

                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                    self.onfloor = True

                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True

                self.position[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation.update()


    def render(self, surface, offset=[0, 0]):
        
        surface.blit(pygame.transform.flip(self.animation.image(), self.flip, False), (self.position[0] - offset[0] + self.animation_offset[0], self.position[1] - offset[1] + self.animation_offset[1]))


class Enemy(PhysicsEntity):

    def __init__(self, game, position, size):

        super().__init__(game, "enemy", position, size)
        
        self.walking = 0


    def render(self, surface, offset=[0, 0]):
        
        super().render(surface, offset=offset)

        if self.flip:
            surface.blit(pygame.transform.flip(self.game.assets["gun"], True, False), (self.rect().centerx - 4 - self.game.assets["gun"].get_width() - offset[0], self.rect().centery - offset[1]))
        else:
            surface.blit(self.game.assets["gun"], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))
    
    
    def update(self, tilemap, movement=[0, 0]):

        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.position[1] + 23)):

                if self.collisions["right"] or self.collisions["left"]:
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])

            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)

            if not self.walking:
                distance = (self.game.player.position[0] - self.position[0], self.game.player.position[1] - self.position[1])

                if abs(distance[1]) < 16:
                    if self.flip and distance[0] < 0:
                        self.game.sfx["shoot"].play()
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                        for _ in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))

                    if not self.flip and distance[0] > 0:
                        self.game.sfx["shoot"].play()
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                        for _ in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))

        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx["hit"].play()

                for _ in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.particles.append(Particle(self.game, "particle", self.rect().center, velocity=[math.cos(angle + math.pi) * speed, math.sin(angle + math.pi) * speed], frame=random.randint(0, 7)))
                
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True



class Player(PhysicsEntity):
    
    def __init__(self, game, position, size):

        super().__init__(game, "player", position, size)
        self.air_time = 0
        self.jumps = 1
        self.dashing = 0
        self.stealth = False
        self.stealth_timer = 120

    
    def update(self, tilemap, movement = (0, 0)):

        super().update(tilemap, movement = movement)

        self.air_time += 1

        if self.air_time > 120:
            if not self.game.dead:
                self.game.screenshake = max(16, self.game.screenshake)
            self.game.dead += 1

        if self.collisions["down"]:
            self.air_time = 0
            self.jumps = 1

        self.wall_slide = False
        if (self.collisions["right"] or self.collisions["left"]) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions["right"]:
                self.flip = False
            else:
                self.flip = True
            self.set_action("wall_slide")

        if not self.wall_slide:

            if self.air_time > 4:
                self.set_action("jump")
            elif movement[0] != 0:
                self.set_action("run")
            else:
                self.set_action("idle")

        if abs(self.dashing) in {60, 50}:
            for _ in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                particle_velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, "particle", self.rect().center, velocity=particle_velocity, frame=random.randint(0, 7)))

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)

        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            self.velocity[1] = 0
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1

            particle_velocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, "particle", self.rect().center, velocity=particle_velocity, frame=random.randint(0, 7)))

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

        if self.stealth:
            self.stealth_timer = max(-120, self.stealth_timer - 1)
        else:
            self.stealth_timer = min(120, self.stealth_timer + 1)


    def render(self, surface, offset=[0, 0]):

        if abs(self.dashing) <= 50:
            super().render(surface, offset=offset)


    def jump(self):

        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 2.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True

            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -2.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True

        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            return True
    

    def dash(self):

        if not self.dashing:
            self.game.sfx["dash"].play()
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60


    def kill(self):
        
        for enemy in self.game.enemies:
            if self.flip:
                distance = [self.position[0] - enemy.position[0], self.position[1] - enemy.position[1]]
            else:
                distance = [enemy.position[0] - self.position[0], enemy.position[1] - self.position[1]]

            if 0 <= distance[0] < 16 and abs(distance[1]) < 10:
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx["hit"].play()
                self.game.enemies.remove(enemy)
                for _ in range(30):
                    angle = random.random() * math.pi * 2
                    self.game.sparks.append(Spark(enemy.rect().center, angle, 2 + random.random()))
                    
                self.game.sparks.append(Spark(enemy.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(enemy.rect().center, math.pi, 5 + random.random()))


    def toggle_stealth(self):

        if self.stealth_timer > 0:
            self.stealth = not self.stealth
    

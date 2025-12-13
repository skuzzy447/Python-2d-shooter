import pygame
import math
import random
import sys
from fractions import Fraction
from arrow import Arrow
from entity import Entity
from get_tileset import get_tileset
from constants import PATH

class Player(Entity):
    def __init__(self, screen, position, zoom, health=100):
        super().__init__(position, screen, None)
        self.shootfx = pygame.mixer.Sound(f"{PATH}/assets/fx/shoot.wav")
        self.shootfx.set_volume(0.5)
        self.screen = screen
        self.health = health
        self.position = position
        self.moving = False
        self.direction = 'down'
        self.frame_delay = 0.2
        self.move_speed = 1
        self.sprite_sheet = get_tileset(pygame.image.load(f"{PATH}/assets/player_sprite_sheet.png").convert_alpha(), zoom)
        self.animations = ((self.sprite_sheet[0], self.sprite_sheet[1], self.sprite_sheet[2], self.sprite_sheet[3], self.sprite_sheet[4]), 
                           (self.sprite_sheet[5], self.sprite_sheet[6], self.sprite_sheet[7], self.sprite_sheet[8], self.sprite_sheet[9]), 
                           (self.sprite_sheet[10], self.sprite_sheet[11], self.sprite_sheet[12], self.sprite_sheet[13], self.sprite_sheet[14]), 
                           (self.sprite_sheet[15], self.sprite_sheet[16], self.sprite_sheet[17], self.sprite_sheet[18], self.sprite_sheet[19]))
        self.animation = self.animations[0]
        self.sprite = self.animation[0]
        self.collider = pygame.Rect()
        self.collider.size = (14 * zoom, 24 * zoom)
        self.collider.center = (511, 510)
        self.knockback_counter = 0
        self.knockback_direction = 'down'

    def sprint(self):
        self.move_speed = 2

    def hit(self, damage, direction):
        self.knockback_counter = 4
        self.knockback_direction = direction
        self.health -= damage
        if self.health <= 0:
            pygame.quit()
            sys.exit()

    def shoot(self, screen, direction, enemies, zoom):
        rotation = math.degrees(math.atan2(-direction.y, direction.x))
        new_arrow = Arrow(screen, pygame.Vector2(self.position.x, self.position.y), enemies, zoom, rotation, direction)
        self.shootfx.play()
        return new_arrow
    
    def zoom(self, zoom):
        self.sprite_sheet = get_tileset(pygame.image.load(f"{PATH}/assets/player_sprite_sheet.png").convert_alpha(), zoom)
        self.animations = ((self.sprite_sheet[0], self.sprite_sheet[1], self.sprite_sheet[2], self.sprite_sheet[3], self.sprite_sheet[4]), 
                           (self.sprite_sheet[5], self.sprite_sheet[6], self.sprite_sheet[7], self.sprite_sheet[8], self.sprite_sheet[9]), 
                           (self.sprite_sheet[10], self.sprite_sheet[11], self.sprite_sheet[12], self.sprite_sheet[13], self.sprite_sheet[14]), 
                           (self.sprite_sheet[15], self.sprite_sheet[16], self.sprite_sheet[17], self.sprite_sheet[18], self.sprite_sheet[19]))
        if self.direction == 'up':
            self.animation = self.animations[2]
        elif self.direction == 'down':
            self.animation = self.animations[0]
        elif self.direction == 'left':
            self.animation = self.animations[3]
        elif self.direction == 'right':
            self.animation = self.animations[1]
        self.sprite = self.animation[0]

        self.collider.size = (16 * zoom, 28 * zoom)
        self.collider.center = (511, 510)
        
    def move(self, direction, colliders, dt):
        if self.direction != direction:
            self.direction = direction
            if direction == 'up':
                self.collider.center = (511, 508)
                self.animation = self.animations[2]
                self.sprite = self.animation[0]
            elif direction == 'down':
                self.collider.center = (511, 512)
                self.animation = self.animations[0]
                self.sprite = self.animation[0]
            elif direction == 'left':
                self.collider.center = (508, 510)
                self.animation = self.animations[3]
                self.sprite = self.animation[0]
            elif direction == 'right':
                self.collider.center = (514, 510)
                self.animation = self.animations[1]
                self.sprite = self.animation[0]
        if self.collider.collidelist(colliders) == -1:
            if direction == 'up':
                self.position.y -= dt * 2 * self.move_speed
            elif direction == 'down':
                self.position.y += dt * 2 * self.move_speed
            elif direction == 'left':
                self.position.x -= dt * 2 * self.move_speed
            elif direction == 'right':
                self.position.x += dt * 2 * self.move_speed

    def knockback(self, colliders, dt):
        if self.knockback_direction == 'up':
            self.collider.center = (511, 508)
            if self.collider.collidelist(colliders) == -1:
                self.position.y -= dt * 2
        elif self.knockback_direction == 'down':
            self.collider.center = (511, 512)
            if self.collider.collidelist(colliders) == -1:
                self.position.y += dt * 2
        elif self.knockback_direction == 'left':
            self.collider.center = (508, 510)
            if self.collider.collidelist(colliders) == -1:
                self.position.x -= dt * 2
        elif self.knockback_direction == 'right':
            self.collider.center = (514, 510)
            if self.collider.collidelist(colliders) == -1:
                self.position.x += dt * 2

    def update(self, colliders, dt):
        if self.moving:
            self.frame_delay -= dt * self.move_speed
            if self.frame_delay <= 0:
                self.frame_delay = 0.25
                self.sprite = self.animation[self.animation.index(self.sprite) + 1] if self.sprite in self.animation[:-1] else self.animation[4]
                if self.sprite == self.animation[1] or self.sprite == self.animation[3]:
                    sound = random.randint(0,1)
                    self.step_fx = pygame.mixer.Sound(f"{PATH}/assets/fx/footstep_grass_{sound}.wav")
                    self.step_fx.play()
                if self.sprite == self.animation[4]:
                    self.sprite = self.animation[0]
        else:
            self.frame_delay -= dt
            if self.frame_delay <= 0:
                self.sprite = self.animation[self.animation.index(self.sprite) + 1] if self.sprite in self.animation[:-1] else self.animation[4]
                self.frame_delay = 0.2
                self.sprite = self.animation[0]
        if self.knockback_counter > 0:
            self.knockback_counter -= 1
            self.knockback(colliders, dt)

def spawn_player(screen, world_size, tilemap, zoom):
    position = pygame.Vector2(world_size / 2, world_size / 2)
    if tilemap[int(position.y)][int(position.x)] >= 32:
        while tilemap[int(position.y)][int(position.x)] >= 32:
            position = pygame.Vector2(random.randint(0, world_size - 1), random.randint(0, world_size - 1))
    return Player(screen, position, zoom)
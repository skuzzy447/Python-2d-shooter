import pygame
import math
import random
from fractions import Fraction
from arrow import Arrow
from entity import Entity
from get_tileset import get_tileset
from constants import PATH

class Player(Entity):
    def __init__(self, screen, position, zoom, health=100):
        super().__init__(position, screen, None)
        self.screen = screen
        self.health = health
        self.position = position
        self.moving = False
        self.direction = 'down'
        self.frame_delay = 0
        self.move_speed = 1
        self.sprite_sheet = get_tileset(pygame.image.load(f"{PATH}/assets/player_sprite_sheet.png").convert_alpha(), zoom)
        self.animations = ((self.sprite_sheet[0], self.sprite_sheet[1], self.sprite_sheet[2], self.sprite_sheet[3], self.sprite_sheet[4]), 
                           (self.sprite_sheet[5], self.sprite_sheet[6], self.sprite_sheet[7], self.sprite_sheet[8], self.sprite_sheet[9]), 
                           (self.sprite_sheet[10], self.sprite_sheet[11], self.sprite_sheet[12], self.sprite_sheet[13], self.sprite_sheet[14]), 
                           (self.sprite_sheet[15], self.sprite_sheet[16], self.sprite_sheet[17], self.sprite_sheet[18], self.sprite_sheet[19]))
        self.animation = self.animations[0]
        self.sprite = self.animation[0]

    def move(self, direction):
        if self.direction == direction and not self.moving:
            self.moving = True
        else:
            self.direction = direction
            if not self.moving:
                if direction == 'up':
                    self.animation = self.animations[2]
                    self.sprite = self.animation[0]
                elif direction == 'down':
                    self.animation = self.animations[0]
                    self.sprite = self.animation[0]
                elif direction == 'left':
                    self.animation = self.animations[3]
                    self.sprite = self.animation[0]
                elif direction == 'right':
                    self.animation = self.animations[1]
                    self.sprite = self.animation[0]
                self.moving = True

    def sprint(self):
        self.move_speed = min(2, self.move_speed + 0.1)
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def shoot(self, screen, mouse_pos, enemies, zoom):
        direction = pygame.Vector2(mouse_pos[0] - 528, mouse_pos[1] - 528).normalize()
        rotation = math.degrees(math.atan2(-direction.y, direction.x))
        new_arrow = Arrow(screen, pygame.Vector2(self.position.x, self.position.y), enemies, zoom, rotation, direction)
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

    def update(self,tilemap, dt):
        if self.moving:
            self.frame_delay += dt
            if self.frame_delay >= 0.1 / self.move_speed:
                self.sprite = self.animation[self.animation.index(self.sprite) + 1] if self.sprite in self.animation[:-1] else self.animation[6]
                self.frame_delay = 0
                
                new_x, new_y = self.position.x, self.position.y
                if self.direction == 'up':
                    new_y -= Fraction(1, 2)
                elif self.direction == 'down':
                    new_y += Fraction(1, 2)
                elif self.direction == 'left':
                    new_x -= Fraction(1, 2)
                elif self.direction == 'right':
                    new_x += Fraction(1, 2)

                if not tilemap[int(new_y)][int(new_x)] >= 32:
                    self.position.x = new_x
                    self.position.y = new_y
                
                if self.sprite == self.animation[2]:
                    self.moving = False
                if self.sprite == self.animation[4]:
                    self.sprite = self.animation[0]
                    self.moving = False

def spawn_player(screen, world_size, tilemap, zoom):
    position = pygame.Vector2(world_size / 2, world_size / 2)
    if tilemap[int(position.y)][int(position.x)] >= 32:
        while tilemap[int(position.y)][int(position.x)] >= 32:
            position = pygame.Vector2(random.randint(0, world_size - 1), random.randint(0, world_size - 1))
    return Player(screen, position, zoom)
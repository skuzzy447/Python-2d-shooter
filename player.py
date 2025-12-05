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
        self.frame_delay = 0.2
        self.move_delay = 0.005
        self.move_speed = 1
        self.sprite_sheet = get_tileset(pygame.image.load(f"{PATH}/assets/player_sprite_sheet.png").convert_alpha(), zoom)
        self.animations = ((self.sprite_sheet[0], self.sprite_sheet[1], self.sprite_sheet[2], self.sprite_sheet[3], self.sprite_sheet[4]), 
                           (self.sprite_sheet[5], self.sprite_sheet[6], self.sprite_sheet[7], self.sprite_sheet[8], self.sprite_sheet[9]), 
                           (self.sprite_sheet[10], self.sprite_sheet[11], self.sprite_sheet[12], self.sprite_sheet[13], self.sprite_sheet[14]), 
                           (self.sprite_sheet[15], self.sprite_sheet[16], self.sprite_sheet[17], self.sprite_sheet[18], self.sprite_sheet[19]))
        self.animation = self.animations[0]
        self.sprite = self.animation[0]
        self.center = 512 - 16 * zoom

    def sprint(self):
        self.move_speed = 2

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def shoot(self, screen, direction, enemies, zoom):
        rotation = math.degrees(math.atan2(direction.y, direction.x))
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
        self.center = 512+14*zoom

    def can_move(self, tilemap, trees):
        new_x, new_y = self.position.x, self.position.y
        if self.direction == 'up':
            new_y -= 1
        elif self.direction == 'down':
            new_y += 1
        elif self.direction == 'left':
            new_x -= 1
        elif self.direction == 'right':
            new_x += 1
        if not tilemap[int(new_y)][int(new_x)] >= 32 and (int(new_x),int(new_y)) not in trees:
            return True
        else:
            return False
        
    def move(self, direction, tilemap, trees):
        if self.direction == direction and not self.moving:
            if self.can_move(tilemap, trees):
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
                if self.can_move(tilemap, trees):
                    self.moving = True

    def update(self, dt):
        if self.moving:
            self.frame_delay -= dt * self.move_speed
            self.move_delay -= (dt / 8) * self.move_speed
            if self.frame_delay <= 0:
                self.frame_delay = 0.2
                self.sprite = self.animation[self.animation.index(self.sprite) + 1] if self.sprite in self.animation[:-1] else self.animation[4]
            if self.move_delay <= 0:
                self.move_delay = 0.005
                new_x, new_y = self.position.x, self.position.y
                if self.direction == 'up':
                    new_y -= Fraction(1,int(16))
                elif self.direction == 'down':
                    new_y += Fraction(1,int(16))
                elif self.direction == 'left':
                    new_x -= Fraction(1,int(16))
                elif self.direction == 'right':
                    new_x += Fraction(1,int(16))
                self.position.x = new_x 
                self.position.y = new_y
                if self.position.x == round(self.position.x) and self.position.y == round(self.position.y):
                    self.moving = False
                if self.sprite == self.animation[4]:
                    self.sprite = self.animation[0]
        else:
            self.frame_delay -= dt
            if self.frame_delay <= 0:
                self.sprite = self.animation[self.animation.index(self.sprite) + 1] if self.sprite in self.animation[:-1] else self.animation[4]
                self.frame_delay = 0.2
                self.sprite = self.animation[0]

def spawn_player(screen, world_size, tilemap, zoom):
    position = pygame.Vector2(world_size / 2, world_size / 2)
    if tilemap[int(position.y)][int(position.x)] >= 32:
        while tilemap[int(position.y)][int(position.x)] >= 32:
            position = pygame.Vector2(random.randint(0, world_size - 1), random.randint(0, world_size - 1))
    return Player(screen, position, zoom)
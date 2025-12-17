import pygame
import multiprocessing
from fractions import Fraction
from random import randint
from entity import Entity
from get_tileset import get_tileset
from constants import *
from pathfind import astar

class Mob(Entity):
    def __init__(self, screen, position, zoom, sprite):
        super().__init__(position, screen, None)
        self.health = 100
        self.path = []
        self.pathfind_delay = 0
        self.new_x, self.new_y = 0,0
        self.moving = False
        self.sprite_sheet_file = sprite
        self.sprite_sheet = get_tileset(sprite, zoom)
        self.animations = ((self.sprite_sheet[0], self.sprite_sheet[1], self.sprite_sheet[2], self.sprite_sheet[3], self.sprite_sheet[4]), 
                           (self.sprite_sheet[5], self.sprite_sheet[6], self.sprite_sheet[7], self.sprite_sheet[8], self.sprite_sheet[9]), 
                           (self.sprite_sheet[10], self.sprite_sheet[11], self.sprite_sheet[12], self.sprite_sheet[13], self.sprite_sheet[14]), 
                           (self.sprite_sheet[15], self.sprite_sheet[16], self.sprite_sheet[17], self.sprite_sheet[18], self.sprite_sheet[19]))
        self.animation = self.animations[0]
        self.sprite = self.animation[0]
        self.anim_delay = 0
        self.direction = 'down'
        self.collider = pygame.Rect()
        self.collider.size = (22 * zoom, 22 * zoom)
        self.knockback_counter = 0
        self.knockback_direction = 'down'
    
    def change_direction(self, direction):
        if direction == self.direction:
            return
        else:
            self.direction = direction
            if direction == 'down':
                self.animation = self.animations[0]
            elif direction == 'right':
                self.animation = self.animations[1]
            elif direction == 'up':
                self.animation = self.animations[2]
            elif direction == 'left':
                self.animation = self.animations[3]
            self.sprite = self.animation[0]
    
    def move(self, dt):
        if len(self.path) > 0:
            if self.position.x == int(self.position.x) and self.position.y == int(self.position.y):      
                if len(self.path) > 1:
                    self.new_x, self.new_y = self.path.pop(1)
            if self.position.x - self.new_x > 0:
                self.change_direction('left')
                self.position.x -= Fraction(1/32)
            elif self.position.x - self.new_x < 0:
                self.change_direction('right')
                self.position.x += Fraction(1/32)
            if self.position.y - self.new_y > 0:
                self.change_direction('up')
                self.position.y -= Fraction(1/32)
            elif self.position.y - self.new_y < 0:
                self.change_direction('down')
                self.position.y += Fraction(1/32)
            
            if self.position.x == self.new_x and self.position.y == self.new_y:
                self.moving = False
                self.sprite = self.animation[0]
            else:
                self.moving = True
            if self.moving:
                self.anim_delay -= dt
                if self.anim_delay <= 0:
                    self.anim_delay = 0.15
                    self.sprite = self.animation[self.animation.index(self.sprite) + 1] if self.sprite in self.animation[:-1] else self.animation[4]
                if self.sprite == self.animation[4]:
                    self.sprite = self.animation[0]

    def zoom(self, zoom):
        self.sprite_sheet = get_tileset(self.sprite_sheet_file, zoom)
        self.animations = ((self.sprite_sheet[0], self.sprite_sheet[1], self.sprite_sheet[2], self.sprite_sheet[3], self.sprite_sheet[4]), 
                           (self.sprite_sheet[5], self.sprite_sheet[6], self.sprite_sheet[7], self.sprite_sheet[8], self.sprite_sheet[9]), 
                           (self.sprite_sheet[10], self.sprite_sheet[11], self.sprite_sheet[12], self.sprite_sheet[13], self.sprite_sheet[14]), 
                           (self.sprite_sheet[15], self.sprite_sheet[16], self.sprite_sheet[17], self.sprite_sheet[18], self.sprite_sheet[19]))
        if self.direction == 'down':
            self.animation = self.animations[0]
        elif self.direction == 'right':
            self.animation = self.animations[1]
        elif self.direction == 'up':
            self.animation = self.animations[2]
        elif self.direction == 'left':
            self.animation = self.animations[3]
        self.sprite = self.animation[0]
        self.collider.size = (22 * zoom, 22 * zoom)

    def pathfind(self, target, tilemap, trees, pipe):
        path = []
        path = astar((int(self.position.x), int(self.position.y)), (target.x, target.y), tilemap, trees)
        pipe.send(path)
        pipe.close()
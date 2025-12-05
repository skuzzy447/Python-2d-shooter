import pygame
import random
from constants import PATH
from pathfind import astar
from entity import Entity
from fractions import Fraction
from get_tileset import get_tileset

class Enemy(Entity):
    def __init__(self, screen, position, zoom):
        super().__init__(position, screen, None)
        self.health = 100
        self.path = []
        self.pathfind_delay = 0
        self.new_x, self.new_y = 0,0
        self.moving = False
        self.sprite_sheet = get_tileset(pygame.image.load(f"{PATH}/assets/slime_sprite_sheet.png").convert_alpha(), zoom)
        self.animations = ((self.sprite_sheet[0], self.sprite_sheet[1], self.sprite_sheet[2], self.sprite_sheet[3], self.sprite_sheet[4]), 
                           (self.sprite_sheet[5], self.sprite_sheet[6], self.sprite_sheet[7], self.sprite_sheet[8], self.sprite_sheet[9]), 
                           (self.sprite_sheet[10], self.sprite_sheet[11], self.sprite_sheet[12], self.sprite_sheet[13], self.sprite_sheet[14]), 
                           (self.sprite_sheet[15], self.sprite_sheet[16], self.sprite_sheet[17], self.sprite_sheet[18], self.sprite_sheet[19]))
        self.animation = self.animations[0]
        self.sprite = self.animation[0]
        self.anim_delay = 0
        self.direction = 'down'

    def pathfind(self, player_pos, tilemap, trees):
        self.path = astar((int(self.position.x), int(self.position.y)), (int(player_pos.x), int(player_pos.y)), tilemap, trees)

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
    
    def update(self, player_pos, tilemap, dt, zoom, trees):
        if self.pathfind_delay <= 0 and self.position.x in range(int(player_pos.x - 20), int(player_pos.x + 20)) and self.position.y in range(int(player_pos.y - 20), int(player_pos.y + 20)):
            self.pathfind(player_pos, tilemap, trees)
            self.pathfind_delay = 2.0
        if self.pathfind_delay > 0:
            self.pathfind_delay -= dt
        if self.move_delay <= 0:
            self.move(dt)
            self.move_delay = .02
        if self.move_delay > 0:
            self.move_delay -= dt
        self.draw(player_pos, zoom)

    def zoom(self, zoom):
        self.sprite_sheet = get_tileset(pygame.image.load(f"{PATH}/assets/slime_sprite_sheet.png").convert_alpha(), zoom)
        self.animations = ((self.sprite_sheet[0], self.sprite_sheet[1], self.sprite_sheet[2], self.sprite_sheet[3], self.sprite_sheet[4]), 
                           (self.sprite_sheet[5], self.sprite_sheet[6], self.sprite_sheet[7], self.sprite_sheet[8], self.sprite_sheet[9]), 
                           (self.sprite_sheet[10], self.sprite_sheet[11], self.sprite_sheet[12], self.sprite_sheet[13], self.sprite_sheet[14]), 
                           (self.sprite_sheet[15], self.sprite_sheet[16], self.sprite_sheet[17], self.sprite_sheet[18], self.sprite_sheet[19]))
        self.animation = self.animations[0]
        self.sprite = self.animation[0]

def add_enemy(screen, updateable, enemies, world_size, tilemap, zoom):
    position = pygame.Vector2(random.randint(0, world_size - 1), random.randint(0, world_size - 1))
    if tilemap[int(position.y)][int(position.x)] >= 32:
        while tilemap[int(position.y)][int(position.x)] >= 32:
            position = pygame.Vector2(random.randint(0, world_size - 1), random.randint(0, world_size - 1))
    new_enemy = Enemy(screen, position, zoom)
    updateable.add(new_enemy)
    enemies.add(new_enemy)
    return new_enemy
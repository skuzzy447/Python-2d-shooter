import pygame
import random
from constants import PATH
from pathfind import astar
from entity import Entity
from fractions import Fraction

class Enemy(Entity):
    def __init__(self, screen, position):
        super().__init__(position, screen, pygame.image.load(f"{PATH}/assets/enemy.png").convert_alpha())
        self.health = 100
        self.path = []
        self.pathfind_delay = 0
        self.new_x, self.new_y = 0,0
        self.moving = False

    def pathfind(self, player_pos, tilemap, trees):
        self.path = astar((int(self.position.x), int(self.position.y)), (int(player_pos.x), int(player_pos.y)), tilemap, trees)

    def move(self, dt):
        if len(self.path) > 0:
            if self.position.x == int(self.position.x) and self.position.y == int(self.position.y):      
                if len(self.path) > 1:
                    self.new_x, self.new_y = self.path.pop(1)
            if self.position.x - self.new_x > 0:
                self.position.x -= Fraction(1/16)
            elif self.position.x - self.new_x < 0:
                self.position.x += Fraction(1/16)
            if self.position.y - self.new_y > 0:
                self.position.y -= Fraction(1/16)
            elif self.position.y - self.new_y < 0:
                self.position.y += Fraction(1/16)
    
    def update(self, player_pos, tilemap, dt, zoom, trees):
        if self.pathfind_delay <= 0 and self.position.x in range(int(player_pos.x - 20), int(player_pos.x + 20)) and self.position.y in range(int(player_pos.y - 20), int(player_pos.y + 20)):
            self.pathfind(player_pos, tilemap, trees)
            self.pathfind_delay = 2.0
        if self.pathfind_delay > 0:
            self.pathfind_delay -= dt
        if self.move_delay <= 0:
            self.move(dt)
            self.move_delay = .05
        if self.move_delay > 0:
            self.move_delay -= dt
        self.draw(player_pos, zoom)

    def zoom(self, zoom):
        self.sprite = pygame.transform.scale(pygame.image.load(f"{PATH}/assets/enemy.png").convert_alpha(), (int(32 * zoom), int(32 * zoom)))

def add_enemy(screen, updateable, enemies, world_size, tilemap):
    position = pygame.Vector2(random.randint(0, world_size - 1), random.randint(0, world_size - 1))
    if tilemap[int(position.y)][int(position.x)] >= 32:
        while tilemap[int(position.y)][int(position.x)] >= 32:
            position = pygame.Vector2(random.randint(0, world_size - 1), random.randint(0, world_size - 1))
    new_enemy = Enemy(screen, position)
    updateable.add(new_enemy)
    enemies.add(new_enemy)
    return new_enemy
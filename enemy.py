import pygame
import random
from constants import PATH
from pathfind import astar
from entity import Entity

class Enemy(Entity):
    def __init__(self, screen, position):
        super().__init__(position, screen, pygame.image.load(f"{PATH}/assets/enemy.png").convert())
        self.health = 100
        self.path = []
        self.pathfind_delay = 0
        #self.sprite = pygame.image.load(f"{PATH}/assets/enemy.png").convert()

    def pathfind(self, player_pos, tilemap):
        self.path = astar((int(self.position.x), int(self.position.y)), (int(player_pos.x), int(player_pos.y)), tilemap)

    def move(self):
        if len(self.path) > 1:
            self.position.x, self.position.y = self.path.pop(1)
    
    def update(self, player_pos, tilemap, dt):
        if self.pathfind_delay <= 0 and self.position.x in range(int(player_pos.x - 20), int(player_pos.x + 20)) and self.position.y in range(int(player_pos.y - 20), int(player_pos.y + 20)):
            self.pathfind(player_pos, tilemap)
            self.pathfind_delay = 2.0
        if self.pathfind_delay > 0:
            self.pathfind_delay -= dt
        if self.move_delay <= 0:
            self.move()
            self.move_delay = 0.5
        if self.move_delay > 0:
            self.move_delay -= dt
        self.draw(player_pos)

def add_enemy(screen, updateable, enemies, world_size, tilemap):
    position = pygame.Vector2(random.randint(0, world_size - 1), random.randint(0, world_size - 1))
    if tilemap[int(position.y)][int(position.x)] == 2:
        while tilemap[int(position.y)][int(position.x)] == 2:
            position = pygame.Vector2(random.randint(0, world_size - 1), random.randint(0, world_size - 1))
    new_enemy = Enemy(screen, position)
    updateable.add(new_enemy)
    enemies.add(new_enemy)
    return new_enemy
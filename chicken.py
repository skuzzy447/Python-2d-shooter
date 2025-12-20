import pygame
import multiprocessing
from fractions import Fraction
from random import randint
from mob import Mob
from get_tileset import get_tileset
from constants import *
from pathfind import astar
from coin import Coin
from settings import world_size

class Chicken(Mob):
    def __init__(self, screen, position, zoom):
        super().__init__(screen, position, zoom, pygame.image.load(f"{PATH}/assets/chicken_sprite_sheet.png").convert_alpha(), False)
        self.target = position
    
    def update(self, player, tilemap, dt, zoom, trees, shop):
        if self.knockback_counter > 0:
            self.knockback_counter -= dt
            print(self.knockback_counter)
        if self.knockback_counter < 0:
            self.knockback_counter = 0
        if self.pathfind_delay <= 0 and not self.pf_process and int(self.position.x) in range(int(player.position.x - 20), int(player.position.x + 20)) and int(self.position.y) in range(int(player.position.y - 20), int(player.position.y + 20)):
            self.target = pygame.Vector2(randint(int(max(0, self.position.x - 2)), int(min(len(tilemap[0])-1,self.position.x + 2))), randint(int(max(0,self.position.y - 2)), int(min(len(tilemap[0])-1,self.position.y + 2))))
            while tilemap[int(self.target.y)][int(self.target.x)] >= 32 or self.target in trees:
                self.target = pygame.Vector2(randint(int(min(world_size-1,max(0,self.position.x - 2))), int(min(world_size-1,max(0,self.position.x - 2)))), randint(int(min(world_size-1,max(0,self.position.y - 2))), int(min(world_size-1,max(0,self.position.y + 2)))))
            self.parent_pipe, self.child_pipe = multiprocessing.Pipe()
            self.pf_process = multiprocessing.Process(target = self.pathfind, args = ((self.target, tilemap, trees, shop, self.child_pipe)))
            self.pf_process.start()
            self.pathfind_delay = randint(4,6)
        if self.parent_pipe and self.parent_pipe.poll():
            new_path = self.parent_pipe.recv()
            if new_path != None:
                self.path = new_path
            self.pf_process.join()
            self.pf_process = None
        if self.pathfind_delay > 0:
            self.pathfind_delay -= dt
        if self.move_delay <= 0:
            self.move(dt, player)
            self.move_delay = 0.02
            if abs(self.position.x - self.new_x) < dt * 2:
                self.position.x = self.new_x
            if abs(self.position.y - self.new_y) < dt * 2:  
                self.position.y = self.new_y
        if self.move_delay > 0:
            self.move_delay -= dt
        if int(self.position.x) in range(int(player.position.x - 20), int(player.position.x + 20)) and int(self.position.y) in range(int(player.position.y - 20), int(player.position.y + 20)):
            self.collider.center = (self.position.x * 32 * zoom - (player.position.x * 32 * zoom - 512), self.position.y * 32 * zoom - (player.position.y * 32 * zoom - 510))
        self.draw(player.position, zoom)

    def die(self, updateable, zoom):
        for _ in range(randint(1,3)):
            new_coin = Coin(self.screen, pygame.Vector2(self.position.x, self.position.y), zoom)
            updateable.add(new_coin)
        self.kill()

def add_chicken(screen, updateable, passives, mobs, world_size, tilemap, trees, zoom):
    position = pygame.Vector2(randint(0, world_size - 1), randint(0, world_size - 1))
    if tilemap[int(position.y)][int(position.x)] >= 32 or (position.x, position.y) in trees:
        while tilemap[int(position.y)][int(position.x)] >= 32 or (position.x, position.y) in trees:
            position = pygame.Vector2(randint(0, world_size - 1), randint(0, world_size - 1))
    new_chicken = Chicken(screen, position, zoom)
    updateable.add(new_chicken)
    mobs.add(new_chicken)
    passives.add(new_chicken)
    return new_chicken
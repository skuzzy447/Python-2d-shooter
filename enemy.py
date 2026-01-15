import pygame
from random import randint
from constants import PATH
from mob import Mob
from fractions import Fraction
from coin import Coin

class Enemy(Mob):
    def __init__(self, screen, position, zoom):
        super().__init__(screen, position, zoom, pygame.image.load(f"{PATH}/assets/slime_sprite_sheet.png").convert_alpha(), True)

    def check_collision(self, player):
        if self.collider.colliderect(player.collider):
            self.move_delay = 0.3
            self.knockback_counter = 4
            player.hit(10, self.direction)
            if self.direction == "up":
                self.knockback_direction = 'down'
            if self.direction == "down":
                self.knockback_direction = 'up'
            if self.direction == "left":
                self.knockback_direction = 'right'
            if self.direction == "right":
                self.knockback_direction = 'left'

    def knockback(self, dt):
        if self.knockback_direction == 'up':
            self.position.y -= Fraction(1/8)
        elif self.knockback_direction == 'down':
            self.position.y += Fraction(1/8)
        elif self.knockback_direction == 'left':
            self.position.x -= Fraction(1/8)
        elif self.knockback_direction == 'right':
            self.position.x += Fraction(1/8)

    def update(self, player, tilemap, dt, zoom, trees, shops):
        if self.pathfind_delay <= 0 and not self.pf_process and int(self.position.x) in range(int(player.position.x - 20), int(player.position.x + 20)) and int(self.position.y) in range(int(player.position.y - 20), int(player.position.y + 20)):
            if self.position != player.position:
                self.path = self.pathfind(player.position, tilemap, trees, shops)
                self.pathfind_delay = 0.5
        if self.pathfind_delay > 0:
            self.pathfind_delay -= dt
        if self.move_delay <= 0:
            self.move(dt, player)
            self.move_delay = .02
        if self.move_delay > 0:
            self.move_delay -= dt
        if int(self.position.x) in range(int(player.position.x - 20), int(player.position.x + 20)) and int(self.position.y) in range(int(player.position.y - 20), int(player.position.y + 20)):
            self.collider.center = (self.position.x * 32 * zoom - (player.position.x * 32 * zoom - 512), self.position.y * 32 * zoom - (player.position.y * 32 * zoom - 510))
        if self.knockback_counter > 0:
            self.knockback_counter -= 1
            self.knockback(dt)
        if self.knockback_counter < 0:
            self.knockback_counter = 0
        self.check_collision(player)
        self.draw(player.position, zoom)

    def die(self, updateable, zoom):
        for _ in range(randint(2,5)):
            new_coin = Coin(self.screen, pygame.Vector2(self.position.x, self.position.y), zoom)
            updateable.add(new_coin)  
        self.kill()

def add_enemy(screen, updateable, enemies, mobs, world_size, tilemap, trees, zoom):
    position = pygame.Vector2(randint(0, world_size - 1), randint(0, world_size - 1))
    if not tilemap[int(position.y)][int(position.x)] >= 32 or not (position.x, position.y) in trees:
        position = pygame.Vector2(randint(0, world_size - 1), randint(0, world_size - 1))
        new_enemy = Enemy(screen, position, zoom)
        updateable.add(new_enemy)
        mobs.add(new_enemy)
        enemies.add(new_enemy)
        return new_enemy
import pygame
from random import randint
from get_tileset import get_tileset
from constants import PATH

class Coin(pygame.sprite.Sprite):
    def __init__(self, screen, position, zoom):
        super().__init__()
        self.screen = screen
        self.position = position
        self.target = pygame.Vector2(self.position.x + randint(-3,3) * 0.1, self.position.y + randint(-3,3) * 0.1)
        self.sprite_sheet = get_tileset(pygame.image.load(f"{PATH}/assets/coin_sprite_sheet.png").convert_alpha(), zoom, tile_width=16, tile_height=16)
        self.sprite = self.sprite_sheet[0]
        self.frame_delay = 0
        self.collider = pygame.Rect()
        self.collider.size = (64 * zoom, 64 * zoom)
        self.speed = 1

    def draw(self, player_pos, zoom):
        screen_x = self.position.x * 32 * zoom - (player_pos.x * 32 * zoom - 512)
        screen_y = self.position.y * 32 * zoom - (player_pos.y * 32 * zoom - 512)
        if screen_x > 0 and screen_y > 0:
            self.screen.blit(self.sprite, (screen_x - 8 * zoom, screen_y - 8 * zoom))

    def zoom(self, zoom):
        self.sprite_sheet = get_tileset(pygame.image.load(f"{PATH}/assets/coin_sprite_sheet.png").convert_alpha(), zoom, tile_width=16, tile_height=16)
        self.sprite = self.sprite_sheet[0]
        self.collider.size = (16 * zoom, 16 * zoom)

    def check_collision(self, player, dt):
        if self.collider.colliderect(player.collider):
            self.target= player.position
            self.speed += dt * 5
            if self.position.distance_to(player.position) < 0.5:
                player.coins += 1
                self.kill()

    def update(self, player, dt, zoom):
        if self.frame_delay > 0:
            self.frame_delay -= dt
        else:
            self.frame_delay = 0.1
            if self.sprite == self.sprite_sheet[13]:
                self.sprite = self.sprite_sheet[0]
            else:
                self.sprite = self.sprite_sheet[self.sprite_sheet.index(self.sprite) + 1] if self.sprite in self.sprite_sheet[:-1] else self.sprite_sheet[13]
        if self.position.distance_to(self.target) > 0.1:
            direction = (self.target - self.position).normalize()
            self.position += direction * dt * 2 * self.speed
        if int(self.position.x) in range(int(player.position.x - 20), int(player.position.x + 20)) and int(self.position.y) in range(int(player.position.y - 20), int(player.position.y + 20)):
            self.collider.center = (self.position.x * 32 * zoom - (player.position.x * 32 * zoom - 512), self.position.y * 32 * zoom - (player.position.y * 32 * zoom - 510))
        self.check_collision(player, dt)
        self.draw(player.position, zoom)
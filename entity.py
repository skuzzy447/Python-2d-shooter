import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, position, screen, sprite):
        super().__init__()
        self.position = position
        self.screen = screen
        self.sprite = sprite
        self.move_delay = 0

    def move(self):
        pass

    def draw(self, player_pos, zoom):
        screen_x = self.position.x * 32 * zoom - (player_pos.x * 32 * zoom - 512)
        screen_y = self.position.y * 32 * zoom - (player_pos.y * 32 * zoom - 512)
        if screen_x > 0 and screen_y > 0:
            self.screen.blit(self.sprite, (screen_x - 16 * zoom, screen_y - 16 * zoom))

    def zoom(self, zoom):
        pass

    def update(self):
        pass
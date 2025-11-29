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

    def draw(self, player_pos):
        screen_x = self.position.x * 32 - (player_pos.x * 32 - 512)
        screen_y = self.position.y * 32 - (player_pos.y * 32 - 512)
        if screen_x > 0 and screen_y > 0:
            self.screen.blit(self.sprite, (screen_x, screen_y))

    def update(self):
        pass
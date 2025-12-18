import pygame
from constants import PATH
class House(pygame.sprite.Sprite):
    def __init__(self, position, screen, zoom):
        super().__init__()
        self.position = position
        self.screen = screen
        self.sprite = pygame.transform.scale(pygame.image.load(f"{PATH}/assets/house.png").convert_alpha(), (int(130 * zoom),(int(128 * zoom))))
        self.collider = pygame.Rect()
        self.collider.size = (130 * zoom, 128 * zoom)

    def update(self, player, zoom):
        self.sprite = pygame.transform.scale(pygame.image.load(f"{PATH}/assets/house.png").convert_alpha(), (int(130 * zoom),(int(128 * zoom))))
        self.collider.size = (110 * zoom, 64 * zoom)
        screen_x = (16*zoom) + self.position.x * 32 * zoom - (player.position.x * 32 * zoom - 512)
        screen_y = self.position.y * 32 * zoom - (player.position.y * 32 * zoom - 512)
        self.collider.center = (screen_x + 52 * zoom, screen_y + 80 * zoom)
        if 1024 + 32*zoom> screen_x > -112 * zoom and 1024 + 32*zoom > screen_y > -112 * zoom:
            self.screen.blit(self.sprite, (screen_x - 16 * zoom, screen_y - 16 * zoom))
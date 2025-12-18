import pygame
from constants import PATH
class House(pygame.sprite.Sprite):
    def __init__(self, position, screen, zoom):
        super().__init__()
        self.position = position
        self.screen = screen
        self.sprite = pygame.transform.scale(pygame.image.load(f"{PATH}/assets/house.png").convert_alpha(), (int(130 * zoom),(int(128 * zoom))))
        self.collider1 = pygame.Rect()
        self.collider1.size = (78 * zoom, 64 * zoom)
        self.collider2 = pygame.Rect()
        self.collider2.size = (30 * zoom, 42 * zoom)
        self.collider3 = pygame.Rect()
        self.collider3.size = (4 * zoom, 40 * zoom)

    def update(self, player, zoom):
        self.sprite = pygame.transform.scale(pygame.image.load(f"{PATH}/assets/house.png").convert_alpha(), (int(130 * zoom),(int(128 * zoom))))
        self.collider1.size = (78 * zoom, 64 * zoom)
        self.collider2.size = (30 * zoom, 42 * zoom)
        self.collider3.size = (2 * zoom, 20 * zoom)
        screen_x = (5*zoom) + self.position.x * 32 * zoom - (player.position.x * 32 * zoom - 512)
        screen_y = self.position.y * 32 * zoom - (player.position.y * 32 * zoom - 512)
        self.collider1.center = (screen_x + 35 * zoom, screen_y + 80 * zoom)
        self.collider2.center = (screen_x + 90 * zoom, screen_y + 69 * zoom)
        self.collider3.center = (screen_x + 103 * zoom, screen_y + 100 * zoom)
        if 1024 + 32*zoom> screen_x > -112 * zoom and 1024 + 32*zoom > screen_y > -112 * zoom:
            self.screen.blit(self.sprite, (screen_x - 16 * zoom, screen_y - 16 * zoom))
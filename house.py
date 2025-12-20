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
        self.collider3.size = (2 * zoom, 19 * zoom)
        self.entry = pygame.Rect()
        self.entry.size = (28 * zoom, 16 * zoom)

    def zoom(self, zoom):
        self.sprite = pygame.transform.scale(pygame.image.load(f"{PATH}/assets/house.png").convert_alpha(), (int(130 * zoom),(int(128 * zoom))))
        self.collider1.size = (78 * zoom, 64 * zoom)
        self.collider2.size = (28 * zoom, 42 * zoom)
        self.collider3.size = (2 * zoom, 19 * zoom)
        self.entry.size = (28 * zoom, 16 * zoom)

    def update(self, player, zoom):
        screen_x = (5*zoom) + self.position.x * 32 * zoom - (player.position.x * 32 * zoom - 512)
        screen_y = self.position.y * 32 * zoom - (player.position.y * 32 * zoom - 512)
        self.collider1.center = ((5*zoom) + self.position.x * 32 * zoom - (player.position.x * 32 * zoom - 512) + 35 * zoom, self.position.y * 32 * zoom - (player.position.y * 32 * zoom - 512) + 80 * zoom)
        self.collider2.center = ((5*zoom) + self.position.x * 32 * zoom - (player.position.x * 32 * zoom - 512) + 90 * zoom, self.position.y * 32 * zoom - (player.position.y * 32 * zoom - 512) + 69 * zoom)
        self.collider3.center = ((5*zoom) + self.position.x * 32 * zoom - (player.position.x * 32 * zoom - 512) + 103 * zoom, self.position.y * 32 * zoom - (player.position.y * 32 * zoom - 512) + 100 * zoom)
        self.entry.center = ((5*zoom) + self.position.x * 32 * zoom - (player.position.x * 32 * zoom - 512) + 89 * zoom, self.position.y * 32 * zoom - (player.position.y * 32 * zoom - 512) + 100 * zoom)
        if 1024 + 32*zoom> screen_x > -112 * zoom and 1024 + 32*zoom > screen_y > -112 * zoom:
            self.screen.blit(self.sprite, (screen_x - 16 * zoom, screen_y - 16 * zoom))
        if self.entry.colliderect(player.collider):
            print("here")
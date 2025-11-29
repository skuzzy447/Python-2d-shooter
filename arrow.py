from entity import Entity
import pygame
from constants import PATH

class Arrow(Entity):
    def __init__(self, screen, position, enemies, rotation=0 , direction=pygame.Vector2(1,0)):
        super().__init__(position, screen, pygame.image.load(f"{PATH}/assets/arrow.png").convert_alpha())
        self.sprite = pygame.transform.rotate(self.sprite, rotation)
        self.direction = direction
        self.enemies = enemies

    def move(self, dt):
        self.position += self.direction * 20 * dt

    def check_collision(self, enemies):
        for enemy in enemies:
            if int(self.position.x) == int(enemy.position.x) and int(self.position.y) == int(enemy.position.y):
                enemy.health -= 100
                self.kill()
                if enemy.health <= 0:
                    enemy.kill()

    def update(self, player_pos, dt):
        self.move(dt)
        self.draw(player_pos)
        self.check_collision(self.enemies)
        if self.position.x > player_pos.x + 16 or self.position.x < player_pos.x - 16 or self.position.y > player_pos.y + 16 or self.position.y < player_pos.y - 16:
            self.kill()
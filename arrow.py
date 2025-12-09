from entity import Entity
import pygame
import math
from constants import PATH
from decimal import Decimal, ROUND_HALF_UP

class Arrow(Entity):
    def __init__(self, screen, position, enemies, zoom, rotation=0 , direction=pygame.Vector2(1,0)):
        super().__init__(position, screen, pygame.transform.scale(pygame.image.load(f"{PATH}/assets/arrow.png").convert_alpha(), (int(32 * zoom), int(32 * zoom))))
        self.rotation = rotation
        self.sprite = pygame.transform.rotate(self.sprite, self.rotation)
        self.direction = direction
        self.enemies = enemies
        self.stuck = False
        self.despawn_timer = 5
        self.hitfx = pygame.mixer.Sound(f"{PATH}/assets/fx/arrow_hit.wav")
        self.hitfx.set_volume(0.25)

    def move(self, dt):
        self.position += self.direction * 20 * dt

    def check_collision(self, enemies, trees, player_position, zoom):
        for enemy in enemies:
            if int(self.position.x) == int(enemy.position.x) and int(self.position.y) == int(enemy.position.y):
                self.hitfx.play()
                enemy.health -= 25
                enemy.position += self.direction / 2
                self.kill()
                if enemy.health <= 0:
                    enemy.kill()
        x = Decimal(self.position.x).quantize(Decimal('1'),rounding = ROUND_HALF_UP)
        y = Decimal(self.position.y).quantize(Decimal('1'),rounding = ROUND_HALF_UP)
        screen_x = float(x) * 32 * zoom - (player_position.x * 32 * zoom - 512)
        screen_y = float(y) * 32 * zoom - (player_position.y * 32 * zoom - 512)
        if (int(x), int(y)) in trees:
            self.stuck = True  
            self.direction = pygame.Vector2(screen_x - 512, screen_y - 512).normalize()
            self.rotation = math.degrees(math.atan2(-self.direction.y, self.direction.x))
    
    def zoom(self, zoom):
        self.sprite = pygame.transform.scale(pygame.image.load(f"{PATH}/assets/arrow.png").convert_alpha(), (int(32 * zoom), int(32 * zoom)))
        self.sprite = pygame.transform.rotate(self.sprite, self.rotation)

    def update(self, player_pos, tilemap, dt, zoom, trees):
        if not self.stuck:
            self.move(dt)
            self.draw(player_pos, zoom)
            self.check_collision(self.enemies, trees, player_pos, zoom)
        else:
            self.draw(player_pos, zoom)
            self.despawn_timer -= dt
            if self.despawn_timer <= 0:
                self.kill()
        if self.position.x > player_pos.x + 16 or self.position.x < player_pos.x - 16 or self.position.y > player_pos.y + 16 or self.position.y < player_pos.y - 16:
            self.kill()
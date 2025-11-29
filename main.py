import pygame
import json
import math
from generate_world import generate
from constants import *
from enemy import Enemy
from enemy import add_enemy
from arrow import Arrow

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 1024))
    clock = pygame.time.Clock()
    dt = 0
    running = True

    Player = pygame.image.load(f"{PATH}/assets/player.png").convert()
    Grass = pygame.image.load(f"{PATH}/assets/grass.png").convert()
    Mountain = pygame.image.load(f"{PATH}/assets/cobblestone.png").convert()
    Water = pygame.image.load(f"{PATH}/assets/water.png").convert()

    world_size = 128
    player_pos = pygame.Vector2(world_size / 2 - 2, world_size / 2 - 2)
    moving = False
    move_cooldown = 0
    max_enemies = world_size // 16


    generate(world_size)
    tilemap = []
    with open(f"{PATH}/tilemap.json", "r") as f:
        tilemap = json.load(f)

    updateable = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    for _ in range(max_enemies):
        new_enemy = add_enemy(screen, updateable, enemies, world_size)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    direction = pygame.Vector2(pygame.mouse.get_pos()[0] - 512, pygame.mouse.get_pos()[1] - 512).normalize()
                    rotation = math.degrees(math.atan2(-direction.y, direction.x))
                    new_arrow = Arrow(screen, pygame.Vector2(player_pos.x, player_pos.y), enemies, rotation, direction)
                    updateable.add(new_arrow)

        keys = pygame.key.get_pressed()
        if not moving:
            if keys[pygame.K_a] and player_pos.x > 0:
                if tilemap[int(player_pos.y)][int(player_pos.x - 1)] != 2:
                    player_pos.x -= 1
                    moving = True
            if keys[pygame.K_d] and player_pos.x < world_size - 1:
                if tilemap[int(player_pos.y)][int(player_pos.x + 1)] != 2:
                    player_pos.x += 1
                    moving = True
            if keys[pygame.K_w] and player_pos.y > 0:
                if tilemap[int(player_pos.y - 1)][int(player_pos.x)] != 2:
                    player_pos.y -= 1
                    moving = True
            if keys[pygame.K_s] and player_pos.y < world_size - 1:
                if tilemap[int(player_pos.y + 1)][int(player_pos.x)] != 2:
                    player_pos.y += 1
                    moving = True

        if moving and move_cooldown <= 0:
            move_cooldown = 0.05
        if moving and move_cooldown > 0:
            move_cooldown -= dt
        if moving and move_cooldown <= 0:
            moving = False

        screen.fill((100,0,25))

        for y in range(max(0, int(player_pos.y - 32)), min(world_size, int(player_pos.y + 32))):
            for x in range(max(0, int(player_pos.x - 32)), min(world_size, int(player_pos.x + 32))):
                screen_x = x * 32 - (player_pos.x * 32 -496)
                screen_y = y * 32 - (player_pos.y * 32 -496)
                if tilemap[y][x] == 0:
                    screen.blit(Grass, (screen_x, screen_y))
                if tilemap[y][x] == 1:
                    screen.blit(Water, (screen_x, screen_y))
                if tilemap[y][x] == 2:
                    screen.blit(Mountain, (screen_x, screen_y))
        
        for entity in updateable:
            if isinstance(entity, Enemy):
                entity.update(player_pos, tilemap, dt)
            else:
                entity.update(player_pos, dt)
        screen.blit(Player, (512 - 16, 512 - 16))
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
import pygame
import json
from math import ceil
from generate_world import generate
from constants import *
from player import Player
from enemy import Enemy
from enemy import add_enemy
from arrow import Arrow
from get_tileset import get_tileset

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 1024))
    clock = pygame.time.Clock()
    dt = 0
    running = True

    ground_tiles = get_tileset(pygame.image.load(f"{PATH}/assets/ground_tileset.png").convert_alpha())

    world_size = 128
    max_enemies = world_size // 16


    generate(world_size)
    tilemap = []
    with open(f"{PATH}/tilemap.json", "r") as f:
        tilemap = json.load(f)

    updateable = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = Player(screen, pygame.Vector2(world_size / 2 - 2, world_size / 2 - 2))
    for _ in range(max_enemies):
        new_enemy = add_enemy(screen, updateable, enemies, world_size, tilemap)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    updateable.add(player.shoot(screen, pygame.mouse.get_pos(), enemies))

        keys = pygame.key.get_pressed()
        if not player.moving:
            if keys[pygame.K_a] and player.position.x > 0:
                if not tilemap[int(player.position.y)][int(player.position.x - 1)] >= 32:
                    player.move('left')
            elif keys[pygame.K_d] and player.position.x < world_size - 1:
                if not tilemap[int(player.position.y)][int(player.position.x + 1)] >= 32:
                    player.move('right')
            elif keys[pygame.K_w] and player.position.y > 0:
                if not tilemap[int(player.position.y - 1)][int(player.position.x)] >= 32:
                    player.move('up')
            elif keys[pygame.K_s] and player.position.y < world_size - 1:
                if not tilemap[int(player.position.y + 1)][int(player.position.x)] >= 32:
                    player.move('down')
            if keys[pygame.K_LSHIFT]:
                player.sprint()
            else:
                player.move_speed = 1

        screen.fill((44.7,45.9,10.6))
        player.update(tilemap, dt)
        for y in range(max(0, int(player.position.y - 32)), min(world_size, int(player.position.y + 32))):
            for x in range(max(0, int(player.position.x - 32)), min(world_size, int(player.position.x + 32))):
                screen_x = x * 32 - (player.position.x * 32 - 512)
                screen_y = y * 32 - (player.position.y * 32 - 512)
                screen.blit(ground_tiles[tilemap[y][x]], (screen_x, screen_y))
        player.draw(player.position)
        for entity in updateable:
            if isinstance(entity, Enemy):
                entity.update(player.position, tilemap, dt)
            else:
                entity.update(player.position, dt)


        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
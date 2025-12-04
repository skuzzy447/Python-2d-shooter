import pygame
import json
from generate_world import generate
from constants import *
from settings import *
from player import Player
from player import spawn_player
from enemy import Enemy
from enemy import add_enemy

def main(): 
    global zoom
    pygame.init()
    screen = pygame.display.set_mode((1024, 1024))
    clock = pygame.time.Clock()   
    dt = 0
    running = True
    ground_tiles = get_tileset(pygame.image.load(f"{PATH}/assets/ground_tileset.png").convert_alpha(), zoom)
    tilemap, tree_list = generate(world_size)

    updateable = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = spawn_player(screen, world_size, tilemap, zoom)
    center = pygame.Surface((1,1))
    center.fill((0,0,255))

    def zoom_entities(zoom_add):
        nonlocal ground_tiles
        global zoom
        zoom += zoom_add
        ground_tiles = get_tileset(pygame.image.load(f"{PATH}/assets/ground_tileset.png").convert_alpha(), zoom)
        for entity in updateable:
            entity.zoom(zoom)
        player.zoom(zoom)
    while running:
        if len(enemies) < max_enemies:
            new_enemy = add_enemy(screen, updateable, enemies, world_size, tilemap)
            new_enemy.zoom(zoom)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    updateable.add(player.shoot(screen, pygame.mouse.get_pos(), enemies, zoom))
            
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    if zoom < 2.5:
                        zoom_entities(0.5)
                elif event.y < 0:
                    if zoom > 1.0:
                        zoom_entities(-0.5)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_EQUALS:
                    if zoom < 2.5:
                        zoom_entities(0.5)
                if event.key == pygame.K_MINUS:
                    if zoom > 1.0:
                        zoom_entities(-0.5)
                if event.key == pygame.K_LSHIFT:
                     player.sprint()
            
            if event.type == pygame.KEYUP:
                 if event.key == pygame.K_LSHIFT:
                      player.move_speed = 1
        keys = pygame.key.get_pressed()
        if not player.moving:
            if keys[pygame.K_a] and player.position.x > 0:
                    player.move('left', tilemap, tree_list)
            elif keys[pygame.K_d] and player.position.x < world_size - 1:
                    player.move('right', tilemap, tree_list)
            elif keys[pygame.K_w] and player.position.y > 0:
                    player.move('up', tilemap, tree_list)
            elif keys[pygame.K_s] and player.position.y < world_size - 1:
                    player.move('down', tilemap, tree_list)

        screen.fill((44.7,45.9,10.6))
        player.update(dt)
        for y in range(max(0, int(player.position.y - 32 // zoom)), min(world_size, int(player.position.y + 32 // zoom))):
            for x in range(max(0, int(player.position.x - 32 // zoom)), min(world_size, int(player.position.x + 32 // zoom))):
                screen_x = x * 32 * zoom - (player.position.x * 32 * zoom - 512)
                screen_y = y * 32 * zoom - (player.position.y * 32 * zoom - 512)
                screen.blit(ground_tiles[tilemap[y][x]], (screen_x, screen_y))
                for (tree_x, tree_y) in tree_list:
                    if tree_x == x and tree_y == y:
                        screen.blit(ground_tiles[30], (screen_x, screen_y))
        #player.draw(player.position, zoom)
        screen.blit(player.sprite, (512,512))
        screen.blit(center, (512+16*zoom,512+16*zoom))
        for entity in updateable:
                entity.update(player.position, tilemap, dt, zoom, tree_list)
        for y in range(max(0, int(player.position.y - 32 // zoom)), min(world_size, int(player.position.y + 32 // zoom))):
            for x in range(max(0, int(player.position.x - 32 // zoom)), min(world_size, int(player.position.x + 32 // zoom))):
                screen_x = x * 32 * zoom - (player.position.x * 32 * zoom - 512)
                screen_y = y * 32 * zoom - (player.position.y * 32 * zoom - 512)
                for (tree_x, tree_y) in tree_list:
                    if tree_x == x and tree_y == y:
                        screen.blit(ground_tiles[29], (screen_x, (y - 1) * 32 * zoom - (player.position.y * 32 * zoom - 512)))
        


        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
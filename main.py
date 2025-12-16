import pygame
import random
from generate_world import generate
from constants import *
from settings import *
from player import Player, spawn_player
from enemy import Enemy, add_enemy
from update_render import update_render

def main(): 
    global zoom
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1024, 1024))
    clock = pygame.time.Clock()   
    dt = 0
    running = True
    ground_tiles = get_tileset(pygame.image.load(f"{PATH}/assets/ground_tileset.png").convert_alpha(), zoom)
    tilemap, tree_list = generate(world_size)

    updateable = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = spawn_player(screen, world_size, tilemap, zoom)
    colliders = []

    music_delay = 10

    light = pygame.Surface((1024, 1024),pygame.SRCALPHA)
    light.fill((10, 10, 20))
    current_color = next(COLORS)
    next_color = next(COLORS)
    start_time = pygame.time.get_ticks()
    def inter_color(color1, color2, factor):
         r1,g1,b1,a1 = color1
         r2,g2,b2,a2 = color2
         r = int(r1+(r2-r1)*factor)
         g = int(g1+(g2-g1)*factor)
         b = int(b1+(b2-b1)*factor)
         a = int(a1+(a2-a1)*factor)
         return r,g,b,a

    def zoom_entities(zoom_add):
        nonlocal ground_tiles
        global zoom
        zoom += zoom_add
        ground_tiles = get_tileset(pygame.image.load(f"{PATH}/assets/ground_tileset.png").convert_alpha(), zoom)
        for entity in updateable:
            entity.zoom(zoom)
        player.zoom(zoom)

    while running:
        elapsed_time = pygame.time.get_ticks() - start_time
        factor = min(elapsed_time / CYCLE_DURATION, 1.0)
        if factor >= 1.0:
             current_color = next_color
             next_color = next(COLORS)
             start_time = pygame.time.get_ticks()
             factor = 0.0

        light_color = inter_color(current_color, next_color, factor)
        light.fill(light_color)
        print(light_color)

        while len(enemies) < max_enemies:
            new_enemy = add_enemy(screen, updateable, enemies, world_size, tilemap, zoom)
            new_enemy.zoom(zoom)
        if music_delay > 0:
             music_delay -= dt / random.randint(1,2)
        if music_delay <= 0:
             music_delay = 120
             i = random.randint(0,1)
             song = pygame.mixer.Sound(f"{PATH}/assets/music/overworld_day_{i}.wav")
             song.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
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
                if event.key == pygame.K_RIGHT:
                     updateable.add(player.shoot(screen, pygame.Vector2(1,0), enemies, zoom))
                if event.key == pygame.K_LEFT:
                     updateable.add(player.shoot(screen, pygame.Vector2(-1,0), enemies, zoom))
                if event.key == pygame.K_UP:
                     updateable.add(player.shoot(screen, pygame.Vector2(0,-1), enemies, zoom))
                if event.key == pygame.K_DOWN:
                     updateable.add(player.shoot(screen, pygame.Vector2(0,1), enemies, zoom))
            
            if event.type == pygame.KEYUP:
                 if event.key == pygame.K_LSHIFT:
                      player.move_speed = 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.position.x > 0:
                player.moving = True
                player.move('left', colliders, dt)
        elif keys[pygame.K_d] and player.position.x < world_size - 1:
                player.moving = True
                player.move('right', colliders, dt)
        elif keys[pygame.K_w] and player.position.y > 0:
                player.moving = True
                player.move('up', colliders, dt)
        elif keys[pygame.K_s] and player.position.y < world_size - 1:
                player.moving = True
                player.move('down', colliders, dt)
        else:
             player.moving = False

        colliders = update_render(screen, player, world_size, ground_tiles, tilemap, tree_list, zoom, updateable, dt, light)
        dt = clock.tick(60) / 1000
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
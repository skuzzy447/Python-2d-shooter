import pygame
import random
from generate_world import generate
from constants import *
from settings import *
from player import Player, spawn_player
from enemy import Enemy, add_enemy

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
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

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

    hearts = get_tileset(pygame.image.load(f"{PATH}/assets/health_sprite_sheet.png").convert_alpha(), zoom, tile_width=160, tile_height=64)
    inventory_sprite = pygame.image.load(f"{PATH}/assets/inventory.png").convert_alpha()

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

        while len(enemies) < max_enemies and current_color == NIGHT_COLOR:
            new_enemy = add_enemy(screen, updateable, enemies, world_size, tilemap, zoom)
            new_enemy.zoom(zoom)
        if current_color == SUNSET_COLOR:
             for enemy in enemies:
                  enemy.kill()
        if music_delay > 0:
             music_delay -= dt / random.randint(1,2)
        if music_delay <= 0:
             music_delay = 120
             i = random.randint(0,8)
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
                     player.shoot(screen, pygame.Vector2(1,0), enemies, zoom, updateable)
                if event.key == pygame.K_LEFT:
                     player.shoot(screen, pygame.Vector2(-1,0), enemies, zoom, updateable)
                if event.key == pygame.K_UP:
                     player.shoot(screen, pygame.Vector2(0,-1), enemies, zoom, updateable)
                if event.key == pygame.K_DOWN:
                     player.shoot(screen, pygame.Vector2(0,1), enemies, zoom, updateable)
            
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
        #rendering and update code
        colliders = []
        screen.fill((44.7,45.9,10.6))
        for y in range(max(0, int(player.position.y - 32 // zoom)), min(world_size, int(player.position.y + 32 // zoom))):
            for x in range(max(0, int(player.position.x - 32 // zoom)), min(world_size, int(player.position.x + 32 // zoom))):
                screen_x = x * 32 * zoom - (player.position.x * 32 * zoom - 512) - 16 * zoom
                screen_y = y * 32 * zoom - (player.position.y * 32 * zoom - 512) - 16 * zoom
                screen.blit(ground_tiles[tilemap[y][x]], (screen_x, screen_y))
                if tilemap[y][x] >= 32:
                     colliders.append(pygame.Rect(screen_x, screen_y, 32 * zoom, 32 * zoom))
                for (tree_x, tree_y) in tree_list:
                    if tree_x == x and tree_y == y:
                        colliders.append(pygame.Rect(screen_x + 8 * zoom, screen_y, 16 * zoom, 32 * zoom))
                        screen.blit(ground_tiles[30], (screen_x, screen_y))
        player.update(colliders, dt)
        healthbar = hearts[int(player.health/10)]
        screen.blit(player.sprite, (512 - 16*zoom,512 - 16*zoom))
        for entity in updateable:
                entity.update(player, tilemap, dt, zoom, tree_list)
        for y in range(max(0, int(player.position.y - 32 // zoom)), min(world_size, int(player.position.y + 32 // zoom))):
            for x in range(max(0, int(player.position.x - 32 // zoom)), min(world_size, int(player.position.x + 32 // zoom))):
                screen_x = x * 32 * zoom - (player.position.x * 32 * zoom - 512) - 16 * zoom
                screen_y = (y - 1) * 32 * zoom - (player.position.y * 32 * zoom - 512 ) - 16 * zoom
                for (tree_x, tree_y) in tree_list:
                    if tree_x == x and tree_y == y:
                        screen.blit(ground_tiles[29], (screen_x, screen_y))
        screen.blit(light,(0,0))
        screen.blit(healthbar, (32,0))
        x = (screen.get_width() / 2) - (inventory_sprite.get_width() / 2)
        y = screen.get_height() - 64
        screen.blit(inventory_sprite, (x,y))
        pygame.display.flip()
        dt = clock.tick(60) / 1000
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
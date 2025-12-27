import pygame
import random
from datetime import datetime
from generate_world import generate
from constants import *
from settings import *
from player import Player, spawn_player
from enemy import Enemy, add_enemy
from chicken import Chicken, add_chicken
from coin import Coin
from arrow import Arrow
from house import House

def main(): 
    global zoom
    print("initializing")
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    game_font = pygame.font.Font(f"{PATH}/assets/pixelon.regular.ttf", 42)
    screen = pygame.display.set_mode((1024, 1024))
    clock = pygame.time.Clock()   
    dt = 0
    running = True
    paused = False
    show_colliders = False
    ground_tiles = get_tileset(pygame.image.load(f"{PATH}/assets/ground_tileset.png").convert_alpha(), zoom)
    treetop_png = pygame.image.load(f"{PATH}/assets/treetop.png").convert_alpha()
    treetop = pygame.transform.scale(treetop_png, (int(treetop_png.get_width() * zoom), int(treetop_png.get_height() * zoom)))
    tilemap, tree_list, shops = generate(world_size, screen, zoom)
    pygame.mouse.set_visible(False)

    updateable = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    passives = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    print("spawning player")
    player = spawn_player(screen, world_size, tilemap, tree_list, zoom)

    colliders = []

    spawn_delay = 0
    music_delay = 10

    light = pygame.Surface((1024, 1024),pygame.SRCALPHA)
    light.fill((10, 10, 20))
    current_color = next(COLORS)
    next_color = next(COLORS)
    elapsed_time = 0

    hearts = get_tileset(pygame.image.load(f"{PATH}/assets/health_sprite_sheet.png").convert_alpha(), 2, tile_width=160, tile_height=64)
    coin_icon = get_tileset(pygame.image.load(f"{PATH}/assets/coin_sprite_sheet.png").convert_alpha(), 4, tile_width=16, tile_height=16)
    coin_icon = coin_icon[0]
    inventory_sprite = pygame.image.load(f"{PATH}/assets/inventory.png").convert_alpha()
    menu = pygame.image.load(f"{PATH}/assets/menu.png").convert_alpha()
    menu_rect = menu.get_rect()
    menu_rect.center = screen.get_rect().center
    menu0, menu1, menu2 = (menu_rect.center[0], menu_rect.center[1] - 110), menu_rect.center, (menu_rect.center[0], menu_rect.center[1] + 110)
    menu_selection = menu0
    menu_cursor = pygame.image.load(f"{PATH}/assets/menu_cursor.png").convert_alpha()
    menu_cursor_rect = menu_cursor.get_rect()
    menu_cursor_rect.center = menu_selection
    
    night = False

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
        nonlocal treetop
        global zoom
        zoom += zoom_add
        ground_tiles = get_tileset(pygame.image.load(f"{PATH}/assets/ground_tileset.png").convert_alpha(), zoom)
        treetop = pygame.transform.scale(treetop_png, (int(treetop_png.get_width() * zoom), int(treetop_png.get_height() * zoom)))
        for entity in updateable:
            entity.zoom(zoom)
        for shop in shops:
            shop.zoom(zoom)
        player.zoom(zoom)

    while running:
        if not paused:
            elapsed_time += dt * 1000
            factor = min(elapsed_time / CYCLE_DURATION, 1.0)
            if factor >= 1.0:
                current_color = next_color
                next_color = next(COLORS)
                elapsed_time = 0
                factor = 0.0
            light_color = inter_color(current_color, next_color, factor)
            light.fill(light_color)
        
        night = False if current_color == DAY_COLOR else True
        if spawn_delay > 0:
            spawn_delay -= dt
        if spawn_delay <= 0:
            spawn_delay = 2
            if len(mobs) < max_mobs and night:
                if len(passives) > 0:
                    passives.sprites()[0].kill()
                new_enemy = add_enemy(screen, updateable, enemies, mobs, world_size, tilemap, tree_list, zoom)
                new_enemy.zoom(zoom)
            if len(mobs) < max_mobs//2 and not night:
                new_chicken = add_chicken(screen, updateable, passives, mobs, world_size, tilemap, tree_list, zoom)
                new_chicken.zoom(zoom)
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
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_F1:
                        date = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                        pygame.image.save(screen, f"{PATH}/screenshot_{date}.png")
                    if event.key == pygame.K_F2:
                        show_colliders = not show_colliders
                    if event.key == pygame.K_F3:
                        print(player.position)
                    if event.key == pygame.K_EQUALS:
                        if zoom < 2.5:
                            zoom_entities(0.5)
                    if event.key == pygame.K_MINUS:
                        if zoom > 1.0:
                            zoom_entities(-0.5)
                    if event.key == pygame.K_LSHIFT:
                        player.sprint()
                    if event.key == pygame.K_RIGHT:
                        player.shoot(screen, pygame.Vector2(1,0), mobs, zoom, updateable)
                    if event.key == pygame.K_LEFT:
                        player.shoot(screen, pygame.Vector2(-1,0), mobs, zoom, updateable)
                    if event.key == pygame.K_UP:
                        player.shoot(screen, pygame.Vector2(0,-1), mobs, zoom, updateable)
                    if event.key == pygame.K_DOWN:
                        player.shoot(screen, pygame.Vector2(0,1), mobs, zoom, updateable)
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    player.move_speed = 1
            if paused:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_selection == menu0:
                            menu_selection = menu1
                        elif menu_selection == menu1:
                            menu_selection = menu2
                        elif menu_selection == menu2:
                            menu_selection = menu0
                        menu_cursor_rect.center = menu_selection
                    if event.key == pygame.K_UP:
                        if menu_selection == menu0:
                            menu_selection = menu2
                        elif menu_selection == menu1:
                            menu_selection = menu0
                        elif menu_selection == menu2:
                            menu_selection = menu1
                        menu_cursor_rect.center = menu_selection
                    if event.key == pygame.K_RETURN:
                        if menu_selection == menu0:
                            paused = False
                        if menu_selection == menu1:
                            pass
                        if menu_selection == menu2:
                            running = False
                        
        if not paused:                  
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.position.x > 0:
                    player.moving = True
                    player.move('left', colliders, dt, zoom)
            elif keys[pygame.K_d] and player.position.x < world_size - 1:
                    player.moving = True
                    player.move('right', colliders, dt, zoom)
            elif keys[pygame.K_w] and player.position.y > 0:
                    player.moving = True
                    player.move('up', colliders, dt, zoom)
            elif keys[pygame.K_s] and player.position.y < world_size - 1:
                    player.moving = True
                    player.move('down', colliders, dt, zoom)
            else:
                player.moving = False
        #rendering and update code
        colliders = []
        screen.fill((44.7,45.9,10.6))
        for y in range(max(0, int(player.position.y - 19 // zoom)), min(world_size, int(player.position.y + 20 // zoom))):
            for x in range(max(0, int(player.position.x - 19 // zoom)), min(world_size, int(player.position.x + 20 // zoom))):
                screen_x = x * 32 * zoom - (player.position.x * 32 * zoom - 512) - 16 * zoom
                screen_y = y * 32 * zoom - (player.position.y * 32 * zoom - 512) - 16 * zoom
                screen.blit(ground_tiles[tilemap[y][x]], (screen_x, screen_y))
                for mob in passives:
                    colliders.append(mob.collider)
                for shop in shops:
                    colliders.append(shop.collider1)
                    colliders.append(shop.collider2)
                    colliders.append(shop.collider3)
                if tilemap[y][x] >= 32:
                     colliders.append(pygame.Rect(screen_x, screen_y, 32 * zoom, 32 * zoom))
                for (tree_x, tree_y) in tree_list:
                    if tree_x == x and tree_y == y:
                        colliders.append(pygame.Rect(screen_x + 8 * zoom, screen_y, 16 * zoom, 32 * zoom))
                        screen.blit(ground_tiles[30], (screen_x, screen_y))
        if not paused:
            player.update(colliders, dt)
            for entity in updateable:
                    if __name__ == "__main__":
                        if isinstance(entity, Enemy) or isinstance(entity, Chicken):
                            entity.update(player, tilemap, dt, zoom, tree_list, shops)
                        elif isinstance(entity, Coin):
                            entity.update(player, dt, zoom)
                        else:
                            entity.update(player, dt, zoom, tree_list, updateable)
            screen.blit(player.sprite, (512 - 16*zoom,512 - 16*zoom))
        for y in range(max(0, int(player.position.y - 32 // zoom)), min(world_size, int(player.position.y + 32 // zoom))):
            for x in range(max(0, int(player.position.x - 32 // zoom)), min(world_size, int(player.position.x + 32 // zoom))):
                screen_x = x * 32 * zoom - (player.position.x * 32 * zoom - 512) - 16 * zoom
                screen_y = (y - 1) * 32 * zoom - (player.position.y * 32 * zoom - 512 ) - 16 * zoom
                for (tree_x, tree_y) in tree_list:
                    if tree_x == x and tree_y == y:
                        screen.blit(treetop, (screen_x, screen_y))
        for shop in shops:
            shop.update(player, zoom)
        if show_colliders:
            for e in updateable:
                if not isinstance(e, Arrow):
                    if int(e.position.x) in range(int(player.position.x - 20), int(player.position.x + 20)) and int(e.position.y) in range(int(player.position.y - 20), int(player.position.y + 20)):
                        pygame.draw.rect(screen, (255,0,0), e.collider, 1)
            for collider in colliders:
                    pygame.draw.rect(screen, (0,255,0), collider, 1)
            for shop in shops:
                pygame.draw.rect(screen, (255,255,0), shop.entry, 1)
            pygame.draw.rect(screen, (0,0,255), player.collider, 1)
        healthbar = hearts[int(player.health/10)]
        screen.blit(light,(0,0))
        screen.blit(healthbar, (32,0))
        screen.blit(coin_icon, (32, 96))
        coin_counter = game_font.render(str(player.coins), False, (255, 255, 255))
        screen.blit(coin_counter, (96, 111))
        x = (screen.get_width() / 2) - (inventory_sprite.get_width() / 2)
        y = screen.get_height() - 64
        screen.blit(inventory_sprite, (x,y))
        if paused:
             screen.blit(menu, menu_rect)
             screen.blit(menu_cursor, menu_cursor_rect)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
import pygame

def update_render(screen, player, world_size, ground_tiles, tilemap, tree_list, zoom, updateable, dt):
        screen.fill((44.7,45.9,10.6))
        player.update(dt)
        for y in range(max(0, int(player.position.y - 32 // zoom)), min(world_size, int(player.position.y + 32 // zoom))):
            for x in range(max(0, int(player.position.x - 32 // zoom)), min(world_size, int(player.position.x + 32 // zoom))):
                screen_x = x * 32 * zoom - (player.position.x * 32 * zoom - 512) - 16 * zoom
                screen_y = y * 32 * zoom - (player.position.y * 32 * zoom - 512) - 16 * zoom
                screen.blit(ground_tiles[tilemap[y][x]], (screen_x, screen_y))
                for (tree_x, tree_y) in tree_list:
                    if tree_x == x and tree_y == y:
                        screen.blit(ground_tiles[30], (screen_x, screen_y))
        screen.blit(player.sprite, (512 - 16*zoom,512 - 16*zoom))
        for entity in updateable:
                entity.update(player.position, tilemap, dt, zoom, tree_list)
        for y in range(max(0, int(player.position.y - 32 // zoom)), min(world_size, int(player.position.y + 32 // zoom))):
            for x in range(max(0, int(player.position.x - 32 // zoom)), min(world_size, int(player.position.x + 32 // zoom))):
                screen_x = x * 32 * zoom - (player.position.x * 32 * zoom - 512) - 16 * zoom
                screen_y = (y - 1) * 32 * zoom - (player.position.y * 32 * zoom - 512 ) - 16 * zoom
                for (tree_x, tree_y) in tree_list:
                    if tree_x == x and tree_y == y:
                        screen.blit(ground_tiles[29], (screen_x, screen_y))
        pygame.display.flip()
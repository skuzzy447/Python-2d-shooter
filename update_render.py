import pygame

def update_render(screen, player, world_size, ground_tiles, tilemap, tree_list, zoom, updateable, dt):
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
        pygame.display.flip()
        return colliders
        
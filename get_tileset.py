import pygame
def get_tileset(image, zoom, tile_size=32):
    image = pygame.transform.scale(image, (int(image.get_width() * zoom), int(image.get_height() * zoom)))
    tile_size = int(tile_size * zoom)
    tiles = []
    for tile_y in range(0, image.get_height() // tile_size):
        for tile_x in range(0, image.get_width() // tile_size):
            tile = image.subsurface(tile_x * tile_size, tile_y * tile_size, tile_size, tile_size)
            tiles.append(tile)
    return tiles
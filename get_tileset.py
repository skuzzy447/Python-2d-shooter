import pygame
def get_tileset(image, zoom, tile_width=32, tile_height=32):
    image = pygame.transform.scale(image, (int(image.get_width() * zoom), int(image.get_height() * zoom)))
    tile_width = int(tile_width * zoom)
    tile_height = int(tile_height * zoom)
    tiles = []
    for tile_y in range(0, image.get_height() // tile_height):
        for tile_x in range(0, image.get_width() // tile_width):
            tile = image.subsurface(tile_x * tile_width, tile_y * tile_height, tile_width, tile_height)
            tiles.append(tile)
    return tiles
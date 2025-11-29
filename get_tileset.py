def get_tileset(image, tile_size=32):
    tiles = []
    for tile_y in range(0, image.get_height() // tile_size):
        for tile_x in range(0, image.get_width() // tile_size):
            tile = image.subsurface(tile_x * tile_size, tile_y * tile_size, tile_size, tile_size)
            tiles.append(tile)
    return tiles
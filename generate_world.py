import random
import json
import os

def generate(size):
    tilemap = []
    for y in range(0,size):
        tilemap.append([])
        for x in range(0,size):
            if y == 0:
                tilemap[y].append(random_tile())
            else:
                if x > 0:
                    if tilemap[y-1][x] == 1 or tilemap[y][x-1] == 1:
                        tilemap[y].append(random.randint(0,1))
                    elif tilemap[y-1][x] == 2 or tilemap[y][x-1] == 2:
                        if random.randint(0,1) == 1:
                            tilemap[y].append(2)
                        else:
                            tilemap[y].append(0)
                    else:
                        tilemap[y].append(random_tile())
                else:
                    if tilemap[y-1][x] == 1:
                        tilemap[y].append(random.randint(0,1))
                    elif tilemap[y-1][x] ==2:
                        if random.randint(0,1) == 1:
                            tilemap[y].append(2)
                        else:
                            tilemap[y].append(0)
                    else:
                        tilemap[y].append(random_tile())
    path = os.path.dirname(os.path.abspath(__file__))
    with open(f"{path}/tilemap.json", "w") as f:
        json.dump(tilemap, f)

def random_tile():
    tile = random.randint(0,40)
    if tile <= 38:
        tile = 0
    elif tile == 39:
        tile = 1
    elif tile == 40:
        tile = 2
    return tile

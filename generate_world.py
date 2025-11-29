import random
import json
import os

def remove_small_lakes(tilemap):
    height = len(tilemap)
    if height == 0:
        return tilemap
    width = len(tilemap[0])
    visited = [[False] * width for _ in range(height)]
    for y in range(len(tilemap)):
        for x in range(len(tilemap[y])):
            if tilemap[y][x] == 31 and not visited[y][x]:
                queue = [(x, y)]
                lake_tiles = []
                visited[y][x] = True
                while queue:
                    current_x, current_y = queue.pop(0)
                    lake_tiles.append((current_x, current_y))
                    visited[current_y][current_x] = True
                    neighbors = [(current_x + 1, current_y), (current_x - 1, current_y),
                                 (current_x, current_y + 1), (current_x, current_y - 1)]
                    for x, y in neighbors:
                        if 0 <= x < width and 0 <= y < height:
                            if tilemap[y][x] == 31 and not visited[y][x]:
                                visited[y][x] = True
                                queue.append((x, y))
                if len(lake_tiles) < 10:
                    for x, y in lake_tiles:
                        tilemap[y][x] = 0
    return tilemap

def build_boulders(tilemap):
    height = len(tilemap)
    if height == 0:
        return tilemap
    width = len(tilemap[0])
    visited = [[False] * width for _ in range(height)]
    for y in range(len(tilemap)):
        for x in range(len(tilemap[y])):
            if tilemap[y][x] == 59 and not visited[y][x]:
                boulder_tiles = []
                boulder_tiles.append((x, y))
                for x, y in boulder_tiles:
                    n = tilemap[y-1][x] if y > 0 else 0
                    s = tilemap[y+1][x] if y < height - 1 else 0
                    e = tilemap[y][x+1] if x < width - 1 else 0
                    w = tilemap[y][x-1] if x > 0 else 0
                    ne = tilemap[y-1][x+1] if y > 0 and x < width - 1 else 0
                    nw = tilemap[y-1][x-1] if y > 0 and x > 0 else 0
                    se = tilemap[y+1][x+1] if y < height - 1 and x < width - 1 else 0
                    sw = tilemap[y+1][x-1] if y < height - 1 and x > 0 else 0
                    if  n >= 32 and s >= 32 and  e >= 32 and  w >= 32 and  ne >= 32 and  nw >= 32 and  se >= 32 and  sw >= 32:
                        tilemap[y][x] = 41
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and  ne >= 32 and  nw >= 32 and  se >= 32 and not  sw >= 32:
                        tilemap[y][x] = 60
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and  ne >= 32 and  nw >= 32 and not  se >= 32 and  sw >= 32:
                        tilemap[y][x] = 52
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and  ne >= 32 and not  nw >= 32 and  se >= 32 and  sw >= 32:
                        tilemap[y][x] = 61
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and not  ne >= 32 and  nw >= 32 and  se >= 32 and  sw >= 32:
                        tilemap[y][x] = 63
                    if   n >= 32 and  s >= 32 and  e >= 32 and not  w >= 32 and  se >= 32:
                        tilemap[y][x] = 40
                    if   n >= 32 and  s >= 32 and not  e >= 32 and  w >= 32 and  sw >= 32:
                        tilemap[y][x] = 42
                    if   n >= 32 and not  s >= 32 and  e >= 32 and  w >= 32 and  ne >= 32 and  nw >= 32:
                        tilemap[y][x] = 49
                    if  not  n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and  se >= 32 and  sw >= 32:
                        tilemap[y][x] = 33
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and not  se >= 32 and not  sw >= 32:
                        tilemap[y][x] = 44
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and  ne >= 32 and not  nw >= 32 and not  se >= 32 and  sw >= 32:
                        tilemap[y][x] = 68
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and not  ne >= 32 and not  nw >= 32 and  se >= 32 and  sw >= 32:
                        tilemap[y][x] = 36
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and  ne >= 32 and not  nw >= 32 and  se >= 32 and not  sw >= 32:
                        tilemap[y][x] = 69
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and not  ne >= 32 and  nw >= 32 and  se >= 32 and not  sw >= 32:
                        tilemap[y][x] = 62
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and not  ne >= 32 and  nw >= 32 and not  se >= 32 and  sw >= 32:
                        tilemap[y][x] = 70
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and  ne >= 32 and not  nw >= 32 and not  se >= 32 and not  sw >= 32:
                        tilemap[y][x] = 65
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and not  ne >= 32 and  nw >= 32 and not  se >= 32 and not  sw >= 32:
                        tilemap[y][x] = 66
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and not  ne >= 32 and not  nw >= 32 and  se >= 32 and not  sw >= 32:
                        tilemap[y][x] = 64
                    if   n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and not  ne >= 32 and not  nw >= 32 and not  se >= 32 and  sw >= 32:
                        tilemap[y][x] = 67
                    if   n >= 32 and not  s >= 32 and  e >= 32 and not  w >= 32:
                        tilemap[y][x] = 48
                    if  not  n >= 32 and  s >= 32 and  e >= 32 and not  w >= 32 and  se >= 32:
                        tilemap[y][x] = 32
                    if   n >= 32 and not  s >= 32 and not  e >= 32 and  w >= 32:
                        tilemap[y][x] = 50
                    if  not  n >= 32 and  s >= 32 and not  e >= 32 and  w >= 32 and  sw >= 32:
                        tilemap[y][x] = 34
                    if  not  n >= 32 and not  s >= 32 and  e >= 32 and  w >= 32:
                        tilemap[y][x] = 57
                    if   n >= 32 and  s >= 32 and not  e >= 32 and not  w >= 32:
                        tilemap[y][x] = 43
                    if   n >= 32 and not  s >= 32 and not  e >= 32 and not  w >= 32:
                        tilemap[y][x] = 51
                    if  not  n >= 32 and  s >= 32 and not  e >= 32 and not  w >= 32:
                        tilemap[y][x] = 35
                    if  not  n >= 32 and not  s >= 32 and  e >= 32 and not  w >= 32:
                        tilemap[y][x] = 56
                    if  not  n >= 32 and not  s >= 32 and not  e >= 32 and  w >= 32:
                        tilemap[y][x] = 58
                    if  not  n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and not se >= 32 and not sw >= 32:
                        tilemap[y][x] = 38
                    if  not  n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and  se >= 32 and not sw >= 32:
                        tilemap[y][x] = 33
                    if  not  n >= 32 and  s >= 32 and  e >= 32 and  w >= 32 and not se >= 32 and sw >= 32:
                        tilemap[y][x] = 33
                    if   n >= 32 and not  s >= 32 and  e >= 32 and  w >= 32 and not ne >= 32 and not nw >= 32:
                        tilemap[y][x] = 54
                    if   n >= 32 and not  s >= 32 and  e >= 32 and  w >= 32 and not ne >= 32 and  nw >= 32:
                        tilemap[y][x] = 49
                    if   n >= 32 and not  s >= 32 and  e >= 32 and  w >= 32 and  ne >= 32 and not nw >= 32:
                        tilemap[y][x] = 49
                    if  not  n >= 32 and  s >= 32 and  e >= 32 and not  w >= 32 and not se >= 32:
                        tilemap[y][x] = 37
                    if   n >= 32 and  s >= 32 and  e >= 32 and not  w >= 32 and not se >= 32:
                        tilemap[y][x] = 45
                    if   n >= 32 and  s >= 32 and not  e >= 32 and  w >= 32 and not sw >= 32:
                        tilemap[y][x] = 47
                    if  not  n >= 32 and  s >= 32 and not  e >= 32 and  w >= 32 and not sw >= 32:
                        tilemap[y][x] = 39
    return tilemap
def generate(size):
    tilemap = []
    for y in range(0,size):
        tilemap.append([])
        for x in range(0,size):
            if y == 0:
                tilemap[y].append(random_tile())
            else:
                if x > 0:
                    if tilemap[y-1][x] == 31 or tilemap[y][x-1] == 31:
                        choice = random.randint(0,10)
                        if choice < 6:
                            tilemap[y].append(31)
                        else:
                            tilemap[y].append(random_tile())
                    elif tilemap[y-1][x] == 59 or tilemap[y][x-1] == 59:
                        tilemap[y].append(random.choice([0,59]))
                    else:
                        tilemap[y].append(random_tile())
                else:
                    if tilemap[y-1][x] == 31:
                        choice = random.randint(0,10)
                        if choice < 6:
                            tilemap[y].append(31)
                        else:
                            tilemap[y].append(random_tile())
                    elif tilemap[y-1][x] == 59:
                        tilemap[y].append(random.choice([0,59]))
                    else:
                        tilemap[y].append(random_tile())
    path = os.path.dirname(os.path.abspath(__file__))
    tilemap = remove_small_lakes(tilemap)
    tilemap = build_boulders(tilemap)
    with open(f"{path}/tilemap.json", "w") as f:
        json.dump(tilemap, f)

def random_tile():
    tile = random.randint(0,100)
    if tile <= 96:
        if random.randint(0,3) == 0:
            if random.randint(0,3) == 0:
                tile = random.randint(0,30)
            else:
                tile = random.randint(0,16)
        else:
            tile = 0
    elif tile == 97:
        tile = 31
    elif tile >= 98:
        tile = 59
    return tile

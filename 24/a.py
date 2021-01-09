from enum import Enum
from typing import NamedTuple

"""

e and w cancel each other out

se and nw cancel each other out

sw and ne cancel each other out

nw + sw = w

ne + se = e

nw + e = ne

ne + w = nw

sw + e = se

se + w = sw

"""

class Tile_Pos(NamedTuple):
    e: int
    w: int
    se: int
    ne: int
    sw: int
    nw: int

class Dir(Enum):
    e = 1,
    w = 2,
    se = 3,
    sw = 4,
    ne = 5,
    nw = 6,

def a(lines):
    tiles = {}  # tile: is black facing up
    for line in lines:
        tile = reduce_tile_pos(dir_dict_to_tile_pos(parse_line(line)))
        try:
            tiles[tile] = not tiles[tile]
        except KeyError:
            tiles[tile] = True
    return sum(tiles.values())

def parse_line(line):
    dir_dict = dict.fromkeys(Dir, 0)
    i = 0
    while i < len(line):
        if line[i] == Dir.e.name or line[i] == Dir.w.name:
            dir = Dir[line[i]]
        else:
            dir = Dir[line[i:i+2]]
            i += 1
        dir_dict[dir] += 1
        i += 1
    return dir_dict

def reduce_tile_pos(tile_pos):
    change = False
    e, w, se, ne, sw, nw = tile_pos
    # nw + sw = w
    if nw and sw:
        nw -= 1
        sw -= 1
        w += 1
        change = True
    # ne + se = e
    if ne and se:
        ne -= 1
        se -= 1
        e += 1
        change = True
    # nw + e = ne
    if nw and e:
        nw -= 1
        e -= 1
        ne += 1
        change = True
    # ne + w = nw
    if ne and w:
        ne -= 1
        w -= 1
        nw += 1
        change = True
    # sw + e = se
    if sw and e:
        sw -= 1
        e -= 1
        se += 1
        change = True
    # se + w = sw
    if se and w:
        se -= 1
        w -= 1
        sw += 1
        change = True
    # e and w cancel each other out
    if e and w:
        e -= 1
        w -= 1
        change = True
    # se and nw cancel each other out
    if se and nw:
        se -= 1
        nw -= 1
        change = True
    # sw and ne cancel each other out
    if sw and ne:
        sw -= 1
        ne -= 1
        change = True
    
    new_tile_pos = Tile_Pos(e, w, se, ne, sw, nw)
    if change:
        return reduce_tile_pos(new_tile_pos)
    return new_tile_pos

def dir_dict_to_tile_pos(dir_dict):
    return Tile_Pos(dir_dict[Dir.e], dir_dict[Dir.w], dir_dict[Dir.se], dir_dict[Dir.ne], dir_dict[Dir.sw], dir_dict[Dir.nw])

def b(lines):
    tile_pos_states = {}  # tile: is black facing up
    for line in lines:
        tile_pos = reduce_tile_pos(dir_dict_to_tile_pos(parse_line(line)))
        try:
            tile_pos_states[tile_pos] = not tile_pos_states[tile_pos]
        except KeyError:
            tile_pos_states[tile_pos] = True
    
    tile_pos_neighbours = {}
    def est_neighbours(tile_pos):
        new_tile_poses = []
        tile_pos_neighbours[tile_pos] = []
        tile_pos_l = list(tile_pos)
        for i in range(len(Dir)):
            tile_pos_cp_l = tile_pos_l[:]
            tile_pos_cp_l[i] += 1
            tile_pos_cp = reduce_tile_pos(tile_pos_cp_l)
            tile_pos_neighbours[tile_pos].append(tile_pos_cp)
            if tile_pos_cp not in tile_pos_states:
                new_tile_poses.append(tile_pos_cp)
        return new_tile_poses

    # establish existing tiles' neighbours
    # "outer" ring of tiles will always be white face up
    new_tile_poses = set()
    for tile_pos in tile_pos_states:
        new_tile_poses.update(est_neighbours(tile_pos))
    for tile_pos in new_tile_poses:
        tile_pos_states[tile_pos] = False
    
    new_tile_poses.clear()
    changes = []
    
    def get_tile_pos_state(tile_pos):
        try:
            return tile_pos_states[tile_pos]
        except KeyError:
            return False

    for _ in range(100):
        for tile_pos in tile_pos_states:
            # get neighbours
            try:
                adj_tile_poses = tile_pos_neighbours[tile_pos]
            except KeyError:
                new_tile_poses.update(est_neighbours(tile_pos))
                adj_tile_poses = tile_pos_neighbours[tile_pos]
            # calc num adj black tiles and determine if flip needed
            n_adj_black_tiles = sum(1 for adj_tile_pos in adj_tile_poses if get_tile_pos_state(adj_tile_pos))
            if tile_pos_states[tile_pos] and (n_adj_black_tiles == 0 or n_adj_black_tiles > 2) or \
               not tile_pos_states[tile_pos] and n_adj_black_tiles == 2:
                changes.append(tile_pos)
        # apply tile flips
        for tile_pos in changes:
            tile_pos_states[tile_pos] = not tile_pos_states[tile_pos]
        # expand tile area
        for tile_pos in new_tile_poses:
            tile_pos_states[tile_pos] = False
        # don't need to perform check on newly expanded area for this round
        # since previous newly expanded area was all white face up anyways
        new_tile_poses.clear()
        changes.clear()
    return sum(tile_pos_states.values())

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))

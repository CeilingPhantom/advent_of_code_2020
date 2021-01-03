from enum import Enum
from itertools import product

class Dir(Enum):
    Right = 0,
    Top = 1,
    Left = 2,
    Bot = 3

class Match:
    def __init__(self, id1, edge1, id2, edge2, is1reverse):
        self.id1 = id1
        self.edge1 = edge1
        self.id2 = id2
        self.edge2 = edge2
        self.is1reverse = is1reverse
    
    def __str__(self):
        return f"{self.id1}: {self.edge1} {self.is1reverse}, {self.id2} {self.edge2}"

class Tile:
    size = 10
    state_combinations = list(product([False, True], [False, True], [0, 0.5, 1, 1.5]))

    def __init__(self, id, right, top, left, bot):
        self.id = id
        self.dirs = {}
        self.dirs[Dir.Right] = right
        self.dirs[Dir.Top] = top
        self.dirs[Dir.Left] = left
        self.dirs[Dir.Bot] = bot

        self.edge_matches = []
    
    @classmethod
    def from_lines(cls, lines):
        i = 0
        id = int(lines[i].split()[1][:-1])
        i += 1
        top = list(lines[i])
        left = [lines[i][0]]
        right = [lines[i][-1]]
        for _ in range(9):
            i += 1
            left.append(lines[i][0])
            right.append(lines[i][-1])
        bot = list(lines[i])
        return cls(id, right, top, left, bot)

    # check if an edge (reversed) is the same as an edge of another tile
    def edges_match(self, other):
        for self_dir in Dir:
            rvs = self.dirs[self_dir][:]
            rvs.reverse()
            for other_dir in Dir:
                if self.dirs[self_dir] == other.dirs[other_dir]:
                    self.edge_matches.append(Match(self.id, self_dir, other.id, other_dir, False))
                    other.edge_matches.append(Match(other.id, other_dir, self.id, self_dir, False))
                elif rvs == other.dirs[other_dir]:
                    self.edge_matches.append(Match(self.id, self_dir, other.id, other_dir, True))
                    other.edge_matches.append(Match(other.id, other_dir, self.id, self_dir, True))

def a(lines):
    tiles = {}
    i = 0
    while i < len(lines):
        tile = Tile.from_lines(lines[i:i+Tile.size+1])
        tiles[tile.id] = tile
        i += Tile.size + 2

    tile_ids = list(tiles.keys())
    for i in range(len(tile_ids)):
        for j in range(i+1, len(tile_ids)):
            tiles[tile_ids[i]].edges_match(tiles[tile_ids[j]])

    r = 1
    for tile in tiles.values():
        if len(tile.edge_matches) == 2:
            r *= tile.id
            print(tile.id, [str(match) for match in tile.edge_matches])
    return r

def b(lines):
    return

"""
Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(a(lines))

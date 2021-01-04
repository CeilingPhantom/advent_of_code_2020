from enum import Enum
from itertools import product

class Dir(Enum):
    Right = 0,
    Top = 1,
    Left = 2,
    Bot = 3

class Tile:
    size = 10
    state_combinations = list(product([False, True], [False, True], [0, 0.5, 1, 1.5]))

    def __init__(self, id, right, top, left, bot, flipped_x=False, flipped_y=False, rotation=0):
        self.id = id
        self.dirs = {}
        self.dirs[Dir.Right] = right
        self.dirs[Dir.Top] = top
        self.dirs[Dir.Left] = left
        self.dirs[Dir.Bot] = bot
        self.flipped_x = flipped_x
        self.flipped_y = flipped_y
        self.rotation = rotation

        self.cache = {}

        # { (self state): { other id: { (other state): self edge that matches opposite edge in other [Dir.Right|Dir.Top|Dir.Left|Dir.Bot] } } }
        # so ... [Dir.Right] would mean self right edge and other left edge match
        self.edge_matches = {}
        self.matches_res = None
    
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

    def get_state(self):
        return (self.flipped_x, self.flipped_y, self.rotation)
    
    def set_state(self, state):
        flipped_x, flipped_y, rotation = state
        if state in self.cache:
            self.flipped_x = flipped_x
            self.flipped_y = flipped_y
            self.rotation = rotation
            self.dirs[Dir.Right] = self.cache[state][Dir.Right]
            self.dirs[Dir.Top] = self.cache[state][Dir.Top]
            self.dirs[Dir.Left] = self.cache[state][Dir.Left]
            self.dirs[Dir.Bot] = self.cache[state][Dir.Bot]
        else:
            if self.flipped_x != flipped_x:
                self.__flip_x()
            if self.flipped_y != flipped_y:
                self.__flip_y()
            self.__rotate(rotation - self.rotation)
            self.cache[state] = {}
            self.cache[state][Dir.Right] = self.dirs[Dir.Right]
            self.cache[state][Dir.Top] = self.dirs[Dir.Top]
            self.cache[state][Dir.Left] = self.dirs[Dir.Left]
            self.cache[state][Dir.Bot] = self.dirs[Dir.Bot]

    # flip along x axis
    def __flip_x(self):
        self.flipped_x = not self.flipped_x
        self.dirs[Dir.Top], self.dirs[Dir.Bot] = self.dirs[Dir.Bot], self.dirs[Dir.Top]
        self.dirs[Dir.Left].reverse()
        self.dirs[Dir.Right].reverse()
    
    # flip along y axis
    def __flip_y(self):
        self.flipped_y = not self.flipped_y
        self.dirs[Dir.Left], self.dirs[Dir.Right] = self.dirs[Dir.Right], self.dirs[Dir.Left]
        self.dirs[Dir.Top].reverse()
        self.dirs[Dir.Bot].reverse()
    
    def __rotate_half_radian(self):
        self.rotation += 0.5
        self.rotation %= 2
        tmp_top = self.dirs[Dir.Top]
        tmp_left = self.dirs[Dir.Left]
        tmp_right = self.dirs[Dir.Right]
        tmp_bot = self.dirs[Dir.Bot]
        self.dirs[Dir.Top] = tmp_right
        self.dirs[Dir.Left] = tmp_top
        self.dirs[Dir.Right] = tmp_bot
        self.dirs[Dir.Bot] = tmp_left

    def __rotate(self, radians):
        radians %= 2
        for _ in range(int(radians*2)):
            self.__rotate_half_radian()

    def edges_match(self, other):
        self_state = self.get_state()
        other_state = other.get_state()
        if self_state not in self.edge_matches:
            self.edge_matches[self_state] = {}
        if other.id not in self.edge_matches[self_state]:
            self.edge_matches[self_state][other.id] = {}
        if other_state not in self.edge_matches[self_state][other.id]:
            self.edge_matches[self_state][other.id][other_state] = []
        # top touches bot
        # left touches right
        if self.dirs[Dir.Top] == other.dirs[Dir.Bot]:
            self.edge_matches[self_state][other.id][other_state].append(Dir.Top)
        if self.dirs[Dir.Bot] == other.dirs[Dir.Top]:
            self.edge_matches[self_state][other.id][other_state].append(Dir.Bot)
        if self.dirs[Dir.Right] == other.dirs[Dir.Left]:
            self.edge_matches[self_state][other.id][other_state].append(Dir.Right)
        if self.dirs[Dir.Left] == other.dirs[Dir.Right]:
            self.edge_matches[self_state][other.id][other_state].append(Dir.Left)
        
        # del other state key if no matches
        if not self.edge_matches[self_state][other.id][other_state]:
            del self.edge_matches[self_state][other.id][other_state]
    
    def get_matches(self):
        if not self.matches_res:
            count = 0
            matches = []
            for self_state, other_matches in self.edge_matches.items():
                for other_id, other_states in other_matches.items():
                    for other_state, matching_edges in other_states.items():
                        count += len(matching_edges)
                        matches.append((self.id, self_state, other_id, other_state, matching_edges))
            self.matches_res = (count, matches)
        return self.matches_res

    def narrow_matches(self, *valid_matches):
        if not self.matches_res:
            return
        for match in valid_matches:
            x_id, x_state, y_id, y_state, x_edges = match
            if x_id == self.id:
                pass

    def __str__(self):
        return f"id: {self.id}; r: {self.dirs[Dir.Right]}; t: {self.dirs[Dir.Top]}; l: {self.dirs[Dir.Left]}; b: {self.dirs[Dir.Bot]}"

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
            get_matches(tiles[tile_ids[i]], tiles[tile_ids[j]])
    
    sorted_tiles = list(tiles.values())
    sorted_tiles.sort(key=lambda tile: tile.get_matches()[0])
    for tile in sorted_tiles:
        count, matches = tile.get_matches()
        print(tile.id, count, matches)

def get_matches(x, y):
    for x_state in Tile.state_combinations:
        x.set_state(x_state)
        for y_state in Tile.state_combinations:
            y.set_state(y_state)
            x.edges_match(y)
            y.edges_match(x)

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

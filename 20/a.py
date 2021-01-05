from enum import Enum

"""
tile borders

top: -->

bot: -->

left: |
      V

right: |
       V

 -->
|   |
V   V
 -->


match orientation rules
assuming 'this' tile is correctly orientated

bool for right, left refers to reversed?
bool for top, bot refers to reversed?

for all dirs,
dirA boolA <> dirB boolB    =>  dirA not boolA <> dirB not boolB

flipX == 1r, flipY
flipY == 1r, flipX
flipX, flipY == (1r + flipY) + flipY == 1r

right, False == 1r, left, True
right, True  == 1r, left, False

top, False   == 1r, bot, True
top, True    == 1r, bot, False

# match                             # equiv to

try to get: right, False <> left, False

right, False <> left, False     =>  nothing
right, False <> left, True      =>  other flipX

right, False <> right, False    =>  other flipY
right, False <> right, True     =>  right, False <1r> left, False   =>  other 1r

right, False <> top, False      =>  right, False <r/2> left, True   =>  other r/2, flipX
right, False <> top, True       =>  right, False <r/2> left, False  =>  other r/2

right, False <> bot, False      =>  right, False <3r/2> left, False =>  other 3r/2
right, False <> bot, True       =>  right, False <3r/2> left, False =>  other 3r/2, flipX


try to get: right, False <> left, False

left, False <> right, False     =>  nothing
left, False <> right, True      =>  other flipX

left, False <> left, False      =>  other flipY
left, False <> left, True       =>  left, False <1r> right, False   =>  other 1r

left, False <> bot, False       =>  left, False <r/2> right, True   =>  other r/2, flipX
left, False <> bot, True        =>  left, False <r/2> right, False  =>  other r/2

left, False <> top, False       =>  left, False <3r/2> right, False =>  other 3r/2
left, False <> top, True        =>  left, False <3r/2> right, False =>  other 3r/2, flipX


try to get: top, False <> bot, False

top, False <> bot, False        =>  nothing
top, False <> bot, True         =>  other flipY

top, False <> top, False        =>  other flipX
top, False <> top, True         =>  other 1r

top, False <> left, False       =>  other r/2
top, False <> left, True        =>  other r/2, flipY

top, False <> right, False      =>  other 3r/2, flipY
top, False <> right, True       =>  other 3r/2


try to get: bot, False <> top, False

bot, False <> top, False        => nothing
bot, False <> top, True         => other flipY

bot, False <> bot, False        => other flipX
bot, False <> bot, True         => other 1r

bot, False <> right, False      =>  other r/2
bot, False <> right, True       =>  other r/2, flipY

bot, False <> left, False       =>  other 3r/2, flipY
bot, False <> left, True        =>  other 3r/2

"""

class Dir(Enum):
    Right = 0,
    Top = 1,
    Left = 2,
    Bot = 3

class Match:
    def __init__(self, id1, edge1, id2, edge2, is_reverse):
        self.id1 = id1
        self.edge1 = edge1
        self.id2 = id2
        self.edge2 = edge2
        self.is_reverse = is_reverse

    def __str__(self):
        return f"{self.id1}: {self.edge1}, {self.id2}: {self.edge2}, {self.is_reverse}"

class Tile:
    size = 10

    orientation_matches = {
        # matching dirA <> other dir into dirA <> opposite dir, False
        # (rotation in radians, flipX, flipY)

        # dir.right <> other dir into dir.right <> dir.left, False
        (Dir.Right, Dir.Right, False):  (0, False, True),
        (Dir.Right, Dir.Right, True):   (1, False, False),
        (Dir.Right, Dir.Top, False):    (0.5, True, False),
        (Dir.Right, Dir.Top, True):     (0.5, False, False),
        (Dir.Right, Dir.Left, False):   (0, False, False),
        (Dir.Right, Dir.Left, True):    (0, True, False),
        (Dir.Right, Dir.Bot, False):    (1.5, False, False),
        (Dir.Right, Dir.Bot, True):     (1.5, True, False),
        
        # dir.left <> other dir into dir.left <> dir.right, False
        (Dir.Left, Dir.Right, False):   (0, False, False),
        (Dir.Left, Dir.Right, True):    (0, True, False),
        (Dir.Left, Dir.Top, False):     (1.5, False, False),
        (Dir.Left, Dir.Top, True):      (1.5, True, False),
        (Dir.Left, Dir.Left, False):    (0, False, True),
        (Dir.Left, Dir.Left, True):     (1, False, False),
        (Dir.Left, Dir.Bot, False):     (0.5, True, False),
        (Dir.Left, Dir.Bot, True):      (0.5, False, False),

        # dir.top <> other dir into dir.top <> dir.bot, False
        (Dir.Top, Dir.Right, False):    (1.5, False, True),
        (Dir.Top, Dir.Right, True):     (1.5, False, False),
        (Dir.Top, Dir.Top, False):      (0, True, False),
        (Dir.Top, Dir.Top, True):       (1, False, False),
        (Dir.Top, Dir.Left, False):     (0.5, False, False),
        (Dir.Top, Dir.Left, True):      (0.5, False, True),
        (Dir.Top, Dir.Bot, False):      (0, False, False),
        (Dir.Top, Dir.Bot, True):       (0, False, True),

        # dir.bot <> other dir into dir.bot <> dir.top, False
        (Dir.Bot, Dir.Right, False):    (0.5, False, False),
        (Dir.Bot, Dir.Right, True):     (0.5, False, True),
        (Dir.Bot, Dir.Top, False):      (0, False, False),
        (Dir.Bot, Dir.Top, True):       (0, False, True),
        (Dir.Bot, Dir.Left, False):     (1.5, False, True),
        (Dir.Bot, Dir.Left, True):      (1.5, False, False),
        (Dir.Bot, Dir.Bot, False):      (0, True, False),
        (Dir.Bot, Dir.Bot, True):       (1, False, False),
    }

    def __init__(self, id, data, right, top, left, bot):
        self.id = id
        self.borders = {}
        self.borders[Dir.Right] = right
        self.borders[Dir.Top] = top
        self.borders[Dir.Left] = left
        self.borders[Dir.Bot] = bot

        self.edge_matches = []

        self.rotation = 0
        self.flipped_x = False
        self.flipped_y = False

        self.adj_tiles = dict.fromkeys(Dir)

        self.data = [list(line) for line in data]
        self.data_updated = True
    
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
        return cls(id, lines[1:], right, top, left, bot)

    # create Match if an edge is the same as an edge of another tile (not reversed or reversed)
    # and set adjacent tiles accordingly
    def edges_match(self, other):
        # clear old match
        self.edge_matches = [match for match in self.edge_matches if match.id2 != other.id]
        other.edge_matches = [match for match in other.edge_matches if match.id2 != self.id]
        for self_dir in Dir:
            # clear old matching adjacent tile
            if self.adj_tiles[self_dir] == other.id:
                self.adj_tiles[self_dir] = None
            rvs = self.borders[self_dir][:]
            rvs.reverse()
            for other_dir in Dir:
                # clear old matching adjacent tile
                if other.adj_tiles[other_dir] == self.id:
                    other.adj_tiles[other_dir] = None
                if self.borders[self_dir] == other.borders[other_dir]:
                    self.edge_matches.append(Match(self.id, self_dir, other.id, other_dir, False))
                    self.adj_tiles[self_dir] = other.id
                    other.edge_matches.append(Match(other.id, other_dir, self.id, self_dir, False))
                    other.adj_tiles[other_dir] = self.id
                    return
                elif rvs == other.borders[other_dir]:
                    self.edge_matches.append(Match(self.id, self_dir, other.id, other_dir, True))
                    self.adj_tiles[self_dir] = other.id
                    other.edge_matches.append(Match(other.id, other_dir, self.id, self_dir, True))
                    other.adj_tiles[other_dir] = self.id
                    return
    
    def get_orientation(self):
        return (self.rotation, self.flipped_x, self.flipped_y)

    # important: rotation is done before flipping
    def apply_orientation(self, orientation):
        rotation, flipped_x, flipped_y = orientation
        if rotation:
            self.data_updated = False
            self.__rotate(rotation)
        if self.flipped_x != flipped_x:
            self.data_updated = False
            self.__flip_x()
        if self.flipped_y != flipped_y:
            self.data_updated = False
            self.__flip_y()

    def __rotate_half_radian(self):
        self.rotation += 0.5
        self.rotation %= 2
        tmp_top = self.borders[Dir.Top]
        tmp_left = self.borders[Dir.Left]
        tmp_right = self.borders[Dir.Right]
        tmp_bot = self.borders[Dir.Bot]
        self.borders[Dir.Top] = tmp_right
        self.borders[Dir.Left] = tmp_top
        self.borders[Dir.Left].reverse()
        self.borders[Dir.Right] = tmp_bot
        self.borders[Dir.Right].reverse()
        self.borders[Dir.Bot] = tmp_left

        tmp_top = self.adj_tiles[Dir.Top]
        tmp_left = self.adj_tiles[Dir.Left]
        tmp_right = self.adj_tiles[Dir.Right]
        tmp_bot = self.adj_tiles[Dir.Bot]
        self.adj_tiles[Dir.Top] = tmp_right
        self.adj_tiles[Dir.Left] = tmp_top
        self.adj_tiles[Dir.Right] = tmp_bot
        self.adj_tiles[Dir.Bot] = tmp_left

    def __rotate(self, radians):
        radians %= 2
        for _ in range(int(radians*2)):
            self.__rotate_half_radian()

    # flip along x axis
    def __flip_x(self):
        self.flipped_x = not self.flipped_x
        self.borders[Dir.Top], self.borders[Dir.Bot] = self.borders[Dir.Bot], self.borders[Dir.Top]
        self.borders[Dir.Left].reverse()
        self.borders[Dir.Right].reverse()
        self.adj_tiles[Dir.Top], self.adj_tiles[Dir.Bot] = self.adj_tiles[Dir.Bot], self.adj_tiles[Dir.Top]
    
    # flip along y axis
    def __flip_y(self):
        self.flipped_y = not self.flipped_y
        self.borders[Dir.Left], self.borders[Dir.Right] = self.borders[Dir.Right], self.borders[Dir.Left]
        self.borders[Dir.Top].reverse()
        self.borders[Dir.Bot].reverse()
        self.adj_tiles[Dir.Left], self.adj_tiles[Dir.Right] = self.adj_tiles[Dir.Right], self.adj_tiles[Dir.Left]
    
    @staticmethod
    def determine_orientation_to_match(match):
        return Tile.orientation_matches[(match.edge1, match.edge2, match.is_reverse)]

    def update_data(self):
        if not self.data_updated:
            self.__rotate_data()
            if self.flipped_x:
                self.__flip_data_x()
            if self.flipped_y:
                self.__flip_data_y()

    def __rotate_data(self):
        for _ in range(int(self.rotation*2)):
            self.__rotate_data_half_radian()
     
    def __rotate_data_half_radian(self):
        new_data = [[None]*Tile.size for _ in range(Tile.size)]
        for i in range(Tile.size):
            for j in range(Tile.size):
                new_data[Tile.size-j-1][i] = self.data[i][j]
        self.data = new_data
    
    def __flip_data_x(self):
        for i in range(Tile.size):
            for j in range(int(Tile.size/2)):
                self.data[j][i], self.data[Tile.size-j-1][i] = self.data[Tile.size-j-1][i], self.data[j][i]
    
    def __flip_data_y(self):
        for i in range(Tile.size):
            for j in range(int(Tile.size/2)):
                self.data[i][j], self.data[i][Tile.size-j-1] = self.data[i][Tile.size-j-1], self.data[i][j]

class Monster:
    def __init__(self):
        self.monster = [
            list("                  # "),
            list("#    ##    ##    ###"),
            list(" #  #  #  #  #  #   "),
        ]
        self.width = len(self.monster[0])
        self.height = len(self.monster)

    def rotate(self, radians):
        radians %= 2
        for _ in range(int(radians*2)):
            self.__rotate_half_radian()
        return self
    
    def __rotate_half_radian(self):
        new_monster = [[None]*self.height for _ in range(self.width)]
        for i in range(self.height):
            for j in range(self.width):
                new_monster[self.width-j-1][i] = self.monster[i][j]
        self.monster = new_monster
        self.width = len(self.monster[0])
        self.height = len(self.monster)
    
    def flip_x(self):
        width = len(self.monster[0])
        height = len(self.monster)
        for i in range(width):
            for j in range(int(height/2)):
                self.monster[j][i], self.monster[height-j-1][i] = self.monster[height-j-1][i], self.monster[j][i]
        return self
    
    def flip_y(self):
        for i in range(self.height):
            for j in range(int(self.width/2)):
                self.monster[i][j], self.monster[i][self.width-j-1] = self.monster[i][self.width-j-1], self.monster[i][j]
        return self
    
    # snippet must have same dimensions as monster
    def in_snippet(self, snippet):
        for i in range(self.height):
            for j in range(self.width):
                if self.monster[i][j] != " " and snippet[i][j] != self.monster[i][j] or snippet[i][j] == "O":
                    return False
        return True

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

    # get any corner tile
    corner = None
    for tile in tiles.values():
        n_matches = len(tile.edge_matches)
        if n_matches == 2 and not corner:
            corner = tile
            break

    top_left = None
    seen = set()
    next_tiles = [corner]
    while next_tiles:
        tile = next_tiles.pop(0)
        if tile.id not in seen:
            seen.add(tile.id)
            # get top left tile
            if tile.adj_tiles[Dir.Bot] and tile.adj_tiles[Dir.Right] and not tile.adj_tiles[Dir.Top] and not tile.adj_tiles[Dir.Left]:
                top_left = tile.id
            for match in tile.edge_matches:
                if match.id2 not in seen and len([1 for t in next_tiles if t.id == match.id2]) == 0:
                    # rematch pair of tile and next_tile since tile has changed orientation
                    next_tile = tiles[match.id2]
                    next_tile.edges_match(tile)
                    [match] = [m for m in tile.edge_matches if m.id2 == next_tile.id]
                    next_tile.apply_orientation(Tile.determine_orientation_to_match(match))
                    next_tiles.append(next_tile)

    # organise tiles together
    img_tiles_data = []
    next_row_leftmost = top_left
    while next_row_leftmost:
        row = []
        img_tiles_data.append(row)
        next_right = next_row_leftmost
        next_row_leftmost = tiles[next_row_leftmost].adj_tiles[Dir.Bot]
        while next_right:
            tiles[next_right].update_data()
            row.append(tiles[next_right].data)
            next_right = tiles[next_right].adj_tiles[Dir.Right]
    
    # trim tile borders and stitch tiles together into an img
    img = []
    for i in range(len(img_tiles_data)):
        rows = [[] for _ in range(Tile.size - 2)]
        for j in range(len(img_tiles_data[i])):
            tile_data = img_tiles_data[i][j][1:-1]
            # remove side borders
            for k in range(len(tile_data)):
                tile_data[k].pop(0)
                tile_data[k].pop(-1)
            # add to rows list
            for k in range(len(rows)):
                rows[k] += tile_data[k]
        for row in rows:
            img.append(row)

    # reorientate monster instead of img
    monster_orientations = []
    # 4 rotations (3 + current)
    for i in range(4):
        r = i*0.5
        m = Monster().rotate(r)
        m_flip_x = Monster().flip_x().rotate(r)
        m_flip_y = Monster().flip_y().rotate(r)
        monster_orientations += [m, m_flip_x, m_flip_y]

    n_monsters = 0
    for m in monster_orientations:
        # create snippet
        for i in range(len(img)-m.height):
            for j in range(len(img[i])-m.width):
                snippet = []
                for k in range(m.height):
                    snippet.append(img[i+k][j:j+m.width])
                if m.in_snippet(snippet):
                    n_monsters += 1
                    # replace '#' with 'O' in img
                    for k in range(m.height):
                        for l in range(m.width):
                            if m.monster[k][l] == "#":
                                img[i+k][j+l] = "O"
        if n_monsters:
            break
    
    # count number of '#'; '#'s taken by monsters have become 'O's
    img_hash_count = 0
    for row in img:
        for c in row:
            img_hash_count += c == "#"
    
    return img_hash_count

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))

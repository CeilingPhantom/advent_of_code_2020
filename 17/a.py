from itertools import product

class Grid3:
    # frames are reflective, i.e. frame at z=1 == frame at z=-1
    # so only have to store n frames rather than 2n-1 frames
    frames = {}  # z -> y -> x
    updates = []

    max_z = 0

    min_y = 0
    max_y = 0

    min_x = 0
    max_x = 0

    def __init__(self, lines):
        self.max_z = 0
        self.max_y = len(lines)
        self.max_x = len(lines[0])
        self.frames[0] = {}
        for i in range(len(lines)):
            self.frames[0][i] = {}
            for j in range(len(lines[i])):
                self.frames[0][i][j] = False if lines[i][j] == "." else True
    
    def get(self, x, y, z):
        try:
            return self.frames[abs(z)][y][x]
        except KeyError:
            return False
    
    def tentative_update(self, x, y, z):
        self.updates.append((x, y, abs(z)))

    def push_updates(self):
        for x, y, z in self.updates:
            # lazy node init
            if z not in self.frames:
                self.frames[z] = {}
            if y not in self.frames[z]:
                self.frames[z][y] = {}
            if x not in self.frames[z][y]:
                self.frames[z][y][x] = True
            else:
                self.frames[z][y][x] = not self.frames[z][y][x]
        self.updates.clear()

    def update(self):
        self.__expand_frames()
        for z in range(self.max_z + 1):
            for y in range(self.min_y, self.max_y + 1):
                for x in range(self.min_x, self.max_x + 1):
                    self.__update(x, y, z)
        self.push_updates()

    def __update(self, x, y, z):
        n_active = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                for k in range(z - 1, z + 2):
                    if not (i == x and j == y and k == z) and self.get(i, j, k):
                        n_active += 1
        if self.get(x, y, z) and n_active not in range(2, 4):
            # deactivate
            self.tentative_update(x, y, z)
        elif not self.get(x, y, z) and n_active == 3:
            # activate
            self.tentative_update(x, y, z)

    def __expand_frames(self):
        # updating min max z y x
        expand_max_z = False
        if self.max_z in self.frames:
            for y in self.frames[self.max_z]:
                for x in self.frames[self.max_z][y]:
                    if self.get(x, y, self.max_z):
                        # active node found in highest z frame, need to expand out by 1 z
                        expand_max_z = True
                        self.max_z += 1
                        break
                if expand_max_z:
                    break
        expand_min_y = expand_max_y = False
        for z in self.frames:
            if not expand_min_y and self.min_y in self.frames[z]:
                for x in self.frames[z][self.min_y]:
                    if self.get(x, self.min_y, z):
                        expand_min_y = True
                        self.min_y -= 1
            if not expand_max_y and self.max_y in self.frames[z]:
                for x in self.frames[z][self.max_y]:
                    if self.get(x, self.max_y, z):
                        expand_max_y = True
                        self.max_y += 1
            if expand_min_y and expand_max_y:
                break
        expand_min_x = expand_max_x = False
        for z in self.frames:
            for y in self.frames[z]:
                if not expand_min_x and self.get(self.min_x, y, z):
                    expand_min_x = True
                    self.min_x -= 1
                if not expand_max_x and self.get(self.max_x, y, z):
                    expand_max_x = True
                    self.max_x += 1
                if expand_min_x and expand_max_x:
                    return
    
    def __str__(self):
        string = ""
        for z in range(self.max_z + 1):
            string += f"z={z}\n"
            for y in range(self.min_y, self.max_y + 1):
                string += str(["#" if self.get(x, y, z) else "." for x in range(self.min_x, self.max_x + 1)]) + "\n"
        return string

def a(lines):
    g = Grid3(lines)
    
    cycles = 6
    for i in range(cycles):
        g.update()
        #print(f"cycle {i+1}")
        #print(g)
    s = 0
    for z in g.frames:
        for y in g.frames[z]:
            for x in g.frames[z][y]:
                if g.get(x, y, z):
                    if z != 0:
                        s += 2
                    else:
                        s += 1
    return s

class Grid4:
    # frames are reflective, i.e. frame at z=1 == frame at z=-1
    # so only have to store n frames rather than 2n-1 frames
    frames = {}  # (z, w) -> y -> x
    updates = []

    max_z_w = 0

    min_y = 0
    max_y = 0

    min_x = 0
    max_x = 0

    def __init__(self, lines):
        self.max_z_w = 0
        self.max_y = len(lines)
        self.max_x = len(lines[0])
        zw = (0, 0)
        self.frames[zw] = {}
        for i in range(len(lines)):
            self.frames[zw][i] = {}
            for j in range(len(lines[i])):
                self.frames[zw][i][j] = False if lines[i][j] == "." else True
    
    def get(self, x, y, z, w):
        try:
            return self.frames[self.__get_zw(z, w)][y][x]
        except KeyError:
            return False
    
    @staticmethod
    def __get_zw(z, w):
        """
        returns the 'lowest' abs val combination tuple (z, w)
        x, y frame at (z=0, w=1) is same as that at (0, -1), (1, 0), (-1, 0)
        """
        z = abs(z)
        w = abs(w)
        return (w, z) if z > w else (z, w)

    def tentative_update(self, x, y, z, w, val):
        if (x, y, self.__get_zw(z, w), val) not in self.updates:
            self.updates.append((x, y, self.__get_zw(z, w), val))

    def push_updates(self):
        for x, y, zw, val in self.updates:
            # lazy node init
            if zw not in self.frames:
                self.frames[zw] = {}
            if y not in self.frames[zw]:
                self.frames[zw][y] = {}
            self.frames[zw][y][x] = val
        self.updates.clear()

    def update(self):
        self.__expand_frames()
        # x, y frame at (z=0, w=1) is same as that at (0, -1), (1, 0), (-1, 0)
        # only have to update 1
        for w in range(self.max_z_w + 1):
            for z in range(w + 1):
                for y in range(self.min_y, self.max_y + 1):
                    for x in range(self.min_x, self.max_x + 1):
                        self.__update(x, y, z, w)
        print("---")
        print(self.updates)
        self.push_updates()

    def __update(self, x, y, z, w):
        n_active = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                for k in range(z - 1, z + 2):
                    for l in range(w - 1, w + 2):
                        if not (i == x and j == y and k == z and l == w) and self.get(i, j, k, l):
                            n_active += 1
        #print(x, y, z, w, n_active)
        if self.get(x, y, z, w) and n_active not in range(2, 4):
            # deactivate
            self.tentative_update(x, y, z, w, False)
        elif not self.get(x, y, z, w) and n_active == 3:
            # activate
            self.tentative_update(x, y, z, w, True)

    def __expand_frames(self):
        # updating min max z y x
        """
        expand_max_z = False
        for z in range(self.max_z_w + 1):
            zw = (z, self.max_z_w)
            for y in self.frames[zw]:
                for x in self.frames[zw][y]:
                    if self.get(x, y, z, self.max_z_w):
                        # active node found in highest z frame, need to expand out by 1 z
                        expand_max_z = True
                        self.max_z_w += 1
                        break
                if expand_max_z:
                    break
            if expand_max_z:
                break
        """
        self.max_z_w += 1
        expand_min_y = expand_max_y = False
        for zw in self.frames:
            z, w = zw
            if not expand_min_y and self.min_y in self.frames[zw]:
                for x in self.frames[zw][self.min_y]:
                    if self.get(x, self.min_y, z, w):
                        expand_min_y = True
                        self.min_y -= 1
            if not expand_max_y and self.max_y in self.frames[zw]:
                for x in self.frames[zw][self.max_y]:
                    if self.get(x, self.max_y, z, w):
                        expand_max_y = True
                        self.max_y += 1
            if expand_min_y and expand_max_y:
                break
        expand_min_x = expand_max_x = False
        for zw in self.frames:
            z, w = zw
            for y in self.frames[zw]:
                if not expand_min_x and self.get(self.min_x, y, z, w):
                    expand_min_x = True
                    self.min_x -= 1
                if not expand_max_x and self.get(self.max_x, y, z, w):
                    expand_max_x = True
                    self.max_x += 1
                if expand_min_x and expand_max_x:
                    return
    
    def __str__(self):
        string = ""
        for w in range(self.max_z_w + 1):
            for z in range(w + 1):
                string += f"zw={(z, w)}\n"
                for y in range(self.min_y, self.max_y + 1):
                    string += str(["#" if self.get(x, y, z, w) else "." for x in range(self.min_x, self.max_x + 1)]) + "\n"
        return string

class Grid4B:
    # frames are reflective, i.e. frame at z=1 == frame at z=-1
    # so only have to store n frames rather than 2n-1 frames
    frames = {}  # w -> z -> y -> x
    updates = []

    min_w = max_w = 0
    min_z = max_z = 0
    min_y = max_y = 0
    min_x = max_x = 0

    def __init__(self, lines):
        self.max_y = len(lines)
        self.max_x = len(lines[0])
        self.frames[0] = {}
        self.frames[0][0] = {}
        for i in range(len(lines)):
            self.frames[0][0][i] = {}
            for j in range(len(lines[i])):
                self.frames[0][0][i][j] = False if lines[i][j] == "." else True
    
    def get(self, x, y, z, w):
        try:
            return self.frames[w][z][y][x]
        except KeyError:
            return False
    
    def tentative_update(self, x, y, z, w):
        self.updates.append((x, y, z, w))

    def push_updates(self):
        for x, y, z, w in self.updates:
            # lazy node init
            if w not in self.frames:
                self.frames[w] = {}
            if z not in self.frames[w]:
                self.frames[w][z] = {}
            if y not in self.frames[w][z]:
                self.frames[w][z][y] = {}
            if x not in self.frames[w][z][y]:
                self.frames[w][z][y][x] = True
            else:
                self.frames[w][z][y][x] = not self.frames[w][z][y][x]
        self.updates.clear()

    def update(self):
        self.__expand_frames()
        for w in range(self.min_w, self.max_w + 1):
            for z in range(self.min_z, self.max_z + 1):
                for y in range(self.min_y, self.max_y + 1):
                    for x in range(self.min_x, self.max_x + 1):
                        self.__update(x, y, z, w)
        self.push_updates()

    def __update(self, x, y, z, w):
        n_active = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                for k in range(z - 1, z + 2):
                    for m in range(w - 1, w + 2):
                        if not (i == x and j == y and k == z and m == w) and self.get(i, j, k, m):
                            n_active += 1
        if self.get(x, y, z, w) and n_active not in range(2, 4):
            # deactivate
            self.tentative_update(x, y, z, w)
        elif not self.get(x, y, z, w) and n_active == 3:
            # activate
            self.tentative_update(x, y, z, w)

    def __expand_frames(self):
        # updating min max z y x
        """
        expand_max_z = False
        if self.max_z in self.frames:
            for y in self.frames[self.max_z]:
                for x in self.frames[self.max_z][y]:
                    if self.get(x, y, self.max_z):
                        # active node found in highest z frame, need to expand out by 1 z
                        expand_max_z = True
                        self.max_z += 1
                        break
                if expand_max_z:
                    break
        """
        self.min_w -= 1
        self.max_w += 1
        
        self.min_z -= 1
        self.max_z += 1

        self.min_y -= 1
        self.max_y += 1

        self.min_x -= 1
        self.max_x += 1
        """
        expand_min_y = expand_max_y = False
        for z in self.frames:
            if not expand_min_y and self.min_y in self.frames[z]:
                for x in self.frames[z][self.min_y]:
                    if self.get(x, self.min_y, z):
                        expand_min_y = True
                        self.min_y -= 1
            if not expand_max_y and self.max_y in self.frames[z]:
                for x in self.frames[z][self.max_y]:
                    if self.get(x, self.max_y, z):
                        expand_max_y = True
                        self.max_y += 1
            if expand_min_y and expand_max_y:
                break
        expand_min_x = expand_max_x = False
        for z in self.frames:
            for y in self.frames[z]:
                if not expand_min_x and self.get(self.min_x, y, z):
                    expand_min_x = True
                    self.min_x -= 1
                if not expand_max_x and self.get(self.max_x, y, z):
                    expand_max_x = True
                    self.max_x += 1
                if expand_min_x and expand_max_x:
                    return
        """
    
    def __str__(self):
        string = ""
        for z in range(self.max_z + 1):
            string += f"z={z}\n"
            for y in range(self.min_y, self.max_y + 1):
                string += str(["#" if self.get(x, y, z) else "." for x in range(self.min_x, self.max_x + 1)]) + "\n"
        return string

class Grid4C:
    nodes = {}  # (w, z, y, x): bool
    updates = []

    min_w = max_w = 0
    min_z = max_z = 0
    min_y = max_y = 0
    min_x = max_x = 0

    def __init__(self, lines):
        self.max_y = len(lines)
        self.max_x = len(lines[0])
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                self.nodes[(0, 0, i, j)] = lines[i][j] == "#"
    
    def get(self, coord):
        try:
            return self.nodes[coord]
        except KeyError:
            return False

    def update(self):
        self.expand()
        w_range = range(self.min_w, self.max_w + 1)
        z_range = range(self.min_z, self.max_z + 1)
        y_range = range(self.min_y, self.max_y + 1)
        x_range = range(self.min_x, self.max_x + 1)
        for coord in product(w_range, z_range, y_range, x_range):
            self.__update(coord)
        self.push_updates()
    
    def __update(self, coord):
        w, z, y, x = coord
        w_range = range(w - 1, w + 2)
        z_range = range(z - 1, z + 2)
        y_range = range(y - 1, y + 2)
        x_range = range(x - 1, x + 2)
        n_active = 0
        for other in product(w_range, z_range, y_range, x_range):
            n_active += 1 * (coord != other and self.get(other))
        if self.get(coord) and n_active not in range(2, 4) or \
           not self.get(coord) and n_active == 3:
            self.updates.append(coord)
    
    def expand(self):
        """
        self.min_w -= 1
        self.max_w += 1
        
        self.min_z -= 1
        self.max_z += 1

        self.min_y -= 1
        self.max_y += 1

        self.min_x -= 1
        self.max_x += 1
        """

        """
        w_range = range(self.min_w, self.max_w + 1)
        z_range = range(self.min_z, self.max_z + 1)
        y_range = range(self.min_y, self.max_y + 1)
        x_range = range(self.min_x, self.max_x + 1)
        p = list(product(w_range, z_range, y_range, x_range))
        """

        # check if need to expand the range of an axis
        def __expand(idx, min_val, max_val):
            expand_min = expand_max = False
            for coord in filter(lambda coord: coord[idx] == min_val or coord[idx] == max_val, self.nodes):
                if self.get(coord):
                    if not expand_min and coord[idx] == min_val:
                        expand_min = True
                    if not expand_max and coord[idx] == max_val:
                        expand_max = True
                if expand_min and expand_max:
                    break
            return (expand_min, expand_max)
        
        a, b = __expand(0, self.min_w, self.max_w)
        self.min_w -= 1*a
        self.max_w += 1*b

        a, b = __expand(1, self.min_z, self.max_z)
        self.min_z -= 1*a
        self.max_z += 1*b

        a, b = __expand(2, self.min_y, self.max_y)
        self.min_y -= 1*a
        self.max_y += 1*b

        a, b = __expand(3, self.min_x, self.max_x)
        self.min_x -= 1*a
        self.max_x += 1*b

    def push_updates(self):
        for coord in self.updates:
            self.nodes[coord] = not self.get(coord)
        self.updates.clear()

def b(lines):
    g = Grid4C(lines)
    cycles = 6
    for i in range(cycles):
        g.update()
    return sum(g.nodes.values())

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))

def a(lines):
    n = 0
    e = 0
    curr_dir = 0
    for line in lines:
        cmd = line[0]
        val = int(line[1:])
        if cmd == "N" or cmd == "F" and curr_dir == 90:
            n += val
        elif cmd == "S" or cmd == "F" and curr_dir == 270:
            n -= val
        elif cmd == "E" or cmd == "F" and curr_dir == 0:
            e += val
        elif cmd == "W" or cmd == "F" and curr_dir == 180:
            e -= val
        elif cmd == "L":
            curr_dir += val
            curr_dir %= 360
        elif cmd == "R":
            curr_dir -= val
            curr_dir %= 360
    return abs(n) + abs(e)

def b(lines):
    x = 0
    y = 0
    n = 1
    e = 10
    for line in lines:
        dir = 0
        cmd = line[0]
        val = int(line[1:])
        if cmd == "N":
            n += val
        elif cmd == "S":
            n -= val
        elif cmd == "E":
            e += val
        elif cmd == "W":
            e -= val
        elif cmd == "L":
            dir -= val
            dir %= 360
        elif cmd == "R":
            dir += val
            dir %= 360
        elif cmd == "F":
            x += val * e
            y += val * n
        
        if dir:
            if dir == 90:
                tmp_n = n
                n = -e
                e = tmp_n
            elif dir == 180:
                n *= -1
                e *= -1
            elif dir == 270:
                tmp_n = n
                n = e
                e = -tmp_n
    return abs(x) + abs(y)

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))

from functools import reduce
import operator

def a(f, xshift=3, yshift=1):
    trees = 0
    x = 0
    y = 0
    for line in f:
        r = y % yshift != 0
        y += 1
        if r:
            continue
        line = line.strip()
        x %= len(line)
        if line[x] == "#":
            trees += 1
        x += xshift
    print(trees)
    return trees

def b(f):
    r = [a(f, 1, 1), a(f, 3, 1), a(f, 5, 1), a(f, 7, 1), a(f, 1, 2)]
    print(r)
    print(reduce(operator.mul, r))

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.readlines()
    b(lines)

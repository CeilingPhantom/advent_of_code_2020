def a(f):
    i = 0
    for line in f:
        stuff = line.strip().split()
        [lo, hi] = map(lambda x: int(x), stuff[0].split("-"))
        letter = stuff[1][:-1]
        pw = stuff[2]
        j = 0
        for c in pw:
            if c == letter:
                j += 1
        if j >= lo and j <= hi:
            i += 1
    print(i)

def b(f):
    i = 0
    for line in f:
        stuff = line.strip().split()
        [lo, hi] = map(lambda x: int(x) - 1, stuff[0].split("-"))
        letter = stuff[1][:-1]
        pw = stuff[2]
        if (pw[lo] == letter) != (pw[hi] == letter):
            i += 1
    print(i)

if __name__ == "__main__":
    with open("in", "r") as f:
        b(f)

def a(lines):
    mask = "X"*36
    mem = {}
    for line in lines:
        words = line.split(" = ")
        if words[0] == "mask":
            mask = words[1]
        else:
            idx = words[0][4:-1]
            val = bin(int(words[1]))[2:]
            val = list("0"*(len(mask)-len(val)) + val)
            for i in range(len(mask)):
                if mask[i] != "X":
                    val[i] = mask[i]
            mem[idx] = int("".join(val), 2)
    return sum(mem.values())

def b(lines):
    mask = "0"*36
    mem = {}
    for line in lines:
        words = line.split(" = ")
        if words[0] == "mask":
            mask = words[1]
        else:
            idx = bin(int(words[0][4:-1]))[2:]
            idx = list("0"*(len(mask)-len(idx)) + idx)
            val = int(words[1])
            for i in range(len(mask)):
                if mask[i] != "0":
                    idx[i] = mask[i]
            for addr in addrs(idx):
                mem[addr] = val
    return sum(mem.values())

def addrs(floating_addr: list):
    try:
        i = floating_addr.index("X")
        a = floating_addr.copy()
        b = floating_addr.copy()
        a[i] = "0"
        b[i] = "1"
        return addrs(a) + addrs(b)
    except ValueError:
        return [int("".join(floating_addr), 2)]

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))

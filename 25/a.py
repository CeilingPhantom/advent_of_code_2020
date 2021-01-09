init_subject_number = 7
divisor = 20201227

def a(lines):
    pub_key1 = int(lines[0])
    pub_key2 = int(lines[1])
    loop_size = 0
    val = 1
    while True:
        if val == pub_key1:
            return transform(pub_key2, loop_size)
        elif val == pub_key2:
            return transform(pub_key1, loop_size)
        loop_size += 1
        val *= init_subject_number
        val %= divisor

def transform(subject_number, loops):
    val = 1
    while loops:
        val *= subject_number
        val %= divisor
        loops -= 1
    return val

def b(lines):
    return

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(a(lines))

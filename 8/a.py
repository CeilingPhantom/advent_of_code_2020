def a(lines):
    (acc, _) = a_helper({}, lines)
    return acc

def a_helper(d, lines, acc=0, line_num=0):
    if line_num >= len(lines):
        return (acc, True)
    if line_num in d:
        return (acc, False)
    d[line_num] = 1
    words = lines[line_num].strip().split()
    cmd = words[0]
    num = int(words[1])
    if cmd == "acc":
        acc += num
    elif cmd == "jmp":
        return a_helper(d, lines, acc, line_num + num)
    return a_helper(d, lines, acc, line_num + 1)

def b(lines):
    # get nop +x and jmp -x cmds
    for i in range(len(lines)):
        words = lines[i].strip().split()
        cmd = words[0]
        num = int(words[1])
        if cmd == "jmp":
            lines_cp = lines.copy()
            lines_cp[i] = f"nop {num}"
        elif cmd == "nop":
            lines_cp = lines.copy()
            lines_cp[i] = f"jmp {num}"
        else:
            lines_cp = []
        if lines_cp:
            (acc, res) = a_helper({}, lines_cp)
            if res:
                return acc
    return

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.readlines()
    print(b(lines))

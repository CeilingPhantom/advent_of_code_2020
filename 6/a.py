def a(lines):
    count = 0
    curr_group = {}
    for line in lines:
        stuff = line.strip()
        if stuff:
            for c in stuff:
                curr_group[c] = 0
        else:
            # print(len(curr_group))
            count += len(curr_group)
            curr_group.clear()
    # last group
    count += len(curr_group)
    return count

def b(lines):
    count = 0
    curr_group = []
    is_first = True
    for line in lines:
        stuff = line.strip()
        if stuff:
            if is_first:
                is_first = False
                curr_group = [*stuff]
            else:
                curr_group = [c for c in curr_group if c in stuff]
        else:
            # print(len(curr_group))
            count += len(curr_group)
            curr_group.clear()
            is_first = True
    # last group
    count += len(curr_group)
    return count

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.readlines()
    print(b(lines))

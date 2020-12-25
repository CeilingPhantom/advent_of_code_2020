def a(lines):
    return len(a_helper(parse_in(lines), ["shiny gold"]))

def a_helper(d, bag_types):
    if len(bag_types) == 0:
        return set()
    new_valid_bag_types = set()
    for k, v in d.items():
        for bag_type in bag_types:
            if bag_type in v:
                new_valid_bag_types.add(k)
    return new_valid_bag_types.union(a_helper(d, new_valid_bag_types))

b_table = {}

def b(lines):
    return b_helper(parse_in(lines), "shiny gold")

def b_helper(d, bag_type):
    if bag_type in b_table:
        return b_table[bag_type]
    count = 0
    for k, v in d[bag_type].items():
        count += v + v*b_helper(d, k)
    b_table[bag_type] = count
    return count

def parse_in(lines):
    d = {}
    for line in lines:
        key, raw_vals = line.strip().split(" bags contain ")
        d[key] = {}
        vals = raw_vals[:-1].split(", ")
        for bag_str in vals:
            words = bag_str.split()
            if (words[0] != "no"):
                count = int(words[0])
                bag_type = " ".join(words[1:-1])
                d[key][bag_type] = count
    return d

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.readlines()
    print(b(lines))

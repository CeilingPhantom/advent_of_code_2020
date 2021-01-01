from itertools import product
rules = {}
unpacked_rules = {}

def a(lines):
    i = fill_rules(lines)
    combinations = combs("0")
    return sum(1 for line in lines[i:] if line in combinations)

def fill_rules(lines):
    i = 0
    while i < len(lines):
        if not lines[i]:
            i += 1
            break
        k, v = lines[i].split(": ")
        if "\"" in v:
            vals = v[1:-1]
            unpacked_rules[k] = vals
        else:
            vals = [x.split() for x in v.split(" | ")]
        rules[k] = vals
        i += 1
    return i

def combs(rule):
    if rule not in unpacked_rules:
        unpacked_rules[rule] = []
        for subcomb in rules[rule]:
            unpacked_rules[rule] += ["".join(x) for x in product(*[combs(subrule) for subrule in subcomb])]
    return unpacked_rules[rule]

# 8: 42 | 42 8
# 11: 42 31 | 42 11 31

# 0: 8 11

def b(lines):
    i = fill_rules(lines)
    # fill in the rules that the recursive ones rely on
    combs("42")
    combs("31")
    #print(unpacked_rules["42"])
    #print(unpacked_rules["31"])
    #print("===")
    # all combinations seem to be same length (8)
    # and contain all different words
    count = 0
    word_len = len(unpacked_rules["42"][0])
    for line in lines[i:]:
        count += b_helper([line[i:i+word_len] for i in range(0, len(line), word_len)])
    return count

def b_helper(words):
    i = 0
    i_lock = False
    j = 0
    for word in words:
        if not i_lock and word in unpacked_rules["42"]:
            i += 1
        elif word in unpacked_rules["31"]:
            j += 1
            i_lock = True
        else:
            return False
    # make sure they occur at least once
    return i != 0 and j != 0 and i > j

if __name__ == "__main__":
    with open("in2", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))

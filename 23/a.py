rounds_a = 100
max_val_a = 9
n_pickup_cups = 3

def a(lines):
    cups = [int(x) for x in lines[0]]

    for _ in range(rounds_a):
        dest_cup_idx = get_dest_cup_idx(cups, max_val_a)
        # move the 3 picked up cups
        for _ in range(n_pickup_cups):
            cups.insert(dest_cup_idx, cups.pop(1))
        # make new curr cup be at the front
        cups.append(cups.pop(0))
    
    # make cup #1 be in front
    cup_1_idx = cups.index(1)
    return "".join(str(x) for x in cups[cup_1_idx+1:] + cups[:cup_1_idx])

def get_dest_cup_idx(cups, max_val, i=1):
    try:
        val = (cups[0] - i) % (max_val + 1)
        if val == 0:
            i += 1
            val = (cups[0] - i) % (max_val + 1)
        idx = cups.index(val)
        if idx < 4:
            return get_dest_cup_idx(cups, i + 1)
        return idx
    except ValueError:
        return get_dest_cup_idx(cups, i + 1)

def a2(lines):
    cups_next = [i+1 for i in range(0, max_val_a+1)]
    cups_input = [int(x) for x in lines[0]]
    for i, cup in enumerate(cups_input[:-1]):
        cups_next[cup] = cups_input[i+1]
    cups_next[cups_input[-1]] = cups_input[0]
    curr_cup = cups_input[0]
    move = 1
    print(f"move {move}")
    print("align", [i for i in range(1,10)])
    print("cups:", cups_next[1:])
    str_cups(cups_next, curr_cup)
    for _ in range(10):
        # "disconnect" linked list and "reconnnect" it
        pickup_cups = [cups_next[curr_cup]]
        for _ in range(2):
            pickup_cups.append(cups_next[pickup_cups[-1]])
        print("pick up:", pickup_cups)
        curr_cup_next = cups_next[pickup_cups[-1]]
        dest_cup = (curr_cup - 1) % (max_val_a + 1)
        if dest_cup == 0:
            dest_cup = max_val_a
        while dest_cup in pickup_cups:
            dest_cup = (dest_cup - 1) % (max_val_a + 1)
            if dest_cup == 0:
                dest_cup = max_val_a
        print("dest:", dest_cup)
        print()
        last_pickup_cup_next = cups_next[dest_cup]
        cups_next[curr_cup] = curr_cup_next
        cups_next[pickup_cups[-1]] = last_pickup_cup_next
        cups_next[dest_cup] = pickup_cups[0]
        curr_cup = cups_next[curr_cup]
        move += 1
        print(f"move {move}")
        print("align", [i for i in range(1,10)])
        print("cups:", cups_next[1:])
        str_cups(cups_next, curr_cup)

rounds_b = 10000000
max_val_b = 1000000

def b(lines):
    # "linked" list of cup to next cup
    cups_next = [i+1 for i in range(0, max_val_b+1)]
    cups_input = [int(x) for x in lines[0]]
    for i, cup in enumerate(cups_input[:-1]):
        cups_next[cup] = cups_input[i+1]
    cups_next[cups_input[-1]] = max_val_a + 1
    cups_next[max_val_b] = cups_input[0]
    curr_cup = cups_input[0]
    for _ in range(rounds_b):
        # "disconnect" linked list and "reconnnect" it
        pickup_cups = [cups_next[curr_cup]]
        for _ in range(2):
            pickup_cups.append(cups_next[pickup_cups[-1]])
        curr_cup_next = cups_next[pickup_cups[-1]]
        dest_cup = (curr_cup - 1) % (max_val_b + 1)
        if dest_cup == 0:
            dest_cup = max_val_b
        while dest_cup in pickup_cups:
            dest_cup = (dest_cup - 1) % (max_val_b + 1)
            if dest_cup == 0:
                dest_cup = max_val_b
        # update connections from curr cup, dest cup, last pickup cup
        last_pickup_cup_next = cups_next[dest_cup]
        cups_next[curr_cup] = curr_cup_next
        cups_next[pickup_cups[-1]] = last_pickup_cup_next
        cups_next[dest_cup] = pickup_cups[0]
        curr_cup = cups_next[curr_cup]
    return cups_next[1] * cups_next[cups_next[1]]

def str_cups(cups_next, curr_cup):
    string = str(curr_cup)
    for _ in range(max_val_b):
        curr_cup = cups_next[curr_cup]
        string += f" {curr_cup}"
    print(string)

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))

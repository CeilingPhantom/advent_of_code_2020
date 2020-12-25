def a(lines):
    lines = [[*x.strip()] for x in lines]
    helper(lines, a_adjacent_occupied, 4)
    n_occupied = 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "#":
                n_occupied += 1
    return n_occupied

def helper(lines, adj_func, max_adj_occupied):
    changes = []
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "L" and adj_func(lines, i, j) == 0:
                changes.append((i, j, "#"))
            elif lines[i][j] == "#" and adj_func(lines, i, j) >= max_adj_occupied:
                changes.append((i, j, "L"))
    if changes:
        for change in changes:
            i, j, sym = change
            lines[i][j] = sym
        helper(lines, adj_func, max_adj_occupied)

def a_adjacent_occupied(lines, y, x):
    n_occupied = 0
    left_x = max(0, x - 1)
    right_x = min(len(lines[0]) - 1, x + 1)
    top_y = max(0, y - 1)
    bot_y = min(len(lines) - 1, y + 1)
    for i in range(top_y, bot_y + 1):
        for j in range(left_x, right_x + 1):
            if i == y and j == x:
                continue
            elif lines[i][j] == "#":
                n_occupied += 1
    return n_occupied

def b(lines):
    lines = [[*x.strip()] for x in lines]
    helper(lines, b_adjacent_occupied, 5)
    n_occupied = 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "#":
                n_occupied += 1
    return n_occupied

def b_adjacent_occupied(lines, y, x):
    adjacent_seats = []
    # top row
    adjacent_seats.append(get_first_seat(lines, y - 1, x - 1, -1, -1))
    adjacent_seats.append(get_first_seat(lines, y - 1, x    , -1, 0))
    adjacent_seats.append(get_first_seat(lines, y - 1, x + 1, -1, 1))
    # mid row
    adjacent_seats.append(get_first_seat(lines, y, x - 1, 0, -1))
    adjacent_seats.append(get_first_seat(lines, y, x + 1, 0, 1))
    # bot row
    adjacent_seats.append(get_first_seat(lines, y + 1, x - 1, 1, -1))
    adjacent_seats.append(get_first_seat(lines, y + 1, x    , 1, 0))
    adjacent_seats.append(get_first_seat(lines, y + 1, x + 1, 1, 1))

    return adjacent_seats.count("#")

def get_first_seat(lines, y, x, y_incr, x_incr):
    if y < 0 or y >= len(lines) or x < 0 or x >= len(lines[0]):
        return "."
    seat = lines[y][x]
    return seat if seat != "." else get_first_seat(lines, y + y_incr, x + x_incr, y_incr, x_incr)

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.readlines()
    print(b(lines))

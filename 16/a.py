from functools import reduce

def a(lines):
    i = 0
    valid_vals = set()
    while lines[i]:
        fields, vals = lines[i].split(": ")
        vals = [val.split("-") for val in vals.split(" or ")]
        vals = [range(int(x), int(y)+1) for x, y in vals]
        for val in vals:
            valid_vals.update(val)
        i += 1
    # skip own ticket
    i += 1
    while lines[i] != "nearby tickets:":
        i += 1
    i += 1
    invalid_fields = []
    while i < len(lines):
        nearby_ticket = [int(x) for x in lines[i].split(",")]
        for field in nearby_ticket:
            if field not in valid_vals:
                invalid_fields.append(field)
        i += 1
    return sum(invalid_fields)

def b(lines):
    col_vals = []
    col_vals_viable_fields = []

    i = 0
    fields = {}
    all_valid_vals = set()
    while lines[i]:
        field, vals = lines[i].split(": ")
        vals = [val.split("-") for val in vals.split(" or ")]
        vals = [range(int(x), int(y)+1) for x, y in vals]
        valid_vals = set()
        for val in vals:
            all_valid_vals.update(val)
            valid_vals.update(val)
        fields[field] = valid_vals

        col_vals.append(set())
        col_vals_viable_fields.append([])

        i += 1
    i += 2
    self_ticket = [int(x) for x in lines[i].split(",")]
    i += 3
    valid_nearby_tickets = []
    while i < len(lines):
        nearby_ticket = [int(x) for x in lines[i].split(",")]
        invalid = False
        for field in nearby_ticket:
            if field not in all_valid_vals:
                invalid = True
                break
        if not invalid:
            valid_nearby_tickets.append(nearby_ticket)
        i += 1
    for ticket in valid_nearby_tickets:
        for i in range(len(ticket)):
            col_vals[i].add(ticket[i])
    for i in range(len(col_vals)):
        for field, valid_vals in fields.items():
            if valid_vals.issuperset(col_vals[i]):
                col_vals_viable_fields[i].append(field)
    # start with ones with only 1 viable field, ...
    s = sorted(zip(col_vals_viable_fields, list(range(len(fields)))), key=lambda pair: len(pair[0]))
    col_vals_viable_fields = [x[0] for x in s]
    cols = [x[1] for x in s]
    cols_dict = dict.fromkeys([x[1] for x in s])

    print(col_vals_viable_fields)
    print([x[1] for x in s])

    taken_fields = []
    departure_fields_idx = []
    for i in range(len(col_vals_viable_fields)):
        if i == 0:
            # assuming first will only contain 1 field
            field = col_vals_viable_fields[i][0]
        else:
            # by inspection, each list in col_vals_viable_fields seem to grow by 1 field
            [field] = [x for x in col_vals_viable_fields[i] if x not in taken_fields]
        taken_fields.append(field)
        cols_dict[i] = field
        if "departure" in field:
            departure_fields_idx.append(cols[i])
        
    #print(cols_dict)
    print(cols_dict)
    print(departure_fields_idx)
    return reduce(lambda x, y: x*y, [self_ticket[i] for i in departure_fields_idx])

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))

import operator

ops = {
    "+": operator.add,
    "*": operator.mul,
}

def a(lines):
    s = 0
    for i in range(len(lines)):
        t = eval_a(lines[i].split())
        s += t
        #print(i, t)
    return s

def eval_a(tokens):
    s = 0
    op = ops["+"]
    expr = []
    i = 0
    while i < len(tokens):
        try:
            # number
            #print("===", s, int(tokens[i]), op)
            s = op(s, int(tokens[i]))
            expr.append(int(tokens[i]))
            i += 1
        except ValueError:
            try:
                # operation
                op = ops[tokens[i]]
                expr.append(tokens[i])
                #print("new op", i, tokens[i], op)
                i += 1
            except KeyError:
                # found opening parentheses
                n_open = tokens[i].count("(") - tokens[i].count(")")
                #print(n_open, i, tokens[i])
                #print("---")
                j = i
                i += 1
                while n_open:
                    n_open = n_open + tokens[i].count("(") - tokens[i].count(")")
                    #print(n_open, i, tokens[i])
                    #print("---")
                    i += 1
                inner = tokens[j:i]
                # trim parentheses from first and last tokens
                inner[0] = inner[0][1:]
                inner[-1] = inner[-1][:-1]
                #print("===", s, inner, op)
                t = eval_a(inner)
                s = op(s, t)
                expr.append(t)
    #print("sum", s, expr)
    return s

def b(lines):
    """
    for line in lines:
        x = b_parser(line.split())
        print(x)
        print(eval_b(x))
    """
    return sum(eval_b(b_parser(line.split())) for line in lines)

def b_parser(tokens):
    exprs = []
    i = 0
    while i < len(tokens):
        try:
            # number
            exprs.append(int(tokens[i]))
            i += 1
        except ValueError:
            try:
                # operation
                _ = ops[tokens[i]]
                exprs.append(tokens[i])
                i += 1
            except KeyError:
                # found opening parentheses
                n_open = tokens[i].count("(") - tokens[i].count(")")
                j = i
                i += 1
                while n_open:
                    n_open = n_open + tokens[i].count("(") - tokens[i].count(")")
                    i += 1
                inner = tokens[j:i]
                # trim parentheses from first and last tokens
                inner[0] = inner[0][1:]
                inner[-1] = inner[-1][:-1]
                t = b_parser(inner)
                exprs.append(t)
    return b_formatter(exprs)

# groups adds
def b_formatter(tokens):
    # won't be first or last token anyways
    for i in range(1, len(tokens) - 1):
        if tokens[i] == "+":
            formatted = tokens[:i-1] + [tokens[i-1:i+2]] + tokens[i+2:]
            return b_formatter(formatted)
    return tokens

def eval_b(tokens):
    if type(tokens) is not list:
        # singular number
        return tokens
    s = None
    for i in range(len(tokens)):
        if s == None:
            s = eval_b(tokens[i])
        elif type(tokens[i]) is str and tokens[i] in ops:
            s = ops[tokens[i]](s, eval_b(tokens[i+1]))
    return s

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))

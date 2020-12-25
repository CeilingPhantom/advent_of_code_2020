from functools import reduce

def a(lines):
    departure = int(lines[0])
    buses = [int(x) for x in lines[1].split(",") if x != "x"]
    lo_bus = buses[0]
    lo_wait = lo_bus - departure % lo_bus
    for bus in buses[1:]:
        wait = bus - departure % bus
        if wait < lo_wait:
            lo_bus = bus
            lo_wait = wait
    return lo_bus * lo_wait

def b(lines):
    buses = [int(x) if x != "x" else x for x in lines[1].split(",")]
    mod_dict = {buses[i]: buses[i] - i for i in range(len(buses)) if buses[i] != "x"}
    #mod_dict = {3: 0, 4: 3, 5: 4}
    #mod_dict = {7:0, 13:13-1, 59:59-4, 31:31-6, 19:19-7}
    #print(mod_dict)

    # chinese remainder theorem
    buses = list(mod_dict.keys())
    buses.sort(reverse=True)
    m = None
    for bus in buses:
        if not m:
            m = bus
            continue
        (a, b) = bezout_primes(m, bus)
        print(m, bus)
        print(a, b)
        print("---")
        mod_dict[m * bus] = (mod_dict[bus]*a*m + mod_dict[m]*b*bus) % (m * bus)
        m *= bus
    print(mod_dict)
    return mod_dict[m]

# x > y
def bezout_primes(x, y):
    q = int(x/y)
    r = x % y
    if r == 1:
        return (1, -q)
    (a, b) = bezout_primes(y, r)
    # 1 = {a}*{y} + {b}*{r}
    #print(f"1 = {a}*{y} + {b}*({x} - {q}*{y})")
    return (b, (a-b*q))

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b(lines))
    #print(bezout_primes(13, 7))

"""
x = 0 mod 7
x = 1 mod 13
x = 4 mod 59
x = 6 mod 31
x = 7 mod 19
"""

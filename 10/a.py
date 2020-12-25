def a(lines):
    s = jolt_set(lines)
    diff1, diff3 = a_helper(s, 0)
    return diff1*diff3

def a_helper(s, curr_jolt, diff1=0, diff3=0):
    if curr_jolt == max(s):
        return (diff1, diff3+1)
    for i in range(1, 3+1):
        if curr_jolt + i in s:
            curr_jolt += i
            if i == 1:
                diff1 += 1
            elif i == 3:
                diff3 += 1
            break
    return a_helper(s, curr_jolt, diff1, diff3)

b_table = {}

def b(lines):
    s = jolt_set(lines)
    return b_helper(s, 0)

def b_helper(s, curr_jolt):
    if curr_jolt not in b_table:    
        count = 0
        if curr_jolt != max(s):
            for i in range(1, 3+1):
                if curr_jolt + i in s:
                    count += b_helper(s, curr_jolt + i)
        else:
            count = 1
        b_table[curr_jolt] = count
    return b_table[curr_jolt]

def jolt_set(lines):
    return set([int(x.strip()) for x in lines])

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.readlines()
    print(b(lines))

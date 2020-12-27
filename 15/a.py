def a(lines):
    #lines[0] = "0,3,6"
    nums = [int(i) for i in lines[0].split(",")]
    history = {nums[i]: [0, i + 1] for i in range(len(nums))}
    num = nums[-1]
    #print(history)
    for i in range(len(nums) + 1, 2020 + 1):
        #print("---")
        h0 = history[num][0]
        new_num = h0 if h0 == 0 else i - 1 - h0
        if new_num not in history:
            history[new_num] = [0]
        else:
            history[new_num].pop(0)
        history[new_num].append(i)
        #print(f"turn {i}, prev_num {num}, new_num {new_num}")
        #print(history)
        num = new_num
    return num

def b(lines):
    #lines[0] = "0,3,6"
    nums = [int(i) for i in lines[0].split(",")]
    history = [0] * 30000000
    for i in range(1, len(nums) + 1):
        history[nums[i - 1]] = i
    num = 0  # will always be 0
    for i in range(len(nums) + 1, 30000000):
        # we know the number to say for this turn, so we
        # update the history for that num to be this turn
        # and determine the number to be spoken next turn
        prev_turn = history[num]
        history[num] = i
        num = 0 if prev_turn == 0 else i - prev_turn
    #print(history)
    return num

def b2(lines):
    nums = [int(i) for i in lines[0].split(",")]
    history = [0] * 30000000
    next_num = 0
    for i in range(1, 30000000):
        if i <= len(nums):
            history[nums[i-1]] = i
        else:
            last_turn_spoken = history[next_num]
            history[next_num] = i
            next_num = (i - last_turn_spoken) * bool(last_turn_spoken)
    return next_num

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.read().splitlines()
    print(b2(lines))

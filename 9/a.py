def a(lines):
    nums = [int(x.strip()) for x in lines]
    region = nums[:25]
    for i in range(25, len(nums)):
        x = nums[i]
        incr_region = False
        for y in region:
            if x - y in region:
                incr_region = True
                region.remove(region[0])
                region.append(x)
                break
        if not incr_region:
            return x

def b(lines):
    nums = [int(x.strip()) for x in lines]
    invalid_num = a(lines)
    lo = 0
    hi = 1
    s = sum(nums[lo:hi])
    while lo < len(nums) and hi < len(nums) and s != invalid_num:
        if s > invalid_num:
            lo += 1
        elif s < invalid_num:
            hi +=1
        s = sum(nums[lo:hi])
    region = nums[lo:hi]
    return min(region) + max(region)

if __name__ == "__main__":
    with open("in", "r") as f:
        lines = f.readlines()
    print(b(lines))

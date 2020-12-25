def a(nums):
    for i in range(0, len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == 2020:
                print(nums[i], nums[j])
                print(nums[i]*nums[j])
                return

def b(nums):
    for i in range(0, len(nums)):
        for j in range(i+1, len(nums)):
            for k in range(j+1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 2020:
                    print(nums[i], nums[j], nums[k])
                    print(nums[i]*nums[j]*nums[k])
                    return


if __name__ == "__main__":
    nums = []
    with open("in", "r") as f:
        for num in f:
            nums.append(int(num.strip()))
    b(nums)

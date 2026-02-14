# https://leetcode.com/problems/count-dominant-indices/description/

def dominantIndices(nums):
    # Can be done with prefix sum as well
    n = len(nums)
    count = 0
    current = sum(nums)

    for i in range(len(nums)-1):
        current = current - nums[i]
        if nums[i] * (n-i-1) > current:
            count += 1

    return count


nums = [4, 1, 2]
print(dominantIndices(nums))

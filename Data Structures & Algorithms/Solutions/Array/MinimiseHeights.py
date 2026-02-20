# https://www.geeksforgeeks.org/problems/minimize-the-heights3351/1
# Note : "Minimise" the difference
# Two pointers approach
# Best explanation : https://www.youtube.com/watch?v=GasFSMyBPto
def minimiseHeights(nums, k):
    nums.sort()
    n = len(nums) - 1
    max_height = nums[n] - k
    min_height = nums[0] + k
    ans = nums[n] - nums[0]

    for i in range(n):
        max_height = max(max_height, nums[i] + k)    # Addn might make the high
        min_height = min(min_height, nums[i+1] - k)  # Subs might make the low

        # Height can't be negative
        if min_height < 0:
            continue

        ans = min(ans, max_height - min_height)

    return ans


nums = [3, 9, 12, 16, 20]
k = 3
print(minimiseHeights(nums, k))

# https://www.geeksforgeeks.org/dsa/largest-sum-contiguous-subarray/
# https://leetcode.com/problems/maximum-subarray/description/

# TC : O(n^2) | SC :O(1)
def maxSubArraySumNaive(nums):
    # Naive approach : Get sum of all subarray one by one, get max
    max_sum = float('-inf')

    for i in range(len(nums)):
        cursum = 0
        for k in range(i, len(nums)):
            cursum += nums[k]
        max_sum = max(max_sum, cursum)

    return max_sum


nums = [2, 3, -8, 7, -1, 2, 3]
print(maxSubArraySumNaive(nums))


# TC : O(n) and SC : O(1)
# The idea of Kadane's algorithm is to traverse over the array from left to
# right and for each element, find the maximum sum among all subarrays ending
# at that element. The result will be the maximum of all these values.
# Sub-array is contagious
def maxSubArraySum(nums):
    currmax = nums[0]
    max_sum = nums[0]

    for i in range(1, len(nums)):
        currmax = max(currmax + nums[i], nums[i])
        max_sum = max(max_sum, currmax)

    return max_sum


nums = [2, 3, -8, 7, -1, 2, 3]
print(maxSubArraySum(nums))

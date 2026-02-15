# https://www.geeksforgeeks.org/dsa/move-negative-numbers-beginning-positive-end-constant-extra-space/
"""
Move all negative numbers to beginning and positive to end with
constant extra space.
Given array does not contain any zeroes.
Order of resultant array does not matter.
"""


# Two pointers | TC : O(n) and SC : O(1)
def move_number(nums):
    low, high = 0, len(nums) - 1

    while low <= high:
        if nums[low] > 0 and nums[high] > 0:
            high -= 1
        elif nums[low] > 0 and nums[high] < 0:
            nums[low], nums[high] = nums[high], nums[low]
            low += 1
            high -= 1
        elif nums[low] < 0 and nums[high] > 0:
            low += 1
            high -= 1
        else:
            low += 1

    return nums


nums = [-12, 11, -13, -5, 6, -7, 5, -3, -6]
print(move_number(nums))

nums = [-1, -5, -6, 12, 14, -6, 98, -34]
print(move_number(nums))

nums = [-1, -5, -6, -12, -14, -6, -98, -34]
print(move_number(nums))

nums = [1, 2, 5, 6, 8, -1]
print(move_number(nums))

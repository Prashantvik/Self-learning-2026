# https://leetcode.com/problems/sort-colors/
def sortColors(nums):
    """
    Do not return anything, modify nums in-place instead.
    """
    # Counting Sort
    zeros, ones, twos = 0, 0, 0
    for num in nums:
        zeros += int(num == 0)
        ones += int(num == 1)
        twos += int(num == 2)

    index, n = 0, len(nums)
    while index < n - 1:
        while zeros:
            nums[index] = 0
            index += 1
            zeros -= 1
        while ones:
            nums[index] = 1
            index += 1
            ones -= 1
        while twos:
            nums[index] = 2
            index += 1
            twos -= 1

    return nums


nums = [2, 0, 2, 1, 1, 0]
print(sortColors(nums))


# Very important to understand this indexdle step for further optimisation
def sortColors_twopass(nums):
    low, zeros, end = 0, 0, len(nums)-1

    while low <= end:
        if nums[low] == 0:
            nums[low], nums[zeros] = nums[zeros], nums[low]
            low += 1
            zeros += 1
        else:
            low += 1

    ones, low = zeros, zeros
    while low <= end:
        if nums[low] == 1:
            nums[low], nums[ones] = nums[ones], nums[low]
            low += 1
            ones += 1
        else:
            low += 1

    return nums


nums = [2, 0, 2, 1, 1, 0]
print(sortColors_twopass(nums))


# Come up with a one-pass algorithm using only constant extra space
# Two pointers | QuickSort Partition | Optimising the twopass function
def sortColors_onepass(nums):
    low, index, high = 0, 0, len(nums)-1
    while index <= high:
        if nums[index] == 0:
            nums[low], nums[index] = nums[index], nums[low]
            low += 1
            index += 1
        elif nums[index] == 1:
            index += 1
        else:
            nums[index], nums[high] = nums[high], nums[index]
            high -= 1

    return nums


nums = [0, 1, 1, 0, 1, 2, 1, 2, 0, 0, 0, 1]
print(sortColors_onepass(nums))

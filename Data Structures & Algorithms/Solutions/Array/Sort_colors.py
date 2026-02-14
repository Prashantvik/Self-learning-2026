# Come up with a one-pass algorithm using only constant extra space
# Two pointers
def sortColors_onepass(nums):
    low, mid, high = 0, 0, len(nums)-1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1

    return nums


nums = [0, 1, 1, 0, 1, 2, 1, 2, 0, 0, 0, 1]
print(sortColors_onepass(nums))

nums = [2, 0, 2, 1, 1, 0]
print(sortColors_onepass(nums))

nums = [2, 0, 1]
print(sortColors_onepass(nums))

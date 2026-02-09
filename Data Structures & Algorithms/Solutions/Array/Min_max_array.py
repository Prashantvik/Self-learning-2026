# Maximum and minimum of an array using minimum number of comparisons

arr = [3, 5, 4, 1, 9]  # Output : [1, 9]


# Can also be done using sorting | TC : O(nlogn) and SC : O(1)
# TC : O(n) and SC : O(1) | Worst Case: 2 * n comparisons
def get_min_max(nums):
    maxi = float('-inf')
    mini = float('inf')

    for i in range(len(nums)):
        maxi = max(maxi, nums[i])
        mini = min(mini, nums[i])

    return [mini, maxi]


result = get_min_max(arr)
print(result)


# Optimise for number of comparisons | Couldn't think from this pov
# Refer : https://www.geeksforgeeks.org/dsa/maximum-and-minimum-in-an-array
# Recursion | Divide and conquer
# Idea : Split the array till it can't be splitted, base case of even/odd len
def get_min_max_optimised(nums, low, high):
    result = [0, 0]

    # Base case | one element
    if low == high:
        result[0] = nums[low]
        result[1] = nums[high]
        return result

    # Base case | two element
    if high == low + 1:
        if nums[high] < nums[low]:
            result[0] = nums[high]
            result[1] = nums[low]
        else:
            result[0] = nums[low]
            result[1] = nums[high]
        return result

    mid = (low + high) // 2

    # Split the array | recursion on left
    left = get_min_max_optimised(nums, low, mid)

    # Split the array | recursion on right
    right = get_min_max_optimised(nums, mid+1, high)

    result[0] = min(left[0], right[0])
    result[1] = max(left[1], right[1])

    return result


nums = [22, 14, 8, 17, 35, 3]
ans = get_min_max_optimised(nums, 0, len(nums)-1)
print(ans)

# https://www.geeksforgeeks.org/problems/cyclically-rotate-an-array-by-one2614/1
# Rotate an array by 1 position | Variation : Rotate by k position
# In place rotation

def rotate_array_left(nums):
    n = len(nums)
    temp = nums[0]

    for i in range(1, n-1):
        nums[i-1], nums[i] = nums[i], nums[i+1]

    nums[n-1] = temp

    return nums


nums = [3, 5, 7, 8, 6, 9, 10]
print(rotate_array_left(nums))


def rotate_array_right(nums):
    n = len(nums)
    temp = nums[n-1]

    for i in range(n-1, 0, -1):
        nums[i], nums[i-1] = nums[i-1], nums[i]

    nums[0] = temp

    return nums


nums = [3, 5, 7, 8, 6, 9, 10]
print(rotate_array_right(nums))

for i in range(5):
    rotate_array_right(nums)

print(nums)


# Rotate an array by k steps in right direction
# Bad code, everytime we rotate by 1, we are doing O(n) work, so total O(n*k)
def rotate_array_k_base(nums, k):
    pass
    # Store the element
    # Shift the array
    # Fill up the stored array


# Optimised Solution | Couldn't come up with approach
# Intution : We can reverse the array and then compare
# Then reverse the first k elements and then reverse the remaining n-k elements
# Helper function
def reverse_array(nums, start, end):
    while start < end:
        nums[start], nums[end] = nums[end], nums[start]
        start += 1
        end -= 1


def rotate_array_k(nums, k):
    n = len(nums)
    # Handle k larger than n | Use of mod
    k = k % n

    reverse_array(nums, 0, n-1)
    reverse_array(nums, 0, k-1)
    reverse_array(nums, k, n-1)


nums = [3, 5, 7, 8, 6, 9, 10]
k = 5
print(f"Original array : {nums}")
rotate_array_k(nums, k)
print(f"After {k} rotation array : {nums}")

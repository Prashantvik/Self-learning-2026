# Array Reverse

arr = [8, 6, 9, 0, 1, 4]
nums = [1, 4, 3, 2, 6, 5]


def reverse_array_loop(nums):
    # Using loop just for the implementation
    n = len(nums)

    for i in range(n//2):
        temp = nums[i]
        nums[i] = nums[n - i - 1]
        nums[n - i - 1] = temp


def reverse_array(nums):
    # Use two pointers approach
    start, end = 0, len(nums) - 1

    while start <= end:
        temp = nums[start]
        nums[start] = nums[end]
        nums[end] = temp
        start += 1
        end -= 1


print(nums)
reverse_array_loop(nums)
print(nums)

print(arr)
reverse_array(arr)
print(arr)

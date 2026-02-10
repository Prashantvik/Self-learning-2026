# https://practice.geeksforgeeks.org/problems/kth-smallest-element/0
# Find the kth smallest element in the given array.
# Quick Sort : https://www.youtube.com/watch?v=7h1s2SojIRw | Abdul Bari

arr = [10, 5, 4, 3, 48, 6, 2, 33, 53, 10]
k = 4


# TC : O(nlogn) | SC : O(1)
def kth_smallest(arr, k):
    arr.sort()
    return arr[k-1]


print(kth_smallest(arr, k))


# TC : O(nlogn) | SC : O(n) | Using Hashmap
def kth_smallest_map(arr, k):
    map = {}

    for i in range(len(arr)):
        if arr[i] in map:
            map[arr[i]] += 1
        else:
            map[arr[i]] = 1

    count = 0
    for key in sorted(map.keys()):  # Sorting the keys | TC : O(nlogn)
        count += map[key]
        if count >= k:
            return key


print(kth_smallest_map(arr, k))


# Couldn't think of optimised solution from this pov
# TC : O(n^2) | SC : O(1) | Using QuickSelect Algorithm
def swap(nums, i, j):
    temp = nums[i]
    nums[i] = nums[j]
    nums[j] = temp


# A more robust Hoare partition implementation
def partition(nums, low, high):
    pivot = nums[low]
    i = low + 1
    j = high
    while True:
        while i <= j and nums[i] <= pivot:
            i += 1
        while i <= j and nums[j] >= pivot:
            j -= 1
        if i < j:
            swap(nums, i, j)
        else:
            break
    swap(nums, low, j)
    return j


def quickselect(nums, k, low, high):
    if low <= high:
        p = partition(nums, low, high)
        if p == k - 1:
            # Found the k-th smallest element
            return nums[p]
        elif p > k - 1:
            # Search the left partition
            return quickselect(nums, k, low, p - 1)
        else:
            # Search the right partition
            return quickselect(nums, k, p + 1, high)
    return None


nums = [10, 5, 4, 3, 48, 6, 2, 33, 53, 10]
k = 4

kth_smallest = quickselect(nums, k, 0, len(nums) - 1)
print(kth_smallest)
print(nums)

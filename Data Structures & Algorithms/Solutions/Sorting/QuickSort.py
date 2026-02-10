# Quick Sort Algorithm
# Algorithm : https://www.youtube.com/watch?v=7h1s2SojIRw
# Analysis  : https://youtu.be/-qOVVRIZzao?si=dFMlNV0xqsOmvTQE
"""QuickSort is a sorting algorithm based on the Divide and Conquer that picks
an element as a pivot and partitions the given array around the picked pivot
by placing the pivot in its correct position in the sorted array.

There are mainly three steps in the algorithm:
- Choose a Pivot: Select an element from the array as the pivot. The choice of
  pivot can vary (e.g., first element, last element, random element, or median)
- Partition the Array: Re arrange the array around the pivot. After
  partitioning, all elements smaller than the pivot will be on its left, and
  all elements greater than the pivot will be on its right.
- Recursively Call: Recursively apply the same process to the two partitioned
  sub-arrays.
- Base Case: The recursion stops when there is only one element left in the
  sub-array, as a single element is already sorted."""


def swap(nums, i, j):
    temp = nums[i]
    nums[i] = nums[j]
    nums[j] = temp


def partition(nums, low, high):
    # Hoare partition scheme
    pivot = nums[low]
    i = low - 1
    j = high + 1

    # Implementation of condition here | index out of range error
    while True:
        while True:
            i += 1
            if nums[i] >= pivot:
                break
        while True:
            j -= 1
            if nums[j] <= pivot:
                break

        if i < j:
            swap(nums, i, j)
        else:
            return j


def quick_sort(nums, low, high):
    if low < high:
        # p is the partitioning index
        p = partition(nums, low, high)
        # Recursively sort the two halves
        quick_sort(nums, low, p)
        quick_sort(nums, p + 1, high)


nums = [7, 10, 4, 3, 20, 15]
quick_sort(nums, 0, len(nums)-1)
print(nums)

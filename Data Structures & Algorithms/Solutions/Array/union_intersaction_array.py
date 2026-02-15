# https://www.geeksforgeeks.org/problems/union-of-two-arrays3538/1
# Union of Arrays with Duplicates
# COMPLEXITY ANALYSIS:
# TC : O(m + n) where m = len(nums1), n = len(nums2) | k <= max(m,n)
# SC : O(distinct values in both arrays)
def array_union(nums1, nums2):
    map = {}
    ans = []

    # Note : if num not in map.keys()
    # On avergae hash lookup takes O(1) time

    for num in nums1:
        if num not in map.keys():
            map[num] = 1
        else:
            map[num] += 1

    for num in nums2:
        if num not in map.keys():
            map[num] = 1
        else:
            map[num] += 1

    # TC : O(k) time where k = distinct elements in both arrays
    for key in map.keys():
        ans.append(key)

    return ans


nums1 = [1, 2, 3, 2, 1]
nums2 = [3, 2, 2, 3, 3, 2]
print(array_union(nums1, nums2))


def array_intersection(nums1, nums2):
    map1, map2 = {}, {}
    ans = []

    for num in nums1:
        if num not in map1.keys():
            map1[num] = 1
        else:
            map1[num] += 1

    for num in nums2:
        if num not in map2.keys():
            map2[num] = 1
        else:
            map2[num] += 1

    # TC : O(k1) time where k1 distinct elements in nums1
    for key in map1.keys():
        if key in map2.keys():
            ans.append(key)

    return ans  # O(1) time

# COMPLEXITY ANALYSIS FOR array_intersection:
# Time Complexity: O(m + n) where m = len(nums1), n = len(nums2)
# Space Complexity: O(distinct elements in nums1 + distinct elements in nums2)


nums1 = [1, 2, 3, 2, 1]
nums2 = [3, 2, 2, 3, 3, 2]
print(array_intersection(nums1, nums2))


# Can also be done using Sets data structure use case

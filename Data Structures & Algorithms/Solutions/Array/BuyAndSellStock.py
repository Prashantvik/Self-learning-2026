# https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/
# Reference : https://www.youtube.com/watch?v=1pkOgXD63yU

def buyandsellstock(nums):
    # Brute force approach
    profit = 0

    for i in range(len(nums)):
        buy = nums[i]
        for k in range(i+1, len(nums)):
            sell = nums[k]
            profit = max(profit, sell - buy)

    return profit


prices = [7, 1, 5, 3, 6, 4]
print(buyandsellstock(prices))
prices = [7, 6, 4, 3, 1]
print(buyandsellstock(prices))


# How does this intuition even come?
# Sliding Window Approach : We can use two pointers to keep track of the
# minimum price and the maximum profit at each step. We can iterate through
# the array and update the minimum price and maximum profit accordingly.
def buyandsellstockOptimised(nums):
    # Two Pointers Approach | One Pass
    profit = 0
    left, right = 0, 1

    while right < len(nums):
        if nums[left] < nums[right]:
            profit = max(profit, nums[right] - nums[left])
        else:
            left = right

        right += 1

    return profit


prices = [7, 1, 5, 3, 6, 4]
print(buyandsellstock(prices))
prices = [7, 6, 4, 3, 1]
print(buyandsellstock(prices))
prices = [7, 2, 1, 3, 2, 1, 5]
print(buyandsellstock(prices))

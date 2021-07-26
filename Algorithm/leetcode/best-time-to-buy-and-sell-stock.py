"""
주식을 사고팔기 가장 좋은 시점
"""
from typing import List
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_value, result = prices[0], 0
        for i in range(1, len(prices)):
            if min_value > prices[i]:
                min_value = prices[i]
            else:
                result = max(result, prices[i] - min_value)
        return result
s = Solution()
s.maxProfit([7, 1, 5, 3, 6, 4])
s.maxProfit([7, 6, 4, 3, 1])

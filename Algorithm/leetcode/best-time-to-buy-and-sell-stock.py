"""
주식을 사고팔기 가장 좋은 시점
"""
from typing import List
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min, result = prices[0], 0
        for i in range(1, len(prices)):
            if min > prices[i]:
                min = prices[i]
            else:
                result = max(result, prices[i] - min)
        return result

s = Solution()
s.maxProfit([7,1,5,3,6,4])
s.maxProfit([7,6,4,3,1])

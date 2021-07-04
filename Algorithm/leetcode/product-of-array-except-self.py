"""
자신을 제외한 배열의 곱
- 배열을 입력받아 output[i]가 자신을 제외한 나머지 모든 요소의
  곱셈 결과가 되도록 출력하라
- 나눗셈을 하지 않고, O(n)에 풀이해라.
"""
import math
from typing import List
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        result = []
        p = 1
        for i in range(0, len(nums)):
            result.append(p)
            p = p * nums[i]
        p = 1
        for i in range(len(nums) -1, 0, -1):
            result[i] = result[i] * p
            p = p * nums[i]
        return result

s = Solution()
s.productExceptSelf([-1, 1, 0, -3, 3])





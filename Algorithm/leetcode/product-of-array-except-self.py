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
        result = [1] * len(nums)
        left_value, right_value = 1, 1
        for idx in range(1, len(nums)):
            rev_idx = len(nums) - idx - 1
            left_value = left_value * nums[idx-1]
            right_value = right_value * nums[rev_idx+1]
            result[idx] *= left_value
            result[rev_idx] *= right_value
        return result

s = Solution()
s.productExceptSelf([-1, 1])

#- 책 풀이
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        out = []
        p = 1
        for i in range(0, len(nums)):
            out.append(p)
            p = p * nums[i]

        p = 1
        for i in range(len(nums)-1, -1, -1):
            out[i] = out[i] * p
            p = p * nums[i]
        return out

s = Solution()
s.productExceptSelf([1, -1])



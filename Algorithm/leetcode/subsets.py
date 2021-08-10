"""
부분 집함
- 모든 부분 집합을 리턴해라
"""
from typing import List
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def dfs(index, num_lists):
            results.append(num_lists[:])
            if index == len(nums):
                return

            for i in range(index, len(nums)):
                num_lists.append(nums[i])
                dfs(i+1, num_lists)
                num_lists.pop()

        results = []
        dfs(0, [])
        return results

s = Solution()
s.subsets([1, 2, 3])
#- brute force로 계산
from typing import List
class Solution:
    # def twoSum(self, nums: List[int], target: int) -> List[int]:
    #     for i in range(len(nums)):
    #         for j in range(i+1, len(nums)):
    #             if nums[i] + nums[j] == target:
    #                 return [i, j]

    # def twoSum(self, nums: List[int], target: int) -> List[int]:
    #     for i in range(len(nums)):
    #         complement = target - nums[i]
    #         if complement in nums[i+1:]:
    #             return [i, nums[i+1:].index(complement) + (i+1)]

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        from collections import defaultdict
        num_map = defaultdict(int)
        for i, num in enumerate(nums):
            num_map[num] = i

        for i, num in enumerate(nums):
            if num_map[target - num] and i != num_map[target - num]:
                return [i, num_map[target - num]]

s = Solution()
s.twoSum([1, 3, 4, 2], target=6)

# Given an array of integers nums and an integer target,
# return indices of the two numbers such that they add up to target.
# You may assume that each input would have exactly one solution,
# and you may not use the same element twice.
# you can return the answer in any order.
from typing import List

nums = [2, 7, 11, 15]
target = 9
nums = [3,2,4]
target = 6
nums = [3,3]
target = 6


class Solution_1:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i, _ in enumerate(nums):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]


class Solution_2:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        from collections import defaultdict
        nums_dict = defaultdict(list)
        for idx, n in enumerate(nums):
            nums_dict[n].append(idx)

        for idx, n in enumerate(nums):
            nums_dict_tmp = nums_dict
            nums_dict_tmp[n].remove(idx)
            if nums_dict_tmp[target - n]:
                return [idx, nums_dict_tmp[target - n][0]]


class Solution_3:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        nums_map = {}
        # 하나의 for 문으로 통합
        for i, num in enumerate(nums):
            if target - num in nums_map:
                return [nums_map[target - num], i]
            nums_map[num] = i


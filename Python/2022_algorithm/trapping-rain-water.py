# 높이를 입력받아 비 온 후
from typing import List
nums = [-1, 0, 1, 2, -1, -4]

tㅋ

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        three_sums = set()
        three_sums.
        for idx in range(len(nums) - 2):

            left, right = idx + 1, len(nums) - 1
            while left < right:
                if nums[idx] + nums[left] + nums[right] < 0:
                    left += 1
                elif nums[idx] + nums[left] + nums[right] > 0:
                    right -= 1
                else:
                    three_sums.append([nums[idx], nums[left], nums[right]])
                    left += 1
                    right -= 1

        return three_sums


s = Solution()
s.threeSum(nums)






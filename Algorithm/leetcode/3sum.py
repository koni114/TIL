"""
3수의 합
- 배열을 입력받아 0을 만들 수 있는 3개의 엘리먼트를 출력해라
"""
#- brute force --> error
from typing import List
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        from collections import defaultdict
        nums = sorted(nums)
        result = []
        for i in range(len(nums)-2):
            if i > 0 and nums[i] == nums[i-1]:
                continue
            for j in range(i+1, len(nums)):
                if j > i + 1 and nums[j] == nums[j-1]:
                    continue
                for k in range(j+1, len(nums)):
                    if k > j + 1 and nums[k] == nums[k-1]:
                        continue
                    if nums[i] + nums[j] + nums[k] == 0:
                        result.append([nums[i], nums[j], nums[k]])
        return result

s = Solution()
s.threeSum([-1,0,1,2,-1,-4])

from typing import List
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        for i in range(len(nums)-2):
            if i > 0 and nums[i] == nums[i-1]:
                continue
            left, right = i+1, len(nums)-1

            while left < right:
                three_sums = nums[i] + nums[left] + nums[right]
                if three_sums > 0:
                    right -= 1
                elif three_sums < 0:
                    left += 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    while left > right and nums[left] == nums[left-1]:
                        left += 1
                    while left < right and nums[right] == nums[right-1]:
                        right -= 1
                    right -= 1
                    left += 1
        return result

s = Solution()
s.threeSum([-1,0,1,2,-1,-4])
s.threeSum([-1,-1,-1,0,1,1,1])
s.threeSum([-2,0,0,2,2])
s.threeSum([-2,0,1,1,2])


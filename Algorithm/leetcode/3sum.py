"""
세 수의 합
- 배열을 입력받아 합으로 0을 만들 수 있는 3개의 엘리먼트를 출력
"""
# brute force 로 해결
from typing import List
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        for i in range(len(nums)-2):
            if i > 0 and nums[i-1] == nums[i]:
                continue
            for j in range(i + 1, len(nums)-1):
                if j > i + 1 and nums[j] == nums[j-1]:
                    continue
                for k in range(j + 1, len(nums)):
                    if k > j + 1 and nums[k] == nums[k-1]:
                        continue
                    if nums[i] + nums[j] + nums[k] == 0:
                        result.append([nums[i], nums[j], nums[k]])

        return result

s = Solution()
s.threeSum([-1, 0, 1, 2, -1, -4])

#- 투 포인터로 합 계산
class Solution(object):
    def threeSum(self, nums):
        nums.sort()
        result = []
        for i in range(len(nums)-2):
            if i >= 1 and nums[i-1] == nums[i]:
                continue
            j, k = i+1, len(nums)-1
            while j < k:
                three_sums = nums[i] + nums[j] + nums[k]
                if three_sums < 0:
                    j += 1
                elif three_sums > 0:
                    k -= 1
                else:
                    result.append([nums[i], nums[j], nums[k]])
                    j += 1
                    k -= 1
                    while j < k and nums[j-1] == nums[j]:
                        j += 1
                    while j < k and nums[k+1] == nums[k]:
                        k -= 1
        return result

s = Solution()
s.threeSum([0, 0, 0])
nums = [0, 0, 0]

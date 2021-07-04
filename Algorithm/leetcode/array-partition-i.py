from typing import List
class Solution:
    def arrayPairSum(self, nums: List[int]) -> int:
        nums.sort()
        result = 0
        for i in range(0, len(nums)-1, 2):
            result += min(nums[i], nums[i+1])
        return result

s = Solution()
s.arrayPairSum([1,4,3,2])
s.arrayPairSum([1,4])


class Solution:
    def arrayPairSum(self, nums: List[int]) -> int:
        return sum(sorted(nums)[::2])

s = Solution()
s.arrayPairSum([1,4,3,2])
s.arrayPairSum([1,4])
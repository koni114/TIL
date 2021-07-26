from typing import List
class Solution:
    def arrayPairSum(self, nums: List[int]) -> int:
        nums.sort()
        return sum(sorted(nums)[::2])


s = Solution()
s.arrayPairSum([1,4,3,2])
s.arrayPairSum([1,4])


class Solution:
    def arrayPairSum(self, nums: List[int]) -> int:
        return sum(sorted(nums)[::2])

s = Solution()
s.arrayPairSum([1, 4, 3, 2])
s.arrayPairSum([1, 4])

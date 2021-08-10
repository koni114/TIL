"""
고유한 정수의 배열 번호가
주어지면 가능한 모든 순열을 반환합니다.
어떤 순서로든 답변을 반환할 수 있습니다.

Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

Input: nums = [0,1]
Output: [[0,1],[1,0]]

Input: nums = [1]
Output: [[1]]
"""
from typing import List
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []

        def dfs(curr, rest):
            if not rest:
                result.append(curr[:])
                return

            for e in rest:
                curr.append(e)
                tmp = rest[:]
                tmp.remove(e)
                dfs(curr, tmp)
                curr.pop(e)

        dfs([], nums)
        return result

s = Solution()
s.permute([1])






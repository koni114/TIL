#- 조합의 합
#- 숫자 집합 candidates 를 조합하여 합이 target 이 되는 원소를 나열해라
#- 각 원소는 중복으로 나열 가능하다
from typing import List
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        def dfs(index, num_lists):
            if sum(num_lists) == target:
                results.append(num_lists[:])
                return
            elif sum(num_lists) > target:
                return

            for i in range(index, len(candidates)):
                num_lists.append(candidates[i])
                dfs(i, num_lists)
                num_lists.pop()

        results = []
        dfs(0, [])
        return results

s = Solution()
s.combinationSum([1], 1)
#- combinations
import itertools
from typing import List
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        def dfs(index, curr_list):
            if len(curr_list) == k:
                results.append(curr_list[:])
                return

            for i in range(index, n+1):
                curr_list.append(i)
                dfs(i + 1, curr_list)
                curr_list.pop()

        results = []
        dfs(1, [])

        return results

    def combine(self, n: int, k: int) -> List[List[int]]:
        return list(itertools.combinations(list(range(1, n+1)), k))


s = Solution()
s.combine(1, 1)
itertools.combinations(list(range(n)), k)

list(itertools.combinations(list(range(1, 5)), 2))
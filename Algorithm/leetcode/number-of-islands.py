"""
'1'(땅)과 '0'(물)의 지도를 나타내는 m x n
2D 이진 그리드가 주어지면 섬의 수를 반환합니다.
섬은 물로 둘러싸여 있으며 인접한 토지를 수평 또는 수직으로 연결하여 형성됩니다.
그리드의 네 모서리가 모두 물로 둘러싸여 있다고 가정할 수 있습니다.

Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]

Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
"""
from typing import List
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        H, W = len(grid), len(grid[0])
        island_num = 0
        ax = [1, -1, 0, 0]
        ay = [0, 0, 1, -1]
        def dfs(i, j):
            stack = [(i, j)]
            while stack:
                x, y = stack.pop()
                grid[x][y] = 0
                for i in range(4):
                    cx, cy = x + ax[i], y + ay[i]
                    if 0 <= cx <= H-1 and 0 <= cy <= W-1 and grid[cx][cy] == "1":
                        stack.append((cx, cy))

        for i in range(H):
            for j in range(W):
                if grid[i][j] == "1":
                    dfs(i, j)
                    island_num += 1

        return island_num

s = Solution()
s.numIslands([
    ["1","1","1","1","0"],
    ["1","1","0","1","0"],
    ["1","1","0","0","0"],
    ["0","0","0","0","0"]
])
"""
이진 트리의 최대 깊이 구하기
"""
# Definition for a binary tree node.
from typing import Optional
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        from collections import deque
        d = deque([root])
        depth = 0
        while d:
            depth += 1
            for _ in range(len(d)):
                cur_root = d.popleft()
                if cur_root.left:
                    d.append(cur_root.left)
                if cur_root.right:
                    d.append(cur_root.right)
        return depth





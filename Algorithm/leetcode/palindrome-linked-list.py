"""
팰린드롬 연결 리스트
- 연결 리스트가 팰린드롬 구조인지 판별해라
"""
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        from collections import deque
        q = deque()
        if not head:
            return True

        node = head

        while node is not None:
            q.append(node.val)
            node = node.next

        while len(q) > 1:
            if q.popleft() != q.pop():
                return False

        return True

s = Solution()
s.isPalindrome([1,2,2,1])



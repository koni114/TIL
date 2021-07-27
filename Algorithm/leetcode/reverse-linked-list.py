# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

#- problem 1
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        rev = None
        slow = head
        while slow:
            rev, rev.next, slow = slow, rev, slow.next
        return rev

#- problem 2
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        def reverse(node: ListNode, prev: ListNode = None):
            if not node:
                return prev
            next, node.next = node.next, prev
            return reverse(next, node)
        return reverse(head)

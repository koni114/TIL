#- 두 수의 덧셈

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1:ListNode, l2:ListNode) -> ListNode:
        first_num_list = self.toList(self.reverseList(l1))
        second_num_list = self.toList(self.reverseList(l2))

        first_num = int("".join((str(e) for e in first_num_list)))
        second_num = int("".join((str(e) for e in second_num_list)))

        return self.toReversedLinkedList(str(first_num + second_num))


    #- linkedList를 reverse 하는 함수
    def reverseList(self, head:ListNode) -> ListNode:
        node, prev = head, None

        while node:
            prev, prev.next, node = node, prev, node.next

        return prev

    #- 연결 리스트를 파이썬의 리스트로 변경
    def toList(self, node):
        list = []
        while node:
            list.append(node.val)
            node = node.next
        return list

    #- list를 linkedlist 로 변경
    def toReversedLinkedList(self, result):
        prev = None
        for r in result:
            node = ListNode(r)
            node.next = prev
            prev = node

        return node




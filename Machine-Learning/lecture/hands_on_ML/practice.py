# 역순 연결 리스트
import sys
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_linklist(head: ListNode):
    node, prev = head, None

    while node:
        next, node.next = node.next, prev
        prev, node = node, next

    return prev

# 리스트를 연결 리스트로 변경하는 코드

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def list_to_linkedlist(lists, l1:ListNode):
    prev = None
    for value in lists:
        node = ListNode(value)
        prev.next = node
        prev = node

    lists = []
    while l1:
        lists.append(l1.val)
        l1 = l1.next


# 연결 리스트를 이용해서 stack 을 구현.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Stack:
    def __init__(self):
        self.last = ListNode()

    def push(self, value):
        self.last = ListNode(value, self.last)

    def pop(self):
        item = self.last.val
        self.last = self.last.next
        return item


# tmp 를 사용하지 않고, a, b를 swap 할 수 있는 방법 ?
a, b = 10, 20
a = a + b  # a = a + b
b = a - b  # b = a
a = a - b
print(a, b)

from collections import deque

class Stack:
    def __init__(self):
        self.q = deque()


def bubble_sort(arr):
    for i in range(len(arr)):
        toggle = 0
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                toggle = 1
        if toggle == 0:
            break
    return arr

bubble_sort([1, 2, 10, 4, 5])

# 선택 정렬.


def selection_sort(arr):
    for i in range(len(arr)):
        min_num, idx = arr[i], i
        for j in range(i, len(arr)):
            if arr[j] < min_num:
                min_num, idx = arr[j], j
        arr[i], arr[idx] = min_num, arr[i]
    return arr

selection_sort([1, 4, 3, 2, 10])

# 삽입 정렬.
def insertion_sort(arr):
    for i in range(1, len(arr)):
        curr_num = arr[i]
        left = i - 1
        while left >= 0 and arr[left] > curr_num:
            arr[left + 1] = arr[left]
            arr[left] = curr_num
            left -= 1

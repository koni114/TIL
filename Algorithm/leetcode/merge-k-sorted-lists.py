"""
- K개 정렬 리스트 병합
  - k개의 정렬된 리스트를 1개의 정렬된 리스트로 병합해라
"""
import heapq
from typing import List
class ListNode:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next
class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:


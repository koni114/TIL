"""
- 원형 데크 디자인: 다음 연산을 제공하는 원형 데크를 디자인해라
  - MyCircularDeque(k): 데크 사이즈를 k로 지정하는 생성자
  - insertFront(): 데크 처음에 아이템을 추가하고 성공할 경우 true 리턴
  - insertLast(): 데크 마지막에 아이템을 추가하고 성공할 경우 true 리턴
  - deleteFront(): 데크 처음에 아이템 삭제 후 true 리턴
  - deleteLast(): 데크 마지막에 아이템을 삭제하고 성공할 경우 true 리턴
  - getFront(): 데크의 첫 번째 아이템을 가져옴. 데크가 비어 있다면 -1을 리턴
  - getRear(): 데크의 마지막 아이템을 가져옴. 데크가 비어 있다면 -1을 리턴
  - isEmpty(): 데크가 비어 있는지 여부를 판별
  - isFull(): 데크가 가득 차 있는지 여부를 판별
"""
class ListNode:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class MyCircularDeque:
    #- head, tail 은 항상 끝과 끝에 존재
    def __init__(self, k: int):
        self.head, self.tail = ListNode(None), ListNode(None)
        self.k, self.max_len = k, 0
        self.head.right, self.tail.left = self.tail, self.head

    def _add(self, node: ListNode, new: ListNode):
        n = node.right
        node.right = new
        new.left, new.right = node, n
        n.left = new

    def _del(self, node: ListNode):
        n = node.right.right
        node.right = n
        n.left = node

    def insertFront(self, value: int) -> bool:
        if self.max_len == self.k:
            return False
        self.max_len += 1
        self._add(self.head, ListNode(value))
        return True

    def insertLast(self, value: int) -> bool:
        if self.max_len == self.k:
            return False
        self.max_len += 1
        self._add(self.tail.left, ListNode(value))
        return True

    def deleteFront(self) -> bool:
        if self.max_len == 0:
            return False
        self.max_len -= 1
        self._del(self.head)
        return True

    def deleteLast(self) -> bool:
        if self.max_len == 0:
            return False
        self.max_len -= 1
        self._del(self.tail.left.left)
        return True

    def getFront(self) -> int:
        return self.head.right.val if self.max_len else -1

    def getRear(self) -> int:
        return self.tail.left.val if self.max_len else -1

    def isEmpty(self) -> bool:
        return self.max_len == 0

    def isFull(self) -> bool:
        return self.max_len == self.k




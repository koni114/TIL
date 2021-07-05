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
#- head, tail 은 항상 head, tail 이어야 함.
#- head 는 왼쪽, tail 은 오른쪽임을 기억
class ListNode():
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class CircularQueue():
    def __init__(self, k):
        self.head, self.tail = ListNode(None), ListNode(None)  #- head, tail 을 정의
        self.k, self.len = k, 0 #- 길이 정보를 담는 변수가 될 len 을 따로 정의
        #- head <-> tail 연결, right, left 로 연결
        self.head.right, self.tail.left = self.tail, self.head

    #- 새로운 노드 삽입, * 중간 삽입 한다는 가정도 들어감
    #- 기존 node.right -> new, new.left -> node,
    #-    new.right -> n, n.left -> new
    def _add(self, node: ListNode, new: ListNode):
        n = node.right
        node.right = new
        new.left, new.right = node, n
        n.left = new

    #- 입력된 node 의 우측 node 를 삭제
    def _del(self, node: ListNode):
        n = node.right.right
        node.right = n
        n.left = node

    def insertFront(self, value):
        if self.len == self.k:  #- 길이가 꽉찬 경우 추가 못함
            return False
        self.len += 1
        self._add(self.head, ListNode(value))
        return True

    def insertLast(self, value):
        if self.len == self.k:
            return False
        self.len += 1
        self._add(self.tail.left, ListNode(value))
        return True

    def deleteFronts(self):
        if self.len == 0:
            return False
        self.len -= 1
        self._del(self.head)

    def deleteLast(self):
        if self.len == 0:
            return False
        self.len -= 1
        self._del(self.tail.left.left)
        return True

    def getFront(self):
        return self.head.right.val if self.len else -1

    def getRear(self):
        return self.tail.left.val if self.len else -1

    def isEmpty(self):
        return self.len == 0

    def isFull(self):
        return self.len == self.k





"""
해시맵 디자인
- 다음의 기능을 제공하는 해시맵을 디자인해라
  - put(key, value): 키, 값을 해시맵에 삽입. 만약 이미 존재하는 키라면 업데이트함
  - get(key): 키에 해당하는 값을 조회. 만약 키가 존재하지 않는다면 -1을 리턴함
  - remove(key): 키에 해당하는 키, 값을 해시맵에서 삭제함
"""
#- 개별 체이닝 방식을 이용한 해시 테이블 구현
import collections


class ListNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.next = None

class MyHashMap:
    def __init__(self):
        self.size = 1000
        self.table = collections.defaultdict(ListNode)

    def put(self, key, value):
        index = key % self.size
        if self.table[index].value is None:
            self.table[index] = ListNode(key, value)
            return

        #- 해당 인덱스에 노드가 존재하는 경우,
        p = self.table[index]
        while p:
            if p.key == key:
                p.value = value
                return
            if p.next is None:
                break
            p = p.next

        p.next = ListNode(key, value)

    def get(self, key):
        index = key % self.size
        if self[key].value is None:
            return -1
        p = self.table[key]
        while p:
            if p.key == key:
                return p.value
            p = p.next
        return -1

    def remove(self, key):
        index = key % self.size
        if self.table[index].value is None:
            return
        #- 인덱스의 첫 번째 노드일 때 삭제처리
        p = self.table[index]
        if p.key == key:
            self.table[key] =ListNode() if p.next is None else p.next
            return

        #- 연결 리스트 노드 삭제
        prev = p
        while p:
            if p.key == key:
                prev.next = p.next
                return
            prev, p = p, p.next




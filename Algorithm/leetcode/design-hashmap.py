"""
해시맵 디자인
- 다음의 기능을 제공하는 해시맵을 디자인해라
  - put(key, value): 키, 값을 해시맵에 삽입. 만약 이미 존재하는 키라면 업데이트함
  - get(key): 키에 해당하는 값을 조회. 만약 키가 존재하지 않는다면 -1을 리턴함
  - remove(key): 키에 해당하는 키, 값을 해시맵에서 삭제함

hashMap.put(1, 1)
"""
#- 개별 체이닝 방식을 이용한 해시 테이블 구현



class ListNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.next = None


class MyHashMap:

    def __init__(self):
        import collections
        self.size = 1000  #- 기본 사이즈는 1000개로 적당히 설정
        self.table = collections.defaultdict(ListNode)

    def put(self, key: int, value: int) -> None:
        index = key % self.size  #- size 의 개수만큼 모듈로 연산을 한 나머지를 해시값으로 정하는 단순한 형태

        #- index 에 노드가 없다면, 삽입 후 종료
        if self.table[index].value is None:
            self.table[index] = ListNode(key, value)
            return

        #- 인덱스에 노드가 존재할 경우, 연결 리스트 처리
        p = self.table[index]
        while p:
            if p.key == key:
                p.value = value
                return
            if p.next is None:
                break
            p = p.next
        p.next = ListNode(key, value)

    def get(self, key: int) -> int:
        index = key % self.size
        if self.table[index].value is None:
            return -1

        p = self.table[index]
        while p:
            if p.key == key:
                return p.value
            p = p.next
        return -1

    def remove(self, key: int) -> None:
        index = key % self.size
        if self.table[index].value is None:
            return
        #- 인덱스의 첫 번째 노드일 때 삭제 처리
        p = self.table[index]
        if p.key == key:
            self.table[index] = ListNode() if p.next is None else p.next
            return

        #- 연결 리스트 노드 삭제
        prev = p
        while p:
            if p.key == key:
                prev.next = prev
                return
            prev, p = p, p.next


date_info = {'year': '2020', 'month': '01'}
new_info = {**date_info, 'day': "14"}

# Your MyHashMap object will be instantiated and called as such:
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)
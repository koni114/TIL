## 연결리스트 정리
- 각 노드가 데이터와 포인터를 가지고 한 줄로 연결되어 있는 방식으로 데이터를 저장하는 자료 구조
- 노드의 포인터가 다음이나 이전의 노드와의 연결을 담당함

~~~python
#- 노드 구현
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
~~~

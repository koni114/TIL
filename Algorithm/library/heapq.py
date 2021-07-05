"""
- 우선순위 큐로 heapq를 사용하는 방법을 알아두자
"""
#- 모듈 import
import heapq

#- 최소 힙 생성
#- heapq 모듈은 파이썬의 보통 리스트를 마치 최소 힙처럼 다룰 수 있도록 해줌
#- 내부적으로 이진 트리에 원소를 추가하는 heappush 함수는 O(logN)의 시간복잡도를 가짐
heap = []

#- 힙에 원소 추가
heapq.heappush(heap, 4)
heapq.heappush(heap, 1)
heapq.heappush(heap, 7)
heapq.heappush(heap, 3)
print(heap)

#- 힙에 원소 삭제
#- heapq 모듈의 heappop() 함수를 이용하여 힙에서 원소 삭제 가능
#- 원소를 삭제할 대상 리스트를 인자로 넘기면, 가장 작은 원소를 삭제 후 값을 리턴
print(heapq.heappop(heap))
print(heap)

#- 최소갑 삭제하지 않고 얻기
#- ** 중요한 것은 인덱스 0에 가장 작은 원소가 있다고 해서, 인덱스 1에 두번째 작은 원소,
#- 인덱스 2에 세번째 작은 원소가 있다는 보장은 없다는 것
#- 그 이유는 pop 을 이용해서 원소를 삭제할 때마다 이진 트리의 재배치를 통해 매번 새로운 최소값을 인덱스 0에
#- 위치시키기 때문
print(heap[0])

#- 기존 리스트를 힙으로 반환 --> O(N)의 복잡도를 가짐
heap = [4, 1, 7, 3, 8, 5]
heapq.heapify(heap)
print(heap)

#- 최대 힙
#- heapq 는 최소 힙(min heap) 기능만 동작하기 때문에 최대 힙(max heap)으로 활용하려면
#- 약간의 요령이 필요

#- 힙에 튜플(tuple)를 원소로 추가하거나 삭제하면, 튜플 내 맨 앞에 있는 값을 기준으로 최소 힙이 구성되는
#- 원리를 이용

#- 따라서 최대 힙을 만드려면 각 값에 대한 우선 순위를 구한 후
#- (우선순위, 값) 구조의 튜플을 힙에 추가하거나 삭제하면 됨

import heapq
nums = [4, 1, 7, 3, 8, 5]
heap = []

for num in nums:
    heapq.heappush(heap, (-num, num))

while heap:
    print(heapq.heappop(heap)[1])


"""
- 클래스를 응용한 heapq 사용 예제
"""
from heapq import heappush, heappop
import functools
@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date

    def __lt__(self, other):
        return self.due_date < other.due_date

def add_book(queue, book):
    heappush(queue, book)

queue = []
add_book(queue, Book('작은아씨들', '2020-06-05'))
add_book(queue, Book('타임 머신', '2020-05-30'))
add_book(queue, Book('돈키호테', '2020-06-07'))
add_book(queue, Book('프랑켄슈타인', '2020-06-05'))

while len(queue):
    book = heappop(queue)
    print(f"{book.title} : {book.due_date}")


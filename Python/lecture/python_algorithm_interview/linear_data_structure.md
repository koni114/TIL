## chapter07 배열
- 자료구조는 크게 메모리 공간 기반의 연속(continuous)방식과 포인터 기반의 연결(link) 방식으로 나뉨
- 배열은 이 중에서 연속 방식의 가장 기본이 되는 자료형임
- 연결 방식의 가장 기본이 되는 자료형은 '연결 리스트'임
- 추상 자료형(ADT)의 실제 구현 대부분은 배열 또는 연결 리스트를 기반으로 함  
  예를 들어 Stack은 연결 리스트로 구현하고, queue는 배열로 구현하는 식임
- 배열은 어느 위치에나 O(1)에 조회가 가능하다는 장점이 있는데, 예를 들어 배열에서 4번째 값에 접근하고 싶다면 int 배열이므로 각각 4바이트, (4-1)x4 = 12가 되고, 0x00에서 시작해 12만큼 증가한 16진수는 0x0C가 됨
- 이제 이 주소를 찾으면 해당 메모리에 배치되어 있는 값을 바로 읽어올 수 있음
- 대부분의 프로그래밍 언어는 동적 배열을 지원하며, 자바에서는 ArrayList, C++에서는 std:vector임
- 파이썬에서는 list가 바로 동적 배열 자료형임. 대부분의 동적 프로그래밍 언어들은 아예 정적 배열 자체가 없음. 파이썬도 마찬가지!
- 동적 배열의 원리는 간단한데, 미리 초깃값을 작게 잡아 배열을 생성하고, 데이터가 추가 되면서 꽉 채워지면 늘려주고 모두 복사하는 식임 
- 대개는 Double이라 하여 2배씩 늘려주게 되는데 당연히 모든 언어가 항상 그런 것은 아니며 각 언어마다 늘려가는 비율은 상이함
- 파이썬의 더블링 구조를 살펴보면 Cython의 내부 구현을 살펴보면 동적 배열인 리스트의 구현은 CPython의 `listobject.c`에 정의되어 있음
- 0, 4, 8, 16 .... 순으로 재할당하도록 정의되어 있음
- 이 재할당 비율을 Growth Factor, 즉 '성장 인자'라고 함. 파이썬의 그로스 팩터는 초반에는 2배씩 늘려 가지만, 전체적으로는 약 1.125배로 다른 언어에 비해서는 다소 조금만 늘려가는 형태로 구현되어 있음 
- 파이썬의 동적 배열 자료형인 리스트에 아이템을 삽입할 때, 동적 배열의 용량이 꽉 차게 되면 크기를 늘려나감. 더블링이 필요할 만큼 공간이 차게 되면 새로운 메모리 공간에 더 큰 크기의 배열을 할당하고 기존 데이터를 복사하는 작업이 필요하므로 O(n) 비용이 발생함
- 즉 최악의 경우 삽입 시 O(n)은 되지만 자주 일어나는 일은 아니고, 분할 상환 분석에 따른 입력 시간은 여전히 O(1)임

### 두 수의 합 문제
- 덧셈하여 타겟을 만들 수 있는 배열의 두 숫자 인덱스를 리턴해라
- 풀 수 있는 방법은 여러가지가 있음
  - brute force로 계산: O(n^2)
  - 모든 조합을 비교하지 않고, 타겟에서 첫 번째 값을 뺀 값이 target - n이 존재하는지 탐색하는 문제로 변경  
  시간 복잡도로는 O(n^2)이지만 파이썬에서 in은 매번 값을 비교하는 것에 비해 훨씬 더 빨리 샐행됨
  - 첫 번째 수를 뺀 결과 키 조회: 평균 O(1), 최악 O(n)

### 빗물 트래핑
#### 투 포인터를 최대로 이동
- 가장 높이가 높은 막대 확인. 왼쪽과 오른쪽을 가르는 장벽 역할을 함
~~~python
volume += left_max - height[left]
...
volume += right_max - right[right]
~~~
- 최대 높이의 막대까지 각각 좌우 기둥 최대 높이 left_max, right_max가 현재 높이와의 차이만큼 물 높이 volume을 더해 나감
~~~Python
if left_max <= right_max:
  volume += left_max - height[left]
  left += 1
else:
  volume += right_max - height[right]
  right -= 1
~~~
- 적어도 낮은 쪽은 그만큼 항상 채워질 것이기 때문에, 좌우 어떤 쪽이든 낮은 쪽은 높은 쪽을 향해서 포인터가 가운데로 점점 이동함
- 오른쪽이 크다면 left += 1로 왼쪽이 이동하고, 그렇지 않다면 right -= 1로 오른쪽이 이동함

### 자신을 제외한 배열의 곱
- 배열을 입력받아 output[i]가 자신을 제외한 나머지 요소의 곱셈 결과가 되도록 출력
~~~python
#- n 만에 풀 수 있는 문제
from typing import List
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        result = [1] * len(nums)
        left_value, right_value = 1, 1
        for idx in range(1, len(nums)):
            rev_idx = len(nums) - idx - 1
            left_value = left_value * nums[idx-1]
            right_value = right_value * nums[rev_idx+1]
            result[idx] *= left_value
            result[rev_idx] *= right_value
        return result
~~~

### 파이썬 최댓값과 최솟값
- 최댓값과 최솟값의 초깃값을 지정하는 방법은 여러가지가 있음
- 가장 쉬운 방법은 `sys`를 활용하는 것. 이 모듈을 사용하면 시스템이 지정할 수 있는 가장 높은 값, 낮은 값을 활용할 수 있음
~~~Python
mx = -sys.maxsize
mn = sys.maxsize
~~~
- 또는 `float()` 를 활용해 무한대 값을 지정하는 방법도 있음
~~~python
mx = -sys.maxsize
mn = sys.maxsize
~~~

## chapter08 연결 리스트
- 연결 리스트는 데이터 요소의 선형 집합으로, 데이터의 순서가 메모리에 물리적인 순서대로 저장되지는 않음
- 컴퓨터 과학에서 배열과 함께 가장 기본이 되는 대표적인 선형 자료구조 중 하나로, 다양한 추상 자료형 구현의 기반이 됨
- 동적으로 새로운 노드를 삽입, 삭제하기가 편리
- 연결 구조를 통해 물리 메모리를 연속적으로 사용하지 않아도 되기 때문에 관리도 쉬움
- 데이터를 구조체로 묶어서 포인터로 연결한다는 개념은 여러 가지 방법으로 다양하게 활용
- 실제 컴퓨터의 물리 메모리에는 구조체 각각이 그림 8-1과 같이 서로 연결된 형태로 구성되어 있음
- 메모리 어딘가에 여기저기 흩뿌려진 형상을 띔
- <b>연결 리스트는 특정 인덱스에 접근하기 위해서는 전체를 순서대로 읽어야 하므로 상수 시간 안에 접근할 수 없음. 즉 탐색에는 O(n)이 소요됨</b>
- 반면 시작, 끝 지점에 아이템을 추가하거나 삭제하는 것은 O(1)에 가능

### 팰린드롬 연결 리스트 문제의 제대로 된 풀이법 - 런너(Runner)
- 입력값이 1 -> 2 -> 3 -> 2 -> 1인 연결 리스트에 런너를 적용해 풀이하는 방법
- 런너(Runner) 방법
  - 순서에 따라 2개의 런너, 빠른 런너(Fast Runner)와 느린 런너(Slow Runner)를 각각 출발 시킴
  - 빠른 런너가 도착 할 때, 느린 런너는 중간 지점에 도착함
  - 느린 런너는 중간까지 이동하면서 역순으로 연결 리스트 rev를 만들어 나감
  - 역순으로 만든 rev와 앞으로 진행할 값과 비교하여 같은지 확인해 나가면 됨
- 코드 구현 방법
- 먼저 빠른 런너 fast와 느린 런너 slow의 초깃값은 다음과 같이 모두 head에서 시작
~~~python
slow = fast = head
~~~
- 런너를 이동할 차례인데, 다음과 같이 next가 존재하지 않을 때까지 이동
- 빠른 런너는 2 칸씩, 느린 런너 slow는 한 칸씩 이동
- 그러면서 역순으로 연결 리스트 rev를 생성하는 로직을 slow 앞에 덧붙임 
~~~python
while fast and fast.next:
  fast = fast.next.next
  rev, rev.next, slow = slow, rev, slow.next #- 역순 연결리스트 만드는 구문
~~~
- 역순 연결 리스트는 현재 값을 slow로 교체
- rev.next는 rev가 됨. 즉 앞에 계속 새로운 노드가 추가되는 형태가 됨


### 다중 할당(multiple Assignment)
- 파이썬에서 다중 할당은 2개 이상의 값을 2개 이상의 변수에 동시 할당하는 것을 말함
- 위의 런너 풀이에서 다중 할당을 사용한 바 있음
~~~python
rev, rev.next, slow = slow, rev, slow.next
~~~
- 이 코드를 보면서 의문이 들었을 수 있는데, 왜 두 줄로 분기하여 풀지 않았을까?
- 예를 들어 다음과 같이 쓸 때 분기하여 쓸 수 있음
~~~python
rev, rev.next = slow,rev
slow = slow.next
~~~
- 중요한 것은 위와 같이 두 줄로 분기하였을 때 문제가 풀리지 않는다
- 두 줄로 늘어트릴 경우는 slow와 rev가 동일한 참조가 됨
- 구문 중간에 rev = slow가 있으니 서로 같은 값을 참조하게 되는 것임
- 즉, `=` 구문이 값을 할당하는 것이 아닌 서로 같은 값을 참조하게 되는 이유는 파이썬의 모든 것은 객체며, primitive types는 존재하지 않음
- 문자와 숫자의 경우만 불변 객체라는 점만 다를 뿐이고, `=` 연산자를 활용해 할당을 진행하게 되면 값을 할당하는 것이 아니라 불변 객체에 대한 참조를 할당하게 됨
- 다음의 실험을 보고 생각해보자
~~~python
id(5)
#- 4390087440

a = 5
id(a)
#- 4390087440

b = 5
id(b)
#- 4390087440
~~~
- 5라는 숫자에 대해 숫자 5와 변수 a,b 모두 동일한 ID를 가짐
- 즉 5라는 값은 메모리 상에 단 하나만 존재하며, a,b 두 변수는 각각 이 값을 가리키는 참조라는 의미
- 그럼 만약 5가 6으로 변경된다면 같은 주소 값을 참조하므로, a,b가 모두 6으로 변경될 것 같지만 그렇지 않음
- 그 이유는 숫자는 불변(immutable) 객체이기 때문. 만약 숫자가 아니라 리스트, 딕셔너리와 같은 자료형이라면 내부 값은 바뀌며, 참조하는 모든 값도 바뀌게 됨
- 다시 돌아와서 rev = 1, slow = 2 -> 3이라고 가정해보자
~~~python
rev, rev.next, slow = slow, rev, slow.next
~~~
- <b>위의 구문은 같은 작업이 동시에 일어나기 때문에, 이 모든 작업은 중간 과정 없이 동시에 일어남. 즉 중간 과정 없이 한 번의 트랜잭션으로 끝나게 됨</b> 
- 만약 다음과 같이 썼다면 어떻게 될까? 
~~~python
#- 여기서 slow, fast 를 =로 할당하는 것은 node 자체를 할당하는 것과 같음
#- rev = 1, slow = 2 -> 3
rev, rev.next = slow, rev   #- 결과: rev = 2 -> 1, 중요한 것은 rev = slow
                            #- 동일하게 참조하기 떄문에 slow도 2 -> 1로 변해버림
slow = slow.next            #- slow.next는 1로 변경됨. 따라서 값이 이상해짐
~~~
- 결과적으로 왜 다중 할당을 하는지, 나누지 않고 한 번에 처리해야 하는지 어느 정도 이해할 수 있음

### 두 정렬 리스트의 병합
- 병합 정렬의 마지막 조합과 동일한 방식으로 첫 번째부터 비교하면서 리턴하면 쉽게 풀 수 있는 문제
~~~python
#- l1, l2를 비교했을 때 반드시 작은 값이 l1으로 오도록 비교하는 방법을 말함
class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        #- l1 이 없거나, l1, l2가 있고 l2.val < l1.val 이면 swap
        #- 즉 l1이 없거나 l1.val이 l2.val 보다 작으면 무조건 swap -> 
        if (not l1) or (l2 and l1.val > l2.val):
            l1, l2 = l2, l1
        if l1:
            l1.next = self.mergeTwoLists(l1.next, l2)
        return l1
~~~

### 리스트를 연결리스트로 변경하는 방법
~~~Python
def to_reversed_linkedlist(arr):
  prev = None
  for value in arr:
    node = ListNode(value)
    node.next = prev
    prev = node
  return prev
~~~

### 두 수의 덧셈
#### 자료형 변환으로 풀이
- 연결리스트를 뒤집은 뒤, 문자열로 이어 붙이고 숫자로 변환 후 덧셈
- 다시 연결 리스트로 변경
~~~python
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
~~~  

#### 잔가산기 구현
- 논리 회로의 전가산기(Full Adders)의 유사한 형태를 구현해보자
- 이진법이 아니라 십진법이라는 차이만 있을 뿐, 자리올림수를 구하는 것까지 가산기의 원리와 거의 동일
- 입력값 A, B, 이전의 자리올림수 이렇게 3가지 입력으로 합(Sum)과 다음 자리올림수 여부를 결정

## chapter09 스택, 큐
- 스택은 거의 모든 애플리케이션을 만들 때 사용되는 자료구조
- 파이썬은 스택 자료형을 별도로 제공하지 않지만, 리스트가 사실상 스택의 모든 연산을 지원
- 리스트는 큐의 모든 연산을 지원하지만, 동적 배열로 구현되어 있어 큐의 연산을  수행하기에는 효율적이지 않기 때문에 deque를 사용
- 스택은 다음과 같은 주요 연산을 지원하는 추상 자료형
  - `push()`: 요소에 컬렉션을 추가함
  - `pop()` : 아직 제거되지 않은 가장 최근에 삽입된 요소를 제거
- 콜 스택이라 하여 컴퓨터 프로그램의 서브루틴에 대한 정보를 저장하는 자료구조에도 널리 활용됨
- 컴파일러가 출력하는 에러도 스택처럼 맨 마지막 에러가 가장 먼저 출력되는 순서를 보임
- 스택 추상 자료형을 연결 리스트로 구현이 가능
- 연결 리스트로 스택을 구현하면 물리 메모리 상에는 순서와 상관없이 여기저기에 무작위로 배치 될 것임

### 연결 리스트를 이용한 스택 ADT 구현
~~~python
class Node:
    def __init__(self, item, next):
        self.item = item
        self.next = next


class Stack:
    def __init__(self):
        self.last = None

    def push(self, item):
        self.last = Node(item, self.last)

    def pop(self):
        item = self.last.item
        self.last = self.last.next
        return item
~~~

### 유효한 괄호
- 파이썬의 리스트는 stack 연산의 push와 pop이 O(1)에 동작하기 때문에 성능에 무리가 없음
~~~python
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        d = {")": "(",
             "]": "[",
             "}": "{"}
        for char in s:
            if char not in s:
                stack.append(char)
            elif not stack or d[char] != stack.pop():
                return False
        return len(stack) == 0
~~~

### 중복 문자 제거
- 중복된 문자를 제외하고 사전식 순서(lexicographical Order)로 나열하라
~~~python
class Solution:
    def removeDuplicateLetters(self, s: str) -> str:
        from collections import Counter
        c, stack = Counter(s), []
        stack.append(s[0])
        c[s[0]] -= 1

        for char in s[1:]:
            while stack and stack[-1] > char and c[stack[-1]] and char not in stack:
                stack.pop()
            if char not in stack:
                stack.append(char)
            c[char] -= 1
        return "".join(stack)
~~~
- 현재 문자 char가 stack[-1]보다 작은 문자이며, 뒤에 stack[-1] 문자가 존재한다면 pop
- 이미 이전에 stack에 들어와 있다면 붙이지 않음

### 일일 온도
- stack을 통해 문제풀이가 가능
~~~python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        result = [0] * len(temperatures)
        stack = [0]

        for idx, value in enumerate(temperatures[1:], 1):
            while stack and temperatures[stack[-1]] < value:
                tmp_idx = stack.pop()
                result[tmp_idx] = idx - tmp_idx
            stack.append(idx)

        return result
~~~

### 큐
- 시퀀스의 한쪽 끝에는 엔티티를 추가하고, 다른 반대쪽에는 제거할 수 있는 엔티티 컬렉션(FIFO)
- BFS나 캐시 등을 구현할 때도 널리 사용됨
- 파이썬에서는 동일한 이름의 queue라는 모듈이 있기는 하지만 이 모듈은 사실상 자료구조로서의 큐보다는 동기화 기능에 집중된 모듈로, 큐 자료형을 위해 널리 쓰이는 모듈은 아님
- 파이썬의 리스트보다는 deque를 사용하는 것이 가장 좋음

### 큐 <-> 스택 구현하기
- 스택으로 큐를 구현하거나 큐로 스택을 구현하려면 큐로 스택을 구현하는 것은 큐 1개로, 스택으로 큐를 구현하는 것은 2개로 가능
- 다음의 코드를 참조하자
~~~Python
#- 스택을 사용한 큐 구현
 def push(self, x: int) -> None:
        for _ in range(len(self.input)):
            self.output.append(self.input.pop())
        self.output.append(x)
        for _ in range(len(self.output)):
            self.input.append(self.output.pop())

#- 큐를 사용한 스택 구현
 def push(self, x: int) -> None:
        self.q.append(x)
        for _ in range(len(self.q)-1):
            self.q.append(self.q.popleft())
~~~

### 원형 큐 디자인
- 원형 큐(Circular Queue)는 FIFO 구조를 지닌다는 점에서 기존 큐와 동일하며, 그러나 마지막 위치가 시작 위치와 연결되는 원형 구조를 띠기 때문에 Ring Buffer라고도 부름
- 기존의 큐는 공간이 꽉차게 되면 더 이상 요소를 추가할 수 없었음. 심지어 앞쪽에 요소들이 deQueue()로 모두 빠져 충분한 공간이 남게 돼도 그쪽으로는 추가할 수 있는 방법이 없음
- 그래서 앞쪽에 공간이 남아 있다면 이 그림처럼 동그랗게 연결해 앞쪽을 추가할 수 있도록 재활용 가능한 구조가 바로 원형 큐임
- front와 rear가 있는데, `enQueue(10)`을 하면 rear 위치에 10을 추가하며, `deQueue()` 하면 front 위치의 값이 삭제됨
- 동작하는 원리도 투 포인터와 비슷함. 마지막 위치와 시작 위치를 연결하는 원형 구조를 만들고, 요소의 시작점과 끝점을 따라 투 포인터가 움직임
- `enQueue()`를 하게 되면 rear 포인터가 앞으로 이동하며, `deQueue()`를 하게 되면 front 포인터가 앞으로 이동함
- 만약 rear 포인터가 front 포인터와 같은 위치에서 서로 만나게 된다면, 여유공간이 하나도 없다는 얘기가 되므로 공간 부족 에러를 발생시킴
- 다음은 원형 큐 디자인의 구현 
~~~python
class MyCircularQueue:

    def __init__(self, k: int):
        self.q = [None] * k
        self.maxlen = k
        self.p1 = 0     #- front
        self.p2 = 0     #- rear

    def enQueue(self, value: int) -> bool:
        if self.q[self.p2] is None:
            self.q[self.p2] = value
            self.p2 = (self.p2 + 1) % self.maxlen
            return True
        else:
            return False

    def deQueue(self) -> bool:
        if self.q[self.p1] is None:
            return False
        else:
            self.q[self.p1] = None
            self.p1 = (self.p1 + 1) % self.maxlen
            return True

    def Front(self) -> int:
        return -1 if self.q[self.p1 - 1] is None else self.q[self.p1]

    def Rear(self) -> int:
        return -1 if self.q[self.p2 - 1] is None else self.q[self.p2]

    def isEmpty(self) -> bool:
        return self.p1 == self.p2 and self.q[self.p1] is None

    def isFull(self) -> bool:
        return self.p1 == self.p2 and self.q[self.p1] is not None
~~~

## chapter10 데크, 우선순위 큐
- 스택과 큐의 연산을 모두 갖고 있는 복합 자료형인 데크와 추출 순서가 일정하게 정해져 있지 않은 우선순위 큐
  
### 데크
- 데크는 Double Ended Queue의 줄임말로, 글자 그대로 양쪽 끝을 모두 추출할 수 있는 큐를 일반화한 형태의 추상 자료형(ADT)임
- 데크는 양쪽에서 삭제와 삽입을 모두 처리할 수 있으며, 스택과 큐의 특징을 모두 갖고 있음
- 이 추상 자료형의 구현은 배열이나 연결 리스트 모두 가능하지만, 특별히 다음과 같이 이중 연결 리스트(Doubly Linked List)로 구현하는 편이 잘 어울림 
- 이중 연결 리스트로 구현하게 되면, 양쪽으로 head와 tail이라는 이름의 두 포인터를 갖고 있다가 새로운 아이템이 추가될 때마다 앞쪽 또는 뒤쪽으로 연결시켜 주기만 하면 됨
- 연결 후에는 포인터를 이동하면 됨
- 파이썬에서는 `collections.deque`로 지원하는데, 이 또한 이중 연결 리스트로 구현되어 있음
- CPython 에서는 고정 길이 하위 배열을 지닌 이중 연결 리스트로 구현되어 있음 
- 이중 연결 리스트를 이용해 deque 자료형을 직접 구현하는 문제를 풀어보자

### 원형 데크 디자인
- 다음 연산을 제공하는 원형 데크를 디자인해라
  - `MyCircularDeque(k)` : 데크 사이즈를 k로 지정
  - `insertFront()`: 데크 처음에 아이템 추가. 성공 후 True return
  - `insertLast()`: 데크 마지막에 아이템을 추가하고 성공할 경우 true 리턴
  - `deleteFront()`: 데크 처음에 아이템 삭제 후 true 리턴
  - `deleteLast()`: 데크 마지막에 아이템을 삭제하고 성공할 경우 true 리턴
  - `getFront()`: 데크의 첫 번째 아이템을 가져옴. 데크가 비어 있다면 -1을 리턴
  - `getRear()`: 데크의 마지막 아이템을 가져옴. 데크가 비어 있다면 -1을 리턴
  - `isEmpty()`: 데크가 비어 있는지 여부를 판별
  - `isFull()`: 데크가 가득 차 있는지 여부를 판별
- 앞서 원형 큐를 배열로 구현해 보았는데, 데크는 `insertFront`와 같이 앞 쪽에 insert를 하는 부분도 존재하므로, 해당 함수 수행시 O(n)의 시간 복잡도가 걸리므로, 이중 연결 리스트로 구현해보자 
- 먼저 초기화 함수를 정의한다
~~~python

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
~~~

### 우선순위 큐
- 큐와 스택과 같은 ADT와 유사하지만 추가로 각 요소의 '우선순위'와 연관되어 있음
- 우선순위 큐는 어떤 특정 조건에 따라 우선순위가 가장 높은 요소가 추출되는 자료형
- 예를들어 최대값 추출이라고 하면 입력 -> [1, 4, 5, 3, 2] 일 때 자동으로 [5, 4, 3, 2, 1] 순으로 추출됨
- 이는 정렬 알고리즘을 사용하면 우선순위 큐를 만들 수 있다는 의미인데, n개의 요소를 정렬하는데 S(n)의 시간이 든다고 할 때, 새 요소를 삽입하거나 요소를 삭제하는 데는 O(S(n))의 시간이 걸림
- 반면 내림차순으로 정렬했을 때 최댓값을 가져오는 데는 맨 앞의 값을 가져오기만 하면 되므로 O(1)로 가능
- 대개 정렬에는 O(nlogn)이 필요하기 때문에 O(S(n))은 O(nlogn) 정도가 듬
- 실제로는 이처럼 단순 정렬보다는 힙 정렬 등의 효율적인 방법을 사용함
- 이외에도 최단 경로를 탐색하는 다익스트라(Dijkstra) 알고리즘 등에 사용되며 힙(Heap) 자료구조와도 관련이 깊음

### k개 정렬 리스트 병합
- 우선순위 큐를 사용해 풀 수 있는 문제
- 우선순위 큐 풀이에 거의 항상 `heapq` 모듈을 사용하므로 잘 파악해두자
~~~python
for lst in lists:
    headq.heappush(heap, (lst.val, lst))
~~~
- lists는 3개의 연결 리스트인 [[1, 4, 5], [1, 3 ,4], [2, 6]]로 구성된 입력값이며, 이 코드는 각 연결 리스트의 루트를 힙에 저장함
- 파이썬의 heapq는 최소 힙을 지원하며, `lst.val`이 작은 순서대로 pop()할 수 있음
- 하지만 이렇게 저장하면 다음과 같은 에러 발생  
  `TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'`  
  이는 중복된 값을 넣을 수 없다는 의미
- 따라서 의미는 없지만 중복 값 처리를 하기 위해 두번째 값에 적절한 값을 삽입 해야 함
~~~python
for i in range(len(lists)):
    ...
    heapq.heappush(heap, (lists[i].val, i, lists[i]))
~~~
- 이제 `heappop()`으로 값을 추출하면 가장 작은 노드의 연결 리스트부터 차례대로 나오게 됨
- 이 값을 결과 노드에 차례대로 나오게 되며 result에 하나씩 추가함
- 또한 k개의 연결 리스트가 모두 힙에 계속 들어 있어야 그중에서 가장 작은 노드가 항상 차례대로 나올 수 있으므로, 추출한 연결 리스트의 그다음 노드는 다음과 같이 다시 힙에 추가함
~~~python
while heap:
    node = heapq.heappop(heap)
    idx = node[1]
    result.next = node[2]

    result = result.next
    if result.next:
        heapq.heappush(heap, (results.next.val, idx, result.next))
~~~

### PriorityQueue vs heapq
- 파이썬에서 우선순위 큐는 queue 모듈의 PriorityQueue 클래스를 이용해 사용할 수 있음
- 우선순위 큐는 힙을 주로 사용해 구현하며, 파이썬의 PriorityQueue 조차 내부적으로는 heapq를 사용하도록 구현되어 있음
- CPython에서 PriorityQueue 클래스는 파이썬 코드로 다음과 같이 선언되어 있음
~~~python
# cpython/Lib/queue.py
class PriorityQueue(Queue):
    ...
    def _put(self, item):
        heappush(self.queue, item)

    def _get(self):
        return heappop(self.queue)
~~~
- 그렇다면, heapq와 PriorityQueue와의 차이점은 무엇일까?  
- <b>차이점은 여기에 스레드 세이프 클래스라는 점이며, heapq 모듈은 스레드 세이프를 보장하지 않음</b>
- 파이썬은 GIL의 특성상 멀티 스레딩이 거의 의미가 없기 때문에 대부분 멀티 프로세싱을 활용하는데, PriorityQueue 모듈의 멀티 스레딩 지원은 사실 큰 의미는 없음
- 또한 스레드 세이프를 보장한다는 얘기는 락킹을 제공한다는 의미이므로 락킹 오버헤드가 발생해 성능에 영향을 미침
- 따라서 굳이 멀티 스레드로 구현할 게 아니라면 PriorityQueue는 사용할 이유가 없음
- 따라서 실무에서도 큐는 대부분 heapq로 구현하고 있음

### 파이썬 전역 인터프리터 락(GIL)
- 아마 '파이썬은 왜 느린가?'를 얘기할 때 가장 자주 듣게되는 얘기가 GIL임
- 파이썬 공식 구현체인 CPython은 개발 초기에 번거로운 동시성 관리를 편하게 하고 스레드 세이프하지 않는 CPython의 메모리 관리를 쉽게 하기 위해, GIL로  파이썬 객체에 대한 접근을 제한하는 형태로 설계함 
- <b>GIL은 global interpreter lock의 약자로서 하나의 스레드가 자원을 독점하는 형태로 실행됨</b>  
- 1994년에 파이썬이 처음 개발되었으니, 그 때 당시에는 충분히 그런 선택을 할 만 했고 GIL 디자인에는 큰 문제가 없었음  
- 하지만 현재처럼 멀티 코어가 당연한 세상에서, 하나의 스레드가 자원을 독점하는 형태로 실행되는 제약은 매우 치명적  
- 최근들어 GIL을 걷어내려고 하는 시도를 하고 있지만, 제약을 극복하기가 쉽지 않음   

## chapter11 해시 테이블
- 해시 테이블 또는 해시 맵은 키를 값에 매핑할 수 있는 구조인, 연관 배열 추상 자료형(ADT)을 구현하는 자료구조
- 해시 테이블의 가장 큰 특징은 대부분의 연산이 시간 복잡도가 O(1)이 라는 점

### 해시
- 해시 함수란 임의 크기 데이터를 고정 크기 값으로 매핑하는 데 사용할 수 있는 함수를 말함 
- 해시 테이블의 핵심은 해시 함수임. 입력값은 AB, 1234BC, AF32B로 각각 3글자, 6글자, 5글자이지만, 화살표로 표시한 특정 함수를 통과하면 2바이트의 고정 크기 값으로 매핑됨
- 여기서 화살표 역할을 하는 함수가 바로 해시 함수
~~~python
ABC    -> A1
1234BC -> CB
AF32B  -> D5
~~~
- <b>해시 테이블을 인덱싱하기 위해 해시 함수를 사용하는 것을 해싱(Hashing)이라 하며, 해싱은 정보를 가능한 한 빠르게 저장하고 검색하기 위해 사용하는 중요한 기법 중 하나임</b>
- 해싱은 최적의 검색이 필요한 분야에 사용되며, 심볼 테이블 등의 자료구조를 구현하기에도 적합함
- 이외에도 해시 함수는 checksum, 손실 압축, 무작위화 함수(Randomization), 암호 등과도 관련이 깊으며 때로는 서로 혼용되기도 함
- 어느 정도 개념이 겹치기는 하지만, 서로 용도와 요구사항이 다른 만큼 각각 다르게 설계되고 최적화됨
- 성능 좋은 해시 함수들의 특징은 다음과 같음
 - 해시 함수 값 충돌의 최소화
 - 쉽고 빠른 연산
 - 해시 테이블 전체에 해시 값이 균일하게 분포
 - 사용할 키의 모든 정보를 이용하여 해싱
 - 해시 테이블 사용 효율이 높을 것

### birthday problem
- 충돌은 생각보다 쉽게 일어나는데, 흔한 예로 birthday problem를 예로 들 수 있음
- 생일의 가지수는 365개이므로, 여러 사람이 모였을 때 생일이 같은 2명이 존재할 확률을 얼핏 생각해보면 366명이 넘어야 할 것 같지만, 23명만 넘어도 50%가 넘고, 57명부터는 99%가 넘음
- 다음의 코드를 작성해서 직접 실험해보자
~~~python
import random
TRIALS = 100000    #- 10만번 실험
same_birthdays = 0 #- 생일이 같은 실험의 수

#- 10만 번 실험 진행
for _ in range(TRIALS):
    birthdays = []
    for i in range(23):
        birthday = random.randint(1, 365)
        if birthday in birthdays:
            same_birthdays += 1
            break
        birthdays.append(birthday)

print(f"{same_birthdays / TRIALS * 100}%")
~~~

### 비둘기집 원리
- n개의 아이템을 m개에 넣을 때, n > m 이라면 적어도 하나의 컨테이너에는 반드시 2개 이상의 아이템이 들어가 있다는 원리를 말함
- 왜 충돌이 일어날 수 밖에 없을까를 비둘기집 원리가 잘 설명함
- 결과적으로는 충돌을 최소화 하는 것이 중요

### 로드 팩터
- 해시 테이블에 저장된 데이터 개수 n을 버킷의 개수 k로 나눈 것
- 로드 펙터 비율에 따라서 해시 함수를 재작성해야 될지, 해시 테이블의 크기를 조정해야 할지를 결정함
- 이 값은 해시 함수가 키들을 잘 분산해 주는지를 말하는 효율성 측정에도 사용됨
- 자바 10에서는 해시맵 디폴트 로드 펙터를 0.75로 정했으며, 로드 펙터가 증가할 수록 해시 테이블의 성능은 점점 떨어지며 자바 10의 경우 0.75를 넘어설 경우 동적 배열처럼 해시 테이블의 공간을 재할당함

### 해시 함수
- 해시 테이블을 인덱싱 하기 위해 해시 함수를 사용하는 것을 해싱이라고 함
- 해싱에는 다양한 알고리즘이 있으며, 최상의 분포를 제공하는 방법은 데이터에 따라 제각각임
- 여러 알고리즘 중, 가장 단순하면서도 널리 쓰이는 정수형 해싱 기법인 모듈로 연산을 이용한 나눗셈 방식 하나만 살펴봄
- 식은 다음과 같음: `h(x) = x mod m`
- 여기서 h(x)는 입력값 x의 해시 함수를 통해 생성된 결과임
- m은 해시 테이블의 크기로, 일반적으로 2의 멱수에 가깝지 않은 소수를 택하는 것이 좋음
- 매우 단순한 방법이지만 실무에서는 많은 키 세트가 충분히 랜덤한 상태고, 키 세트가 어떤 큰 소수에 의해 순환 구조가 될 확률은 낮기 때문에 실제로는 잘 동작함
- x는 어떤 간단한 규칙에 의해 만들어낸 충분히 랜덤한 상태의 키 값
- 조슈아 블로크(effective java의 저자)는 자바를 설계할 때, 값 x를 다음과 같이 다항식의 결과로 정의
- `P(x) = s[0]* x^(n-1) + s[1]*x^(n-2) + ... + s[n-1]`
- x는 31로 하는 거듭제곱 P(31)의 연산으로 정의했다고 밝힌 바 있음
- 31을 매직 넘버로 택했다고 함!
- 더욱 복잡한 함수를 적용 할수도 있었겠지만, 간단한 형태가 성능과 충돌의 적절한 합의점
- 이처럼 해시 함수는 매우 중요한 역할을 하는데, 몇 년전 구글은 함수를 딥러닝으로 학습한 모델을 적용해 충돌을 최소화하는 논문을 발표하며, 해시 테이블 자료구조의 미래를 기대케 하기도 함

### 충돌
- 아무리 좋은 해시 함수라도 충돌은 발생하게 됨. 이런 해시 함수 결과 값 충돌이 발생하는 경우 어떻게 처리하는지 살펴보자

#### 개별 체이닝
- 먼저 다음과 같이 해싱에 의한 해시를 나타내며, 서현과 윤아를 해싱한 결과가 2로 충돌한다고 가정해보자
~~~
키    값  해시  충돌여부  개별 체이닝
윤아  15   2    충돌
유리  47   1    
서현  17   2    충돌    윤아 15 -> 서현 17
수영  7    4
~~~
- <b>해시 테이블의 기본 방식이기도 한 개별 체이닝은 충돌 발생 시 그림과 같이 연결 리스트로 연결하는 방식</b>
- 충돌이 발생한 윤아와 서현은 '윤아'의 다음 아이템이 '서현'인 형태로 서로 연결 리스트로 연결됨
- 기본적인 자료구조와 임의로 정한 알고리즘만 있으면 되므로, 인기가 높음
- 원래 해시 테이블 구조의 원형이기도 하며 가장 전통적인 방식으로, 흔히 해시 테이블이라고 하면 바로 이 방식을 말함
  - 키의 해시 값을 계산
  - 해시 값을 이용해 배열의 인덱스를 구함
  - 인덱스가 동일한 경우 연결 리스트로 연결 
- 잘 구현한 경우는 최선은 O(1)이며, 모든 해시 충돌이 발생했다고 가정할 경우 O(n)이 됨
- 연결 리스트 구조를 좀 더 최적화해서 레드-블랙 트리에 저장하는 형태로 병행해 사용하기도 함

#### 오픈 어드레싱
- 충돌 발생 시 탐사를 통해 빈 공간을 찾아나서는 방식
- 무한정 저장할 수 있는 개별 체이닝 방식과는 달리, 전체 슬롯 이상은 저장할 수 없음
- 충돌이 일어나면 테이블 공간 내에서 탐사를 통해 빈 공간을 찾아 해결하며, 이 때문에 개별 체이닝 방식과는 달리 모든 원소가 반드시 자신의 해시값과 일치하는 주소에 저장된다는 보장은 없음
- 앞서 보았던 키 값(소녀시대)을 입력 값으로 했을 때, 오픈 어드레싱으로 표현하면 다음과 같음
~~~
키    해시  주소 번호     값  
윤아   2      2      유리 47
유리   1      1      윤아 15
서현   2      3      서현 17
      
수영   4      4      수영  7
~~~
- 오픈 어드레싱 방식 중에서 가장 간단한 방식인 선형 탐사(Linear Probing) 방식은 충돌이 발생할 경우 해당 위치부터 순차적으로 탐사를 하나씩 진행함
- 특정 위치가 있으면, 그 다음 위치를 탐사하는 식
- 이렇게 순차적으로 탐사하다가 비어 있는 공간을 발견하면 삽입하게 됨
- 이처럼 선형 탐사 방식은 구현 방법이 간단하면서도, 성능이 좋은 편
- 한 가지 문제점은 해시 테이블에 저장되는 데이터들이 고르게 분포되지 않고 뭉치는 경향이 있다는 점
- 해시 테이블 여기저기에 연속된 데이터 그룹이 생기는 현상을 클러스터링이라고 하는데, 클러스터들이 점점 커지게 되면 인근 클러스터들과 서로 합쳐지는 일이 발생함
- 이런 클러스터링 현상은 탐사 시간을 오래 걸리게 하며, 전체적으로 해싱 효율을 감소시킴
- 오픈 어드레싱 방식은 데이터의 수가 버킷 사이즈 수보다 큰 경우에는 삽입이 안됨
- 따라서 일정 이상 채워지면, 기준이 되는 로드 펙터 비율을 넘어서게 되면 그로스 팩터의 비율에 따라 더 큰 크기의 또 다른 버킷을 생성한 후 여기에 새롭게 복사하는 리해싱(Rehasing) 작업이 일어남. 더블링 개념과 유사

### 언어별 해시 테이블 구현 방식
- 리스트와 함께 파이썬에서 가장 많이 사용되는 자료형인 딕셔너리는 해시 테이블로 구현되어 있음
- 해시 테이블로 구현한 파이썬의 자료형은? --> 딕셔너리
- 파이썬의 해시 테이블은 오픈 어드레싱 방식을 사용함. 체이닝 방식을 사용하지 않은 이유는 해시 충돌 값을 연결 리스트로 저장시에 메모리 할당 오버헤드가 발생해서 사용하지 않았다고 말함
- 보통 오픈 어드레싱과 체이닝 방식과 비교했을 때, 로드 펙터가 0.8정도 이하에서는 오픈 어드레싱이 성능이 좋으며, 0.8 이상에서는 체이닝이 좋음
- 최근 루비나 파이썬 같은 Modern 언어들은 오픈 어드레싱 방식을 택해 성능을 높히는 대신 로드 팩터를 작게 잡아 성능 저하 문제를 해결함
- 파이썬의 로드 팩터는 0.66으로 자바보다 작음


### 해시맵 디자인
~~~python
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
~~~

### zip 함수
- 2개 이상의 시퀀스를 짧은 길이를 기준으로 일대일 대응하는 새로운 튜플 시퀀스를 만드는 역할을 수행
- 파이썬 2에서는 zip()의 결과가 바로 리스트가 되는데, 3+에서는 제너레이터를 리턴
- zip의 결과 자체는 리스트 시퀀스가 아닌 튜플 시퀀스를 만들기 때문에 값을 변경하는 것이 불가능함

### 아스테리스크
- zip()의 파라미터는 1개가 될 수도 있고, 2개, 10개가 될 수도 있음
- 어떻게 하면 이렇게 할 수 있을까? 여기에는 아스테리스크(Asterisk) 혹은 별표를 활용함
- 파이썬에서는 포인터가 존재하지 않음. *는 언팩(unpack) 연산자임
- 시퀀스 언패킹 연산자로 말 그대로 시퀀스를 풀어헤치는 연산자를 뜻하며, 주로 튜플이나 리스트를 언패킹하는 데 사용
- 함수의 파라미터에서는 패킹, 밖에서는 언패킹
- `*` 한 개는 튜플 또는 리스트 등의 시퀀스 언패킹, `**` 2개는 다음과 같이 키/값 페어를 언패킹하는 데 사용됨

## 용어 설명
- 스레드 세이프(thread safe): 멀티 스레드에도 안전한 프로그래밍 개념. 만약 thread safe하지 않는다면 1번 스레드 값이 2번 스레드에서 변경될 수 있어 문제 발생

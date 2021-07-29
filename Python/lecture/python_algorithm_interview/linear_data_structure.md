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

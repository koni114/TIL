"""
- 큐를 이용해 다음 연산을 지원하는 스택을 구현
  - push(x):
  - pop()
  - top()
  - empty()
"""
class MyStack:

    def __init__(self):
        from collections import deque
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        for _ in range(len(self.q)-1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return len(self.q) == 0

obj = MyStack()
obj.push(1)
obj.push(2)
param_2 = obj.pop()
param_3 = obj.top()
param_4 = obj.empty()
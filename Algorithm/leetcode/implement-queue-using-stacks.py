"""
스택을 이용해 다음 연산을 지원하는 큐를 구현
- push(x):
- pop()
- peek()
- empty()
"""
class MyQueue:
    def __init__(self):
        self.input = []
        self.output = []

    def push(self, x: int) -> None:
        for _ in range(len(self.input)):
            self.output.append(self.input.pop())
        self.output.append(x)
        for _ in range(len(self.output)):
            self.input.append(self.output.pop())

    def pop(self) -> int:
        return self.input.pop()

    def peek(self) -> int:
        return self.input[len(self.input)-1]

    def empty(self) -> bool:
        return len(self.input) == 0



obj = MyQueue()
obj.push(1)
obj.push(2)
param_2 = obj.pop()
param_3 = obj.peek()
param_4 = obj.empty()
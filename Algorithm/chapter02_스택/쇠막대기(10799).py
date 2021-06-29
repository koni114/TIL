"""
쇠막대기(10799)
"""
import sys
from collections import deque
inf = sys.stdin
bar = deque(list(inf.readline().strip()))
stack = deque()
result_value = 0
for i, value in enumerate(bar):
    if value == '(':
        stack.append(value)
    else:
        if bar[i-1] == '(':
            result_value += len(stack) - 1
            stack.pop()
        else:
            result_value += 1
            stack.pop()
print(result_value)

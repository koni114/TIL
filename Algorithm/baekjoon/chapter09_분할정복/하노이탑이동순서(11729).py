import sys
from collections import deque
inf = sys.stdin
K = int(inf.readline().strip())  #- 원판의 개수
d = deque()
def hanoi(start, end, size):
    mid = 6 - start - end
    if size == 2:
        d.appendleft([start, mid])
        d.appendleft([start, end])
        d.appendleft([mid, end])
    else:
        hanoi(start, mid, size-1)
        d.appendleft([start, end])
        hanoi(mid, end, size-1)
if K == 1:
    print("1")
    print("1 3")
else:
    hanoi(1, 3, K)
    print(len(d))
    while d:
        start, target = d.pop()
        print(start, target)

"""
괄호(9012번)
"""
import sys
from collections import deque
inf = sys.stdin
n = int(inf.readline().strip())
d = deque([])

for _ in range(n):
    check = deque()
    next_step = False
    d = deque(list(inf.readline().strip()))
    # print(d)
    while len(d) >= 1:
        value = d.popleft()
        if value == '(':
            check.append(0)
        else:
            if len(check) < 1:
                print("NO")
                next_step = True
                break
            else:
                check.pop()

    if not next_step:
        if len(check) >= 1:
            print("NO")
        else:
            print("YES")




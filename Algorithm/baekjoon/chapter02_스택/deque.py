from collections import deque
d = deque([1, 2, 3, 4, 5])
d.append(10)
print(d)

d.appendleft(10)
print(d)

d.popleft()
print(d)

d.pop()
print(d)

d.rotate(-2)
d.rotate(2)

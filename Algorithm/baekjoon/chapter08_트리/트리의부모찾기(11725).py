"""
트리의 부모 찾기
- 루트 없는 트리가 주어짐
- 트리의 루트를 1이라고 정했을 때, 각 노드의 부모를 구하는 프로그램을 작성하시오
"""
import sys
from collections import deque
inf = sys.stdin
N = int(inf.readline().strip())
tree = [deque() for _ in range(N+1)]
check = [0 for _ in range(N+1)]
parent = [0 for _ in range(N+1)]

for _ in range(N-1):
    node1, node2 = [int(i) for i in inf.readline().strip().split()]
    tree[node1].append(node2)
    tree[node2].append(node1)

check[1] = 1
queue = deque([1])

while len(queue):
    now = queue.pop()
    for next in tree[now]:
        if not check[next]:
            check[next] = 1
            parent[next] = now
            queue.appendleft(next)

for i, value in enumerate(parent[2:]):
    print(value)
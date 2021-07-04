"""
- 트리가 입력으로 주어짐
- 트리의 지름이란, 트리에서 임의의 두 점 사이의 거리 중 가장 긴 것을 말함
- 트리가 입력으로 주어짐. 첫 번째 줄에서는 트리의 정점의 개수 V가 주어짐
- 두 번째 줄부터 V개의 줄에 걸쳐 간선의 정보가 주어짐
"""
import sys
from collections import deque
def bfs(start, check):
    queue = deque()
    final_result = 0
    final_node = 0
    check[start] = 1
    queue.appendleft([start, 0])

    while len(queue):
        now, result = queue.pop()
        for next, depth in tree[now]:
            if not check[next]:
                tmp_depth = result + depth
                check[next] = 1
                queue.appendleft([next, tmp_depth])
                if final_result < tmp_depth:
                    final_result = tmp_depth
                    final_node = next

    return final_node, final_result

inf = sys.stdin
V = int(inf.readline().strip())
tree = [deque() for _ in range(V+1)]
for _ in range(V):
    tmp = [int(i) for i in inf.readline().strip().split()][:-1]
    for i in range(1, len(tmp), 2):
        tree[tmp[0]].append([tmp[i], tmp[i+1]])

check1 = [0 for _ in range(V+1)]
start_node = bfs(1, check1)[0]
check2 = [0 for _ in range(V+1)]
print(bfs(start_node, check2)[1])
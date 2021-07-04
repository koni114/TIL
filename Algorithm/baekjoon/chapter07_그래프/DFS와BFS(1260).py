"""
DFS와 BFS(1260)
- 그래프를 DFS 로 탐색한 결과와 BFS 로 탐색한 결과를 출력하는 프로그램을 작성하시오.
- 단, 방문할 수 있는 정점이 여러 개인 경우에는 정점 번호가 작은 것을 먼저 방문
- 더 이상 방문할 수 있는 점이 없는 경우 종료. 정점 번호는 1번 부터 N번 까지임

- 정점의 개수 1 <= N <= 1000
- 간선의 개수 1 <= M <= 10,000
- 탐색을 시작할 정점의 번호 V가 주어짐
"""
import sys
from collections import deque
inf = sys.stdin
node_size, edge_size, start_node = [int(i) for i in inf.readline().strip().split()]
node = [[] for _ in range(node_size+1)]


#- dfs
def dfs(node, start_node):
    path = deque()
    check = [0 for _ in enumerate(node)]

    def dfs_check(x):
        check[x] = 1
        path.append(str(x))
        for next_node in node[x]:
            if not check[next_node]:
                dfs_check(next_node)

    dfs_check(start_node)
    print(" ".join(path).strip())

#- bfs
def bfs(node, start_node):
    queue = deque()
    path = deque()
    check = [0 for _ in enumerate(node)]
    queue.appendleft(start_node)
    check[start_node] = 1

    while len(queue):
        curr_node = queue.pop()
        path.append(str(curr_node))
        for next_node in node[curr_node]:
            if not check[next_node]:
                queue.appendleft(next_node)
                check[next_node] = 1

    print(" ".join(path).strip())


for _ in range(edge_size):
    node1, node2 = [int(i) for i in inf.readline().strip().split()]
    node[node1].append(node2)
    node[node2].append(node1)

for i, edge in enumerate(node):
    node[i] = sorted(edge)

dfs(node, start_node)
bfs(node, start_node)

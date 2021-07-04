"""
NxM 크기의 배열로 표현되는 미로가 있음
- 미로에서 1은 이동할 수 있는 칸을 나타냄
- 0은 이동할 수 없는 칸을 나타냄
- (1, 1)에서 출발하여, (N, M)의 위치로 이동할 때 지나야 하는 최소의 칸 수 계산

- 첫째 줄에 두 정수 N,M(2 <= N, M < 100)이 주어짐
- 다음 N개의 줄에는 M개의 정수로 미로가 주어짐
- 각각의 수들은 붙어서 입력으로 주어짐
"""
#- 값 입력 부분
import sys
from collections import deque
inf = sys.stdin
N, M = map(int, inf.readline().strip().split())
check = [[0 for _ in range(M)] for _ in range(N)]
puzzle = deque()
for _ in range(N):
    d = deque([int(i) for i in list(inf.readline().strip())])
    puzzle.append(d)

#- bfs 초기값 설정(1,1 -> 0,0으로 시작)
nx = [1, -1, 0, 0]
ny = [0,  0, 1, -1]
queue = deque([[0, 0, 1]])
check[0][0] = 1

while len(queue):
    x, y, c = queue.pop()
    for i in range(4):
        cx, cy = x + nx[i], y + ny[i]
        if cx < 0 or cx >= N or cy < 0 or cy >= M:
            continue
        if puzzle[cx][cy] == 1 and check[cx][cy] == 0:
            check[cx][cy] = c+1
            queue.appendleft([cx, cy, c+1])

print(check[N-1][M-1])


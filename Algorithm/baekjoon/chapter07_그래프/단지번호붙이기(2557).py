"""
단지 번호 붙이기(2667)
- 1은 집이 있는 곳, 0은 집이 없는 곳
- 연결된 집의 모임인 단지를 정의하고, 단지에 번호를 붙이려고 함
- 연결되었다는 것은 어떤 집이 좌우, 아래위로 다른 집이 있는 경우를 말함
- 대각선상에 집이 있는 경우는 연결된 것이 아님
- 첫 번째 줄에는 총 단지수 출력
- 각 단지내 집의 수를 오름차순으로 정렬하여 하나씩 출력
"""
import sys
from collections import deque
inf = sys.stdin
N = int(inf.readline().strip())
complex = [[int(i) for i in list(inf.readline().strip())] for _ in range(N)]
check = [[0 for _ in range(N)] for _ in range(N)]

def bfs(x, y):
    queue = deque([[x, y]])
    check[x][y] = 1
    house_num = 1
    while len(queue):
        x, y = queue.pop()
        for i in range(4):
            cx, cy = x + nx[i], y + ny[i]
            if cx < 0 or cx >= N or cy < 0 or cy >= N:
                continue
            if check[cx][cy] == 0 and complex[cx][cy] == 1:
                check[cx][cy] = 1
                house_num += 1
                queue.appendleft([cx, cy])
    return house_num


nx = [1, -1, 0, 0]
ny = [0, 0, 1, -1]
complex_num = deque()
for i in range(N):
    for j in range(N):
        if check[i][j] == 0 and complex[i][j] == 1:
            complex_num.append(bfs(i, j))

print(len(complex_num))
[print(i) for i in sorted(complex_num)]

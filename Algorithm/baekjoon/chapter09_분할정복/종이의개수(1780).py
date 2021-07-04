"""
- 종이의 개수(1780)
- NxN 크기의 행렬로 표현되는 종이가 있음
- 종이의 칸에는 -1, 0, 1의 세 값 중 하나가 저장되어 있다
-  다음과 같은 규칙으로 종이를 자름
  - 만약 종이가 같은 수로 되어 있다면, 이 종이를 그대로 사용
  - (1) 이 아닌 경우에는 종이를 같은 크기의 9개의 종이로 자르고, 각각의 잘린 종이에 대해서 1을 반목
  - 이와 같이 종이를 잘랐을 때, -1로만 채워진 종이, 0으로만 채워진 종이, 1로만 채워진 종이의 개수 구하기

"""
import sys
from collections import defaultdict
inf = sys.stdin
N = int(inf.readline().strip())
paper = [[int(i) for i in inf.readline().strip().split()] for _ in range(N)]
dict_num = defaultdict(int)
def check_paper(x, y, N):
    start_num = paper[x][y]
    for i in range(N):
        for j in range(N):
            if not paper[x+i][y+j] == start_num:
                return False
    return True

def cut_paper(x, y, N):
    if check_paper(x, y, N):
        dict_num[paper[x][y]] += 1
        return

    tmp = N // 3
    for i in range(x, x+N, tmp):
        for j in range(y, y+N, tmp):
            cut_paper(i, j, tmp)

cut_paper(0, 0, N)
for i in range(-1, 2):
    print(dict_num[i])

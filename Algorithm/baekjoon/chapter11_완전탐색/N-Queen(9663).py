"""
N-Queen
- N-Queen 문제는 크기가 N × N인 체스판 위에 퀸 N개를 서로 공격할 수 없게 놓는 문제이다.
- N이 주어졌을 때, 퀸을 놓는 방법의 수를 구하는 프로그램을 작성하시오.

- 첫째 줄에 N이 주어진다. (1 ≤ N < 15)
- 첫째 줄에 퀸 N개를 서로 공격할 수 없게 놓는 경우의 수를 출력한다.
"""
import sys
inf = sys.stdin
N = int(inf.readline().strip())
check = [[False for _ in range(N)] for _ in range(N)]
check_col = [False for _ in range(N)]
check_row = [False for _ in range(N)]
check_right = [False for _ in range(2*N)]
check_left = [False for _ in range(2*N)]
result_value = 0
def chess(row):
    global result_value
    if row == N:
        result_value += 1
        return
    #- col
    for i in range(N):
        if not check[row][i] and not check_col[i] and not check_row[row] \
                and not check_right[N-i+row] and not check_left[i+row]:
            check[row][i] = True
            check_col[i] = True
            check_row[row] = True
            check_right[N-i+row] = True
            check_left[i+row] = True
            chess(row+1)
            check[row][i] = False
            check_col[i] = False
            check_row[row] = False
            check_right[N-i+row] = False
            check_left[i+row] = False

chess(0)
print(result_value)
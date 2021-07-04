"""
정수 X에 사용할 수 있는 연산은 다음 3가지
  - X가 3으로 나누어 떨어지면, 3으로 나눔
  - X가 2로 나누어 떨어지면, 2로 나눔
  - 1을 뺌
정수 N이 주어졌을 때, 위와 같은 연산 세 개를 적절히 사용해서 1을 만들려고 함
연산을 사용하는 횟수의 최솟값을 출력하시오
첫째 줄에 1보다 크거나 같고, 10^6 보다 작거나 같은 정수 N이 주어짐
"""
import sys
from collections import deque
inf = sys.stdin
N = int(inf.readline().strip())

if N <= 3:
    if N == 3:
        print(1)
    if N == 2:
        print(1)
    if N == 1:
        print(0)
else:
    d = [0 for _ in range(N+1)]
    d[1], d[2], d[3] = 0, 1, 1
    for i in range(4, N+1):
        tmp = []
        if i % 3 == 0:
            tmp.append(d[i//3] + 1)
        if i % 2 == 0:
            tmp.append(d[i//2] + 1)
        tmp.append(d[i-1] + 1)
        d[i] = min(tmp)
    print(d[N])

"""
2xn 타일링
- 2xn 크기의 직사각형을 1x2, 2x1 타일로 채우는 방법의 수를 구하는 프로그램을 작성하시오
- 입력 --> 첫째 줄에 n이 주어짐(1 <= n <= 1,000)
- 첫째 줄에 2xn 크기의 직사각형을 채우는 방법의 수를 10,007로 나눈 나머지를 출력
"""
import sys
inf = sys.stdin
N = int(inf.readline().strip())
if N <= 2:
    if N == 1:
        print(1)
    if N == 2:
        print(2)
else:
    tile = [0 for _ in range(N+1)]
    tile[1], tile[2] = 1, 2
    for i in range(3, N+1):
        tile[i] = ((tile[i-1] % 10007) + (tile[i-2] % 10007)) % 10007
    print(tile[N])



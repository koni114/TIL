"""
가장 긴 증가하는 부분 수열
- 수열 A가 주어졌을 때, 가장 긴 증가하는 부분 수열을 구하는 프로그램을 작성하시오

"""
import sys
inf = sys.stdin
N = int(inf.readline().strip())
value = [int(i) for i in inf.readline().strip().split()]
value.insert(0, 0)
dp = [0 for _ in range(N+1)]

if N == 1:
    print(1)
else:
    dp[1] = 1
    for i in range(2, N+1):
        tmp = 1
        for j in range(1, i):
            if value[j] < value[i]:
                tmp = max(dp[j]+1, tmp)
        dp[i] = tmp
    print(max(dp))

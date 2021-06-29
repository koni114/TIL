"""
스티커(9465)
- 스티커는 2행 n열로 배치되어 있음
- 스티커를 한장 떼면, 그 스티커와 변을 공유하는 스티커는 모두 찢어져 사용 X
"""
import sys
inf = sys.stdin
test_case = int(inf.readline().strip())

for _ in range(test_case):
    N = int(inf.readline().strip())
    sticker = []
    dp = []
    for _ in range(2):
        tmp = [int(i) for i in inf.readline().strip().split()]
        tmp.insert(0, 0)
        sticker.append(tmp)
        dp.append([0 for _ in range(N+1)])
    dp.append([0 for _ in range(N+1)])

    if N == 1:
        print(max(sticker[0][1], sticker[1][1]))
    else:
        dp[1][1], dp[2][1] = sticker[0][1], sticker[1][1]
        for i in range(2, N+1):
            dp[0][i] = max(dp[0][i-1], dp[1][i-1], dp[2][i-1])
            dp[1][i] = max(dp[2][i-1], dp[0][i-1]) + sticker[0][i]
            dp[2][i] = max(dp[1][i-1], dp[0][i-1]) + sticker[1][i]
        print(max(dp[0][N], dp[1][N], dp[2][N]))






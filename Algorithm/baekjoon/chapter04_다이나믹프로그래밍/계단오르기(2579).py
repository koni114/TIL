"""
- 계단오르기(2579)
  - 계단 아래 시작점에서 계단 꼭대기에 위치한 도착점까지 가는 게임
  - 계단에는 일정한 점수가 쓰여져 있음
- 계단 오르기 규칙
  - 계단은 한 번에 한 계단, 또는 두 계단씩 오를 수 있음
  - 연속된 세 개의 계단을 밟아서는 안됨
  - 마지막 도착 계단은 반드시 밟아야 함
"""
import sys
inf = sys.stdin
N = int(inf.readline().strip())
stair = [int(inf.readline().strip()) for _ in range(N)]
stair.insert(0, 0)

if N <= 2:
    print(sum(stair[:N+1]))
else:
    dp = [[0, 0, 0] for _ in range(N+1)]
    dp[1][1] = stair[1]
    dp[2][1] = stair[2]
    dp[2][2] = stair[2] + stair[1]
    for i in range(N+1):
        dp[i][1] = stair[i] + max(dp[i-2])
        dp[i][2] = stair[i] + dp[i-1][1]
    print(max(dp[i]))
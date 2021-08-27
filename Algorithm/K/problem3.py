# - 케로와 베로니의 책 사진 찍기
# - 케로와 베로니는 서점에서 카카오스토리에 올릴 책사진을 찍고 있습니다.
# - 둘은 책꽂이에 꽂혀있는 책의 높이가 아래 수식을 만족해야 사진이 만족스럽게 나온다는걸 알아챘습니다.
# - 사진속 책 높이 [x0, x1, …, xj-1] 에서 x0 <= x1 … <= xi and xi >= xi+1 … >= xj-1 … >= xj-1
# - 이 조건을 충족하는 여러 사진이 있으면 케로와 베로니는 책이 가장 많이 나온 사진을 고릅니다.
# - 책꽂이에 꽂혀있는 책의 높이를 배열로 받았을 때 케로와 베로니가 고른 사진에 책이 몇 권 있는지 알려주세요!

# - arr = [10, 8, 9, 15, 12, 6, 7]
# - 주어진 수식을 만족하면서 가장 많은 책이 담긴 사진 [8, 9, 15, 12, 6]의 길이인 5를 반환하시면 됩니다.

#- 제약조건
#- 1 <= n <= 10^5
#- 1 <= arr[i] <= 10^9
# - O(N)으로 풀것


#arr = [4, 6, 10, 8, 8, 9, 15, 12, 6, 6, 7, 7]
#arr = [7,7, 10,10, 8, 9, 15, 14, 12, 6, 7,7]
#arr = [1,2,3,2,1]
#arr = [1,2,3,4,1,2,5555,1,2,3,4,5,6,7,10,1,2]
#arr = [1,1,1,1,1,0,1]
#arr = [3,2,1,2,3,4]
arr = [3, 3, 3, 3, 2, 2, 1, 1, 4, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6]


# 투 포인터 풀이

lt, rt = 0, 1
prev = arr[lt]  # 이전 수
inc, dec = 1, 1  # 오르막, 내리막 카운트 둘다 0 이면 새로 갱신
state = -1  # 현재 오르막인가 내리막인가 오르막 : 1 내리막 : 0
cnt = 1  # 계단수 길이 임시 값
plt = 0  # 중복된 수가 있으면 lt 업데이트 시키기위한 변수
res = -1e9  # 최종 답

while True:
    if rt > len(arr)-1:
        res = max(res, cnt)
        break

    if arr[rt] > prev:  # 이전 수 보다 크면
        if state == 0:  # 내리막이다가 오르막을 만나면 (엣지케이스 처리)
            res = max(res, cnt)
            cnt = 1
            lt = plt
            rt = lt+1
            inc, dec = 1, 1
            state = 1
            continue

        if inc == 1:
            inc = 0
        else:
            if state == 0:  # 이미 오르막 카운트를 썼고, 현재상태가 내리막인데 다시 오르막길이면
                res = max(res, cnt)
                cnt = 1
                lt = plt
                rt = lt+1
                inc, dec = 1, 1
                continue
        plt = rt
        state = 1

    elif arr[rt] < prev:  # 이전 수 보다 작으면
        plt = rt
        if dec == 1:
            dec = 0
        else:
            if state == 1:  # 이미 내리막 카운트를 썼고, 현재상태가 오르막인데 다시 내리막이면
                res = max(res, cnt)
                cnt = 1
                lt = plt
                rt = lt+1
                inc, dec = 1, 1
                continue
        plt = rt
        state = 0

    prev = arr[rt]
    rt += 1
    cnt += 1

print(res)


# dp 풀이

dp = [[0]*len(arr) for _ in range(2)]
dp[0][0] = 1
dp[1][len(arr)-1] = 1

for i in range(1, len(arr)):  # 정방향 증가수열
    if arr[i] >= arr[i-1]:
        dp[0][i] = dp[0][i-1] + 1
    else:
        dp[0][i] = 1
for j in range(len(arr)-2, -1, -1):  # 역방향 증가수열
    if arr[j] >= arr[j+1]:
        dp[1][j] = dp[1][j+1] + 1
    else:
        dp[1][j] = 1

res = -1e9
for i in range(len(arr)):
    res = max(res, dp[0][i]+dp[1][i])

print(res-1)
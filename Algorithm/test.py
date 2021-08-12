#- 1. 한번만 사용한 첫 문자 찾기
#- 문자열에서 한번만 사용한 문자를 찾고자 함. 문자열은 소문자만 사용함
#- 한번만 사용한 문자 중 먼저 나타난 문자의 인덱스를 리턴해야 함.
#- 인덱스는 1부터 시작함. 한번만 사용한 문자가 없을 경우 -1을 리턴해야 함.
#- ex) s = "statistics"
#- -> [a, c]
import sys

s = "falafal"
def solution(s):
    from collections import Counter
    only_one_char_lists = [key for key, value in Counter(s).items() if value == 1]
    return -1 if not only_one_char_lists else min([list(s).index(i)+1 for i in only_one_char_lists])

solution(s)

#- 2. 카카오 스포츠 경기
#- 라이언 왕국와 어피치 왕국은 스포츠 경기 대결을 하고 싶어함
#- 어피치 왕국은 경기를 이기기 위해 팀의 전력을 최대로 만들고 싶어함
#- 각 선수는 1, 2, 3...으로 증가하는 고유한 공격력이 부여되어있습니다.
#- 팀의 출전 명단은 한 명의 선수에서부터 시작하여 다음과 같은 방법으로 출전하는 선수의 수가 증가함

#- 처음 팀에 x 공격력을 가진 선수 한명이 있음
#- x의 각 자릿수의 계승 합이 y가 됨. 그러면 y 공격력을 가진 선수를 출전 명단에 추가함
#- 마찬가지로 y의 각 자리수의 계승 합인 z 공격력을 가진 선수를 출전 명단에 추가함
#- 하지만, 이미 동일한 공격력을 가진 선수는 다시 추가할 수 없음

#- 최대 공격력을 가진 선수가 팀 리더가 되며, 팀 리더의 공격력과 팀 선수들의 수를 곱한 값이 팀의 전력이 됨
#- 첫 선수의 공격력 x가 주어졌을 때, 팀의 전력을 구한 후 그 값을 반환

#- 예제
#- 예를 들어, 한 선수의 공격력이 24이면 다음 출전 선수의 공격력은 26이 됨
# (두 번째 자리수) 2의 계승 + (첫 번째 자리수) 4의 계승 = 2! + 4! = 2 * 1 + 4 * 3 * 2 * 1 = 26

#- 출전 선수들의 공격력이 {4, 24, 26, 722, 5044, 169, 363601 ,1454} 라면
#- 이 팀의 전력은 2908808이 됨
# 363601 * 8 = 2908808

def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)

def solution(n):
    from collections import defaultdict
    players = defaultdict(int)
    players[n] = 1
    best_attacker, curr_player = n, n
    while True:
        next_player = sum([factorial(value) for value in map(int, list(str(curr_player)))])
        if players[next_player]: break
        players[next_player] = 1
        best_attacker = max(best_attacker, next_player)
        curr_player = next_player
    return best_attacker * (len(players))

solution(540)

#- 케로와 베로니의 책 사진 찍기
#- 케로와 베로니는 서점에서 카카오스토리에 올릴 책사진을 찍고 있습니다.
#- 둘은 책꽂이에 꽂혀있는 책의 높이가 아래 수식을 만족해야 사진이 만족스럽게 나온다는걸 알아챘습니다.
#- 사진속 책 높이 [x0, x1, ..., xj-1] 에서 x0 <= x1 ... <= xi and xi >= xi+1 ... >= xj-1 ... >= xj-1
#- 이 조건을 충족하는 여러 사진이 있으면 케로와 베로니는 책이 가장 많이 나온 사진을 고릅니다.
#- 책꽂이에 꽂혀있는 책의 높이를 배열로 받았을 때 케로와 베로니가 고른 사진에 책이 몇 권 있는지 알려주세요!

#- arr = [10, 8, 9, 15, 12, 6, 7]
#- 주어진 수식을 만족하면서 가장 많은 책이 담긴 사진 [8, 9, 15, 12, 6]의 길이인 5를 반환하시면 됩니다.

#- 제약조건
#- 1 <= n <= 10^5
#- 1 <= arr[i] <= 10^9

def solution(arr):
    from collections import deque
    ascend_arr, descend_arr = deque([]), deque([])
    for i in range(len(arr)):
        if i == 0:
            ascend_arr.append(1)
        else:
            if arr[i-1] <= arr[i]:
                ascend_arr.append(ascend_arr[i-1]+1)
            else:
                ascend_arr.append(1)

    max_book = 0
    for i in range(len(arr)-1, -1, -1):
        if i == len(arr)-1:
            descend_arr.appendleft(1)
        else:
            if arr[i+1] <= arr[i]:
                descend_arr.appendleft(descend_arr[0]+1)
            else:
                descend_arr.appendleft(1)

    for i, j in zip(ascend_arr, descend_arr):
        max_book = max(max_book, i+j-1)

    return max_book
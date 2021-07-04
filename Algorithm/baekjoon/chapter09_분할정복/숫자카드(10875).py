"""
숫자카드(10875)
- 숫자카드는 정수 하나가 적혀져 있는 카드
- 상근이는 숫자 카드 N개를 가지고 있음. 정수 M개가 주어졌을 때 이 수가 적혀있는 숫자 카드를
  상근이가 가지고 있는지 아닌지를 구하는 프로그램 작성

- 첫 째줄에 상근이가 가지고 있는 숫자 카드의 개수(1<=N<=500,000)
- 둘째 줄에는 숫자 카드가 적혀있는 정수가 주어짐
  숫자 카드에 적혀있는 수는
"""

#- 파이써닉 풀이
import sys
inf = sys.stdin
card_num = int(inf.readline().strip())
card = {num: "1" for num in inf.readline().strip().split()}
check_num = int(inf.readline().strip())
check = [card.get(num, "0") for num in inf.readline().strip().split()]
print(" ".join(check))

#- binary serach 를 이용한 풀이
def binary_search(arr, value):
    left, right = 0, len(arr)-1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == value:
            return 1
        elif arr[mid] >= value:
            right = mid-1
        else:
            left = mid+1

    return 0

import sys
inf = sys.stdin
card_num = int(inf.readline().strip())
card = [int(i) for i in inf.readline().strip().split()]
card = sorted(card)
check_num = int(inf.readline().strip())
check = [int(i) for i in inf.readline().strip().split()]
is_value_list = [str(binary_search(card, i)) for i in check]
print(" ".join(is_value_list))








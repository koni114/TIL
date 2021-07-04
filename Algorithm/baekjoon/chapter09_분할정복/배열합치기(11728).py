"""
- 배열 합치기(11728)

- 정렬되어 있는 두 배열 A, B가 주어짐. 두 배열을 합친 다음 정렬해서 출력하는 프로그램을 작성

- 첫째 줄에 배열 A의 크기 N, 배열 B의 크기 M이 주어짐(1 <= N, M <= 1,000,000)
"""
import sys
from collections import deque
inf = sys.stdin
N, M = [int(i) for i in inf.readline().strip().split()]
first_list = deque([int(i) for i in inf.readline().strip().split()])
second_list = deque([int(i) for i in inf.readline().strip().split()])
final_list = deque()


while first_list and second_list:
    if first_list[0] < second_list[0]:
        final_list.append(str(first_list.popleft()))
    else:
        final_list.append(str(second_list.popleft()))

while first_list:
    final_list.append(str(first_list.popleft()))

while second_list:
    final_list.append(str(second_list.popleft()))

print(" ".join(final_list))


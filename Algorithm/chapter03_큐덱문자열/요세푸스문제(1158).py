"""
- 1번부터 N 번까지 N명의 사람이 원을 이루면서 앉아 있음
- 양의 정수 k(<=N)이 주어짐
- 순서대로 K번째 사람을 제거. 한 사람이 제거되면 남은 사람들로 이루어진 원을 따라 과정을 계속함
- 이 과정은 N명의 사람이 모두 제거될 때까지 계속됨
- 1 <= K <= N <= 5,000
"""
import sys
from collections import deque
inf = sys.stdin
K, N = [int(i) for i in inf.readline().split()]
result_value = deque()
people = deque(list(range(1, K+1)))
while len(people) >= 1:
    for _ in range(N-1):
        people.append(people.popleft())
    result_value.append(str(people.popleft()))
print('<' + ", ".join(result_value) + ">")

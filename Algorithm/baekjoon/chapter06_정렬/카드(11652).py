"""
카드(11652)
- 준규는 숫자 카드 N장을 가지고 있음
- 숫자 카드에는 정수가 하나 적혀있음
- 준규가 가지고 있는 카드가 주어졌을 때, 가장 많이 가지고 있는 정수를 구하는 프로그램을 작성해라
"""
import sys
from collections import defaultdict
inf = sys.stdin
N = int(inf.readline().strip())
d = defaultdict(int)
for _ in range(N):
    d[int(inf.readline().strip())] += 1
sorted_list = sorted(d.items(), key=lambda x: (-x[1], x[0]))
print(sorted_list[0][0])

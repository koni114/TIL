"""
- 국영수
- 도현이네 반 학생 N명의 이름과 국어, 영어, 수학 점수가 주어진다.
- 다음과 같은 조건으로 학생의 성적을 정렬하는 프로그램을 작성
1. 국어 점수가 감소하는 순서로
2. 국어 점수가 같으면 영어 점수가 증가하는 순서로
3. 국어 점수와 영어 점수가 같으면 수학 점수가 감소하는 순서로
4. 모든 점수가 같으면 이름이 사전 순으로 증가하는 순서로

- 도현이네 반 학생의 수 N(1<= N <= 100,000)
"""
import sys
from collections import namedtuple, deque

inf = sys.stdin
N = int(inf.readline().strip())
d = deque()
for _ in range(N):
    tmp_list = [i for i in inf.readline().strip().split()]
    tmp_list[1:] = [int(i) for i in tmp_list[1:]]
    d.append(tmp_list)

d = sorted(d, key=lambda x: (-x[1], x[2], -x[3], x[0]))
for value in d:
    print(value[0])

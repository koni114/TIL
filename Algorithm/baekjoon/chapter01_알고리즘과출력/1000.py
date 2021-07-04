"""
1001번 묹
A+B
두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.
첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)
첫째 줄에 A+B를 출력한다.

ex1)
1 2
3
"""
import sys
inf = sys.stdin
print(sum([int(i) for i in inf.readline().split()]))


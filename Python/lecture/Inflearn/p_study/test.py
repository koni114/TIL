#- namedtuple 을 이용하여 두 점 사이의 거리를 계산하기

from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])

from math import sqrt
p1 = Point(10, 20)
p2 = Point(15, 30)

l1 = sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
print(round(l1, 4))

# 실 사용 실습
# 반에 20명의 학생이 있고, 4개의 반(A, B, C, D)
# ex) A10, B20, C15 ...
Classes = namedtuple('Classes', ['ranks', 'numbers'])
students2 = [Classes(rank, number)
                for rank in 'A B C D'.split()
                    for number in [str(n) for n in range(1, 21)]]













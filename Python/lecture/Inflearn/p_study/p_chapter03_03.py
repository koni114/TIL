"""
chapter03_03.py
"""

# 객체 -> 파이썬의 데이터를 추상화
# 모든 객체는 id, type -> value

# 일반적인 튜플을 선언하면 다음과 같음
# 아래처럼 데이터를 선언하면, 정확하게 어떤 의미로 선언했는지 알기가 어려움
# 따라서 namedtuple 을 사용하면 좀 더 명확하게 사용 가능
pt1 = (1.0, 5.0)
pt2 = (2.5, 1.5)

from math import sqrt
l1 = sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
print(l1)

# namedtuple 을 활용해서 두 점 사이의 거리를 계산해보기
from collections import namedtuple

Point = namedtuple('Point', 'x y')
pt1 = Point(1.0, 5.0)
pt2 = Point(2.5, 1.5)
l1 = sqrt((pt1.x - pt2.x) ** 2 + (pt1.y - pt2.y) ** 2)
print(l1)

# 네임드 튜플 선언 방법
Point1 = namedtuple('Point', ['x', 'y'])  # 방법 1
Point2 = namedtuple('Point', 'x, y')      # 방법 2
Point3 = namedtuple('Point', 'x y')       # 방법 3

# 변수 명을 선언하고 싶지 않고 namedtuple 에 할당하고 싶을 때 rename = True 로 설정(기본값은 False)
Point4 = namedtuple('Point', 'x y x class', rename=True) # 방법 4
print(Point4)

# 출력
print(Point1, Point2, Point3, Point4)
p1 = Point1(x=10, y=35)
p2 = Point2(20, 40)
p3 = Point3(45, y=20)
p4 = Point4(10, 20, 30, 40)


print(p1)
print(p2)
print(p3)

# rename test
print(p4) # 주의!

# dict to Unpacking -> namedtuple
temp_dict = {'x': 75, 'y': 55}
p5 = Point3(**temp_dict)
print(p5)

# 사용
print(p1[0] + p2[1])
print(p1.x + p1.y)

x, y = p3
print(x, y)

# namedtuple method
temp = [52, 38]

# list를 namedtuple 로 변환
# 이 때, 값이 list <-> namedtuple 의 개수가 맞아야 함
p4 = Point1._make(temp)
print(p4)

# _fields: 필드 네임 확인 -> key 값만 조회
print(p1._fields, p2._fields, p3._fields)

# _asdict() : OrderedDict 반환
print(p1._asdict())
print(p4._asdict())

# 실 사용 실습
# 반에 20명의 학생이 있고, 4개의 반(A, B, C, D)
# ex) A10, B20, C15 ...

Classes = namedtuple('Classes', ['rank', 'number'])

# 그룹 리스트를 선언
numbers = [str(n) for n in range(1, 21)]
ranks = 'A B C D'.split()

# List Comprehension
students = [Classes(rank, number)
            for rank in ranks
                for number in numbers]

print(len(students))
print(students)

# 위의 List Comprehension 에서 가독성을 위하여 추천하는 방식
students2 = [Classes(rank, number)
             for rank in 'A B C D'.split()
                for number in [str(n) for n in range(1, 21)]]

# 출력
for s in students:
    print(s)

# 가공하고자 하는 데이터를 구상화할 수 있음
# Json, DataBase, RestAPI 로 Web 으로 전송도 가능








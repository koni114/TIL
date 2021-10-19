"""
chapter03-02
- 난이도가 있지만 단순한 클래스 예제 진행
"""

# 클래스 예제 2
# 벡터를 쉽게 계산해 줄 수 있는 클래스를 만들어 모든 개발자들이 사용 가능하도록 만드는 예제.
# (5, 2) + (4, 3) = (9, 5)
# (10, 3) * 5 = (50, 15)
# (5, 10) 의 최대 값 = 10
# Framework, library 를 만드는 개발자가 인정받는 개발자


class Vector(object):
    def __init__(self, *args):
        '''
        Create a vector, example : v = Vector(5, 10)
        '''
        if len(args) == 0:
            self._x, self._y = 0, 0
        else:
            self._x, self._y = args

    def __repr__(self):
        '''
        Return the vector information.
        '''
        return f'Vector({self._x}, {self._y})'

    def __add__(self, other):
        '''
        Return the vector add self and other
        '''
        return Vector(self._x + other._x, self._y + other._y)

    def __mul__(self, y):
        '''
        multiply each self x and other
        '''
        return Vector(self._x * y, self._y * y)

    def __bool__(self):
        '''
        check vector is (0,0)
        '''
        return bool(max(self._x, self._y))

# Vector 인스턴스 생성
v1 = Vector(2, 5)
v2 = Vector(23, 35)
v3 = Vector()

print(v1)
print(v2)
print(v3)

# 매직 메소드
print(v1 + v2)
print(v2 * 0)
print(bool(v1), bool(v2))
print(bool(v3))

# method 단위로 주석을 호출하고 싶은 경우
print(Vector.__init__.__doc__)
print(Vector.__add__.__doc__)



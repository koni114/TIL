"""
chapter03-01 파이썬 데이터 모델
- 파이썬 핵심 구조 설명
- 매직 메소드 실습
- 클래스 매직 메소드 실습
"""

# Special Method(Magic Method)
# 파이썬의 핵심 4가지 -> 시퀀스(Sequence), 반복(Iterator), 함수(Functions), 클래스(Class)
# 4가지를 정복을 한다면, 파이썬을 바라보는 시야가 훨씬 깊어짐

# 매직 메소드는 클래스 안에 정의할 수 있는 특별한(Built-in, 만들어져 있음) 메소드
# 더블 언더 스코어로 시작하는 것

# 기본형
# 파이썬에서의 모든 것들은 class! 즉 int 를 출력하면 class 가 나옴
print(int(10))
print(int)

# 모든 속성 및 메소드 출력
# dir 함수를 통해 int, float 를 출력하면, 평소 많이 사용해보았던 것들과 그렇지 못했던 매직 메소드들을 확인 가능
print(dir(int))
print(dir(float))

n = 10
print(type(n)) # class 임을 확인
print(n + 100) # 내부적으로 __add__ 가 호출 됨
print(n.__add__(100)) # 위와 동일한 결과값이 나옴
print(n.__doc__) # int 가 의미하는 것이 무엇인지 확인 가능

print(n.__bool__()) # 0 이면 False 임
print(n.__bool__(), bool(n))   # 두 개는 동일
print(n * 100, n.__mul__(100)) # 두 개는 동일

# 클래스 끼리의 연산 수행해보기
# 클래스 예제1


class Fruit:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    def __str__(self):
        return f'Fruit Class Info : {self._name}, {self._price}'

    def __add__(self, other):
        print("called >> __add__")
        return self._price + other._price

    def __sub__(self, other):
        print("called >> __sub__")
        return self._price - other._price

    def __le__(self, other):
        print("called >> __le__")
        if self._price <= other._price:
            return True
        else:
            return False

    def __lt__(self, other):
        print("called >> __lt__")
        if self._price < other._price:
            return True
        else:
            return False

    def __gt__(self, other):
        print("called >> __gt__")
        if self._price > other._price:
            return True
        else:
            return False

    def __ge__(self, other):
        print("called >> __ge__")
        if self._price >= other._price:
            return True
        else:
            return False


# 인스턴스 생성
s1 = Fruit('Orange', 7500)
s2 = Fruit('Banana', 3000)

print(s1._price + s2._price) # 일반적인 계산, 가독성, 코드 수가 많이 늘어남
print(s1 + s2)
print(s1 - s2)

print(s1 <= s2)
print(s1 >= s2)

print(s1 < s2)
print(s1 > s2)



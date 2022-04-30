# 2022-05-01.py
# 열거형(Enumerate Type). 언어의 상수 역할을 하는 식별자.
# Python 3.4 에서 새로 추가
# 일부 열거자 자료형은 언어에 기본으로 포함되어 있음. 예를 들어 False, True 값이 미리 정의된 열거형으로 볼 수 있음.
# --> False == 0, True == 1
print(0 == False)
print(1 == True)

from enum import Enum


class Rainbow(Enum):
    Red = 0
    Orange = 1
    Yellow = 2
    Green = 3
    Blue = 4
    Navy = 5
    Purple = 6

# 자료형(type)을 확인해보니, enum 형태의 Rainbow 로 확인됨
type(Rainbow.Blue)

# Enum 호출하기
# 아래와 같이 호출하면 실제 Enum의 값은 나오지 않음
print(Rainbow["Blue"])
print(Rainbow.Blue)

# Key : Value 형식으로 보이지만 딕셔너리가 작동하는 것과는 다름
# 딕셔너리에는 key 를 호출하면 Value 가 나왔지만, Enum 은 HTML 태그의 작동 방식과 더 유사함
# name, value 를 호출하는 방식으로 사용함
print(Rainbow.Blue.name)
print(Rainbow.Blue.value)

class Port(Enum):
    SSH = 22
    Telnet = 23
    SMTP = 25
    HTTP = 80
    HTTPS = 443


print(Port.HTTP.value)

# Enum 은 왜 쓸까?
# 특정 상태를 하나의 집합으로 만들어 관리함으로써 코드를 정리하는데 수월함.
# 즉, 가독성이 높아지고 문서화를 하는데 도움이 됨

# Enum 에 대한 몇가지 팁
# 다른 언어에서는 기본적으로 Enum 을 상속 받도록 만든 다음,
# 내가 커스터마이징하려는 변수만 선언을 하면 값을 지정하지 않아도 기본값이 0, 1, 2, ... 이런식으로 설정이 되지만,
# 아쉽게도 파이썬은 모든 변수를 직접 지정해줘야합니다.

# 일일이 코드를 할당하기 귀찮은 경우,
#  enum 안에 있는 auto() 함수를 이용할 수 있습니다.
import enum

class Rainbow(enum.Enum):
    Red = enum.auto()
    Orange = enum.auto()
    Yellow = enum.auto()
    Green = enum.auto()
    Blue = enum.auto()
    Navy = enum.auto()
    Purple = enum.auto()

# 위의 방법도 귀찮은 경우,
# 파이썬에서 Enum 을 지원하기 이전에 사용하던 방법을 써도 됨
# Enum 을 직접 함수로 만들어 사용하는 것


def my_enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


Rainbow = my_enum('Red', 'Orange', 'Yellow',
                  'Green', 'Blue', 'Navy', 'Purple')

print(Rainbow.Red)
print(Rainbow.Orange)
print(Rainbow.Purple)

"""
병행성(Concurrency)
- 병행성, 흐름제어 설명
- 이터레이터(Iterator)
- 제네레이터(Generator)
- __iter__, __next__
- 클래스 기반 제너레이터 구현
"""

# Chapter06-01
# 병행성(Concurrency)
# 이터레이터, 제너레이터
# Iterator, Generator

# 제너레이터는 반복 가능한 객체를 리턴
# 파이썬 반복 가능한 객체(Iterable)
# ex) collections, text file, list, Dict, Set, Tuple, unpacking, *args ..

# 제너레이터란 ?
# Iterator 를 return 하는 함수

t = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# 즉 __iter__ 메소드가 존재한다는 것은 for loop 처리가 가능하다는 의미
# 내부적으로, t 가 __iter__ -> __next__ 를 통해 하나하나 실행함!
for c in t:
    print(c)


# next 함수가 마지막에 도달하면, StopIteration 발생
# 아래와 같은 구문은 위의 for 문의 결과와 동일.
# 아래와 같이 구성되어 있다는 것만 기억하자(내부적 원리는 그러하다!)

w = iter(t)
while True:
    try:
        print(next(w))
    except StopIteration:
        print("iter 객체의 마지막에 도달하였습니다.")
        break

print()

# 반복형 확인
# 0. dir

# 1. hasattr
print(hasattr(t, '__iter__'))

# 2. abc
from collections import abc
print(isinstance(t, abc.Iterable)) # True -> 반복 가능

# 클래스 기반 이터레이터 구현
# 한 단어 씩을 return 해주는 splitter 구현
class WordSplitter:
    def __init__(self, text):
        self._idx = 0
        self._text = text.split(' ')

    def __next__(self):
        # print('Called __next__')
        try:
            word = self._text[self._idx]
        except IndexError:
            raise StopIteration('Stopped Iteration. ')
        self._idx += 1
        return word

    def __repr__(self):
        return f"WordSplit({self._text})"

wi = WordSplitter('Do today what you could do tomorrow')

# 마지막에는 예외가 잡히면서 아무것도 출력되지 않음.
print(wi)
for _ in range(10):
    print(next(wi))

# next 패턴은 예외 처리, index 처리 등을 해주어야 하기 때문에 불편함
# 즉 위의 클래스를 generator 패턴으로 변경해보자

# generator
# 1. 지능형 리스트, 딕셔너리, 집합 -> 데이터 양이 증가할 경우에 메모리 사용량이 증가 --> 제너레이터 사용 권장
# 2. 단위 실행 가능한 코루틴(Coroutine) 구현과 연동 가능
# 3. 작은 메모리 조각 사용

class WordSplitGenerator:
    def __init__(self, text):
        self._text = text.split(" ")

    def __iter__(self):
        for word in self._text:
            yield word # generator. return 이 따로 없어도 됨

        def __repr__(self):
            return f"WordSplitGenerator({self._text})"

wg = WordSplitGenerator('Do today what you could do tomorrow')
wt = iter(wg)

print(wt) # generator 라고 호출
for _ in range(6):
    print(next(wt))





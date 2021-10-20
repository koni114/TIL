"""
- 파이썬 일급 함수(객체)
  - 일급 함수의 개념은 파이썬에 국한된 개념은 아님
- 익명함수(Lambda)
- Callable 설명
- Partial 설명
"""
# chapter05-01
# 일급 함수(일급 객체)
# 파이썬 함수 특징
#   1. 런타임 초기화
#   2. 변수 할당 가능
#   3. 함수 인수 전달 가능
#   4. 함수 결과 반환 가능(return)

# 5! = 5 x 4 x 3 x 2 x 1

# 함수는 객체 취급을 하고 있음
def factorial(n):
    '''
    Factorial Function -> n : int
    '''
    if n == 1:
        return 1
    return n * factorial(n-1)


class A:
    pass

print(factorial(5))
print(factorial.__doc__)
print(type(factorial)) # class function 으로 나옴! 1급 객체
print(type(A))
print(dir(factorial))  # class 가 가지고 있는 Magic method 가 보임
print(set(sorted(dir(factorial))) - set(sorted(dir(A)))) # 함수만 가지고 있는 속성이 나옴
print(factorial.__name__)
print(factorial.__code__)

# 변수 할당
var_func = factorial
print(var_func)
print(var_func(10))
print(list(map(var_func, range(1, 11)))) # 각각의 factorial 을 list 로 뽑아낸 것

# 함수 인수 전달 및 함수로 결과 반환 -> 고위 함수(Higher-order function)
# map, filter, reduce

print(list(map(var_func, filter(lambda x: x % 2, range(1, 6))))) # filter 함수의 인자로 함수를 전달
print([var_func(i) for i in range(1, 6) if i % 2])

# reduce
# python version 이 높아짐에 따라 reduce 함수가 functools 로 빠짐
from functools import reduce
from operator import add

print(sum(range(1, 11)))
print(reduce(add, range(1, 11)))

# 익명 함수(lambda)
# 가급적 주석 작성
# 가급적 함수 작성, 익명함수는 꼭 필요한 순간에만 써라
# 일반 함수 형태로 리팩토링 권장

print(reduce(lambda x, t: x + t, range(1, 11)))

# Callable : 호출 연산자 --> 메소드 형태로 호출 가능한지 확인
# 호출 가능 확인
# __call__ 함수가 있으면 함수로써 호출이 가능

print(callable(str))
str('a')

print(callable(A))
print(callable(list))
print(callable(var_func))
print(callable(3.14)) # 상수여서 함수로서의 호출은 불가능함 ex) 3.14(test).. X

# partial 사용법 : 인수 고정 --> 콜백 함수에 사용
# 매우 중요 !!
from operator import mul
from functools import partial

print(mul(10, 10))

# 10은 항상 박혀있고, 뒤에 값만 변동이 있다고 가정할 때 partial 사용
five = partial(mul, 5)
print(five(10))
print(five(100))

six = partial(five, 6)
print(six()) # 인자를 넣을 필요 없이 5 x 6 = 30 이 나옴
print([five(i) for i in range(1, 11)]) # 5 의 배수를 만듬


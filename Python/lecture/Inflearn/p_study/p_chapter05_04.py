"""
데코레이터(Decorator)
- 클로저 -> 데코레이터 관계
- 데코레이터 실습(1)
- 데코레이터 실습(2)
"""
# chapter05-04.py
# 데코레이터(decorator)
# 데코레이터를 사용하려면 다음과 같은 내용을 기억하고 있어야 함
# - 클로저
# - 일급 함수
# - 가변 인자
# - 언패킹

# 장점
# 중복 제거, 코드 간결, 공통 함수 작성 등
# 로깅, 프레임워크, 유효성 체크 -> 공통 기능으로 요약
# 조합해서 사용하기 편함

# 단점
# 1. 가독성이 떨어짐
# 2. 특정 기능에 한정된 함수 -> 단일 함수로 작성하는 것이 유리
# 3. 디버깅 불편

# 데코레이터 실습
# ex) 모든 함수를 실행할 때마다 실행 시간을 측정하고 싶을 때
# ex) 홈페이지 사용시 클릭할 때 마다 통계를 갱신하고 싶을 때

import time

def perf_clock(func):
    # free scope -> func 를 가지고 있을 것임
    def perf_clocked(*args):
        st = time.perf_counter()
        result = func(*args)
        et = time.perf_counter() - st
        name = func.__name__
        arg_str = ','.join(repr(arg) for arg in args)
        print(f"[%0.5fs] %s(%s) -> %r" % (et, name, arg_str, result))
        return result
    return perf_clocked


def time_func(seconds):
    time.sleep(seconds)


def sum_func(*numbers):
    return sum(numbers)

# 데코레이터 미사용
none_deco1 = perf_clock(time_func)
none_deco2 = perf_clock(sum_func)

print(none_deco1, none_deco1.__code__.co_freevars)
print(none_deco2, none_deco1.__code__.co_freevars)

print('-' * 50, 'Called None Decorator -> time_func')
print()
none_deco1(1.5)
print('-' * 40, 'Called None Decorator -> sum_func')
none_deco2(100, 200, 300, 400, 500)

# 데코레이터 사용
@perf_clock
def time_func(seconds):
    time.sleep(seconds)

@perf_clock
def sum_func(*numbers):
    return sum(numbers)

print('-' * 50, 'Called None Decorator -> time_func')
print()
time_func(1.5)
print('-' * 50, 'Called None Decorator -> sum_func')
print()
sum_func(100, 200, 300, 400, 500)

# 코드 생산성은 데코레이터를 사용하는 것이 훨씬 좋음

"""
chapter06-03.py
코루틴(coroutine)
- generator 에서 coroutine 으로 이어지는 것을 이해해보자
"""

# ** 코루틴(coroutine)
# yield 라는 명령어를 통해 메인과 서브루틴 서로 상호 작용함
# 단일 싱글 스레드에서 yield 라는 명령어를 통해 stack 기반으로 동작하는 '비동기' 작업
# 코루틴 제어 -> 상태를 양방향 전송(yield <-> send)
# 서브루틴은 메인루틴을 호출하면 서브루틴에서 수행(흐름제어)
# 코루틴은 루틴 실행 중 중지한 다음 다시 실행 가능. 시점을 기억하고 있음(동시성 프로그래밍)
# 스레드에 비해 오버헤드가 감소
# 파이썬 3.5 이상에서 def -> async, yield -> await 명령어로 사용가능
# 비동기는 async, yield from -> await 로 사용 가능

# ** 스레드(thread)
# os 에서 관리하며, 동시에 각자 맡은 작업을 수행할 수도 있고, 한가지 작업을 할 수도 있음
# CPU 코어에서 실시간 또는 시분할로 '비동기' 작업을 수행
# 싱글 스레드나 멀티 스레드를 사용 가능한데, 코딩이 복잡한데 이유는 자원을 공유하며 deadlock 발생 가능성이 있음
# 또한 컨텍스트 스위칭 비용이 크며, 자원 소비 가능성이 커짐
# 오히려 싱글 스레드에서 짠 코드가 멀티 스레드보다 빠른 경우가 있음 -> 스위칭 비용이 크기 때문

# 코루틴 예제
# 코루틴 ex1
# 코루틴, 제너레이터, 단순 함수 등은 모두 함수로 선언하기 떄문에, 함수 내부를 보면서 확인 가능 해야함
def coroutine1():
    print('>>> coroutine started.')
    i = yield
    print(f'>>> coroutine received {i}')

# 제너레이터 선언1
# 메인 루틴 : coroutine1 함수를 호출하는 호출부 이므로 메인 루틴이라고 할 수 있음
# 서브 루틴 : coroutine1 함수 내부를 서브 루틴이라고 할 수 있음
# yield 기본 전달 값 --> None
cr1 = coroutine1()
print(cr1, type(cr1)) # cr1 은 generator 이며, 타입도 generator 임
next(cr1)
next(cr1) # coroutine received None -> StopIteration

# send 함수를 통해 메인 루틴과 서브 루틴을 통해 데이터를 교환할 수 있음
# 시작하기도 전에 send 하면 error 발생
cr1 = coroutine1()
next(cr1)
cr1.send(100) # coroutine received 100 --> 100 이라는 값을 전달 받은 것을 확인 가능

# coroutine ex2
# 파이썬에서는 코루틴의 상태 확인 가능
# GEN_CREATED : 처음 대기 상태
# GEN_RUNNING : 실행 상태
# GEN_SUSPENDED : yield 대기 상태
# GEN_CLOSED : 실행 완료 상태

def coroutine2(x):
    print(f'>>> coroutine started : {x}')
    y = yield x
    print(f'>>> coroutine received : {y}')
    z = yield x + y
    print(f'>>> coroutine received : {z}')

cr3 = coroutine2(10)
print(next(cr3)) # yield x 가 반환됨. y 값을 받기 위해 대기 상태 됨

cr3.send(100) # yield x + y 가 반환됨. z 값을 받기 위해 대기 상태 됨
cr3.send(1000) # z 값이 print 를 통해 출력후 StopIteration 발생

# 코루틴의 상태값 확인해보기
from inspect import getgeneratorstate
cr3 = coroutine2(10)
print(getgeneratorstate(cr3)) # GEN_CREATED
print(next(cr3))
print(getgeneratorstate(cr3)) # GEN_SUSPENDED
print(next(cr3))
cr3.send(100)

# y = yield x 에서 오른쪽에 있으면 나한테 주는 것. 왼쪽에 있으면 값을 받는 것

# coroutine ex3
# StopIteration 자동 처리(3.5 -> await 으로 처리가능)
# 중첩 코루틴 처리

def generator1():
    for x in 'AB':
        yield x
    for y in range(1, 4):
        yield y

t1 = generator1()
print(next(t1)) # A 출력
print(next(t1)) # B 출력
print(next(t1)) # 1 출력
print(next(t1)) # 2 출력
print(next(t1)) # 3 출력

print(next(t1)) # StopIteration

t2 = generator1()
print(list(t2)) # ['A', 'B', 1, 2, 3]

def generator2():
    yield from 'AB'
    yield from range(1, 4)

t3 = generator2()
print(next(t3)) # A 출력
print(next(t3)) # B 출력
print(next(t3)) # 1 출력
print(next(t3)) # 2 출력
print(next(t3)) # 3 출력







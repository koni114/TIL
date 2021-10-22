"""
클로저 기초(Closure)
- 파이썬 변수 범위(Scope)
- Global 선언
- 클로저 사용 이유
- Class 형태로 Closure 를 구현
  - closure : class 안에 있는 특정 scope 안에 있는 데이터를 저장하는 방식(snapshot)
  - closure 를 잘 이해해야 병행성 등을 이해할 수 있음
"""
# 클로저 기초
# 파이썬의 변수 범위(scope)

# 파이썬 변수 범위(scope)
def func_v1(a): # error : b를 선언하지 않음
    print(a)
    print(b)

func_v1(10) # b는 선언되지 않았으므로 error

# Ex2
b = 20
def func_v2(a):
    print(a)
    print(b)

func_v2(10) # 10, 20 이 선언이 됨. 즉 b는 global scope 에 있는 변수를 출력함

# Ex3
c = 30

def func_v3(a):
    print(a)
    # 안에 선언 되어 있으면 local 변수로 판단함
    print(c) # unbounded error 발생 : referenced before assignment
    c = 40

func_v3(10)

def func_v3(a):
    c = 40
    print(a)
    print(c)

func_v3(10) # 정상 출력

c = 30
def func_v3(a):
    global c
    print(a)
    print(c)
    c = 40 # 함수 내부적으로 c를 global 로 선언했으므로 global 값이 바뀜

print(">> ", c)
func_v3(10)
print('>>>', c)

## Closure(클로저) ##
# 클로저는 함수 안에 있는 변수를 기억하고 있음
# 서버 프로그래밍에서 중요한 것은 동시성(Concurrency) 제어인데,
# 동시성 제어란, 같은 메모리 공간에 여러 자원이 접근하기 때문에 제어가 필요한 상태를 말함
# 파이썬은 교착상태 등을 해결하기 위해서 메모리를 공유하지 않고 메세지 전달로 처리하기 위한 역할 수행하는데, 이 때 클로저 사용
# 클로저는 scope 안에 있는 값을 기억하기 때문
# 안정적인 오픈 소스(Tomcat, JBOSS) 등을 사용함.
# 클로저는 데이터는 공유하되 변경되지 않는(Immutable, Read Only) CASE 구조를 적극적으로 사용 -> 함수형 프로그래밍과 연결
# 클로저는 불변자료구조 및 atom(원자성), STM -> 멀티스레드(Coroutine) 프로그래밍에 강점을 제공
# 이 때 멀티스레드를 사용하지 않고 코루틴을 사용함
# 클로저를 알아야 데코레이터, 코루틴을 이해할 수 있음
# 클로저는 상태를 기억함 -> 여러 명이 같이 사용할 수 있고..의 동시성 제어

a = 100
print(a + 100)
print(a + 1000) # a 의 값은 고정되어 있음

# 결과를 누적하려면? 함수를 사용 -> ex sum
print(sum(range(1, 51)))
print(sum(range(51, 101)))


# 예제
# 클래스를 선언하는데, 계속 인자를 넣어 호출할 때마다 값을 포함해 평균값을 출력하는 클래스를 선언해보자

class Averager:
    def __init__(self):
        self._series = []

    # 클래스를 함수처럼 사용 가능
    def __call__(self, v):
        self._series.append(v)
        print(f'inner >> {self._series} / {len(self._series)}')
        return sum(self._series) / len(self._series)


averager_cls = Averager()
print(dir(averager_cls)) # call 구현된 것 확인 : 함수로써 호출 가능
print(averager_cls(10)) # 클래스 인스턴스를 함수처럼 실행하고 있음
print(averager_cls(30))
print(averager_cls(50))

# 결과적으로 Averager 라고 하는 클래스가
# 인자를 넣어 실행될 때마다 특정 배열에 값이 계속 누적되어 기억함


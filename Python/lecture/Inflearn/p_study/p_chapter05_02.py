"""
클로저 기초(Closure)
- 파이썬 변수 범위(Scope)
- Global 선언
- 클로저 사용 이유
- Class -> Closure 구현
"""
# 클로저 기초
# 파이썬의 변수 범위(scope)

def func_v1(a):
    print(a)
    print(b)

func_v1(10) # b는 선언되지 않았으므로 error

# Ex2
b = 20
def func_v2(a):
    print(a)
    print(b)

func_v2(10) # 10, 20 이 선언이 됨

# Ex3
c = 30

def func_v3(a):
    global c
    print(a)
    print(c) # 안에 같은 이름이 있을 때는 local 변수로 인식됨을 확인
    c = 40

print(">> ", c)
func_v3(10)
print('>>>', c)

# Closure(클로저) 사용 이유
# 서버 프로그래밍 -> 동시성(Concurrency) 제어 -> 같은 메모리 공간에 여러 자원이 접근 -> 교착상태(Dead Lock)
# 메모리를 공유하지 않고 메세지 전달로 처리하기 위한 역할 수행
# 클로저는 공유하되 변경되지 않는(Immutable, Read Only) 적극적으로 사용 -> 함수형 프로그래밍
# 클로저는 불변자료구조 및 atom, STM -> 멀티스레드(Coroutine) 프로그래밍에 강점
# 클로저는 상태를 기억함

a = 100
print(a + 100)
print(a + 1000)

# 결과 누적(함수 사용)
print(sum(range(1, 51)))
print(sum(range(51, 101)))

# 클래스 이용


class Averager:
    def __init__(self):
        self._series = []

    # 클래스를 함수처럼 사용 가능
    def __call__(self, v):
        self._series.append(v)
        print(f'inner >> {self._series} / {len(self._series)}')
        return sum(self._series) / len(self._series)


average_cls = Averager()
print(dir(average_cls)) # call 구현된 것 확인 : 함수로써 호출 가능
print(average_cls(10)) # 함수처럼 실행하고 있음
print(average_cls(30))
print(average_cls(50))


# chapter05-03
# 외부에서 호출된 함수의 변수값, 상태(reference) 복사 후 저장 -> 후에 접근 가능하도록 도와줌

# 파이썬 변수 범위(Scope)

# Closure 사용
def closure_ex1():
    # Free variable.
    # 클로저 영역
    series = [] # 함수가 리턴이 되면(average) 원래는 series 변수가 소멸되는데, 클로저 영역의 자유 영역
                # 은 소멸되지 않는 것이 핵심

    def averager(v):
        series.append(v)
        print(f"inner >>> {series}, {len(series)}")
        return sum(series) / len(series)
    return averager

avg_closure1 = closure_ex1()
print(avg_closure1(10))
print(avg_closure1(30))
print(avg_closure1(50)) # 자유 변수에 누적됨을 확인

# 클로저 형태의 클래스를 선언하던지, 클로저를 선택해서 개발하는 것은 개발자의 몫
# 클로저에서 자유 변수를 어떻게 취급하는지 확인해보자

# function inspection
print(dir(avg_closure1))
print(dir(avg_closure1.__code__)) # co 가 붙은 것들이 있음을 확인 ex) co_freevars...
print(avg_closure1.__code__.co_freevars) # series 가 자유변수임을 확인
print(avg_closure1.__closure__[0].cell_contents) # series 의 값을 확인 가능

# 잘못된 클로저 사용 예

def closure_ex2():
    # Free variable
    cnt = 0
    total = 0
    def averager(v):
        cnt += 1
        total += v
        return total / cnt
    return averager


avg_closure2 = closure_ex2()
avg_closure2(10) # 예외 발생

def closure_ex3():
    # Free variable
    cnt = 0
    total = 0
    def averager(v):
        nonlocal cnt, total # free variable 변수를 사용한다고 선언
        cnt += 1
        total += v
        return total / cnt
    return averager

avg_closure3 = closure_ex3()
avg_closure3(10) # 정상 출력!
avg_closure3(20)
avg_closure3(30)

# 함수 내에서 global 변수를 사용하는 것은 좋은 코드는 아님
# 함수 내에서는 왠만하면 local variable 로 선언하는 것이 좋음
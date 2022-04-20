# 코루틴에 값 보내기
def number_coroutine():
    while True:
        x = (yield)
        print(x)

# next 함수로 코루틴의 코드를 최초로 실행하여 yield 위치까지 도착.
# 이후 send 함수를 통해 값을 코루틴에 보내면, 보낸 값을 사용하여 내부 로직이 작동한 후,
# 다음 yield 위치까지 도착하는 로직 구조.

# 코루틴에서 바깥으로 값 전달하기
def sum_coroutine():
    total = 0
    while True:
        x = (yield total)
        total += x


co = sum_coroutine()
print(next(co))
print(co.send(1))
print(co.send(2))
print(co.send(3))

# 코루틴 종료.
# 코루틴 강제 종료. close()

def number_coroutine2():
    try:
        while True:
            x = (yield)
            print(x, end=" ")
    except GeneratorExit:
        print()
        print("코루틴 종료")


co = number_coroutine2()
next(co)

co.send(1)
co.send(2)
co.send(3)
co.close()

## 코루틴 안에서 예외 값 발생시키기.
def sum_coroutine3():
    total = 0
    try:
        while True:
            x = (yield)
            total += x
    except RuntimeError:
        print("코루틴 종료")
        yield total


co = sum_coroutine3()
next(co)

for i in range(20):
    co.send(i)

co.throw(RuntimeError, "예외로 코루틴 끝내기")

# 퍼스트 클래스 함수(First Class function)
'''
퍼스트 클래스 함수란 프로그래밍 언어가 함수를 first-class citizen 으로 취급하는 것을 뜻함
좀 더 쉽게 설명하자면
-> 함수를 변수에 할당 가능
-> 함수 자체를 함수의 return 값으로 전달 가능
-> 함수를 인자로 전달 가능
하다는 것을 의미한다.
'''

# 실습을 통해 더 쉽게 이해해 보도록 하자
def square(x):
    return x * x

print(square(5))

f = square

print(square)
print(f)

# 둘다 메모리 주소값이 return(같은 값)
# 그렇다면, f도 진짜 함수처럼 호출할 수 있는지 확인해 보자
f(5)

# f(5) 구문으로 square 함수를 호출한 것을 볼 수 있음
# 위에서 언급했듯이 프로그래밍 언어가 퍼스트클래스 함수를 지원하면
# 금방 해본 것처럼 변수에 함수를 할당할 수 있을 뿐 아니라 인자로써 다른 함수에 전달하거나
# 함수의 리턴값으로도 사용할 수 있음

# 다음 예제를 또 보면서 생각해보자

def my_map(func, arg_list):
    result = []
    for i in arg_list:
        result.append(func(i))
    return result

num_list = [1, 2, 3, 4, 5]
squares = my_map(square, num_list)

print(squares)

# my_map 함수에 square 함수를 인자로 전달한 후 for 루프 안에서
# square 함수를 호출한 것을 볼 수 있다.
# but, 궂이 이렇게 까지 해야할 필요성을 느낄수 있다.
# 사실은 훨씬 더 간단하게 구현할 수 있는 방법은 많다. 그렇다면 왜 이런식으로 first-class
# 함수를 구현해서 사용해야 할까?


# 1. 이미 정의된 여러 함수를 간단히 재활용 할 수 있다.
# 다음 코드를 확인해 보자

def square(x):
    return x * x

def cube(x):
    return x * x * x

def quad(x):
    return x * x * x * x

def my_map(func, arg_list):
    result = []
    for i in arg_list:
        result.append(func(i))
    return result

squares = my_map(square, num_list)
cubes = my_map(cube, num_list)
quads = my_map(quad, num_list)

print(squares)
print(cubes)
print(quads)

# 위의 예제와 같이 이미 정의되어 있는 함수 square, cube, quad 와 같은 여러개의 함수나
# 모듈이 있다고 가정했을 때 my_map과 같은 wrapper 함수를 하나만 정의하여
# 기존의 함수나 모듈을 수정할 필요없이 편리하게 사용 가능

def logger(msg):

    def log_message():
        print('Log:', msg)

    return log_message

log_hi = logger('Hi')
print(log_hi)
log_hi()

# 위에 정의된 log_message 함수를 logger 함수의 리턴값으로 리턴하여
# log_hi 라는 변수에 할당한 후 호출한 것을 볼 수 있습니다.
# 여기서 !!!! 특이한 점을 하나 발견할 수 있는데, msg와 같은 함수의 지역변수 값은
# 함수가 호출된 이후에 메모리상에서 사라지므로 다시 참조할 수가 없는데
# msg 변수에 할당됐던 'Hi' 값이 logger 함수가 종료된 이후에도 참조가 되었다는 것이다.
# 이러한 함수를 "closure 함수"라고 부르며 이 함수는 다른 함수의 지역변수를 그 함수가 종료된
# 이후에도 기억을 할 수 있다.

# 정말 log_message가 기억을 하고 있는지, msg 변수를 지역변수로 가지고 있는 logger함수를
# 글로벌 네임스페이스에서 완전히 지운 후 log_message 를 호출시켜보자

def logger(msg):

    def log_message():
        print('Log:', msg)

    return log_message

log_hi = logger('Hi')
print(log_hi)
log_hi()

del logger

try:
    print(logger)
except NameError:
    print('NameError: logger는 존재하지 않습니다.')

log_hi()

# logger가 지워진 뒤에도 log_hi()를 실행하여 log_message가 호출된 것을 볼 수 있음
# closure에 대해서는 다음에 더 다뤄보도록 하자


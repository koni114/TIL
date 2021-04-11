# 데코레이터(Decorator)
# 사전적 의미 그대로, 기존의 코드에 여러가지 기능들을 추가하는 파이썬 구문
# 해당 개념이 어려울 수 있지만, 충분히 쉽게 이해할 수 있다

# 우선 해당 코드를 보자
def outer_function(msg):
    def inner_function():
        print(msg)
    return inner_function

hi_func = outer_function('Hi')
bye_func = outer_function('Bye')

hi_func()
bye_func()

# 위의 코드는 closure의 개념이 들어간 코드이다.
# 충분히 이해가 갈 것이라고 생각된다.
# 데코레이터 코드도 위의 코드와 아주 유사하다.
# ** 다만, 함수를 다른 함수의 인자로 전달한다는 점이 조금 틀리다!
# 다음 데코레이터 예제를 참고해보자

def decorator_function(original_function): #1
    def wrapper_function(): #5
        return original_function() #7
    return wrapper_function#6

def display(): #2
    print("display 함수가 실행됐습니다.") #8

decorated_display = decorator_function(display) #3

decorated_display() #4

# 위의 코드는 다음과 같은 내용을 가지고 있다.

# 1. 데코레이터 함수인 decorator_function 과 일반 함수인 display를
#    #1과, #2에서 정의하였다.

# 2. #3에서 decorated_display라는 변수에 display 함수를 인자로 가지는
#    decorator_function을 실행한 return 값을 할당
#    물론 리턴 값은 wrapper function이 된다.
#    아직 wrapper function은 실행되지 않았다(조심! -> () 안 붙었다)

# 3. #4의 decorated_display()를 통해 wrapper_function이 호출되면
#    #5의 wrapper_function이 호출되고, #7에서 display 함수가 호출되고
#    #8의 print가 호출되고 문자열이 출력된다.

# 도대체 이걸 왜 쓰는것인가..?
# 가장 큰 이유는 기존의 코드를 수정하지 않고도 wrapper 함수를 이용하여
# 여러가지 기능을 추가할 수 있기 때문!!

# 다음 코드 예제를 보자

def decorator_function(original_function):
    def wrapper_function():
        print("{}함수가 호출되기 전 입니다.".format(original_function.__name__))
        return original_function()
    return wrapper_function

def display_1():
    print('display_1 함수가 실행됐습니다.')

def display_2():
    print('display_2 함수가 실행됐습니다.')

display_1 = decorator_function(display_1)
display_2 = decorator_function(display_2)

display_1()
print("-"*20)
display_2()

# 하나의 데코레이터 함수를 만들어 display_1, display_2,
# 두 개의 함수에 기능을 추가 할 수 있음
# but, 일반적으로 위의 구문은 사용하지 않고, "@" 심볼과 데코레이터 함수의 이름을 붙여
# 쓰는 간단한 구문을 사용함.

# 다음 코드와 같이 간소화 시킬 수 있음!

def decorator_function(original_function):
    def wrapper_function():
        print('{} 함수가 호출되기전 입니다.'.format(original_function.__name__))
        return original_function()
    return wrapper_function

@decorator_function
def display_1():
    print('display_1 함수가 실행됐습니다.')

@decorator_function
def display_2():
    print('display_2 함수가 실행됐습니다.')


# display_1 = decorator_function(display_1) -> 필요 없게 된다!
# display_2 = decorator_function(display_2)

display_1()
print("-"*20)
display_2()

# @심볼을 사용한 데코레이터 구문이 추가되어 코드가 조금 더 간단하게 된 것을 알수있다.
# 만약 인수를 가진 함수를 데코레이팅 하고 싶은 경우?

@decorator_function
def display_info(name, age):
    print("display_info({}, {}) 함수가 실행되었습니다.".format(name, age))

display_info('john', 30)

# 다음과 같이 display_info 함수를 실행하면, TypeError가 발생
# why ? -> wrapper_function은 인자를 받지 않는데 2개의 인자가 전달되었다는 타입 에러 발생

# 코드 수정 후 해결 가능!
def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):  #1
        print('{} 함수가 호출되기전 입니다.'.format(original_function.__name__))
        return original_function(*args, **kwargs)  #2
    return wrapper_function


display()
print("-"*20)
display_info('John', 25)

# 여기서 주의해야 할 점은, decorator_function을 수정했을 때,
# 다시 @ 심볼을 reading 해야한다

# 궁금한 것은 original_function <- display_info('John', 25)으로 들어가는 것 아닌가?
# 그러면 wrapper_function의 인자로 original_function 의 인자를 받을 필요가 없는것이 아닐까?
# 나중에 알아보자..

# 데코레이터는 이런 함수 형식 말고도 클래스 형식을 사용할 수도 있음

class DecoratorClass:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, *args, **kwargs):
        print('{} 함수가 호출되기 전입니다.'.format(self.original_function.__name__))
        return self.original_function(*args, **kwargs)

@DecoratorClass
def display_1():
    print('display_1 함수가 실행됐습니다.')

@DecoratorClass
def display_info(name, age):
    print("display_info({}, {}) 함수가 실행되었습니다.".format(name, age))

display_1()
print("-"*20)
display_info('John', 20)

# 위의 결과 처럼, DecoratorClass로 변경하니 decorator_function을 사용하는 것과 똑같은 결과가 출력
# 하지만, 클래스 형식의 데코레이터는 잘 사용하지 않고, 보통 함수 형식이 많이 사용
# 클래스 형식도 있다는 점만 알아두자

# 사실.. 이해는 할 수 있지만, 이 걸 어떻게 프로젝트에 응용하지..? 라는 생각이 들 것이다.
# 다음 예제를 통해 실제 프로젝트에서 데코레이터가 어떻게 쓰이는지 보자

# 데코레이터는 로그를 남기거나 유저의 로그인 상태등을 확인하여 로그인 상태가 아니면
# 로그인 페이지로 리다이렉트(redirect)하기 위해 많이 사용

# 또한 프로그램의 성능을 테스트하기 위해서도 많이 쓰임
# 리눅스나 유닉스 서버 관리자는 스크립트가 실행되는 시간을 측정하기 위해
# date와 time 명령어를 많이 사용

# 데코레이터를 이용해서 스크립트 실행 시간을 측정할 수 있는 로깅 기능을 만들어보자.
import datetime
import time

def my_logger(original_function):
    import logging
    logging.basicConfig(filename='{}.log'.format(original_function.__name__)
                        , level=logging.INFO)

    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        logging.info(
            '[{}] 실행결과 args - {}, kwargs - {}'.format(timestamp, args, kwargs))
        return original_function(*args, **kwargs)

    return wrapper

@my_logger
def display_info(name, age):
    time.sleep(1)
    print("display_info({}, {}) 함수가 실행됐습니다.".format(name, age))

display_info('John', 25)




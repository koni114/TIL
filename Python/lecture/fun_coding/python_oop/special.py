# 다른 변수에 함수 할당 가능
def calc_square(digit):
    return digit * digit

calc_square(2)
func1 = calc_square
print(calc_square)
func1(2)

# 함수가 할당된 변수는 동일한 함수처럼 활용 가능
# func1 이라는 변수는 calc_square 함수를 가리키고,
# calc_square와 마찬가지로 인자도 넣어서 결과도 얻을 수 있음
# 완전 calc_square와 동일
print(func1)  #- 주소값 동일
func1(2)     #- 결과 4

class MyClass:
    def my_class(self):
        print("안녕")
        pass

object1 = MyClass()
my_class1 = object1.my_class
my_class1()

# 함수를 다른 함수에 인자로 넣을 수도 있음
def calc_square(digit):
    return digit * digit

def calc_plus(digit):
    return digit + digit

def calc_quad(digit):
    return digit * digit * digit * digit

def list_square(function, digit_list):
    result = list()
    for digit in digit_list:
        result.append(function(digit))
    print(result)


num_list = [1, 2, 3, 4, 5]
list_square(calc_square, num_list)
list_square(calc_plus, num_list)
list_square(calc_quad, num_list)


def logger(msg):
    message = msg

    def msg_creator():
        print('[HIGH LEVEL]: ', message)

    return msg_creator

log1 = logger('Dave Log-in')
print(log1)
log1()

def html_creator(tag):
    def text_wrapper(msg):
        print('<{0}>{1}<{0}>'.format(tag, msg))
    return text_wrapper

h1_html_creator = html_creator('hi')
h1_html_creator('H1 태그는 타이틀을 표시하는 태그입니다.')

#############
## closure ##
#############


def outer_func(num):
    # 중첩 함수에서 외부 함수의 변수에 접근 가능
    def inner_func():
        print(num)
        return '안녕'

    return inner_func


closure_func = outer_func(10)  #- First-class function
closure_func()


def calc_square(digit):
    return digit * digit


def calc_power_3(digit):
    return digit * digit * digit


def calc_quad(digit):
    return digit * digit * digit * digit


print(calc_square(2))
print(calc_power_3(2))
print(calc_quad(2))

def calc_power(n):
    def power(digit):
        return digit ** n
    return power

power2 = calc_power(2)
power3 = calc_power(3)
power4 = calc_power(4)

print(power2(2))
print(power3(2))
print(power4(2))

###############
## decorator ##
###############
import datetime


def datetime_decorator(func): # <-- 데코레이터 이름, func가 이 함수 안에 넣을 함수가 됨

    def wrapper():
        print(' time ' + str(datetime.datetime.now()))
        func()
        print(datetime.datetime.now())

    return wrapper

#- 데코레이터 적용
@datetime_decorator
def logger_login_david():
    print("David login")

@datetime_decorator
def logger_login_anthony():
    print("anthony login")

@datetime_decorator
def logger_login_tina():
    print("Tina login")

logger_login_david()
logger_login_anthony()
logger_login_tina()

# decorator 함수 정의
def outer_func(function):
    def inner_func():
        print("decorated added")
        function()
    return inner_func

@outer_func
def log_func():
    print("logging")


# 파라미터가 있는 함수에 Decorator 적용
def outer_func(function):
    def inner_func(digit1, digit2):
        if digit2 == 0:
            print("cannot be divided with zero")
            return
        return function(digit1, digit2)
    return inner_func

@outer_func
def divide(digit1, digit2):
    return digit1 / digit2

#- closure function 개념 이용
inner_func = outer_func(divide)
inner_func(10, 10)

def type_checker(function):
    def inner_func(digit1, digit2):
        if (type(digit1) != int) or (type(digit2) != int):
            print("only integer support")
            return
        return function(digit1, digit2)
    return inner_func

@type_checker
def divide(digit1, digit2):
    return(digit1, digit2)



def general_decorator(function):
    def wrapper(*args, **kwargs):
        print("function is decorated")
        return function(*args, **kwargs)
    return wrapper

@general_decorator
def calc_square(digit):
    return digit * digit

@general_decorator
def calc_plus(digit):
    return digit + digit

@general_decorator
def calc_quad(digit1, digit2, digit3, digit4):
    return digit1 * digit2 * digit3 * digit4

print(calc_square(2))
print(calc_plus(2))
print(calc_quad(10, 11, 12, 13))


def decorator1(function):
    def wrapper():
        print("decorator1")
        function()
    return wrapper


def decorator2(function):
    def wrapper():
        print("decorator2")
        function()
    return wrapper

@decorator1
@decorator2
def hello():
    print("hello")


def h1_tag(function):
    def func_wrapper(self, *args, **kwargs):
        return "<h1>{0}</h1>".format(function(self, *args, **kwargs))
    return func_wrapper


class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @h1_tag
    def get_name(self):
        return self.first_name + ' ' + self.last_name


davelee = Person('Lee','Dave')
print(davelee.get_name())

def decorator(num):
    def outer_wrapper(function):
        def inner_wrapper(*args, **kwargs):
            print('decorator1 {}'.format(num))
            return function(*args, **kwargs)
        return inner_wrapper
    return outer_wrapper

def print_hello():
    print("hello")

print_hello = decorator(1)(print_hello)

@decorator(1)
def print_hello():
    print("hello")

print_hello()

my_list = [1, 2, 3, 4, 5]
print(next(my_list))       #- error -> iterator 객체가 아님

my_list = [1, 2, 3, 4, 5]
print(my_list)
iter_list = iter(my_list)
next(iter_list)

iterator_my_list = iter(my_list)
next(iterator_my_list)


# Counter class    -> num을 입력받는 iterable 객체 클래스
# Counter_Iterator -> iterator 객체 클래스

class Counter:
    def __init__(self, stop, multiple):
        self.current = 0
        self.stop = stop
        self.multiple = multiple

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.stop:
            return_value = self.current
            self.current += self.multiple
            return return_value
        else:
            raise StopIteration

counter_iter = iter(Counter(17, 5))
next(counter_iter)

### iterator - 협업과제2
# - 다음 dataset은 이름을 가지고 있음(타이타닉호 승선자 명단)
# - string에서 Mr, Miss, Mrs 정보를 출력해서 각각 Male, Female 출력해주는 데코레이터 작성
# - 해당 데코레이터를 활용해서 이름 정보 리스트 변수를 넣어, 이름을 출력하는 함수를 작성
# - dataset과 이름에서 Mr. Miss. Mrs 정보를 추출하는 코드는 다음 코드를 참고

from sklearn import datasets
import re
import pandas as pd
titanic = pd.read_csv('train.csv')
Name = list(titanic.loc[:,'Name'])

p = re.compile('([A-Za-z]+)\.')
for name in Name:
    matched = p.search(name)
    print(matched.group())


def check_male_or_female(function):
    def inner_func(*args):
        import re
        p = re.compile('([A-Za-z]+)\.')
        matched_value = p.search(*args)
        return function(matched_value)
    return inner_func

@check_male_or_female
def test(name):
    print(name)

########################
## 파이썬 comprehension ##
########################

dataset = [4, True, 'Dave', 2.1, 3]
int_data = [num for num in dataset if type(num) == int]
print(int_data)

int_data = [1, 1, 2, 3, 3, 4]
square_data_set = {num * num for num in int_data}
print(square_data_set)

id_name = {1:"Dave", 2:'David', 3:'Anthony'}
name_id = {key:name for key, name in id_name.items() if key > 1}
print(name_id)

def str_data():
    data = 'hi Dave'
    for item in data:
        return item

char = iter(str_data())
next(char)

def str_data():
    data = 'hi Dave'
    for item in data:
        yield item

char = iter(str_data())
next(char)

# list comprehension의 예
square_data = [num ** 2 for num in range(5)]
print(type(square_data))
print(square_data)
print(sum(square_data))

# generator expression의 예
square_data = (num ** 2 for num in range(5))
print(type(square_data))
print(square_data)
print(sum(square_data))


print(sum(square_data))

square_data = (num ** 2 for num in range(5))
for num in range(2):
    print(next(square_data))

# 다시 for loop를 돌리면?

for num in square_data:
    print(num)


# 파이썬 특수 문법(데코레이터, 이터레이터등)
## chapter01 - 중첩 함수(Nested function)
- 함수 내부에 정의된 또 다른 함수
- 중첩함수는 해당 함수가 정의된 함수 내에서 호출 및 반환 가능
- 함수 안에 선언된 변수는 함수 안에서만 사용 가능한 원리와 동일
~~~python
def outer_func():
    print('call outer_func function')

    def inner_func():
        return 'call inner_func function'

    print(inner_func())

outer_func()

# 결과
# call outer_func function
# call inner_func function
~~~
- 중첩함수는 함수 밖에서는 호출 불가
- <b>중첩 함수에서 외부 함수의 변수에 접근 가능</b>
~~~python
def outer_func(num):
    # 중첩 함수에서 외부 함수의 변수에 접근 가능
    def inner_func():
        print(num)
        return 'complex'

    return inner_func

fn = outer_func(10)
print(fn())

#- 결과
# 10
# complex
~~~

## chapter02 - First-class function
- First-class object
  - 해당 언어 내에서 일반적으로 다른 모든 개체에 통용가능한 동작(operation)이 지원되는 개체를 의미
  - 이동작은 주로 함수의 인자로 전달되거나, 함수의 return값이 되거나, 수정되고 할당되는 것들을 전제로 함
  - 예를들어 list, str, int 등의 자료형들은 모두 first-class object임
  - <b>파이썬에서는 함수도 일급 객체!</b>
- First-class function
  - First-class 함수: 함수 자체를 인자로 다른 함수에 전달
  - 다른 함수의 결과값으로 리턴, 함수를 변수에 할당할 수 있는 함수 
- 파이썬에서는 모든 것이 객체
- 파이썬 함수도 객체로 되어 있어서, 기본 함수 기능 이외 객체와 같은 활용이 가능  
  (파이썬의 함수들은 First-class 함수로 사용 가능)
- 지금까지 배운 언어의 맥락과는 뿌리가 다른 사고 - 함수형 프로그래밍에서부터 고안된 기법
~~~python
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
func1(2)      #- 결과 4

class MyClass:
    def my_class(self):
        print("안녕")
        pass

object1 = MyClass()
my_class1 = object1.my_class
my_class1()
~~~
- 함수를 다른 함수에 인자로 넣을 수도 있음
~~~python
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
~~~
- 함수의 결과값으로 함수를 리턴할 수도 있음
~~~python
# 예제 1
def logger(msg):
    message = msg

    def msg_creator():
        print('[HIGH LEVEL]: ', message)

    return msg_creator

log1 = logger('Dave Log-in')
print(log1)
log1()

# 예제 2
def html_creator(tag):
    def text_wrapper(msg):
        print('<{0}>{1}<{0}>'.format(tag, msg))
    return text_wrapper

h1_html_creator = html_creator('hi')
h1_html_creator('H1 태그는 타이틀을 표시하는 태그입니다.')

#- 출력
<hi>H1 태그는 타이틀을 표시하는 태그입니다.<hi>
~~~

## chapter03 - Closure function
- 함수와 해당 함수가 가지고 있는 데이터를 함께 복사, 저장해서 별도 함수로 활용하는 기법으로 First-class 함수와 동일
- 외부 함수가 소멸되더라도, 외부 함수 안에 있는 로컬 변수 값과 중첩함수(내부함수)를 사용할 수 있는 기법
~~~python
def outer_func(num):
    # 중첩 함수에서 외부 함수의 변수에 접근 가능
    def inner_func():
        print(num)
        return '안녕'

    return inner_func


closure_func = outer_func(10)  #- First-class function
closure_func()
~~~
- 위의 예제에서 closure_func이 바로 closure임
- `closure_func = outer_func(10)` 에서 outer_func 함수는 호출 종료
- `clousre_func()` 은 결국 inner_func 함수를 호출
- `outer_func(10)` 호출 종료시 num 값은 없어졌으나, closure_func()에서 inner_func이 호출되면서  
  이전의 num값(10)을 사용함
~~~python
del outer_func 
~~~
- 심지어 outer_func 함수를 아예 삭제해버려도 fn(), 즉 `inner_func()` 의 num값 10은 살아있음
- 언제 closure를 사용할까? 
  - closure는 객체와 유사
  - 일반적으로 제공해야할 기능(method)가 적은 경우, closure를 사용하기도 함
  - 제공해야 할 기능이 많은 경우는 class를 사용하여 구현
~~~python
# closure 적용 전
def calc_square(digit):
    return digit * digit


def calc_power_3(digit):
    return digit * digit * digit


def calc_quad(digit):
    return digit * digit * digit * digit


print(calc_square(2))
print(calc_power_3(2))
print(calc_quad(2))

# closure 적용 후
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
~~~

## chapter04 - 데코레이터(decorator)
- 함수 앞 뒤에 기능을 추가해서 손쉽게 함수를 활용할 수 있는 기법
- Closure function을 활용
~~~python
@decorate_func
def function():
    print("what is decorator function?")
~~~
- 여러 함수에 동일한 기능을 @데코레이터 하나로 간편하게 추가할 수 있음
- 예를 들어 파라미터가 있는 함수에 파라미터 유효성 검사가 필요할 때
  - 파라미터가 있는 함수가 있을 때마다, 유효성 검사 코드를 넣기가 불편
  - 만약 유효성 검사 코드 수정이 필요하다면 관련 함수를 모두 수정해야 하므로 매우 불편
- 데코레이터 작성법
~~~python
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
~~~
- Nested function, Closure function과 함께 데코레이터를 풀어서 작성해보자
- 먼저 데코레이터를 사용하지 않고 nested function과 closure function을 이용하여 데코레이터 만들어보기
~~~python
# decorating할 함수
def log_func():
    print("logging")

# 원래 함수 -> nested function과 closer 개념을 이용한 decorator 작성
def outer_func(function):
    def inner_func():
        print("decoration added")
        function()
    return inner_func

log_func()
outer_func(log_func)()

#- 결과
logging
decoration added
logging
~~~
- 위의 결과를 한번에 데코레이터로 작성하면,
~~~python
@outer_func
def log_func():
    print("logging")

log_func()
~~~
- 파라미터가 있는 함수에 데코레이터 적용하기
  - 중첩함수에 꾸미고자 하는 함수와 동일하게 파라미터를 가져가면 됨  
~~~python
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
~~~
- quiz: 초간단 연습
  - type checker 데코레이터 만들기(인자 유효성 검사)
  - digit1, digit2를 곱한 값을 출력하는 함수 만들기
  - type_checker 데코레이터로 digit1, digit2가 정수가 아니면 only integer support 출력하고 끝냄
  - if(type(digit1) != int) or if(type(digit2) != int)   
~~~python 
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

divide(1, 1)
~~~

### 파라미터에 관계없이 모든 함수에 적용 가능한 Decorator 만들기
- 파라미터는 어떤 형태이든 결국 (*args, **kwargs)로 표현 가능
- 데코레이터의 내부 함수 파라미터를 (*args, **kwargs)로 작성하면 어떤 함수이든 데코레이터 적용 가능
~~~python
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
~~~
- 한 함수에 데코레이터 여러개 지정하기
  - 한 함수에 여러 개의 데코레이터 지정 가능(여러 줄로 @데코레이터 써주면 됨)
  - <b>데코레이터를 나열한 순서대로 실행됨</b>
~~~python
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

hello()
# decorator1
# decorator2
# hello
~~~

### method decorator
- 클래스의 method에도 데코레이터 적용 가능
  - <b>클래스 method는 첫 파라미터가 self이므로 이 부분을 데코레이터 작성시에 포함시켜야 함</b>
~~~python
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
~~~

### 파라미터가 있는 Decorator 만들기(심화)
- decorator에 파라미터를 추가할 수 있음
- 중첩 함수의 하나 더 깊게 두어 생성 가능
~~~python
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
print_hello()

@decorator(1)
def print_hello():
    print("hello")

print_hello()
~~~

## 이터레이터(interator)
- 몇몇 특수한 데이터 집합은 내부의 각 데이터로 분리해서 처리할 수 있음
- 예) list, set, dictionary 등의 컬렉션(collection)
  - 문자열: 문자열을 이루는 각 문자 Sequence
- 이와 같은 컬렉션(collection), Sequence 등을 iterable 객체(iterable object)라고 함
- <b>간단히 for문으로 각 데이터를 탐색할 수 있는 데이터 집합</b>
~~~python
for num in [1, 2, 3, 4, 5]
    print(num)

for char in "David Lee"
    print(char)
~~~
- iterable 과 iterator
  - iterable 객체 : iterator를 리턴할 수 있는 객체
    - 이터레이터를 리턴할 수 있는 객체 ex) list, string..
  - iterator
    - 순차적으로 다음 데이터를 리턴할 수 있는 객체
    - iterator는 내장 함수 next 함수 사용해서, 순환하는 다음 값을 반환함
    - 더이상 next할 객체가 없으면 error 발생
- 내장 함수 iter()
  - iterator 객체를 생성할 수 있음
~~~python
my_list = [1, 2, 3, 4, 5]
print(next(my_list))       #- error -> iterator 객체가 아님

my_list = [1, 2, 3, 4, 5]
print(my_list)
iter_list = iter(my_list)
next(iter_list)
~~~
- 내장 함수 `next()`
  - iterator의 다음 값, 즉 순환하는 값을 반환
  - 더이상 순환할 값이 없으면 StopIteration 발생
- for 구문과 iterator
  - for 구문 사용시, 파이썬은 매번 next함수로 iterator의 다음 값을 읽어내는 것
  - StopIteration 발생할 때까지 next 함수를 호출한다고 보면 됨

### Custom 이터레이터 만들기
- 직접 만들 수 있음
  - iterable 객체는 iter 메서드를 가지고 있는 클래스
  - iterator 객체는 next 메서드를 가지고 있는 클래스
- iterable 객체와 iterator 클래스 만들기
~~~python
class Counter:
    def __init__(self, stop):
        self.stop = stop       #- 반복을 끝낼 숫자

    def __iter__(self):        #- iterable 객체는 __iter__ 메서드가 존재함
        return Counter_Iterator(self.stop)


class Counter_Iterator:
    def __init__(self, stop):
        self.current = 0
        self.stop = stop

    def __next__(self):
        if self.current < self.stop:
            return_value = self.current
            self.current += 1
            return return_value
        else:
            raise StopIteration

counter_iterator = iter(Counter(5))
print(next(counter_iterator))
~~~
- 위의 클래스를 두 개로 분리하는 것이 아니라, 하나로 합칠 수 있음
~~~python
class Counter:
    def __init__(self, stop):
        self.current = 0
        self.stop = stop


    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.stop:
            return_value = self.current
            self.current += 1
            return return_value
        else:
            raise StopIteration

counter_iterator = iter(Counter(5))
print(next(counter_iterator))
~~~

### iterator - 협업과제1
- 특정 수와 배수를 입력받아 특정 수의 배수를 특정 수까지 리턴하는 이터레이터 만들기
~~~python
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
~~~

### iterator - 협업과제2
- 다음 dataset은 이름을 가지고 있음(타이타닉호 승선자 명단)
- string에서 Mr, Miss, Mrs 정보를 출력해서 각각 Male, Female 출력해주는 데코레이터 작성
- 해당 데코레이터를 활용해서 이름 정보 리스트 변수를 넣어, 이름을 출력하는 함수를 작성
- dataset과 이름에서 Mr. Miss. Mrs 정보를 추출하는 코드는 다음 코드를 참고
~~~python
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
~~~

## 파이썬 comprehension
- 다른 Sequence로 부터 새로운 Sequence를 만들 수 있는 기능

### list comprehension
- `[출력표현식 for 요소 in 입력Sequence [if 조건식]]`
- 입력 Sequence는 Iteration이 가능한 데이터 Sequence 혹은 컬렉션
- `[if 조건식]`은 실제 리스트 괄호가 아니라, 옵션(넣어도되고 안넣어도되고)이라는 의미
- 컴프리핸션이라는 용어는 꼭 기억하자
~~~python
# 종류가 다른 데이터에서 정수형만 가지고 오기
dataset = [4, True, 'Dave', 2.1, 3]
int_data = [num for num in dataset if type(num) == int]
print(int_data)
~~~

### Set comprehension
- `{출력표현식 for 요소 in 입력Sequence [if 조건식]}`
- 입력 Sequence로부터 조건에 맞는 새로운 Set 컬렉션을 리턴
~~~python
int_data = [1, 1, 2, 3, 3, 4]
square_data_set = {num * num for num in int_data}
print(square_data_set)

# 결과
[16, 1, 4, 9]
~~~

### Dictionary comprehension
- `{Key:Value for 요소 in 입력Sequence [if 조건식]}`
~~~python
iid_name = {1:"Dave", 2:'David', 3:'Anthony'}
name_id = {key:name for key, name in id_name.items() if key > 1}
print(name_id)
~~~

## 파이썬 제너레이터(Generator)
- iterator를 만들어주는 기능
- generator를 이해하기 위해 yield 키워드를 이해하자
- yield란
  - return은 결과값을 리턴하고, 함수를 종료
  - yield는 yield라고 적은 곳에서 잠시 함수 실행을 멈추고 호출한 곳에 값을 전달
    - 해당 함수는 현재 실행된 상태를 계속 유지
    - 따라서, 다시 해당 함수를 호출하면 현재 실행된 상태를 기반으로 다음 코드를 실행
~~~python
def str_data():
    data = 'hi Dave'
    for item in data:
        yield item

char = iter(str_data())
next(char)
~~~

### Generator Expression
- Generator Comprehension 이라고도 함
- List comprehension과 형식 유사
  - List Comprehension은 앞뒤를 [] 대괄호로 표현
  - Generator Expression() 둥근 괄호로 표현 
- 실제 컬력션 데이터를 리턴하지 않고, 표현식만 유지
  - yield 방식으로 실제 호출할 때 관련 데이터 리턴(lazy operation)
~~~python
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

#- 여기서 한번더 sum(square_data)를 수행하면, 모든 데이터를 다 리턴했으므로, 더이상 리턴할 데이터가 없음
print(sum(square_data))

~~~python
- 다음과 같이 활용 가능함을 꼭 기억하자!
~~~psquare_data = (num ** 2 for num in range(5))
for num in range(2):
    print(next(square_data))

# 다시 for loop를 돌리면?
for num in square_data:
    print(num)
~~~
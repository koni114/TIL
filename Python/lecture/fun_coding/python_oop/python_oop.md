# python 객체 지향 프로그래밍
## chapter01 - 프로그래밍 언어론
- 컴파일러 : 고급언어로 작성된 코드를 한번에 기계어로 변환하는 프로그램 ex) JAVA, C
- 인터프리터: 고급언어로 작성된 코드를 한줄씩 기계어로 변환하는 프로그램 ex) Python, R

## chapter02 - 객체지향 프로그래밍
- 객체지향 프로그래밍
  - 객체(object) 단위로 데이터와 기능(함수)를 하나로 묶어서 쓰는 언어
- 객체지향 프로그래밍 핵심
  - class --> 자동차 설계도
    - attribute와 method를 갖는 데이터 타입
    - attribute는 변수와 유사
    - method는 함수와 유사  
- object?
  - 선언된 클래스(설계도)를 기반으로 만들어진 실체(instance) 
- <b>객체지향 프로그래밍 작성 방법</b>
  - 클래스 설계(attribute와 method 구성)
  - 설계한 클래스를 기반으로 클래스를 코드로 작성
  - 클래스를 기반으로 필요한 객체 생성
  - 해당 객체의 attribute와 method를 조작하여 프로그램 수행 

## chapter03 - 간단실습
- 파이썬 클래스의 method는 항상 첫 번째 파라미터로 self를 사용
- 인자가 필요없을 때에도 self 사용
- 클래스의 attribute 내부 접근시, self.attribute명으로 접근

## chapter04 - 생성자와 소멸자
- 생성자(__init__)
  - method이므로 첫 번째 인자는 self로 설정
  - 생성자에서는 보통 해당 클래스가 다루는 데이터를 정의 
- 소멸자(__del__)
  - 클래스 소멸시 호출 

## chapter05 - 객체지향(public, private, protected)
- 정보 은닉 방식
  - class의 attribute, method에 대해 접근을 제어할 수 있는 기능  
- private -> protected -> public
  - private으로 선언된 attribute, method는 해딩 클래스에서만 접근 가능
  - protected : 해당 클래스 또는 해당 클래스를 상속받은 클래스에서만 접근 가능
  - public : public으로 선언된 attribute, method는 어떤 클래스라도 접근 가능

### 파이썬에서의 private, protected, public
- public
  - java, c++ 언어 등의 객체지향 언어와는 달리, 파이썬에서의 모든 attribute, method는 기본적으로 public
  - 즉, 클래스 외부에서 attibute, method 접근 가능(사용 가능) 
- protected
  - 해당 속성의 앞에 _(single underscore)를 붙여서 표시만 함
  - <b>실제 제약되지는 않고 일종의 경고 표시로 사용됨</b>
~~~python
class Quadrangle:
    def __init__(self, width, height, color):
        self._width = width
        self._height = height
        self._color = color

    def get_area(self):
        return self._width * self._height

    def _set_area(self, width, height):
        self._width = width
        self._height = height



square = Quadrangle(5, 5, "black")
print(square.get_area())
print(square._width)                
square._width = 10
print(square.get_area())
square._set_area(3, 3)
print(square.get_area())
~~~ 
- private
  - <b>__를 붙이면 실제로 해당 이름으로 접근 허용 안됨</b>
  - 실제로는 __를 붙이면, 해당 이름이 `__classname__` 해당 속성 또는 메소드 이름으로 변경되기 때문 
~~~python
class Quadrangle:
    def __init__(self, width, height, color):
        self.__width = width
        self.__height = height
        self.__color = color

    def get_area(self):
        return self.__width * self.__height

    def __set_area(self, width, height):
        self.__width = width
        self.__height = height

square = Quadrangle(5, 5, "black")
dir(square)
~~~
- 다음을 확인 가능
~~~python
'_Quadrangle__color',
'_Quadrangle__height',
'_Quadrangle__set_area',
'_Quadrangle__width',
~~~
- 다음과 같이 접근시 에러 발생
  - `AttributeError: 'Quadrangle' object has no attribute '__set_area'` 
~~~python
square = Quadrangle(5, 5, 'black')
print(sqaure.__set_area(10, 10))
print(sqaure.get_area())
print(sqaure.__width)
~~~

## chapter06 - 상속
### Class Inheritance(상속)
- 추상화(abstraction)
  - 여러 클래스에 중복되는 특성, 메서드를 하나의 기본 클래스로 작성하는 작업
- 상속(Inheritance)
  - 기본 클래스의 공통 기능을 물려받고, 다른 부분만 추가 또는 변경
  - 기본 클래스는 부모 클래스, Parent, Super, Base class라고 부름
  - 기본 클래스 기능을 물려받는 클래스는 자식 클래스, Child, Sub, Derived class 라고 부름   
  - 부모 클래스가 둘 이상인 경우는 다중 상속이라고 부름

### 클래스와 객체간의 관계 확인
- `isinstance(객체, 클래스)`
~~~python
print(isinstance(figure1, Figure))
print(isinstance(square, Figure))
print(isinstance(figure1, Quadrangle))
print(isinstance(square, Quadrangle))

# 결과
True
True
False
True
~~~

### Method Override
- 부모 클래스의 method를 자식 클래스에서 재정의(override)
- <b>자식 클래스에서 부모 클래스의 메서드와 이름만 동일하면 메서드 재정의가 가능함</b>  
  Java/C는 인자까지 동일해야 override 가능

### 자식 클래스에서 부모 클래스 메서드 호출 : super, self
- `super().[부모 클래스의 method 호출]`
~~~python
class Person(object):
    def work(self):
        print('work hard')


class Student(Person):
    def work(self):
        print('Study hard')

    def parttime(self):
        super().work()


student1 = Student()
student1.work()
student1.parttime()

# 결과
Study hard
work hard
~~~

### 자식 클래스에서 부모 클래스 메서드 확장하는 방법
- 부모 클래스 메서드 기능에 추가적인 기능 필요한 경우
  - 부모 클래스 메서드는 그대로 이용하면서 자식 클래스 메서드에서 필요한 기능만 정의
  - `[상속받은부모클래스명].[메서드명]` 을 호출하고, 필요한 기능 추가 정의
~~~python
class Person(object):
    def work(self):
        print('work hard')


class Student(Person):
    def work(self):
        Person.work(self)   #- 부모 클래스 메서드 호출
        print('Study hard')
~~~

### 추상 클래스 사용하기
- 메서드 목록만 가진 클래스, 상속받은 클래스에서 해당 메서드를 구현해야 함
- 예를 들어 게임에서 모든 캐릭터는 공격하기, 이동하기의 공통 기능을 가지고 있음ㄴ
  - 공통 기능을 추상 클래스로 만들고, 각 세부 기능은 해당 메서드에서 구현
- 사용법
  - abc 라이브러리를 가져옴(`from abc import *`)
  - 클래스 선언시 () 괄호 안에 `metaclass = ABCMeta`를 지정 
  - 해당 클래스에서 메서드 선언시 상단에 @abstractmethod를 붙여줘야 함 
~~~python
from abc import *
class Character(metaclass=ABCMeta):
    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def move(self):
        pass


class Elf(Character):
    def attack(self):
        print("practice the black art")

    def move(self):
        print("fly")
~~~

## chapter07 클래스 속성과 메서드
### 클래스 변수와 인스턴스 변수
- 클래스 변수
  - 클래스 정의에서 메서드 밖에 존재하는 변수
    - 해당 클래스를 사용하는 모두에게 공용으로 사용되는 변수
    - 클래스 변수는 클래스 내외부에서 "클래스명.변수명" 으로 엑세스 가능  
- 인스턴스 변수
  - 클래스 정의에서 메서드 안에서 사용되면서 "self.변수명"처럼 사용되는 변수
  - <b>각 객체별로 서로 다른 값을 가짐</b>
  - 클래스 내부에서는 self.인스턴스변수명을 사용하여 엑세스, 클래스 밖에서는 객체명.인스턴스변수명으로 엑세스 
~~~python
class Figure:
    count = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        Figure.count += 1

    def __del__(self):
        Figure.count -= 1

    def calc_area(self):
        return self.width * self.height
~~~

### instance method, static method, class method
- instance method
  - 해당 객체 안에서 호출(지금까지 다룬 self.메서드 명을 의미함)
  - 해당 메서드를 호출한 객체에만 영향을 미침
  - 객체 속성에 접근 가능
- static method
  - 객체와 독립적이지만, 로직상 클래스 내에 포함되는 메서드
  - self 파라미터를 갖고 있지 않음
  - <b>객체 속성에 접근 불가</b>
  - <b>정적 메서드는 메서드 앞에 @staticmethod 라는 Decorator를 넣어야 함</b>
  - 클래스명.정적메서드명 또는 객체명.정적메서드명 둘 다 호출가능 
~~~python
class Figure(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calc_area(self):
        return self.width * self.height

    @staticmethod
    def is_sqaure(rect_width, rect_height):
        if rect_width == rect_height:
            print("정사각형이 될 수 있습니다")
        else:
            print("정사각형이 될 수 없는 너비/높이 입니다.")
~~~
- class method
  - 해당 클래스 안에서 호출(해당 클래스로 만들어진 객체에서 호출되는 것이 아니라, 클래스 자체에서 호출)
  - self 파라미터 대신, cls 파라미터를 가짐
  - 클래스 변수 접근 가능하며, cls 클래스 변수명으로 엑세스 가능. 단 객체 속성/메서드는 접근 불가
  - <b>클래스 메서드는 메서드 앞에 @classmethod라는 Decorator를 넣어야 함</b>
  - 클래스명.클래스메서드명 또는 객체명.클래스메서드명 둘 다 호출 가능


## chapter08 다형성(polymorphism)
- 같은 모양의 코드가 다른 동작을 하는 것
- 키보드의 예
  - push(keyboard) : 키보드를 누룬다는 동일한 코드에 대해 ENTER, ESC, A 등 실제 키에 따라 동작이 다른 것을 의미
  - 다형성은 코드의 양을 줄이고, 여러 객체 타입을 하나의 타입으로 관리가 가능하여 유지보수에 좋음 
  - <b>Method Override</b>도 다형성의 한 예

### 예1 - 메서드명을 동일하게 하여 같은 모양의 코드가 다른 동작을 하게 함
~~~python
class Person(object):
    def __init__(self, name):
        self.name = name

    def work(self):
        print(self.name + " works hard !")

class Student(Person):
    def work(self):
        print(self.name + " study hard !")
~~~

## 연산자 중복 정의(Operator Overloading)
- 객체에서 필요한 연산자를 재정의 하는 것
- 연산자 중복을 위해 미리 정의된 특별한 메서드 존재: __로 시작하여 __로 끝나는 특수 함수
- 해당 메소드들을 구현하면, 객체에 여러가지 파이썬 내장 함수나 연산자를 재정의하여 사용 가능 

### 예1) 연산자 중복을 사용하여 높이와 너비를 각각 더하는 객체 클래스 정의
~~~python
class Figure:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Quadrangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __add__(self, second):
        return Quadrangle(self.width + second.width, self.height + second.height)

rectangle1 = Quadrangle(2, 3)
rectangle2 = rectangle1 + Figure(2, 3)
rectangle2.width
rectangle2.height
~~~
- `__len__` : 연산자 길이 len(class)
- `__getitem__` : 연산자 A[index] - 리스트
~~~python
def __getitem__(self, index):
    if index == 0:
        print(1)
    else:
        print(2)
~~~
- `__str__` : 문자열 변환 : str 
- `__mul__` : 연산자 곱셈
~~~python
def __mul__(self, num):
    return Quadrangle(self.width * num , self.height * num) 
~~~
- 객체 주소 확인하기 : `is`, == 연산자 이해하기
  - is(객체명) : 객체가 가리키는 주소값
  - is와 == 연산자 차이
    - is: 가리키는 객체 자체가 같은 경우 True
    - ==: 가리키는 값들이 같은 경우 True  

### quiz
- 사전조건: Keyword 클래스를 생성
  - 클래스 인자로 영어 단어 한개를 받음
  - attribute: 영어 단어
  - method : 연산자 오버로딩 - len(): 영어 단어 길이 리턴
- quiz1
  - Keyword 클래스로 10개의 임의 영어 단어를 가지고 각각 객체로 만들어서 하나의 리스트에 넣음
- quiz2
  - 영어 단어 길이를 기준으로 리스트 정렬
  - __len__(self) 정의
  - sorted 함수와 lambd로 길이 순 정렬 기법
- quiz3
  - 영어 단어의 두 번쨰 알파벳을 기준으로 리스트를 정렬하기
  - __getitem__(self, key) 정의하기     
~~~python
class Keyword(object):
    def __init__(self, word):
        self.word = word

    def __len__(self):
        return len(self.word)

    def __getitem__(self, index):
        return self.word[index]

    def get_word(self):
        return self.word


test_list = ['hello', 'world', 'my', 'name', 'is', 'heo', 'jae', 'hun', 'haha', 'hehe']
obj_list = [Keyword(word) for word in test_list]
obj_list_1 = sorted(obj_list, key=lambda x: len(x), reverse=True)
obj_list_2 = sorted(obj_list, key=lambda x: x[1])
[obj.get_word() for obj in obj_list_1]
[obj.get_word() for obj in obj_list_2]
~~~

## chapter10 - 다중 상속
- 다중 상속: 2개 이상의 클래스를 상속받는 경우
- 상속 받은 모든 클래스의 attribute와 method를 모두 사용 가능
~~~python
class PartTimer(Student, Worker):
    def find_job(self):
        print('Find a job')
~~~
- <b>다중 상속된 클래스의 나열 순서가 자식 클래스의 속성 호출에 영향을 줌</b>
- 상속된 클래스 중 앞에 나열된 클래스부터 속성을 찾음
~~~python
lass Person(object):
    def sleep(self):
        print('sleep')


class Student(object):
    def study(self):
        print("study hard !")

    def play(self):
        print('play with friends')


class Worker(Person):
    def work(self):
        print('work hard !')

    def play(self):
        print('drinks alone')


class PartTimer(Student, Worker):
    def find_job(self):
        print('Find a job')

parttimer1 = PartTimer()
parttimer1.study()
parttimer1.work()
parttimer1.play()

# 결과
study hard !
work hard !
play with friends
~~~
- <b>다음 코드는 최상위 클래스 메서드를 두 번 호출하게 되는 문제점이 있음</b> 
~~~python
class Person(object):
    def __init__(self):
        print("I am a person")


class Student(object):
    def __init__(self):
        Person.__init__(self)
        print('I am a student')


class Worker(Person):
    def __init__(self):
        Person.__init__(self)
        print("I am a worker")


class PartTimer(Student, Worker):
    def __init__(self):
        Student.__init__(self)
        Worker.__init__(self)
        print("I am a part-timer and student")

parttimer1 = PartTimer()

# 결과
I am a person
I am a student
I am a person
I am a worker
I am a part-timer and student
~~~
- `super()` 내장함수를 사용하면 위의 문제를 해결할 수 있음
~~~python
class Person(object):
    def __init__(self):
        print("I am a person")


class Student(object):
    def __init__(self):
        super().__init__()
        print('I am a student')


class Worker(Person):
    def __init__(self):
        super().__init__()
        print("I am a worker")


class PartTimer(Student, Worker):
    def __init__(self):
        super().__init__()
        print("I am a part-timer and student")

parttimer1 = PartTimer()

# 결과
I am a person
I am a worker
I am a student
I am a part-timer and student
~~~
- 다양한 상속구조에서 메서드 이름을 찾는 순서는 `__mro__`에 튜플로 정의되어 있음
- MRO: Method Resolution Order의 약자
~~~python
PartTimer.__mro__

# 결과
(__main__.PartTimer,
 __main__.Student,
 __main__.Worker,
 __main__.Person,
 object)
~~~

## chapter10 - 포함(composition)
- 다른 클래스 일부 기능을 그대로 이용하고 싶으나, 전체 기능 상속은 피하고 싶을 때 사용
- <b>Composition or Aggregation 이라고 함</b>
- 상속 관계가 복잡한 경우, 코드 이해가 어려운 경우가 많음
- 컴포지션은 명시적인 선언, 상속은 암시적인 선언

### 컴포지션 예시
~~~python
class Calc:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.calc2 = Calc2(x, y)

    def add(self):
        return self.x + self.y

    def subtract(self):
        return self.x - self.y

    def multiply(self):
        return self.calc2.multiply() # 해당 클래스 객체에 명시적으로 활용


class Calc2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):
        return self.x + self.y

    def multiply(self):
        return self.x * self.y
~~~

### 협업 과제 수행
- 클래스 설계해보기: 게임 캐릭터 클래스 만들기
- attribute : name, health_point, striking_power, defensive_power
- attribute 명시적 입력이 없으면, name = 'yourname', health_point = 100, striking_power = 3  
  defensive_power = 3이 디폴트로 입력되도록 함
- method: info() - 게임 케릭터 name, health_point, striking_power, defensive_power 출력
- 다음 시나리오가 동작할 수 있도록 작성
- 게임 케릭터는 3명이 존재
  - Warrior
    - name : 원하는 이름
    - health_point = 100
    - striking_power = 3
    - defensive_power = 1
  - Elf
    - name: 원하는 이름
    - health_power = 100
    - strking_power = 1
    - defensive_power = 3
  - Wizard
    - name: 원하는 이름
    - health_point = 50
    - striking_power = 2
    - defensive_power = 2        
- 각 3명의 캐릭터는 특별한 메서드를 가짐
  - Warrior
    - attack: 상대방 객체를 입력받아 '칼로 찌르다' 출력  
      상대방의 receive 메서드 호출해서 striking_power 만큼 상대방의 health_point를 낮춤
    - receive: 상대방의 striking_point를 입력으로 받아 자신의 health_point를 그만큼 낮추기  
               health_point가 0 이하면 '죽었음' 출력   
  - Elf
    - attack: 상대방 객체를 입력받아 '마법을 쓰다' 출력  
      상대방의 receive 메서드 호출해서 striking_power 만큼 상대방의 health_point를 낮춤
    - receive: 상대방의 striking_point를 입력으로 받아 자신의 health_point를 그만큼 낮추기  
               health_point가 0 이하면 '죽었음' 출력 
    - wear_manteau : 1번 공격을 막음
  - Wizard
    - attack: 상대방 객체를 입력받아 '마법을 쓰다' 출력  
      상대방의 receive 메서드 호출해서 striking_power 만큼 상대방의 health_point를 낮춤
    - receive: 상대방의 striking_point를 입력으로 받아 자신의 health_point를 그만큼 낮추기  
               health_point가 0 이하면 '죽었음' 출력 
    - use_wizard : 자신의 health_point를 3씩 올려줌
- 각 3명의 캐릭터 객체를 만들어, attack 메서드를 호출해서 한 명의 캐릭터 죽여보기
~~~python
from abc import *
from abc import ABC


class Character(object, metaclass=ABCMeta):
    def __init__(self, name='yourname', health_point=100, striking_power=3, defensive_power=3):
        self.name = name
        self.health_point = health_point
        self.striking_power = striking_power
        self.defensive_power = defensive_power

    def info(self):
        print(self.name, self.health_point, self.striking_power, self.defensive_power)

    @abstractmethod
    def attack(self, obj):
        pass

    @abstractmethod
    def receive(self, obj):
        pass


class Warrior(Character):
    def attack(self, obj):
        print("칼로 찌르다")
        obj.receive(self.striking_power)

    def receive(self, striking_point):
        if self.health_point <= striking_point:
            self.health_point = 0
            print("죽었음")
        else:
            self.health_point = self.health_point - striking_point


class Elf(Character):
    def __init__(self, name='yourname', health_point=100, striking_power=3, defensive_power=3):
        super().__init__(name, health_point, striking_power, defensive_power)
        self.wear_manteau = 1

    def attack(self, obj):
        print("마법을 쓰다")
        obj.receive(self.striking_power)

    def receive(self, obj):
        if self.wear_manteau == 1:
            self.wear_manteau = 0
            pass
        if self.health_point <= obj.striking_power:
            self.health_point = 0
            print("죽었음")
        else:
            self.health_point = self.health_point - obj.striking_power


class Wizard(Elf):
    def use_wizard(self):
        self.health_point += 3


warrior1 = Warrior()
warrior2 = Warrior()
elf1 = Elf(name='efl1', health_point=100, striking_power=1, defensive_power=3)
warrior1.attack(warrior2)
print(warrior2.health_point)
~~~

## chapter12 - 5가지 클래스 설계의 원칙(S.O.L.I.D)
- S - SRP(Single responsibility principle) 단일 책임 원칙
- O - OCP(Open Closed Principle) 폐쇄 원칙
- L - LSP(Liskov Substitution Principle) 리스코프 치환 법칙
- I - ISP(Interface Segregation Principle) 인터페이스 분리 원칙
- D - DIP(Dependency Inversion Principle) 의존성 역전 법칙

### 중복 코드는 제거해라
- 중복 코드는 함수로 만들던지, 클래스 메서드/인터페이스로 만들던지 반드시 하나의 코드로 만드는 것이 중요
- 최적화는 제일 나중에 할 것. 잘돌아가면 bottleneck이 존재할때만

### SRP - 단일 책임 원칙
- 클래스는 단 한개의 책임을 가져야 함(클래스 수정할 이유가 오직 하나여야 함)
- 예) 계산기 기능 구현시, 계산을 하는 책임과 GUI를 나타낸다는 책임을 서로 분리하여 각각 클래스로 설계해야함
~~~python
# 나쁜예
# 학생성적과 수강하는 코스를 한개의 class에서 다루는 예
# 한 클래스에서 두개의 책임을 갖기 때문에, 수정이 용이하지 않음
class StudentScoreAndCourseManager(object):
    def __init__(self):
        scores = {}
        courses = {}

    def get_score(self, student_name, course):
        pass

    def get_courses(self, student_name):
        pass

# 변경예
class ScoreManager(object):
    def __init__(self):
        scores = {}

    def get_scores(self, student_name, course):
        pass


class CourseManager(object):
    def __init__(self):
        courses = {}

    def get_courses(self, student_name):
        pass
~~~

### OCP(Open Closed Principle) 개방 - 폐쇄 원칙
- 확장에는 열려있어야 하고, 변경에는 닫혀있어야 함
- 예) 캐릭터 클래스를 만들 때, 캐릭터마다 행동이 다르다면, 행동 구현은 캐릭터 클래스의 자식 클래스에서 재정의
  - 이경우, 캐릭터 클래스는 수정할 필요 없고(변경에 닫혀 있음)
  - 자식 클래스에서 재정의하면 됨(확장에 대해서 개방됨)
~~~
# 나쁜예
# Circle에 대한 면적 계산은 AreaCaculator에서 수용 불가능
class Rectangle(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Circle:
    def __init__(self, radius):
        self.radius = radius


class AreaCalculator(object):
    def __init__(self, shapes):
        self.shapes = shapes

    def total_area(self):
        total = 0
        for shape in self.shapes:
            total += shape.width * shape.height
        return total


shapes = [Rectangle(2, 3), Rectangle(1, 6)]
calculator = AreaCalculator(shapes)
print("The total Area is : ", calculator.total_area())
~~~
~~~
# 좋은 예
class Rectangle(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2


class AreaCalculator(object):
    def __init__(self, shapes):
        self.shapes = shapes

    def total_area(self):
        total = 0
        for shape in self.shapes:
            total += shape.area()
        return total


shapes = [Rectangle(2, 3), Rectangle(1, 6), Circle(5), Circle(7)]
calculator = AreaCalculator(shapes)
print("The total Area is : ", calculator.total_area())
~~~

### LSP - 리스코프 치환 법칙
- 자식 클래스는 언제든지 자신의 부모 클래스와 교체할 수 있음
- 예시
  - 갤럭시폰 is a kind of 스마트폰
    - 스마트폰은 다른 사람과 전화와 메세지가 가능
    - 스마트폰은 데이터 또는 와이파이를 이용해 인터넷을 사용할 수 있음
    - 스마트폰은 앱 마켓을 통해 앱을 다운 받을 수 있음
  - 위 설명을 갤럭시 폰으로 대체하면 다음과 같음
    - 갤럭시폰은 다른 사람과 전화와 메세지가 가능
    - 갤럭시폰은 데이터 또는 와이파이를 이용해 인터넷을 사용할 수 있음
    - 갤럭시폰은 앱 마켓을 통해 앱을 다운 받을 수 있음     
- 위의 캐릭터 예제를 LSP 원칙을 고려하면 다음과 같음
~~~python
class Character(object, metaclass=ABCMeta):
    def __init__(self, name='yourname', health_point=100, striking_power=3, defensive_power=3):
        self.name = name
        self.health_point = health_point
        self.striking_power = striking_power
        self.defensive_power = defensive_power

    def info(self):
        print(self.name, self.health_point, self.striking_power, self.defensive_power)

    @abstractmethod
    def attack(self, obj):
        pass

    @abstractmethod
    def receive(self):
        pass


    # speical로 퉁침
    @abstractmethod
    def special(self):
        pass
~~~

### ISP - 인터페이스 분리 법칙
- 클래스에서 사용하지 않는 메서드는 분리해야 함  
  인터페이스에서 선언해서 클래스에서 선언해야하는 경우는 인터페이스에서 선언을 하지 않아야 함
- metaclass란?
  - 클래스를 만들기 위해 파이썬에서는 기본 metaclass가 사용
  - 즉, 클래스를 만들기 위해서는 metaclass라는 것이 필요
  - class 생성시, 아무것도 넣지 않으면 기본 파이썬에서 클래스를 만들기 위한 메타클래스가 쓰인다고 보면 됨
  - 추상 클래스 만들시에는 기본 메타클래스로는 생성이 어려우니, 다음과 같이 작성
    - `class Character(metaclass = ABCMeta)`
  - 싱글톤을 위해 기본 메타클래스를 바꾸는 것임
    - `class PrintObject(metaclass = Singleton)`     

### DIP - 의존성 역전 법칙
- 부모 클래스는 자식 클래스의 구현에 의존해서는 안됨
  - 자식 클래스 코드 변경 또는 자식 클래스 변경시, 부모 클래스 코드를 변경해야 하는 상황을 만들면 안됨
- 자식 클래스에서 부모 클래스 수준에서 정의한 추상 타입에 의존할 필요 있음
~~~python
# 나쁜예
# bubble_sort의 이름이 바뀌면, 상속 클래스인 SortManager의 BubbleSort도 바뀌어야 함
class BubbleSort:
    def bubble_sort(self):
        # sorting algorithm
        pass


class SortManager:
    def __init__(self):
        self.sort_method = BubbleSort()

    def begin_sort(self):
        self.sort_method.bubble_sort()
~~~
~~~python
class BubbleSort:
    def sort(self):
        print("bubble_sort")
        # sorting algorithm
        pass


class QuickSort:
    def sort(self):
        print("Quick_sort")
        pass


class SortManager:
    def __init__(self, sort_method):
        self.sort_method = sort_method

    def begin_sort(self):
        self.sort_method.sort()
~~~

## chapter13 디자인 패턴
- 객체 지향 설계 패턴
  - 객체 지향 프로그래밍 설계 경험을 통해 추천되는 설계 패턴을 기술한 것
  - 실제 여러 프로그램을 설계해보면서 문제를 발견하고, 디자인 패턴을 적용해 보아야 이해할 수 있음
  - 현 단계에서는 주요하고 그나마 간단한 패턴을 통해 디자인 패턴이 무엇인지를 이해해보도록 함
- <b>디자인 패턴 적용시 주의할 점</b>
  - 현업에서는 굉장히 디자인 패턴을 좋아하는 개발 조직과, 아예 디자인 패턴을 쓰지 말라고 하는 개발 조직도 있음
  - 디자인 패턴을 쓰면, 코드를 이해하기 힘들어짐
  - 코드는 단순하게 읽기 쉽게 쓰는 것이 유지보수도 더 쉽고, 개발이 쉬울 때가 많음
  - 다만 디자인 패턴을 선호하는 조직에서는 반드시 철저하게 써야함 

### Singleton 패턴
- 클래스에 대한 객체가 단 하나만 생성되게 하는 방법
- 예)
  - 계산기 클래스를 만들고, 여러 파일에 있는 코드에서 필요할 때마다 해당 계산기 객체로 불러서 계산을 하려 함
  - 매번 계산할 때마다 계산기 객체를 만들 필요가 없음
  - 객체 생성시 시간과 메모리를 소비하므로, 불필요한 객체 생성 시간과 메모리 효율을 절약할 수 있음  
- 어떤 객체는 하나만 만들면 되는 객체가 있음
  - 예) 데이터베이스를 연결하고, 데이터베이스를 제어하는 인터페이스 객체
  - 보통 프로그램은 여러 파일로 만드는데, 각 파일에서 해당 객체를 그대로 사용하려면 부득이 동일 클래스로 객체를 만들어야 함
  - 각각 파일마다 객체를 별도로 생성하지 않고, 동일한 객체를 사용하고 싶을 때, 싱글톤이라는 기법으로 프로그램에서 한번 만들어진 동일 객체 사용할 수 있음 
- 싱글톤 코드는 여러가지 방법으로 만들 수 있지만, 이 중 가장 많이 사용되는 코드를 기술
~~~python
class Singleton(type):  #- type 상속 받음
    __instances = {}    #- 클래스의 인스턴스를 저장할 속성

    def __call__(cls, *args, **kwargs):   #- 클래스로 인스턴스를 만들 때 호출되는 메서드
        if cls not in cls.__instances:    #- 클래스로 인스턴스를 생성하지 않았는지 확인
            cls.__instances[cls] = super().__call__(*args, **kwargs) #- 생성하지 않았으면 인스턴스를 생성하여 해당 클래스 사전에 저장

        return cls.__instances[cls] #- class instance 반환


class PrintObject(metaclass=Singleton):
    def __init__(self):
        print("This is called by super().__call__")

#- 결과를 확인해보면 주소값이 같은 인스턴스 임을 확인
object1 = PrintObject()
object2 = PrintObject()
print(object1)
print(object2)
~~~
- 다음과 같이 `__init__`, `__new__`를 이용하여 싱글톤 객체를 생성할 수 있음
~~~python
class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__ is called\n")
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, data):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__ is called\n")
            self.data = data
            cls._init = True

# 결과는 3, 3이 나옴
s1 = Singleton(3)
s2 = Singleton(4)
print(s1.data)
print(s2.data)
~~~

## Observer 패턴
- 객체의 상태 변경시, 관련된 다른 객체들에게 상태 변경을 통보하는 디자인 패턴
- 관찰자(관련된 다른 객체)들에게 비관찰자(해당 객체)의 특정 이벤트 발생을 자동으로 모두 전달하는 패턴
~~~python
class Observer:
    def __init__(self):
        self.observers = list()
        self.msg = str()

    def notify(self, event_data):       #- 핵심은 요기
        for observer in self.observers:
            observer.notify(event_data)

    def register(self, observer):
        self.observers.append(observer)

    def unregister(self, observer):
        self.observers.remove(observer)


class SNSNotifier:
    def notify(self, event_data):
        print(event_data, 'received..')
        print('send sms')


class EmailNotifier:
    def notify(self, event_data):
        print(event_data, 'received..')
        print('send email')


class PushNotifier:
    def notify(self, event_data):
        print(event_data, 'received..')
        print('send push notification')


notifier = Observer()

sms_notifier = SNSNotifier()
email_notifier = EmailNotifier()
push_notifier = PushNotifier()

notifier.register(sms_notifier)
notifier.register(email_notifier)
notifier.register(push_notifier)

notifier.notify('user activation event')
~~~

### Builder pattern
- 생성하는 객체가 하위 객체들을 포함하고 있어 복잡하거나, 구성을 정교하게 할 필요성이 있을 때, 빌더 패턴을 사용해  
  복잡한 유형을 단순화 할 수 있음
- 빌더 패턴을 사용하는 목적은 두 가지로 분리
  - 결합도 분리 --> 생성자에 파라미터를 전달해야 하는 부분이 바뀔 경우
  - 생성자에 전달하는 인수에 의미 부여 --> 생성자를 통한 객체 생성시 어떤 인스턴스를 생성할 것인지 의미부여
- 다른 언어에서는 어렵지만, 파이썬은 간단히 언어 자체에서 해결됨
- 생성자에 들어갈 매개 변수가 복잡하여 가독성이 떨어지고, 어떤 변수가 어떤 값인지 알기 어려움
  - 예) `student('aaron', 20, 180, 180, 'cs', ['data structures', 'artificial intelligence'])` 
- 전체 변수 중 일부 값만 설정하는 경우
  - 예) `Student('aaron', --, 180, 180, ???, ???)` 
- 일반적으로 우리가 설정하는 방법으로 간단히 해결 가능


### Factory pattern
- 객체를 생성하는 팩토리 클래스를 정의하고, 어떤 객체를 만들지는 팩토리 객체에서 결정하여 객체를 만들도록 하는 패턴
- 예) 모바일 플랫폼별 스마트폰 객체 만들기 구현해보기
~~~python
## Factory pattern
class AndroidSmartPhone:
    def send(self, message):
        print("send a message via Android platform")


class WindowsSmartphone:
    def send(self, message):
        print("send a message via Widnow Mobile platform")


class iOSSmartphone:
    def send(self, message):
        print("send a message via iOS platform")


class SmartphoneFactory(object):
    def __init__(self):
        pass

    def create_smartphone(self, device_type):
        if device_type == 'android':
            smartphone = AndroidSmartPhone()
        elif device_type == 'window':
            smartphone = WindowsSmartphone()
        else:
            smartphone = iOSSmartphone()

        return smartphone


smartphone_factory = SmartphoneFactory()
message_sender1 = smartphone_factory.create_smartphone('android')
message_sender1.send('hi')

message_sender2 = smartphone_factory.create_smartphone('window')
message_sender2.send('hi')

message_sender3 = smartphone_factory.create_smartphone('ios')
message_sender3.send('hi')
~~~

## chapter14 - 특별한 파이썬 클래스 작성법(namedtuple)
### collections.namedtuple
- 클래스없이 객체를 생성할 수 있는 방법 - 클래스에 attribute만 있는 경우에 해당
  - tuple 클래스 활용
  - attribute만 있는 클래스의 경우만 해당  
~~~python
import collections

Employee = collections.namedtuple('Person', ['name', 'id'])
employee1 = Employee('Dave', '4011')
print(employee1)
print(type(employee1))

Employee = collections.namedtuple('Person', 'name, id')
employee1 = Employee('Dave', '4011')
print(employee1)
print(type(employee1))
~~~
- Person과 Employee 관계
  - Employee = Person 의미, Employee가 Person이라는 실제 클래스를 참조
  - 헷깔리는 부분으로 보통은 다음과 같이 동일한 클래스 이름을 사용
    - `Employee = collections.namedtuple('Employee', ['name', 'id'])`  
~~~python
Employee = collections.namedtuple('Employee', ['name', 'id'])
employee1 = Employee('Dave', '4011')
print(employee1)
print(type(employee1))
~~~
- 다음과 같이 명시적으로 속성명을 적을 수도 있음
~~~python
Employee = collections.namedtuple('Employee', ['name', 'id'])
employee1 = Employee(name='Dave', id='4011')
print(employee1)
print(type(employee1))
~~~
- 일반적인 튜플처럼 속성 접근(권장하지는 않음. 추후 일반 클래스로 바꾼다면 관련 코드를 모두 변경해야함)

### typing.NamedTuple
- 파이썬 3.6에서 추가된 클래스(collections namedtuple의 개선 방식)
- 파고들면 끝이 없긴 하지만, 가벼운 마음으로 참고
- 가독성이 조금 나아졌다고 함
~~~python
from typing import NamedTuple
class Employee(NamedTuple):
    name: str
    id: int = 3 #- default 값 선언 가능

employee1 = Employee('Guido', 2)
print(employee1)
print(employee1.name, employee1.id)
~~~
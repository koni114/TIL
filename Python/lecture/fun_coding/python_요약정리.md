## 요약 정리
- `isinstance(객체, 클래스)` : 해당 객체가 입력된 클래스의 객체인지 확인
- method override : 부모 클래스의 메소드를 자식 클래스에서 재정의  
  파이썬 같은 경우는 메소드의 파라미터가 동일하지 않아도 됨
- 자식 클래스에서 부모 클래스 메서드 호출: `super().method()`
- 자식 클래스에서 부모 클래스 메서드 확장: `[상속받은부모클래스명].[메서드명]` ex) Person.work(self)
- 추상클래스: 반드시 자식 클래스에서 추상클래스의 메소드를 정의해야 함  
  `@abstractmethod`를 이용해서 정의
- `from abc import *`, `metaclass=ABCMeta`로 지정
- 클래스변수 : 클래스 내에서 공통으로 사용되는 변수  
  클래스변수는 클래스 내에서 `[클래스명].변수명`으로 접근 
- 인스턴스변수 : 클래스 정의에서 메서드 안에서 사용되면서 self.로 정의  
  객체 생성시 입력되는 인스턴스 값에 따라서 달라짐
- instance method 
  - 객체 생성 후 호출 가능
  - 해당 메서드를 호출한 객체에만 영향을 미침
- static method
  - 객체와 클래스에 독립적(`self`, `cls` 명령어를 사용하지 않음)
  - `@staticmethod`라고 데코레이터 넣어야 함
  - `[클래스명].정적메서드명`, `[객체명].정적메서드명` 둘 다 호출 가능
- class method
  - 해당 클래스 안에서 호출, `cls`, 클래스 변수 접근 가능
  - 객체/속성 메서드는 접근 불가
  - `@classmethod`라는 데코레이터 추가 
- overloading, overriding
  - overloading : 동일한 클래스에서 동일한 메서드명을 파라미터만 달리해서 정의하는 것
    - <b>파이썬은 overloading이 없음</b> 
  - overriding : 부모 클래스의 메소드를 자식 클래스에서 메소드명을 동일하게 해서 재정의 하는 것 
- operator overloading : 객체에서 필요한 연산자 재정의  
  연산자 중복을 위해 미리 정의된 특별한 메서드 존재 : `[__메서드명__]`
- 메직 메서드(던더 메소드)
  - `__add__(self, second)` : 두 객체를 더하게 해줌
  - `__len__` : 연산자 길이 ex) len(instance)
  - `__getitem__` : 연산자 A[index] list
~~~python
def __getitem__(self, index):
  if index == 0:
    print(1)
  else:
    print(2)
~~~
  - `__str__`: 문자열 반환 str(instance)
  - `__mul__`: 연산자 곱셈
- 파이썬은 다중 상속 가능, 상속된 순서를 우선순위로 해서 속성을 찾음
- `__mro__`에 다양한 상속구조에서 메서드 이름을 찾는 순서가 정의되어 있음
- 컴포지션(Composition) : 다른 클래스의 기능을 사용하고 싶지만, 전체 기능이 아닌 일부 기능만 사용하고 싶은 경우 사용  
  ex) `self.calc2 = Calc2(x, y)`, `self.calc2.multiply()`
- 5가지 클래스 설계의 원칙(SOLID)
- S - SRP(Single responsibility principle) : 단일 책임 원칙
  - 클래스를 수정할 이유가 오직 하나여야 함(잘 지킬 수는 없음)    
- O - OCP(Open Closed Principle) : 개방 폐쇄 원칙
  - 확장에는 열려있어야 하고, 변경에는 닫혀있어야 함
  - 케릭터 클래스는 수정 x(폐쇄), 자식 클래스에서 재정의(확장)
- L - LSP(Liskov Subsitution Principle) : 리스코프 치환 법칙
  - 자식 클래스는 언제든지 부모 클래스와 교체할 수 있음 
  - ex) 스마트폰 -> 겔럭시폰
- I - ISP(Interface Segregation Principle) : 인터페이스 분리 원칙
  - 클래스에서 사용되지 않는 메서드는 분리해야 함
  - 해당 기능이 필요 없는데도, 인터페이스에서 선언해서 클래스에서 선언해야하는 경우는 인터페이스에서 선언을 하지 않아야 함
- D - DIP(Dependency Inversion Principle) : 의존성 역전 법칙 
  - 부모 클래스는 자식 클래스의 구현에 의존해서는 안됨 
- metaclass: 클래스를 만들기 위해서 필요한 것  
  추상클래스 만들시 기본 메타클래스로는 생성이 어려우니, 다음과 같이 작성  
  `class Character(metaclass = ABCMeta)`
- 디자인 패턴
  - 싱글톤 패턴(singleton pattern) : 클래스에 대한 객체가 하나만 생성되게 하는 방법
- `__call__`: 인스턴스 객체로서 호출시켜 주는 함수 `a = MyClass(); a()`  
- `callable()` : 객체가 호출 가능한지 확인 
- `__new__`: 새로운 인스턴스를 만들기 위해 가장 먼저 호출되는 메서드  
  __new__에서 인스턴스를 반환하지 않으면 __init__은 실행되지 않음  
  사용자가 어떤 목적으로 클래스의 생성 과정에 관여하고 싶을 때 직접 `__new__` 메서드를 구현  
  `__new__`는 클래스에 정의되어 있지 않으면 알아서 object 클래스의 __new__가 호출되어 객체가 생성됨  
  사용자가 클래스의 `__new__`를 오버라이딩 할때는 사용자가 직접 object 클래스의 `__new__` 메서드를 호출해서 객체를 생성하고 생성된 객체를 리턴하는 코드 구현
- singleton 생성 방법 - 1
  - `type` metaclass 상속받음
  - 컨테이너에 인스턴스 존재 여부를 check 해서 singleton 구현
~~~python
class singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]
~~~
- singleton 생성 방법 -2
  - `__new__` 메서드 오버라이딩
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
~~~
- observer 패턴 
  - 객체의 상태 변경시, 관련된 다른 객체들에게 상태 변경을 통보하는 디자인 패턴 
  - `self.observers = list()` -> 다양한 클래스 인스턴스를 담는 컨테이너 선언
  - 이벤트 발생시, 컨테이너의 인스턴스들의 함수에 이벤트 전달하는 형식
- builder 패턴
  - 객체의 생성 방법과 표현 방법을 분리하는 패턴
  - 빌터 패턴을 사용하는 이유는 1. 생성자에 파라미터 전달하는 부분이 바뀌는 경우, 2. 생성자에 전달하는 인수에 의미 부여 두가지
  - 파이썬에서는 간단히 언어 자체에서 해결됨. why? 생성자는 키워드 인자로 지정이 가능하기 때문
- factory 패턴
  - 객체를 생성하는 펙토리 클래스를 정의하고, 어떤 객체를 만들 것인지는 팩토리 객체에서 결정
- `collections.namedtuple` 
  - 특별한 파이썬 클래스 작성법
  - 클래스에 attribute만 있는 경우에 해당
  - 보통 입력되는 인자가 개수가 너무 많아지는 경우 사용
~~~python
Employee = namedtuple('Employee', ['name', 'id'])
~~~
- 3.6부터 추가된 클래스(collections namedtuple의 개선방식)
~~~python
from typing import NamedTuple
class Employee(NamedTuple):
  name: str
  id: int = 3

employee1 = Employee('Guido', 2)
~~~ 
- first-class function : 해당 언어 내에서 일반적으로 다른 모든 개체에 통용가능한 동작이 지원되는 개체를 의미  
ex) 함수의 인자, 리턴값 등 ..
- 데코레이터: 함수 앞 뒤에 기능을 추가해서 손쉽게 함수를 활용할 수 있는 기법  
  closure function을 활용
- iterator, iterable 객체
 - iterable : iterator를 리턴할 수 있는 객체
 - iterator : 데이터를 순차적으로 리턴할 수 있는 객체 
- custom 이터레이터 만들기
  - iterable 객체: iter 메서드를 가지고 있는 클래스
  - iterator 갹체: next 메서드를 가지고 있는 클래스 
- 파이썬 제너레이터(generator)
  - iterator를 만들어 주는 기능
  - generator를 이해하기 위해 `yield` 키워드를 이해
  - `yield`는 `yield`라고 적은 곳에서 잠시 함수 실행을 멈추고 호출한 곳에 값을 전달
- generator expression
  - yield 방식으로 실제 호출할 때 관련 데이터 리턴(lazy operation) 




## chapter02 프로그래밍 언어 선택
- 제네릭이란 파라미터의 타입이 나중에 지정되게 해서 재활용성을 높일 수 있는 프로그래밍 스타일
- 파이썬은 동적 타입 언어이기 때문에 제네릭이 필요 없음. 하지만 동적 타이핑의 장점이자 단점은 얼핏 사용하기엔 매우 편하지만 코드의 복잡도가 높아질수록 혼란을 가중시킨다는 점
- 타입을 아예 명시하지 않으면 가독성을 낮추고 버그 발생 확률이 높아짐
- PEP는 Python Enhancement Proposal의 약자
- 파이썬에서는 구조체가 없을 뿐더러 클래스 또한 데이터 타입을 지정할 수 없어, 구조체와 같은 형태를 정의하려면 namedtuple 을 사용해야 헀음. 하지만 파이썬 3.7부터 dataclass를 지원하며 @dataclass 데코레이션으로 타입 힌트와 함께 활용함으로써 다음과 같이 class를 이용해 구조체 형태로 정의할 수 있음

## chapter03 파이썬
- 네덜란드의 컴퓨터 과학자 귀도 반 로섬이 최초로 개발
- 원칙은 첫째, 읽기 쉬워야 한다. 중괄호로 묶기 보다는 깔끔하게 인덴트로 처리한 공백으로 둘러쌈
- 사용자가 원하는 모듈 패키지를 만들 수 있어야 했으며, 다른 프로그램에서 사용할 수 있게 함

### 인덴트
- 파이썬의 대표적인 특징이기도 한 인덴트는 공식 가이드인 PEP 8에 따라 공백 4칸을 원칙으로 함

### 네이밍 컨벤션
- 자바와 달리 단어를 밑줄로 구분하여 표기하는 Snake Case를 따름
- 직접 작성하는 코드는 소문자 변수명과 함수명을 기본으로 해야함
- 특히 파이썬은 Pythonic Way에 굉장한 자부심이 있어, 카멜 케이스뿐만 아니라 자바 스타일로 코딩하는 것을 지양함
- 파이썬의 PEP 8 및 철학에 따라 스네이크 코딩을 지향한다고 얘기해야 함
- 카멜 케이스(helloWorld), 스네이크 케이스(hello_world), 파스칼 케이스(HelloWorld)

### 타입 힌트
- 파이썬은 동적 타입 언어이지만, 타입을 지정할 수 있는 타입 힌트가 PEP 484 문서에 추가됨
- 이 기능은 파이썬 3.5 부터 사용이 가능
- 타입 힌트를 지정한다고 할지다로 여전히 동적으로 할당될 수 있으므로 주의가 필요함

### 리스트 컴프리헨션
- 리스트 컴프리헨션이란, 기존 리스트를 기반으로 새로운 리스트를 만들어내는 구문
- 가독성을 위하여 map, filter 대신 리스트 컴프리핸션을 사용하는 것이 좋음. 또한 성능도 조금 더 좋음

### 제너레이터
- 루프의 반복 동작을 제어할 수 있는 루틴 형태를 말함
- 예를 들어 숫자 1억 개를 만들어내 계산하는 프로그램을 작성한단고 가정할 때, 어딘가에 1억개를 저장하고 있어야 함. 제너레이터를 사용하면 단순히 제너레이터만 생성해두고 필요할 때 언제든지 숫자를 만들어낼 수 있음 
- `yield` 구문을 사용하면 제너레이터를 리턴할 수 있음
- yield는 제너레이터가 여기까지 실행 중이던 값을 내보낸다는 의미로, 중간값을 리턴한 다음 함수는 종료되지 않고 계속해서 맨 끝에 도달할 때까지 실행됨
~~~python
def get_natual_number():
    n = 0
    while True:
        n += 1
        yield n

g = get_natual_number()
for _ in range(100):
    print(next(g)) 
~~~

### range
- 파이썬 3.x 버전 이후 `range()` 함수가 제너테리어 역할을 하는 range 클래스를 리턴하는 형태로 변경됐고, `xrange()`는 사라짐
- 즉 다음의 두 코드를 비교해서 기억해야함
~~~python
a = [n for n in range(1000000)]
b = range(1000000)

len(a)
len(b)

type(a)
type(b)

sys.getsizeof(a)
sys.getsizeof(b)

# Out[45]: 8697456
# Out[46]: 48
~~~
- 미리 생성하지 않은 값은 인덱스에 접근이 안될 거라 생각할 수 있으나 인덱스로 접근 시에는 바로 생성하도록 구현되어 있기 때문에 다음과 같이 리스트와 거의 동일한 느낌으로 불편 없이 사용 가능 

### enumerate
- enumerate는 "열거하다"의 뜻으로, 여러 가지 자료형을 인덱스를 포함한 enumerate 객체로 리턴함

### 나눗셈 연산자
- `//`는 정수형을 결과로 리턴하면서 내림(Floor Division) 연산자의 역할을 함
- 다시 말해 몫(Quotient)를 구하는 연산자임
~~~python
5 // 3
5 % 3
divmod(5, 3) #- 몫과 나머지 연산이 동시에 return
~~~

### print
~~~python
#- print 함수는 항상 줄바꿈을 함
print("A1", "A2")
print("A1", "A2", sep=',')
print("A1", "A2", end=' ')
a = ['A', 'B']
print(" ".join(a))
#- f-string 을 통한 출력 방법이 좋음: 3.6+ 에서만 지원
idx, fruit = 1, "Apple"
print(f"{idx + 1}: {fruit}")
~~~

### pass
- 코딩을 하다 보면 일단 코드의 전체 골격을 잡아두고 내부에서 처리할 내용을 차근차근 생각하며 만들겠다는 의도로 다음과 같이 코딩하는 경우가 있음
- 이럴 때는 pass를 통해 오류를 막아야 함 pass는 mockup 인터페이스부터 구현한 다음에 추후 구현을 진행할 수 있게 함

### locals
- 로컬에 선언된 모든 변수를 조회할 수 있는 기능이므로, 디버깅에 많은 도움이 됨
- `pprint` 모듈에 함수를 사용시, 줄바꿈 처리를 해줘 가독성이 좋음
~~~python
import pprint
pprint.pprint(locals())
~~~

### 구글 파이썬 스타일 가이드
- 구글에서 정한 가이드인데, PEP 8에서는 설명하지 않는 좋은 코드를 위한 지침이 여럿 있음
- 함수의 기본 값으로 가변 객체를 사용하지 않아야 함. 함수가 객체를 수정하면 기본값이 변경되기 때문
- 대신 Immutable 객체를 사용하는 것이 좋으며, None을 명시적으로 할당하는 것도 좋은 방법
- True, False를 판별할 때도 implicit인 방법을 사용하는 것이 간결하고 가독성이 높음
~~~python
#- Yes
if not users:
    print("no users")
if foo == 0:
    self.handle.zero()
if i % 10 == 0:
    pass

#- No
if len(users) == 0:
    pass
if foo is not None and not foo:
    pass
if not i % 10:
    pass
~~~
- 최대 줄 길이는 80자로 암묵적으로 정함

## chapter04 빅오, 자료형
- 빅오(big-O)란 입력값이 무한대로 향할 때 함수의 상한을 설명하는 수학적 표기 방법
- 빅오로 시간 복잡도를 표현할 때는 최고차항만을 표기, 계수는 무시함
- 추이에 따른 빅오 표기법의 종류는 다음과 같음
  - O(1)
  - O(logn)
  - O(n)
  - O(nlogn): 병합 정렬를 비롯한 효율적인 정렬 알고리즘이 해당됨 
  - O(n^2): 버블 정렬과 같은 알고리즘이 해당
  - O(2^n): n^2보다 훨씬 큼. 피보나치 수를 재귀로 계산하는 알고리즘
  - O(n!): 각 도시를 방문하고 돌아오는 가장 짧은 경로를 찾는 외판원 문제
- 빅오는 시간 복잡도 외에 공간 복잡도를 표현하는 데에도 널리 쓰임. 또한 알고리즘은 '시간과 공간이 트레이드오프' 관계임. 즉 실행 시간이 빠른 알고리즘은 공간을 많이 사용하고, 공간을 적에 차지하는 알고리즘은 실행 시간이 느리다는 얘기

### 상한과 최악
- 빅오(O)는 상한(upper bound)를 의미함. 이외에도 하한을 나타내는 빅오메가, 평균을 의미하는 빅세타가 있는데, 학계와 달리 업계에서는 빅세타와 빅오를 하나로 합쳐서 단순화해서 표현하려는 경향이 있음
- <b>여기서 중요한 점은 상한을 최악의 경우와 혼동하는 것인데, 빅오 표기법은 정확하게 쓰기에는 너무 길고 복잡한 함수를 '적당히 정확하게' 표현하는 방법일 뿐, 최악의 경우/평균적인 경우의 시간 복잡도와는 아무런 관계가 없는 개념임</b>
- 빅오 표기법은 주어진 경우의 수행 시간 상한을 나타냄

### 분할 상환 분석
- 시간 또는 메모리를 분석하는 알고리즘 복잡도를 계산할 때, 알고리즘 전체를 보지 않고 최악의 경우만 살펴보는 것은 지나치게 비관적이라는 이유로 분할 상환 분석이 등장하게 된 계기가 됨
- 분할 상환 분석이 유용한 대표적인 예로 '동적 배열'을 들 수 있는데, 동적 배열에서 더블링이 일어나는 일은 어쩌다 한 번 뿐이지만, 이로 인해 '아이템 삽입 시간 복잡도는 O(n)'라고 얘기하는 것은 지나치게 비관적이며 정확하지도 않음
- 따라서 최악의 경우를 여러 번에 걸쳐 골고루 나눠주는 형태로 알고리즘의 시간 복잡도를 계산할 수 있음

### 병렬화
- 일부 알고리즘은 병렬화를 통해 실행 속도를 높일 수 있음

### 자료형
#### 숫자
- 파이썬에서는 숫자 정수형으로 int만 제공하며, 버전 2.4부터는 int가 충분하지 않으면 자동으로 long으로 변경됨
- 버전 3부터는 아예 Int 단일형으로 통합됨. int는 임의 정밀도를 지원하며, 더 이상 파이썬에서 고정 정밀도 정수형은 지원하지 않음
- bool은 엄밀히 따지면 논리 자료형인데 파이썬에서는 내부적으로 1(True), 0(False)으로 처리되는 Int의 서브 클래스
- int는 object의 하위 클래스이기도 하기 때문에 결국 다음과 같은 구조를 띔  
  object > int > bool

#### 임의 정밀도
- 무제한 자리수를 제공하는 정수열을 말함. 엄청나게 긴 정수를 입력받으면 그것을 잘라서 2^30진법으로 만듬
- 자리수 단위로 구분한 값을 별도로 계산하여 처리하게 됨. 당연히 숫자를 임의 정밀도로 처리하면 계산 속도가 저하됨
- 그러나 숫자를 단일형으로 처리할 수 있으므로 언어를 매우 단순한 구조로 만들 수 있을 뿐만 아니라, 언어를 사용하는 입장에서도 더 이상 오버플로를 고민할 필요가 없어 잘못된 계산 오류를 방지할 수 있음

### 원시 타입(primitive type)
- C는 원시타입, 자바는 원시 타입과 객체를 지원하며, 파이썬은 원시타입을 지원하지 않음
- C나 java는 성능에 대한 우선순위가 높은 언어인 반면에 파이썬은 편리한 기능 제공에 우선순위를 둔 언어이기 때문

### 객체
- 파이썬은 모든 것이 객체임. 이 중에서 크게 불변 객체와 가변 객체로 구분할 수 있음
  - bool : 불변
  - int : 불변
  - float : 불변
  - list : 가변
  - tuple : 불변
  - str : 불변
  - set : 가변
  - dict : 가변

### 불변 객체
- 파이썬은 모든 것이 객체인데, 변수를 할당하는 작업은 해당 객체에 대해 참조를 한다는 의미
- 문자와 숫자도 객체인데, 불변 객체의 차이만 있을 뿐임
- 다음의 실험을 통해 확인해보자
~~~python
10
a = 10
b = a
id(10), id(a), id(b)
 (4392811440, 4392811440, 4392811440)
~~~
- 만약 모두 원시 타입이라면 각각의 값들은 모두 각 메모리의 다른 영역에 위치할 것임
- 하지만 파이썬은 모든 것이 객체이므로, 메모리 상에 위치한 객체의 주소를 얻어오는 id() 함수를 실행한 결과는 놀랍게도 모두 동일함
- 만약 10이 11이 된다면 a 변수와 b 변수 값이 모두 11로 바뀌게 될 것인데, 그러나 그런일은 일어나지 않음
- 숫자와 문자 모두 불변 객체이기 때문. 
  즉 값을 담고 있는 변수는 사실 참조일 뿐이고 실제 값을 갖고 있는 int와 str은 모두 불변 객체임

### 가변 객체
- int, str과는 달리 list는 값이 바뀔 수 있으며, 이 말은 다른 변수가 참조하고 있을 떄 그 변수의 값 또한 변경된다는 뜻 
~~~python
a = [1, 2, 3, 4, 5]
b = a
print(b)
a[2] = 4
print(a)
print(b)

#- [1, 2, 4, 4, 5]
#- [1, 2, 4, 4, 5]
~~~
- 파이썬은 `b = a` 를 통해 a와 b는 동일한 메모리 주소를 가리키게 되지만, `b = 7`로 새로운 값을 할당하게 되면 더 이상 b 변수는 a 변수를 참조하지 않음
- b 변수는 7이라는 새로운 객체를 참조하게 됨

#### is와 ==
- is는 id 값을 비교하는 연산자
~~~python
a = [1, 2, 3]
a == a
a == list(a)
a is a
a is list(a)

#-
# True
# True
# True
# False

import copy
a == copy.deepcopy(a)
a is copy.deepcopy(a)

#- True
#- False
~~~

### 속도
- 파이썬의 문제는 속도인데, 다음의 파이썬 객체 구조는 파이썬이 C나 자바 같은 다른 언어에 비해 느린 이유 중 하나임
- 단순히 정수형 덧셈을 할 때 C는 메모리에서 값을 꺼내 한번 연산하면 끝인 원시 타입에 비해, 파이썬의 객체는 값을 거내는 데만 해도 var -> PyObject HEAD에서 타입코드를 찾는 등의 여러 단계의 부가 작업이 필요함
- 넘파이는 빠른 속도로 유명한데, 넘파이는 C로 만든 모듈이며 내부적으로 리스트를 C의 원시 타입으로 처리하기 떄문

### 자료구조, 자료형, 추상 자료형
- 자료구조는 데이터에 효율적으로 접근하고 조작하기 위한 조직, 관리, 저장 구조를 말함
- 자료형이란 일종의 데이터 속성(attribute)으로서, 컴파일러 또는 인터프리터에게 프로그래머가 데이터를 어떻게 사용하는지를 알려줌. 즉 자료의 유형 자체를 말함
- 자료구조는 원시 자료형을 기반으로 하는 배열, 연결 리스트, 객체 등을 말하며, 자료형의 관점에서 보자면 여러 원시 자료형을 조합한 자료구조는 복합 자료형이 됨
- 추상 자료형은 ADT라고 부르며 자료형에 대한 수학적 모델을 지칭함  
  해당 유형의 자료에 대한 연산들을 명기한 것  
  ADT는 행동만을 정의할 뿐, 실제 구현 방법은 명시하지 않음. OOP에서 추상화를 떠올리면 쉽게 이해가 가는데 필수적인 속성만 보여주고, 불필요한 정보는 감추는 것을 의미함
- ADT의 대표적인 것들은 복소수, 리스트, 스택, 큐, 맵, 우선순위 큐, 집합 등이 있음

## chapter05 리스트, 딕셔너리
- 파이썬에서의 리스트는 말 그대로 순서대로 저장하는 시퀀스이자 변경 가능한 목록(mutable list)를 말함
- 입력 순서가 유지되며, 동적 배열로 구성되어 있음
- 다음은 리스트의 주요 연산과 시간 복잡도
  - `len(a)` : O(1)
  - `a[i]`: O(1)
  - `a[i:j]`: O(k)
  - `elem in a`: O(n)
  - `a.count(elem)`: O(n)
  - `a.index(elem)`: O(n)
  - `a.append(elem)`: O(1)
  - `a.pop()`: O(1)
  - `a.pop(0)`: O(n) 
  - `del a[i]`: O(n)
  - `a.sort()`: O(nlogn)
  - `min(a), max(a)` : O(n)
  - `a.reverse()`: O(n)

### 리스트의 특징
- 파이썬의 리스트는 연속된 공간에 요소를 배치하는 배열의 장점과 다양한 타입을 연결해 배치하는 연결 리스트의 장점을 모두 취한 듯한 형태를 띄며, 실제로 리스트를 잘 사용하기만 해도 배열과 연결 리스트가 모두 필요 없을 정도로 강력함
- CPython에서 리스트는 요소에 대한 포인터 목록(ob_item)을 갖고 있는 구조체(Struct)로 선언되어 있음
- 리스트에 요소를 추가하거나 조작하기 시작하면 ob_item의 사이즈를 조절해 나가는 형태로 구현되어 있음
- 리스트는 객체로 되어 있는 모든 자료형을 포인터로 연결함
- 즉 파이썬이 모든 것이 객체이기 때문에 파이썬의 리스트는 이들 객체에 대한 포인터 목록을 관리하는 형태로 구현되어 있음
- <b>연결 리스트에 대한 포인터 목록을 배열 형태로 관리</b>하고 있으며, 덕분에 파이썬의 리스트는 배열과 연결 리스트를 합친 듯이 강력한 기능을 제공
- <b>즉 다시 강조하면 파이썬의 리스트는 연결 리스트에 대한 포인터 목록을 관리하기 때문에 정수, 문자, 불리언 등 제각기 다양한 타입을 동시에 단일 리스트에서 관리하는 것이 가능</b>
~~~python
a = ['a', 1, True]
~~~
- 이 기능은 매우 강력한데, 각 자료형의 크기는 저마다 다 다르기 때문에 이들을 연속된 메모리 공간에 할당하는 것이 불가능함
- 결국 각각의 객체에 대한 참조로 구현할 수 밖에 없음. 인덱스를 조회하는 데에도 모든 포인터의 위치를 찾아가서 타입 코드를 확인하고 값을 일일이 살펴봐야 하는 추가적인 작업이 필요하기 때문에 필연적으로 속도는 떨어질 수 밖에 없음

### 딕셔너리
- 파이썬의 딕셔너리는 키/값 구조로 되어 있는 딕셔너리를 말하며, 파이썬 3.7+ 부터는 입력 순서가 유지되며, 내부적으로는 해시 테이블(Hash Table)로 구현되어 있음
- 즉 딕셔너리는 해시할 수만 있다면 immutable 객체는 key로 사용할 수 있음. 이 과정을 해싱이라고 함
- 또한 해시 테이블은 입력과 조회가 O(1)임
- 파이썬 3.6+ 부터는 딕셔너리의 메모리 사용량이 개선(20%감소)됨 
- 추가적으로 파이썬에서는 딕셔너리를 효율적으로 사용하기 위한 모듈을 많이 지원하는데, defaultdict, Counter, orderedDict

## chapter06 문자열 조작 
- `[::-1]`로 문자열을 뒤집으면, 코드도 간략하지만 내부적으로 C로 구현되어 있어 훨씬 더 좋은 속도를 기대할 수 있음

### 문자열 슬라이싱
- 파이썬에서는 문자열 슬라이싱이라는 매우 편리한 기능을 제공하는데, 내부적으로 매우 빠르게 동작함
- 위치를 지정하면 해당 위치의 배열 포인터를 얻게 되며, 이를 통해 연결된 객체를 찾아 실제 값을 찾아냄
- 이 과정은 매우 빠르게 진행되므로, 문자열을 조작할 때는 항상 슬라이싱을 우선으로 사용하는 편이 속도 개선에 유리

#### 슬라이싱을 기준으로 한 파이썬 문자열 처리 상대 실행 시간
- 슬라이싱 : 1
- 리스트 reverse() : 5
- reversed() + join(): 6
- for 반복: 12
- while 반복: 21
- 재귀: 54

### 문자열 조작
- `sorted` 함수는 별도의 메모리에 정렬된 배열을 반환하며, `.sort()` 함수는 In-place 함수이므로, 되도록이면 .sort 함수를 사용하는 것이 좋음
- `sorted()`는 key 옵션을 지정해 정렬을 위한 키 또는 함수를 별도로 지정할 수 있음
~~~python
c = ["ccc", "aaaa", "d", "bb"]
sorted(c, key=len)

# Out[31]: ['d', 'bb', 'ccc', 'aaaa']
~~~
- 다음은 함수를 이용해 첫 문자열과 마지막 문자열 순으로 정렬하도록 지정
~~~python
a = ['cde', 'cfc', 'abc']
def fn(s):
    return s[0], s[-1]

print(sorted(a, key=fn))
# ['abc', 'cfc', 'cde']
~~~
- 폰 노이만이 설계한 병합 정렬이 가장 인기있는 정렬 알고리즘 중 하나인데, 이는 퀵소트와 비교했을 때 일정하게(nlogn)의 안정적인 성능을 보이며, 무엇보다 안정 정렬이라는 점에서 많이 선호되는 편
- 퀵소트는 편차가 큰 편
- 파이썬에서의 `sort()` 함수는 팀소트라는 알고리즘을 사용
- 팀소트 알고리즘은 팀 피터스가 2002년도에 파이썬을 위해 C로 구현한 알고리즘이며, "실제 데이터는 대부분 정렬되어 있을 것이다"라고 가정하고 알고리즘을 설계함
- 팀소트는 개별 알고리즘이 아니라 삽입 + 병합 정렬을 휴리스틱하게 적절히 조합해 사용하는 정렬 알고리즘
- 대부분의 경우 정렬이 필요할 때에는 파이썬의 정렬 함수를 사용하는 것이 가장 빠름
- 팀소트는 자바 컬렉션의 공식 정렬 알고리즘으로 적용되기도 함
- 다음은 정렬 알고리즘별 시간 복잡도
  - 퀵 정렬:  최선 nlogn, 평균 nlogn, 최악: n^2
  - 병합 정렬: 최선 nlogn, 평균 nlogn, 최악: nlogn 
  - 팀소트: 최선 n, 평균 nlogn, 최악 nlogn

### 가장 긴 팰린드롬 부분 문자열
- 가장 긴 팰린드롬 부분 문자열을 출력해라
~~~python
#- input: "babad"
#- output: "bab" or "aba"

#- input: "cbbd"
#- output: "bb"
~~~
- 다음 문제는 중앙을 중심으로 확장하는 풀이 방법으로 풀 수 있음
- 2칸, 3칸으로 구성된 투 포인터가 슬라이딩 윈도우 처럼 계속 앞으로 전진해 나가면서 윈도우에 들어온 문자열이 팰린드롬인 경우 그 자리에 멈추고, 투 포인터가 점점 확장하는 식임
- 다음 코드를 확인하면 직관적으로 이해 가능
~~~python
#- 특징 설명
#- 짝수, 홀수를 각각 검사하면서, 슬라이딩 윈도우 진행하는데, 만약 s[left], s[right]가 같으면 인덱스를 확장(left -= 1, right += 1)
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) < 2 or s == s[::-1]:
            return s

        def extend(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left+1:right]

        result = ""
        for i in range(len(s)):
            result = max(result, extend(i, i+1), extend(i, i+2), key=len)
        
        return result
~~~

### 유니코드와 UTF-8
- 초기에 문자를 표현하던 방식은 ASCII 인코딩 방식으로, 1바이트에 모든 문자를 표현함
- 처음 1비트는 체크섬(checksum)으로 제외하여 7비트, 128글자로 문자를 표현했음
- 이렇게 되면 한글이나 한자 같은 문자는 2개 이상의 특수 문자를 합쳐서 표현하곤 했는데, 당연히 이런 방식은 비정상적이며, 경우에 따라서는 깨지거나 제대로 표현되지 않는 경우가 잦음
- 이런 문제를 해결하기 위해 2~4바이트의 공간에 여유 있게 문자를 할당하고자 등장한 방식이 유니코드(Unicode)임
- 그러나 유니코드 자체는 1바이트로 표현 가능한 문자도 2바이트 이상의 공간을 사용하기 때문에 메모리 낭비가 심함
- 따라서 이를 가변 길이 인코딩 방식으로 효율적으로 인코딩하는 대표적인 방식이 UTF-8임
- <b>파이썬이 버전 3으로 넘어오면서 가장 큰 변화 중 하나는 바로 문자열의 처리 방식</b>  
  기존 CPython에서 문자열을 처리하던 `stringobject.c` 는 아예 `unicodeobject.c`
 로 이름과 구현까지 변경되는 큰 변화가 있었음
- 파이썬 2 이전에는 한글을 비롯한 특수문자들이 모두 별도로 인코딩되는 구조여서 콘솔에서 원래 값을 제대로 출력하기가 쉽지 않았음
- 파이썬 3에 이르러서는 문자열은 모두 유니코드 기반으로 전환됐고, 덕분에 많은 부분이 개선됨

### 유니코드의 가변 길이 문자 인코딩 빙식, UTF-8
- 예를들어 Python이라는 영문 문자열을 고정 길이 유니코드 방식으로 표현한다면 다음과 같음
~~~Python
P             y           t           h           o           n
0x50 00 00 00 79 00 00 00 74 00 00 00 68 00 00 00 6f 00 00 00 6e 00 00 00 s
~~~
- 이 방식은 확실히 문제가 있는데, 영문자는 ASCII 코드로도 충분히 표현이 가능하기 때문에 각 문자당 1바이트로도 충분한데, 모든 문자가 4바이트를 차지하기 때문에 사실상 문자마다 3바이트씩 빈 공간으로 낭비되고 있음
- 이러한 문제점을 해결하기 위하여 가변 인코딩 방식이 등장했고 그중 가장 유명한 방식이 UTF-8임
- 그렇다면 UTF-8은 어떤 방식으로 인코딩할까? 다음은 6-3에서 확인할 수 있음
~~~
바이트 수 | 바이트 1 | 바이트 2 | 바이트 3 | 바이트 4
  1      0xxxxxx
  2      110xxxxx 10xxxxxx 
  3      1110xxxx 10xxxxxx  10xxxxxx
  4      11110xxx 10xxxxxx  10xxxxxx 10xxxxxx
~~~
- 시작 비트를 살펴보면 문자의 전체 바이트를 결정할 수 있음
- 첫 바이트의 맨 앞 비트를 확인해서 0인 경우 1바이트, 10인 경우 특정 문자의 중간 바이트, 110인 경우 2바이트, 1110인 경우 3바이트, 11110인 경우 4바이트..
- 총 4바이트로 제한하여 약 100만자 정도를 표현할 수 있게 됨
- 중요한 것은 유니코드 값에 따라 가변적으로 바이트를 결정하여 불필요한 공간 낭비를 절약할 수 있다는 점
- 127 이하라면 1바이트로 표현되며 ASCII 문자는 128개며 이 문자들의 유니코드 값은 동일하므로, 영문, 숫자를 포함한 SCII 문자는 모두 그대로 1바이트에 표현이 가능

## chapter07 배열
- 자료구조는 크게 메모리 공간 기반의 연속(continuous)방식과 포인터 기반의 연결(link) 방식으로 나뉨
- 배열은 이 중에서 연속 방식의 가장 기본이 되는 자료형임
- 연결 방식의 가장 기본이 되는 자료형은 '연결 리스트'임
- 추상 자료형(ADT)의 실제 구현 대부분은 배열 또는 연결 리스트를 기반으로 함  
  예를 들어 Stack은 연결 리스트로 구현하고, queue는 배열로 구현하는 식임
- 배열은 어느 위치에나 O(1)에 조회가 가능하다는 장점이 있는데, 예를 들어 배열에서 4번째 값에 접근하고 싶다면 int 배열이므로 각각 4바이트, (4-1)x4 = 12가 되고, 0x00에서 시작해 12만큼 증가한 16진수는 0x0C가 됨
- 이제 이 주소를 찾으면 해당 메모리에 배치되어 있는 값을 바로 읽어올 수 있음
- 대부분의 프로그래밍 언어는 동적 배열을 지원하며, 자바에서는 ArrayList, C++에서는 std:vector임
- 파이썬에서는 list가 바로 동적 배열 자료형임. 대부분의 동적 프로그래밍 언어들은 아예 정적 배열 자체가 없음. 파이썬도 마찬가지!
- 동적 배열의 원리는 간단한데, 미리 초깃값을 작게 잡아 배열을 생성하고, 데이터가 추가 되면서 꽉 채워지면 늘려주고 모두 복사하는 식임 
- 대개는 Double이라 하여 2배씩 늘려주게 되는데 당연히 모든 언어가 항상 그런 것은 아니며 각 언어마다 늘려가는 비율은 상이함
- 파이썬의 더블링 구조를 살펴보면 Cython의 내부 구현을 살펴보면 동적 배열인 리스트의 구현은 CPython의 `listobject.c`에 정의되어 있음
- 0, 4, 8, 16 .... 순으로 재할당하도록 정의되어 있음
- 이 재할당 비율을 Growth Factor, 즉 '성장 인자'라고 함. 파이썬의 그로스 팩터는 초반에는 2배씩 늘려 가지만, 전체적으로는 약 1.125배로 다른 언어에 비해서는 다소 조금만 늘려가는 형태로 구현되어 있음 
- 파이썬의 동적 배열 자료형인 리스트에 아이템을 삽입할 때, 동적 배열의 용량이 꽉 차게 되면 크기를 늘려나감. 더블링이 필요할 만큼 공간이 차게 되면 새로운 메모리 공간에 더 큰 크기의 배열을 할당하고 기존 데이터를 복사하는 작업이 필요하므로 O(n) 비용이 발생함
- 즉 최악의 경우 삽입 시 O(n)은 되지만 자주 일어나는 일은 아니고, 분할 상환 분석에 따른 입력 시간은 여전히 O(1)임

### 두 수의 합 문제
- 덧셈하여 타겟을 만들 수 있는 배열의 두 숫자 인덱스를 리턴해라
- 풀 수 있는 방법은 여러가지가 있음
  - brute force로 계산: O(n^2)
  - 모든 조합을 비교하지 않고, 타겟에서 첫 번째 값을 뺀 값이 target - n이 존재하는지 탐색하는 문제로 변경  
  시간 복잡도로는 O(n^2)이지만 파이썬에서 in은 매번 값을 비교하는 것에 비해 훨씬 더 빨리 샐행됨
  - 첫 번째 수를 뺀 결과 키 조회: 평균 O(1), 최악 O(n)

### 빗물 트래핑
#### 투 포인터를 최대로 이동
- 가장 높이가 높은 막대 확인. 왼쪽과 오른쪽을 가르는 장벽 역할을 함
~~~python
volume += left_max - height[left]
...
volume += right_max - right[right]
~~~
- 최대 높이의 막대까지 각각 좌우 기둥 최대 높이 left_max, right_max가 현재 높이와의 차이만큼 물 높이 volume을 더해 나감
~~~Python
if left_max <= right_max:
  volume += left_max - height[left]
  left += 1
else:
  volume += right_max - height[right]
  right -= 1
~~~
- 적어도 낮은 쪽은 그만큼 항상 채워질 것이기 때문에, 좌우 어떤 쪽이든 낮은 쪽은 높은 쪽을 향해서 포인터가 가운데로 점점 이동함
- 오른쪽이 크다면 left += 1로 왼쪽이 이동하고, 그렇지 않다면 right -= 1로 오른쪽이 이동함

### 자신을 제외한 배열의 곱
- 배열을 입력받아 output[i]가 자신을 제외한 나머지 요소의 곱셈 결과가 되도록 출력
~~~python
#- n 만에 풀 수 있는 문제
from typing import List
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        result = [1] * len(nums)
        left_value, right_value = 1, 1
        for idx in range(1, len(nums)):
            rev_idx = len(nums) - idx - 1
            left_value = left_value * nums[idx-1]
            right_value = right_value * nums[rev_idx+1]
            result[idx] *= left_value
            result[rev_idx] *= right_value
        return result
~~~

### 파이썬 최댓값과 최솟값
- 최댓값과 최솟값의 초깃값을 지정하는 방법은 여러가지가 있음
- 가장 쉬운 방법은 `sys`를 활용하는 것. 이 모듈을 사용하면 시스템이 지정할 수 있는 가장 높은 값, 낮은 값을 활용할 수 있음
~~~Python
mx = -sys.maxsize
mn = sys.maxsize
~~~
- 또는 `float()` 를 활용해 무한대 값을 지정하는 방법도 있음
~~~python
mx = -sys.maxsize
mn = sys.maxsize
~~~

## chapter08 연결 리스트
- 연결 리스트는 데이터 요소의 선형 집합으로, 데이터의 순서가 메모리에 물리적인 순서대로 저장되지는 않음
- 컴퓨터 과학에서 배열과 함께 가장 기본이 되는 대표적인 선형 자료구조 중 하나로, 다양한 추상 자료형 구현의 기반이 됨
- 동적으로 새로운 노드를 삽입, 삭제하기가 편리
- 연결 구조를 통해 물리 메모리를 연속적으로 사용하지 않아도 되기 때문에 관리도 쉬움
- 데이터를 구조체로 묶어서 포인터로 연결한다는 개념은 여러 가지 방법으로 다양하게 활용
- 실제 컴퓨터의 물리 메모리에는 구조체 각각이 그림 8-1과 같이 서로 연결된 형태로 구성되어 있음
- 메모리 어딘가에 여기저기 흩뿌려진 형상을 띔
- <b>연결 리스트는 특정 인덱스에 접근하기 위해서는 전체를 순서대로 읽어야 하므로 상수 시간 안에 접근할 수 없음. 즉 탐색에는 O(n)이 소요됨</b>
- 반면 시작, 끝 지점에 아이템을 추가하거나 삭제하는 것은 O(1)에 가능


### 팰린드롬 연결 리스트 문제의 제대로 된 풀이법 - 런너(Runner)
- 입력값이 1 -> 2 -> 3 -> 2 -> 1인 연결 리스트에 런너를 적용해 풀이하는 방법
- 런너(Runner) 방법
  - 순서에 따라 2개의 런너, 빠른 런너(Fast Runner)와 느린 런너(Slow Runner)를 각각 출발 시킴
  - 빠른 런너가 도착 할 때, 느린 런너는 중간 지점에 도착함
  - 느린 런너는 중간까지 이동하면서 역순으로 연결 리스트 rev를 만들어 나감
  - 역순으로 만든 rev와 앞으로 진행할 값과 비교하여 같은지 확인해 나가면 됨
- 코드 구현 방법
- 먼저 빠른 런너 fast와 느린 런너 slow의 초깃값은 다음과 같이 모두 head에서 시작
~~~python
slow = fast = head
~~~
- 런너를 이동할 차례인데, 다음과 같이 next가 존재하지 않을 때까지 이동
- 빠른 런너는 2 칸씩, 느린 런너 slow는 한 칸씩 이동
- 그러면서 역순으로 연결 리스트 rev를 생성하는 로직을 slow 앞에 덧붙임 
~~~python
while fast and fast.next:
  fast = fast.next.next
  rev, rev.next, slow = slow, rev, slow.next #- 역순 연결리스트 만드는 구문
~~~
- 역순 연결 리스트는 현재 값을 slow로 교체
- rev.next는 rev가 됨. 즉 앞에 계속 새로운 노드가 추가되는 형태가 됨


### 다중 할당(multiple Assignment)
- 파이썬에서 다중 할당은 2개 이상의 값을 2개 이상의 변수에 동시 할당하는 것을 말함
- 위의 런너 풀이에서 다중 할당을 사용한 바 있음
~~~python
rev, rev.next, slow = slow, rev, slow.next
~~~
- 이 코드를 보면서 의문이 들었을 수 있는데, 왜 두 줄로 분기하여 풀지 않았을까?
- 예를 들어 다음과 같이 쓸 때 분기하여 쓸 수 있음
~~~python
rev, rev.next = slow,rev
slow = slow.next
~~~
- 중요한 것은 위와 같이 두 줄로 분기하였을 때 문제가 풀리지 않는다
- 두 줄로 늘어트릴 경우는 slow와 rev가 동일한 참조가 됨
- 구문 중간에 rev = slow가 있으니 서로 같은 값을 참조하게 되는 것임
- 즉, `=` 구문이 값을 할당하는 것이 아닌 서로 같은 값을 참조하게 되는 이유는 파이썬의 모든 것은 객체며, primitive types는 존재하지 않음
- 문자와 숫자의 경우만 불변 객체라는 점만 다를 뿐이고, `=` 연산자를 활용해 할당을 진행하게 되면 값을 할당하는 것이 아니라 불변 객체에 대한 참조를 할당하게 됨
- 다음의 실험을 보고 생각해보자
~~~python
id(5)
#- 4390087440

a = 5
id(a)
#- 4390087440

b = 5
id(b)
#- 4390087440
~~~
- 5라는 숫자에 대해 숫자 5와 변수 a,b 모두 동일한 ID를 가짐
- 즉 5라는 값은 메모리 상에 단 하나만 존재하며, a,b 두 변수는 각각 이 값을 가리키는 참조라는 의미
- 그럼 만약 5가 6으로 변경된다면 같은 주소 값을 참조하므로, a,b가 모두 6으로 변경될 것 같지만 그렇지 않음
- 그 이유는 숫자는 불변(immutable) 객체이기 때문. 만약 숫자가 아니라 리스트, 딕셔너리와 같은 자료형이라면 내부 값은 바뀌며, 참조하는 모든 값도 바뀌게 됨
- 다시 돌아와서 rev = 1, slow = 2 -> 3이라고 가정해보자
~~~python
rev, rev.next, slow = slow, rev, slow.next
~~~
- <b>위의 구문은 같은 작업이 동시에 일어나기 때문에, 이 모든 작업은 중간 과정 없이 동시에 일어남. 즉 중간 과정 없이 한 번의 트랜잭션으로 끝나게 됨</b> 
- 만약 다음과 같이 썼다면 어떻게 될까? 
~~~python
#- 여기서 slow, fast 를 =로 할당하는 것은 node 자체를 할당하는 것과 같음
#- rev = 1, slow = 2 -> 3
rev, rev.next = slow, rev   #- 결과: rev = 2 -> 1, 중요한 것은 rev = slow
                            #- 동일하게 참조하기 떄문에 slow도 2 -> 1로 변해버림
slow = slow.next            #- slow.next는 1로 변경됨. 따라서 값이 이상해짐
~~~
- 결과적으로 왜 다중 할당을 하는지, 나누지 않고 한 번에 처리해야 하는지 어느 정도 이해할 수 있음

### 두 정렬 리스트의 병합
- 병합 정렬의 마지막 조합과 동일한 방식으로 첫 번째부터 비교하면서 리턴하면 쉽게 풀 수 있는 문제
~~~python
#- l1, l2를 비교했을 때 반드시 작은 값이 l1으로 오도록 비교하는 방법을 말함
class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        #- l1 이 없거나, l1, l2가 있고 l2.val < l1.val 이면 swap
        #- 즉 l1이 없거나 l1.val이 l2.val 보다 작으면 무조건 swap -> 
        if (not l1) or (l2 and l1.val > l2.val):
            l1, l2 = l2, l1
        if l1:
            l1.next = self.mergeTwoLists(l1.next, l2)
        return l1
~~~

### 리스트를 연결리스트로 변경하는 방법
~~~Python
def to_reversed_linkedlist(arr):
  prev = None
  for value in arr:
    node = ListNode(value)
    node.next = prev
    prev = node
  return prev
~~~

### 두 수의 덧셈
#### 자료형 변환으로 풀이
- 연결리스트를 뒤집은 뒤, 문자열로 이어 붙이고 숫자로 변환 후 덧셈
- 다시 연결 리스트로 변경
~~~python
class Solution:
    def addTwoNumbers(self, l1:ListNode, l2:ListNode) -> ListNode:
        first_num_list = self.toList(self.reverseList(l1))
        second_num_list = self.toList(self.reverseList(l2))

        first_num = int("".join((str(e) for e in first_num_list)))
        second_num = int("".join((str(e) for e in second_num_list)))

        return self.toReversedLinkedList(str(first_num + second_num))


    #- linkedList를 reverse 하는 함수
    def reverseList(self, head:ListNode) -> ListNode:
        node, prev = head, None

        while node:
            prev, prev.next, node = node, prev, node.next

        return prev

    #- 연결 리스트를 파이썬의 리스트로 변경
    def toList(self, node):
        list = []
        while node:
            list.append(node.val)
            node = node.next
        return list

    #- list를 linkedlist 로 변경
    def toReversedLinkedList(self, result):
        prev = None
        for r in result:
            node = ListNode(r)
            node.next = prev
            prev = node

        return node
~~~  

#### 잔가산기 구현
- 논리 회로의 전가산기(Full Adders)의 유사한 형태를 구현해보자
- 이진법이 아니라 십진법이라는 차이만 있을 뿐, 자리올림수를 구하는 것까지 가산기의 원리와 거의 동일
- 입력값 A, B, 이전의 자리올림수 이렇게 3가지 입력으로 합(Sum)과 다음 자리올림수 여부를 결정
- 
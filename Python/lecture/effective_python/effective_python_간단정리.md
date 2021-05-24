## effective_python 간단정리
### 1-bytes와 str 차이 알아두기
- 파이썬은 문자열 데이터의 시퀀스 표현방법은 두 가지
  - `bytes`, `str`
- bytes 타입의 인스턴스에는 부호가 없는 8바이트 데이터가 그대로 들어감
- str 인스턴스에는 사람이 사용하는 언어의 문자를 표현하는 유니코드 코드 포인트가 들어있음
- 중요한 것은 str 인스턴스에는 직접 대응하는 이진 인코딩이 없고, bytes에는 직접 대응하는 텍스트 인코딩이 없음
- 두 개를 구분하는 help function을 만들어서 적용해야 함
- `bytes`와 `str`는 연산이 불가능함

### 2-str-format 보다는 f-문자열을 사용하자
~~~python
f_string = f'{key:<5} = {value:.2f}'
f'내가 고른 숫자는 {number: .{places}f}'
~~~

### 3-복잡한 식을 쓰지 말고 help function 사용해라
- 파이썬은 복잡한 한줄 식을 사용할 수 있지만 가독성이 좋지 않음 -> 사용 x
- 복잡한 식을 help function으로 만들자

### 4- 인덱스 사용 대신에 언패킹 사용하자
~~~python
snacks = [('베이컨', 350), ('도넛', 240), ('머핀', 190)]
for rank, (name, calories) in enumerate(snacks):
    print(f"{rank} : {name}은 {calories}입니다.")
~~~

### 5- range보다는 enumerate를 사용해라
- range는 가독성이 떨어질 수 있음(ex) `range(len(list))`). 차라리 enumerate 사용하자

### 6- for나 while 루프 뒤에 else 사용하지 말자
- for/while 뒤에 else를 붙여 사용이 가능한데, else는 루프가 끝나자마자 실행됨 
- 조심해야 할 것은 '루프가 정상적으로 완료되지 않으면' else문을 실행해라 가 아님
- 빈 sequence에 대해서 for loop 실행시, else 블록이 바로 실행됨
- else는 동작의 혼동을 줄 수 있으므로 사용하지 말자
~~~python
for i in range(3):
    print(i)
    break
else:
    print("Else block")

>>>
0

for i in []:
    print("Loop", i)
    break
else:
    print("Else block!")

>>>
Else block!
~~~

### 7- 대입식을 사용해 반복을 피하자
- 대입식을 영어로 assignment expression 이라고 하며, 왈러스 연산자라고도 함
- python 3.8부터 도입되었으며, 다음과 같이 사용하며 반복을 피할 수 있음
~~~python
if count := fresh_fruit.get('레몬', 0):
    print(count)
~~~

### 11-시퀀스 슬라이싱 하는 법을 익혀라
- 두 번째 인덱스는 포함되지 않음
- 범위를 지정한 인덱싱은 인덱싱의 범위가 넘어가도 무시됨
- [:]만 사용하면 리스트가 그대로 복사됨

### 12- 스트라이드와 슬라이스를 한 식에 같이 쓰지 말라 
- 스트라이트: 리스트를 일정한 간격을 두고 슬라이싱 할 수 있는 구문

### 13- 슬라이싱보다는 나머지를 모두 잡아내는 언패킹을 사용하자
- 슬라이싱하면 인덱스 오류 발생 여지 있음
- 이 때는 *식(starred expression)을 사용한 언패킹을 사용
- 코드가 더 짧고, 인덱스 경계 어긋나서 오류 날 여지 줄여줌
- 별표 식은 항상 리스트 인스턴스가 됨
- 별표 식만 사용할 수 없음
- 별표 식에 할당되는 값이 없으면 []이 됨
~~~python
first, * middle, last = [1,2,3,4]
print(f"middle : {middle}")

middle : [2, 3]
~~~
### 14-복잡한 기준을 사용해 정렬할 때는 key 파라미터 사용하자
- `__repr__`: 클래스를 출력시킬 수 있는 함수
- 튜플은 매직 메소드인 __lt__ 정의가 들어 있음.
- 리스트 타입의 `sort` 메소드는 key 함수가 반환하는 값이 서로 같은 경우 리스트에 들어 있던 원래 순서를 그대로 유지해줌
- 같은 리스트에 대해서 서로 다른 기준으로 <b>sort를 여러번 호출해도 된다는 의미</b>
- 정수형에 대해서는 reverse -> 마이너스를 붙여 계산 가능, 나머지 타입은 불가능
~~~python
tools.sort(key=lambda x: x.name)
places.sort(key=lambda x: x.lower())
power.tools.sort(key= lambda x: (x.weight, x.name))
power.tools.sort(key= lambdax : (-x.weight, x.name))
~~~

### 15-딕셔너리 삽입 순서에 의존할 때는 조심해라
- python 3.5버전 이전에는 딕셔너리에 대한 순서를 보장해 주지 않음  
  그 이유는 내장 hash 함수와 인터프리터가 초기에 시작할 때 초기화되는 seed값을 사용하는 해시 테이블 알고리즘으로 만들어졌기 때문
- 실행 시마다 달라지는 seed값 때문에 삽입 순서가 일치하지 않음
- 파이썬 3.6 버전부터는 딕셔너리가 삽입 순서를 보존하도록 동작이 개선됨  
  --> 좋은점: 함수에서 딕셔너리 등을 입력받을 때 디버깅 하기가 편함
- <b>key 삽입과 popitem을 자주해야 한다면, OrderedDict가 더 나음</b>
- 덕 타이핑: 동적 타이핑의 한 종류로, 객체의 변수 및 메소드의 집합이 객체의 타입을 결정한다는 의미
- <b>만약 dict 대신 다른 클래스를 사용해 딕셔너리와 거의 유사한 클래스를 사용한다면, 입력 순서대로 return이 되지 않음(`iter()` 사용시)</b>
- 해결방안은 3가지
  - 입력 순서가 반환 순서로 성립되지 않는다고 가정하고 코드 작성
  - `isinstance`를 사용하여 dict 타입인지 검사
  - type annotation을 사용해서 함수에 입력 파라미터를 dict 디스턴스로 강제하는 것  
    `def get_winner(ranks: Dict[str, int]) -> str:`

### 16- in을 사용하고 딕셔너리 키가 없을 때 KeyError를 처리하기 보다는 get을 사용해라
~~~python
#- in을 사용한 코드문
#- 가독성이 떨어짐
if key in counters:
    count = counters[key]
else:
    count = 0

counters[key] = count + 1
~~~
~~~python
#- get을 사용한 코드문
#- 가독성이 높음
counters[key] = counters.get(key, 0) + 1
~~~
- <b>항상 리스트 파라미터 입력시 참조인지, 복사인지 생각하기</b>
- `setdefault` : 키가 없으면 제공받은 디폴트 값을 키에 입력  
  해당 함수의 문제점은, `setdefault` 함수에 전달된 디폴트 값이 별도로 복사되지 않고 딕셔너리에 참조로 대입됨  
  결과적으로 `setdefault` 함수를 사용하는 것 자체가 지름길인 경우는 드뭄
~~~python
names = votes.setdefault(key, [])
names.append(who)
~~~

### 17- 내부 상태에서 원소가 없을 경우 setdefaultdict보다 defaultdict를 사용해라
- `collections` -> `defaultdict` 함수는 해당 key 값이 없는 경우 default 값을 입력시켜줌
- 키로 어떤 값이 들어올지 모르는 딕셔너리를 만들 때, defaultdict을 사용 가능하다면 사용해라 
~~~python
from collections import defaultdict
data = defaultdict(set)
~~~

### 18- __missing__을 사용해 키에 따라 다른 디폴트 값을 생성하는 방법을 알아두라
- `setdefault`와 `defaultdict` 타입이 처리 못하는 경우가 있을 때 사용
- `setdefault`에서는 default 값이 발생시키는 error에 대처를 못함
- `defaultdict`에서는 default로 입력하는 함수에 파라미터 입력이 안됨
- 이럴 때 `__missing__` 특별 클래스 사용
  - dict 타입의 자식 클래스 만들고
  - `__missing__` 특별 메서드를 구현하면 키가 없는 경우를 처리하는 로직을 커스텀화 할 수 있음
  - key가 dict에 없으면 `__missing__`가 호출됨
  - 키에 해당하는 디폴트 값을 호출해 딕셔너리에 넣어준 다음(`self[key] = value`) 그 값을 반환(`return value`)
~~~python

class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value

pictures = Pictures()
handle = pictures[path]
~~~

### 19-함수가 여러 값을 반환하는 경우 절대로 네 값 이상을 언패킹하지 마라
- 네 값 이상 언패킹 하면 생기는 문제점
  - 순서를 혼동하기 쉬움
  - 함수를 호출하는 부분과 반환 값을 언패킹 하는 부분이 길어 가독성이 나빠짐 
- 더 많은 값을 언패킹 해야 한다면, `namedtuple` 이나 class를 선언하여 반환하자

### 20-None을 반환하기보다는 예외를 발생시켜라
- 함수 내 오류 발생시 None을 return하면 반환 값을 잘못 해석하는 경우가 있음(`if not result`)
- 위의 해결 방안 2가지
  - 반환 값을 길이가 2인 튜플로 분리하는 것(`(True, a/b), (False, None)`)  
  - <b>더 좋은 방법은 `Exception`을 통해 호출한 쪽으로 던져서(`raise`) 호출자가 처리하게 하는 것</b>
~~~python
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('잘못된 입력')


x, y = 5, 2
try:
    result = careful_divide(x, y)
except ValueError:
    print("잘못된 입력")
else:
    print("결과는 %.1f 입니다." % result)
~~~
### 21- 변수 영역과 클로저의 상호작용 방식을 이해해라
- 숫자로 이루어진 list를 정렬하는데, 정렬한 리스트의 앞쪽에는 우선 순위를 부여한 몇몇 숫자를 위치시켜야 한다고 가정
- `numbers`: 숫자 `group`: 우선순위에 포함되는 group
~~~python
def sort_priority(numbers, group):
    def helper(x):
        if x in group:
            return 0, x
        else:
            return 1, x
    return numbers.sort(key=helper)
~~~
- 위의 함수가 정상적이게 작동하는 이유는 세가지
  - 파이썬은 클로저를 지원: `group` 변수에 접근 가능
  - 파이썬 함수는 first-class object임. 따라서 key 인자로 클로저 함수를 전달 가능
  - 파이썬에서 튜플을 포함한 시퀀스는 0번 인덱스 비교 후 같으면 1번 인덱스를 비교하는 default rule을 가지고 있음 
- `nonlocal`, `global` 명령어는 되도록이면 사용하지 말자. 코드가 길어질수록 파악하기가 힘들고, 함수 동작을 더 이해하기 힘들게 함
- 같은 결과를 만들어내는 클래스를 정의해서 사용하자  
  다음의 `__call__` 메서드 + `sort(key=)` 조합은 꼭 기억해두자
- `__call__` 특별 메서드는 인스턴스 자체를 함수처럼 호출될 수 있도록 함
- 클로저 함수 안에 변수를 선언하는 것과, `nonlocal`를 선언하고 참조하는 것은 다른 것임을 꼭 기억하자
~~~python
class Sorter:
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return 0, x
        else:
            return 1, x


sorter = Sorter(group)
numbers.sort(key=sorter)
~~~
### 22-변수 위치 인자를 사용해 시각적인 잡음을 줄이자 
- 위치 기반의 인자를 가변인자(varargs)나 스타인자(star args)라고 부르기도 함
- 위치 인자를 가변적으로 받을 수 있으면 함수 호출이 더 깔끔해지고 시각적 잡음도 줄어듬
- 좋은 점
  - 리스트를 받으면, 반드시 []라고 넘겨주어야 함 --> 위치 인자는 값을 넘기지 않아도 됨
- 문제 점
  - 위치 인자가 함수로 전달되기 전에 항상 튜플로 변환됨. 함수를 호출하는 쪽에서 제너레이터 앞에 * 연산자를 사용하면 제너레이터의 모든 원소를 얻기 위해 반복한다는 의미가 됨  
  즉, 튜플은 모든 값을 포함하기 떄문에 메모리 소비가 많아질 수 있음
  - 함수에 새로운 위치 인자를 추가하면 해당 함수를 호출하는 모든 코드를 변경해야 한다는 것  
    해당 문제를 해결하기 위해서는 추가되는 인자는 반드시 키워드 기반의 인자만 사용해야 함 

### 23-키워드 인자로 선택적인 기능을 제공해라
- 선택적인 기능 --> 인자를 받느냐, 받지 않느냐에 따라서 내부 로직이 바뀔 수 있다는 점
- 딕셔너리 내용물을 ** 연산자를 사용할 수 있음
~~~python
my_kwargs = {
    'number': 20,
    'divisor': 7,
}
remainder(**my_kwargs)
~~~
- 키워드 인자를 지정하면 좋은 점 3가지
  - 코드를 처음 보는 사람들에게 호출의 의미를 명확히 알려줄 수 있음 
  - 키워드 인자의 경우, 디폴트 값을 지정할 수 있음. 디폴트 값을 지정함으로써 잡음을 줄일 수 있음
  - 어떤 함수를 사용하던 기존 호출자에게는 하위 호환성을 제공하면서 함수 파라미터 확장이 가능

### 24- None과 docstring을 사용해 동적인 디폴트 인자를 지정해라
- 다음의 디폴트 인자는 함수가 정의되는 시점에 단 한번만 호출됨  
  결과적으로 `datetime.now()`는 갱신되지 않음
~~~python
def log(message, when=datetime.now()):
    print(f"{when}: {message}")
~~~
- <b>디폴트 인자 값은 모듈이 로드(load)될 떄 단 한번만 평가되는데, 보통 프로그램이 시작할 때 모듈을 로드하는 경우가 많음</b>
- 이를 해결하는 방법은 디폴트로 None을 지정하고 docstring에 문서화 하는 것 
- 디폴트 인자 값으로 None을 사용하는 것은 인자가 mutable인 경우 특히 중요
~~~python
import json

def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default
~~~
- `decode` 함수를 통해 반환받은 객체는 동일한 딕셔너리 객체임
- 타입 에너테이션을 사용할 때도 None을 사용해 키워드 인자의 디폴트 값을 표현하는 방식을 적용할 수 있음

### 25-위치로만 인자를 지정하게 하거나 키워드로만 인자를 지정하게 하여 함수 호출을 명확하게 만들라
- 보통 키워드 인자를 사용하면 더 좋은점이 많은데, 문제는 키워드 인자를 사용하는 것이 선택사항이므로, 호출하는 쪽에서 명확성을 위해 키워드 인자를 꼭 쓰도록 강요 할 수 없음
- `*` 기호를 사용하여 위치 인자의 마지막과 키워드만 사용하는 인자의 시작을 구분해 줌   
  `safe_division_c(number, divisor, *, ignore_overflow = True...)`
- `/` 기호는 위치로만 지정하는 인자의 끝을 표시(3.7 이하에서는 지원하지 않음)
- `*`와 `/` 연산자 사이에 있는 인자는 둘다 사용 가능

### 26-functions.wrap을 사용해 함수 데코레이터를 정의해라
- 파이썬 데코레이터는 실행 시점에 다른 함수를 변경할 수 있게 해줌
- 데코레이터를 사용하면 instrospection을 사용하는 도구가 잘못 작동할 수 있음
- 직접 데코레이터를 구현할 때 introspection에서 문제가 생기지 않길 바란다면 wraps 데코레이터 사용하기
~~~python
from functools import wraps

def trace(func):
    @wraps(func) #- function wraps
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({kwargs!r})"
              f"-> {result!r}")
        return result
    return wrapper
~~~

### 27- map과 filter 대신 comprehension을 사용해라
- comprehension 코딩 스타일은 <b>제너레이터를 사용하는 함수로 확장 가능</b>
- 제너레이터는 함수가 순차적으로 반환하는 값으로 이뤄지는 <b>스트림</b>을 만들어줌
- map 함수에서 사용하는 lambda function은 시각적으로 좋지 않음
~~~python
cp1 = [x ** 2 for x in range(10)]       #- comprehension
map1 = map(lambda x: x ** 2, range(10)) #- map 
~~~

### 28- 컴프리헨션 내부에 제어 하위 식을 3개 이상 사용하자 마라
- 만약 하위 식을 3개 이상써야 한다면, help function을 작성하여 사용하자

### 29- 대입식을 사용해 컴프리헨션 안에서 반복 작업을 피하자
- 8개의 묶음으로 물건을 판매한다고 했을 때, 판매가 가능한 물품과 묶음 개수를 반환해주는 코드 작성해보기
~~~python
#- python 3.8 이상
found = {name: batches
            for name in order
             if (batches := get_batches(stock.get(name, 0), 8))}
~~~
- 다음과 같이 값 식에서 왈러스 연산자를 통해 변수를 정의하고, 조건식에서 변수를 사용할 시 에러 발생
~~~python
result = {name: (tenth := count // 10)
            for name, count in stock.items() if tenth > 10} #- 조건식에서 tenth 사용
~~~
- 컴프리헨션 값 부분에서 연산자 사용시, 그 값에 대한 조건이 없다면 컴프리헨션 밖으로 변수가 누출됨  
  for 루프도 마찬가지로 발생. 중요한 것은 컴프리헨션 자체는 누출이 발생하지 않음
~~~python
half = [(last := count // 2) for count in stock.values()]
print(f"{half}의 마지막 원소는{last}")  #- 누출 발생 
[count for count in stock.values()] #- count 누출 발생 x
~~~
- assignment expression을 통해 comprehension이나 generator 식의 조건 부분에서 사용한 값을 컴프리헨션이나 제너레이터의 다른 위치에서 재사용 가능
- 조건이 아닌 부분에서도 사용가능하지만, 누출 때문에 그런 형태의 사용은 피해야 함 

### 30- 리스트 반환보다는 제너레이터를 사용해라
- 제너레이터 사용시 가독성을 개선할 수 있음
- 제너레이터는 `yield` 명령어를 `return` 대신 사용함으로써 개선 가능
- 제너레이터가 만들어내는 이터레이터는 함수의 본문에서 `yield`가 반환하는 값들로 이루어진 집합을 만들어냄
- <b>제너레이터가 반환하는 이터레이터에는 상태가 있기 때문에 호출하는 쪽에서는 재사용이 불가능</b>
- 제너레이터를 사용하면 <b>작업 메모리에 모든 입력과 출력을 저장할 필요가 없으므로</b> 입력이 아주 커도 출력 시퀀스를 만들 수 있음
- 다음은 제너레이터 함수 예제 코드(텍스트의 띄어쓰기 위치인 index 집합 생성 제너레이터)
~~~python
text = "컴퓨터(영어: Computer, 문화어: 콤퓨터, 순화어: 전산기)는 진공관"
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1
~~~

### 31- 인자에 대해 이터레이션 할 때는 방어적이 되어라  
- 함수 내에서 이터레이터를 여러번 사용해야 할 경우가 있음
- 문제는 이미 소진된 이터레이터에 대해 이터레이션을 수행해도 아무런 오류가 발생하지 않음  
  for 루프, 리스트 생성자, 그 외의 많은 표준 파이썬 라이브러리에서는 연산 도중에 `StopIteration` 예외가 던져지는 것을 가정하기 때문 
- 이렇게 되면 소진된 이터레이터를 구분할 수 없는 큰 문제가 발생하게 됨  
- 한가지 해결방법은 이터레이터가 호출 될 때마다 새로운 이터레이터를 생성하는 것이 있지만, 이 보다 더 좋은 해결방법은 이터레이터 <b>프로토콜(protocol)을 구현한 새로운 컨테이너 클래스를 제공 하는 것</b>

#### 이터레이터 프로토콜
- iterator: 데이터를 순차적으로 반환할 수 있는 객체
- iterable: 이터레이터를 반환할 수 있는 객체 ex) list, string, dict ...
- 이터레이터 프로토콜은 파이썬의 for 루프나 그의 연관된 식들이 컨테이너 타입의 내용을 방문할 때 사용하는 절차
- `for x in foo` 라는 식은 내부적으로 `iter(foo)` 를 호출함
- `iter` 내장 함수는 `foo.__iter__` 라는 특별 메서드를 호출 
- `__iter__` 메서드는 반드시 이터레이터 객체를 반환해야 함 ex) `yield int(line)`
  - 제너레이터 식
  - `yield` 를 통해 반환하는 제너레이터 함수로 `__iter__` 선언
  - `iter(list)`, `iter(string)`  
- 결과적으로 실제 코드를 작성할 떄 우리가 정의하는 클래스에서 `__iter__` 메서드를 제너레이터로 구현하기만 하면 모든 동작을 만족시킬 수 있음
~~~python
def america_travel_normalize(num_list):
    total = sum(num_list)
    result = []
    for num in num_list:
        result.append(100 * num / total)
    return result

class ReadVisits:
    def __init__(self, file_path):
        self.file_path = file_path

    def __iter__(self):
        with open(self.file_path) as f:
            for line in f:
                yield int(line)

visits = ReadVisits('text.txt')
percentages = america_travel_normalize(visits)
print(percentages)
print(sum(percentages))
~~~
- 위의 코드가 잘 동작하는 이유는, `sum` 메서드가 `ReadVisits.__iter__` 를 호출해서 새로운 이터레이터 객체를 호출하기 때문. for 루프도 마찬가지!
- 두 이터레이터는 서로 독립적으로 진행되고 소진됨. 문제는 입력 데이터를 여러 번 읽는다는 것  
  즉, 여러 번 읽어야 하는 경우에는 리스트를 고려해보는 것도 생각해 보아야 함
- <b>이터레이터 프로토콜에 따르면, 이터레이터가 iter 내장 함수에 전달되는 경우, 전달받은 이터레이터가 그대로 반환됨</b>
- 이러한 개념을 예외처리 하여, 방어적으로 이터레이터를 프로그래밍 할 수 있음
~~~python
def normalize_defensive(numbers):
    #- 1번 방법 
    if iter(numbers) is numbers:
        raise TypeError("컨테이너를 제공해야 합니다.")
    ...
    #- 2번 방법: collection.abc 내장 모듈의 Iterator 인지 isinstance로 검사
    if isinstance(numbers, Iterator)
~~~
- list와 ReadVisit 클래스 인스턴스는 iterable 객체이므로 정상적이게 작동함
- 요약 정리
  - 입력 인자를 여러번 이터레이션하는 함수나 메서드를 조심하자. 입력받은 인자가 이터레이터면 함수가 이상하게 작동할 수 있음
  - 파이썬의 이터레이터 프로토콜은 컨테이너와 이터레이터가 `iter`, `next` 내장 함수나 for 루프 등의 관련 식과 상호작용하는 절차를 정의
  - `iter` 메서드를 제너레이터로 정의하면 쉽게 이터러블 컨테이터 타입을 정의할 수 있음
  - 어떤 값이 이터레이터인지 감지하려면, 이 값을 iter 내장 함수에 넘겨서 반환하는 값이 원래 값과 같은지 확인 필요
  - 다른 방법으로 `collections.abc.Iterator` 클래스를 `isinstance` 와 함께 사용 가능

### 32- 긴 리스트 컴프리헨션보다는 제너레이터 식을 사용해라
- 리스트 컴프리헨션의 문제점은 입력 시퀀스와 같은 수의 원소가 들어있는 리스트 인스턴스를 만들어내어 입력이 커질 시 상당히 큰 메모리를 잡아 먹을 수 있다는 것
- 이러한 문제를 해결하기 위하여 제너레이터 식을 제공. 제너레이터 식은 컴프리헨션과 제너레이터를 일반화 한 것으로 <b>제너레이터 식을 실행해도 시퀀스 전체가 실체화되지 않음</b>
- 대신 제너레이터 식에 들어있는 식으로부터 원소를 하나씩 만들어내는 이터레이터가 생성됨
- 제너레이터 식은 이터레이터로 즉시 평가되며, 더 이상 시퀀스 원소 계산이 진행되지 않음
- 제너레이터의 또다른 강력한 특징은 두 제너레이터를 합성 할 수 있음
- <b>아주 큰 입력 스트림을 처리해야 한다면, 제너레이터 식 사용하자</b>
~~~python
g = (x for x in range(10))
print(next(g))

#- generator 합성 가능
roots = ((x, x**0.5) for x in g)
next(roots)
~~~

### 33- yield from을 이용해 여러 제너레이터를 합성해라
- 제너레이터는 강점이 많아 다양한 프로그램에서 여러 단계에 걸쳐 한 줄기로 사용됨
- `yield from`을 사용하면 여러 제너레이터를 하나로 묶을 수 있음(가독성도 높아짐)
- `yield from`은 근본적으로 파이썬 인터프리터가 for 루프를 내포시키고 yield 식을 처리하도록 함
- 성능적인 측면에서도 for 루프를 이용한 연결보다 `yield from`이 더 빠름
~~~python
def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)
~~~

### 34-send로 제너레이터에 데이터를 주입하지 말라
- `send` 메서드를 제너레이터에서 사용하면 중간에 값을 주입시킬 수 있음(양방향 채널로 격상됨)
- `send` 메서드를 사용하면 입력을 제너레이터에 스트리밍하는 동시에 출력을 내보낼 수 있음
- 제너레이터를 이터레이션할 때 `yield` 식이 반환하는 값을 받으면 일반적으로 None임
~~~python
def my_generator():
    received = yield 1
    print("Hello")
    print(f"받은 값 = {received}")


it = iter(my_generator())
output = next(it)
print(f"출력값 = {output}")

#- 더이상 iteration할 데이터가 없으므로, print 구문 2개를 실행시키고 
#- stopIteration 예외를 발생시킴
try:
    next(it)
except StopIteration:
    pass
~~~
- 최초로 시작한 제너레이터는 아직 yield 식에 도달하지 못했기 때문에 최초로 send를 호출할 때 인자로 전달할 수 있는 유일한 값은 None임
- 즉, 우리가 `send`를 통해서 제너레이터에 값을 전달할 때는 최초로 None을 전달해야함
- `send`를 이용하는 것은 다음과 같은 문제점 존재
  - 코드를 이해하기 어렵고, 오른쪽에 `yield`를 사용하는 것은 직관적이지 않음
  - `yield from`을 통해 연결할 때, 항상 최초 실행시 None이 발생
- 결과적으로 `send`를 사용하지 말고 다른 방법으로 접근하는 것이 좋음

### 35- 제너레이터 안에서 throw로 상태를 변화시키지 마라
- 제너레이터 안에서 Exception을 던질 수 있는 `throw` 메서드가 존재함
- throw는 어떤 제너레이터에 대해 throw가 호출되면 이 제너레이터는 값을 내놓은 `yield`로부터 평소처럼 제너레이터 실행을 계속하는 대신, `throw`로 전달한 Exception을 전달
- `throw` 메서드를 사용하면 제너레이터가 마지막으로 실행한 yield 식의 위치에서 예외를 발생시킬 수 있음
- `throw` 를 사용하면 가독성이 나빠짐. 예외를 잡아내고 다시 발생시키는데 준비 코드가 필요하며, 내포 단계가 깊어짐
- 제너레이터에서 예외적인 동작을 제공하는 더 나은 방법은 `__iter__` 메서드를 구현하는 클래스를 사용하면서 예외적인 경우에 상태를 전이시키는 것 
- 다음의 코드는 `throw`를 사용해서 exception을 발생시키지 않고, reset 함수 실행
~~~python
class Timer:
    def __init__(self, period):
        self.current = period
        self.period = period

    def reset(self):
        self.current = self.period

    def __iter__(self):           #- iter 메소드를 제너레이터로 정의함
        while self.current:       
            self.current -= 1
            yield self.current


def run():
    timer = Timer(4)
    for current in timer:
        if check_for_reset():
            timer.reset()
        else:
            announce(current)

run()
~~~

### 36- 이터레이터나 제너레이터 사용시 itertools를 사용해라
- `itertools.chain`
- `itertools.repeat`
- `itertools.cycle`
- `itertools.tee`
- `itertools.zip_longest`
- `itertools.islice`
- `itertools.takewhile`
- `itertools.dropwhile`
- `itertools.filterfalse`
- `itertools.accumulate`
- `itertools.product`
- `itertools.permutations`
- `itertools.combinations`
- `itertools.combinations_with_replacement`

### 37-내장 타입을 여러 단계로 내포시키기보다는 클래스를 합성해라
- 내장타입(dict, list)를 통해 여러 단계를 내포시키면 향후 유지보수 등에 있어 어려워짐  
  --> 클래스를 사용해서 구조적으로 구현하자
- <b>원소가 3개 이상인 튜플을 이용한다면 collections 내장 모듈의 namedtuple 타입을 고려하자</b>
- namedtuple 선언: `Grade = namedtuple('Grade', ('score', 'weight'))`
- `namedtuple`의 장점
  - 키워드 기반 인자와 위치 기반 인자를 모두 사용할 수 있음
  - 해당 클래스 기반의 객체 필드 접근시, 애트리뷰트 사용 가능(ex) `Grade.score`, `Grade.weight`)
  - 애트리뷰트를 사용할 수 있으므로, 나중에 유지보수시 클래스를 쉽게 바꿀 수 있음
- `namedtuple`의 한계
  - default 인자를 지정할 수 없어, 선택적인 property가 많은 데이터에는 namedtuple을 사용하기는 어려움
  - 숫자 인덱스나 이터레이션도 가능해서, 외부에서 제공하는 API의 경우 이런 특성으로 인해 namedtuple을 실제 클래스로 변경하기 어려울 수 있음
- 다음의 예시는 기억하기
  - Grade라는 namedtuple 사용해서 튜플의 단점을 제거
  - 계층적 클래스 구조를 통해 추상화 계층을 생성
~~~python
from collections import namedtuple
from collections import defaultdict

Grade = namedtuple('Grade', ("score", "weight"))

#- 단일 과목을 표현하는 클래스
class Subject:
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

#- 마지막으로 모든 학생을 저장하는 컨테이너 만들 수 있음
class Gradebook:
    def __init__(self):
        self._students = defaultdict(Student)

    def get_student(self, name):
        return self._students[name]
~~~
- 딕셔너리, 긴 튜플, 다른 내장 타입이 복잡하게 내포된 데이터 값으로 사용하는 딕셔너리를 만들지 말라
- 완전한 클래스가 제공되는 유연성이 필요하지 않고 가벼운 불변 데이터 컨테이너가 필요하면 namedtuple을 사용해라
- 내부 상태를 표현하는 딕셔너리가 복잡해지면 이 데이터를 관리하는 코드를 여러 클래스로 나눠서 재작성해라

### 38- 간단한 인터페이스의 경우 클래스 대신 함수를 받아라
- 파이썬 내장 API중 상당수는 함수를 전달해서 동작을 원하는대로 바꿀 수 있도록 해줌
- API가 실행되는 과정에서 우리가 전달한 함수를 실행하는 경우, 해당 함수를 <b>훅(hook)</b>이라고 부름
  ex) sort 메서드의 key 인자로 hook을 받을 수 있음
- 훅을 추상 클래스를 통해 정의해야 하는 언어도 있지만, 파이썬은 단순히 인자와 반환값이 잘 정의된 상태가 없는 함수를 훅으로 사용가능한데, 그 이유는 파이썬에서의 함수는 first-class-object 때문 이기도 함 
- defaultdict에 전달하는 디폴트 값 훅이 존재하지 않는 키에 접근하는 총 횟수를 세고 싶다고 하자  
  다음과 같은 3가지 방법으로 코드 구현 가능
  - 클로저 함수를 통해 구현 
  - 작은 클래스 구현
  - `__call__` 메서드가 포함된 클래스 구현 후 클래스 객체를 전달 --> 가장 좋음  
    코드를 처음 보는 사람도 `__call__`이 클래스의 동작을 알아보기 위한 첫 시작점이라는 것을 알 수 있음
- 파이썬의 여러 컴포넌트 사이에 간단한 인터페이스가 필요할 때는 클래스를 정의하고 인스턴스화하는 대신 간단한 함수를 사용할 수 있음
- 파이썬 함수나 메서드는 first-class object, 따라서 함수나 함수 참조를 식에 사용 가능
- `__call__` 특별 메서드를 사용하면 클래스의 인스턴스인 객체를 일반 파이썬 함수처럼 사용 가능
- 상태를 유지하기 위한 함수가 필요한 경우, 클로저 함수 대신에 `__call__` 메서드가 있는 클래스를 정의할 지 고려해보자

### 39- 객체를 제너릭하게 구성하려면 @classmethod를 통한 다형성을 활용해라
- 다음을 만족하는 코드를 구현해보기 - (Classmethod 활용 안하고)
- thread를 활용해서 mapreduce 구현하기
  - 데이터를 read 할 수 있는 공통클래스 `InputData` 를 기반으로 여러 하위 클래스 구조 생성
  - map, reduce 함수를 구현하는 공통클래스 `Worker` 를 기반으로 여러 하위 클래스 구조 생성
  - 두 공통 클래스를 연결시켜주는 함수 구현(`generate_inputs`, `create_workers`, `execute`)
  - 최종 `mapreduce` 함수를 통해 실행
  - `reduce` 함수는 file의 총 줄 수를 더하는 함수
~~~python
import os
from threading import Thread
import random


class InputData:
    def read(self):
        raise NotImplementedError


class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        with open(self.path) as f:
            return f.read()


class Worker:
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, * rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(data_dir):
    input_list = generate_inputs(data_dir)
    workers = create_workers(input_list)
    return execute(workers)

def write_test_files(tmpdir):
    if not os.path.isdir(tmpdir):
        os.mkdir(tmpdir)
    for i in range(100):
        with open(os.path.join(tmpdir, str(i)), 'w') as f:
            f.write('\n' * random.randint(1, 100))


tmpdir = 'test_dir'
if not os.path.isdir(tmpdir):
    os.mkdir(tmpdir)

for i in range(100):
    with open(os.path.join(tmpdir, str(i)), 'w') as f:
        f.write('\n' * random.randint(0, 100))

write_test_files(tmpdir)
result = mapreduce(tmpdir)
print(f"file들의 총 줄 수는 {result} 입니다.")
~~~
- 다음은 제너릭한 코드를 구현하기 위해 classmethod의 다형성을 활용한 예제  
(위의 코드와 비교해가면서 확인하자)
~~~python
import os
from threading import Thread
from random import randint


def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, *rest = workers
    for worker in rest:
        first.reduce(worker)
    return first.result

class GenericInputData:
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData(GenericInputData):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))


class GenericWorker:

    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCountWorker(GenericWorker):

    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)


tmpdir = 'test_dir'
if not os.path.isdir(tmpdir):
    os.mkdir(tmpdir)

for i in range(100):
    with open(os.path.join(tmpdir, str(i)), 'w') as f:
        f.write('\n' * randint(1, 100))


config = {'data_dir':tmpdir}
result = mapreduce(LineCountWorker, PathInputData, config)
print(f"총 {result} 개의 줄이 있습니다.")
~~~
- <b>중요한 사실은 classmethod를 통해 `__init__`이 아닌 함수로 생성자를 만들어낼 수 있다는 점</b>
- 제너릭한 함수를 만들어 낸다는 것은 함수의 input을 함수나 클래스로 받아 해당 클래스의 함수를 호출하는 구조를 잡아내는 것
- 위의 코드에서 `input_class.generate_inputs`가 다형성의 예

### 40-super로 부모 클래스를 초기화해라
- 자식 클래스에서 부모 클래스를 초기화하는 일반적인 방법은 부모클래스의 `__init__`
 메서드를 직접 호출하는 것
~~~python
class MyBaseClass:
    def __init__(self, value):
        self.value = value


class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)
~~~
- 하지만 해당 방식으로 호출 할 때, 다이아몬드 상속 같은 경우, 원인을 알기가 매우 어려움
- 이 때 `super`라는 내장 함수를 사용하면 다이아몬드 계층의 공통 상위 클래스를 단 한번만 호출함
- 또한 파이썬에는 표준 메서드 결정 순서가 있는데, 이는 상위 클래스 초기화하는 순서를 정의하고, 이 때 C3 선형화 알고리즘을 사용함
- 부모 클래스를 초기화 할 때는 `super` 내장 함수를 아무 인자 없이 호출해라

### 41- 기능을 합성 할 때는 믹스인 클래스를 활용해라
- 파이썬은 다중 상속을 지원하는 언어이지만, 다중 상속은 피하는 것이 좋으며 믹스인을 사용할지 고려해야 함
- <b>믹스인은 자식 클래스가 사용할 메서드 몇 개만 정의하는 클래스</b>
- 믹스인 클래스는 자체 애트리뷰트 정의가 없으므로, 믹스인 클래스의 `__init__` 메서드를 호출할 필요도 없음
- `className.__dict__` 를 꼭 기억. 해당 클래스 인스턴스의 애트리뷰트를 dict로 전환
- `isinstance` 를 이용해서, `list`, `dict`, `__dict__` 등을 비교해서 해당 케이스마다 적용이 가능
- 믹스인의 장점은 제너릭 기능을 쉽게 연결할 수 있고, 오버라이드해서 변경 가능
- 다음의 믹스인 코드 구조 기억하기
~~~python
class ToDictMixIn:
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixIn):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value
~~~
- 다음과 같이 믹스인에 있는 함수를 오버라이드 해서 사용 가능
~~~python
def _traverse(self, key, value):
    if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
        return value.value
    else:
        return super()._traverse(key, value)
~~~
- 믹스인은 서로 합성해서 사용 가능한데, 다음의 클래스를 기억하자. 해당 클래스의 정의되어 있지 않은 `to_dict` 함수가 정의(상속하거나 정의)되어 있어야 함을 가정하고, `__init__` 메서드가 키워드 인자를 받아야 한다는 것
- 믹스인을 사용할 때 상하위 상속 계층에 이미 해당 믹스인을 적용한 클래스가 있어도 문제 없음  
  이런 경우에도 super가 동작하는 방식으로 인해 믹스인을 적용한 클래스가 제대로 작동함
- 믹스인은 필요에 따라 인스턴스 메서드는 물론 클래스 메서드도 포함될 수 있음
- 믹스인을 합성하면 단순한 동작으로부터 더 복잡한 기능을 만들어낼 수 있음
~~~python
import json


class jsonMixIn:

    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(** kwargs)     #- 상속받을 하위 클래스는 키워드 인자를 받아야 함

    #- 하위 클래스는 to_dict 메서드를 가지고 있어야 함
    def to_json(self):
        return json.dumps(self.to_dict())
~~~

### 42- 비공개 애트리뷰트보다는 공개 애트리뷰트를 사용해라
- 파이썬에서 클래스의 애트리뷰트에 대한 가시성은 공개(public), 비공개(private), 두 가지밖에 없음
- 인스턴스 뒤에 (.)을 붙이면 공개 애트리뷰트에 접근 가능
- 밑줄 두 개(__)를 붙이면 비공개 필드가 됨. 비공개 필드는 해당 클래스 안에서만 접근 가능
- <b>비공개 애트리뷰트의 동작은 애트리뷰트 이름을 바꾸는 단순한 방식으로 구현됨</b>  
  명명 규칙만 달라지는 것인데, 예를 들어 `__private_field`라는 애트리뷰트 접근 코드를 `_MyChildObject__private_field`라는 이름으로 바꿔줌  
  <b>즉 해당 명으로 접근하면 private도 인스턴스에서는 접근이 가능하다는 말</b>
- 객체 애트리뷰트 딕셔너리를 확인하면 실제로 해당 명으로 들어가 있음을 확인 가능
- 이렇게 private 애트리뷰트도 오픈되어 있는 이유는 파이썬 언어의 철학에서 옴
~~~python
class MyObject:
    def __init__(self):
        self.public_field = 5      #- public
        self.__private_field = 10  #- private
~~~
- 비공개 애트리뷰트로 접근을 막으려고 시도하기보다는 보호된 필드를 사용하면서 문서에 적절한 가이드를 남기자
- 우리가 코드 작성을 제어할 수 없는 하위 클래스에서 이름 충돌이 일어나는 경우를 막고 싶을 때만 비공개 애트리뷰트를 사용할 것을 권함

### 43- 커스텀 컨테이너 타입은 collections.abc를 상속해라
- 모든 파이썬 클래스는 함수의 애트리뷰트를 함께 캡슐화하는 일종의 컨테이너라 볼 수 있음
- 클래스가 시퀀스처럼 작동하게 하려면 트리 노드를 깊이 우선 순회하는 커스텀 `__getItem__` 메서드를 구현하면 됨
~~~python
#- index --> list[index] 라고 생각하면 됨
def __getitem__(self, index):
    for i, item in enumerate(self._traverse()):
        if i == index:
            return item.value
    raise IndexError(f"인텍서 - 범위 초과: {index}")
~~~
- `__getItem__`을 구현하는 것만으로는 리스트 인스턴스에서 기대할 수 있는 모든 시퀀스 의미 구조를 제공할 수 없다는데 있음
- `len()` 함수는 `__len__` 이라는 특별 메서드를 구현해야 작동함
~~~python
def __len__(self):
    for count, _ in enumerate(self._traverse(), 1):
        pass
    return count
~~~
- <b>내장 `collection.abc` 모듈 안에 컨테이너 타입에 정의해야 하는 전형적인 메서드를 모두 제공하는 추상 기반 클래스 정의가 여러가지 들어가 있음<b>
- 이런 추상 기반 클래스의 하위 클래스를 만들고 필요한 메서드 구현을 잃어버리면 실수한 부분을 알려줌
~~~python
from collections.abc import Sequence

class BadType(Sequence):
    pass

foo = BadType()
>>>
TypeError: Can't instantiate abstract class BadType with abstract methods __getitem__, __len__
~~~
- `Set`, `MutableMapping`과 같이 파이썬의 관례에 맞춰 구현해야 하는 특별 메서드가 훨씬 많은 더 복잡한 컨테이너 타입을 구현할 때는 이런 추상 기반 클래스가 주는 이점이 더 커짐
- `collections.abc` 모듈 외에도, 파이썬에서는 객체 비교와 정렬을 위해 사용하는 다양한 특별 메서드들이 존재함
- 컨테이너 클래스나 비컨테이너 클래스에서 모두 이런 특별 메서드를 구현할 수 있음

### 82- 커뮤니티에서 만든 모듈을 어디서 찾을 수 있을지 알아두라
- 파이썬 패키지 인덱스(PyPI)에는 풍부한 패키지가 들어가 있음(http://pypi.org)
- `pip`를 사용하면 새로운 모듈을 쉽게 설치할 수 있음
- `python3 pip install pandas`
- 패키지를 지속적으로 추적하고 관리할 수 있게 venv와 같이 쓰는 것이 중요

### 83- 가상 환경을 의존해 의존 관계를 격리하고 반복 생성할 수 있게 해라
- `pip`로 설치한 패키지들은 기본적으로 전역 위치에 저장됨  
  이로 인해 우리 시스템에서 실행되는 모든 파이썬 프로그램이 모듈의 영향을 받게 됨
- 패키지 설치 후 이 패키지가 의존하는 다른 패키지 목록을 볼 수 있음  
  `python3 -m show Sphinx`
- 파이썬에서는 전역적으로 모듈은 한 버전만 설치 가능
- 이런 의존 관계를 해소하고자 <b>venv라는 도구를 사용</b>. venv라는 가상 환경을 제공하는데, 파이썬 3.4부터 파이썬 설치시 pip와 venv 모듈을 default로 제공함
- venv를 사용하면 좋은 점
  - 파이썬 환경을 독립적으로 구성 가능
  - 한 시스템 안에 같은 패키지의 다양한 버전을 서로 충돌없이 사용가능   
    한 컴퓨터 안에서 여러 다른 프로젝트 작업을 진행하면서 프로젝트마다 각각 다른 도구 활용 가능
- <b>venv는 각 버전의 패키지와 의존 관계를 별도의 디렉토리에 저장함</b>
~~~shell
$ which python3             #- 디렉토리 확인
$ python3 --version         #- 버전 확인
$ python3 -c 'import ptyz'  #- pytz 패키지 임포트 가능 여부 확인
$ python3 -m venv myproject #- venv를 이용해 myproject라는 가상 환경을 만듬
$ cd myproject              #- ** 가상환경 디렉토리롤 이동해야만 venv 실행 가능
$ source bin/activate       #- 가상 환경 사용
                            #- 명령줄 프롬프트에서 가상환경명이 붙여짐
$ which python3             #- 명령줄 도구가 가상 환경 디렉터리 안에 도구 경로로 바뀜

~~~
- venv 환경 복사시, `python3 -m pip freeze > requirement.txt` 명령을 이용해 현재 명시적으로 의존하는 모든 의존 관계를 파일에 저장 가능(관례적인 이름 --> requirement.txt)
~~~shell
$ python3 -m pip freeze > requirement.txt
$ cat requirement.txt
~~~
- 해당 venv 환경과 동일한 환경을 새로 만들고 싶으면 다음과 같이 실행
~~~shell
$ python -m venv otherproject
$ cd otherproject
$ source bin/source
$ python3 -m pip install -r /tmp/project/requirement.txt
~~~
- <b>파이썬 버전은 requirement.txt 파일에 들어가지 않음. 따라서 별도 관리가 필요</b>
- <b>가상 환경을 사용할 때 가상 환경 디렉토리를 통째로 옮기면 모든 요소가 깨짐. 이유는 python3 등의 명령줄 도구 경로가 하드코딩돼 있기 때문</b>
- 따라서 새로운 가상 환경을 만든 후 원래 디렉터리에서 requirement.txt를 실행해 얻은 requirement.txt 파일로 모든 모듈을 재설치하면 됨

### 84-모든 함수, 클래스, 모듈에 독스트링을 작성해라
- 파이썬은 코드 블록에 문서를 첨부하는 기능을 기본으로 제공 
- `python3 -m pydoc -p 1234`로 파이썬 문서 확인 가능
~~~python
#- 함수 docstring
def test():
  """주어진 함수는 test 용도입니다."""
  return None
print(repr(palindrome.__doc__))
~~~
- 함수 docstring 작성시 알아둘 것들
  - 함수에 인자가 없고 반환 값만 있다면 설명은 한줄로!
  - 함수가 아무 값도 반환하지 않는다면 아무것도 쓰지 않기
  - 함수 내에 예외 발생 포함시, 예외 발생 상황에 대한 설명을 포함해야함
  - 가변인자, 키워드 인자를 받는다면, 목적 설명하기
  - 함수에 디폴트 값이 있는 인자가 있다면, 언급해야 함
  - 함수가 제너레이터라면, 이터레이션시 어떤 값이 발생하는지 작성해야 함
  - 함수가 비동기 코루틴이라면, 독스트링에 언제 이 코루틴의 비동기 실행이 중단되는지 설명해야 함
- 독스트링과 애너테이션이 제공하는 정보가 중복된다면 한쪽으로 몰아야 함


### 85-패키지를 사용해 모듈을 체계화하고 안정적인 API를 제공해라
- 코드가 많아지고 모듈이 많아지면 코드를 이해하기가 어려우므로, 코드를 좀 더 쉽게 이해할 수 잇도록 다른 계층을 추가하는데, 파이썬은 <b>패키지</b>를 제공함
- <b>파이썬의 패키지는 대부분의 경우, __init__.py 라는 빈 파일을 추가함으로써 패키지를 정의함</b>
~~~python
# package directory structure
mypackage/__init__.py
mypackage/models.py
mypackage/utils.py

# main.py
from mypackage import models
from anaylsis.utils import log_base2_bucket
from frontend.utils import stringify

#- 패키지 안에 동일한 이름의 함수가 있는경우, --> as 사용
from analysis.utils import inspect as analysis_inspect
from frontend.utils import inspect as frontend_inspect

analysis.utils.insert(value) #- as 사용 안할시, 더 좋음
~~~
- 모듈이나 패키지의 `__all__` 특별 애트리뷰트를 통해 API 소비자에게 노출할 것들을 제한
- `__all__`의 값은 모듈에서 외부로 공개된 API로 export할 모든 이름이 들어있는 리스트
- `from foo import *` 실행시, foo.__all__에 있는 애트리뷰트만 import 가능
- __all__가 정의되어 있지 않으면 public attribute만 import 됨
~~~python
#- utils.py
__all__ = ['simulate_collision']

def _dot_products(a, b):
    print(a, b)

def simulate_collision(a, b):
    print(a, b)

#- inits.py
__all__ = []

from . modules import *
__all__ += modules.__all__

from . utils import *
__all__ += utils.__all__
~~~
- `__all__`에 제외됐다는 말은 `from mypackage import *` 명령으로 임포트해도 임포트되지 않는다는 뜻
- 모듈과 모듈 사이에 공유되어야 하는 API 제작시, all 기능이 불필요하거나, 사용하지 말아야 할 수 있음
- `from foo import *`보다는 명시적으로 `from a import b`를 쓰자 

### 86-배포 환경을 설정하기 위해 모듈 영역의 코드를 사용해라
- 개발환경과 가동환경이 다를 때를 생각하여 좋은 방법은 시작시 프로그램을 일부 오버라이드해서 배포되는 환경에 따라 다른 기능을 제공하도록 하는 것
- 다음의 코드는 개발환경(dev_main.py) vs production 환경(prod_main.py)에 따라, 실행되는 db가 다른 코드
~~~python
# dev_main.py
TESTING = True  #- 해당 코드가 __main__에 들어감

import db_connection
db = db.connection.Database()

# prod_main.py
TESTING = False

import db.connection
db = db.connection.Database()

# db_connection.py
import __main__   #- ** dev_main, prod_main에 있는 TESTING 변수를 가져오기 위함

class TestingDatabase:
  ...

class RealDatabase:
  ...

if __main__.TESTING:
  Database = TestingDatabase
else:
  Database = RealDatabase
~~~
- 핵심은 db_connection.py 에서 모듈 범위에서 코드가 수행된다는 점
- 배포 설정 환경이 복잡해지면, config 파일 등으로 옮겨야 함. configparser 내장 모듈 같은 도구를 사용하면 production 코드로부터 유지 보수 할 수 있음
- 특히 협업할 떄 설정과 코드를 구분하는 것이 중요
- 다른 측면으로, host platform에 따라 다르게 작성해야 한다는 것을 알면 모듈에서 최상위 모듈을 정의하기 전에 sys 모듈을 살펴보면됨
~~~python
# db_connection.py
import sys
class Win32Database:
  ...
class PosixDatabase:
  ...

if sys.platform.startswith('win32'):
  Database = Win32Database
else:
  Database = PosixDatabase
~~~

### 87- 호출자를 API로부터 보호하기 위하여 최상위 Exception을 정의해라
- API 정의시, 내부적으로 정의한 exception도 매우 중요
- 파이썬 언어, 표준 라이브러리에는 이미 예외 계층 구조가 내장되어 있음. 이를 사용해도 되고, 직접 만들어 사용해도 됨
- <b>내장 exception인 ValueError를 사용해도 되지만, API 같은 경우 새로운 예외 계층 구조를 정의하는 것이 훨씬 좋음</b>
- 최상위 예외가 있으면, API 사용자들이 더 쉽게 오류를 잡아 낼 수 있음  
  디음의 코드를 확인
~~~python
#- 최상위 예외를 포함한 경우 --> API 호출 위치 + API 내 오류 위치까지 확인가능
#- 만약 API 내부적으로 오류가 정의되어 있지 않으면, 알기 어려움
import my_module
import logging

try:
    weight = my_module.determine_weight(1, -1)
except my_module.Error:
    logging.exception('예상치 못한 오류')

>>> 
ERROR:root:예상치 못한 오류
Traceback (most recent call last):
  File "<input>", line 5, in <module>
  File "/Users/heojaehun/gitRepo/TIL/effectivePython/my_module.py", line 22, in determine_weight
    raise InvaildVolumeError('부피는 0보다 커야함')
my_module.InvaildVolumeError: 부피는 0보다 커야함
~~~
- 최상위 예제 구현시, 3가지 장점 존재 
  - 사용자가 API 호출을 잘못 했을 때, 더 쉽게 이해 가능
  - API 모듈 코드의 버그를 발견할 떄 도움됨 --> 정의되지 않은 예외 발생시 이것은 버그!  
    `Exception` 으로 확인. 소비자쪽에서 try/except를 통해 모듈의 버그를 확인해야 함
  - 미래의 API를 보호해줌. 추가적인 Exception 하위 클래스 추가 가능
- `raise ValueError('hello world') from exc` --> valueError + 기존 발생한 Exception(exc)까지 포함한 예외 확인

### 88 순환 의존성을 깨는 방법 알아두기
- A, B라는 모듈에서 각각 B, A의 모듈을 import하는 상호 의존적인 경우 발생
- 모듈을 import 하는 과정은 다음과 같음
  - `sys.path`에서 모듈 위치를 검색
  - 모듈의 코드를 로딩하고 컴파일 되는지 확인 
  - 임포트할 모듈에 상응하는 빈 모듈 객체를 만듬
  - 모듈을 `sys.modules`에 넣음
  - 모듈 객체에 있는 코드를 실행해서 모듈의 내용을 정의
- <b>여기서 중요한 점은, 모듈 레지스트리를 통해 모듈이 이미 import 했는지를 확인하고, 만약 이미 등록되어 있다면 cache에서 해당 객체를 사용함. 여기서 말하는 cache의 등록은 sys.modules에 넣는 것을 말함(4단계)</b>
- 즉, 어떤 모듈의 애트리뷰트를 정의하는 코드(5단계)가 실제로 실행되기 전까지는 모듈의 애트리뷰트가 정의되지 않는다는 점임
- 이런 문제 해결 방법은 코드 리펙터링을 통해 정의 부분을 의존 관계의 트리 맨 밑바닥으로 보내는 것
- 또는 순환 import를 깨는 3가지 방법 수행
  - import 순서를 바꾼다 -> PEP 8 가이드에 위배됨. 파일 뒷부분에 import를 넣으면 코드 순서를 약간만 바꿔도 망가짐. 추천X
  - 임포트 시점에 부작용을 최소화한 모듈 사용 --> import 시점에 함수 실행 X  
    하지만 함수 자체를 정의하지 못할 수도 있음. 또한 객체 정의 부분과 실행 부분이 나눠져 복잡해짐
  - import문을 메서드 안에서 사용 --> <b>프로그램이 실행될 때 모듈 임포트가 일어나기 때문에 동적 임포트라고 함</b> -> 동적 임포트는 피하는 것이 좋음  
  임포트 실행을 미루기 때문에 예기치 못하는 오류로 인해 문제 발생 여지가 있음. 하지만 이러한 감수를 전체 구조를 수정하는 것보단 낫다면 수행해야함
- 동적 임포트는 리펙터링과 복잡도 증가를 최소화하면서 모듈 간의 순환 의존 관계를 깨는 가장 단순한 해법임

### 89-리펙터링과 마이그레이션 방법을 알려주기 위해 warning을 사용해라
- 내가 만든 API를 여러 호출 지점에서 사용하고 있다고 가정하고, 코드 수정을 알릴 때 `warning`을 사용할 수 있음
- `warning` 내장 모듈을 사용해 사람들에게 의사를 전달할 때는 `warning` 사용
- 다음의 stringIO를 이용해 발생하는 warning 등을 문자열 객체로 전달받을 수 있음
~~~python
import warnings
import contextlib
import io

def fake_error():
    warnings.warn("fake error", DeprecationWarning)

fake_stderr = io.StringIO()
with contextlib.redirect_stderr(fake_stderr):
    fake_error()

print(fake_stderr.getvalue())
~~~
- `warnings.wran` 함수 파라미터로 stacklevel를 사용하면, 호출 스택의 위치를 변경할 수 있음
~~~Python
warnings.warn("warning!!", DeprecationWarning, stacklevel=3)
~~~
- warnings은 경고 발생시 특정 작업을 수행하게 할 수 있는데, 한가지 방법은 모든 경고를 오류로 바꿔 예외 처리를 하게끔 하는 것
- 모든 오류를 경고로 바꾸는 방법
  - `warnings.simplefilter('error')`
  - shell에서 `python -W error ex6.py`
~~~python
import warnings
import contextlib
import io

warnings.simplefilter('error')
try:
    warnings.warn('이 사용법은 향후 금지될 예정입니다.')
except DeprecationWarning:
    print("DeprecationWarning이 실제로 발생함")
    pass

>>>
UserWarning: 이 사용법은 향후 금지될 예정입니다.
~~~
- 오류를 무시하는 방법: `warnings.simplefilter('ignore')`
- 프로덕션 배포 후 warning -> error로 발생하는 것은 위험하므로, logging 내장 모듈에 복제하는 것을 고려할 수 있음
- 실제 사용시 발생할 수 있는 미묘한 경우를 테스트가 다 체크하지 못한 경우에 이런 기능을 사용하는 것이 좋음
- API 라이브러리 관리자는 `contextManager`를 통해 `warnings.catch_warnings`를 저장하고, 경고 메세지 개수, 분류 등을 확인 가능
~~~python
with warnings.catch_warnings(record=True) as found_warnings:
    found = warnings.warn('warning!', DeprecationWarning)

assert len(found_warnings) == 1
single_warnings = found_warnings[0]
assert single_warnings.category == DeprecationWarning
~~~

### 90-typing 정적 분석을 통해 버그를 없애라
- API는 문서를 보고 참조할 수도 있지만 typing 모듈을 통해 정적 분석 도구 지원
- <b>typing 모듈은 타입 검사 기능은 지원하지 않음</b>
- 대표적인 typing 지원 도구는 mypy, pyre 등이 있음
- mypy와 함꼐 프로그램 실행 방법 `$ python3 -m mypy --strict example.py`
- 함수 --> 타입 에너테이션 지정 방법
~~~python
def subtract(a: int, b: int) -> int:
    return a - b
~~~
- 다음은 덕타입을 지원하는 제너릭 함수에 에너테이션을 붙인 예제
~~~python
from typing import Callable, List, TypeVar

Value = TypeVar('Value')
Func = Callable[[Value, Value], Value]

def combine(func: Func, values:list[Value]) -> Value:
    ...
~~~
- typing 모듈에 예외는 포함되지 않는다는 사실에 유의. 파이썬 typing 모듈은 예외를 인터페이스 정의의 일부분으로 간주하지 않음
- `from __future__ import annotation`을 사용하면(3.7이상) 전방 참조 가능
~~~python
from __future__ import annotations

class FirstClass:
    def __init__(self, value: SecondClass) -> None:
        self.value = value

class SecondClass:
    def __init__(self, value: int) -> None:
        self.value = value


second = SecondClass(5)
first = FirstClass(second)
~~~
- 타입 힌트는 100% 사용하지 말고, 중요한 부분에만 사용하자

## 용어 정리
- refactoring
  - 외부 동작을 바꾸지 않으면서, 내부 구조를 개선하는 일
  - 코드가 작성된 후에 디자인을 개선하는 방법
  - 모든 것을 미리 생각하기보다는 개발하면서 지속적으로 좋은 디자인을 찾음
- 제너릭 함수
  - 어떤 하나의 함수가 여러 타입의 인자를 받고, 인자의 타입에 따라 적절한 동작을 하는 함수 
  - 클래스 내부에서 사용할 데이터 타입을 외부에서 지정하는 기법
- 직렬화
  - 파이썬 객체를 일련의 byte들로 변환하는 것을 직렬화, 그 반대로 decode하는 것을 역직렬화라고 함 

## effective_python 간단정리
### 1-bytes와 str 차이 알아두기
- 파이썬은 문자열 데이터의 시퀀스 표현방법은 두 가지
  - `bytes`, `str`
- bytes 타입의 인스턴스에는 부호가 없는 8바이트 데이터가 그대로 들어감
- str 인스턴스에는 사람이 사용하는 언어의 문자를 표현하는 유니코드 코드 포인트가 들어있음
- 중요한 것은 str 인스턴스에는 직접 대응하는 이진 인코딩이 없고, bytes에는 직접 대응하는 텍스트 인코딩이 없음
- 두 개를 구분하는 help function을 만들어서 적용해야 함
~~~python
def to_str(str_or_bytes):
    if isinstance(str_or_bytes, bytes):
        return str_or_bytes.decode('utf-8')
    else:
        return str_or_bytes
~~~
- `bytes`와 `str`는 연산이 불가능함

### 2-str-format 보다는 f-문자열을 사용하자
- f-문자열은 간결하지만 위치 지정자 안에 파이썬 식을 포함시킬 수 있어 강력함
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
~~~python
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
b = a
print("이전 a", a)
print("이전 b", b)
a[:] = [101, 102, 103]
print("이후 a", a)
print("이전 b", b) #- 중요! 

>>>
이전 a ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
이전 b ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
이후 a [101, 102, 103]
이전 b [101, 102, 103]
~~~


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
    numbers.sort(key=helper)
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
- <b>wrap를 wrapper 함수에 적용하면, wraps가 데코레이터 내부에 들어가는 함수에서 중요한 메타데이터를 복사해서 wrapper 함수에 적용해줌</b>
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
comp1 = [x ** 2 for x in range(10) if x % 2 == 0]
map1 = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, range(10))))
assert comp1 == map1
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
- 다른 InputData나 Worker 하위 클래스를 사용하고 싶다면 각 하위 클래스에 맞게 generate_inputs, create_workers, mapreduce를 재작성해야 함
- 즉 객체를 구성할 수 있는 제너릭한 방법이 필요하다는 것ㄴ
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
- <b>내장 `collection.abc` 모듈 안에 컨테이너 타입에 정의해야 하는 전형적인 메서드를 모두 제공하는 추상 기반 클래스 정의가 여러가지 들어가 있음</b>
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

### 44-세터와 게터 메서드 대신 평범한 애트리뷰트를 사용해라
- `@property`, `@func.setter`를 사용해서 함수를 선언하면, 세터와 게터 기능이 제공됨
- 위의 두 데코레이션을 사용하면, 값을 할당하거나 가져갈 때 제약을 걸 수 있고, 예외처리가 가능함
- `@property`를 사용해 부모 클래스의 애트리뷰트도 제한할 수 있음
- `@property`를 사용할 때는 단순히 get, set 구현 이외의 동작(특히 heavy code)은 일반 메소드를 사용해야 함  
예를 들어 시간이 오래 걸리는 help function, I/O, DB query등의 질의는 사용X
- 또한 해당 애트리뷰트를 제외한 다른 애트리뷰트를 정의하거나 할당하면 디버깅이 어려워짐
- `@property`의 가장 큰 단점은 하위 클래스 사이에서만 공유가 가능하며, 다른 클래스와 공유는 불가능. 이럴 때는 descriptor를 제공
- 다음은 `@property`를 통한 코드 예시
~~~python
class Resister:
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


class FixedResistance(Resister):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms #- self.ohms라고 하면 무한 recurive에 빠짐

    @ohms.setter
    def ohms(self, ohms):
        #- 부모 객체인 경우, error 발생
        if hasattr(self, '_ohms'):
            raise ValueError('ohms는 불변 객체입니다.')
        self._ohms = ohms


test = FixedResistance(0)
test.voltage = 10
test.ohms = 20              #- ValueError 
~~~

### 45-애트리뷰트를 리펙터링하는 대신 @property를 사용해라
- `@property`의 고급 사용법으로 간단한 수치 애트리뷰트를 특정 변수 할당이나 호출에 따라 계산해 제공하는 방법이 있음
- <b>기존 클래스를 호출하는 코드를 전혀 바꾸지 않아도, 클래스 애트리뷰트의 기존 동작을 변경할 수 있기 때문에 유용함</b>
- `@property`는 인터페이스를 점차 개선해나가는 과정에서 중간 필요한 기능들을 제공하는 수단으로 유용
- 다음의 코드는 leaky bucket(리키 버킷) 흐름 제어 알고리즘을 구현한 것  
  `Bucket` 클래는 남은 가용 용량(quota)와 잔존 시간을 표현함
~~~python
from datetime import datetime, timedelta


class Bucket:
    '''
    시간을 일정한 간격으로 구분하고, 가용 용량을 전부 소비하거나, period가 지났을 떄
    가용 용량을 reset됨

    시간이 reset되면 알아서 quota를 채워주는 것이 아님.
    '''
    def __init__(self, period):
        '''args
        timedelta: 시간에 대해서 period를 입력받아 datetime 형태로 반환
                    datetime 자료형과 사칙연산이 가능
        quota: 사용 가용 용량
        '''
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return f"Bucket(quota= {self.quota})"


def fill(bucket, amount):
    '''bucket에 용량을 채워주는 함수

    현재 시간과 instance reset time의 차가 period보다 크면
    시간과 quota reset
    그렇지 않으면 quota에 += amount

    args
        bucket: bucket class instance
        amount: 가용하고자 하는 양
    '''
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.reset_time = now
        bucket.quota = 0
    bucket.quota += amount


def deduct(bucket, amount):
    '''bucket에 용량 할당 가능 여부 확인 함수

    now - reset_time > period  --> False(quota = 0이 되므로)
    bucket.quota - amount < 0  --> False
    '''
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    else:
        bucket.quota -= amount
        return True


bucket = Bucket(60)
fill(bucket, 100)
print(bucket)

if deduct(bucket, 99):
    print("99 용량 사용")
else:
    print("가용 용량이 작아서 99 용량을 처리할 수 없음")

if deduct(bucket, 3):
    print('3 용량 사용')
else:
    print("가용 용량이 작아 사용할 수가 없습니다.")
print(bucket)
~~~
- 위 코드의 문제점 
  - 버킷 시작시 가용 용량이 얼마인지 알 수 없음
  - 버킷에 새로운 가용 용량을 할당하기 전까지는 defualt는 항상 False를 반환
  - `deduct`를 호출하는 쪽에서 자신이 차단된 이유를 명확히 파악하기 어려움
- 위 코드의 문제점을 해결하고자 재설정된 가용 용량인 `max_quota`와 이번 주기 버킷에서 소비한 용량의 합계인 `quota_consumed`를 추적하도록 클래스를 변경 가능
- 이 때 `@property`를 사용해서 간략한 코드로 구현 가능!
~~~python
from datetime import datetime, timedelta

def fill(bucket, amount):
    #- bucket : bucket class
    #- amount : 가용 용량
    now = datetime.now()
    #- 지나간 시간이 period보다 길면, 가용용량과 시간 reset 시킴
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


#- 필요한 용량 할당 가능 여부 확인
def deduct(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        print("time check")
        return False
    if bucket.quota - amount < 0:
        print(f"bucket.quata:{bucket.quota} - {amount}")
        return False
    else:
        bucket.quota -= amount
        return True #- bucket의 가용 용량이 충분하므로, 필요한 분량을 사용함

class NewBucket:
    def __init__(self, period):
        '''
        args
            max_quota: 재설정 가용 용량(주기 동안 채워 넣은 양)
            quota_cosumed: 주기 동안 소비된 양
        '''
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return (f"NewBucket(max_quota={self.max_quota}), "
                f"quota_consumed={self.quota_consumed}")

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        '''

        amount == 0: 새로운 주기가 되고 가용 용량을 재설정
        delta <0 & quota_consumed == 0 d --> 새로운 주기가 되고 가용 용량을 추가하는 경우
        '''
        delta = self.max_quota - amount
        if amount == 0:
            self.quota_consumed = 0
            self.max_quota =0
        elif delta < 0:
            assert self.quota_consumed == 0
            self.max_quota += amount
        else:
            assert self.max_quota > self.quota_consumed
            self.quota_consumed += delta

bucket = NewBucket(60)   #- 60초 setting
print("최초 bucket:", bucket)
fill(bucket, 100)
print("보충 후:", bucket)


if deduct(bucket, 99):
    print("99 용량 사용")
else:
    print("가용 용량이 작아 99 용량을 처리할 수 없음")

print(bucket)

>>>
최초 bucket: NewBucket(max_quota=0), quota_consumed=0
보충 후: NewBucket(max_quota=100), quota_consumed=0
99 용량 사용
여전히  NewBucket(max_quota=100), quota_consumed=99
~~~
- 가장 좋은 점은 <b>Bucket.quota</b>를 사용하는 코드를 변경할 필요도 없고 이 클래스의 구현이 변경됐음을 알 필요도 없음
- 객체가 처음부터 제대로 인터페이스를 제공하지 않거나 아무 기능도 없는 데이터 컨테이너 역할만 하는 경우가 실전에서 자주 발생
- 시간이 지나면서 코드가 커지거나, 프로그램이 다루는 영역이 넓어지거나, 장기적으로 코드를 깔끔하게 유지할 생각이 없는 프로그래머들이 코드에 기여하는 등의 경우 이런 일이 발생
- <b>너무 @property를 과용하지는 말고, 많아지면 클래스를 리펙터링 해야함</b>

### 46-재사용 가능한 @property 메서드를 만들려면 디스크립터를 사용해라
- `@property`의 문제점
  - 가장 큰 문제점은 재사용성인데, 같은 클래스에 속하는 여러 애트리뷰트로 사용이 안되고, 서로 무관한 클래스 사이에서 `@property` 데코레이터를 적용한 메서드를 재사용할 수도 없음 
- 예를 들어 학생의 특정 과목 점수가 백분율(1 ~ 100사이) 값인지를 검증하는 코드를 구현할 때, `@property`를 사용해서 구현이 가능함, 하지만 과목 개수가 늘어날 때마다 일일이 `@property`와 `@func.setter`함수를 구현해야하고, 수정이 있을 때마다 각 메서드를 전부 수정해 주어야 함
- 이런 경우 파이썬에서 적용할 수 있는 좋은 방법은 디스크립터(descriptor)를 사용하는 것
- 디스크립터 프로토콜은 파이썬 언어에서 애트리뷰트 접근을 해석하는 방법을 정의함
- <b>디스크립터 클래스는 `__get__` 과 `__set__`</b> 함수를 제공하고, 이 두 메서드를 사용하면 별다른 준비 코드 없이 검증을 편하게 할 수 있음
- 같은 로직을 한 클래스 안에 속한 여러 다른 애트리뷰트에 적용할 수 있으므로, 디스크립터가 믹스인보다 낫다
- 다음 코드는 Grade의 인스턴스인 클래스 애트리뷰트가 들어있는 Exam 클래스를 생략 정의함  
~~~python
class Grade:
    def __get__(self, instance, instance_type):
        ...

    def __set__(self, instance, value):
        ...


class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


exam = Exam()
exam.writing_grade = 40
#- 다음과 같이 해석됨
Exam.__dict__['writing_grade'].__set__(exam, 40)

exam.writing_grade
#- 다음과 같이 해석됨
Exam.__dict__['writing_grade'].__get__(exam, Exam)
~~~
- 이런 동작을 이끌어 내는 것은 `__getattribute__` 메서드임
- Exam 인스턴스 `writing_grade` 라는 이름의 애트리뷰트가 없으면, Exam 클래스의 애트리뷰트를 대신 사용. 이 클래스의 애트리뷰트가 `__get__`, `__set__` 메서드가 정의된 객체라면 디스크립터 프로토콜을 따라야 한다고 결정
- 다음과 같이 디스크립터를 정의할 수 있는데, 문제는 Grade 인스턴스를 공유할 시 문제 발생
~~~python
class Grade:
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError("점수는 0과 100사이 입니다.")
        self._value = value

first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print("쓰기 : ", first_exam.writing_grade)
print("과학 : ", first_exam.science_grade)

#- 문제는 여기서 발생
second_exam = Exam()
second_exam.writing_grade = 75
print(f"두 번쨰 쓰기 점수 : {second_exam.writing_grade} 맞음")
print(f"첫 번쨰 쓰기 점수 : {first_exam.writing_grade} 틀림: 82점이어야 함")

>>>
쓰기 :  82
과학 :  99
두 번쨰 쓰기 점수 : 75 맞음
첫 번쨰 쓰기 점수 : 75 틀림: 82점이어야 함
~~~
- 프로그램이 실행되는 동안, Exam 클래스가 처음 정의될 때, 이 애트리뷰트에 대한 Grade 인스턴스가 단 한번만 생성됨
- Exam 인스턴스가 생성될 때마다 Grade 인스턴스가 생성되지는 않음
- 이를 해결하려면 Grade 클래스가 각각 Exam 인스턴스에 대해 값을 따로 찾게 해야함
  인스턴스별 상태(ex) `dict[instance]`)를 딕셔너리에 저장하면 이런 구현이 가능
~~~python 
class Grade:
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError("점수는 0과 100 사이에 존재해야함")
        else:
            self._values[instance] = value
~~~
- 위의 코드는 메모리를 누수시킴. `values` 딕셔너리는 프로그램이 실행되는 동안 `__set__` 호출에 전달된 모든 Exam 인스턴스에 대한 참조 저장함
- 따라서 참조 카운터가 0이 될 수 없으며, 따라서 garbage collection이 인스턴스 메모리를 재활용 못함
- 이 문제를 해결하기 위해 파이썬 `weakref` 내장 모듈을 사용할 수 있음
- 이 모듈은 `WeakKeyDictionary`라는 특별한 클래스를 제공하며, `_values`의 딕셔너리 대신 이 클래스 사용 가능
- `WeakKeyDictionary`는 약한 참조를 사용하므로, gc가 언제든지 재활용 가능
- `self._values = WeakkeyDictionary()`

### 47-지연 계산 애트리뷰트가 필요하면 `__getattr__`, `__getattribute__`, `__setattr__`을 사용해라
- 파이썬은 훅을 활용하면 시스템을 서로 접합하는 제너릭 코드를 쉽게 작성할 수 있음
- 이러한 제너릭 코드를 작성하기 위해 앞서 배운 평범한 인스턴스 애트리뷰트나, `@property`, 디스크립터는 미리 애트리뷰트를 정의해야 하므로 사용할 수 없음
- 이런 용도에는 <b>`__getattr__`이라는 특별 메서드 사용하면 됨</b>. 이 특별 메소드는 객체의 인스턴스 딕셔너리에 찾을 수 없는 애트리뷰트에 접근할 때마다 `__getattr__`이 호출됨
- `__getattr__(self, name)`, `setattr(self, name, value)`로 들어감
~~~python
class LazyRecord:
    def __init__(self):
        self.exists = 5

    #- name: attribute
    def __getattr__(self, name):
        value = f"{name}을 위한 값"
        setattr(self, name, value)
~~~
- 항상 조심해야 할 것은 무한 재귀를 조심해서 코드를 구현하자
~~~python
class LoggingLazyRecord(LazyRecord):

    def __getattr__(self, name):
        print(f"*호출: __getattr__({name!r})"
                f"인스턴스 딕셔너리 채워 넣음")
        result = super().__getattr__(name)
        print(f"*반환: {result!r}")
        return result
~~~
- 이런 기능은 예를 들어 스키마가 없는 데이터에 지연 계산으로 접근하는 등의 활용이 필요할 때 아주 유용
- `__getattribute__` 특별 메서드는 DB의 트렌젝션 코드를 구현할 때 처럼 항상 애트리뷰트에 접근할 때 사용가능
- `__getattr__`과 `__getattribute__`에서 존재하지 않는 프로퍼티를 사용할 때 발생하는 표준적인 예외가 Attribute error임
- 파이썬에서 기본 기능을 구현할 때는 `hasattr` 또는 `getattr` 내장 함수를 통해 프로퍼티 값을 꺼내오는 기능 사용가능
- 위의 두 함수는 `__getattr__` 호출 전에 인스턴스 딕셔너리에 존재하는지 확인. 없으면 `__getattr__` 호출 
- `__getattribute__`와 `__setattr__` 함수의 문제점은 원하지 않을 때도 항상 호출을 한다는 점  
다음과 같이 어떤 객체와 관련된 키가 있을 때만 접근하고 싶다고 하자
~~~python
class Parent:
    def __init__(self, data):
        self._data = data    #- 생성자 초기 입력 dict

    def __getattribute__(self, name):
        data_dict = super().__getattribute__('_data')
        return data_dict.get(name, 0)
~~~
- <b>__getattribute__와 __setattr__ 에서 무한 재귀를 피하려면 super()에 있는 메서드를 사용해 인스턴스 애트리뷰트에 접근하자</b>
- `__setattr__`은 애트리뷰트에 값을 입력할 때마다 호출되어 사용됨


### 48- `__init__subclass__`를 사용해 하위 클래스를 검증해라
- 메타클래스를 정의하지 않고 하위 클래스를 검증하는 방법(python 3.6이상)으로 `__init__subclass__` 특별 메서드 사용 가능
- 
~~~python
class BetterPolygon:
    sides = None

    def __init_subclass__(cls):
        if cls.sides < 3:
            raise ValueError("side는 3 이상이어야 합니다.")

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180
~~~
- `__init__subclass__` 메소드 말고도 Meta class의 `__new__`를 이용해서 하위 클래스 애트리뷰트 설정 가능
- 메타클래스는 type을 상속해서 정의
- 메타클래스는 `__new__` 메서드를 통해 자신과 연관된 클래스의 내용을 받음
- 다음의 메타클래스 정의를 보여주는 코드
- 클래스 이름(name), 클래스가 상속하고 있는 부모 클래스들(bases), class 본문에 정의된 모든 클래스 애트리뷰트(class_dict)에 접근 가능
- 모든 클래스는 object를 상속하고 있지만, 메타클래스가 받는 부모 클래스의 튜플 안에는 object가 들어있지 않음
- <b>클래스 정의 전에 클래스의 파라미터 검증이 필요하다면, `__new__` 에 기능 추가</b>
~~~python
class MetaClass(type):
    def __new__(meta, name, bases, class_dict):
        print(f"실행 : {name}, 메타 {meta}.__new__")
        print(f"기반 클래스들 : {bases}")
        print(class_dict)
        return type.__new__(meta, name, bases, class_dict)

#- 다음과 같이 하위 클래스의 애트리뷰트 검증 가능 - Meta class 이용
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        if bases:
            if class_dict['sides']  < 3:
                raise ValueError('다각형 변은 3개 이상이어야 함')
        return type.__new__(meta, name, bases, class_dict)
~~~
- 메타클래스의 단점은 여러개의 메타클래스를 지정받을 수 없음
- `__new__` 는 클래스의 본문이 처리된 직후 수행됨. 즉 메타클래스를 사용하면 정의된 직후, 인스턴스 선언 전에 정의를 변경할 수 있음
- 메타클래스를 사용하면 너무 복잡해질 수 있으므로, `__init__subclass__`를 사용 권장
- `__init_subclass__` 정의에서 `super().__init_subclass__`를 호출해 여러 계층에 걸쳐 클래스를 검증하고 다중 상속을 제대로 처리하도록 해라
- `__init_subclass__` 특별메서드는 클래스 인스턴스가 만들어지기 직전에 코드 검증

### 49- __init__subclass__를 사용해 클래스 확장을 등록해라
- 다음 코드는 직렬화와 역직렬화를 수행하는 코드를 구현  
  이 때 다양한 CASE로 직렬화를 수행하지만, 이를 역직렬화하는 함수는 공통으로 구현
- `__init__subclass__`를 사용해서 특별 메서드를 이용
~~~python
#- 역직렬화를 공통 함수로 가져가게끔 할 수 있는 전략
#- 직렬화 할 때, 'class':key를 생성
#- register_class 함수를 통해 registry 인스턴스 딕셔너리에 저장
#- 역직렬화 수행시, registry 안에 있는 함수에 해당 클래스 사용해서 수행
#- 역직렬화 된 값은 다시 클래스로 할당해 __repr__ 결과값으로 출력되게끔 함

import json

registry = {}


def register_class(target_class):
    registry[target_class.__name__] = target_class


def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])


class BetterSerializable:
    def __init__(self, * args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args
        })

    def __repr__(self):
        name = self.__class__.__name__
        params = ','.join(str(x) for x in self.args)
        return f"{name}({params})"


class BetterRegisteredSerializable(BetterSerializable):
    def __init_subclass__(cls):
        super().__init_subclass__()
        register_class(cls)


class Vector1D(BetterRegisteredSerializable):
    def __init__(self, magnitude):
        super().__init__(magnitude)
        self.magnitude = magnitude


before = Vector1D(6)
data = before.serialize()
deserialize(data)
~~~
- 클래스 등록(`registry`)는 파이썬 프로그램을 모듈화 할 때 유용한 패턴
- 메타클래스를 사용하면 프로그램 안에서 기반 클래스를 상속한 하위 클래스가 정의될 때마다 등록 코드를 자동으로 실행 가능
- 메타클래스를 클래스 등록에 사용하면 클래스 등록 함수를 호출하지 않아서 생기는 오류를 피할 수 있음
- 표준적인 메타클래스 방식보다 `__init__subclass__`가 더 다음. 깔끔하고 초보자가 이해하기 쉬움

### 50-`__set__name__` 으로 클래스 애트리뷰트를 표시해라
- 메타클래스의 기능 중, 클래스 정의 이후와 클래스 사용 시점 이전에 프로퍼티를 변경하거나 표시할 수 있는 기능
- 애트리뷰트가 포함된 클래스 내부에서 애트리뷰트를 좀 더 관찰하고자 디스크립터를 쓸 때 이런 접근 방식 활용
- `getattr(instance, name, 'defaultValue')`, `setattr(instance, name, value)`
- 디스크립터 클래스를 사용함으로써 Field 인스턴스를 할당받은 애트리뷰트 값이 변화할 때, `setattr` 내장 함수를 통해 인스턴스별 상태를 직접 인스턴스 딕셔너리에 저장할 수 있고, 나중에 `getattr` 인스턴스의 상태를 읽을 수 있음
- return시 호출 애트리뷰트 명이 아닌 다른 명으로 (`_value`) 호출하지 않으면 무한재귀 현상 발생
~~~python
class Field:
    def __init__(self, name):
        self.name = name
        self.internal_name = "_" + self.name

    def __get__(self, instance, instance_type):
        # print("instance : ", instance)
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Customer:
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')
~~~
- 위의 코드에서 `first_name = Field('first_name')` -> `first_name = Field()` 로 변경하기 위한 메타클래스 정의
~~~python
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                print(f"key : {key}, value : {value}")
                value.key = key
                value.internal_name = "_" + key
            cls = type.__new__(meta, name, bases, class_dict)
            return cls


class DatabaseRow(metaclass=Meta):
    pass


class Field:
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        # print("instance : ", instance)
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()
~~~
- 하지만 `DatabaseRow` 메타클래스 상속을 잊거나, 불가피하게 상속받지 못하는 경우가 있을 수 있는데, 이 때 `__set__name__`(파이썬 3.6이상) 메서드 사용 가능
- 클래스가 정의될 때마다 파이썬은 해당 클래스 안에 들어있는 디스크립터 인스턴스인 `__set__name__`을 호출함
- <b>`__set__name__`은 디스크립터 인스턴스를 소유 중인 클래스와 디스크립터 인스턴스가 대입될 애트리뷰트 이름을 인자로 받음</b>
~~~python
class Field:
    '''
    __set_name__:
        name --> LHS에 존재하는 애트리뷰트
    '''
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.internal_name = "_" + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(self, self.internal_name, "")

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class FixedCustomer:
    first_name = Field()

test = FixedCustomer()
print(test.__dict__)
test.first_name = '메르센'
print(test.__dict__)
~~~


### 51-합성 가능한 클래스 확장이 필요하면 메타클래스보다는 클래스 데코레이터를 사용해라
- 메타클래스 사용시 처리하지 못하는 경우가 있는데, 예를 들어 클래스의 모든 함수 및 메서드에 전달되는인자, 반환 값, 발생한 예외를 출력하고 싶다고 했을 때, 여러 메타클래스를 사용하기도 어렵고, 클래스에 대한 제약이 너무 많음
- <b>이 때 파이썬은 클래스 데코레이터을 지원함. 클래스 데코레이터는 함수 데코레이터처럼 사용할 수 있음</b>
- 클래스 선언 앞에 @ 기호와 데코레이터 함수를 적으면 됨. 이때 데코레이터 함수는 인자로 받은 클래스를 적절히 변경해서 재생성해야 함
~~~python
def my_class_decorator(klass):
    klass.extra_param = 'check'
    return klass

@my_class_decorator
class MyClass:
    pass

print(MyClass)
print(MyClass.extra_param)

>>>
<class '__main__.MyClass'>
check
~~~
- 다음과 같이 클래스 데코레이터를 사용해서 전체 코드를 구현할 수 있음
~~~python
import types
from functools import wraps


def trace_func(func):
    if hasattr(func, 'tracing'):
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            result = e
            raise
        finally:
            print(f"{func.__name__}({args!r}, {kwargs!r}) -> "
                  f"{result!r}")

    wrapper.tracing = True
    return wrapper


trace_types = (
    types.MethodType,
    types.FunctionType,
    types.BuiltinFunctionType,
    types.BuiltinMethodType,
    types.MethodDescriptorType,
    types.ClassMethodDescriptorType)


def trace(klass):
    for key in dir(klass):
        value = getattr(klass, key)
        if isinstance(value, trace_types):
            wrapped = trace_func(value)
            setattr(klass, key, wrapped)
    return klass


@trace
class TraceDict(dict):
    pass

trace_dict = TraceDict([('안녕', 1)])
trace_dict['거기'] = 2
trace_dict['안녕']

>>>
__new__((<class '__main__.TraceDict'>, [('안녕', 1)]), {}) -> {}
__getitem__(({'안녕': 1, '거기': 2}, '안녕'), {}) -> 1
~~~

### 65- try/except/finally의 각 블록을 잘 활용해라
- `finally`
  - 예외가 필요하더라도, 정리 코드가 필요할 때 사용(ex) 파일 핸들을 안전하게 닫기 위하여) 
- 복합적인 문장 안에 모든 요소를 다 사용하고 싶다면, `try/except/else/finally`를 사용하자
- `else` 블록을 사용하면, try 블록에 들어갈 코드를 최소화 할 수 있으며, try 블록에 들어가는 코드가 줄어들면 발생할 여지가 있는 예외를 서로 구분할 수 있으므로 가독성이 좋아짐
~~~python
UNDEFINED = object()

def divide_json(path):
    print("파일 열기")
    handle = open(path, 'r+')
    try:
        print("* 데이터 읽기")
        data = handle.read()
        print("* JSON 데이터 읽기")
        op = json.loads(data)      #- valueError가 발생할 수 있음
        print("* 계산 수행")
        value = (
            op['numerator'] / op['denominator'])
    except ZeroDivisionError as e:
        print("* ZeroDivisionError 처리")
        return UNDEFINED
    else:
        print("* 계산 결과 쓰기")
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)        #- 파일의 커서 위치를 0(맨처음)으로 이동
        handle.write(result)
        return value
    finally:
        print("* close() 호출")
        handle.close()
~~~

### 66-재사용 가능한 try/finally 동작을 원한다면 contextlib와 with문을 사용해라
- 파이썬의 `with` 문은 코드가 특별한 컨텍스트(context) 안에서 실행되는 경우를 표현
- 예를 들어 mutually exclusive mutax lock을 with 문에서 사용하면 lock을 소유했을 때만 코드 블록이 실행되는 것을 의미함 
~~~python
from threading import Lock
lock = Lock()
with lock:
    ...

#- 위의 with 문은 아래 코드문과 동일함
lock.acquire()
try:
    #
    ...
finally:
    lock.release()
~~~
- 이 경우에는 with 문 쪽이 더 나음. `try/finally` 구조를 반복적으로 사용할 필요가 없고 코드를 빠트릴 염려가 없기 때문
- `contextlib` 내장 모듈을 사용하면 우리가 만든 객체나 함수를 `with` 문에 쉽게 쓸 수 있음
- `contextlib` 모듈은 `with` 에 쓸 수 있는 함수를 간단히 만들 수 있는 `contextmanager` 데코레이터를 제공함
- 다음은 특정 CASE에서 logging level을 변경시켜 Logging 하기 위하여 `contextmanager`를 구현한 코드 예제
~~~python
import logging
from contextlib import contextmanager

def my_function():
    logging.debug('디버깅 데이터')
    logging.error('이 부분은 오류 로그')
    logging.debug('추가 디버깅 데이터')


@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)


with debug_logging(logging.DEBUG):
    print("* 내부")
    my_function()

print("* 외부")
my_function()
~~~
- `with`문에 전달된 컨텍스트 매니저가 객체를 반환할 수도 있음. 이렇게 반환된 객체는 with 복합문의 지역 변수로 활용됨
- 가장 큰 활용의 예로, `with`문에 open을 전달하면 `as`를 통해 대상으로 지정된 파일 핸들을 전달, `with` 블록을 나갈 때 핸들을 닫음
~~~python
filename = 'test.txt'
with open(filename, 'w') as handle:
    handle.write('데이터 입니다.')
~~~
- 이 코드에서 문제가 될 수 있는 부분을 강조함으로써, 파일 핸들이 열린 채로 실행되는 코드의 양을 줄이도록 우리를 복돋음
- `contextmanager` 데코레이터를 적용한 함수에서 `as` 에게 대상변수를 넘기기 위한 방법은 `yield` 를 선언해서 넘기면 됨
~~~python
@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)

with log_level(logging.DEBUG, 'my_log') as logger:
    logger.debug(f"대상 : {logger.name} !")
    logging.debug('이 메세지는 출력되지 않음')

>>>
DEBUG:my_log:대상 : my_log !
~~~

#### 핵심 내용
- `with` 문을 사용하면, `try/finally` 블록을 통해 사용해야 하는 로직을 재활용하면서 시각적인 잡음도 줄일 수 있음
- `contextlib` 내장 모듈이 제공하는 `contextmanager` 데코레이터를 사용하면 with 문에 사용가능
- 컨텍스트 매니저가 `yield` 하는 값은 `with` 문의 `as` 부분에 전달됨. 이를 활용하면 특별한 컨텍스트 내부에서 실행되는 코드 안에서 직접 그 컨텍스트에 접근할 수 있음

### 67-지역 시간에는 time 보다는 datetime 을 활용해라
- 협정 세계시(Coordinated Universal Time, UTC)는 시간대와 독립적으로 시간을 나타낼 때 쓰는 표준. 유닉스 기준 시간이 몇 초 흘렀는지를 계산하는데, 현재 위치를 기준으로 시간을 계산하는 인간에게는 적합하지 않음
- 파이썬에서 시간대를 변환하는 방법은 `time` 내장 모듈을 사용하거나, `datetime` 모듈을 사용하는데, `datetime` 모듈을 사용하자

#### time 모듈
- time 모듈이 플랫폼에 따라 다르게 작동함
- time 모듈의 동작은 호스트 운영체제의 C 함수가 어떻게 작동하는지에 따라 달라짐
- 따라서 파이썬에서는 time 모듈의 동작을 신뢰할 수 없으며, 여러 시간대에서 time 모듈이 일관성 있게 동작한다고 보장할 수 없으므로, 여러 시간대를 다뤄야 하는 경우에는 time 모듈 사용하면 안됨

#### datetime 모듈
- `datetime`도 마찬가지로 여러 시간대에 속한 시간을 상호 변환할 수 있음
~~~python
from datetime import datetime, timezone

now = datetime(2021, 5, 29, 10, 10, 4)
now_utc = now.replace(tzinfo=timezone.utc)
now_local = now_utc.astimezone()
print(now_local)

>>>
2021-05-29 19:10:04+09:00

#- local time -> UTC Timezone
time_str = '2021-05-29 14:09:10'
time_format = '%Y-%m-%d %H:%M:%S'
now = datetime.strptime(time_str, time_format)
time_tuple = now.timetuple()
utc_now = time.mktime(time_tuple)

~~~
- `datetime` 모듈은 한 지역 시간을 다른 지역 시간으로 바꾸는 신뢰할 수 있는 기능을 제공
- `datetime`은 `tzinfo` 클래스와 이 클래스 안에 있는 메서드에 대해서만 시간대 관련 기능을 제공
- 파이썬 기본 설치에는 UTC를 제외한 시간대 정의가 들어있지 않음
- `pytz` 패키지를 설치하여, default로 제공되지 않는 시간대 정보를 추가할 수 있음
- `pytz`에는 우리에게 필요한 모든 시간대 정보에 대한 완전한 데이터베이스가 들어있음
- <b>`datetime`과 pytz를 사용하면 호스트 컴퓨터가 실행 중인 운영체제와 관계없이 어떤 환경에서도 일관성 있게 시간을 변환할 수 있음</b>

### 68- copyreg를 사용해 pickle을 더 신뢰성 있게 만들어라
- `pickle` 내장 모듈을 사용하면 파이썬 객체를 바이트 스트림으로 직렬화하거나, 바이트 스트림을 객체로 역직렬화 할 수 있음
- `pickle`의 문제점은 `pickle`로 저장 후, 클래스를 변경하고 다시 로드하면 저장된 클래스 애트리뷰트 그대로 저장되어 있음
- `copyreg` 내장 모듈을 사용하면 이런 문제를 쉽게 해결할 수 있음. 파이썬 객체를 직렬화, 역직렬화할 때 사용할 함수를 등록할 수 있으므로 pickle 동작을 제어할 수 있고, 그에 따라 `pickle` 동작의 신뢰성을 높일 수 있음
~~~python
import pickle

class GameState:
    def __init__(self, level=0, lives=4, points=0, magic=10):
        self.level = level
        self.lives = lives
        self.points = points
        


def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs, )


def unpickle_game_state(kwargs):
    return GameState(**kwargs)

import copyreg
copyreg.pickle(GameState, pickle_game_state)

state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)
~~~
- 위의 예제에서, 필드를 제거하면 오류 발생. 이때 `copyreg` 함수에게 전달하는 함수에 버전 파라미터를 추가하면 이 문제 해결 가능
- <b>클래스가 바뀔 때마다 버전을 지정하여 `unpickle_game_state`를 수정하면 됨</b>
- 만약 클래스 이름을 변경하거나, 클래스를 다른 모듈로 옮기는 방식으로 코드를 리펙터링 하는 경우가 있는데, 이 때 pickle이 깨지는 현상 발생
- 이 때 `copyreg`를 사용하여, 사용할 함수에 대해 클래스를 재지정 할 수 있음
~~~python
copyreg.pickle(BetterGameState, pickle_game_state)
~~~
- `unpickle_game_state` 함수가 위치하는 모듈의 경로는 바꿀 수 없음을 기억하자  
  어떤 함수를 사용해 데이터를 직렬화하고 나면, 해당 함수를 똑같은 임포트 경로에서 사용할 수 있어야 함

## 69-정확도가 매우 중요한 경우에는 decimal을 사용해라
- `double precision` 부동소수점 타입은 IEEE 754 표준을 따르고, 파이썬 언어는 허수 값을 포함하는 표준 복소수 타입도 제공함
- 하지만 IEEE 754 부동소수점 수의 내부 표현법으로 인해 결과는 올바른 값보다 약간 작음
~~~python 
rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print(cost)
>>>
5.364999999999999
~~~
- 이에 대한 해결책으로 `decimal` 내장 모듈에 들어있는 `Decimal` 클래스를 사용하는 것
- `Decimal` 클래스는 디폴트로 소수점 이하 28번째 자리까지 고정소수점 수 연산을 제공
- `Decimal`에 인스턴스를 지정하는 방법은 크게 두 가지인데, 첫 번째는 문자열로 지정하는 방법과, 두 번째는 int, float으로 지정하는 방법이 있음
- 정확한 답이 필요하다면, str로 지정해서 넣어라(정수를 넘길 때는 문제 X)
~~~python
print(Decimal('1.45'))
print(Decimal(1.45))

>>>
1.45
1.4499999999999999555910790149937383830547332763671875
~~~
- `Decimal` 클래스에는 원하는 소수점 이하 자리까지 근삿값을 계산하는 내장함수가 들어있음
~~~python
from decimal import ROUND_UP
Decimal('0.01').quantize(Decimal('0.01'), rounding=ROUND_UP)
print(f"반올림 전 {small_cost}, 반올림 후 : {rounded}")
~~~

### 70- 최적화하기 전에 프로파일링을 해라
- 파이썬은 프로그램이 각 부분이 실행 시간을 얼마나 차지하는지 결정할 수 있게 해주는 프로파일러를 제공
- 프로파일러가 있기 때문에 프로그램에서 가장 문제가 되는 부분을 집중적으로 최적화하고 프로그램에서 속도에 영향을 미치지 않는 부분은 무시할 수 있음
- 파이썬에는 두 가지 내장 프로파일러가 있음. 하나는 순수하게 파이썬으로 작성되었고, 하나는 C 확장 모듈로 되어 있음
- <b>cProfile 내장 모듈이 더 낫다. 이유는 프로파일 대상 프로그램의 성능에 최소롤 영향을 미치기 때문</b>
- 순수 파이썬 버전은 부가 비용이 많이 들어 결과가 왜곡될 수 있음
- <b>파이썬 프로그램을 프로파일링 할 때는 외부 시스템 성능이 아니라, 코드 자체 성능을 측정하도록 유의해야 함</b>
- 프로파일러 통계에서 각 열의 의미
  - `ncalls`: 프로파일링 기간 동안 함수가 몇 번 호출됐는지 보여줌
  - `tottime`: 프로파일링 기간 동안 대상 함수를 실행하는데 걸린 시간의 합계를 보여줌
  - `tottime percall`: 프로파일링 기간 동안 호출될 때마다 걸린 시간 평균
  - `cumtime`: 함수 실행시 걸린 누적 시간을 보여줌. 해당 함수를 호출한 다른 함수를 실행하는데 걸린 시간이 모두 포함됨
  - `cumtime percall`: 프로파일링 기간동안 함수가 호출될 때마다 누적 시간 평균을 보여줌
- 해당 함수가 많이 호출된 이유에 대해서는 알기 어려운데, 파이썬 프로파일러는 각 함수를 프로파일링한 정보에 대해 그 함수를 호출한 함수들이 얼마나 기여했는지를 보여주는 `print_callers` 메서드를 제공
~~~python
from cProfile import Profile
from random import randint
from pstats import Stats


def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result


def insert_value(array, value):
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)


max_size = 10 ** 4
data = [randint(1, max_size) for _ in range(max_size)]
test = lambda: insertion_sort(data)

profiler = Profile()
profiler.runcall(test)
stats = Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
stats.print_callers()
~~~

### 71-생산자-소비자 큐로 deque를 사용해라
- 다음의 코드는 email 송수신 하는 시스템을 생산자-소비자 queue를 구현한 것
~~~python
from random import randint


class Email:
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message


class NotEmailError(Exception):
    pass


def try_receive_email():
    pass


def produce_email(queue):
    while True:
        try:
            email = try_receive_email()
        except NotEmailError:
            return
        else:
            queue.append(email)


def consume_one_email(queue):
    if not queue:
        return
    else:
        email = queue.pop(0)
    print(f"read email: {email}")


def loop(queue, keep_running):
    while keep_running:
        produce_email(queue)
        consume_one_email(queue)

def my_end_func():
    return randint(1, 100) > 1


loop([], my_end_func())
~~~
- Email을 `produce_email`, `consume_one_email`로 구분해서 처리하는 이유는 지연 시간과 단위 시간당 스루풋 사이의 상충 관계로 귀결됨
- 생산자-소비자 문제를 큐로 리스트를 사용해도 어느 정도까지는 잘 동작하지만, 크기가 늘어나면 리스트 타입의 성능은 선형보다 나빠짐
- 리스트의 원소에 대해 `pop(0)`를 사용해 원소를 큐에서 빼내는데 걸리는 시간이 큐 길이가 늘어남에 따라 큐 길이의 제곱에 비례해 늘어나는 것을 볼 수 있음
- `pop(0)`를 하면 리스트의 모든 남은 원소를 제 위치로 옮겨야 해서, 전체 리스트 내용을 다시 제대입하기 떄문
- 리스트의 모든 원소에 대해 `pop(0)`를 호출하므로 대략 len(queue) * len(queue) 연산을 수행해야 모든 대기열 원소를 소비할 수 있음
- `deque(데크)`는 시작과 끝 지점에 원소를 빼거나 넣는데 걸리는 시간이 상수 시간이 걸림 

### 72-정렬된 시퀀스 검색을 할 때는 bisect를 사용해라
- 보통 리스트에서 `index` 함수를 사용해 특정 값을 찾아내려면 리스트 길이에 선형으로 비례하는 시간이 필요
- 파이썬 내장 `bisect` 모듈은 순서가 정해져 있는 리스트에 대해 이런 유형의 검사를 효과적으로 수행
- `bisect_left` 함수를 사용하면 정렬된 원소로 이루어진 시퀀스에 대해 이진 검색을 효율적으로 수행할 수 있음
- `bisect_left`가 반환하는 인덱스는 리스트에 찾는 값이 존재하는 경우 이 원소의 인덱스이며, 리스트에 찾는 값의 원소가 존재하지 않는 경우 정렬 순서상 해당 값을 삽입해야 할 자리의 인덱스
- `bisect` 모듈이 사용하는 이진 검색 알고리즘의 복잡도는 log복잡도  
이는 100만개의 리스트를 bisect로 정렬하는 속도와, 20인 리스트를 list.index로 정렬하는 속도가 동일하다는 의미
- `bisect`는 리스트 타입 뿐만 아니라, 시퀀스처럼 작동하는 모든 파이썬 객체에 대해 bisect 모듈의 기능을 사용할 수 있다는 점
~~~python
from bisect import bisect_left
from collections import deque

data = list(range(10**5))
bisect_left(data, 91234)

d = deque([i for i in range(100000)])
bisect_left(d, 91234)
~~~

### 73- 우선순위 큐로 heapq를 사용하는 방법을 알아두라
- 프로그램에서 원소 간의 상대적인 중요도에 따라 원소를 정렬해야 하는 경우가 있음. 이런 경우에는 우선순위 큐가 적합함
- 예를 들어, 도서관에서 대출한 책을 관리하는 프로그램을 작성할 때, 제출 기한을 넘긴 경우 통지하는 시스템을 만든다고 해보자
- 만약 리스트를 기반으로 만든다면, 책을 추가 할 때마다 제출 기한으로 정렬해야하는 추가비용 발생
- 또한 제출기한 전에 반납된 책을 제거 비용도 선형보다 커짐
- 이러한 문제를 우선순위 큐를 통해 해결할 수 있는데, 파이썬은 원소가 들어있는 리스트에 대해 우선순위 큐를 효율적으로 구현하는 내장 `heapq` 모듈 제공
- heap은 여러 아이템을 유지하되 새로운 원소를 추가하거나 가장 작은 원소를 제거할 때 로그 복잡도가 드는 데이터 구조
- 우선순위 큐에 들어갈 원소들이 서로 비교 가능하고 원소 사이에 자연스러운 정렬 순서가 존재해야 heapq 모듈이 제대로 작동 가능
- `functools` 내장 모듈이 제공하는 `total_ordering` 클래스 데코레이터를 사용하고 `__lt__` 특별 메서드를 구현하면 빠르게 Book 클래스를 비교 가능
~~~python
@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date

    def __lt__(self, other):
        return self.due_date < other.due_date

    def __repr__(self):
        return f"Book('{self.title}', '{self.due_date}')"
~~~
- `heappush`, `heappop` 함수를 통해 구현

### 74-bytes를 복사하지 않고 다루려면 memoryview와 bytearray를 사용해라
- 파이썬이 CPU 위주의 계산 작업을 추가적인 노력없이 병렬화해줄 수는 없지만, 스루풋이 높은 병렬 I/O를 다양한 방식으로 지원할 수는 있음
- 그럼에도 불구하고 I/O 도구를 잘못 사용해서 파이썬 언어가 I/O 위주의 부하에 대해서도 너무 느리다는 결론으로 이어지기 쉬움
- 기반 데이터를 bytes 인스턴스로 슬라이싱하려면 메모리를 복사해야 하는데, 이 과정이 CPU 시간을 점유한다는 점
~~~python
chunk = video_data[byte_offset:byte_offset+size] #- 메모리를 복사함ㄴ
~~~
- `memoryview`를 사용하면 문제를 해결할 수 있는데, CPython의 고성능 버퍼 프로토콜을 프로그램에 노출시켜줌
- 버퍼 프로토콜은 런타임과 C 확장이 bytes와 같은 객체를 통하지 않고 하부 데이터 버퍼에 접근할 수 있게 해주는 저수준 C API임
- `memoryview` 인스턴스의 가장 좋은 점은 슬라이싱을 하면 데이터를 복사하지 않고 새로운 memoryview 인스턴스를 만들어 준다는 점
~~~python
data = '동해물과 abc 백두산이 마르고 닳도록'.encode('utf8')
view = memoryview(data)
chunk = view[12:19]
print(chunk)
print("크기 : ", chunk.nbytes)
print("뷰의 데이터 :", chunk.tobytes())
print("내부 데이터 :", chunk.obj)

>>>
<memory at 0x7f889fcaf6d0>
크기 :  7
뷰의 데이터 : b' abc \xeb\xb0'
내부 데이터 : b'\xeb\x8f\x99\xed\x95\xb4\xeb\xac\xbc\xea\xb3\xbc abc \xeb\xb0\xb1\xeb\x91\x90\xec\x82\xb0\xec\x9d\xb4 \xeb\xa7\x88\xeb\xa5\xb4\xea\xb3\xa0 \xeb\x8b\xb3\xeb\x8f\x84\xeb\xa1\x9d'
~~~
- 복사가 없는(zero-copy) 연산을 활성화함으로써 memoryview는 Numpy 같은 수치 계산 확장이나 이 예제 프로그램과 같은 I/O 위주 프로그램이 커다란 메모리를 빠르게 처리해야 하는 경우에 성능을 엄청나게 향상 시킬 수 있음
- bytes 인스턴스의 단점 중 하나는 읽기 전용이라 인덱스를 이용해 변경이 불가능한데, 이를 `bytesarray` 타입을 사용해서 해결 가능
- `bytesarray`는 bytes에서 원하는 값을 바꿀 수 있는 가변(mutable) 버전과 같음
~~~python
my_array = bytearray('hello 안녕'.encode('utf-8'))
my_array[0] = 0x79
print(my_array)
~~~
- `bytearray`도 `memoryview`를 통해 감쌀 수 있음. `memoryview`를 슬라이싱해서 객체를 만들고, 이 객체에 데이터를 대입하면 하부의 `bytearray` 버퍼에 데이터가 대입됨
~~~python
my_array = bytearray('row, row, row, your boat'.encode('utf8'))
my_view = memoryview(my_array)
write_view = my_view[3:13]
write_view[:] = b'-10 bytes-'
print(my_array)

>>>
bytearray(b'row-10 bytes-, your boat')
~~~
- `socket.recv_into`나 `RawIOBase.readinto`와 같은 여러 파이썬 라이브러리 메서드가 버퍼 프로토콜을 사용해 데이터를 빠르게 받아드리거나 읽을 수 있음
- 이런 메서드를 사용하면 새로 메모리를 할당하고 데이터를 복사할 필요가 없어짐
~~~Python
video_array = bytearray(video_cache)
write_view = memoryview(video_array)
chunk = write_view[byte_offset: byte_offset + size]

socket.recv_into(chunk)
~~~

### 테스트와 디버깅 
- 파이썬은 컴파일 시점에 정적 검사(static type checking)을 수행하지 않음
- 파이썬 인터프리터가 컴파일 시점에 프로그램이 제대로 작동할 것이라고 확인할 수 있는 요소가 전혀 없음
- 파이썬은 optional하게 type annotation을 지원하며, 이를 활용해 정적 분석을 수행함으로써 여러 가지 오류를 감지 할 수 있음
- 컴파일 시점의 정적 검사는 모든 것을 해결해 주지는 못함. 즉 테스트 코드를 작성하여 충분히 테스트를 해보아야 함
- 다른 언어보다도 파이썬에서 테스트를 통해 코드의 올바름을 검증하는 것이 중요한 것은 사실
- <b>파이썬의 동적 기능을 사용해 프로그램의 동작을 다른 동작으로 오버라이드함으로써 테스트를 구현하고 프로그램이 예상대로 작동하는지 확인 가능</b>

### 75-디버깅 출력에는 repr 문자열을 사용해라
- `print` 함수는 인자로 받은 대상을 사람이 읽을 수 있는 문자열로 표시함  
  예를 들어 기본 문자열을 출력하면 주변에 따옴표를 표시하지 않고 내용을 출력함
~~~python
print('foo 뭐시기')

>>>
foo 뭐시기
~~~
- 다른 대부분의 출력 방식도 마찬가지인데, 문제는 어떤 값을 사람이 읽을 수 있는 형식의 문자열로 바꿔도 이 값의 실제 타입과 구체적인 구성을 명확히 알기 어렵다는 것
- 예를 들어 print의 기본 출력을 사용하면 5라는 수와 '5'라는 문자열 구분이 안됨
- `repr` 내장 함수는 객체의 출력 가능한 표현을 반환하는데, 이는 객체를 가장 명확하게 이해할 수 있는 문자열 표현이어야 함
~~~python
a = '\x07'
print(a)         #- 공백 출력
print(repr(a))   #- '\x07' 출력
~~~
- `repr`이 돌려준 값을 eval 내장 함수에 넘기면 repr에 넘겼던 객체와 같은 객체가 생겨야 함
- `print`를 사용해 디버깅 할 때도 값을 출력하기 전에 repr를 호출해서 다른 경우에도 명확히 차이를 볼 수 있게 만들어야 함
- 클래스 같은 경우 `__repr__` 특별 메서드를 정의해서 인스턴스의 출력 가능한 표현을 원하는 대로 만들 수 있음

### 76-TestCase 하위 클래스를 사용해 프로그램에서 행동 방식을 검증해라
- 파이썬에서 테스트를 작성하는 표준적인 방법은 `unittest` 내장 모듈을 쓰는 것
- 테스트를 정의하려면 `test_utils.py`, `utils_test.py` 둘 중 하나의 이름의 파일을 만들어야 함
- 위의 파일에 원하는 동작이 들어있는 테스트를 추가함
~~~python 
from unittest import TestCase, main
from utils import to_str


class UtilsTestCase(TestCase):
    def test_so_str_bytes(self):
        self.assertEqual('hello', to_str(b'hello'))

    def test_str_to_str(self):
        self.assertEqual('hello', to_str('hello'))

    def test_failing(self):
        self.assertEqual('incorrect', to_str('hello'))

~~~
- <b>테스트는 TestCase의 하위 클래스로 구성됨. 각각의 테스트 케이스는 `test_` 라는 단어로 시작하는 메서드들임</b>
- 어떤 테스트 메서드가 아무런 Exception도 발생시키지 않고 실행이 끝나면 성공한 것으로 간주
- 테스트 중 일부가 실패하더라도 TestCase 하위 클래스는 최초로 문제가 발생한 지점에서 실행 중단을 하지 않음
- 한 테스트만 수행해보고 싶은 경우 `python unils_test.py ClassName.methodName` 으로 실행
- 테스트 메서드 내부에 있는 breakpoint에서 직접 디버거를 호출해 테스트가 실패한 원인을 깊게 파고들 수 있음 
- `assertEqual`은 두 값이 같은지 비교하고, `assertTrue`는 주어진 불린 식이 참인지 검증 
- 이런 메서드들은 테스트가 왜 실패했는지 알려주므로, 모든 입력과 출력을 표시해주므로 파이썬 내장 assert 문보다 더 나음
- 예외가 발생하는지 검증하기 위해 `with` 문 안에서 `contextmanager`로 사용할 수 있는 `assertRaises` 메서드도 있음
~~~python
class UtilErrorTestCase(TestCase):
    def test_to_str_ban(self):
        with self.assertRaises(UnicodeError): #- UnicodeError 발생하는 경우 OK return
            to_str(object())
~~~
- 테스트 코드의 가독성을 위해 testCase 하위 클래스 안에 help function 작성 가능   
  help function 이름이 test로 시작하면 안됨
- help function은 TestCase가 제공하는 assert method를 호출하지 않고, `fail` method를 호출하여 해당 로직이 잘못됐음을 표현
~~~python 
try:
    next(expected_it)
except StopIteration:
    pass
else:
    self.fail('실제보다 예상한 제너레이터가 더 김')
~~~
- 보통 한 모듈 안에 포함된 모든 테스트 함수를 한 `TestCase` 하위 클래스에 정의함
- `TestCase` 클래스가 제공하는 `subTest` 도우미 메서드를 사용하면 한 테스트 메서드 안에 여러 테스트를 정의할 수 있음
- `subTest`를 사용하면 하위 테스트 케이스 중 하나가 실패해도 다른 테스트 케이스를 계속 진행 가능 

### 77-setUp, tearDown, setUpModule, tearDownModule을 사용해 각각의 테스트를 격리해라
- `TestCase` 클래스는 테스트 메서드를 실행하기 전에 테스트 환경을 구축해야 하는 경우가 자주 있는데, 이러한 테스트 과정을 테스트 하네스라고 함
- 테스트 하네스를 구현하려면 `TestCase` 하위 클래스 안에서 `setUp`, `tearDown` 메서드를 오버라이드 해야함
- `setUp`은 테스트 메서드를 실행 전 호출,  `tearDown` 테스트 메서드 실행 후 호출  
  두 메서드 활용시 테스트를 서로 격리된 상태에서 실행할 수 있음
- 예를 들어 테스트를 위해 임시 디렉토리를 생성하고, 테스트 종료 후 지울 수 있음
~~~python
from unittest import TestCase, main
from pathlib import Path
from tempfile import TemporaryDirectory


class EnvironmentTest(TestCase):
    def setUp(self):
        self.test_dir = TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)

    def teardown(self):
        self.test_dir.cleanup()

    def test_modify_name(self):
        with open(self.test_path / 'data_bin', 'w') as f:
            ...
~~~
- 프로그램이 복잡해지면, 코드를 독립적으로 실행하는 대신, 모듈 사이의 end-to-end 상호작용을 검증하는 테스트가 필요할 수도 있음
- 단위 테스트와 통합 테스트는 둘 다 반드시 필요함
- 통합 테스트에 필요한 테스트 환경을 구축할 때 계산 비용이 너무 비싸거나, 너무 오랜 시간 소요될 경우가 있는데 이를 위해 `unittest` 모듈은 모듈 단위의 테스트 하네스 초기화를 지원함  
해당 자원을 단 한번만 초기화하고, 초기화를 반복하지 않고도 testCase의 클래스 내 메서드 테스트가 가능
- 위의 초기화는 `setUpModule`과 `tearDownModule` 메서드를 정의해 동작을 수행함

### 78-목(mock)을 사용해 의존 관계가 복잡한 코드를 테스트해라
- 테스트를 작성할 때 공통 기능으로, 사용하기에 너무 느리거나 어려운 함수와 클래스의 mock을 만들어 사용하는 기능이 있음
- mock은 자신이 흉내내려는 대상에 의존하는 다른 함수들이 어떤 요청을 보내면 어떤 응답을 보내야 할지 알고, 요청에 따라 적절한 응답을 돌려줌
- 파이썬 `unittest.mock` 내장 모듈을 사용하면 `mock`을 만들고 테스트 할 수 있음
- 다음 코드는 DB에 접속하지 않고 `get_animals` 함수를 시뮬레이션 하는 Mock 인스턴스
~~~python
mock = Mock(spec=get_animals)
expected = [
    ('점박이', datetime(2020, 6, 5, 11, 15)),
    ('털보', datetime(2020, 6, 5, 12, 30)),
    ('조조', datetime(2020, 6, 5, 12, 45))
]
mock.return_value = expected
~~~
- `mock`의 `return_value` 애트리뷰트는 mock이 호출되었을 때 반환할 값
- `spec=` 인자는 mock이 흉내 내야하는 대상 
- 다음과 같이 mock 활용 가능
~~~python
database = object()
result = mock(database, '미어캣')
assert result == expected
~~~
- `assert_called_once_with` 라는 메서드를 제공해서 인자가 목에게 제대로 전달했는지 확인
~~~python
mock.assert_called_once_with(database, '미어캣')
mock.assert_called_once_with(database, '기린')   #- AssertionError

from unittest.mock import ANY
mock.assert_called_with(ANY, '미어캣')
~~~
- Mock 클래스에는 예외 발생을 쉽게 모킹할 수 있는 도구도 제공함
~~~python
mock = Mock(spec=get_animals)
mock.side_effect = MyError('에구머니나! 큰 문제 발생')
result = mock(database, '미어캣')
mock.assert_called_with(database, '미어캣')
~~~
- mock을 활용하여 test code 제작시 mock 함수를 주입하는 방법 중 `unittest.mock.patch` 관련 함수들로 mock 주입 가능 
- `patch`를 사용해 `get_animals`를 mock으로 대치 가능  
  다양한 모듈, 클래스, 애트리뷰트에 대해 patch 사용 가능
- `with`문, 데코레이터, `TestCase` 클래스 안의 `setUp`, `tearDown` 메서드에서 사용할 수도 있음
- C 확장 모듈 같은 경우는 변경 불가능
~~~python
from unittest.mock import patch
def get_animals(database, species):
    # 데이터베이스에 질의함
    ...
    # (이름, 급양 시간) 튜플 리스트를 반환함

print('패치 외부  :', get_animals)

with patch('__main__.get_animals'):
    print("패치 내부 :", get_animals)

>>>
패치 외부  : <function get_animals at 0x7ff84e783e60>
패치 내부 : <MagicMock name='get_animals' id='140704445275984'>

#- error
with patch('datetime.datetime.utcnow'):
    datetime.utcnow.return_value = fake_now

#- 다음과 같이 help function을 만들어 적용
def get_do_rounds_time():
    return datetime.utcnow()

with patch('__main__.get_do_rounds_time'):
    ...
~~~
- 테스트가 끝나면 `patch.multiple`을 사용한 with 문 안에서 목 호출이 제대로 이뤄졌는지 검증할 수 있음


### 80-pdb를 사용해 대화형으로 디버깅해라
- 프로그램 개발시 디버깅으로 `print` 함수를 사용하거나, `unittest` 모듈을 사용해서 테스트케이스를 작성하는 것에 추가적으로 파이썬 내장 대화형 디버거를 사용해 볼 수 있음
- 대화형 내장 디버거를 사용하면 프로그램의 상태를 들여다보고, 지역 변수를 출력하고, 파이썬 프로그램을 한 번에 한 문장씩 실행할 수 있음
- 파이썬은 문제를 조사할 위치에 디버거를 초기화 할 수 있도록 `breakpoint()`를 추가하여 디버거 수행
- 프로그램을 시작한 터미널에서는 대화형 파이썬 셀이 시작됨
- 다음은 pdb 프롬포트에서 유용한 함수들
  - `where` : 현재 실행 중인 프로그램 호출 스택 출력
  - `up` : 실행 호출 스택에서 현재 관찰 중인 함수를 호출한 쪽으로 호출 스택을 한 단계 이동
  - `down` : 실행 호출 스택에서 한 수준 아래로 호출 스택 영역 이동
- 다음 다섯가지 디버거 명령을 통해 실행을 다양한 방식으로 제어 가능
  - `step`: 프로그램 다음 줄 실행 후 디버거 실행. 다음 줄에 함수 호출 부분이 있다면, 해당 함수로 들어가 첫 번째 줄에서 디버거 실행
  - `next`: 프로그램 다음 줄 실행 후 디버거 실행. 다음 줄에 함수 호출 부분이 있다면, 해당 함수 실행하고 반환 후 디버거 실행
  - `return`: 현재 함수가 반환될 때까지 프로그램을 계속 실행
  - `continue`: 다음 중단점에 도달할 때까지 프로그램 실행. 중단점에 도달하지 못하면 프로그램 실행이 끝날 때까지 프로그램 실행
  - `quit`: 디버거에서 나가면서 프로그램 중단시킴
- 디버거 시작하는 다른 방법은 사후 디버깅이 있음. 예외가 발생하거나 프로그램 문제 발생시 디버깅 가능
- `$ python3 -m pdb -c continue main.py` 명령어 사용
- 또는 예외 발생시 `import pdb; pdb.pm()` 을 호출하면 사후 디버깅 사용 가능
- 파이썬 기본 구현인 CPython은 메모리 관리를 위해 `reference counting`을 사용
- 어떤 객체를 가리키는 참조가 모두 없어지면 참조된 객체도 메모리에서 삭제되고 메모리 공간을 다른 데이터에 내줄수 있음


### 81- 프로그램이 메모리를 사용하는 방식과 메모리 누수를 이해하기 위해 tracemalloc을 사용해라
- 파이썬 기본 구현인 CPython은 메모리 관리를 위해 <b>reference counting</b>을 사용
- 어떤 객체를 가리키는 참조가 모두 없어지면 참조된 객체도 메모리에서 삭제되고 메모리 공간을 다른 데이터에 내어줄 수 있음
- CPython에는 cycle detector가 들어 있으므로 자기 자신을 참조하는 객체의 메모리도 언젠가는 garbage collection 됨
- 즉 이론적으로는 대부분의 프로그래머가 memory allocation 이나 해제하는 것을 신경쓰지 않아도 됨 
- 하지만 실전에서는 더이상 참조하지 않는 메모리를 계속 유지해 메모리를 소진하게 되는 경우가 있음
- 메모리 사용 디버깅 방법
- `gc` 내장 모듈을 사용해 모든 객체 나열할 수 있음. 문제는 어떻게 할당됐는지 모름
- 파이썬 3.4부터는 이런 문제를 해결해주는 `tracemalloc` 이라는 내장 모듈이 새로 도입


### 82- 커뮤니티에서 만든 모듈을 어디서 찾을 수 있을지 알아두라
- 파이썬 패키지 인덱스(PyPI)에는 풍부한 패키지가 들어가 있음(http://pypi.org)
- `pip`를 사용하면 새로운 모듈을 쉽게 설치할 수 있음
- `python3 pip install pandas`
- 패키지를 지속적으로 추적하고 관리할 수 있게 venv와 같이 쓰는 것이 중요


### 83- 가상 환경을 의존해 의존 관계를 격리하고 반복 생성할 수 있게 해라
- `pip`로 설치한 패키지들은 기본적으로 전역 위치에 저장됨  
  이로 인해 우리 시스템에서 실행되는 모든 파이썬 프로그램이 모듈의 영향을 받게 됨
- 패키지 설치 후 이 패키지가 의존하는 다른 패키지 목록을 볼 수 있음  
  ` python3 -m pip show Sphinx`
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
  '''주어진 함수는 test 용도입니다.'''
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
db = db_connection.Database()

# prod_main.py
TESTING = False

import db_connection
db = db_connection.Database()

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
- 메타 클래스(meta-class)
  - 메타 클래스는 사용하면 class문을 가로채서 클래스가 정의될 때마다 특별한 동작을 제공할 수 있음 
- 제너레이터
  - 함수가 점진적으로 반환하는 값으로 이뤄지는 스트림을 만들어줌
- 오프셋(offset)
  - 두 번째 주소를 만들기 위해 기준이 되는 주소에 더해진 값을 의미 
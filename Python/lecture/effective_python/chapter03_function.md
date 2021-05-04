## Chapter03 - 함수
### 19-함수가 여러 값을 반환하는 경우 절대로 네 값 이상을 언패킹하지 마라
- 언패킹 구문의 한 가지 효과는 언패킹을 사용하면 함수가 둘 이상의 값을 반환할 수 있다는 것
- 다음과 같이 악어 개체군의 대한 여러 통계를 계산하다고 했을 때, 다음과 같이 언패킹을 통해 코드를 구현할 수 있음
~~~python
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    return minimum, maximum


lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]
minimum, maximum = get_stats(lengths)
print(f"최소:{minimum}, 최대:{maximum}")
~~~
- 여러 값을 한꺼번에 처리하는 별표 식을 사용해 여러 값을 반환받을 수도 있음
- 예를 들어 각 악어 개체의 몸 길이가 전체 개체군의 몸 길이 평균에 비해 얼마나 큰지 계산하는 다른 함수가 필요하다고 하자
~~~python
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    return minimum, maximum


lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]
minimum, maximum = get_stats(lengths)
print(f"최소:{minimum}, 최대:{maximum}")


def get_avg_ratio(numbers):
    average = sum(numbers) / len(numbers)
    scaled = [x / average for x in numbers]
    scaled.sort(reverse=True)
    return scaled


longest, * middle, shortest = get_avg_ratio(lengths)
print(f"최대 길이: {longest:>4.0%}")
print(f"최소 길이: {shortest:>4.0%}")
~~~
- 만약 다음과 같이 몸 길이의 평균, 중앙값, 악어 개체군의 개체 수까지 요구하는 것으로 바뀌었다고 해서 함수를 다음과 같이 수정했다고 하자
~~~python
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    count = len(numbers)
    average = sum(numbers) / count

    sorted_numbers = sorted(numbers)
    middle = count // 2
    if count % 2 == 0:
        lower = sorted_numbers[middle - 1]
        upper = sorted_numbers[middle]
        median = (lower + upper) / 2
    else:
        median = sorted_numbers[middle]

    return minimum, maximum, average, median, count

lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]
minimum, maximum, average, median, count = get_stats(lengths)
~~~
- 이 코드에는 두 가지 문제가 있다
  - 모든 반환 값이 수(number)이기 때문에 순서를 혼동하기 쉬움
  - 함수를 호출하는 부분과 반환 값을 언패킹 하는 부분이 길어 가독성이 나빠짐
- 즉 4개 이상의 언패킹 구문은 사용하지 말자. 이 보다 더 많은 값을 언패킹 해야 한다면 light class나 namedtuple을 사용하고 함수도 이런 값을 반환하게 만드는 것이 낫다

### 20-None을 반환하기보다는 예외를 발생시켜라
- 다음과 같이 None을 발생시키면 반환 값을 잘못 해석하는 경우가 발생할 수 있다
~~~python
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

x, y = 1, 0
result = careful_divide(x, y)
if not result:
    print('잘못된 입력')
~~~
- 즉 None이라는 값은 반드시 false 를 return 하여 다음과 같이 코드문을 작성했지만, 0인 경우에도 if 로직에서 0을 만들어 내므로, 실수를 발생시켰다
- 첫 번째 해결방안은 반환 값을 2-튜플로 분리하는 것이다
~~~python
def careful_divide(a, b):
    try:
        return True, a/b
    except ZeroDivisionError:
        return False, None

success, result = careful_divide(10, 0)
if not success:
    print('잘못된 입력')
~~~
- 하지만 위의 코드도 결국 `success`를 잘못 입력받는다면 문제가 발생할 여지가 충분하다
- 더 좋은 방법은 None을 반환하지 않고 Exception을 호출한 쪽으로 발생시켜서 호출자가 이를 처리하게 하는 것이다
- 다음 코드에서 `ZeroDivisionError`가 발생한 경우 이를 `ValueError`로 바꿔 던져 입력 값이 잘못됨을 알린다
~~~python
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('잘못된 입력')

x,y = 5, 2
try:
    result = careful_divide(x, y)
except ValueError:
    print("잘못된 입력")
else:
    print('결과는 %.1f 입니다.' % result)

>>>
결과는 2.5입니다.
~~~
- 이 접근 방법을 확장해서 타입 애너테이션을 사용하는 코드에도 적용할 수 있음
- 함수의 반환값이 항상 float이라고 지정할 수 있고, 그에 따라 None이 결코 반환되지 않음을 알릴 수 있음
~~~python
def careful_divide(a: float, b: float) -> float:
    """a를 b로 나눈다
    Raises:
        ValueError: b가 0이어서 나눗셈을 할 수 없을 때
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('잘못된 입력')
~~~

### 21-변수 영역과 클로저의 상호작용 방식을 이해해라
- 숫자로 이루어진 list를 정렬하는데, 정렬한 리스트의 앞쪽에는 우선순위를 부여한 몇몇 숫자를 위치시켜야 한다고 가정하자
- 이 패턴은 사용자 인터페이스를 표시하면서 중요한 메세지나 예외적인 이벤트를 다른 것보다 우선해 표시하고 싶을 때 사용
- 이 경우 해결하는 일반적인 방법은 `sort` 메서드에 `key` 인자로 help function을 전달하는 것 
~~~python
def sort_priority(values, group):
    def helper(x):
        if x in group:
            return 0, x
        else:
            return 1, x
    values.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = [2, 3, 5, 7]
sort_priority(numbers, group)
print(numbers)

>>>
[2, 3, 5, 7, 1, 4, 6, 8]
~~~
- 이 함수가 예상대로 작동하는 세 가지 이유가 있음
  - 파이썬이 클로저(closure)를 지원: 클로저란 자신이 정의된 영역 밖의 변수를 참조하는 함수. 클로저로 인해 도우미 함수가 sort_priority 함수의 group 인자에 접근할 수 있음
  - 파이썬에서 함수는 first-class citizen 객체임: 이로 인해 sort 함수에서 클로저 함수를 key 인자로 전달 가능
  - 파이썬에서는 시퀀스(튜플 포함)를 비교하는 구체적인 규칙 존재: 시퀀스를 비교할 때 0번 인덱스에 있는 값을 비교한 다음, 이 값이 같으면 1번 인덱스에 있는 값을 비교함. 이로 인해 helper 클로저가 반환하는 튜플이 서로 다른 두 그룹을 정렬하는 기준 역할을 할 수 있음
  - 이미 알고 있겠지만, 다음의 코드는 `found`가 False가 return 됨을 꼭 기억하자
~~~python
def sort_priority(numbers, group):
    found = False
    def helper(x):
        if x in group:
            found = True
            return 0, x
        else:
            return 1, x

    numbers.sort(key=helper)
    return found


numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = [2, 3, 5, 7]
found = sort_priority(numbers, group)
print(numbers)
print("발견 : ", found)

>>>
[2, 3, 5, 7, 1, 4, 6, 8]
발견 :  False
~~~
- 정렬 결과는 맞지만, found가 True여야 하는데 False다. 왜 그럴까? 
- <b>식 안에서 변수를 참조할 때 파이썬 인터프리터는 이 참조를 해결해기 위하여 다음 순서로 영역을 뒤진다</b>
  - 현재 함수의 영역
  - 현재 함수를 둘러싼 영역(nonlocal)
  - 현재 코드가 들어있는 모듈의 영역(global scope)
  - 내장 영역(built-in scope), len, str 등이 함수가 들어있는 영역
- 해당 영역에 전부 없으면, NameError를 발생시킨다
- 중요한 것은 읽기는 다음과 같은 영역의 순서로 참조하는데, 쓰기(대입)는 변수가 현재 그 영역에 정의돼 있다면 변수의 값만 바뀌고, 없다면 새로운 변수를 정의함
- 즉 helper 함수 내에서 정의된 found 함수는 새로운 변수로 정의되는 것이다
- 이 문제는 영역 지정 버그(scoping bug)라고 부르기도 함. 하지만 이것은 내부 영역의 변수가 전역 변수의 영역에 쓰레기 변수를 생성하는 것을 막고, 확실한 영역을 정하게 하므로써 버그를 막음
- 실제 위의 코드문을 정상적으로 실행시키려면 `nonlocal`이라는 명령어를 선언해주면 됨
~~~python
def sort_priority(numbers, group):
    found = False
    def helper(x):
        if x in group:
            nonlocal found
            found = True
            return 0, x
        else:
            return 1, x

    numbers.sort(key=helper)
    return found


numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = [2, 3, 5, 7]
found = sort_priority(numbers, group)
print(numbers)
print("발견 : ", found)
~~~
- <b>하지만 왠만하면 nonlocal 구문은 사용하지 말자. 코드가 길어질수록 알아보기 힘들고, 함수 동작을 더 이해하기 힘들게 만든다</b>
- 다음과 같이 위의 결과와 같은 결과를 만들어내는 클래스를 정의해서 사용하자
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


numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = [2, 3, 5, 7]
sorter = Sorter(group)
numbers.sort(key=sorter)
print(numbers)
~~~
#### 기억해야 할 내용
- 클로저 함수는 자신이 정의된 영역 외부에서 정의된 변수도 참조할 수 있음
- 기본적으로 클로저 내부에 사용한 대입문은 클로저를 감싸는 영역에 영향을 끼칠 수 없음
- 클로저가 자신을 감싸는 영역의 변수를 변경한다는 사실을 표시할 때는 `nonlocal` 문을 사용해라
- 간단한 함수가 아닌 경우에는 nonlocal 문을 사용하지 마라
- 변수를 선언하는 것과, list 등의 자료형을 nonlocal에 선언하고 참조하는 것은 다른 것임을 인식하자

### 22-변수 위치 인자를 사용해 시각적인 잡음을 줄이자 
- 위치 인자(positional argument)를 가변적으로 받을 수 있으면 함수 호출이 더 깔끔해지고 시각적 잡음도 줄어듬  
  이런 위치 기반의 인자를 가변 인자(varargs)나 스타 인자(star args)라고 부르기도 함
- 스타 인자는 이름을 관례적으로 가변 인자의 이름을 *args라고 붙이는 것에서 유래됨
- 예를 들어 다음과 같이 디버깅 정보를 로그에 남기고 싶다고 할 떄, 인자 수가 고정되어 있으면 메세지와 값의 list를 받는 함수가 필요
~~~python
def log(message, values):
    if not values:
        print(message)
    else:
        values_str = '.'.join(str(x) for x in values)
        print(f"{message} : {values_str}")

log('내 숫자는', [1, 2])
log('안녕', [])
~~~
- 로그에 남길 값이 없을 때도 빈 리스트를 넘겨야 한다면 귀찮을 뿐 아니라 코드 잡음도 많음
- 마지막 인자 앞에 *를 붙이면 됨. 로그 메세지의 첫 번째 파라미터는 반드시 필요하지만, 그 이후의 모든 위치 인자는 선택사항
- 가변 인자를 써도 함수 본문은 바뀌지 않음. 단지 호출하는 인자만 바뀜
~~~python
def log(message, *values):  #- 달라진 유일한 부분
    if not values:
        print(message)
    else:
        values_str = '.'.join(str(x) for x in values)
        print(f"{message} : {values_str}")

log('내 숫자는', 1, 2)
log('안녕') #- 훨씬 좋음
~~~
- 이미 시퀀스가 있는데 가변 인자 함수에 시퀀스를 사용하고 싶으면 *연산자를 사용하면 된다
- `*` 연산자는 파이썬이 시퀀스의 원소들을 함수의 위치 인자로 넘길 것을 명령
~~~python
log('좋아하는 숫자는', *favorites)
favorites = [7, 33, 99]

>>>
좋아하는 숫자는 : 7,33,99
~~~
- 가변적인 위치 인자를 받는 데는 두 가지 문제점이 있다
- 위치 인자가 함수로 전달되기 전에 항상 튜플로 변환됨. 이는 함수를 호출하는 쪽에서 제너레이터 앞에 * 연산자를 사용하면 제너레이터의 모든 원소를 얻기 위해 반복한다는 뜻
- 이렇게 만들어지는 튜플은 제너레이터가 만들어낸 모든 값을 포함하며, 이로 인해 메모리를 아주 많이 소비하거나 프로그램이 중단돼버릴 수 있음
~~~python
def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

it = my_generator()
my_func(*it)
~~~
- args를 받는 함수는 인자 목록에서 가변적인 부분에 들어가는 인자의 개수가 처리하기 좋을 정도로 충분히 작다는 사실을 이미 알고 있는 경우에 적합
- *args의 두 번째 문제점은 함수에 새로운 위치 인자를 추가하면 해당 함수를 호출하는 모든 코드를 변경해야만 한다는 것
~~~python
def log(sequence, message, *values):
    if not values:
        print(f'{sequence} - {message}')
    else:
        values_str = ','.join(str(x) for x in values)
        print(f"{sequence} - {message}: {values_str}")

log(1, '좋아하는 숫자는', 7, 33)
log(1, '안녕')
log('좋아하는 숫자는', 7, 33)
~~~
- 위의 버그를 발생시키지 않으려면 *args를 받아들이는 함수를 확장할 때는 키워드 기반의 인자만 사용해야 함

### 23-키워드 인자로 선택적인 기능을 제공해라
~~~python
def remainder(number, divisor):
    return number % divisor

assert remainder(20, 7) == 6  #- 위치에 따라 인자를 넘길 수 있음


remainder(20, 7)
remainder(20, divisor=7)
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)
remainder(number=20, 7)          #- 위치 기반 인자를 지정하려면 키워드 인자보다 앞에 지정해야 함
remainder(20, number=7)          #- 각 인자는 한 번만 지정해야 함
~~~
~~~python
my_kwargs ={
    'number':20,
    'divisor':7,
}
assert remainder(**my_kwargs) == 6 #- 딕셔너리 내용물을 ** 연산자를 사용할 수 있음

my_kwargs = {
'divisor': 7,
}
assert remainder(number=20, **my_kwargs) == 6

my_kwargs = {
    'number': 20,
}

other_kwargs = {
    'divisor': 7,
}

assert remainder(**my_kwargs, **other_kwargs) == 6
~~~
~~~python
#- 모든 키워드 인자를 dict에 모아주는 **kwargs라는 파라미터 사용
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

print_parameters(alpha=1.5, beta=9, 감마=4)
~~~
- 키워드 인자가 제공하는 유연성을 활용하면 3가지 이점 존재
- 첫 번쨰: 키워드 인자를 사용하면 코드를 처음 보는 사람들에게 호출의 의미를 명확히 알려줄 수 있음
- 두 번쨰: 키워드 인자의 경우, 디폴트 값을 지정할 수 있음
- 다음의 코드를 비교하면 디폴트 값을 지정함으로써 잡음을 줄일 수 있음을 확인 가능
~~~python
def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

#- 위의 식에서 측정 값을 한 시간이나, 하루 단위의 유입량을 추정하고 싶을 때,
#- 다음과 같이 default 연산자를 추가하여 손쉽게 수정 가능
def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period
~~~
- 세 번째: 어떤 함수를 사용하던 기존 호출자에게는 하위 호환성을 제공하면서 함수 파라미터를 확장할 수 있는 방법을 제공
- 즉, 별도의 코드 마이그레이션을 하지 않아도, 기능을 추가할 수 있음
- 앞에서 본 `flow_rate` 함수를 확장해 킬로그램이 아닌 무게 단위를 이용해 시간당 유입량을 계산하고 싶다고 하자
~~~python
def flow_rate(weight_diff, time_diff, period=1, units_per_kg = 1):
    return ((weight_diff * units_per_kg) / time_diff) * period

#- 기존의 함수 수정 없이 코드 구현이 가능하다는 것!
pounds_per_hour = flow_rate(weight_diff, time_diff, period=3600, units_per_kg=2.2)
~~~
#### 기억해야 할 내용
- 함수 인자를 위치에 따라 지정할 수도 있고, 키워드를 사용해 지정할 수도 있음
- 키워드를 사용하면 위치 인자만 사용할 때는 혼동할 수 있는 여러 인자의 목적을 명확히 할 수 있음
- 키워드 인자에 디폴트 값을 함께 사용하면 기본 호출 코드를 마이그레이션하지 않고도 함수에 새로운 기능을 쉽게 추가할 수 있음
- 선택적 키워드 인자는 항상 위치가 아니라 키워드를 사용해 전달해야 함

### 24-None과 docstring을 사용해 동적인 디폴트 인자를 지정해라
- 종종 키워드 인자 값으로 정적으로 정해지지 않는 타입의 값을 써야 할 때가 있음
- 예를 들어 로그 메세지와 시간을 함께 출력하고 싶다고 하자. 기본적으로 함수 호출 시간을 포함하길 원함
- 함수가 호출될 때마다 디폴트 인자가 재계산된다고 가정하면 다음과 같은 접근 방법을 사용할 수 있음
~~~python
from time import sleep
from datetime import datetime


def log(message, when=datetime.now()):
    print(f"{when}: {message}")

log("안녕!")
sleep(0.1)
log("다시 안녕!")
~~~
- <b>하지만 디폴트 인자는 이런 식으로 작동하지 않음. 함수가 정의되는 시점에 datetime.now가 단 한 번만 호출됨</b>
- 따라서 timestamp가 항상 같음. 디폴트 인자의 값은 모듈이 로드(load)될 때 단 한번만 평가되는데, 보통 프로그램이 시작할 때 모듈을 로드하는 경우가 많음
- 디폴트 값을 계산하는 코드가 들어 있는 모듈이 로드된 다음 다시 `datetime.now()` 디폴트 인자가 평가되지는 않음
- 이를 해결하는 방법은 <b>디폴트로 None을 지정하고 실제 동작을 docstring에 문서화 하는 것</b>
~~~python
def log(message, when=None):
    """메세지와 타임스탬프를 로그에 남김

    Args:
        message: 출력할 메세지
        when: 메세지가 발생한 시각(datetime),
          디폴트 값은 현재 시간,
    """
    if when is None:
        when = datetime.now()
    print(f"{when} : {message}")

#- 이제는 타임스탬프가 달라짐
log("안녕!")
sleep(0.1)
log("다시 안녕!")

>>>
2021-05-04 00:22:39.700729 : 안녕!
2021-05-04 00:22:39.801721 : 다시 안녕!
~~~
- <b>디폴트 인자 값으로 None을 사용하는 것은 인자가 mutable인 경우 특히 중요</b>
- 예를 들어 JSON으로 인코딩된 값을 얻으려고 하는데, 데이터 디코딩에 실패하면 디폴트로 빈 딕셔너리를 반환하고 싶음
~~~python
import json

def decode(data, default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default


foo = decode('잘못된 데이터')
foo['stuff'] = 5
boo = decode('잘못된 데이터')
boo['hello'] = 10

print('foo :', foo)
print('boo :', boo)

>>>
foo : {'stuff': 5, 'hello': 10}
boo : {'stuff': 5, 'hello': 10}

assert foo is boo 
~~~
- 위의 결과의 원인은 foo와 bar가 모두 default 파라미터와 같기 때문. 둘은 모두 동일한 딕셔너리 객체임
- 이 해법도 마찬가지로 키워드 인자의 디폴트 값으로 None을 지정하고, 함수의 독스트링에 동작 방식을 기술하는 것
~~~python
import json


def decode(data, default=None):
    """문자열로부터 JSON 데이터를 읽어온다

    Args:
        data: 디코딩할 JSON 데이터
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}
            return default

foo = decode("잘못된 데이터")
foo['stuff'] = 1
boo = decode('또 잘못된 데이터')
boo['hello'] = 5

print("foo :", foo)
print("boo :", boo)
~~~
- 이 접근 방법은 타입 애너테이션을 사용해도 잘 작동함
- 다음 코드에서 `when` 인자에는 datetime인 Optional 값이라는 타입 애너테이션이 붙어 있음
- 따라서 when에 사용할 수 있는 두 값은 None과 datetime 개체 뿐
~~~python
from typing import Optional
from datetime import datetime


def log_typed(message: str, when: Optional[datetime]=None) -> None:
    """메세지와 타입 스탬프를 남김

    Args:
        message: 출력할 메세지
        when: 메세지가 발생한 시각(datetime)
            디폴트 값은 현재 시각
    """
    if when is None:
        when = datetime.now()
    print(f"{when}: {message}")
~~~
#### 기억해야 할 내용
- 디폴트 인자 값은 그 인자가 포함된 함수 정의가 속한 모듈이 로드되는 시점에 한번만 평가됨. 이로 인해 동적인 값의 경우 이상한 동작이 일어날 수 있음
- 동적인 값을 가질 수 있는 키워드 인자의 디폴트 값을 표현할 때는 None을 사용  
  그리고 함수의 독스트링에 실제 동적인 디폴트 인자가 어떻게 동작하는지 문서화 해두자
- 타입 애너테이션을 사용할 때도 None을 사용해 키워드 인자의 디폴트 값을 표현하는 방식을 적용할 수 있음

### 26-functions.wrap을 사용해 함수 데코레이터를 정의해라
- 파이썬은 함수에 적용할 수 있는 데코레이터(decorator)를 정의하느 특수한 구문을 제공함
- 데코레이터는 자신이 감싸고 있는 함수가 호출되기 전과 후에 코드를 추가로 실행해 줌
- 또한 자신이 감싸고 있는 함수의 입력 인자, 반환 값, 함수에서 발생한 오류에 접근할 수 있다는 뜻
- 함수의 의미를 강화하거나 디버깅을 하거나 함수를 등록하는 등의 일에 이런 기능을 유용하게 쓸 수 있음
- 예를 들어 함수가 호출될 때마다 인자 값과 반환 값을 출력하고 싶다고 하자  
  이런 기능은 재귀적 함수에서 함수 호출이 재귀적으로 내포되는 경우를 디버깅할 때 특히 유용
~~~python
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args!r})"
              f"-> {result!r}")
        return result
    return wrapper

@trace
def fibonacci(n):
    """n번쨰 피보나치 수를 반환한다."""
    if n in (0, 1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))
~~~
- @ 기호를 사용하는 것은 이 함수에 대해 데코레이터를 호출한 후, 데코레이터가 반환한 결과를 원래 함수가 속해야 하는 영역에 원래 함수와 같은 이름으로 등록하는 것과 같음
~~~python
fibinacci = trace(fibinacci)
~~~
- 해당 코드의 문제점은 데코레이터가 반환하는 함수의 이름이 fibonacci가 아니게 됨
~~~python
print(fibonacci)

>>>
<function trace.<locals>.wrapper at 0x7fcf2a24a200>
~~~
- 이러한 결과가 나오는 이유는 trace 함수는 자신의 본문에 정의된 wrapper 함수를 반환함
- 데코레이터로 인해 이 wrapper 함수가 모듈에 fibonacci라는 이름으로 등록되는데, 이런 동작은 디버거와 같이 인트로스펙션을 하는 도구에서 문제가 됨
- 예를 들어 꾸며진 fibonacci 함수에 help 내장 함수를 호출하면 쓸모가 없음  
  다음과 같이 호출하면 fibonacci 함수의 맨 앞부분에 있는 docstring이 출력되어야 하지만, 실제로는 그렇지 않음
~~~python
help(fibonacci)

>>>
Help on function wrapper in module __main__:
wrapper(*args, **kwargs)
~~~
- 데코레이터가 감싸고 있는 원래 함수의 위치를 찾을 수 없기 때문에 객체 직렬화도 깨짐
~~~python
import pickle
pickle.dumps(fibonacci)

>>>
AttributeError: Can't pickle local object 'trace.<locals>.wrapper'
~~~
- 문제를 해결하는 방법은 `functools` 내장 모듈에 정의된 `wraps` 도우미 함수를 사용하는 것
- 이 함수는 데코레이터 작성을 돕는 데코레이터
- wraps를 wrapper 함수에 적용하면 wraps가 데코레이터 내부에 들어가는 함수에서 중요한 메타데이터를 복사해 wrapper 함수에 적용해줌
~~~python
from functools import wraps


def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({kwargs!r})"
              f"-> {result!r}")
        return result
    return wrapper

@trace
def fibonacci(n):
    """n번쨰 피보나치 수를 반환한다."""
    if n in (0, 1):
        return n
    return (fibonacci(n-2) + fibonacci(n-1))

fibonacci = trace(fibonacci)
print(fibonacci)

>>>
<function fibonacci at 0x7fcf2a229830>
~~~
- 파이썬 함수에는 이 예제에서 살펴본 것보다 더 많은 표준 애트리뷰트가 있음(`__name__`, `__module__`, `__annotations__`). 파이썬 언어에서 함수의 인터페이스를 처리하려면 이런 애프리뷰트도 보존돼야 함
- wraps을 사용하면 이 모든 애트리뷰트를 제대로 복사해서 함수가 제대로 작동하도록 해줌

### 기억해야 할 내용
- 파이썬 데코레이터는 실행 시점에 함수가 다른 함수를 변경할 수 있게 해주는 구문
- 데코레이터를 사용하면 디버거 등 인트로스펙션을 사용하는 도구가 잘못 작동할 수 있음
- 직접 데코레이터를 구현할 때 인트로스펙션에서 문제가 생기지 않길 바란다면 wraps 데코레이터 사용하기



### 용어 정리
- 인트로스펙션(introspection)
  - 특정 클래스가 어떤 클래스로부터 파생되었는지, 혹은 어떤 함수가 구현되어 있는지, 객체에는 어떤 속성이 있는지에 대한 상세한 정보를 런타임에 얻거나 조작하는 기술 
  - 이러한 인트로스펙션 덕분에 Python은 실행 시점에 프로그램의 내부 속성 정보를 조작할 수 있다고 함
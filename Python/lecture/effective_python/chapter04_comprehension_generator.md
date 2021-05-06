## chapter04 컴프리헨션과 제너레이터
- 컴프리헨션 코딩 스타일은 제너레이터를 사용하는 함수로 확장할 수 있음
- 제너레이터는 함수가 점진적으로 반환하는 값으로 이뤄지는 스트림을 만들어줌

### 27-map과 filter 대신 컴프리핸션을 사용해라
- map 내장 함수보다 리스트 컴프리헨션이 더 명확함
- lambda 함수는 시각적으로 그렇게 좋지 않음
~~~python
[x ** 2 for x in range(10)]            #- 더 명확함
list(map(lambda x: x**2, range(10)))

[x ** 2 for x in range(10) if x % 2 == 0]
list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(10))))
~~~

#### 기억해야 할 내용
- 리스트 컴프리헨션은 lambda 식을 사용하지 않기 때문에 같은 일을 하는 map과 filter 내장 함수를 사용하는 것보다 더 명확함
- 딕셔너리와 집합도 컴프리헨션으로 생성 가능

### 28-컴프리헨션 내부에 제어 하위 식을 세 개 이상 사용하지 말라
- 컴프리헨션은 여러 수준의 루프를 지원하며, 각 수준마다 여러 조건을 지원
- 제어 하위 식이 세개 이상인 컴프리헨션은 가능하면 피하고, 도우미 함수를 작성하자

### 29-대입식을 사용해 컴프리헨션 안에서 반복 작업을 피하자
~~~python
stock = {
    '못': 125,
    '나사못': 35,
    '나비너트': 8,
    '와셔': 24
}

order = ['나사못', '나비너트', '클립 ']


def get_batches(count ,size):
    return count // size

result = {}
for name in order:
    count = stock.get(name, 0)
    batches = get_batches(count, 8)
    if batches:
        result[name] = batches

print(result)

#- 컴프리헨션을 사용해 불필요한 시각적 잡음을 제거
found = {name: get_batches(stock.get(name, 0), 8)
            for name in order
                if get_batches(stock.get(name, 0), 8)}
print(found)
~~~
- 컴프리헨션 식의 문제는 `get_batches(stock.get(name, 0), 8)`이 반복된다는 단점이 있음
- 8 -> 4로 입력하는 등의 실수가 있을 수 있음
- 이러한 문제를 해결하기 위한 방법으로 3.8에서 도입된 왈러스 연산자를 사용하는 것
~~~python
found = {name: batches
            for name in order
            if (batches := get_batches(stock.get(name, 0), 8))}
~~~
- 해당 코드는 왈러스 연산자를 사용하여 stock 딕셔너리에 한번만 접근하게 됨
- 대입식을 컴프리헨션의 "값 식"에 사용해도 문법적으로는 올바른데, 문제는 다른 부분에서 변수를 읽으려고 하면 평가되는 순서 때문에 실행시점에 오류 발생
~~~python
result = {name: (tenth := count // 10)
            for name, count in stock.items() if tenth > 0}
~~~
- 이 문제를 해결하려면 대입식을 조건식으로 옮기고 대입식에서 만들어진 변수 이름을 컴프리헨션의 값 식에서 참조하면 해결 가능
~~~python
result = {name: tenth
            for name, count in stock.items() if ((tenth := count // 10) > 0)}
~~~
- <b>컴프리헨션 값 부분에서 왈러스 연산자를 사용할 때 그 값에 대한 조건 부분이 없다면  
  루프 밖 영역으로 루프 변수가 누출됨!</b>
~~~python
half = [(last := count // 2) for count in stock.values()]
print(f"{half}의 마지막 원소는{last}")
~~~
- 이러한 누출은 일반적인 for 루프에서 발생하는 루프 변수 누출과 비슷함
~~~python
for count in stock.values():
    pass
print(f"{count}")

>>>
24
~~~
- <b>중요한 것은 컴프리헨션에서는 누출이 일어나지 않는다</b>
~~~python
[count for count in stock.values()]
print(f"{count}") 
~~~

#### 기억해야 할 내용
- 대입식을 통해 컴프리헨션이나 제너레이터 식의 조건 부분에서 사용한 값을 컴프리헨션이나 제너레이터의 다른 위치에서 재 사용가능
- 조건이 아닌 부분에도 대입식을 사용할 수 있지만, 그런 형태의 사용은 피해야 함

### 30- 리스트를 반환하기 보다는 제너레이터를 사용해라
- 제너레이터를 사용하면 리스트 반환에 비해 가독성을 개선할 수 있음
- <b>제너레이터는 yield 식을 사용하는 함수에 의해 만들어짐</b>
- 다음의 코드는 제너레이터 함수를 정의한 코드
~~~python
address = "컴퓨터(영어: Computer, 문화어: 콤퓨터, 순화어: 전산기)는 진공관"
def index_words_iter(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1


it = index_words_iter(address)
print(next(it))
print(next(it))

>>>
0
8
~~~
- 제너레이터가 반환하는 이터레이터에 상태가 있기 때문에 호출하는 쪽에서 재사용이 불가능

### 기억해야 할 내용
- 제너레이터를 사용하면 결과를 리스트에 합쳐서 반환하는 것 보다 더 깔끔
- 제너레이터가 반환하는 이터레이터는 제너레이터 함수의 본문에서 yield가 반환하는 값들로 이뤄진 집합을 만들어냄
- 제너레이터를 사용하면 작업 메모리에 모든 입력과 출력을 저장할 필요가 없으므로 입력이 아주 커도 출력 시퀀스를 만들 수 있음 

### 31- 인자에 대해 이터레이션할 때는 방어적이 돼라
- 객체가 원소로 들어있는 리스트를 함수가 파라미터로 받았을 때, 이 리스트를 여러 번 이터레이션 하는 것이 중요할 때가 종종 있음
- 다음의 코드는 미국 텍사스 주의 여행자 수를 분석하는데, 데이터가 도시별 방문자 수라고 가정하자
- 이 때 각 도시가 전체 여행자 수 중에서 차지하는 비율을 계산하고 싶음
~~~python
def america_travel_normalize(num_list):
    total = sum(num_list)
    result = []
    for num in num_list:
        result.append(100 * num / total)
    return result

#- 다음과 같이 잘 작동함
visits = [15, 35, 80]
percentages = america_travel_normalize(visits)
print(percentages)
print(sum(percentages))

>>>
[11.538461538461538, 26.923076923076923, 61.53846153846154]
100.0
~~~
- 만약 위의 코드의 규모의 확장성 고려시, 리스트가 아닌 제너레이터를 정의
~~~python
def read_visits(file_path):
    with open(file_path) as f:
        for line in f:
            yield int(line)

it = read_visits('test.txt')
print(next(it))
print(next(it))
~~~
- 위의 제너레이터를 활용하여 `america_travel_normalize` 함수를 수행하면 결과는 아무것도 나오지 않는다
~~~python
percentages = america_travel_normalize(it)
print(percentages)

>>>
[]
~~~
- 이런 결과가 나온 이유는 이터레이터가 결과를 한 번만 만들어내기 때문
- 이미 StopIteration 예외가 발생한 이터레이터나 제너레이터를 다시 이터레이션하면 아무 결과도 얻을 수 없음
- <b>중요한 것은, 이미 소진된 이터레이터에 대해 이터레이션을 수행해도 아무런 오류가 발생하지 않음</b>
- for루프, 리스트 생성자, 그 외 파이썬 표준 라이브러리에 있는 많은 함수가 일반적인 연산 도중에 StopIteration 예외가 던져지는 것을 가정함
- 이런 함수들은 출력이 없는 이터레이터와 이미 소진돼버린 이터레이터를 구분할 수 없음
- 이런 문제를 해결하기 위하여 이터레이터를 소진시키면서 이터레이터의 전체 내용을 리스트에 넣을 수 있음
~~~python
it = read_visits('test.txt')
percentages = america_travel_normalize_copy(it)
print(percentages)
assert sum(percentages) == 100
~~~
- 사실 이 방법은 read_visits를 제너레이터로 바꿔 쓰기로 결정했던 근본적인 이유인 규모 확장성 문제와 같음
- 따라서 다른 호출 방법은 호출될 때 마다 새로운 이터레이터를 반환하는 함수를 만드는 것
~~~python
#- 방법1 -> 새로운 제너레이터를 항상 생성 -> get_iter function 전달
def normalize_func(get_iter):
    total = sum(get_iter())
    result = []
    for value in get_iter():
        percent = 100 * value / total
        result.append(percent)
    return result

def get_iter():
    return read_visits('test.txt')

percentages = normalize_func(get_iter)

#- 방법2 -> lambda 함수를 사용하여 전달도 가능
percentages = normalize_func(lambda: read_visits('test.txt'))
~~~
- 위의 코드는 정상적으로 작동하긴 하지만, 람다 함수를 이런식으로 넘기는 것은 보기에 좋지 않음
- <b>더 나은 방법은 이터레이터 프로토콜(protocol)을 구현한 새로운 컨테이너 클래스를 제공 하는 것</b>

#### 이터레이터 프로토콜(iterator protocol)
- iterator: 순차적으로 다음 데이터를 리턴할 수 있는 객체
- iterable: 이터레이터를 리턴할 수 있는 객체 ex) list, string..
- 파이썬의 for 루프나 그의 연관된 식들이 컨테이너 타입의 내용을 방문할 때 사용하는 절차
- `for x in foo`라고 하는 구문을 사용하면 내부적으로는 `iter(foo)`를 호출함
- `iter` 내장 함수는 foo.__iter__라는 특별 메서드를 호출
- `__iter__` 메서드는 반드시 이터레이터 객체를 반환해야 함
- for 루프는 반환받은 이터레이터 객체가 데이터를 소진할 때까지 반복적으로 이터레이터 객체에 대해 next 내장 함수를 호출
- 즉 실제 코드를 작성할 때 우리가 정의하는 클래스에서 `__iter__` 메서드를 제너레이터로 구현하기만 하면 모든 동작을 만족 시킬 수 있음
~~~python
class ReadVisits:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

visits = ReadVisits('test.txt')
percentages = america_travel_normalize(visits)
print(percentages)
print(sum(percentages))
~~~
- 이 코드가 잘 작동하는 이유는 normalize 함수 안의 sum 메서드가 `ReadVisits.__iter__`를 호출해서 새로운 이터레이터 객체를 할당하기 때문
- 각 숫자를 정규화하기 위한 for 루프도 `__iter__` 를 호출해서 두 번째 이터레이터 객체를 만듬
- 두 이터레이터는 서로 독립적으로 진행되고 소진됨. 이로 인해 두 이터레이터는 모든 입력 데이터 값을 볼 수 있는 별도의 이터레이션을 만들어냄. 이 접근 방법의 유일한 단점은 입력 데이터를 여러 번 읽는다는 것
- <b>프로토콜에 따르면 이터레이터가 iter 내장 함수에 전달되는 경우에는 전달받은 이터레이터가 그대로 반환됨</b>
- 반대로 컨테이너 타입이 iter에 전달되면 매번 새로운 이터레이터 객체가 반환됨
- 따라서 입력값이 이런 동작을 하는지 검사해서 반복적으로 이터레이션할 수 없는 인자인 경우에는 TypeError를 발생시켜 인자를 거부할 수 있음 
~~~python
#- 방법1 
#- iterator가 iter 내장함수에 전달되는 경우는 전달받은 이터레이터가 그대로 반환
#- 컨테이너 타입이 iter에 전달되면 새로운 iterator가 반환됨을 이용
def normalize_defensive(numbers):
    if iter(numbers) is numbers:
        raise TypeError("컨테이너를 제공해야 합니다.")
    total = sum(numbers)
    result = []
    for value in get_iter():
        percent = 100 * value / total
        result.append(percent)
    return result

#- 방법2
#- collection.abc 내장 모듈 isinstance 를 사용해 검사
def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):   #- <<-- 
        raise TypeError("컨테이너를 제공해야 합니다.")
    total = sum(numbers)
    result = []
    for value in get_iter():
        percent = 100 * value / total
        result.append(percent)
    return result    
~~~
- 결과적으로 `normalize_defensive`는 리스트와 ReadVisits에 대해 모두 제대로 작동함.  
  <b>리스트나 ReadVisits 모두 이터레이터 프로토콜을 따르는 이터러블 컨테이너 --> iterable 객체</b>이기 떄문!
~~~python
percentages = normalize_defensive(numbers=visits)
percentages = normalize_defensive(numbers=ReadVisits('test.txt'))
~~~

### 기억해야 할 내용
- 입력 인자를 여러번 이터레이션하는 함수나 메서드를 조심해라. 입력받은 인자가 이터레이터면 함수가 이상하게 작동할 수 있다
- 파이썬의 이터레이터 프로토콜은 컨테이너와 이터레이터가 iter, next 내장 함수나 for 루프 등의 관련 식과 상호작용하는 절차를 정의
- __iter__ 메서드를 제너레이터로 정의하면 쉽게 이터러블 컨테이너 타입을 정의할 수 있음
- 어떤 값이 이터레이터인지 감지하려면, 이 값을 iter 내장 함수에 넘겨서 반환하는 값이 원래 값과 같은지 확인하면 됨  
  다른 방법으로 `collections.abc.Iterator` 클래스를 `isinstance`와 함께 사용할 수 있음

### 32- 긴 리스트 컴프리헨션보다는 제너레이터 식을 사용해라
- 리스트 컴프리헨션의 문제점은 입력 시퀀스와 같은 수의 원소가 들어 있는 리스트 인스턴스를 만들어 낼 수 있다는 것  
  이 것은 입력의 크기가 작으면 문제가 되지 않지만, 입력이 커지면 메모리를 상당히 많이 사용
- 예를 들어 특정 파일의 줄의 길이를 저장한다고 했을 때, 파일이 아주 크거나, 절대로 끝나지 않는 네트워크 소켓이라면  
  리스트 컴프리헨션을 사용하는 것이 문제가 될 수 있음
- 다음 코드는 입력이 작은 경우에 처리할 수 있는 컴프리헨션 코드 방식이다
~~~python
value = [len(x) for x in open('test.txt')]
print(value)
~~~
- 이러한 문제를 해결하기 위하여 <b>제너레이터 식(generator expression)</b>을 제공함
- 제너레이터 식은 리스트 컴프리헨션과 제너레이터를 일반화 한 것. <b>제너레이터 식을 실행해도 출력 시퀀스 전체가 실체화 되지 않음</b>
- 그 대신 제너레이터 식에 들어 있는 식으로부터 원소를 하나씩 만들어내는 이터레이터가 생성됨
- 제너레이터 식은 이터레이터로 즉시 평가되며, 더 이상 시퀀스 원소 계산이 진행되지 않음
~~~python
it = (len(x) for x in open('test.txt'))
print(it)

>>>
<generator object <genexpr> at 0x7fc05e9f2e50>
~~~
- `next` 함수를 통해 다음 값을 얻어 올 수 있으며, 제너레이터 식을 사용하면 메모리를 모두 소모하는 것을 염려할 필요 없이 원소를 원하는 대로 가져와 소비할 수 있음
~~~python
print(next(it))
print(next(it))
~~~
- 제너레이터 식의 또 다른 강력한 특징은 두 제너레이터 식을 합성할 수 있다는 것
~~~python
roots = ((x, x**0.5) for x in it)
next(roots)

>>>
(3, 1.7320508075688772)
~~~
- 결과적으로 아주 큰 입력 스트림에 대해 여러 기능을 합성해 적용해야 한다면, 제너레이터 식을 선택해라
- 다만 제너레이터가 반환하는 이터레이터에는 상태가 있기 때문에 이터레이터를 한 번만 사용해야 함

### 기억해야 할 내용
- 입력이 크면 메모리를 너무 많이 사용하기 때문에 리스트 컴프리헨션은 문제를 일으킬 수 있음
- 제너레이터 식은 이터레이터처럼 한 번에 원소를 하나씩 출력하기 때문에 메모리 문제를 피할 수 있음
- 제너레이터 식이 반환한 이터레이터를 다른 제너레이터 식의 하위 식으로 사용함으로써 제너레이터 식을 서로 합성할 수 있음
- 서로 연결된 제너레이터 식은 매우 빠르게 실행되며 메모리도 효율적으로 사용됨

## 33-yield from을 사용해 여러 제너레이터를 합성해라
- 제너레이터는 강점이 많아 다양한 프로그램에서 여러 단계에 걸쳐 한 줄기로 사용되고 있음
- 예를 들어 제너레이터를 사용해 화면의 이미지를 움직이게 하는 그래픽 프로그램이 있다고 하자. 원하는 시각적인 효과를 얻으려면 처음에는 이미지가 빠르게 이동하고, 잠시 멈춘 다음 다시 이미지가 느리게 이동해야 함
~~~python
def move(period, speed):
    for _ in range(period):
        yield speed

def pause(delay):
    for _ in range(delay):
        yield 0
~~~
- 최종 에니메이션을 만드려면 move와 pause를 합성해서 변위 시퀀스를 하나만 만들어야 함
- 애니메이션의 각 단계마다 제너레이터를 호출해서 차례로 이터레이션하고 각 이터레이션에서 나오는 변위를 순서대로 내보내는 방식으로 다음과 같이 시퀀스를 만듬
~~~python
def animate():
    for delta in move(4, 5.0):
        yield delta
    for delta in pause(3):
        yield delta
    for delta in move(2, 3.0):
        yield delta


def render(delta):
    print(f"Delta: {delta:.1f}")


def run(func):
    for delta in func():
        render(delta)


run(animate)
~~~
- 위의 코드는 animate가 너무 반복적이라 가독성이 떨어짐
- 이 문제의 해법은 `yield from` 식을 사용하는 것. 이는 고급 제너레이터 기능으로, 제어를 부모 제너레이터에게 전달하기 전에 내포된 제너레이터가 모든 값을 내보냄
~~~python
def animate_composed():
    yield from move(4, 5.0)
    yield from pause(3)
    yield from move(2, 3.0)


run(animate_composed)
~~~
- <b>`yield from`은 근본적으로 파이썬 인터프리터가 for 루프를 내포시키고 yield 식을 처리하도록 함</b>
  결과적으로 성능도 더 좋아짐
- 다음 코드에서는 timeit 내장 모듈을 통해 마이크로 벤치마크를 실행함으로써 성능이 개선되는지 살펴봄
~~~python
import timeit
def child():
    for i in range(1_000_000):
        yield i

def slow():
    for i in child():
        yield

def fast():
    yield from child()

baseline = timeit.timeit(
    stmt='for _ in slow(): pass',
    globals=globals(),
    number=50)
print(f"수동 내포: {baseline:2f}s")

comparison = timeit.timeit(
    stmt='for _ in fast(): pass',
    globals=globals(),
    number=50)
print(f"합성 사용: {comparison:2f}s")

reduction = (baseline - comparison) / baseline
print(f"{reduction:.1%} 시간이 적게 듬")

>>>
수동 내포: 3.555208s
합성 사용: 3.266115s
8.1% 시간이 적게 듬
~~~
- 만약 제너레이터를 합성한다면 `yield from`을 사용해라

#### 기억해야 할 내용
- `yield from`식을 사용하면 여러 내장 제너레이터를 모아 제너레이터 하나로 합성할 수 있음
- 직접 내포된 제너레이터를 이터레이션하면서 각 제너레이터의 출력을 내보내는 것보다 yield from을 사용하는 것이 성능면에서 더 좋음

### 34-send로 제너레이터에 데이터를 주입하지 말라
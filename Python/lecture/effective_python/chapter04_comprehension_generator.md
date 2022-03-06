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
#- (공구)의 개수가 들어있는 stock을 조사해서 batch_size 를 입력하여 각 공구별 batch 값을 구하는 예제
#- 주문이 들어오면 batch size를 계산

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
#- america_travel_normalize 
#  --> 해당 도시 여행자 수 / 전체 여행자 수 * 100 인 비율을 나타내는 값을 계산하여 배열에 저장하는 함수

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
#- collection.abc 내장 모듈 Iterator인지 isinstance를 사용해 검사
def normalize_defensive(numbers):
    if isinstance(numbers, Iterator):   #- <<-- 
        raise TypeError("컨테이너를 제공해야 합니다.")
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result    
~~~
- 결과적으로 `normalize_defensive`는 리스트와 ReadVisits에 대해 모두 제대로 작동함.  
  <b>리스트나 ReadVisits 모두 이터레이터 프로토콜을 따르는 이터러블 컨테이너 --> iterable 객체</b>이기 때문!
~~~python
percentages = normalize_defensive(numbers=visits)
percentages = normalize_defensive(numbers=ReadVisits('test.txt'))
~~~

### 기억해야 할 내용
- 입력 인자를 여러번 이터레이션하는 함수나 메서드를 조심해라. 입력받은 인자가 이터레이터면 함수가 이상하게 작동할 수 있다
- 파이썬의 이터레이터 프로토콜은 컨테이너와 이터레이터가 iter, next 내장 함수나 for 루프 등의 관련 식과 상호작용하는 절차를 정의
- `__iter__` 메서드를 제너레이터로 정의하면 쉽게 이터러블 컨테이너 타입을 정의할 수 있음
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

#### 기억해야 할 내용
- 입력이 크면 메모리를 너무 많이 사용하기 때문에 리스트 컴프리헨션은 문제를 일으킬 수 있음
- 제너레이터 식은 이터레이터처럼 한 번에 원소를 하나씩 출력하기 때문에 메모리 문제를 피할 수 있음
- 제너레이터 식이 반환한 이터레이터를 다른 제너레이터 식의 하위 식으로 사용함으로써 제너레이터 식을 서로 합성할 수 있음
- 서로 연결된 제너레이터 식은 매우 빠르게 실행되며 메모리도 효율적으로 사용됨

### 33-yield from을 사용해 여러 제너레이터를 합성해라
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
- 직접 내포된 제너레이터를 이터레이션하면서 각 제너레이터의 출력을 내보내는 것보다 `yield from`을 사용하는 것이 성능면에서 더 좋음

### 34-send로 제너레이터에 데이터를 주입하지 말라
- 앞서 제너레이터 함수를 통해 이터레이션이 가능한 출력 값을 만들어 낼 수 있음을 확인했는데, 이러한 데이터 채널은 단방향임
- 제너레이터가 데이터를 내보내면서 다른 데이터를 받아들일 때 직접 쓸 수 있는 방법이 없는 것처럼 보임
- 다음은 소프트웨어 라디오를 사용해 신호를 내보낸다고 하자. 다음 코드는 주어진 간격과 진폭에 따른 sine wave 값을 생성
~~~python
import math


def wave(amplitude, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = amplitude * fraction
        yield output


def transmit(output):
    if output is None:
        print(f"출력 None")
    else:
        print(f"출력: {output:>5.1f}")


def run(it):
    for output in it:
        transmit(output)


run(wave(3.0, 8)) 
~~~
- 위의 코드는 잘 작동하는데, 하지만 별도의 입력을 사용해 진폭을 지속적으로 변경해야 한다면 이 코드는 쓸모가 없음
- 제너레이터를 이터레이션 할 때마다 진폭을 변조할 수 있는 방법이 필요
- 파이썬 제너레이터는 `send` 메서드를 지원함. 이 메서드는 `yield` 식을 양방향 채널로 격상시켜 줌
- send 메서드를 사용하면 입력을 제너레이터에 스트리밍하는 동시에 출력을 내보낼 수 있음
- 일반적으로 제너레이터를 이터레이션할 때 `yield` 식이 반환하는 값은 None임
~~~python
def my_generator():
    received = yield 1
    print(f"받은 값 = {received}")


it = iter(my_generator())
output = next(it)           #- 첫번째 제너레이터 출력을 얻음
print(f"출력값 = {output}")

try:
    next(it)                #- 종료될 때까지 제너레이터를 실행함
except StopIteration:
    pass
~~~
- for 루프나 next 내장 함수로 제너레이터를 이터레이션하지 않고 send 메서드를 호출하면, 제너레이터가 재개될 때 yield가 send에 전달된 파라미터 값을 반환함
- 하지만 방금 시작한 제너레이터는 아직 yield 식에 도달하지 못했기 때문에 최초로 send를 호출할 때 인자로 전달할 수 있는 유일한 값은 None뿐임
~~~python
it = iter(my_generator())
output = it.send(None)
print(f"출력값 : {output}")

try:
    it.send('안녕!')
except StopIteration:
    pass
~~~
- 이런 동작을 활용해 입력 시그널을 바탕으로 사인 파의 진폭을 변조할 수 있음
- 먼저 Yield 식이 반환한 진폭 값을 amplitude에 저장하고, 다음 Yield 출력 시 이 진폭 값을 활용하도록 wave 제너레이터를 변경해야 함
~~~python
def wave_moduling(steps):
    step_size = 2 * math.pi / steps
    amplitude = yield
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        output = radians * fraction
        amplitude = yield output
~~~
- 다음으로는 run 함수를 수정해서 매 이터레이션마다 wave_modulating 제너레이터에게 스트리밍하도록 만듬
- 아직 제너레이터가 yield 식에 도달하지 못했으므로 send에 보내는 첫 번째 입력은 None이어야 함
~~~python
def run_modulating(it):
    amplitudes = [None, 7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10]
    for amplitude in amplitudes:
        output = it.send(amplitude)
        transmit(output)

run_modulating(wave_moduling(12))
~~~
- 위의 코드는 정상적이게 잘 작동함. 제너레이터가 첫 번째 yield 식에 도달할 때까지는 amplitude 값을 받지 못하므로, 예상대로 첫 번째 출력은 None임
- 해당 코드의 문제점은 이해하기 어렵고, 대입문의 오른쪽에 yield를 사용하는 것은 직관적이지 않음
- 또한 제너레이터 고급 기능을 잘 모를 경우는 send와 yield 사이의 연결을 알아보기 어려움
- 또한 프로그램의 요구 사항이 복잡해져, 여러 신호의 시퀀스로 이루어진 복잡한 파형을 사용해야 한다고 하자
- 한가지 방법은 `yield from` 식을 이용해 여러 제너레이터를 합성하는 것
- 기존 wave 함수에 `yield from` 을 이용한 것과 `wave_modulating`은 결과적으로 차이가 남
~~~python
def complex_wave():
    yield from wave(7.0, 3)
    yield from wave(2.0, 4)
    yield from wave(10.0, 5)

run(complex_wave())

>>>
출력:   0.0
출력:   6.1
출력:  -6.1
출력:   0.0
출력:   2.0
출력:   0.0
출력:  -2.0
출력:   0.0
출력:   9.5
출력:   5.9
출력:  -5.9
출력:  -9.5


def complex_wave_modulating():
    yield from wave_moduling(3)
    yield from wave_moduling(4)
    yield from wave_moduling(5)

run_modulating(complex_wave_modulating())

>>>
출력: None
출력:   0.0
출력:   1.8
출력:  -3.6
출력: None
출력:   0.0
출력:   1.6
출력:   0.0
출력:  -4.7
출력: None
출력:   0.0
출력:   1.2
~~~
- 출력에 None이 여럿 보이는데, 내포된 제너레이터에 대한 yield from 식이 끝날 때마다  다음 yield from 식이 실행됨
- 각각의 내포된 제너레이터는 send 메서드 호출로부터 값을 받기 위해 아무런 값도 만들어내지 않는 단순한 yield 식으로 시작함
- 이로 인해 부모 제너레이터가 자식 제너레이터를 옮겨갈 때마다 None이 출력됨
- <b>이는 yield from과 send를 따로 사용할 때는 제대로 작용하던 특성이 같이 사용할 때는 깨짐</b>
- 결과적으로 해결할 방법은 있지만, 그정도의 노력을 기울일 만한 가치는 없음. `send` 메서드를 아예 쓰지 않고 단순한 접근 방법을 사용할 것을 권장함
- 가장 쉬운 해결책은 wave 함수에 이터레이터를 전달하는 것
~~~python
def wave_cascading(amplitude_it, steps):
    step_size = 2 * math.pi / steps
    for step in range(steps):
        radians = step * step_size
        fraction = math.sin(radians)
        amplitude = next(amplitude_it)
        output = amplitude * fraction
        yield output


def complex_wave_cascading(amplitude_it):
    yield from wave_cascading(amplitude_it, 3)
    yield from wave_cascading(amplitude_it, 4)
    yield from wave_cascading(amplitude_it, 5)


def run_cascading():
    amplitudes = [7, 7, 7, 2, 2, 2, 2, 10, 10, 10, 10, 10]
    it = complex_wave_cascading(iter(amplitudes))
    for _ in amplitudes:
        output = next(it)
        transmit(output)
~~~

#### 기억해야 할 내용
- send 메서드를 사용해 데이터를 제너레이터에 주입할 수 있음
- 제너레이터는 send로 주입된 값을 yield 식이 변환하는 값을 통해 받으며, 이 값을 변수에 저장해 활용할 수 있음
- send와 yield from 식을 함께 사용하면 제너레이터의 출력에 None이 불쑥불쑥 나타내는 의외의 결과를 얻을 수 있음
- 합성할 제너레이터들의 입력으로 이터레이터를 전달하는 방식이 send를 사용하는 방식보다 더 낫다. send는 가급적 사용하지 말라

### 35-제너레이터 안에서 throw로 상태를 변화시키지 말라
- 제너레이터의 고급 기능으로 yield from 식과 send 메서드 외에, 제너레이터 안에서 Exception을 다시 던질 수 있는 throw 메서드가 있음
- `throw` 는 어떤 제너레이터에 대해 throw가 호출되면 이 제너레이터는 값을 내놓은 `yield`로부터 평소처럼 제너레이터 실행을 계속하는 대신, throw가 제공한 Exception을 다시 던짐
- 다음 코드는 이런 동작 방식을 보여줌
~~~python
class MyError(Exception):
    pass

def my_generator():
    yield 1
    yield 2
    yield 3


it = my_generator()
print(next(it))
print(next(it))
print(it.throw(MyError('test error')))

>>>
1
2
Traceback (most recent call last):
  File "<input>", line 13, in <module>
  File "<input>", line 6, in my_generator
MyError: test error
~~~
- throw를 호출해 제너레이터에 예외를 주입해도, 제너레이터는 try/except 복합문을 사용해 마지막으로 실행된 yield 문을 둘러쌈으로써 이 예외를 잡아낼 수 있음
~~~python
def my_generator():
    yield 1

    try:
        yield 2
    except MyError:
        print("MyError 발생")
    else:
        yield 3

    yield 4


it = my_generator()
print(next(it))
print(next(it))
print(it.throw(MyError('test error')))

>>>
1
2
MyError 발생
4
~~~
- 이 기능은 제너레이터와 제너레이터를 호출하는 쪽 사이에 양방향 통신 수단을 제공함
- 경우에 따라서는 이 양방향 통신 수단이 유용할 수도 있음. 예를 들어 작성하는 프로그램에 간헐적으로 재설정할 수 있는 타이머가 필요하다고 해보자

#### Timer 예제
- 다음은 throw 메서드에 의존하는 제너레이터를 통해 타이머를 구현하는 코드임
- yield 식에서 Reset 예외가 발생할 때마다 period로 재설정됨
- 매 초 한 번 풀링(polling)되는 외부 입력과 이 재설정 이벤트를 연결할 수도 있음(`check_for_reset()`)
- 그 후에는 timer를 구동시키는 run 함수를 정의할 수 있음
- run 함수는 throw를 사용해 타이머를 재설정하는 예외를 주입하거나, 제너레이터를 출력에 대해 announce 함수를 호출
~~~python
class Reset(Exception):
    pass

def timer(period):
    current = period
    while current:
        current -= 1
        try:
            yield current
        except Reset:
            current = period

def check_for_reset():
    ...


def announce(remaining):
    print(f"{remaining} 틱 남음")


def run():
    it = timer(4)
    while True:
        try:
            if check_for_reset():
                current = it.throw(Reset())
            else:
                current = next(it)
        except StopIteration:
            break
        else:
            announce(current)

run()
~~~
- 위의 코드는 잘 실행되지만, 필요 이상으로 읽기 어려움. 각 내포 단계마다 StopIteration 예외를 잡아내거나 throw를 할지, next나 announce를 호출할지 결정하는데, 이로 인해 코드에 잡음이 많음
- 이 기능을 구현하는데 더 단순한 방법은 <b>이터러블 컨테이너 객체를 사용해 상태가 있는 클로저를 정의하는 것</b>
- 다음의 코드는 꼭 기억하자
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
- 결과적으로 출력은 throw를 사용하던 예전 버전과 똑같지만, 훨씬 더 이해하기 쉽게 구현됨
- 따라서 예외적인 경우를 처리해야 한다면 throw를 전혀 사용하지 말고 iterable class를 사용할 것을 권장!

#### 기억해야 할 내용
- throw 메서드를 사용하면 제너레이터가 마지막으로 실행한 yield 식의 위치에서 예외를 발생시킬 수 있음
- throw를 사용하면 가독성이 나빠짐. 예외를 잡아내고 다시 발생시키는 데 준비 코드가 필요하며, 내포 단계가 깊어짐
- <b>제너레이터에서 예외적인 동작을 제공하는 더 나은 방법은 `__iter__` 메서드를 구현하는 클래스를 사용하면서 예외적인 경우에 상태를 전이시키는 것</b> 

### 36 이터레이터나 제너레이터를 다룰 때는 itertools를 사용해라
- `itertools` 내장 모듈에는 이터레이터를 구조화하거나 사용할 때 쓸모 있는 여러 함수가 있음
- 3가지 범주로 나눠서 itertools 내장모듈 함수에 대해서 알아보자

#### 여러 이터레이터 연결하기
~~~python
import itertools

#- chain : 여러개의 이터레이터를 하나로 합칠 때
it = itertools.chain([1, 2, 3], [4, 5, 6])
print(list(it))

#- repeat: 한 값을 계속 반복하고 싶을 때
it = itertools.repeat('Hi', 3)
print(list(it))

#- cycle: 특정 이터레이터를 게속 반복하고 싶을 때
it = itertools.cycle([1,2])
result = [next(it) for _ in range(10)]
print(result)

#- tee : 한 이터레이터를 병렬적으로 두 번째 인자로 지정된 개수
#-       의 이터레이터로 만들고 싶을 때
it1, it2, it3 = itertools.tee(['하나', '둘'], 3)
print(list(it1))
print(list(it2))
print(list(it3))

#- zip_logest
#- 여러 이터레이터 중 짧은 쪽 이터레이터를 fillvalue로 채워 return

keys = ['하나', '둘', '셋']
values = [1,2]

normal = list(zip(keys, values))
print('zip:', normal)

it = itertools.zip_longest(keys, values, fillvalue='None')
longest = list(it)
print(longest)
print("zip longest : ", longest)
~~~

#### 이터레이터에서 원소 거르기
~~~python
#- islice
# 이터레이터를 복사하지 않으면서 slicing하고 싶을 때 사용
# 동작은 리스트의 시퀀스 슬라이싱과 스트라이딩과 비슷
import itertools


values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
first_five = itertools.islice(values, 5)
print(list(first_five))

middle_odds = itertools.islice(values, 2, 8, 2)
print("중간의 홀수들 : ", list(middle_odds))

#- takewhile
#- False가 반환될 때까지의 원소를 돌려줌
values = list(range(10))
less_than_seven = lambda x: x < 7
it = itertools.takewhile(less_than_seven, values)
print(list(it))

#- dropwhile
#- takewhile의 반대
values = list(range(10))
less_than_seven = lambda x : x < 7
it = itertools.dropwhile(less_than_seven, values)
print(list(it))

#- filterfalse
#- filterfalse는 filter 내장 함수의 반대
#- 즉, 이터레이터에서 false에 해당하는 모든 원소를 돌려줌
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = lambda x: x % 2 == 0
filter_result = filter(evens, values)
print("Filter: ", list(filter_result))

filter_false_result = itertools.filterfalse(evens, values)
print("Filter false:", list(filter_false_result))
~~~

#### 이터레이터에서 원소의 조합 만들어내기
~~~python
#- accumulate
#- 파라미터를 두 개 받는 함수를 반복 적용하면서 이터레이터 원소 값 하나를 줄여줌
#- 함수가 돌려주는 이터레이터는 원본 이터레이터의 각 원소에 대해 누적된 결과를 내놓음

import itertools

values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sum_reduce = itertools.accumulate(values)
print("합계 :", list(sum_reduce))

def sum_modulo_20(first, second):
    output = first + second
    return output % 20


modulo_reduce = itertools.accumulate(values, sum_modulo_20)
print('20으로 나눈 나머지의 합계:', list(modulo_reduce))


#- product
#- 하나 이상의 이터레이터에 들어 있는 데카르트 곱을 반환
single = itertools.product([1,2], repeat=2)
print("리스트 한 개:", list(single))

multiple = itertools.product([1,2], ['a', 'b'])
print("리스트 두 개:", list(multiple))

#- permutations
#- 이터레이터가 내놓은 원소들로부터 만들어낸 길이 N인 순열을 돌려줌
it = itertools.permutations([1,2,3,4] ,2)
print(list(it))


#- combinations
#- combinations는 이터레이터가 내놓은 원소들로부터 만들어낸 길이 N인 조합을 돌려줌
it = itertools.combinations([1,2,3,4], 2)
print(list(it))


#- combinations_with_replacement
#- combinations와 같지만 원소의 반복을 허용함
it = itertools.combinations_with_replacement([1,2,3,4], 2)
print(list(it))
~~~

#### 기억해야 할 내용
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
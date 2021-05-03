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
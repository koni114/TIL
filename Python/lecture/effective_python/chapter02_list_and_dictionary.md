# chapter02 list and dictionary
### 11-시퀀스를 슬라이싱하는 방법을 익혀라
- 처음과 끝을 포함할 때는 인덱스를 포함하지 말아라
- 음수를 포함한 인덱싱을 잘 사용해라
~~~python
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('가운데 2개 :', a[3:5])
print('처음과 끝을 제외한 나머지 :', a[1:7])
print(a[-3:])    # ['f', 'g', 'h']
print(a[:-1])    # ['a', 'b', 'c', 'd', 'e', 'f', 'g']
print(a[-3:-1])  # ['f', 'g'] 
~~~
- 범위를 지정한 인덱싱은 인덱싱의 범위가 넘어가도 무시됨
- 리스트를 슬라이싱한 결과는 완전히 새로운 리스트이기 때문에 결과로 얻은 리스트를 수정해도 원래 리스트트 변경되지 않음
~~~python
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
b = a[2:5]
b[0] = 99
print(a[2:5])   #- ['c', 'd', 'e']
print(b)        #- [99, 'd', 'e']
~~~
- 인덱스 없이 [:]만 사용하면 리스트가 그대로 복사됨
- 시작과 끝 인덱스가 없는 슬라이스에 대입하면 슬라이스가 참조하는 리스트의 내용을 대입하는 리스트의 복사본으로 덮어씀
~~~python
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
b = a
print("이전 a", a)
print("이전 b", b)
a[:] = [101, 102, 103]
print("이후 a", a)
print("이전 b", b)
~~~
- 리스트 슬라이스에 다른 길이가 다른 리스트를 대입이 가능

### 12-스트라이드와 슬라이스를 한 식에 함께 사용하지 말라
- 스트라이드(stride) : 파이썬은 리스트로 일정한 간격을 두고 슬라이싱을 할 수 있는 구문
- 다음의 구문은 인덱스를 짝수와 홀수 그룹을 나누는 방법
~~~python
x = ['빨강','주황','노랑','파랑','초록','자주']
x[::2]   #- 짝수 인덱스 호출
x[1::2]  #- 홀수 인덱스 호출
~~~
- 스트라이드의 가장 큰 활용 방법은 -1을 넣어 글자를 뒤집는 것
~~~python
x = 'mongoose'
x[::-1]  #- 'esoognom'
~~~
- 유니코드(우리가 사용하는 문자) 데이터를 UTF-8로 인코딩한 문자열에서는 이 코드가 동작하지 않음
~~~python
x = "안녕하세요"  #- 유니코드 문자열
y = x.encode('utf-8')
z = y[::-1]
z.decode('utf-8') #- UnicodeDecodeError
~~~
- 다음과 같이 슬라이싱 구문에 스트라이드를 같이 쓰면 매우 혼란스러우므로 
  같이 쓰는 것은 피하자(스트라이딩 한 후 슬라이싱하자)
- <b>스트라이딩한 다음 슬라이싱 하면 데이터를 한 번더 얕게 복사함. 따라서 첫 번째 연산에서 슬라이스의 크기를 최대한 줄여야 함</b>
- 만약 두 단계에서의 메모리를 감당할 수 없다면, `itertools` 내장 모듈의 `islice` 메서드를 고려하자

### 13- 슬라이싱보다는 나머지를 모두 잡아내는 언패킹을 사용하자
- 기본 언패킹의 한 가지 한계점은 언패킹할 시퀀스의 길이를 알고 있어야 한다는 점이다
- 다음의 예는 오류를 발생
~~~python
car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)
oldest, second_oldest = car_ages_descending

#- error
ValueError: too many values to unpack (expected 2)
~~~
- 보통 이런 경우에는 해결하기 위하여 인덱싱을 통한 슬라이싱을 이용함
~~~python
oldest = car_ages_descending[0]
second_oldest = car_ages_descending[1]
others = car_ages_descending[2:]

print(oldest, second_oldest, others)
~~~
- 위의 코드는 잘 작동하지만, 시각적으로 noise가 많고, 잘못된 오류로 인해서 인덱싱이 잘못 될 경우, off-by-one error를 발생시킬 수 있음
- <b>파이썬은 이런 문제를 해결하기 위하여 별표 식(starred expression)</b>을 사용해 모든 값을 담는 언패킹을 할 수 있도록 지원
~~~python
oldest, second_oldest, * others = car_ages_descending
print(oldest, second_oldest, others)
~~~
- 이 코드가 더 좋은 이유는 더 짧고, 인덱스 경계 값이 어긋나서 오류가 발생할 여지가 없다는 것
- 별표는 어디에든 사용할 수 있는데, 꼭 언패킹해야만 하는 값 외에 여분의 슬라이스가 하나 필요한 경우, 나머지를 모두 잡아내는 기능의 이점을 살릴 수 있음
~~~python
oldest, *others, youngest = car_ages_descending
print(oldest, youngest, others)
~~~
- 별표식만을 이용해 언패킹할 수 없음을 기억하자
- 한 수준의 언패킹 패턴에 두개의 별표를 사용할 수 없다
~~~python
* others = car_ages_descending
# SyntaxError: starred assignment target must be in a list or tuple 
first, * middle, * second_middle, last = [1,2,3,4]
# SyntaxError: two starred expressions in assignment
~~~
- 여러 계층으로 이뤄진 구조를 언패킹할 때는 서로 다른 부분에 포함되는 한 별표 식을 여럿 사용해도 됨
- 다음의 방식을 권장하지는 않지만, 이해하면 좋다!
~~~python
((loc1, (best1, *rest1)),
(loc2, (best2, *rest2))) = car_inventory.items()

print(f'{loc1} 최고는 {best1}, 나머지는 {len(rest1)}종')
print(f'{loc2} 최고는 {best2}, 나머지는 {len(rest2)}종')

>>> 
시내 최고는 그랜저, 나머지는 2종
>>>
공항 최고는 제네시스 쿠페, 나머지는 3종
~~~
- <b>별표 식은 항상 list 인스턴스가 됨. 언패킹하는 시퀀스에 남는 원소가 없으면 별표 식 부분은 []이 됨</b>
~~~python
short_list = [1,2]
first, second, *rest = short_list
print(first, second, rest)

>>>
1 2 []
~~~
- 별표 식은 항상 리스트를 만들어내기 때문에 이터레이터를 별표 식으로 언패킹하면 out of memory error 발생할 수 있음
- 따라서 결과 데이터가 모두 메모리에 들어갈 수 있다고 확신할 때만 나머지를 모두 잡아내는 언패킹을 사용해야 함

### 14- 복잡한 기준을 사용해 정렬할 때는 key 파라미터를 사용하자
- list의 내장 타입에는 리스트의 원소를 여러 기준에 따라 정렬할 수 있는 sort 메서드가 들어가 있음
~~~python
numbers = [93, 86, 11, 68, 70]
numbers.sort()
print(numbers)
~~~
- sort를 통해 객체를 처리하려면 어떻게 해야하는지 살펴보자
- 다음은 매직메소드인 `__repr__`를 정의한 class이다
~~~python
class Tool:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f'Tool({self.name!r}, {self.weight})'


tools = [
    Tool('수준계', 3.5),
    Tool('해머', 1.25),
    Tool('스크류드라이버', 0.5),
    Tool('끌', 0.25)
]

tools
~~~
- 위의 `tools` 변수에 `sort`함수를 호출하면 비교 특별 메서드가 정의되어 있지 않으므로 정렬할 수 없다
~~~python
tools.sort()

>>>
AttributeError: 'set' object has no attribute 'sort'
~~~
- 만약 `__lr__` 특별 메소드를 정의하면 sort함수를 사용할 수 있다
- 하지만 사용자가 원하는 순서를 반영하고 싶으면 `key` 파라미터를 활용한다
- `key`는 함수어야 함
- `key` 함수에는 정렬할 리스트의 원소가 전달됨. 이 원소는 정렬가능한 값(숫자, 문자열 등..)이어야 함
- 다음 예제는 name으로 정렬한 예시임
~~~python
tools.sort(key=lambda x: x.name)
tools

>>> 
[Tool('끌', 0.25), Tool('수준계', 3.5), Tool('스크류드라이버', 0.5), Tool('해머', 1.25)]
~~~
- key로 전달될 원소가 기본 타입(문자열..등)인 경우에는 값을 변형할 수도 있음
~~~python
places = ['home', 'work', 'New York', 'Paris']
places.sort()
print("대소문자 구분 : ", places)

>>>
대소문자 구분 :  ['New York', 'Paris', 'home', 'work']

places.sort(key=lambda x: x.lower())
print("대소문자 무시 : ", places)

>>>
대소문자 무시 :  ['home', 'New York', 'Paris', 'work']
~~~
- 파이썬에서 가장 쉬운 해법은 튜플을 사용하는 것  
- 즉 튜플은 매직 메소드인 `__lt__` 정의가 들어있다는 것. 이 특별 비교 메서드는 튜플의 각 위치를 이터레이션하면서 각 인덱스에 해당하는 원소를 한 번에 하나씩 비교하는 방식을 구현돼 있음
~~~python
saw = (5, '원형 톱')
jackhammer = (40, '착암기')
jackhammer < saw

>>>
False
~~~
- 다음과 같이 weight로 정렬하고, 그 후 name으로 정렬할 수 있음
~~~python
power_tools = [
    Tool('드릴', 4),
    Tool('원형 톱', 5),
    Tool('착암기', 40),
    Tool('연마기', 4)
]

power_tools.sort(key=lambda x: (x.weight, x.name))
power_tools

>>>
[Tool('드릴', 4), Tool('연마기', 4), Tool('원형 톱', 5), Tool('착암기', 40)]
~~~
- <b>key 함수의 한 가지 제약 사항은 모든 비교 기준의 정렬 순서가 같아야 한다는 점이다(모두 오름차순이거나 내림차순이어야 함)</b>
- 따라서 숫자값의 경우 - 부호를 통해 오름차순을 내림차순으로 변경할 수 있음(문자열은 안됨)
~~~python
power_tools.sort(key=lambda x: (-x.weight, x.name))
power_tools.sort(key=lambda x: (x.weight, -x.name)) #- error
~~~
- 파이썬에서는 위의 상황을 해결하기 위하여 stable sort 알고리즘을 제공함
- <b>리스트 타입의 sort 메소드는 key 함수가 반환하는 값이 서로 같은 경우 리스트에 들어 있던 원래 순서를 그대로 유지해줌</b>
- 즉 같은 리스트에 대해서 서로 다른 기준으로 sort를 여러 번 호출해도 된다는 의미
- 다음과 같이 weight 기준 내림차순, name 기준 오름차순으로 정렬하는데, sort를 두번 호출하는 방식으로 정렬 수행 
~~~python
power_tools.sort(key=lambda x: x.name)
power_tools.sort(key=lambda x: x.weight, reverse=True)
power_tools

>>>
[Tool('착암기', 40), Tool('원형 톱', 5), Tool('드릴', 4), Tool('연마기', 4)]
~~~
- 연속적으로 sort 함수를 사용해 내가 원하는 정렬을 만들어 낼 수 있는데, 역순으로 호출해야 함을 잊지말자

### 딕셔너리 삽입 순서에 의존할 때에는 조심해라
- 파이썬 3.5버전 이전에는 딕셔너리에 대한 순서를 보장하지 않았음  
  그 이유는 예전의 딕셔너리 구현이 내장 hash 함수와 파이썬 인터프리터가 시작할 때 초기화되는 seed 값을 사용하는 해시 테이블 알고리즘으로 만들어졌기 때문
- 따라서 인터프리터 실행 시마다 달라지는 seed값 때문에 삽입 순서가 일치하지 않음
- 파이썬 3.6 버전부터는 딕셔너리가 삽입 순서를 보존하도록 동작이 개선됐음
~~~python
baby_names = {
    'cat':'kitten',
    'dog':'puppy'
}

baby_names
>>>
{'cat': 'kitten', 'dog': 'puppy'}
~~~
- 이로 인해 편해진 점은 함수에 대한 키워드 인자인 `**kwargs` 는 예전에는 순서가 뒤죽박죽이라 함수 호출을 디버깅하기가 힘들었음
~~~python

def my_func(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

my_func(goose='gosling', kangaroo='joey')

>>>
goose = gosling
kangaroo = joey
~~~
- 클래스도 인스턴스 디셔너리에 dict 타입을 사용하는데, 예전 파이썬 버전에서는  
  object 필드가 난수 같은 동작을 보임
~~~python
class MyClass:
    def __init__(self):
        self.alligator = 'hatching'
        self.elephant = 'calf'

a = MyClass()
for key, value in a.__dict__.items():
    print(f'{key} = {value}')
~~~
- collection 내장 모듈에는 삽입 순서를 유지해주는 OrderedDict라는 클래스가 있었음  
  클래스의 동작이 표준 dict의 동작과 비슷하기는 하지만, `OrderedDict`의 성능 특성은 dict와 많이 다름
- <b>키 삽입과 popitem 호출을 자주 처리해야 한다면, 표준 파이썬에서 제공하는 dict보다 OrderedDict가 더 나음</b>
- 하지만 딕셔너리를 처리할 때 삽입 순서 관련 동작이 항상 성립한다고 생각해서는 안됨
- 파이썬에서는 프로그래머가 list, dict등의 표준 프로토콜(protocol)을 흉내 내는 커스텀 컨테이너 타입을 쉽게 정의할 수 있음  
- 파이썬은 정적 타입 지정 언어가 아니기 때문에 대부분의 경우 코드는 엄격한 클래스 계층보다는 객체의 동작이 객체의 실질적인 타입을 결정하는 <b>덕 타이핑</b>에 의존하며, 이로 인해 가끔 어려운 함정에 빠질 수 있음
- 다음의 코드를 보면서 실제로 확인해보자
- 다음은 특정 콘테스트에서 득표를 가장 많이 받은 득표자를 확인하는 코드다
~~~python
votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863
}


def populate_ranks(votes, ranks):
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i


def get_winner(ranks):
    return next(iter(ranks))


ranks = {}
populate_ranks(votes, ranks)
print(ranks)
winner = get_winner(ranks)
print(winner)

>>>
{'otter': 1, 'fox': 2, 'polar bear': 3}
otter
~~~
- 이 때 요구사항이 변경되어, 결과를 보여줄 떄 등수가 아닌 알파벳순으로 표시해야 한다고 생각해보자  
  `collections.abc` 모듈을 사용해 딕셔너리와 비슷하지만 내용을 알파벳 순서대로 이터레이션 해주는 클래스를 새로 정의할 수 있음
~~~python
from collections.abc import MutableMapping


class SortedDict(MutableMapping):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        keys = list(self.data.keys())
        keys.sort()
        for key in keys:
            yield key

    def __len__(self):
        return len(self.data)


sorted_ranks = SortedDict()
populate_ranks(votes, sorted_ranks)
print(sorted_ranks.data)
winner = get_winner(sorted_ranks)
print(winner)

>>>
{'otter': 1, 'fox': 2, 'polar bear': 3}
fox
~~~
- SortedDict class는 표준 딕셔너리의 프로토콜을 지키므로, 오류가 발생하지 않지만 실행 결과는 요구사항과 맞지 않는다
- 그 이유는 `get_winner`함수의 구현이 `populate_ranks`의 삽입 순서에 맞게 딕셔너리를 이터레이션 한다고 가정하는데 있음
- 이 코드는 `dict` 대신 `SortedDict`를 사용하므로 이 가정은 더이상 성립하지 않음
- 이 문제를 해결하기 위한 세 가지 방법이 있음

- 해결방안1 : ranks 딕셔너리가 어떤 특정 순서로 이터레이션된다고 가정하지 않고 `get_winner`함수를 구현하는 것
~~~python
def get_winner(ranks):
    for name, rank in ranks.items():
        if rank == 1:
            return name
~~~
- 해결방안2 : 함수 맨 앞에 ranks의 타입이 우리가 원하는 타입인지 검사하는 것. 그렇지 않으면 예외를 던짐
~~~python
def get_winner(ranks):
    if not isinstance(ranks, dict):
        raise TypeError('dict instance가 필요합니다.')
    return next(iter(ranks))
~~~
- 해결방안3 : type annotation을 사용해서 `get_winner`에 전달되는 값이 딕셔너리와 비슷한 동작을 하는 Mutable Mapping 인스턴스가 아니라 dict 인스턴스가 되도록 강제하는 것
~~~python
def get_winner(ranks):
    if not isinstance(ranks, dict):
        raise TypeError('dict instance가 필요합니다.')
    return next(iter(ranks))

from typing import Dict, MutableMapping

def populate_ranks(votes: Dict[str, int],
                   ranks: Dict[str, int]) -> None:
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks[name] = i

def get_winner(ranks: Dict[str, int]) -> str:
    return next(iter(ranks))

class SortedDict(MutableMapping[str, int]):
~~~

### 16-in을 사용하고 딕셔너리 키가 없을 때 KeyError를 처리하기 보다는 get을 사용해라
- dict안에 key가 없을 수 있는데, 이 때 keyError가 발생한다. 이 때 `get` 함수를 사용하면 훨씬 간결하게 처리할 수 있음
~~~python
counters = {
    '폼퍼니켈':2,
    '샤워도우':1
}

key = '밀'
#- 가독성이 떨어지는 코드
if key in counters:
    count = counters[key]
else:
    count = 0

counters[key] = count + 1

#- 가독성이 높은 코드
counters[key] = counters.get(key, 0) + 1
~~~
- 만약 딕셔너리에 저장된 값이 리스트처럼 더 복잡한 값이라면 어떻게 해야 할까? 
- 예를 들어 득표수만 세는 것이 아니라, 어떤 사람이 어떤 유형의 빵에 투표했는지도 알고 싶은 경우다
~~~python
votes = {
    '바게트': ['철수', '순이'],
    '치아바타': ['하니', '유리']
}
key = '브리오슈'
who = '단이'

if key in votes:
    names = votes[key]
else:
    votes[key] = names = []
names.append(who)
print(votes)
~~~
- 위의 예제는 `votes[key] = names = []`를 한줄로 처리하고, 디폴트 값으로 빈 리스트를 딕셔너리에 넣고  
  나면 참조를 통해 리스트 내용을 변경할 수 있으므로, `append`를 호출한 다음 리스트를 다시 딕셔너리에 대입할 필요는 없음 
- 다음과 같이 keyError 예외가 발생한다는 것을 이용할 수도 있음
~~~python
try:
    names = votes[key]
except KeyError:
    votes[key] = names = []
names.append(who)
~~~
- 이 방법은 키가 있을 때는 한번만 읽으면 되고, 키가 없을 때는 키를 한 번 읽고 한번 대입하면 되므로 조금 더 효율적임 
- 다음은 `get`과 왈러스 연선자를 이용하여 조금 더 간결하게 만든 코드문
~~~python
if (name := votes.get(key)) is None:
    votes[key] = names = []
names.append(who)
~~~
- dict 타입은 이 패턴을 더 간단히 사용하게 해주는 `setdefault` 메서드를 제공함
- `get`과 다른 점은 키가 없으면 제공받은 디폴트 값을 키에 입력하고, 입력된 값을 반환
- 즉 이 값은 새로 저장된 디폴트 값일 수도 있고, 이미 딕셔너리에 있던 키에 해당하는 값일 수도 있음
~~~python
names = votes.setdefault(key, [])
names.append(who)
~~~
- 위의 코드는 확실히 짧지만 가독성이 떨어짐. 특히 `setdefault`라는 말의 의미가 이상하다. 값을 얻는 함수인데 왜 setdefault일까?
- <b>또한 키가 없으면 setdefault에 전달된 디폴트 값이 별도로 복사되지 않고 딕셔너리에 직접 대입됨</b>
- 다음 코드는 값이 리스트인 경우 이런 동작으로 인해 벌어지는 상황을 보여줌
~~~python
data = {}
key = 'foo'
value = []
data.setdefault(key, value)
print('이전 : ', data)
value.append('hello')
print('이후 : '. data)
~~~
- <b>이는 키에 해당하는 디폴트 값을 setdefault에 전달할 때마다 그 값을 새로 만들어야 한다는 것</b>
- 즉 호출할 때마다 리스트를 새로 만들어야 하므로 성능이 크게 저하될 수 있음
- 만약 가독성과 효율성을 향상시키고자 디폴트 값에 사용하는 객체를 재활용한다면 이상한 동작을 하게되고 버그가 발생할 것임
- 다음의 최초 예제에서 왜 `setdefault`를 사용하지 않았을까?
~~~python
count = counters.setdefault(key, 0)
counters[key] = count + 1
~~~
- 이유는, `count` 값을 증가시키고 나면 다시 딕셔너리에 저장해야 하므로, setdefault가 수행하는 디폴트 값 대입은 불필요함
- 즉 setdefault는 키를 한 번 읽고, 대입을 두 번하므로, 불 필요함
- 결과적으로 setdefault를 사용하는 것이 딕셔너리 키를 처리하는 지름길인 경우는 드물다

### 17-내부 상태에서 원소가 없는 경우를 처리할 때는 setdefault보다 defaultdict를 사용해라
- `collections` 내장 모듈에 있는 defaultdict 클래스는 키가 없을 때 자동으로 값을 저장해서 간단히 처리할 수 있도록 해줌
- 키가 없을 때 default 값을 만들기 위해 호출할 함수를 제공해야 함
~~~python
from collections import defaultdict


class Visits:
    def __init__(self):
        self.data = defaultdict(set)

    def add(self, country, city):
        self.data[country].add(city)


visits = Visits()
visits.add('영국', '바스')
visits.add('영국', '런던')
print(visits.data)
~~~
- `add` 코드는 data 딕셔너리에 있는 키에 접근하면 항상 기존 set 인스턴스가 반환된다고 가정
- `add` 메서드가 아주 많이 호출되면 집합 생성에 따른 비용도 커지는데, 이 구현에서 불필요한 set이 만들어지는 경우는 없음 
- 키로 어떤 값이 들어올지 모르는 딕셔너리를 관리할 때, collections 내장 모듈에 있는 defaultdict 인스턴스가 상황에 맞다면 defaultdict를 사용해라

### 18- __missing__을 사용해 키에 따라 다른 디폴트 값을 생성하는 방법을 알아두라
- 앞서 setdefaultdict과 defaultdict 타입이 필요한 처리를 못하는 경우가 있음
- 예를 들어 파일 시스템에 있는 SNS 프로필 사진을 관리하는 프로그램을 작성한다고 가정해보자
- 필요할 때 파일을 읽고 쓰기 위해 프로필 사진의 경로와 열린 파일 핸들을 연관시켜주는 딕셔너리가 필요
- 다음 코드에서는 일반 dict 인스턴스를 사용하고 get 메서드와 대입식을 통해 키가 딕셔너리에 있는지 검사함
~~~python
pictures = {}
path = 'profile_1234.png'

handle = pictures.get(path)
if handle is None:
    try:
        handle = open(path, 'a+b')
    except OSError:
        print(f'경로를 알 수 없습니다 : {path}')
        raise
    else:
        pictures[path] = handle

handle.seek(0)
image_data = handle.read()
~~~
- 위의 코드는 내포되는 블록 깊이가 깊어지고, 딕셔너리를 많이 읽는 단점이 있음
- 따라서 다음 코드와 같이 setdefault를 이용해 작성할 수 있다
~~~python
try:
    handle = pictures.setdefault(path, open(path, 'a+b'))
except OSError:
    print(f'경로를 열 수 없습니다: {path}')
    raise
else:
    handle.seek(0)
    image_data = handle.read()
~~~
- 위의 코드는 문제가 많다. 파일 핸들을 만드는 내장 함수인 open이 딕셔너리에 경로가 있는지 여부와 관계없이  
  항상 호출됨
- 이로 인해 같은 프로그램상에 존재하던 열린 파일 핸들과 혼동될 수 있는 새로운 파일 핸들이 생길 수 있음 
- 또한 open이 예외를 발생시킬 때, 같은 줄에 있는 setdefault가 던지는 예외와 구분하지 못할 수도 있음
- 그래서 다음코드는 defaultdict를 활용하여 함수를 작성해 보았다
~~~python
from collections import defaultdict

path = 'file_1234.png'

def open_picture(profile_path):
    try:
        return open(profile_path, 'a+b')
    except OSError:
        print(f'경로를 열 수 없습니다: {profile_path}')
        raise


pictures = defaultdict(open_picture)
handle = pictures[path]
handle.seek(0)
image_data = handle.read()

>>>
TypeError: open_picture() missing 1 required positional argument: 'profile_path'
~~~
- 문제는 <b>defaultdict 생성자에 전달한 함수는 인자를 받을 수 없다</b> 이로 인해 파일 경로를 사용해 open을 호출할 방법이 없음
- 이런 상황에서는 setdefault와 defaultdict 모두 필요한 기능을 제공하지 못함 
- 이런 상황이 흔히 발생하기 때문에 파이썬은 다른 해법을 내장해 제공함. <b>dict 타입의 하위 클래스를 만들고 `__missing__` 특별 메서드를 구현하면 키가 없는 경우를 처리하는 로직을 커스텀화 할 수 있음</b>
~~~python
class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value


pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()
~~~
- `path`가 딕셔너리에 없으면 `__missing__` 메서드가 호출됨. 해당 메소드는 키에 해당하는 디폴트 값을 호출해 딕셔너리에 넣어준 다음에 호출한 쪽에서 그 값을 반환해야 함
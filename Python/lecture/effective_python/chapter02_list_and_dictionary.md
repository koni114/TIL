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

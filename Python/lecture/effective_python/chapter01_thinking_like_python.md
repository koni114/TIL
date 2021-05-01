### 사용 중인 파이썬의 버전 알아두기
- 파이썬2는 2020년 1월 1일부터 지원 중지
- 파이썬 버전 알아두기
~~~python
import sys
print(sys.version_info)
print(sys.version)
~~~

### PEP 8 가이드 따르기
#### 공백
- 문법적으로 중요한 들여쓰기는 탭 보다는 4칸 스페이스 사용
- 긴 식을 다음 줄에 이어서 쓸 경우에는 일반적인 들여쓰기보다 4 스페이스 더 들여쓰기
- 함수와 클래스 사이는 2줄
- 클래스 안에 메소드는 한줄 띄어쓰기

#### 명명규약
- 함수, 변수, attribute는 소문자와 밑줄을 사용
- protected instance attribute는 첫칸을 밑줄로 시작
- private instance attribute는 두칸을 밑줄로 시작
- 클래스는 CapitalizedWord처럼 여러 단어를 붙임. 각 단어의 첫글자는 대문자
- 모듈 수준의 상수는 ALL_CAPS처럼 모든 글자 대문자 

#### 식과 문
- 빈 container나 sequence를 검사할 때는 길이를 비교하지 말고, 빈 컨테이너나 시퀀스가 비어 있지 않은 경우 True로 평가하는 것을 이용해 조건문을 활용
- 한줄짜리 if, for, while, except 복합문 사용하지 않기

#### 임포트
- import문은 항상 제일 앞에 배치
- 모듈을 import할 때는 절대적인 이름을 사용. 현 모듈의 경로에 상대적인 이름을 사용 하지 않기
~~~python
from bar import foo #- 좋은 예
import foo          #- 나쁜 예
~~~ 
- 반드시 상대적인 경로로 임포트 해야하는 경우는 `from . import foo`
로 명시하기
- import 적을 때 표준 라이브러리 모듈, 서드 파티 모듈, 사용자 customizing 모듈 순서로 섹션 나누기

### bytes와 str 차이 알아두기
- 파이썬에서는 문자열 데이터의 시퀀스를 표현하는 두가지 방식이 있음
  - <b>`bytes`와 `str`</b>
- bytes 타입의 인스턴스에는 부호가 없는 8바이트 데이터가 그대로 들어감(종종 아스키 인코딩을 사용해 내부 문자를 표시)  
~~~python
a = b'h\x65llo'
print(list(a))
print(a)
~~~
- str 인스턴스에는 사람이 사용하는 언어의 문자를 표현하는 유니코드 코드 포인트가 들어 있음
~~~python
a = 'a\u0300 propos'
~~~
- <b>중요한 사실은 str 인스턴스에는 직접 대응하는 이진 인코딩이 없고, bytes에는 직접 대응하는 텍스트 인코딩이 없음</b>
- 처리할 입력이 원하는 문자 시퀀스인지 확실히 하려면 도우미 함수를 사용하자
~~~python
def to_str(str_or_bytes):
    if isinstance(str_or_bytes, bytes):
        value = str_or_bytes.decode('utf-8')
    else:
        value = str_or_bytes

    return value
~~~
- bytes 인스턴스를 str 인스턴스에 더할 수 없음
- bytes와 str인스턴스를 (>, ==, +, %와 같은) 연산자에 섞어서 사용할 수 없음
- 이진 데이터를 파일에서 읽거나 파일에 쓰고 싶으면 항상 이진 모드('rb'나 'wb')로 파일 열기
- `open`에 encoding 파라미터를 명시적으로 전달하자

### str-format을 쓰기 보다는 f-문자열을 통한 인터폴레이션 사용하기
- % 연산자를 사용하는 C 스타일 형식화 문자열은 여러 가지 단점과 번잡성이라는 문제가 있음
- str.format도 C 스타일 형식 문자열의 문제점을 그대로 가지고 있으므로 사용을 피해야 함
- f-문자열은 값을 문자열 안에 넣는 새로운 구문으로 C 스타일 형식과 문자열의 가장 큰 문제점을 해결
- f-문자열은 간결하지만 위치 지정자 안에 파이썬 식을 포함시킬 수 있어 강력함
~~~python
key = 'my_var'
value = 1.234
f_string = f'{key:<10} = {value:.2f}'    #- 가장 간결하고 가독성이 좋음
c_tuple = '%-10s = %.2f' % (key, value)
str_args = '{:<10} = {:.2f}'.format(key, value)
str_kw = '{key:<10} = {value:.2f}'.format(key=key, value=value)
c_dict = '%(key)-10s = %(value).2f' % {'key':key, 'value':value}
assert f_string == c_tuple == c_dict
assert f_string == str_args == str_kw
~~~
~~~python
pantry = (('아보카도',1), ('바나나',2), ('체리',3))
for i, (item, count) in enumerate(pantry):
    old_style = '#%d: %-3s = %d' % (
        i+1,
        item.title(),
        round(count)
    )

    f_string = f'#{i+1}: {item.title():<3s} = {round(count)}'

    assert f_string == old_style
~~~
- 다음과 같이 출력할 숫자 개수를 파라미터화 할 수 있음
~~~python
places = 3
number = 1.23456
print(f'내가 고른 숫자는 {number: .{places}f}')
~~~

### 복잡한 식을 쓰지 말고, help function을 제작해라
- 다음의 식을 help function을 통해 간결화해라!
~~~python
from urllib.parse import parse_qs
my_values = parse_qs('빨강=5&파랑=0&초록=', keep_blank_values=True)
print(repr(my_values))

#- 복잡한 식 -> 가독성이 떨어짐
int(my_values.get('빨강')[0] or 0)
int(my_values.get('파랑')[0] or 0)
int(my_values.get('초록')[0] or 0)

#- 다음과 같이 두 세번 반복되는 logic은 반드시 함수를 작성하자
def get_first_int(values, key, default=0):
    found = values.get(key, [""])
    if found[0]:
        return int(found[0])
    else:
        return default

get_first_int(my_values, '빨강')
~~~
- 파이썬 문법을 사용하면 아주 복잡하고 읽기 어려운 한 줄짜리 식을 쉽게 작성할 수 있지만, 좋지 않음
- 복잡한 식을 help function으로 옮기자. 특히 같은 로직을 반복해 사용할 때에는 도우미 함수를 꼭 사용하자

### 인덱스 사용 대신에 대입을 사용해 언패킹하자
~~~python
snacks = [('베이컨', 350), ('도넛', 240), ('머핀', 190)]
#- 인덱스를 사용하는 경우,
for i in range(len(snacks)):
    item = snacks[i]
    name = item[0]
    calories = item[1]
    print(f'#{i+1}: {name}은 {calories} 칼로리입니다.')

#- 언패킹을 사용하는 경우
for rank, (name, calories) in enumerate(snacks, 1):
    print(f'#{rank}: {name}은 {calories} 칼로리입니다.')
~~~

### range보다는 enumerate를 사용해라
- `range(len(list))`는 가독성이 떨어질 수 있음. 차라리 `enumerate` 함수를 사용하자
- enumerate는 지연 계산 제너레이터(lazy generator)로 감쌈
- emumerate의 두 번째 파라미터로 어디부터 수를 세기 시작할 것인지 지정할 수 있음
~~~python
flavor_list = ['바닐라', '초콜릿', '딸기', '피칸']
for i,flavor in enumerate(flavor_list, 1):
    print(f'#{i}: {flavor}')
~~~

### for나 while 루프 뒤에 else 블록을 사용하지 말자
- 파이썬은 다른 언어들과 다르게 루프가 반복 수행하는 내부 블록 다음에 else 블록을 추가 할 수 있음
- for/else에서 `else`는 루프가 끝나자마자 실행됨
- 조심해야 할 것은 '루프가 정상적으로 완료하지 않으면 else문을 실행해라'가 아닌 반대로 동작한다는 것
- 실제로 루프 안에서 break문을 실행하면 else 블록이 실행되지 않음
~~~python 
for i in range(3):
    print('Loop', i)
    break
else:
    print('Else block!')

# 결과
Loop 0
~~~
- 빈 sequence에 대해서 루프를 실행하면 else 블록이 바로 실행됨
~~~python
for i in []:
    print('Loop', i)
    break
else:
    print('Else block!')

# 결과
Else block!
~~~
- <b>동작이 직관적이지 않고 혼동을 야기할 수 있으므로 루프 뒤에 else 블록은 사용하지 말자</b>

### 대입식을 사용해 반복을 피하자(중요)
- 대입식은 영어로 assignment expression 또는 왈러스 연산자라고도 부름
- 왈러스 연산자는 `a := b`라고 쓰며 `a 왈러스 b`라고 읽음
- <b>python 3.8부터 도입된 연산자</b>
- 대입식은 대입문이 쓰일 수 없는 위치에서 변수에 값을 대입할 수 있으므로 유용함  
  예를 들어 if문의 조건식 안에서 대입식을 쓸 수 있음
- 대입식의 값은 왈러스 연산자 왼쪽에 있는 식별자에 대입된 값으로 평가됨
~~~python 
fresh_fruit = {
    '사과': 10,
    '바나나': 8,
    '레몬': 5
}

def make_lemonade(count):
    print("레모네이드를 만들어냅니다!")

def out_of_stuck(count):
    print("재고 소진!")

#- 왈러스 연산자를 사용하기 전
count = fresh_fruit.get('레몬', 0)
if count:
    make_lemonade(count)
else:
    out_of_stuck(count)

#- 왈러스 연산자 사용
if count := fresh_fruit.get('레몬', 0):
    make_lemonade(count)
else:
    out_of_stuck(count)
~~~


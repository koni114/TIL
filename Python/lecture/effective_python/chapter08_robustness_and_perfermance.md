## chapter08 강건성과 성능
- 유용한 파이썬 프로그램을 만들었다면, 오류가 발생해도 문제 없도록 production화 해야함
- 예상치 못한 상황을 만나도 프로그램을 신뢰할 수 있도록 만드는 것은 프로그램을 제대로 작동시키는 것 만큼이나 중요!
- 파이썬은 프로그램을 더 강화시켜 다양한 상황에서 프로그램을 강건하게 만드는 데 도움이 되는 다양한 기능과 모듈을 내장하고 있음
- 강건성에는 규모 확장성과 성능이라는 차원이 포함됨. 알고리즘 복잡도나 다른 계산 부가 비용으로 인해 아주 큰 데이터를 처리하는 파이썬 프로그램이 전체적으로 느려지는 경우가 자주 있음
- 다행히 파이썬은 최소의 노력으로 고성능을 달성할 수 있도록 다양한 데이터 구조와 알고리즘을 제공함

### 65- try/except/finally의 각 블록을 잘 활용해라
- 파이썬에서 예외를 처리하는 과정은 try/except/else/finally 라는 네 블록에 해당됨
- 전체 복합문에서 각 블록은 서로 다른 목적에 쓰이며, 다양하게 조합하면 유용함

#### finally 블록
- 예외를 함수 자신을 호출한 함수 쪽(호출 스택의 위)로 전달해야 하지만, 예외가 발생하더라도 정리 코드를 실행해야 한다면 `try/finally`를 사용해라
- 파일 핸들을 안전하게 닫기 위해 try/finally를 사용하는 경우가 자주 있음
~~~python
def try_finally_example(filename):
    print("* 파일 열기")
    handle = open(filename, encoding='utf-8') #- OSError가 발생할 수 있음
    try:
        print("* 데이터 읽기")
        return handle.read() # Unicode Decode Error 발생 가능
    finally:
        print("* close() 호출")
        handle.close()
~~~
- read 메서드에서 예외가 발생하면 항상 `try_finally_example`을 호출한 쪽으로 이 예외가 전달되지만, `finally` 블록에 있는 handle의 close 메서드가 먼저 호출됨
~~~python
filename = 'random_data.txt'
with open(filename, 'wb') as f:
    f.write(b"\xf1\wfefdege\sfdfe") #- 잘못된 utf-8 이진 문자열

try_finally_example(filename)

>>> 
* 파일 열기
* 데이터 읽기
* close() 호출
Traceback (most recent call last):
...
~~~
- 파일을 열 때 발생하는 오류(파일이 없을 때 발생하는 OSError)는 finally 블록을 전혀 거치지 않고 호출한 쪽에 전달해야 하므로 try 블록 앞에서 Open을 호출해야 함
~~~python
try_finally_example('does_not_exist.txt')

>>>
* 파일 열기
Traceback (most recent call last):
~~~

#### else 블록
- 코드에서 처리할 예외와 호출 스택을 거슬러 올라가며 전달할 예외를 명확히 구분하기 위해 try/catch/else를 사용해라
- try 블록이 예외를 발생시키지 않으면 else 블록이 실행됨
- <b>else 블록을 사용하면 try 블록 안에 들어갈 코드를 최소화 할 수 있음</b>
- try 블록에 들어가는 코드가 줄어들면 발생할 여지가 있는 예외를 서로 구분할 수 있으므로 가독성이 좋아짐
- 예를 들어 문자열에서 JSON 딕셔너리 데이터를 읽어온 후 어떤 키에 해당하는 값을 반환하고 싶다고 하자
~~~Python
def load_json_key(data, key):
    try:
        print("* JSON 데이터 읽기")
        result_dict = json.loads(data) # ValueError가 발생할 수 있음
    except ValueError as e:
        raise KeyError(key) from e
    else:
        print("* 키 검색")
        return result_dict[key]        # keyError 발생 가능
~~~
- 성공적으로 실행되는 경우, JSON 데이터가 try 블록 안에서 디코딩된 다음에 else 블록 안에서 키 검색이 일어남
~~~python
assert load_json_key('{"foo":"bar"}', 'foo') == 'bar'

>>> 
* JSON 데이터 읽기
* 키 검색
~~~
- 입력이 올바른 JSON이 아니라면 `json.loads`가 디코딩하는 중간에 ValueError를 발생시킴. 이는 except 블록에 의해 처리됨
~~~python
load_json_key('{"foo": bad payload', 'foo')

>>>
* JSON 데이터 읽기
ValueError 처리
Traceback (most recent call last):
KeyError: 'foo'
...
~~~
- 키 검색에서 예외가 발생하면, try 블록 외부이므로 호출자에게 이 예외가 전달됨
- else 절은 try/except 뒤에 따라오는 코드를 except 블록과 시각적으로 구분해줌
- 이렇게 하면 예외가 전파되는 방식을 더 명확히 볼 수 있음
~~~python
load_json_key('{"foo": "bar"}', '존재하지 않음')

>>>
Traceback (most recent call last):
KeyError: '존재하지 않음'
~~~

#### 모든 요소를 한꺼번에 사용하기
- 복합적인 문장 안에 모든 요소를 다 사용하고 싶다면 try/except/else/finally를 사용해라
- 예를 들어 수행할 작업에 대한 설명을 파일에서 읽어 처리한 다음, 원본 파일 자체를 변경하고 싶음
- 이 경우 try 블록을 사용해 파일을 읽고 처리하며, try 블록 안에서 발생할 것으로 예상되는 예외를 처리하고자 except 블록을 사용함
- else 블록을 사용해 원본 파일의 내용을 변경하고, 이 과정에서 오류가 생기면 호출한 쪽에 예외를 돌려줌
- finally 블록은 파일 핸들을 닫음
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
- 정상적인 경우 try, else, finally 블록이 실행됨
~~~python
temp_path = 'random_data.json'

with open(temp_path, 'w') as f:
    f.write('{"numerator": 1, "denominator": 10}')

assert divide_json(temp_path) == 0.1

>>>
파일 열기
* 데이터 읽기
* JSON 데이터 읽기
* 계산 수행
* 계산 결과 쓰기
* close() 호출
~~~
- 계산이 잘못된 경우 try, except, finally 블록은 실행되지만 else는 실행안됨
- JSON 데이터가 잘못된 경우, try 블록이 실행돼 예외가 발생하고 finally 블록이 실행됨. 그리고 예외가 호출한 쪽에 전달됨. except와 else 블록은 실행되지 않음

#### 기억해야 할 내용
- try/finally 복합문을 사용하면 try 블록이 실행되는 동안 예외가 발생하든 발생하지 않든 정리 코드를 실행할 수 있음
- else 블록을 사용하면 try 블록 안에 넣을 코드를 최소화하고, try/except 블록과 성공적인 경우에 수행해야 할 코드를 시각적으로 구분할 수 있음
- try 블록이 성공적으로 처리되고 finally 블록이 공통적인 정리 작업을 수행하기 전에 실행해야 하는 동작이 있는 경우 else 블록을 사용할 수 있음

### 66-재사용 가능한 try/finally 동작을 원한다면 contextlib과 with 문을 사용해라
- 파이썬의 with 문은 코드가 특별한 컨텍스트(context) 안에서 실행되는 경우를 표현
- 예를 들어 상호 배제 락(뮤텍스)를 with 문 안에서 사용하면 락을 소유했을 때만 코드 블록이 실행되는 것을 의미함
~~~Python
from threading import Lock
lock = Lock()
with lock:
    # 어떤 불변 조건을 유지하면서 작업을 수행함
    ...
~~~
- Lock 클래스가 with 문을 적절히 활성화해주므로 위 예제는 다음 try/finally 구조와 동등함
~~~python
lock.acquire()
try:
    # 어떤 불변 조건을 유지하면서 작업을 수행함
    ...
finally:
    lock.release()
~~~
- 이 경우에는 with 문 쪽이 더 낫다. try/finally 구조를 반복적으로 사용할 필요가 없고, `acquire`에 대응하는 `release` 을 실수로 빠트리는 경우를 방지할 수 있기 때문
- `contextlib` 내장 모듈을 사용하면 우리가 만든 객체나 함수를 with 문에서 쉽게 쓸 수 있음
- `contextlib` 모듈은 with 문에 쓸 수 있는 함수를 간단히 만들 수 있는 `contextmanager` 데코레이터를 제공함
- 이 데코레이터를 사용하는 방법이 `__enter__`와 `__exit__` 특별 메서드를 사용해 새로 클래스를 정의하는 방법보다 훨씬 쉬움
- 예를 들어 어떤 코드 영역에서 디버깅 관련 로그를 더 많이 남기고 싶다고 하자
- 다음 코드는 두 단계의 심각성 수준에서 디버깅 로그를 남기는 함수를 정의함
~~~python
import logging

def my_function():
    logging.debug("디버깅 데이터")
    logging.error("이 부분은 오류 로그")
    logging.debug("추가 디버깅 데이터")
~~~
- 프로그램의 디폴트 로그 수준은 WARNING임. 따라서 이 함수를 실행하면 error 메세지만 화면에 출력됨
~~~python
my_function()

>>>
ERROR:root:이 부분은 오류 로그
~~~
- 컨텍스트 메니저를 정의하면 이 함수의 로그 수준을 일시적으로 높일 수 있음
- 이 도우미 함수는 with 블록을 실행하기 직전에 로그 심각성 수준을 높이고, 블록을 실행한 직후에 심각성 수준을 이전 수준으로 회복시켜줌
~~~python
from contextlib import contextmanager

@contextmanager
def debug_logging(level):
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield #- 이 부분이 with문 본문에서 수행될 코드문
    finally:
        logger.setLevel(old_level)
~~~
- `yield` 식은 with 블록의 내용이 실행되는 부분을 지정함
- `with` 블록 안에서 발생한 예외는 어떤 것이든 `yield` 식에 의해 다시 발생되기 때문에 이 예외의 도우미 함수(이 경우는 debug_logging)안에서 잡아낼 수 있음
- 이제 같은 로그 함수를 호출하되, 이번에는 debug_logging 컨텍스트 안에서 실행하자. with 블록 안에서는 화면에 모든 로그 메세지가 출력됨
- with 블록 밖에서 같은 함수를 실행하면 디버그 수준의 메세지는 화면에 출력되지 않음
~~~python
with debug_logging(logging.DEBUG):
    print("* 내부:")
    my_function()

print("* 외부")
my_function()

>>>
* 내부:
DEBUG:root:디버깅 데이터
ERROR:root:이 부분은 오류 로그
DEBUG:root:추가 디버깅 데이터
* 외부
ERROR:root:이 부분은 오류 로그
~~~

#### with와 대상 변수 함께 사용하기
- with문에 전달된 컨텍스트 매니저가 객체를 반환할 수도 있음. 이렇게 반환된 객체는 with 복합문의 일부로 지정된 지역 변수에 대입함
- 이를 통해 with 블록 안에서 실행되는 코드가 직접 컨텍스트 객체와 상호작용할 수 있음
- 예를 들어 파일을 작성하고 이 파일이 제대로 닫혔는지 확인하고 싶음. with 문에 open을 전달하면 이렇게 할 수 있음
- open은 with 문에서 as를 통해 대상으로 지정된 변수에게 파일 핸들을 전달하고, with 블록에서 나갈 때 이 핸들을 닫음
~~~python
with open('my_function.txt', 'w') as handle:
    handle.write('데이터입니다.')
~~~
- 이런 접근 방법은 파일 핸들을 매번 수동으로 열고 닫는 것보다 더 파이썬다운 방식임
- 이 방식을 사용하면 코드 실행이 with 문을 벗어날 때 결국에는 파일이 닫힌다고 확신할 수 있음
- 그리고 코드에서 문제가 될 수 있는 부분을 강조함으로써 파일 핸들이 열린 채로 실행되는 코드의 양을 줄이도록 우리를 북돋움
- 일반적으로 파일 핸들이 열려있는 부분을 줄이면 좋음
- <b>우리가 만든 함수가 as 대상 변수에게 값을 제공하도록 하기 위해 필요한 일은 컨텍스트 매니저 안에서 yield에 값을 넘기는 것뿐</b>
- 예를 들면, 다음과 같이 Logger 인스턴스를 가져와 로그 수준을 설정하고 yield로 대상을 전달하는 컨텍스트 매니저를 만들 수 있음
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
~~~
- with의 as 대상 변수로 얻은 로그 객체에 대해 debug와 같은 로그 관련 메서드를 호출하면, with 블록 내의 로그 심각성 수준이 낮게 설정돼 있으므로 디버깅 메세지가 출력됨
- 하지만 디폴트 로그 심각성 수준이 WARNING이기 때문에 logging 모듈을 직접 사용해 debug 로그 메서드를 호출하면 아무 메세지도 출력되지 않음
~~~python
with log_level(logging.DEBUG, 'my-log') as logger:
    logger.debug(f"대상 : {logger.name}!")
    logging.debug("이 메세지는 출력되지 않음")

>>>
DEBUG:my-log:대상 : my-log!
~~~
- with 문이 끝날 때 로그 심각성 수준이 원래대로 복구되므로, with 문 밖에서 my-log라는 로거에 대해 debug를 통해 메세지를 출력해도 아무 메세지가 표시되지 않음
- 하지만 error로 출력한 로그는 항상 출력됨
~~~python
logger = logging.getLogger("my-log")
logger.debug("디버그 메세지는 출력되지 않음")
logger.error("오류 메세지는 출력됨")

>>>
ERROR:my-log:오류 메세지는 출력됨
~~~
- 나중에 with 문을 바꾸기만 하면 로거 이름을 바꿀 수 있음. 이렇게 로거 이름을 바꾼 경우 with의 as 대상 변수가 가리키는 Logger가 다른 인스턴스를 가리키게 되지만, 이에 맞춰 다른 코드를 변경할 필요 없음
~~~python
with log_level(logging.DEBUG, 'other-log') as logger: #- other-log 로 변경
    logger.debug(f'대상 : {logger.name}!')  #- 코드가 변경되지 않음
    logging.debug('이 메세지는 출력되지 않음')

>>>
DEBUG:other-log:대상 : other-log!
~~~

#### 기억해야 할 내용
- with 문을 사용하면 try/finally 블록을 통해 사용해야 하는 로직을 재활용하면서 시각적인 잡음도 줄일 수 있음
- contextlib 내장 모듈이 제공하는 contextmanager 데코레이터를 사용하면 with 문에 사용가능
- 컨텍스트 매니저가 yield 하는 값은 with 문의 as 부분에 전달됨. 이를 활용하면 특별한 컨텍스트 내부에서 실행되는 코드 안에서 직접 그 컨텍스트에 접근할 수 있음

### 67- 지역 시간에는 time보다는 datetime을 사용해라
- 협정 세계시(Coordinated Universal Time, UTC)는 시간대와 독립적으로 시간을 나타낼 때 쓰는 표준임
- 유닉스 기준 시간 이후 몇 초가 흘렀는지 계산함으로써 시간을 표현하는 컴퓨터는 UTC를 잘 처리할 수 있음
- 하지만 자신의 현재 위치를 기준으로 따지는 인간에게는 적합하지 않음
- 사람들은 정오 8시나 오후 8시라고 얘기하지 UTC 15:00 마이너스 7시간 이라고 말하지는 않음
- 파이썬에서 시간대를 변환하는 방법은 두 가지임. 예전 방식은 time 내장 모듈을 사용하는데, 프로그래머가 실수하기 쉬움
- 새로운 방식은 `datetime` 내장 모듈을 사용하며, 파이썬 커뮤니티에서 만들어진 `pytz`라는 패키지를 활용하면 아주 잘 작동함
- 왜 `datetime`이 최선이고 `time`을 피해야 하는지 이해하려면 `time`과 `datetime`을 모두 제대로 알아야 함

##### time 모듈
- time 내장 모듈에 있는 localtime 함수를 사용해 유닉스 타임스탬프(UTC로 된 유닉스 기준 시간으로부터 몇 초가 흘렀는지)를 호스트 컴퓨터의 시간대에 맞는 지역 시간으로 변환함
- 지역 시간은 `strtime` 함수를 사용해 사람이 이해하기 쉬운 표현으로 출력함 
~~~python
import time
now = 159823184
local_tuple = time.localtime()
time_format = '%Y-%m-%d %H:%M:%S'
time_str = time.strftime(time_format, local_tuple)
print(time_str)

>>>
2021-05-15 13:38:32
~~~
- 반대로 변환해야 할 경우도 많음. 이 경우에는 사용자가 입력한 2021-05-15 13:38:32와 같은 지역 시간 표현을 지역 시간에 해당하는 유닉스 타임스탬프로 바꾸고, 이 값을 다시 UTC 시간대에 해당하는 유닉스 타임스탬프로 변환해야 함
- `strptime` 함수를 사용해 시간을 표현하는 문자열을 구문 분석한 다음, mktime을 호출해 지역 시간을 유닉스 타임스탬프로 변환함
~~~python
time_tuple = time.strptime(time_str, time_format)
utc_now = time.mktime(time_tuple)

>>>
1621111112.0
~~~
- 어떤 지역 시간대에 속한 시간을 어떻게 다른 시간대로 변환할 수 있을까? 예를 들어 서울에서 비행기를 타고 센프란시스코로 이동하는 경우, 센프란시스코에 도착했을 때 현지 시간으로 몇 시쯤인지 궁금할 것임
- 처음에는 time, localtime, strptime 함수가 반환하는 값을 직접 조작해 시간대를 변경하려고 생각할 수 있음
- 하지만 시간대를 변환하는 것은 좋은 생각이 아님. 시간대는 각 지역의 법에 따라 정해지므로 직접 조작하기에는 너무 복잡함
- 특히 세계 주요 도시의 출발/도착 시간을 변환해야 한다면 시간 변환이 너무 복잡해짐
- 여러 운영체제가 시간대 변경을 자동으로 해주는 설정 파일을 제공함. 우리의 플랫폼이 이런 설정을 지원한다면 파이썬에서도 time 모듈을 통해 이런 시간대를 활용할 수 있음
- 하지만 원도우 같은 플랫폼에서는 time 제공하는 시간대 관련 기능 중 몇 가지를 사용할 수 없음
- 예를 들어 다음 코드는 한국 표준 시간(KST)을 사용해 출발 시간을 구문 분석함
~~~python
import os     
parse_format = '%Y-%m-%d %H:%M:%S %Z'  # %Z는 시간대를 뜻함
depart_icn = '2020-08-27 19:13:04 KST'
time_tuple = time.strptime(depart_icn, parse_format)
time_str = time.strftime(time_format, time_tuple)
print(time_str)

>>>
2020-08-27 19:13:04
~~~
- KST로 설정한 시간이 제대로 작동하므로 다른 시간대도 잘 처리할 것으로 예상할 수 있음
- 하지만 실제로 그렇지 않음. strptime에 PDT를(미국 태평양 시간대) 사용하면 다음과 같은 오류 발생
~~~python
arrival_sfo = '2020-08-28 04:13:04 PDT'
time_tuple = time.strptime(arrival_sfo, time_format)

>>>
ValueError: unconverted data remains:  PDT
~~~
- 여기서 문제는 time 모듈이 플랫폼에 따라 다르게 작동한다는데 있음
- time 모듈의 동작은 호스트 운영체제의 C 함수가 어떻게 작동하는지에 따라 달라짐
- 따라서 파이썬에서는 time 모듈의 동작을 신뢰할 수 없음. 여러 시간대에서 time 모듈이 일관성 있게 동작한다고 보장할 수 없으므로, 여러 시간대를 다뤄야 하는 경우에는 time 모듈을 사용하면 안됨
- 여러 시간대 사이의 변환을 다룬다면 datetime 모듈을 사용해라

#### datetime 모듈
- 파이썬에서 시간을 표시하는 두 번째 방법은 datetime 내장 모듈에 있는 datetime 클래스를 사용하는 것임
- time 모듈과 마찬가지로 datetime을 사용하면 UTC나 지역 시간 등 여러 시간대에 속한 시간을 상호 변환 할 수 있음
- 다음 코드는 UTC로 된 시간을 컴퓨터의 지역 시간인 KST로 바꿈
~~~python
from datetime import datetime, timezone

now = datetime(2020, 8, 27, 10, 13, 4)      #- 시간대 설정이 안된 시간을 만듬
now_utc = now.replace(tzinfo=timezone.utc)  #- 시간대를 UTC로 강제 지정
now_local = now_utc.astimezone()            #- UTC 시간을 디폴트 시간대로 변환
print(now_local)

>>>
2020-08-27 19:13:04+09:00
~~~
- 또한 datetime 모듈을 사용하면 지역 시간을 UTC로 된 유닉스 타임스탬프로 쉽게 바꿀 수 있음
~~~python
time_str = '2020-08-27 19:13:04'
now = datetime.strptime(time_str, time_format)
time_tuple = now.timetuple()
utc_now = time.mktime(time_tuple)
print(utc_now)

>>>
1598523184.0
~~~
- time 모듈과는 달리 datetime 모듈은 한 지역 시간을 다른 지역 시간으로 바꾸는 신뢰할 수 있는 기능을 제공
- 하지만 datetime은 자신의 tzinfo 클래스와 이 클래스 안에 있는 메서드에 대해서만 시간대 관련 기능을 제공
파이썬 기본 설치에는 UTC를 제외한 시간대 정의가 들어있지 않음
- 다행히 파이썬 패키지 인덱스에서 pytz 모듈을 내려받아 기본 설치가 제공하지 않는 시간대 정보를 추가할 수 있음. pytz에는 우리에게 필요한, 모든 시간대 정보에 대한 완전한 데이터베이스가 들어 있음
- pytz를 효과적으로 사용하려면 항상 지역 시간을 UTC로 바꾸어야 함. 그 후 UTC 값에 대해 우리가 필요로 하는 datetime 연산을 수행. 그리고 UTC를 지역시간으로 바꾸자
~~~python
import pytz
arrival_sfo = '2020-08-28 04:13:04'
sfo_dt_naive = datetime.strptime(arrival_sfo, time_format)  #- 시간대가 설정되어 있지 않은 시간
eastern = pytz.timezone('US/Pacific')                       #- 센프란시스코의 시간대
sfo_dt = eastern.localize(sfo_dt_naive)                     #- 시간대를 센프란시스코 시간대로 변경
utc_dt = pytz.utc.normalize(sfo_dt.astimezone(pytz.utc))    #- UTC로 변경
print(utc_dt)
~~~
- 일단 UTC datetime을 얻으면, 이를 한국 지역 시간으로 변환할 수 있음
~~~python
korea = pytz.timezone('Asia/Seoul')
korea_dt = korea.normalize(utc_dt.astimezone(korea))
print(korea_dt)

>>>
2020-08-28 20:13:04+09:00
~~~
- 마찬가지로 네팔 시간으로도 쉽게 바꿀 수 있음
~~~python
nepal = pytz.timezone('Asia/Katmandu')
nepal_dt = nepal.normalize(utc_dt.astimezone(nepal))
print(nepal_dt)

>>>
2020-08-28 16:58:04+05:45
~~~
- datetime과 pytz를 사용하면 호스트 컴퓨터가 실행 중인 운영체제와 관계없이 어떤 환경에서도 일관성 있게 시간을 변환할 수 있음

### 기억해야 할 내용
- 여러 다른 시간대를 변환할 떄는 time 모듈을 쓰지 말라
- 여러 다른 시간대를 신뢰할 수 있게 변환하고 싶으면 datetime과 pytz 모듈을 함게 사용해라
- 항상 시간을 UTC로 표시하고, 최종적으로 표현하기 직전에 지역 시간으로 변환해라

### 68- copyreg를 사용해 pickle을 더 신뢰성 있게 만들어라
- `pickle` 내장 모듈을 사용하면  파이썬 객체를 바이트 스트림으로 직렬화하거나, 바이트 스트림을 파이썬 객체로 역직렬화 할 수 있음
- 피클된 바이트 스트림은 서로 신뢰할 수 없는 당사자 사이의 통신에 사용하면 안됨
- pickle의 목적은 우리가 제어하는 프로그램들이 이진 채널을 통해 서로 파이썬 객체를 넘기는데 있음
- 예를 들어 파이썬 객체를 사용해 게임 중인 플레이어의 진행 상태를 표현하고 싶다고 하자. 진행 상태는 플레이어의 레벨과 남은 생명 개수가 들어있음
~~~python
class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4


state = GameState()
state.level += 1
state.lives -= 1

print(state.__dict__)
{'level': 1, 'lives': 3}
~~~
- 사용자가 게임을 그만두면 나중에 이어서 진행할 수 있도록 프로그램이 게임 상태를 파일에 저장하며, pickle 모듈을 사용하면 상태를 쉽게 저장할 수 있음
- 다음 코드는 dump 함수를 사용해 GameState 객체를 파일에 기록함
~~~python
import pickle
state_path = 'game_state.bin'
with open(state_path, 'wb') as f:
    pickle.dump(state, f)
~~~
- 나중에 이 파일에 대해 load 함수를 호출하면 직렬화한 적이 전혀 없었던 것처럼 다시 GameState 객체를 돌려받을 수 있음
~~~python

with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

print(state_after.__dict__)

>>>
{'level': 1, 'lives': 3}
~~~
- 이런 접근 방법을 사용하면 시간이 지나면서 게임 기능이 확장될 때 문제가 발생함
- 플레이어가 최고점을 목표로 점수를 얻을 수 있게 게임을 변경한다고 생각해보자
- 사용자의 점수를 추적하기 위해 GameState 클래스에 새로운 필드를 추가해야함 
~~~python
class GameState:
    def __init__(self):
        self.level = 0
        self.lives = 4
        self.points = 0  #- 새로운 필드

state = GameState()
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)

>>>
{'level': 0, 'lives': 4, 'points': 0}
~~~
- 사용자가 예전 버전에서 저장한 GameState 객체를 사용해 게임을 이어서 진행하길 원하면 어떻게 해야할까?
- 다음은 과거 GameState 클래스 정의가 들어있는 프로그램을 사용해 예전 게임 파일을 역직렬화 한 경우임
~~~python 
with open(state_path, 'rb') as f:
    state_after = pickle.load(f)

print(state_after.__dict__)

>>>
{'level': 1, 'lives': 3}
~~~
- points 필드가 사라졌음. 특히 새로 반환받은 object가 GameState의 클래스이므로 굉장히 혼란스러움
~~~python
assert isinstance(state_after, GameState)
~~~
- 이런 동작은 pickle 모듈이 작동하는 방식의 부산물이라고 할 수 있음
- pickle의 주 용도는 객체 직렬화를 쉽게 만드는 것임. 우리가 pickle을 사용하는 방식이 아주 간단한 수준을 벗어나는 순간, pickle 모듈의 동작은 예상할 수 없는 방식으로 망가지기 시작함
- `copyreg` 내장 모듈을 사용하면 이런 문제를 쉽게 해결할 수 있음. 파이썬 객체를 직렬화하고 역직렬화할 때 사용할 함수를 등록할 수 있으므로 pickle의 동작을 제어할 수 있고, 그에 따라 `pickle` 동작의 신뢰성을 높일 수 있음

#### 디폴트 애트리뷰트 값
- 가장 간단한 경우, 디폴트 인자가 있는 생성자를 사용하면 GameState 객체를 언피클했을 때도 항상 필요한 모든 애트리뷰트를 포함시킬 수 있음
- 다음 코드는 이런식으로 생성자를 만든 것임
~~~python
class GameState:
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points
~~~
- 이 생성자를 피클링에 사용하려면 GameState 객체를 받아 copyreg 모듈이 사용할 수 있는 튜플 파라미터로 변환해주는 도우미 함수가 핊요함
- 이 함수가 반환한 튜플 객체에는 1. 언피클 시 사용할 함수와 2. 언피클 시 이 함수에 전달해야 하는 파라미터 정보가 들어감
~~~python
def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs, )
~~~
- 이제 `unpickle_game_state` 도우미 함수를 정의해야 함. 이 함수는 직렬화한 데이터와 pickle_game_state가 돌려주는 튜플에 있는 파라미터 정보를 인자로 받아 그에 대응하는 GameState 객체를 돌려줌. 생성자를 감싼 간단한 함수임 
~~~python
def unpickle_game_state(kwargs):
    return GameState(**kwargs)
~~~
- 이제 이 함수를 `copyreg` 내장 모듈에 등록함
~~~python
import copyreg
copyreg.pickle(GameState, pickle_game_state)
~~~
- 함수를 등록한 다음에는 직렬화와 역직렬화가 예전처럼 잘 작동함
~~~python
state = GameState()
state.points += 1000
serialized = pickle.dumps(state)
state_after = pickle.loads(serialized)
print(state_after.__dict__)

>>>
{'level': 0, 'lives': 4, 'points': 1000}
~~~
- 변경 함수를 등록한 다음, 다시 GameState의 정의를 바꿔서 사용자가 마법 주문을 얼마나 사용했는지 알 수 있게 함
- 이 변경은 GameState에 points 필드를 추가하는 변경과 비슷함
~~~python
class GameState:
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic    #- 추가한 필드
~~~
- 하지만 앞에서 points를 추가했던 경우와 달리, 예전 버전의 GameState를 역직렬화해도 애트리뷰트가 없다는 오류가 발생하지 않고 게임 데이터가 제대로 만들어짐
- pickle 모듈의 디폴트 동작은 object에 속한 애트리뷰트만 저장한 후 역직렬화할 때 복구하지만, unpickle_game_state는 GameState의 생성자를 직접 호출하므로 이런 경우에도 객체가 제대로 생성됨
- GameState의 생성자 키워드 인자에는 파라미터가 들어오지 않는 경우 설정할 디폴트 값이 지정돼 있음
- 따라서 예전 게임 상태 파일을 역직렬화하면 새로 추가한 magic 필드의 값은 디폴트 값으로 설정됨
~~~python
class GameState:
    def __init__(self, level=0, lives=4, points=0, magic=5):
        self.level = level
        self.lives = lives
        self.points = points
        self.magic = magic    #- 추가한 필드

print("이전:", state.__dict__)
state_after = pickle.loads(serialized)
print("이후:", state_after.__dict__)

>>>
이전: {'level': 0, 'lives': 4, 'points': 1000}
이후: {'level': 0, 'lives': 4, 'points': 1000, 'magic': 5}
~~~

#### 클래스 버전 지정
- 가끔은 파이썬 객체의 필드를 제거해 예전 버전 객체와의 하위 호환성이 없어지는 경우도 발생
- 이런 식의 변경이 일어나면 디폴트 인자를 사용하는 접근 방법을 사용할 수 없음
- 예를 들어 생명에 제한을 두는 것이 나쁜 것임을 깨닫고, 게임에서 생명이라는 개념을 없애고 싶다고 하자. 다음  코드는 lives 필드를 없앤 새로운 GameState 정의임
~~~python
class GameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic
~~~
- 문제는 이렇게 변경한 뒤에는 예전 게임 데이터를 역직렬화할 수 없다는 점임
- `unpickle_game_state` 함수에 의해 이전 데이터의 모든 필드가 `GameState` 생성자에게 전달되므로,  클래스에서 제거된 필드도 생성자에게 전달됨
~~~python
pickle.loads(serialized)

>>>
Traceback (most recent call last):
TypeError: __init__() got an unexpected keyword argument 'lives'
~~~
- `copyreg` 함수에게 전달하는 함수에 버전 파라미터를 추가하면 이 문제를 해결할 수 있음
- 새로운 GameState 객체를 피클링할 때는 직렬화한 데이터의 버전이 2로 설정됨
~~~python
def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    kwargs['version'] = 2
    return unpickle_game_state, (kwargs, )
~~~
- 이전 버전 데이터에는 version 인자가 들어있지 않음. 따라서 이에 맞춰 GameState 생성자에 전달할 인자를 적절히 변경할 수 있음
~~~python
def unpickle_game_state(kwargs):
    version = kwargs.pop('version', 1)
    if version == 1:
        del kwargs['lives']
    return GameState(**kwargs)
~~~
- 이제는 이전에 직렬화했던 객체도 제대로 역직렬화됨
~~~python
copyreg.pickle(GameState, pickle_game_state)
print("이전:", state.__dict__)
state_after = pickle.loads(serialized)
print("이후:", state_after.__dict__)

>>>
이전: {'level': 0, 'lives': 4, 'points': 1000}
이후: {'level': 0, 'points': 1000, 'magic': 5}
~~~
- 미래에 같은 클래스의 버전이 변경되는 경우에도 이와 같은 접근 방법을 계속 사용할 수 있음
- 이전 버전의 객체를 새 버전 객체에 맞추기 위해 필요한 모든 로직을 `unpickle_game_state` 함수에 넣을 수 있음

#### 안정적인 임포트 경로
- pickle을 할 때 마주칠수 있는 다른 문제점으로, 클래스 이름이 바뀌어 깨지는 경우를 볼 수 있음
- 프로그램이 존재하는 생명 주기에서 클래스 이름을 변경하거나, 클래스를 다른 모듈로 옮기는 방식으로 코드를 리펙터링하는 경우가 있음
- 불행히도 충분한 주의를 기울이지 않으면, 이런 변경이 일어난 경우 pickle 모듈이 제대로 작동하지 않음
- 다음 코드는 GameState 클래스를 BetterGameState 라는 이름으로 바꾸고, 기존 GameState 클래스를 프로그램에서 완전히 제거한 경우를 보여줌
~~~python
class BetterGameState:
    def __init__(self, level=0, points=0, magic=5):
        self.level = level
        self.points = points
        self.magic = magic
~~~
- 이제 이전 GameState 객체를 역직렬화하려고 시도하면 GameState 클래스를 찾을 수 없으므로 오류가 발생함
~~~python
pickle.loads(serialized)

>>>
Traceback ...
AttributeError: ...
~~~
- 이 예외가 발생하는 것은 피클된 데이터 안에 직렬화한 클래스의 임포트 경로가 들어 있기 때문
- 이 경우에도 `copyreg` 를 쓰는 것이 해결 방법이 될 수 있음. `copyreg`를 쓰면 객체를 언피클할 떄 사용할 함수에 대해 안정적인 식별자를 지정할 수 있음
- 이로 인해 여러 다른 클래스에서 다른 이름으로 피클된 데이터를 역직렬화 할 때 서로 전환할 수 있음
- 이 기능은 한 번 더 간접 계층을 추가해줌
~~~python
copyreg.pickle(BetterGameState, pickle_game_state)
~~~
- `copyreg`를 쓰면 BetterGameState 대신 unpickle_game_state에 대한 임포트 경로가 인코딩된다는 사실을 알 수 있음
~~~python
state = BetterGameState()
serialized = pickle.dumps(state)
print(serialized)
~~~
- 여기에는 `unpickle_game_state` 함수가 위치하는 모듈의 경로를 바꿀 수 없다는 작은 문제가 숨어 있음
- 일단 어떤 함수를 사용해 데이터를 직렬화하고 나면, 해당 함수를 미래에도 똑같은 임포트 경로에서 사용할 수 있어야 함

#### 기억해야 할 내용
- 신뢰할 수 있는 프로그램 사이에 객체를 직렬화하고 역직렬화할 때는 pickle 내장 모듈이 유용함
- 시간이 지남에 따라 클래스가 바뀔 수 있으므로 이전에 피클한 객체를 역직렬화하면 문제가 생길 수 있음
- 직렬화한 객체의 하위 호환성을 보장하고자 copyreg 내장 모듈과 pickle을 함께 사용해라

### 69-정확도가 매우 중요한 경우에는 decimal을 사용해라
- 파이썬은 수치 데이터를 처리하는 코드를 작성하기에 매우 좋은 언어임
- 파이썬 정수 타입은 실용적으로 어떤 크기의 정수든 표현할 수 있음
- double precision 부동소수점 타입은 IEEE 754 표준을 따르고, 파이썬 언어는 허수 값을 포함하는 표준 복소수 타입도 제공함
- 하지만 이런 타입들만으로는 충분하지 않은 경우가 있음
- 예를 들어 국제 전화 고객에게 부과할 통화료를 계산하는 경우를 생각해보자. 고객이 통화한 시간을 분과 초 단위로 알고 있으며, 미국과 남극 사이의 도수(분)당 통화료가 1.45달러/분이라고 하자. 전체 통화료는 얼마일까? 
- 부동소수점 수를 사용한 계산 결과는 어느 정도 타당해 보임
~~~python
rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print(cost)

>>>
5.364999999999999
~~~
- IEEE 754 부동소수점 수의 내부 표현법으로 인해 결과는 올바른 값보다 0.000...001 만큼 더 작음
- 물론 이 값을 센트 단위로 반올림해서 고객에게 5.37달러를 적절히 부과하자고 생각할 수도 있음
- 하지만 부동소수점 수의 오류로 인해 이 값을 가장 가까운 센트 단위로 반올림하면, 최종 요금이 늘어나지 않고 줄어들게 됨(5.364가 5.36으로 버려짐)
~~~python
print(round(cost, 2))

>>>
5.36
~~~
- 이 문제에 대한 해결 방법은 `decimal` 내장 모듈에 들어 있는 `Decimal` 클래스를 사용하는 것
- Decimal 클래스는 디폴트로 소수점 이하 28번째 자리까지 고정소수점 수 연산을 제공
- 심지어 자리수를 늘릴 수도 있음. 이 기능을 활용하면 IEEE 754 부동소수점 수에 존재하는 문제를 우회할 수 있음
- `Decimal`을 사용하면 반올림 처리도 원하는 대로 더 정확히 할 수 있음
- 예를 들어, 미국과 남극 사이의 통화료 문제를 `Decimal`을 사용해 처리하면 근사치가 아니라 정확한 요금을 구할 수 있음
~~~python
rate = Decimal('1.45')
seconds = Decimal(3*60 + 42)
cost = rate * seconds / Decimal(60)
print(cost)

>>>
5.365
~~~
- Decimal 인스턴스에 값을 지정하는 방법은 두 가지
- 첫째, 숫자가 들어 있는 str를 Decimal 생성자에 전달하는 방법. 이렇게 하면 파이썬 부동소수점 수의 근본적인 특성으로 인해 발생하는 정밀도 손실을 막을 수 있음
- 둘째, int나 float 인스턴스를 생성자에게 전달하는 방법. 다음 코드를 보면 결괏값이 다름
~~~Python 
print(Decimal('1.45'))
print(Decimal(1.45))

>>>
1.45
1.4499999999999999555910790149937383830547332763671875
~~~
- `Decimal` 생성자에 정수를 넘기는 경우에는 이런 문제가 발생하지 않음
~~~python
print("456")
print(456)

>>>
456
456
~~~
- 정확한 답이 필요하다면, 좀 더 주의를 기울여서 Decimal 생성자에 str을 넣어라
- 다시 통화료 예제로 돌아가서 연결 비용이 훨씬 저렴한 지역 사이의 짧은 통화도 지원하고 싶음
- 예를 들어 통화 시간은 5초, 통화료는 분당 0.05원임
~~~python
rate = Decimal('0.05')
seconds = Decimal('5')
small_cost = rate * seconds / Decimal(60)
print(small_cost)

>>>
0.004166666666666666666666666667
~~~
- 계산할 값이 너무 작아서 센트 단위로 반올림하면 0이 나옴. 이런 일이 벌어지면 안됨
~~~python
print(round(small_cost, 2))

>>>
0.00
~~~
- 다행히 Decimal 클래스에는 원하는 소수점 이하 자리까지 원하는 방식으로 근삿값을 계산하는 내장함수가 들어있음
- 이 방식은 앞에서 다뤘던 비싼 통화료에 경우에도 잘 작동함
~~~python
from decimal import ROUND_UP
rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(f"반올림 전: {cost} 반올림 후: {rounded}")

>>>
반올림 전: 5.365 반올림 후: 5.37
~~~
- `quantize` 메서드를 이런 방식으로 사용하면 통화 시간이 짧고 요금이 저렴한 통화료도 제대로 처리할 수 있음
~~~python
rounded = small_cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
print(f"반올림 전 {small_cost} , 반올림 후 : {rounded}")

>>>
반올림 전 0.004166666666666666666666666667 , 반올림 후 : 0.01
~~~
- Decima은 고정소수점 수에 대해서는 잘 작동하지만, 여전히 정밀도에 한계가 있음
- 정밀도 제한 없이 유리수를 사용하고 싶다면 `fractions` 내장 모듈에 있는 `Fraction` 클래스를 사용해라

#### 기억해야 할 내용
- 파이썬은 실질적으로 모든 유형의 숫자 값을 표현할 수 있는 내장 타입과 클래스를 제공
- 돈과 관련된 계산 등과 같이 높은 정밀도가 필요하거나 근삿값 계산을 원하는 대로 제어해야 할 때는  
  Decimal 클래스가 이상적임
- 부동소수점 수로 계산한 근사값이 아니라 정확한 답을 계산해야 한다면 Decimal 생성자에 float 인스턴스 대신 str 인스턴스를 넘겨라

### 70-최적화하기 전에 프로파일링을 해라
- 파이썬의 동적인 특성으로 인해 실행 시간 성능이 예상과 달라 놀랄 때가 있음
- 느릴 것으로 예상한 연산이 실제로는 매우 빠르거나 빠를 것으로 예상한 언어 기능이 실제로는 아주 느린 경우가 있음
- 이로 인해 파이썬 프로그램이 느려지는 원인을 명확히 보지 못할 수 있음
- 가장 좋은 접근 방법은 프로그램을 최적화하기 전에 우리의 직관을 무시하고 직접 프로그램 성능을 측정하는 것
- 파이썬은 프로그램의 각 부분이 실행 시간을 얼마나 차지하는지 결정할 수 있게 해주는 프로파일러를 제공
- 프로파일러가 있기 때문에 프로그램에서 가장 문제가 되는 부분을 집중적으로 최적화하고 프로그램에서 속도에 영향을 미치지 않는 부분은 무시할 수 있음
- 예를 들어 프로그램에서 알고리즘이 느린 이유를 알아보고 싶다고 하자. 다음 코드에서 삽입 정렬(insertion sort)를 사용해 데이터 리스트를 정렬하는 함수를 정의함
~~~python
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
~~~
- `insert_sort`와 `insert_value`를 프로파일링 하려면 먼저 난수 데이터 집합을 만들고 프로파일러에 넘길 test 함수를 정의함
~~~python
from random import randint
=
max_size = 10**4
data = [randint(0, max_size) for _ in range(max_size)]
test = lambda : insertion_sort(data)
~~~
- 파이썬에는 두 가지 내장 프로파일러가 있음. 하나는 순수하게 파이썬으로 작성되었고 다른 하나는 C 확장 모듈로 돼 있음
- cProfile 내장 모듈이 더 낫다. 이유는 프로파일 대상 프로그램의 성능에 최소롤 영향을 미치기 때문
- 순수 파이썬 버전은 부가 비용이 많이 들어 결과가 왜곡될 수 있음

#### NOTE
- 파이썬 프로그램을 프로파일링할 때는 외부 시스템 성능이 아니라 코드 자체 성능을 측정하도록 유의해야 함
- 네트워크가 데스크에 있는 자원에 접근하는 함수에 주의해라
- 이런 함수가 사용하는 하부 시스템이 느리면 프로그램 실행 시간이 매우 느려질 수 있음
- 우리의 프로그램이 이런 느린 자원의 응답 시간을 가리기 위하여 캐시를 사용한다면 프로파일링을 시작하기 전에 캐시를 적절히 예열해둬야 함 

- 다음 코드는 cProfile 모듈에 있는 Profile 객체를 인스턴스화하고, 이 인스턴스의 runcall 메서드를 사용해 테스트 함수를 실행함 
~~~python
from cProfile import Profile

profilers = Profile()
profiler.runcall(test)
~~~
- 테스트 함수가 실행되고 나면 pstats 내장 모듈에 있는 Stats 클래스를 사용해 성능 통계를 추출할 수 있음. Stats에 들어 있는 여러 메서드를 사용해 관심 대상 프로파일 정보를 선택하고 정렬하는 방법을 조절해 내가 관심 있는 항목만 표시할 수 있음
~~~python
from cProfile import Profile

profiler = Profile()
profiler.runcall(test)

from pstats import Stats
stats = Stats(profiler)
stats.sort_stats('cumulative') #- 누적 통계
stats.print_stats()

>>>
        20003 function calls in 1.157 seconds
   Ordered by: cumulative time
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    1.157    1.157 <input>:20(<lambda>)
        1    0.003    0.003    1.157    1.157 <input>:1(insertion_sort)
    10000    1.138    0.000    1.154    0.000 <input>:8(insert_value)
     9986    0.016    0.000    0.016    0.000 {method 'insert' of 'list' objects}
       14    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
~~~
- 프로파일러 통계에서 각 열의 의미는 다음과 같음
  - `ncalls`: 프로파일링 기간 동안 함수가 몇 번 호출됐는지 보여줌
  - `tottime`: 프로파일링 기간 동안 대상 함수를 실행하는데 걸린 시간의 합계를 보여줌  
    대상 함수가 다른 함수를 호출한 경우, 이 다른 함수를 실행하는 데 걸린 시간은 제외됨
  - `tottime percall`: 프로파일링 기간 동안 함수가 호출될 때마다 걸린 시간의 평균을 보여줌  
    대상 함수가 다른 함수를 호출한 경우, 이 다른 함수를 실행하기 위해 걸린 시간은 제외됨  
    `tottime`을 `ncalls`로 나눈 값과 같음
  - `cumtime`: 함수를 실행할 때 걸린 누적 시간을 보여줌. 이 시간에는 호출한 다른 함수를 실행하는데 걸린 시간이 모두 포함됨
  - `cumtime percall` : 프로파일링 기간동안 함수가 호출될 때마다 걸린 누적 시간 평균을 보여줌  
    이 시간에는 대상 함수가 호출한 다른 함수를 실행하는 데 걸린 시간이 모두 포함됨. 이 값은 cumtime을 ncall로 나눈 값과 같음
- 앞의 프로파일러 통계 표를 보면, 우리 코드에서 누적 시간으로 CPU를 제일 많이 사용한 함수는 insert_value 함수라는 점을 알 수 있음
- 이 함수를 bisect 내장 모듈을 사용해 다시 구현했음
~~~Python
from bisect import bisect_left

def insert_value(array, value):
    i = bisect_left(array, value)
    array.insert(i, value
~~~
- 프로파일러를 다시 실행해서 새로운 프로파일러 통계 표를 얻음
- 이전의 insert_value 함수에 비해 새로 정의한 함수의 누적 실행 시간이 거의 100배 가까이 줄어듬
~~~python
stats.print_stats()
         30003 function calls in 0.025 seconds
   Ordered by: cumulative time
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.025    0.025 <input>:5(<lambda>)
        1    0.002    0.002    0.025    0.025 <input>:1(insertion_sort)
    10000    0.003    0.000    0.023    0.000 <input>:1(insert_value)
    10000    0.015    0.000    0.015    0.000 {method 'insert' of 'list' objects}
    10000    0.005    0.000    0.005    0.000 {built-in method _bisect.bisect_left}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

~~~
- 전체 프로그램을 프로파일링 했는데, 공통 유틸리티 함수가 대부분의 실행 시간을 차지한다는 사실을 발견할 때도 있음. 프로그램의 여러 부분에서 이런 유틸리티 함수를 호출하기 때문에 프로퍼일러의 디폴트 출력을 사용하면 이런 상황을 제대로 이해하기 어려울 수 있음
- 예를 들어 다음 프로그램에서는 두 함수가 반복적으로 my_utility 함수를 호출함
~~~python
def insert_value(array, value):
    i = bisect_left(array, value)
    array.insert(i, value)

def my_utility(a, b):
    c = 1
    for i in range(100):
        c += a * b

def first_func():
    for _ in range(1000):
        my_utility(4, 5)

def second_func():
    for _ in range(10):
        my_utility(1, 3)

def my_program():
    for _ in range(20):
        first_func()
        second_func()


from cProfile import Profile
profile = Profile()
profile.runcall(my_program)

from pstats import Stats
stats = Stats(profile)
stats.sort_stats('cumulative')
stats.print_stats()

>>>
20242 function calls in 0.114 seconds
Ordered by: cumulative time
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.114    0.114 <input>:19(my_program)
       20    0.003    0.000    0.113    0.006 <input>:11(first_func)
    20200    0.110    0.000    0.110    0.000 <input>:6(my_utility)
       20    0.000    0.000    0.001    0.000 <input>:15(second_func)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
~~~
- `my_utility` 함수가 실행 시간의 대부분을 차지하는 것은 분명하다
- 하지만 이 함수가 왜 이렇게 많이 호출됐는지 즉시 알아보기는 어려움. 프로그램 코드를 살펴보면 my_utility를 호출하는 부분이 여러 곳이라는 사실을 알 수 있지만, 여전히 혼란스러울 뿐
- <b>이런 상황을 처리하고자 파이썬 프로파일러는 각 함수를 프로파일링한 정보에 대해 그 함수를 호출한 함수들이 얼마나 기여했는지를 보여주는 `print_caller` 메서드를 제공함</b>
~~~Python
stats.print_callers()
~~~
- 이 프로파일러 정보 표는 왼쪽에 호출된 함수를, 오른쪽에 그 함수를 호출한 함수를 보여줌
- 다음표를 보면 `first_func`가 `my_utility` 함수를 가장 많이 썼다는 점을 분명히 알 수 있음
~~~python
   Ordered by: cumulative time
Function                                          was called by...
                                                      ncalls  tottime  cumtime
<input>:19(my_program)                            <- 
<input>:11(first_func)                            <-      20    0.003    0.113  <input>:19(my_program)
<input>:6(my_utility)                             <-   20000    0.109    0.109  <input>:11(first_func)
                                                         200    0.001    0.001  <input>:15(second_func)
<input>:15(second_func)                           <-      20    0.000    0.001  <input>:19(my_program)
{method 'disable' of '_lsprof.Profiler' objects}  <- 
~~~
- 이 프로파일러 정보 표는 왼쪽에 호출된 함수를, 오른쪽에 그 함수를 호출한 함수를 보여줌
- 다음 표를 보면 first_func가 my_utility 함수를 가장 많이 썼다는 점을 분명히 알 수 있음

#### 기억해야 할 내용
- 파이썬 프로그램을 느리게 하는 원인이 불분명한 경우가 많으므로 프로그램을 최적화하기 전에 프로파일링하는 것이 중요
- profile 모듈 대신 cProfile 모듈을 사용해라. cProfile이 더 정확한 프로파일링 정보를 제공함
- 함수 호출 트리를 독립적으로 프로파일링하고 싶다면 Profile 객체의 runcall 메서드를 사용하기만 하면 됨
- Stats 객체를 사용하면 프로파일링 정보 중에서 프로그램 성능을 이해하기 위해 살펴봐야 할 부분만 선택해 출력할 수 있음

### 71 생산자-소비자 큐로 deque를 사용하라
- 프로그램을 작성할 때 자주 쓰는 기능으로, 선입선출 queue가 있음
- 프로그래머들은 종종 파이썬 내장 리스트 타입을 FIFO 큐로 쓰곤 함
- 예를 들어 수신된 전자우편을 장기 보관하기 위해 처리하는 프로그램이 있는데, 이 프로그램이 리스트 생산자-소비자 큐로 사용한다고 하자
- 다음 코드는 메세지를 표현하는 클래스를 보여줌
~~~python
class Email:
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.message = message
~~~
- 전자우편을 수신하는 역할을 맡는 함수를 하나 정의하자
- 이 함수는 소켓이나 파일 시스템, 또는 다른 유형의 I/O 시스템을 사용해 전자우편을 받을 수 있음
- 이 함수가 어떻게 구현되었는지는 중요치 않음. 이 함수가 Email 인스턴스를 반환하거나 NoEmailError 예외를 발생시킨다는 인터페이스만 중요함
~~~python
class NotEmailError(Exception):
    pass

def try_receive_email():
    # Email 인스턴스를 하나 반환하거나, # NoEmailError를 발생
~~~
- 생산자 함수는 전자우편을 받아 나중에 소비될 수 있게 큐에 넣음
- 이 함수는 리스트의 append 메서드를 이용해 새 메세지를 큐 맨 뒤에 추가함으로써 이전에 받은 메세지들이 모두 처리된 다음에 처리되게 만듬
~~~python
def produce_emails(queue):
    while True:
        try:
            email = try_receive_email()
        except NotEmailError:
            return
        else:
            queue.append(email)
~~~
- 소비자 함수는 전자우편을 가지고 유용한 일을 수행함. 이 함수는 큐에 대해 `pop(0)`을 호출
~~~python
def consume_one_email(queue):
    if not queue:
        return
    email = queue.pop(0) # 소비자
    print(f"read email: {email}")
~~~
- 마지막으로 각 부분을 하나로 엮어줄 루프 함수가 필요함. 이 함수는 `keep_running` 함수가 False를 반환할 때까지 생산과 소비를 번갈아 반복함
~~~python
def loop(queue, keep_running):
    while keep_running():
        produce_emails(queue)
        consume_one_email(queue)

# 99%확률로 True를 반환
def my_end_func():
    return random.randint(0, 100) > 1

loop([], my_end_func())
~~~
- 어차피 produce_email 안에서 try_receive_email로부터 전자우편을 받는데, 왜 Email을 produce_emails 안에서 처리하지 않을까?(하나의 함수에서 producer-consumer를 동시 처리해도 무방한데, 함수를 두개로 나눈 이유)
- 이 문제는 결국 지연 시간과 단위 시간당 스루풋 사이의 상충 관계로 귀결됨
- 생산자-소비자 큐를 사용할 때는 가능하면 빨리 원소를 수집하길 원하므로 새로운 원소를 받아들이는 지연 시간을 최소화하고 싶을 때가 많음
- 소비자는 큐에 쌓인 원소를 일정한 스루풋(앞의 예제에서는 루프를 한 번 돌때마다 하나씩)으로 처리함
- 이렇게 하면 종단점 사이(end-to-end)의 지연 시간을 희생함으로써 안정적인 성능 프로파일과 일관성 있는 스루풋을 달성할 수 있음
- 이와 같은 생산자-소비자 문제는 큐로 리스트를 사용해도 어느 정도까지는 코드가 잘 동작하지만, 크기(cardinality, 리스트 안에 있는 원소 개수)가 늘어나면 리스트 타입의 성능은 선형보다 더 나빠짐
- 리스트를 FIFO 큐로 사용할 때 성능이 어떤지 분석하기 위해 timeit 내장 모듈을 사용해 마이크로 벤치마크를 수행할 수 있음
~~~python
import timeit

def print_results(count, tests):
    avg_iteration = sum(tests) / len(tests)
    print(f'\n원소 수: {count:>5,} 걸린시간: {avg_iteration:.6f}초')
    return count, avg_iteration

def list_append_benchmark(count):
    def run(queue):
        for i in range(count):
            queue.append(i)

    #- 1000번 run(queue) 수행시 걸린 시간을 list로 return 해줌      
    tests = timeit.repeat(
        setup='queue = []',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)
~~~
- 여러 크기의 리스트를 사용해 이 벤치마크 함수를 실행하면 데이터 크기와 성능의 관계를 비교할 수 있음
~~~python
def print_delta(before, after):
    before_count, before_time = before
    after_count, after_time = after
    growth = 1 + (after_count - before_count) / before_count
    slowdown = 1 + (after_time - before_time) / before_time
    print(f'데이터 크기 {growth:>4.1f}배, 걸린 시간 {slowdown:>4.1f}배')

baseline = list_append_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    comparison = list_append_benchmark(count)
    print_delta(baseline, comparison)
~~~
- 이 결과는 리스트 타입에 이쓴 append 메서드가 거의 상수 시간이 걸린다는 것을 보여줌
- 따라서 데이터 크기가 커짐에 따라 큐에 데이터를 넣는 데 걸리는 전체 시간이 선형적으로 늘어남
- 내부적으로 원소가 추가됨에 따라 리스트 타입이 원소를 저장하기 위해 가용량을 늘리는 부가 비용이 약간 발생하지만 이 비용은 매우 적고 append를 반복 호출하므로 여러 append 호출이 이 비용을 분할상환해줌   
- 다음 코드는 큐의 맨 앞에서 원소를 제거하는 pop(0)를 벤치마크함
~~~python
import collections

def deque_append_benchmark(count):
    def prepare():
        return collections.deque()

    def run(queue):
        for i in range(count):
            queue.append(i)

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)
    return print_results(count, tests)

baseline = deque_append_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    comparison = deque_append_benchmark(count)
    print_delta(baseline, comparison)
~~~
- 놀랍게도, 리스트에서 pop(0)를 사용해 웤소를 큐에서 빼내는데 걸리는 시간이 큐 길이가 늘어남에 따라 큐 길이의 제곱에 비례해 늘어나는 것을 볼 수 있음
- 이유는 pop(0)을 하면 리스트의 모든 남은 원소를 제 위치로 옮겨야 해서, 결과적으로 전체 리스트 내용을 다시 제대입하기 때문
- 리스트의 모든 원소에 대해 pop(0)을 호출하므로 대략 len(queue) * len(queue) 연산을 수행해야 모든 대기열 원소를 소비할 수 있음
- 데이터가 커지면 이러한 코드는 원할히 작동할 수 없음
- 파이썬 collections 내장 모듈에는 deque 클래스가 들어있음. deque는 양방향 큐 구현이며 '데크'라고 읽음
- 데크의 시작과 끝 지점에 원소를 넣거나 빼는 데는 상수 시간이 걸림
- 따라서 데크는 FIFO 큐를 구현할 때 이상적임
- 다른 벤치마크를 실행해보면 append 성능이 리스트를 사용하는 경우와 거의 비슷하다는 사실을 알 수 있음
~~~Python
def dequeue_popleft_benchmark(count):
    def prepare():
        return collections.deque(range(count))

    def run(queue):
        while queue:
            queue.popleft()

    tests = timeit.repeat(
        setup='queue = prepare()',
        stmt='run(queue)',
        globals=locals(),
        repeat=1000,
        number=1)

    return print_results(count, tests)

baseline = dequeue_popleft_benchmark(500)
for count in (1_000, 2_000, 3_000, 4_000, 5_000):
    comparison = dequeue_popleft_benchmark(count)
    print_delta(baseline, comparison)
~~~

### 기억해야 할 내용
- 생산자는 append를 호출해 원소를 추가하고 소비자는 pop(0)을 사용해 원소를 받게 만들면 리스트 타입을 FIFO 큐로 사용할 수 있음. 하지만 리스트를 FIFO 큐로 사용하면, 큐 길이가 늘어남에 따라 pop(0)의 성능이 선형보다 더 크게 나빠지기 때문에 문제가 될 수 있음
- collections 내장 모듈에 있는 deque 클래스는 큐 길이와 상관없이 상수 시간만에 append와 popleft를 수행하기 때문에 FIFO 큐 구현에 이상적임

### 72-정렬된 시퀀스를 검색할 떄에는 bisect를 사용해라
- 보통 프로그램이 구체적으로 처리해야 하는 정보의 유형이 무엇이든, 리스트에서 index 함수를 사용해 특정 값을 찾아내려면 리스트 길이에 선형으로 비례하는 시간이 필요
~~~python
data = list(range(10**5))
index = data.index(91234)
assert index == 91234
~~~
- 찾는 값이 리스트 안에 들어있는지 모른다면, 원하는 값이 같거나 그보다 큰 값의 인덱스 중 가장 작은 인덱스를 찾고 싶을 것임
- 가장 간단한 방법은 리스트를 앞에서부터 선형으로 읽으면서 각 원소를 찾는 값과 비교하는 것
~~~Python
data = list(range(10**5))
index = data.index(91234)
assert index == 91234

def find_closest(sequence, goal):
    for index, value in enumerate(sequence):
        if goal < value:
            return index
    raise ValueError(f"범위를 벗어남: {goal}")

index = find_closest(data, 91234.56)
assert index == 91235
~~~
- 파이썬 내장 `bisect` 모듈은 순서가 정해져 있는 리스트에 대해 이런 유형의 검사를 효과적으로 수행함
- `bisect_left` 함수를 사용하면 정렬된 원소로 이뤄진 시퀀스에 대해 이진 검색을 효율적으로 수행할 수 있음
- `bisect_left`가 반환하는 인덱스는 리스트에 찾는 값의 원소가 존재하는 경우 이 원소의 인덱스이며, 리스트에 찾는 값의 원소가 존재하지 않는 경우 정렬 순서상 해당 값을 삽입해야 할 자리의 인덱스
~~~python
from bisect import bisect_left

index = bisect_left(data, 91234)
assert index == 91234

index = bisect_left(data, 91234.56)
assert index == 91235

index = bisect_left(data, 91234.23)
assert index == 91235
~~~
- `bisect` 모듈이 사용하는 이진 검색 알고리즘의 복잡도는 로그 복잡도임
- 이는 길이가 100만인 리스트를 bisect로 검색하는 데 걸리는 시간과 길이가 20인 리스트를 list.index로 선형 검색하는데 걸리는 시간이 거의 같다는 뜻임(math.log(10**6) == 19.93)
- timeit을 사용해 마이크로 벤치마크를 수행해서 bisect를 사용하면 실제 성능이 향상되는지 검증할 수 있음
~~~python
import random
import timeit

size = 10 ** 5
iterations = 1000

data = list(range(size))
to_lookup = [random.randint(0, size)
             for _ in range(iterations)]

def run_linear(data, to_lookup):
    for index in to_lookup:
        data.index(index)

def run_bisect(data, to_lookup):
    for index in to_lookup:
        bisect_left(data, index)

baseline = timeit.timeit(
    stmt='run_linear(data, to_lookup)',
    globals=globals(),
    number=10)
print(f'선형 검색: {baseline:.6f}초')

comparison = timeit.timeit(
    stmt='run_bisect(data, to_lookup)',
    globals=globals(),
    number=10)
print(f'이진 검색: {comparison:.6f}초')

slowdown = 1 + ((baseline - comparison) / comparison)
print(f'선형 검색이 {slowdown:.1f}배 더 걸림')

>>>
선형 검색: 6.426039초
이진 검색: 0.006127초
선형 검색이 1048.8배 더 걸림
~~~
- `bisect`에서 가장 좋은 점은 리스트 타입뿐만 아니라 시퀀스처럼 작동하는 모든 파이썬 객체에 대해 bisect 모듈의 기능을 사용할 수 있다는 점임
- `bisect` 모듈은 더 고급스런 기능도 제공함

#### 기억해야 할 내용
- 리스트에 들어 있는 정렬된 데이터를 검색할 때 index 메서드를 사용하거나 for 루프와 맹목적인 비교를 하면 선형 시간이 걸림
- bisect 내장 모듈의 bisect_left 함수는 정렬된 리스트에서 원하는 값을 찾는데 로그 시간이 걸림. 따라서 접근 방법보다 훨씬 빠름

### 73- 우선순위 큐로 heapq를 사용하는 방법을 알아두라
- 때로는 프로그램에서 원소를 받은 순서가 아닌 원소 간의 상대적인 중요도에 따라 원소를 정렬해야 하는 경우가 있음
- 이런 목적에는 우선순위 큐가 적합함
- 예를 들어 도서관에서 대출한 책을 관리하는 프로그램을 작성한다고 하자. 회원 중에는 계속 신간만 대출하는 사람이 있고, 대출한 책을 제시간에 반납하는 사람이 있으며, 연체된 책이 있음을 통지해야 하는 사람이 있음
- 다음은 대출한 책을 표현하는 클래스임 
~~~python
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
~~~
- 만기일(due_date)를 넘긴 경우에는 연체 사실을 통지하는 메세지를 보내는 시스템이 필요
- 안타깝지만 책의 최대 대출 기간이 얼마나 최근에 발간된 책인지, 얼마나 유명한 책인지 등의 요소에 따라 달라지므로, 이 경우에는 FIFO 큐를 사용할 수 없음
- 예를 들어 오늘 대출한 책이 내일 대출한 책보다 만기일이 더 늦을 수 있음. 당므 코드에서는 표준 리스트를 사용하고 새로운 Book이 도착할 떄마다 원소를 정렬해서 이런 기능을 구현함
~~~python
def add_book(queue, book):
    queue.append(book)
    queue.sort(key=lambda x: x.due_date, reverse=True)

queue = []
add_book(queue, Book('돈키호테', '2020-06-07'))
add_book(queue, Book('프랑켄슈타인', '2020-06-05'))
add_book(queue, Book('레미제라블', '2020-06-08'))
add_book(queue, Book('전쟁과 평화', '2020-06-03'))
~~~
- 대출한 책의 목록에서는 책이 항상 정렬돼 있다고 가정하면, 연체된 책을 검사하기 이해 리스트의 마지막 원소를 검사하는 것 뿐
- 다음 코드는 리스트에서 연쳬된 책이 있으면 그런 책을 한 권 찾아 큐에서 제거하고 돌려주는 함수를 정의
~~~python
class NoOverdueBooks(Exception):
    pass

def next_overdue_book(queue, now):
    if queue:
        book = queue[-1]
        if book.due_date < now:
            queue.pop()
            return book
    raise NoOverdueBooks
~~~
- 이 함수를 반복적으로 호출해서 연체된 책들을 찾고, 연체 기간이 가장 긴 책부터 짧은 책 순서로 회원들에게 통지할 수 있음
~~~python
now = '2020-06-10'
found = next_overdue_book(queue, now)
print(found.title)

found = next_overdue_book(queue, now)
print(found.title)

>>>
전쟁과 평화
프랑켄슈타인
~~~
- 책이 만기일 이전에 반환되면, 리스트에서 반납된 Book을 제거해 연체 통지가 예정된 책 목록에서 책을 제거할 수 있음
~~~python

def return_book(queue, book):
    queue.remove(book)

queue = []
book = Book('보물섬', '2020-06-04')

add_book(queue, book)
print('반납 전', [x.title for x in queue])

return_book(queue, book)
print('반납 후', [x.title for x in queue])

>>>
반납 전 ['보물섬']
반납 후 []
~~~
- 그리고 모든 책이 반납됐는지 확인하고 나면 return_books 함수는 정해진 예외를 발생시킴
~~~python
try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass
else:
    assert False
~~~
- 하지만 이 해결 방법의 계산 복잡도는 이상적이지 않음. 연체된 책을 검사하거나 제거하는 비용은 상수이지만, 책을 추가할 때마다 전체 리스트를 다시 정렬해야 하는 추가 비용이 들어감
- 추가할 책이 `len(queue)`만큼 있다면, 이를 정렬하는 데 드는 비용은 대략 len(queue) * math.log(len(queue)) 이므로, 책을 모두 추가하는데는  len(queue) * len(queue) * math.log(len(queue)) 로 선형보다 더 크게 증가함
- 책이 만기일 이전에 반납되면, 이 책을 큐에서 선형 검색으로 찾은 후 제거해야 함
- 책을 제거하면 리스트에 있는 모든 원소 하나씩을 뒤로 옮겨야 하는데, 이 경우의 비용도 선형보다 더 커짐
- 이러한 문제를 우선순위 큐를 통해 해결할 수 있음. 다행히 파이썬은 원소가 들어 있는 리스트에 대해 우선순위 큐를 효율적으로 구현하는 내장 `heapq` 모듈을 제공함
- heapq에서 heap은 여러 아이템을 유지하되 새로운 원소를 추가하거나 가장 작은 원소를 제거할 때 로그 복잡도가 드는 데이터 구조
- heapq 모듈의 좋은 점은 제대로 작동하는 힙을 어떻게 구현해야 하는지에 대해 우리가 신경쓸 필요가 없다는 점
- 다음 코드는 heapq를 사용해 add_book 함수를 다시 구현한 것
- 큐는 여전히 일반 리스트임. `heappush` 함수는 앞에서 사용한 list.append 호출을 대신함
- 그리고 이 큐에 대해 더이상 `list.sort` 를 호출할 필요가 없음
- 다음 코드 수행시 에러가 발생함
~~~python
from heapq import heappush

def add_book(queue, book):
    heappush(queue, book)

queue = []
add_book(queue, Book('작은 아씨들', '2020-06-05'))
add_book(queue, Book('타임 머신', '2020-05-30'))

>>>
TypeError: '<' not supported between instances of 'Book' and 'Book'
~~~
- 우선순위 큐에 들어갈 원소들이 서로 비교 가능하고 원소 사이에 자연스러운 정렬 순서가 존재해야 heapq 모듈이 제대로 작동할 수 있음
- `functools` 내장 모듈이 제공하는 `total_ordering` 클래스 데코레이터를 사용하고 `__lt__` 특별 메서드를 구현하면 빠르게 Book 클래스에 비교 가능과 자연스러운 정렬 순서를 제공할 수 있음
~~~python
import functools

@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date

    def __lt__(self, other):
        return self.due_date < other.due_date
~~~
- 이제는 `heapq.heappush` 함수를 사용해도 아무 문제없이 책을 우선순위 큐에 등록할 수 있음
~~~python
queue = []
add_book(queue, Book('돈키호테', '2020-06-07'))
add_book(queue, Book('프랑켄슈타인', '2020-06-05'))
add_book(queue, Book('레미제라블', '2020-06-08'))
add_book(queue, Book('전쟁과 평화', '2020-06-03'))
~~~
- 다른 방법으로, 순서와 관계없이 모든 책이 들어있는 리스트를 만들고 리스트의 sort 메서드를 사용해 힙을 만들 수 있음
~~~python
queue = [
Book('돈키호테', '2020-06-07'),
Book('프랑켄슈타인', '2020-06-05'),
Book('레미제라블', '2020-06-08'),
Book('전쟁과 평화', '2020-06-03'),
]

queue.sort()
~~~
- 또는 `heapq.heapify` 함수를 사용하면 선형 시간에 힙을 만들 수 있음
~~~Python
from heapq import heapify

queue = [
    Book('돈키호테', '2020-06-07'),
    Book('프랑켄슈타인', '2020-06-05'),
    Book('레미제라블', '2020-06-08'),
    Book('전쟁과 평화', '2020-06-03'),
]
heapify(queue)
~~~
- 대출 만기를 넘긴 책을 검사하려면 리스트의 마지막 원소가 아니라 첫 번째 원소를 살펴본 다음, `list.pop`함수 대신에 `heapq.heappop` 함수를 사용함
~~~python
from heapq import heappop
def next_overdue_book(queue, now):
    if queue:
        book = queue[0]
        if book.due_date < now:
            heappop(queue)
            return book
    raise NoOverdueBooks
~~~
- 이제 현재 시간보다 만기가 이른 책을 모두 찾아 제거할 수 있음
~~~python
now = '2020-06-02'
book = next_overdue_book(queue, now)
print(book.title)

book = next_overdue_book(queue, now)
print(book.title)

try:
    next_overdue_book(queue, now)
except NoOverdueBooks:
    pass
else:
    assert False
~~~
- `heapq` 구현에 대해 한 가지 의문이 남아있는데, 제시간에 반납된 책은 어떻게 처리해야 할까?
- 해결 방법은 우선순위 큐에서 책을 절대 제거하지 않는 것
- 만기일이 되면 정상 반납된 책이 우선순위 큐의 맨 앞에 있으므로, 큐에서 연체된 책을 처리할 때 이미 반환된 책은 그냥 무시하면 됨
- 다음 코드에서는 책의 반환 상태를 추적하고자 새로운 필드를 추가해 이런 기능을 구현함
~~~python
@functools.total_ordering
class Book:
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date
        self.returned = False
~~~
- 그 후 `next_overdue_book` 함수를 변경해 이미 반환된 책을 무시하게 만듬
~~~python
def next_overdue_book(queue, now):
    while queue:
        book = queue[0]
        if book.returned:
            heappop(queue)
            continue
        
        if book.due_date < now:
            heappop(queue)
            return book
        
        break
    
    raise NoOverdueBooks
~~~
- 이 접근 방법을 택하면 책을 반납할 때  우선순위 큐를 변경할 필요가 없어지므로 return_book 함수가 아주 빨라짐
~~~python
def return_book(queue, book):
    book.returned = True
~~~
- 이 해법의 단점은 도서관의 모든 책이 대출된 후 만기 이전에 반환된 경우 가장 빠른 만기일이 될 때까지는 힙의 크기가 최대 크기에서 줄어들지 않는다는 것
- heapq를 사용하면 힙 연산은 빨라지지만, 이런 저장소 부가 비용으로 인해 메모리 사용량이 크게 늘어날 수 있음
- 이런 단점에도 불구하고 튼튼한 시스템을 구축하려고 한다면 ,최악의 경우를 가정하고 계획을 세워야 함
- 따라서 무슨 이유로든 대출된 모든 책이 연체될 수도 있다고 가정해야 함
- 이런 메모리 비용은 우리가 계획을 세울 때 제약을 추가함으로써 완화시킬 방법을 고안해야 하는 설계상의 고려 사항임

#### 기억해야 할 내용
- 우선순위 큐를 사용하면 선입선출이 아니라 원소의 중요도에 따라 처리할 수 있음
- 리스트 연산을 사용해 우선순위를 구현하면 큐 크기가 커짐에 따라 프로그램의 성능이 선형보다 더 빠르게 나빠짐
- `heapq` 내장 모듈은 효율적으로 규모 확장이 가능한 우선순위 큐를 구현하는 데 필요한 모든 기능을 제공함
- `heapq`를 사용하려면 우선순위를 부여하려는 자연스러운 순서를 가져야 함. 이는 원소를 표현하는 클래스에 대해 `__lt__`와 같은 특별 메서드가 있어야 함

### 74- bytes를 복사하지 않고 다루려면 memoryview와 bytearray를 사용해라
- 파이썬이 CPU 위주의 계산 작업을 추가적인 노력없이 병렬화해줄 수는 없지만, 스루풋이 높은 병렬 I/O를 다양한 방식으로 지원할 수는 있음
- 그럼에도 불구하고 이런 I/O 도구를 잘못 사용해서 파이썬 언어가 I/O 위주의 부하에 대해서도 너무 느리다는 결론으로 이어지기가 쉬움
- 예를 들어 TV나 영화를 모두 내려받지 않고도 시청할 수 있게 네트워크를 통해 스트리밍하는 미디어 서버를 만든다고 하자
- 이런 시스템의 기능으로 플레이 중인 비디오를 플레이 시간상 앞이나 뒤로 이동해서 일부를 건너뛰거나 반복하는 기능이 있음
- 클라이언트 프로그램에서 사용자가 선택한 시간에 대응하는 데이터 덩어리를 서버에 요청해 이 기능을 구현할 수 있음 
~~~python
def timecode_to_index(video_id, timecode):
    # video data의 offset을 반환


def request_chunk(video_id, byte_offset, size):
    #- video id에 대한 비디오 데이터 중 바이트 오프셋에서부터 size만큼 반환

video_id = ...
timecode = '01:09:14:28'
byte_offset = timecode_to_index(video_id, timecode)
size = 20 * 1024 * 1024 #- 20MB
video_data = request_chunk(video_id, byte_offset, size)
~~~
- `request_chunk` 요청을 받아 요청에 해당하는 20MB의 데이터를 돌려주는 서버 측 핸들러를 어떻게 구현할 수 있을까? 
- 이 예제의 경우 서버의 명령과 제어 부분은 이미 만들어져 있다고 가정하자
- 여기서는 요청받은 데이터 덩어리를 메모리 캐시에 들어 있는 수 기가바이트 크기의 비디오 정보에서 꺼낸 후 소켓을 통해 클라리언트에게 돌려주는 과정에 집중
- 다음은 서버 핸들러를 구현한 코드를 보여줌
~~~Python
socket = ...             #- 클라이언트가 연결한 소켓
video_data = ...         #- video_id에 해당하는 데이터가 들어 있는 bytes 
byte_offset = ...        #- 요청받은 시작 위치
size = 20 * 1024 * 1024  #- 요청받은 데이터 크기

chunk = video_data[byte_offset:byte_offset+size]
socket.send(chunk)
~~~
- 이 코드의 지연 시간과 스루풋은 video_data에서 20MB의 비디오 덩어리를 가져오는 데 걸리는 시간과 이 데이터를 클라이언트에게 송신하는 데 걸리는 시간이라는 두 가지 요인에 의해 결정됨
- 소켓이 무한히 빠르다고 가정하면, 이 코드의 지연시간과 스루풋은 데이터 덩어리를 가져와 만드는 데 걸리는 시간에 따라 결정됨
- 따라서 최대 성능을 알아보려면 소켓 송신 부분은 무시하고 데이터 덩어리를 만들기 위해 bytes 인스턴스를 슬라이싱하는 방법에 걸리는 시간을 측정하면 됨
- timeit을 이용한 마이크로 벤치마크를 통해 이 방법의 특성을 알아볼 수 있음
~~~Python
import timeit

def run_test():
    chunk = video_data[byte_offset:byte_offset+size]

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f"{result:0.9f}초")

>>>
0.004925669초
~~~
- 클라이언트에게 보낼 20MB의 슬라이스를 꺼내는 데 대략 5밀리초가 걸림
- 이는 우리 서버 최대 전체 스루풋이 이론적으로 20MB / 5밀리초 = 7.3GB/초라는 뜻임
- 이 보다 빨리 메모리에서 비디오 데이터를 꺼내올 수는 없음
- 이 서버에서 병렬로 데이터 덩어리를 요청할 수 있는 클라이언트의 최대 개수는 1 CPU - 초 / 5밀리초 = 200임(1초동안 멀티스레드로 처리할 수 있는 클라이언트 개수가 200개)
- 이 개수는 `asyncio` 내장 모듈 같은 도구가 지원할 수 있는 수만 건의 동시 접속에 비하면 아주 작음
- <b>문제는 기반 데이터를 bytes 인스턴스로 슬라이싱하려면 메모리를 복사해야 하는데, 이 과정이 CPU 시간을 점유한다는 점임</b>
- 이 코드를 더 잘 작성하는 방법은 파이썬이 제공하는 `memoryview` 내장 타입을 사용하는 것
- memoryview는 CPython의 고성능 버퍼 프로토콜을 프로그램에 노출시켜줌
- 버퍼 프로토콜은 런타입과 C 확장이 bytes와 같은 객체를 통하지 않고 하부 데이터 버퍼에 접근할 수 있게 해주는 저수준 C API임
- memoryview 인스턴스의 가장 좋은 점은 <b>슬라이싱을 하면 데이터를 복사하지 않고 새로운 memoryview 인스턴스를 만들어 준다는 점</b>
- 다음 코드는 bytes 인스턴스를 둘러싸는 memoryview를 만들고, 이 memoryview의 슬라이스를 살펴봄
~~~python
data = '동해물과 abc 백두산이 마르고 닳도록'.encode('utf8')
view = memoryview(data)
chunk = view[12:19]
print(chunk)
print('크기:', chunk.nbytes)
print("뷰의 데이터:", chunk.tobytes())
print("내부 데이터: ", chunk.obj)

>>>
<memory at 0x7fd5891221f0>
크기: 7
뷰의 데이터: b' abc \xeb\xb0'
내부 데이터:  b'\xeb\x8f\x99\xed\x95\xb4\xeb\xac\xbc\xea\xb3\xbc abc \xeb\xb0\xb1\xeb\x91\x90\xec\x82\xb0\xec\x9d\xb4 \xeb\xa7\x88\xeb\xa5\xb4\xea\xb3\xa0 \xeb\x8b\xb3\xeb\x8f\x84\xeb\xa1\x9d'
~~~
- 복사가 없는(zero-copy) 연산을 활성화함으로써 memoryview는 Numpy 같은 수치 계산 확장이나 이 예제 프로그램 같은 I/O 위주 프로그램이 커다란 메모리를 빠르게 처리해야 하는 경우에 성능을 엄청나게 향상 시킬 수 있음
- 다음은 앞의 예제를 `memoryview`를 사용해 마이크로 벤치마크를 이용해 성능을 측정한 결과임
~~~python
video_view = memoryview(video_data)
def run_test():
    chunk = video_view[byte_offset:byte_offset+size]

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

print(f"{result:0.9f} 초")

>>>
0.000000250초
~~
- 결과는 250나노초임. 이제 서버의 이론적인 최대 스루풋은 20MB/250나노초 = 164TB/초
- 병렬 클라이언트의 경우 이론적으로 최대 1 CPU - 초 / 250나노초 = 400만개까지 지원 가능
- 성능 개선으로 인해 이제 프로그램 성능은 CPU의 성능이 아니라 클라이언트 소켓 연결의 성능에 따라 전적으로 제한됨
- 이제 데이터가 반대 방향으로 흘러야 한다고 생각해보자
- 일부 클라이언트가 여러 사용자게에 방송을 하기 위해 서버로 라이브 비디오 스트림을 보내야 함
- 그렇게 하려면 사용자가 가장 최근에 보낸 비디오 데이터를 캐시에 넣고 다른 클라이언트가 캐시에 있는 비디오 데이터를 읽게 해야 함
- 다음은 클라이언트가 서버로 1MB 데이터를 새로 보낸 경우를 구현한 코드임
~~~python
socket = ...
video_cache = ...
byte_offset = ...
size = 1024 * 1024
chunk = socket.recv(size)
video_view = memoryview(video_cache)
before = video_view[:byte_offset]
after = video_view[byte_offset + size:]
new_cache = b''.join([before, chunk, after])
~~~
- socket.recv 메서드는 bytes 인스턴스를 반환함. 간단한 슬라이스 연산과 bytes.join 메서드를 사용하면 현재의 `bytes_offset`에 있는 기존 캐시 데이터를 새로운 데이터로 스플라이스(splice)할 수 있음
- 이런 연산의 성능을 확인하기 위해 또 다른 마이크로 벤치마크를 실행할 수 있음
- 여기서는 가짜 소켓을 사용하기 때문에 이 성능 테스트는 I/O 상호작용을 테스트하지 않고 메모리 연산의 성능만 테스트함
~~~python
def run_test():
    chunk = socket.recv(size)
    before = video_view[:byte_offset]
    after = video_view[byte_offset + size:]
    new_cache = b''.join([before, chunk, after])

timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

>>>
0.033520550초
~~~
- 1MB 데이터를 받아 비디오 캐시를 갱신하는데 33밀리초가 걸림. 이는 수신 시 최대 스루풋이 1MB / 33밀리초 = 31MB/초이고, 비디오를 이런 방식으로 스트리밍해 방송하는 클라이언트는 최대 31MB / 1MB = 31개로 제한된다는 뜻
- 이런 구조는 확장성이 없음
- 이런 코드를 작성하는 더 나은 방법은 파이썬 내장 `bytearray` 타입과 `memoryview`를 같이 사용하는 것
- bytes 인스턴스의 한 가지 단점은 읽기 전용이라 인덱스를 사용해 변경이 불가능하다는 점임
~~~python
my_bytes = b'hello'
my_bytes[0] = b'\x79'

>>>
TypeError: 'bytes' object does not support item assignment
~~~
- <b>bytearray 타입은 bytes에서 원하는 있는 값을 바꿀 수 있는 가변(mutable) 버전과 같음</b>
- 인덱스를 사용해 bytearray의 내용을 바꿀 때는 바이트 문자열(한 글자짜리)이 아니라 정수를 대입함
~~~python
my_array = bytearray('hello 안녕'.encode('utf8')) #- b"가 아니라# " 문자열
my_array[0] = 0x79
print(my_array)

>>>
bytearray(b'yello \xec\x95\x88\xeb\x85\x95')
~~~
- bytearray도 memoryview를 통해 감쌀 수 있음. memoryview를 슬라이싱해서 객체를 만들고, 이 객체에 데이터를 대입하면 하부의 bytearray 버퍼에 데이터가 대입됨
- 이런 방법을 사용하면, 앞에서 bytes 인스턴스를 스플라이스해 클라이언트로부터 받은 데이터를 덧붙였던 것과 달리 데이터 복사에 드는 비용이 사라짐
~~~python
my_array = bytearray('row, row, row, your boat'.encode('utf8'))
my_view = memoryview(my_array)
write_view = my_view[3:13]
write_view[:] = b'-10 bytes-'
print(my_array)

>>>
bytearray(b'row-10 bytes-, your boat')
~~~
- `socket.recv_into` 나 `RawIOBase.readinto`와 같은 여러 파이썬 라이브러리 메서드가 버퍼 프로토콜을 사용해 데이터를 빠르게 받아들이거나 읽을 수 있음
- 이런 메서드를 사용하면 새로 메모리를 할당하고 데이터를 복사할 필요가 없어짐
- 다음 코드는 스플라이스를 하지 않고 `socket.recv_into`와 `memoryview` 슬라이스를 사용해 하부의 `bytearray`에 데이터를 수신함
~~~python
video_array = bytearray(video_cache)
write_view = memoryview(video_array)
chunk = write_view[byte_offset: byte_offset + size]

socket.recv_into(chunk)
~~~
- 마이크로 벤치마크를 실행해 이런 방법과 앞에서 본 `socket.recv`를 사용하는 방법의 성능을 비교할 수 있음
~~~python
def run_test():
    chunk = write_view[byte_offset:byte_offset + size]
    socket.recv_into(chunk)

result = timeit.timeit(
    stmt='run_test()',
    globals=globals(),
    number=100) / 100

>>>
0.000033925 초
~~~
- 1MB 데이터를 받는 데 33마이크로초가 걸림. 이는 이 서버의 최대 스루풋이 1MB / 33마이크로초 = 31GB/초이고, 최대 31GB / 1MB = 31,000개의 클라이언트를 병렬로 처리할 수 있다는 의미 
- 이런 규모 확장성이 바로 우리가 원하던 확장성임!

#### 기억해야 할 내용
- `memoryview` 내장 타입은 객체의 슬라이스에 대해 파이썬 고성능 버퍼 프로토콜로 읽고 쓰기를 지원하는, 복사가 없는 인터페이스를 제공
- `bytearray` 내장 타입은 복사가 없는 읽기 함수(`socket.recv_from`)에 사용할 수 있는 bytes와 비슷한 변경 가능한 타입을 제공
- `memoryview`로 bytearray를 감싸면 복사에 따른 비용을 추가 부담하지 않고도 수신받은 데이터를 버퍼에서 원하는 위치에 스플라이스 할 수 있음

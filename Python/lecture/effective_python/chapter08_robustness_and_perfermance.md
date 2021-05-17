## chapter08 강건성과 성능
- 유용한 파이썬 프로그램을 만들었다면, 오류가 발생해도 문제 없도록 production화 해야함
- 예상치 못한 상황을 만나도 프로그램을 신뢰할 수 있도록 만드는 것은 프로그램을 제대로 작동시키는 것 만큼이나 중요!
- 파이썬은 프로그램을 더 강화시켜 다양한 상황에서 프로글맹르 강건하게 만드는 데 도움이 되는 다양한 기능과 모듈을 내장하고 있음
- 강건성에는 규모 확장성과 성능이라는 차원이 포함됨. 알고리즘 복잡도나 다른 계산 부가 비용으로 인해 아주 큰 데이터를 처리하는 파이썬 프로그램이 전체적으로 느려지는 경우가 자주 있음
- 다행히 파이썬은 최소의 노력으로 고성능을 달성할 수 있도록 다양한 데이터 구조와 알고리즘을 제공함

### 65- try/except/finally의 각 블록을 잘 활용해라
- 파이썬에서 예외를 처리하는 과정은 try/except/else/finally 라는 네 블록에 해당됨
- 전체 복합문에서 각 블록은 서로 다른 목적에 쓰이며, 다양하게 조합하면 유용함

#### finally 블록
- 예외를 호출 스택의 위(함수 자신을 호출한 함수 쪽)로 전달해야 하지만, 예외가 발생하더라도 정리 코드를 실행해야 한다면 `try/finally`를 사용해라
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
import json

def load_json_key(data, key):
    try:
        print("* JSON 데이터 읽기")
        result_dict = json.loads(data) # ValueError가 발생할 수 있음
    except ValueError as e:
        print("ValueError 처리")
        raise KeyError(key) from e
    else:
        print("* 키 검색")
        return result_dict[key]        # keyError 발생 가능

assert load_json_key('{"foo":"bar"}', 'foo') == 'bar'

load_json_key('{"foo": bad payload', 'foo')
load_json_key('{"foo": "bar"}', '존재하지 않음')

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
        handle.seek(0)
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
        yield
    finally:
        logger.setLevel(old_level)
~~~
- yield 식은 with 블록의 내용이 실행되는 부분을 지정함
- `with` 블록안에서 발생한 예외는 어떤 것이든 `yield` 식에 의해 다시 발생되기 때문에 이 예외의 도우미 함수(이 경우는 debug_logging)안에서 잡아낼 수 있음
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

###
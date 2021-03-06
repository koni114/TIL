# python 에서의 동시성관리 내용 정리
## Python 표준 함수를 asyncio에서 비동기로 호출하는 방법
- 파이썬 3.4에서 `asyncio` 가 추가되어 I/O 바운드된 작업을 단일 스레드에서 비동기로 처리할 수 있는 방법이 생김
- 하지만 대부분의 파이썬 내장 라이브러리 함수들은 코루틴이 아닌 일반 함수들이며, 이들은 모두 블럭킹 방식으로 동작함.  
  즉 asyncio 의 비동기는 실질적으로는 I/O 액세스처럼 CPU가 관여할 필요가 없는 일들에 대해서 "병렬적으로 기다리는" 식으로 동시다발적인 처리의 전체 수행 시간을 줄이는 식으로 동작하는데, 그 중에 이런 블럭킹 함수로 처리되는 과정이 끼어 있다면 수행 시간 단축이 어렵게 됨

### 런루프
- 파이썬에서는 Global Interpreter lock 이라는 기재가 있어 멀티 스레드로 병렬 작업을 처리하더라도 실질적으로 여러 스레드가 동시에 진행되지 못하고 CPU는 한 번에 하나의 스레드만 처리함 
~~~
## 흔히 생각하는 멀티스레드

( -- 은 작업을 수행하는 시간,  ..은 스레드가 중단되는 시간을 의미)
메인스레드 ------------------------------> 진행
스레드 1     생성 -----------------------> 진행
스레드 2           생성 -----------------> 진행

## 실제 파이썬의 멀티 스레드
메인스레드 ------....---...---......-----> 진행
스레드 1    생성 ----.........---........> 진행
스레드 2            생성---......---.....> 진행
~~~
- 위 도식에서 `---` 로 표현된 부분은 스레드가 일을 하는 시간이며, `...`로 표현된 부분은 다른 스레드가 일하는 동안 해당 스레드가 멈춰있는 시간
- 즉 아래/위 두 케이스에서 같은 시간 동안 멀티스레드가 실행되었다고 가정하면 처리된 일의 총 량은 `-`의 개수와 같다고 볼 수 있으며, 파이썬의 멀티스레드는 단일 스레드에서의 작업량과 다를 바가 없는 일을 처리함(오히려 컨텍스트 스위칭에 들어가는 비용이 있기 때문에 더 느림)
- 이 관점에서 생각해볼 것이, `asyncio`는 본래 단일 스레드에서 I/O 작업의 대기 시간이 CPU 사용시간에 포함되지 않도록 여러 코루틴을 옮겨가며 실행하는 것이라는 점. 그리고 멀티 스레드처리에서 `...`에 해당하는 시간이 그냥 다른 스레드를 위해 해당 스레드가 쉬는 것이 아니라 해당 스레드가 I/O 작업을 기다리는 시간으로 만들면 어떠냐는 것임
- 즉 멀티스레드로 분기하여 실행되는 블럭킹 함수 콜 자체를 I/O 작업으로 보고, 이를 기다리는동안 중지하는 비동기 코루틴이 있다면 되지 않을까? 이를 위해 스레드 작업의 상태에 따라 런루프에 시그널을 보내고, 해당 함수 콜 자체를 비동기 코루틴으로 감싸는 처리를 해줘야 하는 데 이는 난이도가 있는 작업
- 이런 기능을 이미 런루프 클래스에서 제공하고 있음. `run_in_executor()` 함수가 이 용도로 사용됨

### 예제
- 이게 실제로 효과가 있는지 확인해보자. 기본 라이브러리에서 네트워크 액세스를 처리하는 `urllib.request.urlopen` 함수를 생각해보자. 이 함수는 비동기 코루틴이 아닌 일반 함수이며, HTTP 요청을 보낸 후 응답을 받을 때까지 블럭되는 함수
- 이 함수를 호출해서 콘텐츠를 받아오는 함수를 하나 작성해보자
~~~python
from urllib.request import urlopen
import time


async def get_url_data(url: str) -> (str, str, str):
    """
        특정 URL 에 요청을 보내 HTML 문서를 문자열로 받음
        URL, 응답텍스트, 포맷팅된 소요시간을 리턴
    :param url: 요청보내고자 하는 URL
    :return: HTML 문서 문자열
    """
    print(f"Request for : {url}")
    s = time.time()
    res = urlopen(url)
    data = res.read().decode()
    return url, data, f"{time.time() - s:.3f}"
~~~
- 몇 개의 URL 집합에 대해서 이 함수를 테스트 해보자
~~~python
async def test_urls(co, urls):
    s = time.time()
    fs = {co(url) for url in urls}
    for f in asyncio.as_completed(fs):
        url, body, t = await f
        print(f"Response from: {url}, {len(body)}Bytes - {f}sec")
    print(f"{time.time() - s:0.3f}sec")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_urls(get_url_data, urls))
~~~
- 이 코드는 비록 코루틴으로 각 URL을 테스트하는 코드를 작성하였지만, `urlopen` 함수 자체가 블럭킹 함수이므로 동시에 실행되는 것이 아니라 하나씩 실행됨
- `print()`하는 지점까지는 번갈아가며 실행되지만 HTTP 통신을 하는 동안은 한 번에 하나씩만 실행되고, 실제 출력되는 결과도 요청을 보낸 순서대로 출력됨
- 다음은 스레드를 사용하여 비동기 코루틴으로 변환하여 실행하는 코드
~~~python
async def get_url_data2(url):
    print(f"Request for: {url}")

    loop = asyncio.get_event_loop()
    s = time.time()
    res = await loop.run_in_executor(None, urlopen, url)
    data = res.read().decode()
    return url, data, f"{time.time() - s: .3f}"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_urls(get_url_data2, urls))
~~~
- 일반 함수호출이 아닌 런루프 + 스레드 조합의 코루틴으로 감싼 호출을 사용함. 실제 완료 시간이 체감상으로 확 줄어드는 것을 볼 수 있음

### 예제 수행 결과 비교
- 비동기 코루틴으로 바꿔서 실행한 경우에 총 수행 시간은 일반 함수 호출을 사용한 것보다 약 절반 이하로 실행됨
- 개별 HTTP 요청에 소요된 시간이 더 짧아지지는 않음
- 전체 수행 시간은 가장 오래걸린 연결 시간보다 약간 큰 값임
- 결과가 출력되는 순서는 요청을 시작한 순서와 다르며, 이는 응답시간이 빠른 순으로 표시됨. 결국 6개의 연결이 동시에 수행되었다가, 먼저 완료된 것 순으로 결과가 출력되었음을 알 수 있음
- 일반 함수 호출모드에서 테스트한 결과에서 총 시간은 개별 연결 시간의 합과 비슷
- 개별 연결에 걸린 시간에 상관없이 출력 순서는 요청 순서와 일치함. 즉 HTTP 통신 자체가 동시에 이루어지지 못하고 순서대로 하나씩 실행된 셈

### 정리
- 런루프 `run_in_executor()`를 사용하면 기존의 표준 함수들도 병렬적으로 동작하는 코루틴으로 완전하게 변환할 수 있음
- 어차피 I/O 대기 시간을 병렬적으로 쉬어버리는 식으로 스케줄링 되기 때문에 GIL의 영향을 우회해서 훌륭하게 전체 수행 시간을 단축할 수 있으며, 기존의 함수를 그대로 쓸 수 있다는 막강한 장점이 있음
- 다만 스레드를 별도로 생성해서 동작하기 때문에 메모리 자원을 보다 많이 사용하게 되는 문제가 있고, 또한 I/O 바운드되는 작업에만 적용할 수 있음
- 예를 들어 CPU를 많이 사용하는 계산이 필요한 소수 검사 등의 연산은 당연히 스레드를 동시에 돌리지 못함
- 물론 이 경우에도 `ProcessPoolExecutor` 를 사용해서 다중 프로세스로 처리하는 방법도 있을 것임

## 파이썬 동시성 프로그래밍
### 동시성(Concurrent)과 병렬성(Parallelism)
- 싱글 코어 CPU에서 여러 개의 thread 를 통해 작업을 수행하는 경우는 동시성에 해당되며, 멀티 코어 CPU에서 여러 개의 thread를 통해 작업하는 경우는 병렬성이 있다고 할 수 있음

### 파이썬에서의 동시성 프로그래밍
- 파이썬에서 동시성 프로그래밍을 하는 방법은 정말 많은데, 가장 쉽게 떠올릴 수 있는 방법은 멀티프로세싱과 멀티스레딩
- 파이썬에서는 GIL 때문에 하나의 프로세스에서 동시에 여러 개의 스레드를 병렬적으로 수행시킬 수 없음  
  즉, 멑티 코어 환경에서 하나의 프로세스는 동시에 여러 개의 코어를 사용할 수 없다는 뜻
- 그래서 만약 수행하고자 하는 작업이 CPU bound job 이고 multi-core CPU 환경인 경우에는 멀티프로세싱을 사용하는 것이 유리
- 이유는 하나의 프로세스 내에서 아무리 여러개의 스레드를 만든다고해도, 하나의 스레드에서 순차적으로 수행하는 것과 비교하여 딱히 성능이 좋아지지 않기 때문. 
- context switching을 생각하면 멀티스레딩 쪽이 오히려 더 느릴 수도 있음. 게다가 여러개의 스레드를 사용하면 메모리 사용량도 많아짐
- 하지만 수행하고자 하는 작업이 I/O bound job이면 얘기가 달라지는데, 어떤 스레드가 I/O를 수행하기 위해 block이 되면 GIL을 반환하게 되고, 그 동안 다른 스레드가 실행될 수 있기 때문
- 물론 복수의 스레드가 복수의 코어에서 병렬적으로 실행될 수 없다는 사실은 변함이 없지만, 하나의 스레드만 사용하여 여러 작업을 동시에 수행하고자 하는 경우에는 이 스레드가 block이 되면 아무런 일도 하지 않게 되기 때문에 이런 경우에는 멀티스레딩을 사용할 가치가 충분히 있는 것임
- 하지만 스레드는 직접 사용하기가 까다로움. race condition 도 발생할 수 있고, 메모리 사용량과 context switching 측면에서도 비용이 비쌈

### 코루틴
- 파이썬에서 동시성 프로그래밍을 할 수 있는 또다른 방법은 코루틴(Coroutine)을 사용하는 것
- 코루틴은 특정 언어에 종속되는 개념이 아닌 general한 개념
- 보통의 프로그램은 함수1에서 함수2를 호출한 경우 함수2를 서브루틴이라고 부름
- 이 때 함수1과 함수2는 종속적인 관계를 갖는다고 볼 수 있음. 함수2에 정의된 일련의 코드가 모두 수행되면 항상 함수1로 실행의 흐름이 돌아가게 됨
- 하지만 코루틴은 서로 종속적인 관계가 아닌 상호 협력적인(cooperative) 관계임  
  코루틴1은 원하는 시점에 코루틴2, 혹은 코루틴3에게 실행의 흐름을 넘겨줄 수 있음
- 그러면 코루틴1은 실행 흐름을 넘겨준 지점에서 멈춰있는 상태가 되고 나중에 언제든지 해당 지점부터 다시 이어서 실행될 수 있는 상태가 됨
- 실행 흐름을 양보(yield)받은 코루틴은 처음 실행되는 거라면 처음부터 실행되고 만약 이전에 코드를 실행하다 멈춰져있는 상태라면 멈춘 지점부터 다시 순차적으로 코드가 실행되기 시작함
- 그리고 마찬가지로 원하는 시점에 다른 코루틴으로 실행 흐름을 넘겨줄 수 있음
- 이것은 한편으로는 스레드와 비슷한데, 다른 코루틴에게 실행의 흐름을 넘겨주는 행위는 스레드간의 컨텍스트 스위칭과 비슷하다고 할 수 있음
- 다만 스레드간의 컨텍스트 스위칭이 발생하는 시점과 다음에 어떤 스레드가 실행될 것인지 결정하는 것은 kernel 영역에서, 즉 OS에 의해 결정되는 반면, 코루틴간에 흐름이 변경되는 지점은 user 영역에서, 즉 개발자가 코드로 명시하게 됨
- 즉 코루틴간의 제어의 흐름을 개발자가 완벽하게 컨트롤 할 수 있다는 뜻  
  (물론 여러 코루틴이 실행되는 스레드가 컨텍스트 스위칭에 의해 실행이 멈춰 그 안에서 수행되던 모든 코루틴의 실행도 함께 멈출 수 있음)
- 이는 preemptive 한 OS의 native thread 와는 대조된다. 게다가 코루틴은 스레드보다 메모리 사용량도 적으며, 컨텍스트 스위칭으로 인한 비용도 없음
- 파이썬에서는 주로 이 코루틴과 이벤트 루프를 함께 사용하여 편리하게 동시성 프로그래밍을 할 수 있게 하는 패키지들이 많음
- 많은 패키지들은 다음과 같이 구현되어 있음
  - 코루틴은 큐 안에 들어가고 이벤트 루프는 큐 안에 있는 코루틴을 하나씩 빼 코드를 실행하다가 비동기 작업이 시작되면 해당 라인에서 멈추어 다시 큐의 뒷부분에 넣는다
  - 만약 큐에서 코루틴을 꺼냈는데 비동기 작업이 종료된 상태라면 결과값을 사용하여 멈췄던 부분부터 다시 코드를 실행함
- 이렇기 때문에 하나의 스레드로도 여러 비동기 작업들을 동시에 수행할 수 있는 것임
- 또한 우리가 원하는 시점에 context switching 없이 다음 코루틴에게 실행권을 양도할 수 있게 됨

### 파이썬에서 코루틴 사용하기
- '1. <b>generator</b>
  - 제너레이터를 코루틴으로 사용할 수 있음
  - generator의 동작 방식을 보면 코루틴의 동작 방식과 동일함
  - 제너레이터 내부에서 yield 키워드를 만날 때마다 실행의 흐름이 generator 를 인자로 next() 함수를 호출한 쪽으로 넘어가면서 값을 뱉음
  - 그리고 언제든지 next() 메소드를 사용하여 generator 의 이전에 멈춘 지점부터 실행하여 다음 yield 문을 만날 때까지 실행됨
  - 파이썬 3.4 부터는 subgenerator 에게 위임하기 위한 문법으로 `yield from`이 추가되었는데 이를 통해 generator 를 활용한 동시성 프로그래밍이 더 편해짐 
- '2. <b>asyncio</b>
  - 파이썬 빌트인 라이브러리인 `asyncio` 와 파이썬 3.5 버전부터 도입된 `async/await` 키워드를 통한 방법 
  - asyncio 는 자체적으로 coroutine과 event loop 를 가지고 있어 이를 통해 동시성 프로그래밍을 지원
  - 동작 원리와 구현 스타일은 전체적으로 generator 방식과 매우 유사

### 파이썬 서버 및 프레임워크의 동시성
- 보통 파이썬으로 프로덕션 수준의 서버를 개발한다면 Flask의 Werkzeug 과 같이 프레임워크에 내장된 WSGI 서버를 사용하기 보다는 uWSGI나 Gunicorn과 같은 별도의 서버를 사용하는 경우가 많음
- gunicorn의 경우는 worker-class 옵션을 통해 각 worker process 가 어떤 방식으로 요청을 처리하게 할 지 설정할 수 있는데, 기본적으로는 하나의 worker process 가 최대 하나의 요청만 동기적으로 처리하게 됨
- worker-class 옵션을 gthread로 설정하여 멀티스레드 기반으로 동작하도록 할 수도 있고, gevent와 같은 비동기 worker를 사용하여 처리하도록 할 수도 있음
- 주의할 점이 있다면 gunicorn 에서 gevent worker 를 사용하고 스크립트 코드상에서는 asyncio를 사용한다면 각자 코루틴과 이벤트 루프의 구현체가 다르기 때문에 둘의 호환을 위한 중간 라이브러리를 추가로 사용하거나 두 곳에서 같은 라이브러리를 사용하도록 통일해야 함
- 애초부터 비동기 프레임워크를 사용할수도 있음. 특히 Sanic 이나 Quart 같은 프레임워크는 플라스크와 사용 방법이 매우 비슷하여 처음 사용하는데도 큰 무리가 없음
- 이들은 비동기 서버를 내장하여 뷰 함수를 작성할 때 `async def`와 같이 정의함
- 이러한 비동기 서버 및 비동기 worker 들은 멀티스레드를 사용하지 않고도 요청을 비동기적으로 처리할 수 있게끔 함

## Python 동시성과 병렬성 문법 - GIL과 Multithreading
### 멀티 스레드, 멀티 프로세스 개념
- Process 는 컴퓨터에서 연속적으로 실행되고 있는 컴퓨터 프로그램이며, 메모리에 올라와 실행되고 있는 독립적인 프로그램 인스턴스
- Thread는 프로세스 내에서 동작되는 여러 실행의 흐름 단위
- 하나의 프로세스 내에서 생성된 thread 끼리 해당 프로세스의 영역을 공유함
- Process는 독립적이며, thread 는 프로세스의 서브넷임
- Process는 각각 독립적인 자원을 가짐. thread는 프로세스의 자원을 공유함. Process는 별도의 Code, Data, Stack, Heap을  
  독립적으로 가지는 반면, Thread는 Stack 만 독립적으로 가지고, Code, Data, Heap 은 서로 공유
- Process는 자신만의 주소 영역을 가짐. Thread는 주소 영역을 공유함
- Process간에는 IPC 기법으로 통신해야하지만 Thread는 필요가 없음

### 멀티 스레드
- 한 개의 단일 어플리케이션을 여러 스레드로 구성 후 작업 처리하는 것을 말함
- 장점 '1. 사용자에 대한 응답성 향상
  - 동시에 독립적으로 처리가 가능한 작업에 대해서 멀티 스레딩으로 처리하면 다른 cpu 코어에서 동시 처리가 가능해지며 응답시간이 짧아질 수 있음
- 장점 '2. 자원 공유의 효율성
  - thread는 하나의 프로세스 내에서 자원 공유가 가능하기 때문에 프로세스의 데이터를 모두 접근 가능
  - 각각의 스레드로 나뉘어져 있다면 IPC 기법과 같이 프로세스간 자원 공유를 위해 번거로운 작업이 필요없음
  - 동시 실행을 위해 6개의 프로세스를 만들면 6개의 프로세스 공간이 필요해짐. 하지만 6개의 스레드를 만들면 1개 프로세스 공간만 있으면 됨
- 단점 '1. 하나의 thread에 문제 발생시, 전체 프로세스가 영향을 받음
- 단점 '2. thread 를 많이 생성하게 되면, Context Switching이 많이 일어나 성능이 저하되기도 함
- 단점 '3. 자원을 공유하기 때문에 deadlock 상태, 디버깅이 어렵고, 단일 프로세스에서 멀티 스레드는 효과가 약하다는 단점을 가지고 있음

### Python의 GIL(Global Interpreter Lock) 이란? 
- python 에서는 멀티 스레드로 코딩을 했어도, 한 타이밍에서는 한 thread 만 python object에 접근하도록 해놓음
- 즉, 단일 스레드만이 Python object 에 접근하게 제한하는 mutex   
  그 이유는 CPython 에서는 메모리 관리가 문제가 생길 때 이를 해결하기 위해 thread safe 한 구조 설정
- 

### 멀티 프로세스
- 한 개의 단일 어플리케이션을 여러 프로세스로 구성 후 작업을 처리하는 것을 말함
- 장점 '1. 한 개의 프로세스 문제 발생은 다른 프로세스에 영향을 주지 않음
- 단점 '1. 복잡한 구현. 복잡한 통신 방식 사용. 오버 헤드 발생 가능성

## 참조
- https://soooprmx.com/python-표준-함수를-asyncio에서-비동기로-호출하는-방법/
- https://sgc109.github.io/2020/11/25/python-and-concurrency/
- https://libertegrace.tistory.com/entry/Python-동시성과-병렬성-문법-Multithreading
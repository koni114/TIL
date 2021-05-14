## chapter07- 동시성과 병렬성
- 동시성(concurrency)란 컴퓨터가 같은 시간에 여러 다른 작업을 처리하는 것처럼 보이는 것을 뜻함
- 예를 들어 CPU 코어가 하나인 컴퓨터에서 운영체제는 유일한 프로세서 코어에서 실행되는 프로그램을 아주 빠르게 변경할 수 있음
- 이렇게 하면 여러 프로그램이 번갈아가며 실행되면서 프로그램이 동시에 수행되는 것 같은 착각을 불러일으킬 수 있음
- 병렬성(parallelism)이란 같은 시간에 여러 다른 작업을 실제로 처리하는 것을 뜻함
- CPU 코어가 여러 개인 컴퓨터는 여러 프로그램을 동시에 실행시킬 수 있음
- 각 CPU 코어는 서로 다른 프로그램의 명령어를 실행하기 때문에 각각의 프로그램이 같은 시점에 앞으로 진행될 수 있음
- 동시 프로그램은 여러 다양한 실행 경로나 다양한 I/O 흐름을 제공할 수 있으므로 문제를 해결하는 과정이 동시에 독립적으로 실행되는 것처럼 보이게 할 수 있음
- 병렬성과 동시성의 가장 큰 차이는 속도이며, 병렬성은 속도가 증가하지만, 동시성은 증가하지 않음
- 파이썬을 사용하면 다양한 스타일로 동시성 프로그램을 쉽게 작성할 수 있음. 스레드(thread)는 상대적으로 적은 양의 동시성을 제공하지만, 코루틴(coroutine)은 수많은 동시성 함수를 사용할 수 있게 해줌
- 파이썬은 시스템 콜(system call), 하위 프로세스(subprocess), C 확장(extension)을 사용해 작업을 병렬로 수행할 수 있음
- 하지만 동시성 파이썬 코드가 실제 병렬적으로 실행되게 만드는 것은 매우 어려움

### 52-자식 프로세스를 관리하기 위해 subprocess를 사용해라
- 파이썬은 실전을 거치면서 자식 프로세스 실행 및 관리 라이브러리가 있음
- 이런 라이브러리는 commandline utility 등과 같은 다양한 다른 도구를 연결하는 좋은 도구가 됨
- 이런 경우 가독성과 유지 보수성을 높이기 위해 스크립트를 파이썬으로 다시 작성하는 것은 자연스러운 선택
- 파이썬이 시작한 자식 프로세스는 서로 병렬적으로 실행되기 때문에 파이썬이 컴퓨터의 모든 CPU 코어를 사용할 수 있고, 그에 따라 프로그램의 throughput을 최대로 높일 수 있음
- 파이썬 자체는 한 CPU에 묶여 있지만, 파이썬을 사용해 CPU를 많이 사용하는 여러 부하(과부하 아님)를 조작하면서 서로 협력하게 조정하기는 쉬움
- 파이썬이 하위 프로세스를 실행하는 방법은 많음(`os.popen`, `os.exec`). 하지만 자식 프로세스를 관리할 때는 `subprocess` 내장 모듈을 사용하는 것이 좋음
- `subprocess` 모듈을 사용하면 하위 프로세스를 쉽게 실행할 수 있음
- 다음 코드는 이 모듈의 run 편의 함수를 사용해 프로세스를 시작하고 프로세스의 출력을 읽고, 프로세스가 오류 없이 깔끔하게 종료했는지 검사함
~~~python
import subprocess

result = subprocess.run(['echo', '자식 프로세스에게 보내는 인사'],
                        capture_output=True, #- True면 출력을 결과값을 변수에 저장 가능
                        encoding='utf-8')    #- 결과물을 encoding

#- 예외가 발생하지 않으면 문제없이 잘 종료된 것임
result.check_returncode()
print(result.stdout)

>>>
자식 프로세스에게 보내는 인사
~~~
- 파이썬에서 `subprocess` 등의 모듈을 통해 자식 프로세스는 부모 프로세스인 파이썬 인터프리터와 독립적으로 실행됨
- run 함수 대신에 `Popen` 클래스를 사용해 하위 프로세스를 만들면, 파이썬이 다른 일을 하면서 주기적으로 자식 프로세스의 상태를 검사(polling)할 수 있음
~~~python
proc = subprocess.popen(['sleep', '1'])
while proc.poll() is None:
    print("작업 중...")
print("종료 상태", proc.poll())
~~~
- 자식 프로세스와 부모 프로세스를 분리하면 부모 프로세스가 원하는 개수만큼 자식 프로세스를 병렬로 실행할 수 있음
- 다음 코드는 Popen을 사용해 자식 프로세스를 한꺼번에 실행함
~~~Python
import time

start = time.time()
sleep_procs = []
for _ in range(10):
    proc = subprocess.Popen(['sleep', '1'])
    sleep_procs.append(proc)

for proc in sleep_procs:
    proc.communicate()    #- 결과물을 받아오는 함수. 
                          #- 자식 프로세스의 출력을 읽어옴. 자식 프로세스가 종료할 때까지 대기
end = time.time()
delta = end - start
print(f"{delta: .3}초 만에 끝남")

>>>
 1.03초 만에 끝남
~~~
- 각 프로세스가 순차적으로 실행됐다면, 총 지연 시간은 여기서 측정한 1초 이하의 값이 아니라 10초 이상이였을 것임
- 파이썬 프로그램의 데이터를 파이프(pipe)를 사용해 하위 프로세스로 보내거나, 하위 프로세스의 출력을 받을 수 있음
- 이를 통해 여러 다른 프로그램을 사용해서 병렬적으로 작업을 수행할 수 있음
- 예를 들어 openssl 명령줄 도구를 사용해 데이터를 암호화한다고 해보자. 명령줄 인자를 사용해 자식 프로세스를 시작하고 자식 프로세스와 I/O 파이프를 연결하는 것은 아주 쉬움
~~~python
def run_encrypt(data):
    env = os.environ.copy()
    env['password'] = 'zf7ShyBhZOraQDdE/FiZpm/m/8f9X+M1'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env.password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()     #- 자식이 입력을 받도록 보장함
    return proc
~~~
- 다음 코드는 난수 바이트 문자열을 암호화 함수에 연결하지만, 실전에서는 파이프를 통해 사용자 입력, 파일 핸들, 네트워크 소켓 등에서 받은 데이터를 암호화 함수에 보내게 될 것임
~~~python
procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_encrypt(data)
    procs.append(proc)
~~~
- 자식 프로세스는 병렬로 실행되면서 입력을 소비함. 다음 코드는 자식 프로세스가 끝나기를 기다렸다가 마지막 츨력을 가져옴
- 출력은 예상대로 암호화된 바이트 문자열임
~~~python
for proc in procs:
    out, _ = proc.communicate()
    print(out[-10:]) #- 암호문이 너무 길어 10개만 짤라서 확인

>>>
b't\xf7\xe6!\t\x16\x9b+@\xe6'
b'\x80f\x04a\xed\x82\x18\x00\xdf\xcb'
b" \xa1'o\x06\xe4\x9c\x1b+e"
~~~
- 유닉스 파이프라인처럼 한 자식 프로세스의 출력을 다음 프로세스의 입력으로 계속 연결시켜 여러 병렬 프로세스를 연쇄적으로 연결도 가능
- 다음은 openssl 명령줄 도구를 하위 프로세스로 만들어 입력 스트림의 월풀(Whirpool) 해시를 계산함
~~~python
encrypt_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(10)

    encrypt_proc = run_encrypt(data)
    encrypt_procs.append(encrypt_proc)

    hash_proc = run_hash(encrypt_proc.stdout)
    hash_procs.append(hash_proc)

    #- 자식이 입력 스트림에 들어오는 데이터를 소비하고 communicate() 메서드가
    #- 불필요하게 자식로부터 오는 입력을 훔쳐가지 못하게 만듬
    #- 또 다운스트림 프로세스가 죽으면 SIGPIPE를 업스트림 프로세스에 전달함
    encrypt_proc.stdout.close()
    encrypt_proc.stdout = None
~~~
- 자식 프로세스들이 시작되면 프로세스간 I/O가 자동으로 일어남
~~~python
for proc in encrypt_procs:
    proc.communicate()
    assert proc.returncode == 0

for proc in hash_procs:
    out, _ = proc.communicate()
    print(out[-10:])

assert proc.returncode == 0

>>>
b'\xe2&\x80\xec\x99\xf4\xfe\x9e\xa4\xcd'
b"'\x89\x191\xe6LT0\x13;"
b'\x12\x18\x10\xe9K%2]\xe7\xf6'
~~~
- 자식 프로세스가 결코 끝나지 않는 경우, 입력이나 출력 파이프를 기다리면서 block되는 경우를 우려한다면, timeout 파라미터를 communicate 메서드에 전달할 수 있음
- timeout 값을 전달하면 자식 프로세스가 주어진 시간 동안 끝나지 않을 경우 예외 발생
- 따라서 잘못 동작하는 하위 프로세스를 종료할 수 있음
~~~Python
proc = subprocess.Popen(['sleep', '10'])
try:
    proc.communicate(timeout=0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('종료 상태', proc.poll())

>>>
종료 상태 -15
~~~

#### 기억해야 할 내용
- subprocess 모듈을 사용해 자식 프로세스를 실행하고 입력과 출력 스트림을 관리할 수 있음
- 자식 프로세스는 파이썬 인터프리터와 병렬로 실행되므로 CPU 코어를 최대로 쓸 수 있음
- 간단하게 자식 프로세스를 실행하고 싶은 경우에는 run 편의 함수를 사용해라. 유닉스 스타일의 파이프라인이 필요하면 Popen 클래스를 사용해라
- 자식 프로세스가 멈추는 경우나 교착 상태를 방지하려면 communicate 메서드에 대해 timeout 파라미터를 사용해라

### 53-블로킹 I/O의 경우 스레드를 사용하고 병렬성을 피해라
- 파이썬의 표준 구현을 CPython이라고 하는데, 소스 코드를 구문 분석하여 바이트 코드로 변환하고, 이 코드를 스택 기반 인터프리터로 실행함
- <b>바이트코드 인터프리터에는 파이썬 프로그램이 실행되는 동안 일관성 있게 유지해야 하는 상태가 존재함</b>
- CPython은 전역 인터프리터 락(Global Interpreter Lock, GIL)이라는 방법을 사용해 일관성을 강제로 유지함
- 근본적으로 GIL은 상호 배제 락(mutual exclusion lock)이며, CPython이 선점형 멀티스레드로 인해 영향을 받는 것을 방지함
- 선점형 멀티스레드에서는 한 스레드가 다른 스레드의 실행을 중간에 인터럽트시키고 제어를 가져올 수 있음
- 이런 인터럽트가 예기치 못한 때 발생하면 인터프리터의 상태가 오염될 수 있음
- GIL은 CPython 자체와 CPython이 사용하는 C 확장 모듈이 실행되면서 인터럽트가 함부로 발생하는 것을 방지해 인터프리터 상태가 제대로 유지되고 바이트코드 명령들이 제대로 실행되도록 만듬
- <b>GIL은 큰 부작용이 있는데, C++나 자바로 작성된 프로그램에서 실행 스레드가 여럿 있다는 말은 이런 프로그램이 여러 CPU 코어를 동시에 활용할 수 있다는 뜻임. 파이썬도 다중 스레드를 지원하지만, GIL로 인해 여러 스레드 중 하나만 앞으로 진행할 수 있음</bs>
- 따라서 파이썬 프로그램의 속도를 높이고 병렬 처리를 수행하고자 스레드를 사용한다면 크게 실망할 수 있음
- 예를 들어 파이썬으로 계산량이 매우 많은 작업을 수행하고 싶다고 하자
- 다음은 계산량이 많은 작업의 예로 사용할 평이하게 작성한 인수 찾기 알고리즘이다
~~~python
import time

numbers = [2139079, 1214759, 1516637, 1852285]
start = time.time()

for number in numbers:
    list(factorize(number))

end = time.time()
delta = end - start
print(f"총 {delta: 3f} 초 걸림")

>>>
총  0.404845 초 걸림
~~~
- 다른 언어는 컴퓨터에 있는 모든 CPU 코어를 활용할 수 있으므로, 다중 스레드를 사용해 계산을 수행하는 것이 타당
- 이를 파이썬 코드로 수행해보자. 다음 코드는 위의 코드 계산을 수행하는 스레드 정의임
~~~python

from threading import Thread

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))

start = time.time()
threads = []
for number in numbers:
    thread = FactorizeThread(number) #- 4개의 스레드 생성(4코어일 경우)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time.time()
print(f"총 {delta:.3f} 초 걸림")

>>>
총 0.405 초 걸림
~~~
- 놀랍게도 스레드를 하나만 써서 순차적으로 factorize를 실행할 때보다 시간이 더 오래걸림
- 다른 언어에서 각 수에 스레드를 하나씩 할당하면, 스레드 생성과 스레드 실행 조정에 따른 부가 비용이 들기 때문에 네 배(numbers에 4개의 숫자가 들어있음)보다 약간 적은 수준의 속도 향상을 볼 수 있음
- 2코어 시스템이라면 최대 2배까지 속도 향상을 예상할 수 있음
- 하지만 사용할 수 있는 CPU가 많은데도 스레드를 사용해 속도가 느려질 것이라고는 예상하지 못했을 것임. 이 결과는 표준 CPython 인터프리터에서 프로그램을 사용할 때 GIL(락 충돌과 스케줄링 부가 비용)에 미치는 영향을 잘 보여줌
- CPython에서도 다중 코어를 활용할 수 있는 방법이 있지만, 코딩하는데 상당한 노력이 들어감
- 이런 한계에도 불구하고 파이썬이 스레드를 지원하는 이유는 무엇일까? -> 두 가지 타당한 이유가 있음
- 첫 째, 다중 스레드를 사용하면 프로그램이 동시에 여러 일을 하는 것처럼 보이게 만들기 쉬움. 동시성 작업의 동작을 잘 조화시키는 코드를 직접 작성하기는 어려움
- <b>스레드를 사용하면 우리가 작성한 함수를 파이썬으로 동시에 실행시킬 수 있음</b>
- 파이썬 GIL로 인해 스레드 중 하나만 앞으로 진행할 수 있음에도 불구하고, CPython이 어느 정도 균일하게 스레드를 실행시켜 주므로, 다중 스레드를 통해 여러 함수를 동시에 실행시킬 수 있음
- 두 번째는 블로킹(blocking) I/O를 다루기 위해서임. 블로킹 I/O는 특정 시스템 콜을 사용할 때 일어남
- 파이썬 프로그램은 시스템 콜을 사용해 컴퓨터 운영체제가 자신 대신 외부 환경과 상호작용하도록 의뢰함
- 파일 쓰기나 읽기, 네트워크와 상호작용하거나, 디스플레이 장치와 통신하기 등의 작업이 블로킹 I/O에 속함
- 스레드를 사용하면 운영체제가 시스템 콜 요청에 응답하는 데 걸리는 시간 동안 파이썬 프로그램이 다른 일을 할 수 있음
- 예를 들어 직렬 포트(serial port)를 통해 원격 제어 헬리콥터에 신호를 보내고 싶다고 하자
- 이 동작을 대신해 느린 시스템 콜(select)를 사용할 것임. 이 함수는 운영체제에게 0.1초 동안 블록한 다음에 제어를 돌려달라고 요청하는데, 동기적으로 직렬 포트를 사용할 때 벌어지는 상황과 비슷 
~~~python
import select
import socket

def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)
~~~
- 이 시스템 콜을 순차적으로 실행하면 실행에 필요한 시간이 선형으로 증가함
~~~python
import select
import socket

def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)

start = time.time()

for _ in range(5):
    slow_systemcall()
end = time.time()
delta = end - start
print(f"총 {delta: .3f} 초 걸림")
~~~
- 문제는 `slow_systemcall` 함수가 실행되는 동안 프로그램이 아무런 진전을 이룰 수 없다는 것
- 이 프로그램의 주 실행 스레드는 select 시스템 콜에 의해 블록됨
- 헬리콥터에 신호를 보내는 동안 헬리콥터가 다음에 어디로 이동할지 계산할 수 있어야 함. 그렇지 않으면 헬리콥터는 추락할 수 있음
- 블로킹 I/O와 계산을 동시에 수행해야 한다면 시스템 콜을 스레드로 옮기는 것을 고려해봐야 함
- 다음 코드는 `slow_systemcall` 함수를 여러 스레드에서 따로따로 호출함. 이렇게 하면 직렬 포트와 통신하면서 주 스레드는 필요한 계산을 수행할 수 있음
~~~python
start = time.time()
threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)
~~~
- 스레드를 시작한 후, 다음 코드는 시스템 콜 스레드가 끝나기 전에 헬리콥터의 다음 움직임을 계산함
~~~Python
import select
import socket
import time
from threading import Thread

def slow_systemcall():
    select.select([socket.socket()], [], [], 3)
    print("system call!")

start = time.time()

threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)

def compute_helicopter_location(index):
    print("helicopter signal come")
    time.sleep(3)
    pass

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'총 {delta:.3f} 초 걸림')
~~~
- 병렬화한 버전은 순차적으로 실행했을 때 보다 시간이 1/5로 줄어듬
- 이는 GIL로 인해 생기는 한계가 있더라도, 파이썬이 여러 스레드를 통해 시스템 콜을 병렬로 실행 할 수 있음을 보여줌
- <b>GIL은 파이썬 프로그램이 병렬로 실행되지 못하게 막지만, 시스템 콜에는 영향을 끼칠 수 없음</b>
- 이런 코드가 동작하는 이유는 파이썬 스레드가 시스템 콜을 하기 전에 GIL을 해제하고 시스템 콜에서 반환되자마자 GIL을 획득하기 때문
- 스레드 외에도 `asyncio` 내장 모듈 등 블로킹 I/O를 처리하는 방법이 많이 있으며, 이런 대안마다 중요한 장점이 존재함
- 코드를 가급적 손대지 않고 블로킹 I/O를 병렬로 실행하고 싶을 때는 스레드를 사용하는 것이 가장 바람직함

### 기억해야 할 내용
- 파이썬 스레드는 GIL(global interpreter lock)으로 인해 다중 CPU 코어에서 병렬로 실행될 수 없음
- GIL이 있음에도 불구하고 파이썬 스레드는 여전히 유용. 스레드를 사용하면 여러 일을 동시에 진행하는 프로그램을 쉽게 기술할 수 있기 때문
- 파이썬 스레드를 사용해 여러 시스템 콜을 병렬로 할 수 있음. 이를 활용하면 블로킹 I/O와 계산을 동시에 할 수 있음

### 54-스레드에서 데이터 경합을 피하기 위해 Lock을 사용해라
- 초보 파이썬 프로그래머는 전역 인터프리터 락(GIL)을 배운 뒤 코드에서 더 이상 상호 배제 락을 사용하지 않아도 되는 것으로 생각한다
- GIL이 다중 CPU에서 파이썬 쓰레드들이 병렬적으로 실행될 수 없게 막는다면, 파이썬 스레드들이 프로그램의 데이터 구조에 동시에 접근할 수 없게 막는 락 역할도 해줘야 하지 않을까? 
- 리스트나 딕셔너리 같은 몇 가지 타입에 대해 테스트해보면 이런 가정이 성립하는 것처럼 보이기까지 함
- 하지만 GIL이 동시 접근을 보장해주는 락 역할을 하는 것처럼 보여도 실제로는 전혀 그렇지 않음
- GIL은 여러분을 보호해주지 못함. 파이썬 스레드는 한 번에 단 하나만 실행될 수 있지만, 파이썬 인터프리터에서 어떤 스레드가 데이터 구조에 대해 수행하는 연산은 연속된 두 바이트코드 사이에서 언제든 인터럽트될 수 있음
- 여러 스레드가 같은 데이터 구조에 접근하면 위험함. 이런 인트럽트로 인해 실질적으로는 언제든지 데이터 구조에 대한 불변 조건이 위반될 수 있고, 그에 따라 프로그램의 상태가 오염될 수 있음
- 예를 들어 병렬적으로 여러 가지의 개수를 세는 프로그램을 작성한다고 하자. 센서 네트워크에서 광센서를 통해 빛이 들어온 경우를 샘플링하는 예를 생각해 볼 수 있음
- 시간이 지나면서 빛이 들어온 횟수를 모두 세고 싶다면 새로운 클래스를 사용해 셀 수 있음
~~~python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset
~~~
- 센서를 읽을 때는 블로킹 I/O를 수행하므로 센서마다 작업자 스레드를 할당한다고 하자
- 각 작업자 스레드는 센서 값을 측정한 다음에 카운터를 최댓값까지 증가시킬 수 있음
~~~python
def worker(sensor_index, how_many, counter):
    print("reading sensor!")
    for _ in range(how_many):
        counter.increment(1)
~~~
- 병렬로 센서마다 하나씩 worker 스레드를 실행하고, 모든 스레드가 값을 다 읽을 때까지 기다림
~~~python
threads = []
for i in range(5):
    thread = Thread(target=worker, args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()        #- thread가 종료할 때까지 기다림

expected = how_many * 5
found = counter.count
print(f"카운터 값은 {expected}여야 하는데, 실제로는 {found} 입니다.")
~~~
- 해당 코드는 단순해 보이고, 결과도 뻔한 것 같지만, 실제 실행한 결과는 예상과 전혀 다름
- 파이썬 인터프리터는 실행되는 모든 스레드를 강제로 공평하게 취급해서 각 스레드의 실행 시간을 거의 비슷하게 만듬
- 이를 위해 파이썬은 실행 중인 스레드를 일시중단시키고 다른 스레드를 실행시키는 일을 반복함
- 중요한 것은 파이썬이 스레드를 언제 중단시킬지 알 수 없다는 점
- 심지어 atomic한 것처럼 보이는 연산을 수행하는 도중에도 파이썬이 일시 중단시킬 수 있음 
- 이로 인해 방금 본 예제와 같은 결과가 생김
- `Counter` 객체의 `increment` 메서드는 간단해 보임. 작업자 스레드 입장에서 보면 다음 문장과 같음
~~~python
counter.count += 1
~~~
- 하지만 객체 애트리뷰트에 대한 `+=` 연산자는 실제로는 세가지 연산으로 이뤄짐
- 방금 본 문장은 다음과 같음
~~~python
value = getattr(counter, 'count')
result = value + 1
setattr(counter, 'count', result)
~~~
- 카운터를 증가시키는 파이썬 스레드는 새 연산 사이에서 일시 중단될 수 있고, 이런 일시 중단으로 인해 스레드 간 연산 순서가 뒤섞이면서 value의 이전 값을 카운터에 대입하는 일이 생길 수 있음
- 다음은 두 스레드 A와 B 사이에서 이런 나쁜 상호작용이 일어난 경우
~~~python 
#- 스레드 A에서 실행
value_a = getattr(counter, 'count')

#- 스레드 B로 컨텍스트 스위칭
value_b = getattr(counter, 'count')
result_b = value_b + 1

#- 다시 스레드 #A로 컨텍스트 전환
result_a = value_a + 1
setattr(counter, 'count', result_a)
~~~
- 스레드 A가 완전히 끝나기 전에 인터럽트가 일어나서 스레드 B가 실행됨
- 스레드 B의 실행이 끝나고 다시 스레드 A가 중간부터 실행을 재개함
- 이로 인해 스레드 B가 카운터를 증가시켰던 결과가 모두 사라짐
- <b>이와 같은 데이터 경합이나 다른 유형의 데이터 구조 오염을 해결하기 위하여 파이썬은 `threading` 내장 모듈 안에 도구들을 제공</b>
- 가장 간단하지만 유용한 도구로 `Lock` 클래스가 있음. `Lock` 클래스는 상호 배제 락(뮤텍스)임
- 락을 사용하면 `Counter` 클래스가 여러 스레드의 동시 접근으로부터 자신의 현재 값을 보호할 수 있음
- 한 번에 단 하나의 스레드만 락을 획득할 수 있음. 다음 코드에서는 `with`문을 사용해 락을 획득하고 해제함
- with 문을 사용하면 락을 획득한 상태에서 수행해야 하는 코드를 쉽게 알아볼 수 있음
~~~python
from threading import Lock
class LockingCounter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset
~~~
- 이제 예전과 같이 worker 스레드를 실행하되 `LockingCounter`를 사용한다
~~~python
from threading import Lock
class LockingCounter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset

from threading import Thread
how_many = 10 ** 5
counter = LockingCounter()

threads = []
for i in range(5):
    thread = Thread(target=worker, args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()        #- thread가 종료할 때까지 기다림

expected = how_many * 5
found = counter.count
print(f"카운터 값은 {expected}여야 하는데, 실제로는 {found} 입니다.")

>>>
카운터 값은 500000여야 하는데, 실제로는 500000 입니다.
~~~
- 이제는 에상 실행 결과가 들어맞는다. Lock이 문제를 해결해줌 

### 기억해야 할 내용
- 파이썬에는 GIL이 있지만, 파이썬 프로그램 코드는 여전히 여러 스레드 사이에 일어나는 데이터 경합으로부터 자신을 보호해야 함
- 코드에서 여러 스레드가 상호 배제 락 없이 같은 객체를 변경하도록 허용하면 코드가 데이터 구조를 오염시킬 것임
- 여러 스레드 사이에서 프로그램의 불변 조건을 유지하려면 threading 내장 모듈의 Lock 클래스를 활용해라

### 55- Queue를 사용해 스레드 사이의 작업을 조율해라
- 파이썬 프로그램이 동시에 여러 일을 수행한다면 각 작업을 잘 조율해야 함
- 동시성 작업을 처리할 때 가장 유용한 방식은 함수 파이프라인임
- 파이프라인은 순차적으로 실행해야 하는 여러 단계가 있고, 각 단계마다 실행할 구체적인 함수가 정해짐
- 파이프라인의 한쪽 끝에는 새로운 작업이 계속 추가되고, 각 함수는 동시에 실행될 수 있고 각 단계에서 처리해야 하는 일을 담당함
- 작업은 매 단계 함수가 완료될 때마다 다음 단계로 전달되며, 더 이상 실행할 단계가 없을 떄 끝남
- 이런 접근 방법은 작업 처리에 블로킹 I/O이나 하위 프로세스가 포함되는 경우에 좋은데, 더 쉽게 병렬화 할 수 있기 때문
- 예를 들어 디지털 카메라에서 이미지 스트림을 계속 가져와 이미지 크기를 변경하고 온라인 포토 갤러리에 저장하고 싶다고 하자. 3단계 파이프라인으로 나눠 프로그램을 구성할 수 있음
- 첫 번째 단계에서 새 이미지를 얻고, 얻은 이미지는 두 번째 단계의 크기 변환 함수로 보내 처리함
- 크기가 조정된 이미지를 마지막 단계의 업로드 함수에 전달해 처리
~~~python
def download(item):
    pass

def resize(item):
    pass

def upload(item):
    pass
~~~
- 가장 먼저 필요한 기능은 파이프라인의 단계마다 작업을 전달할 방법임. producer-consumer를 이용해 이를 모델링 할 수 있음
~~~python
from collections import deque
from threading import Lock

class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()
~~~
- 생산자인 디지털 카메라는 미처리 작업을 표현하는 deque 끝에 새로운 이미지를 추가함
~~~python
    def put(self, item):
        with self.lock:
            self.items.append(item)
~~~
- 파이프라인의 첫 번째 단계인 소비자는 미처리 작업을 표현하는 deque의 맨 앞에서 이미지를 제거함
~~~python
    def get(self):
        with self.lock:
            return self.items.popleft()
~~~
- 다음 코드는 방금 본 것과 비슷한 큐(queue)에서 가져온 작업에 함수를 적용하고, 그 결과를 다른 큐에 넣는 스레드를 통해 파이프라인의 각 단계를 구현함
- 그리고 각 작업자가 얼마나 많이 새로운 입력을 검사(polled_count)했고 얼마나 많이 작업을 완료(work_done)했는지 추적함
~~~python
from threading import Thread
import time

class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0
~~~
- 가장 까다로운 곳은 입력 큐가 비어 있는 경우를 작업자 스레드가 제대로 처리하는 부분
- 큐가 비어있다는 말은 이전 단계가 아직 작업을 완료하지 못했다는 뜻
- 다음 코드에서 IndexError 예외를 잡아내는 부분이 바로 이런 경우. 이를 조입 라인을 일시 중단시키는 것으로 생각할 수 있음
~~~Python
def run(self):
    while True:
        self.polled_count += 1
        try:
            item = self.in_queue.get()
        except IndexError:
            time.sleep(0.1)
        else:
            result = self.func(item)
            self.out_queue.put(result)
            self.work_done += 1
~~~
- 이제 파이프라인을 조율하기 위한 조율 지점 역할을 할 수 있도록 각 단계별로 큐를 생성하고 각 단계에 맞는 작업 스레드를 만들어서 서로 연결할 수 있음
~~~python
download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()

done_queue = MyQueue()
threads = [
    Worker(download, download_queue, resize_queue),
    Worker(resize, resize_queue, upload_queue),
    Worker(upload, upload_queue, done_queue)
]
~~~
- 각 단계를 처리하기 위해 세 가지 스레드를 시작하고, 파이프라인의 첫 번쨰 단계에 원하는 만큼 작업을 넣음
- 다음 코드는 download 함수에 필요한 실제 데이터 대신 간단한 object를 사용함
~~~python
for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())
~~~
- 이제 `done_queue`를 지켜보면서 파이프라인이 모든 원소를 처리할 때까지 기다림
~~~python
while len(done_queue.items) < 1000:
    pass
~~~
- 이 코드는 제대로 작동하지만, 스레드들이 새로운 작업을 기다리면서 큐를 폴링하기 때문에 부작용이 생김
- `run` 메서드 안의 까다로운 부분인 `IndexError` 예외를 잡아내는 부분이 상당히 많이 실행됨
~~~python
processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print(f"{processed} 개의 아이템을 처리했습니다."
      f"이 때 폴링을 {polled}번 했습니다.")

>>>
1000 개의 아이템을 처리했습니다.이 때 폴링을 3009번 했습니다.
~~~
- 해당 코드의 문제점이 4가지 추가로 있음
- 작업자 함수의 속도가 달라지면 앞에 있는 단계가 그보다 더 뒤에 있는 단계의 진행을 방해하면서 파이프라인을 막을 수 있음
- 아로 인에 뒤에 있는 단계는 작업을 받지 못하는 starvation 상태가 돼서 작업이 없으므로, 루프를 빠르게 돌며 새로운 작업이 들어왔는지 자신의 입력 큐를 계속 검사함
- <b>이로 인해 직업자 스레드가 유용하지 않은 일을 하느라 CPU 시간을 잡아먹게 됨</b>
- 두 번째, 모든 작업이 다 끝났는지 검사하기 위해 추가로 `done_queue`에 대해 busy waiting을 수행해야 함
- 세 번째, Worker의 run 메서드가 루프를 무한히 반복함. 현재 구현에서는 작업자 스레드에게 루프를 중단할 시점임을 알려줄 뚜렷한 방법이 없음
- 네 번째, 파이프라인 진행이 막히면 프로그램이 임의로 중단될 수 있음 how? 첫 번째 단계가 빠르게 진행되는데 두 번쨰 단계가 느리게 진행되면, 첫 번째 단계와 두 번째 단계를 연결하는 큐의 크기가 계속 늘어남. 언젠간 메모리를 다 소모하고 프로그램이 죽어버릴 것임
- 즉, 제대로 작동하는 prosumer-consumer 큐를 직접 구현하기가 어려움. 이를 Queue 내장 함수를 통해 구현할 수 있음

#### 대안: queue
- queue 내장 모듈에 있는 Queue 클래스는 앞서 설명한 모든 문제를 해결할 수 있는 기능 제공
- Queue는 새로운 데이터가 나타날 때까지 `get` 메서드가 블록되게 만들어서 작업자의 busy waiting 문제를 해결함
- 예를 들어 다음 코드는 큐에 입력 데이터가 들어오기를 기다리는 스레드를 하나 시작함
~~~python
from queue import Queue

my_queue = Queue()
def consumer():
    print("소비자 대기")
    my_queue.get()
    print('소비자 완료')

thread = Thread(target=consumer)
thread.start()
~~~
- 이 스레드가 먼저 실행되지만, Queue 인스턴스에 원소가 `put`돼서 `get` 메서드가 반환할 원소가 생기기 전까지 이 스레드는 끝나지 않음
~~~python
print("생산자 데이터 추가")
my_queue.put(object())
print("생산자 완료")
thread.join()

>>>
생산자 데이터 추가
생산자 완료
소비자 완료
~~~
- 파이프라인 중간이 막히는 경우를 해결하기 위해 Queue 클래스에서는 두 단계 사이에 허용할 수 있는 미완성 작업의 최대 개수를 지정할 수 있음(queue buffer 크기)
- 이렇게 버퍼 크기를 정하면 큐가 이미 가득 찬 경우 put이 블록됨(위의 네 번째 문제 해결)
- 다음 코드는 큐 원소가 소비될 때까지 대기하는 스레드를 정의함
~~~python
def consumer():
    time.sleep(0.1)
    my_queue.get()
    print("소비자 1")
    my_queue.get()
    print("소비자 2")
    print("소비자 완료")

thread = Thread(target=consumer)
thread.start()
~~~
- 큐에 원소가 없을 경우 소비자 스레드가 대기하므로, 생산자 스레드는 소비자 스레드가 `get`을 호출했는지 여부와 관계없이 put을 두 번 호출해 객체를 큐에 추가할 수 있음
- 하지만 코드에서 Queue의 크기는 1임. 이는 생산자가 두 번쨰로 호출한 put이 큐에 두 번째 원소를 넣으려면 소비자가 최소 한 번이라도 get을 호출할 때까지 기다려야 한다는 뜻
~~~python
my_queue.put(object())
print("생산자 1")
my_queue.put(object())
print("생산자 2")
print("생산자 완료")
thread.join()

생산자 1
소비자 1
생산자 2
생산자 완료
소비자 2
소비자 완료
~~~
- 이 모든 동작을 Queue 하위 클래스에 넣고, 처리가 끝났음을 작업자 스레드에게 알리는 기능을 추가할 수 있음
- 다음 코드는 큐에 더 이상 다른 입력이 없음을 표시하는 특별한 센티넬(sentinel) 원소를 추가하는 close 메서드를 정의함
~~~python
class ClosableQueue(Queue):
    SENTINAL = object()

    def close(self):
        self.put(self.SENTINEL)
~~~
- 그 후 큐를 이터레이션하다가 이 특별한 object를 찾으면 이터레이션을 끝냄
- 그리고 이 `__iter__` 메서드는 큐의 작업 진행을 감시할 수 있게 하고자 `task_done`을 적당한 횟수만큼 호출해줌
~~~python
class ClosableQueue(Queue):
    SENTINAL = object()

    def close(self):
        self.put(self.SENTINAL)

    def __iter__(self):
        while(True):
            item = self.get()
            try:
                if item is self.SENTINAL:
                    return
                yield item
            finally:
                self.task_done()
~~~
- 이제 작업자 스레드가 `ClosableQueue` 클래스의 동작을 활용하게 할 수 있음(세 번째 문제점 해결)
- 이 스레드는 for 루프가 끝나면 종료됨
~~~python
class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func =func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)
~~~
- 이렇게 정의한 새 작업자 클래스를 사용해 작업자 스레드를 새로 정의함
~~~Python
download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
threads = [
    StoppableWorker(download, download_queue, resize_queue),
    StoppableWorker(resize, resize_queue, upload_queue),
    StoppableWorker(upload, upload_queue, done_queue)
]
~~~
- 이전과 마찬가지로 thread를 실행하고 첫 번쨰 단계의 입력 큐에 모든 입력 작업을 추가한다음, 입력이 모두 끝났음을 표시하는 신호를 추가함
~~~python
for thread in threads:
    thread.start()

for _ in range(1000):
    download_queue.put(object())

download_queue.close()
~~~
- 마지막으로 각 단계를 연결하는 큐를 join함으로써 작업 완료를 기다림(join을 선언하면 해당 작업이 끝날 때까지 기다림)
- 각 단계가 끝날 때마다 다음 단계의 입력 큐의 close를 호출해서 작업이 더 이상 없음을 통지
- 마지막 done_queue에는 예상대로 모든 출력이 들어 있음 
~~~python
download_queue.join()
resize_queue.close()
resize_queue.join()
upload_queue.close()
upload_queue.join()
print(done_queue.qsize(), '개의 원소가 처리됨')

for thread in threads:
    thread.join()

>>>
1000 개의 원소가 처리됨
~~~
- 이 접근 방법을 확장해 단계마다 여러 작업자를 사용할 수 있음
- 그러면 I/O 병렬성을 높일 수 있으므로, 이런 유형에 속한 프로그램의 속도를 상당히 증가시킬 수 있음
- 이를 위해 먼저 다중 스레드를 시작하고 끝내는 도우미 함수를 만듬
- `stop_threads` 함수는 소비자 스레드의 입력 큐마다 close를 호출하는 방식으로 작동
- 이렇게 하면 모든 작업자를 깔끔하게 종료시킬 수 있음
~~~python
def start_threads(count, *args):
    threads = [StoppableWorker(*args) for _ in range(count)]
    for thread in threads:
        thread.start()
    return threads


def stop_threads(closable_queue, threads):
    for _ in threads:
        closable_queue.close()

    closable_queue.join()

    for thread in threads:
        thread.join()

download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
download_threads = start_threads(
    3, download, download_queue, resize_queue)
resize_threads = start_threads(
    4, resize, resize_queue, upload_queue)
upload_threads = start_threads(
    5, upload, upload_queue, done_queue)

for _ in range(1000):
    download_queue.put(object())

stop_threads(download_queue, download_threads)
stop_threads(resize_queue, resize_threads)
stop_threads(upload_queue, upload_threads)

print(done_queue.qsize(), '개의 원소가 처리됨')

>>>
1000개의 원소가 처리됨
~~~
- 선형적인 파이프라인의 경우, Queue가 잘 작동하지만, 다른 도구가 더 나은 상황도 많음

#### 기억해야 할 내용
- 순차적인 작업을 동시에 여러 파이썬 스레드에서 실행되도록 조직하고 싶을 떄, 특히 I/O 위주의 프로그램인 경우라면 파이프라인이 매우 유용
- 동시성 파이프라인을 만들 때 발생할 수 있는 여러가지문제(busy waiting, 작업자에게 종료를 알리는 방법, 잠재적인 메모리 사용량 폭발등)를 잘 알아두자
- Queue 클래스는 튼튼한 파이프라인을 구축할 때 필요한 기능인 블로킹 연산, 버퍼 크기 지정, join을 통한 완료 대기 등을 모두 제공함

## 용어 정리
- 업스트림, 다운스트림
  - 업스트림: 로컬에서 서버로 전달되는 데이터의 흐름
  - 다운스트림: 서버에서 로컬로 전달되는 데이터의 흐름  
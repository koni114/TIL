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


### 3-언제 동시성이 필요한지 인식하는 방법을 알아두라
- 프로그램이 다루는 영역이 커짐에 따라서 불가피하게 복잡도도 증가함
- 프로그램의 명확성, 테스트 가능성, 효율성을 유지하면서 늘어나는 요구 조건을 만족시키는 것은 프로그래밍에서 가장 어려운 부분임
- 그중에서도 가장 처리하기 어려운 일은 단일 스레드 프로그램을 동시 실행되는 여러 흐름으로 이뤄진 프로그램으로 바꾸는 경우일 것임
- 이런 문제를 겪을 수 있은 경우를 예제로 살펴보자
- 한 게임이 있는데, 임의의 크기인 2차원 그리드가 있으며, 이 그리드의 각 셀(cell)은 비어 있거나(empty) 살아 있을 수 있음
~~~python
ALIVE = "*"
EMPTY = '-'
~~~
- 클럭이 한 번 틱할 때마다 게임이 진행됨. 틱마다 각 셀은 자신의 주변 여덟 개 셀이 살아 있는지 보고, 주변 셀 중 살아있는 셀의 개수에 따라 계속 살아남을지, 죽을지, 재생성할지를 결정함
- 각 셀의 상태를 컨테이너 클래스를 사용해 표현할 수 있음
- 이 클래스는 임의의 좌표에 있는 셀의 값을 설정하는 메서드를 제공해야 함
- 그리드 크기를 벗어나는 좌표는 나머지 연산을 사용해 적절한 그리드 내부 좌표로 바뀜(wrap around)
- 그리드 클래스는 무한히 반복되는 공간처럼 작동함
~~~python
class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def get(self, x, y):
        return self.rows[y % self.height][x % self.height]

    def set(self, y, x, state):
        self.row[y % self.height][x % self.width] = state

    def __str__(self):
        pass
~~~
- 클래스가 작동하는 모습을 보기 위해 Grid 인스턴스를 만들고 초기 상태를 고전적인 글라이더 형태로 설정함
~~~Python
ALIVE = "*"
EMPTY = '-'


class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def get(self, x, y):
        return self.rows[y % self.height][x % self.height]

    def set(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

    def __str__(self):
        result = ""
        for list in self.rows:
            tmp = ""
            for list_str in list:
                tmp += list_str
            result += tmp + '\n'
        return result

grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)
print(grid)
~~~
- 다음으로는 특정 셀의 주변 상태를 얻을 방법이 필요하므로, 그리드에 대해 질의를 수행해 살아있는 주변 셀 수를 반환하는 도우미 함수를 만든다
- 코드 결합을 줄이고자 Grid 인스턴스를 넘기는 대신 get 함수를 파라미터로 받는 간단한 함수를 사용한다
~~~python
def count_neighbors(y, x, get):
    n_ = get(y-1, x+0)
    ne = get(y-1, x+1)
    c_ = get(y+0, x+1)
    se = get(y+1, x+1)
    s_ = get(y+1, x+0)
    sw = get(y+1, x-1)
    w_ = get(y+0, x-1)
    nw = get(y-1, x-1)
    neighbor_states = [n_, ne, c_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count
~~~
- 콘웨이 생명 게임의 규칙
  - 두 개 이하가 살아 있으면 가운데 셀이 죽음
  - 네 개 이상이 살아 있으면 가운데 셀이 죽음
  - 정확히 3개가 살아있으면 가운데 셀이 살아있으면 계속 살아남고, 빈 셀이면 살아있는 상태로 바뀜
~~~python
def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
        else:
            if neighbors == 3:
                return ALIVE
        return state
~~~
- `count_neighbors` 와 `game_logic` 함수를 셀 상태를 변화시키는 다른 함수와 연결할 수 있음
- 각 제너레이션마다 이 함수를 한 그리드 셀에 대해 호출해서, 현재 셀 상태를 알아내고 이웃 셀의 상태를 살펴본 후 다음 상태를 결정한 다음 다음 결과 그리드의 셀 상태를 적절히 갱신함
- 여기서도 Grid 인스턴스를 넘기는 대신 그리드를 설정하는 함수를 set 파라미터로 받는 함수 인터페이스를 사용해 코드의 결합도를 낮춤
~~~python
def step_cell(x, y, get, set):
    state = get(x, y)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state
~~~
- 마지막으로 셀로 이뤄진 전체 그리드를 한 단계 진행시켜서 다음 세대의 상태가 담긴 그리드를 반환하는 함수를 정의함
- 여기서 중요한 세부 사항은 방금 우리가 만든 함수들이 이전 세대의 Grid 인스턴스에 대해 get 메서드를 호출해주는 함수와 다음 세대의 Grid 인스턴스에 대해 set 메서드를 호출해주는 함수에 의존한다는 점
- 이로 인해 모든 셀이 동일하게 작동하도록 할 수 있음. 이 기능은 생명 게임이 제대로 작동하려면 반드시 필요
- 앞에서 Grid 대신 get과 set에 대한 함수 인터페이스를 사용했으므로 이 기능을 쉽게 구현할 수 있음
~~~python
def simulate(grid):
    next_grid = Grid(grid.height, grid.width)
    for y in range(grid.width):
        for x in range(grid.height):
            step_cell(y, x, grid.get, next_grid.set)
        return next_grid
~~~
- 이제 한 번에 한 세대씩 전체 그리드를 진행 할 수 있음
- `game_logic` 함수에 구현한 간단한 규칙을 사용해 글라이더가 오른쪽 아래 방향으로 움직이는 모습을 볼 수 있음
~~~Python
class ColumnPrinter:
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(
                row_count, len(data.splitlines()) + 1)

        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line

                if (i + 1) < len(self.columns):
                    rows[j] += ' | '

        return '\n'.join(rows)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate(grid)

print(columns)
~~~
- 단일 코어에서 한 스레드로 실행하는 프로그램의 경우에는 이런 코드가 잘 동작함. 하지만 프로그램의 요구 사항이 바뀌어서 이제는 앞에서 살짝 암시한 바와 같이, `game_logic` 함수 안에서 약간의 I/O(소켓 통신 등)가 필요하다고 하자
- 예를 들어 그리드 상태와 인터넷을 통한 사용자 간 통신에 의해 상태 전이가 결정되는 MMOG(Massively Multiplayer Online Game)가 이런 경우임
- 앞의 구현을 어떻게 확장하면 이런 기능을 지원하게 할 수 있을까?
- 가장 단순한 방법은 블로킹 I/O를 game_logic안에 직접 추가하는 것
~~~python
def game_logic(state, neighbors):
    # 블로킹 I/O를 여기서 수행함
~~~
- 하지만 이 접근 방법은 블로킹 I/O로 인해 프로그램이 느려짐
- I/O의 지연 시간이 100밀리초이고 그리도에 셀이 45개 있으면, simulate 함수에서 순차적으로 처리되기 때문에 한 세대를 처리하는데 최소 4.5초가 걸림
- 게임을 즐길수 없을 정도이며, 나중에 그리드가 10000개의 셀을 포함하게 변경해야 한다면 각 세대를 계산하는데 15분이 걸림 
- <b>해결책은 I/O를 병렬로 수행해서 그리드 크기와 관계 없이 각 세대를 대략 100밀리초 안에 계산할 수 있게 만드는 것</b>
- <b>각 작업 단위에 대해 동시 실행되는 여러 실행 흐름을 만들어내는 과정을 팬아웃(fan-out)이라고 함</b> 
- 전체를 조율하는 프로세스안에서 다음 단계로 진행하기 전에 동시 작업 단위의 작업이 모두 끝날 때까지 기다리는 과정을 팬인(fan-in)이라고 함
- 파이썬은 팬아웃과 팬인을 지원하는 여러 가지 내장 도구를 제공하며ㄴ, 각 도구는 서로 다른 장단점을 지님
- 따라서 각 접근 방식의 장단점을 이해하고 상황에 따라 원하는 직업에 가장 알맞는 도구를 택해야함

#### 기억해야 할 내용
- 프로그램이 커지면서 범위와 복잡도가 증가함에 따라 동시에 실행되는 여러 실행 흐름이 필요해지는 경우가 많음
- 동시성을 조율하는 가장 일반적인 방법으로는 Fan-out -> Fan-In이 있음
- 파이썬은 팬아웃과 팬인을 구현하는 다양한 방법 제공

### 57-요구에 따라 팬아웃을 진행하려면 새로운 스레드를 생성하지 마라
- 파이썬에서 병렬 I/O를 실행하고 싶을 때는 자연스레 스레드를 가장 먼저 고려하게 됨. 하지만 여러 동시 실행 흐름을 만들어내는 팬아웃을 수행하고자 스레드를 사용할 경우 중요한 단점과 마주치게 됨
- 이 단점을 보여주기 위해 다룬 생명 게임 예제를 계속 살펴보
- 여기서는 스레드를 사용해 `game_logic` 안에서 I/O를 수행함으로써 생기는 지연 시간을 해결함
- 먼저 스레드를 사용할 때는 데이터 구조에 대해 가정한 내용을 유지하도록 여러 스레드를 조율해야 함
- Grid 클래스에 락 관련 동작을 추가하면, 여러 스레드에서 인스턴스를 동시에 사용해도 안전한 하위 클래스를 정의할 수 있음
~~~python
from threading import Lock

class LockingGrid(Grid):
    def __init__(self, height, width):
        super().__init__(height, width)
        self.lock = Lock()

    def __str__(self):
        with self.lock:
            return super().__str__()

    def get(self, y, x):
        with self.lock:
            return super().get(y, x)

    def set(self, y, x, state):
        with self.lock:
            return super().set(y, x, state)
~~~
- 이제 각 `step_cell` 호출마다 스레드를 정의해 팬아웃하도록 simulate 함수를 다시 정의할 수 있음
- 스레드는 병렬로 실행되며, 다른 I/O가 끝날 때까지 기다리지 않아도 됨
- 그 후 다음 세대로 진행하기 전에 모든 스레드가 작업을 마칠 때까지 기다리므로 팬인 할 수 있음
~~~python
def count_neighbors(y, x, get):
    n_ = get(y - 1, x + 0) # 북(N)
    ne = get(y - 1, x + 1) # 북동(NE)
    e_ = get(y + 0, x + 1) # 동(E)
    se = get(y + 1, x + 1) # 남동(SE)
    s_ = get(y + 1, x + 0) # 남(S)
    sw = get(y + 1, x - 1) # 남서(SW)
    w_ = get(y + 0, x - 1) # 서(W)
    nw = get(y - 1, x - 1) # 북서(NW)
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count

def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY # 살아 있는 이웃이 너무 적음: 죽음
        elif neighbors > 3:
            return EMPTY # 살아 있는 이웃이 너무 많음: 죽음
    else:
        if neighbors == 3:
            return ALIVE # 다시 생성됨
    #여기서 블러킹 I/O를 수행한다.
    #data = my_socket.recv(100)
    return state

def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)


def simulate_threaded(grid):
    next_grid = LockingGrid(grid.height, grid.width)

    threads = []
    for y in range(grid.height):
        for x in range(grid.width):
            args = (y, x, grid.get, next_grid.set)
            thread = Thread(target=step_cell, args=args)
            thread.start()  # 팬아웃
            threads.append(thread)

    for thread in threads:
        thread.join()  # 팬인

    return next_grid
~~~
- 앞서 본 예제의 step_cell을 그대로 사용하고, 구동 코드가 LockingGrid와 simulate_threaded 구현을 사용하도록 두 줄만 바꾸면 방금 만든 그리드 클래스 코드를 구동할 수 있음
~~~python
grid = LockingGrid(5, 9)            # 바뀐부분
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate_threaded(grid)  # 바뀐부분

print(columns)
~~~
- 코드는 예상대로 잘 동작하지만, 세가지 문제점이 존재
  - Thread 인스턴스를 서로 안전하게 조율하려면 몇 가지 도구가 필요함(Locking 등). 이로 인해 가독성이 떨어짐  
    이러한 복잡도 때문에 유지 보수 및 확장성이 떨어짐
  - 스레드는 메모리를 많이 사용하며, 스레드 하나당 8MB를 사용함. 현재 45개까지는 괜찮지만, 향후 10000개로 늘어났을 경우에는 out-of-memory 현상이 발생할 수 있음
  - 스레드를 시작하는 비용이 비싸며, context switching에 비용이 발생하기 때문에 스레드는 성능에 부정적인 영향을 미칠 수 있음 
- 게다가 이 코드는 무엇인가 잘못되었을 때 디버깅하기가 매우 어려움
- 예를 들어 I/O 예외가 발생했다고 가정해보자. I/O는 신뢰할 수 없기 때문에 `game_logic` 함수에서 예외가 발생했을 가능성이 매우 높은
~~~python
def game_logic(state, neighbors):
    # IOError가 발생하는 것을 에뮬레이션함
    raise OSError('I/O 문제 발생')
~~~
- 이 함수를 가리키는 Thread 인스턴스를 실행하고, 프로그램의 sys.stderr 출력을 메모리상의 StringIO 버퍼로 전달해 이 코드에서 어떤 일이 벌어지는지 살펴볼 수 있음
~~~python
import contextlib
import io

fake_stderr = io.StringIO()
with contextlib.redirect_stderr(fake_stderr):
    thread = Thread(target=game_logic, args=(ALIVE, 3))
    # 스레드 시작이나 join에는 문제 없음
    thread.start()
    thread.join()

print(fake_stderr.getvalue())

>>>
Exception in thread Thread-85:
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/threading.py", line 926, in _bootstrap_inner
    self.run()
  File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "<input>", line 67, in game_logic
OSError: I/O 문제 발생
~~~
- 예상대로 I/O 문제가 발생함. 하지만 Thread를 만들고 join을 호출하는 코드는 영향을 받지 않음
- 이유는 Thread 클래스가 target 함수에서 발생하는 예외를 독립적으로 잡아내서 sys.stderr로 예외의 트레이스를 출력하기 때문
- 이런 예외는 결코 최초의 스레드를 시작한 쪽으로 다시 던져지지 않음
- 이와 같은 여러 문제가 있으므로, 지속적으로 새로운 동시성 함수를 시작하고 끝내야 하는 경우 스레드는 적절한 해법이 아님
- 파이썬은 이러한 경우에 더 적합한 해법을 제공함

#### 기억해야 할 내용
- 스레드는 많은 단점이 있음. 스레드를 시작하고 실행하는데 비용이 들기 때문에 스레드가 많이 필요하면 상당히 많은 메모리를 사용함. 그리고 스레드 사이를 조율하기 위해 Lock과 같은 특별한 도구를 사용해야 함
- 스레드를 시작하거나 스레드가 종료하기를 기다리는 코드에게 스레드 실행 중에 발생한 예외를 돌려주는 파이썬 내장 기능은 없음. 이로 인해 스레드 디버깅이 어려워짐

### 58-동시성과 Queue를 사용하기 위해 코드를 어떻게 리펙터링해야 하는지 이해해라
- 바로 앞에서는 Thread를 사용해 생명 게임 예제의 병렬 I/O 문제를 해결할 경우 어떤 단점이 있는지 살펴봄 
- 다음은 queue 내장 모듈의 Queue 클래스를 사용해 파이프라인을 스레드로 실행되게 구현하는 것
- 일반적인 접근 방법은 다음과 같음. 생명 게임 세대마다 셀당 하나씩 스레드를 생성하는 대신, 필요한 병렬 I/O의 숫자에 맞춰 미리 정해진 작업자 스레드를 만듬
- 프로그램은 이를 통해 자원 사용을 제어하고, 새로운 스레드를 자주 시작하면서 생기는 부가 비용을 덜 수 있음
- 이를 위해 작업자 스레드의 `game_logic` 함수 사이의 통신에 ClosableQueue 인스턴스 두 개를 사용함
~~~python
from queue import Queue

class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return   # 스레드를 종료시킨다
                yield item
            finally:
                self.task_done()

in_queue = ClosableQueue()
out_queue = ClosableQueue()
~~~
- `in_queue`에서 원소를 소비하는 스레드를 여러 개 시작할 수 있음
- 각 스레드는 `game_logic`를 호출해 원소를 처리한 다음, `out_queue`에 결과를 넣음
- 각 스레드는 동시에 실행되며, 병렬적으로 I/O를 수행하므로, 그에 따라 세대를 처리하는데 필요한 지연 시간이 줄어듬
~~~python
from threading import Thread

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue, **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

def game_logic_thread(item):
    y, x, state, neighbors = item
    try:
        next_state = game_logic(state, neighbors)
    except Exception as e:
        next_state = e
    return (y, x, next_state)

# 스레드를 미리 시작한다
threads = []
for _ in range(5):
    thread = StoppableWorker(
        game_logic_thread, in_queue, out_queue)
    thread.start()
    threads.append(thread)
~~~
- 이런 큐와 상호작용하면서 상태 전이 정보를 요청하고 응답을 받도록 `simulate` 함수를 재정의 할 수 있음
- 원소를 `in_queue`에 추가하는 과정은 팬아웃이고, `out_queue`가 빈큐가 될 떄까지 원소를 소비하는 과정은 팬인임
~~~python
def simulate_pipeline(grid, in_queue, out_queue):
    for y in range(grid.height):
        for x in range(grid.width):
            state = grid.get(y, x)
            neighbors = count_neighbors(y, x, grid.get)
            in_queue.put((y, x, state, neighbors))  # 팬아웃
    in_queue.join()
    out_queue.close()
    next_grid = Grid(grid.height, grid.width)
    for item in out_queue:  # 팬인
        y, x, next_state = item
        if isinstance(next_state, Exception):
            raise SimulationError(y, x) from next_state
        next_grid.set(y, x, next_state)

    return next_grid
~~~
- `Grid.get`과 `Grid.set` 호출은 모두 새로운 simuate_pipeline 함수 안에서만 일어남
- 이는 동기화를 위해 Lock 인스턴스를 사용하는 Grid 구현을 새로 만드는 대신에 기존의 단일 스레드 구현을 쓸 수 있다는 뜻
- 이 코드는 전의 사용한 코드보다 디버깅도 더 쉬움
- `game_logic` 함수 안에서 I/O를 하는 동안 발생하는 예외는 모두 잡혀서 `out_queue` 로 전달되고 주 스레드에서 다시 던져짐
~~~python
def game_logic(state, neighbors):
    ...
    raise OSError("게임 로직에서 I/O 발생")
    ...

simulate_pipeline(Grid(1,1), in_queue, out_queue)

>>>
Traceback ...
~~~
- simulate_pipeline을 루프 안에서 호출해 이 세대별 다중 스레드 파이프라인을 구동할 수 있음
~~~python
class ColumnPrinter:
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(
                row_count, len(data.splitlines()) + 1)

        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line

                if (i + 1) < len(self.columns):
                    rows[j] += ' | '

        return '\n'.join(rows)


grid = LockingGrid(5, 9)            # 바뀐부분
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate_threaded(grid)  # 바뀐부분

print(columns)

for thread in threads:
    in_queue.close()
for thread in threads:
    thread.join()
~~~
- 결과는 이전과 같음. 메모리를 폭발적으로 사용하는 문제, 스레드 시작 비용, 스레드를 디버깅 하는 문제 등을 해결했지만 여전히 많은 문제가 남아있음
  - Better way 56에서 본 simlate thread 함수의 방식보다 simultate_pipeline 함수가 더 따라가기 어려움
  - 코드의 가독성을 개선하려면 `ClosableQueue`아 `StoppableWorker`라는 추가 지원 클래스가 필요하며, 이에 따라 복잡도가 늘어남
  - 병렬성을 활용해 필요에 따라 자동으로 시스템 규모가 확장되지 않음. 따라서 미리 부하를 예측해서 잠재적인 병렬성 수준을 미리 지정해야함
  - 디버깅을 활성화하려면 발생한 예외를 작업 스레드에서 수동으로 잡아 Queue를 전달함으로써 주 스레드에서 다시 발생시켜야 함
- 하지만 이 코드의 가장 큰 문제점은 요구 사항이 다시 변경될 떄 들어남. 예를 들어 `game_logic`
뿐 아니라 `count_neighbors` 함수에서도 I/O를 수행해야 한다고 가정해보자
~~~python
def count_neighbors(y, x, get):
    ...
    # 여기서 블로킹 #I/O를 수행함
    data = my_socket.recv(100)
    ...
~~~
- 이 코드를 병렬화하려면 `count_neighbors`를 별도의 스레드에서 실행하는 단계를 파이프라인에 추가해야함
- 이때 작업자 스레드 사이에서 예외가 제대로 전달돼 주 스레드까지 도달하는지 확인해야함
- 그리고 작업자 스레드 사이의 동기화를 위해 Grid 클래스에 대해 Lock을 사용해야 함
- `count_neighbors_thread` 작업자와 그에 해당하는 Thread 인스턴스를 위해 또 다른 Queue 인스턴스 집합을 만들어야 함
- 마지막으로 파이프라인의 여러 단계를 조율하고 작업을 제대로 팬아웃하거나 팬인하도록 `simulate_phased_pipeline`를 변경해야 함
- 바꾼 구현을 사용하면 다단계로 변경한 파이프라인을 처음부터 끝까지 실행할 수 있음
~~~python
from queue import Queue
from threading import Thread
from threading import Lock
import time

from queue import Queue

class ClosableQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return   # 스레드를 종료시킨다
                yield item
            finally:
                self.task_done()

in_queue = ClosableQueue()
logic_queue = ClosableQueue()
out_queue = ClosableQueue()

class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue, **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)

ALIVE = '*'
EMPTY = '-'

class SimulationError(Exception):
    pass

class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def get(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def set(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

    def __str__(self):
        output = ''
        for row in self.rows:
            for cell in row:
                output += cell
            output += '\n'
        return output

class LockingGrid(Grid):
    def __init__(self, height, width):
        super().__init__(height, width)
        self.lock = Lock()

    def __str__(self):
        with self.lock:
            return super().__str__()

    def get(self, y, x):
        with self.lock:
            return super().get(y, x)

    def set(self, y, x, state):
        with self.lock:
            return super().set(y, x, state)

def count_neighbors(y, x, get):
    n_ = get(y - 1, x + 0) # 북(N)
    ne = get(y - 1, x + 1) # 북동(NE)
    e_ = get(y + 0, x + 1) # 동(E)
    se = get(y + 1, x + 1) # 남동(SE)
    s_ = get(y + 1, x + 0) # 남(S)
    sw = get(y + 1, x - 1) # 남서(SW)
    w_ = get(y + 0, x - 1) # 서(W)
    nw = get(y - 1, x - 1) # 북서(NW)
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    # 여기서 블러킹 I/O를 수행한다
    #data = my_socket.recv(100)
    return count

def count_neighbors_thread(item):
    y, x, state, get = item
    try:
        neighbors = count_neighbors(y, x, get)
    except Exception as e:
        neighbors = e
    return (y, x, state, neighbors)

def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY # 살아 있는 이웃이 너무 적음: 죽음
        elif neighbors > 3:
            return EMPTY # 살아 있는 이웃이 너무 많음: 죽음
    else:
        if neighbors == 3:
            return ALIVE # 다시 생성됨

    # 여기서 블러킹 I/O를 수행한다
    #data = my_socket.recv(100)
    return state

def game_logic_thread(item):
    y, x, state, neighbors = item
    try:
        next_state = game_logic(state, neighbors)
    except Exception as e:
        next_state = e
    return (y, x, next_state)

# 스레드를 미리 시작한다
threads = []

for _ in range(5):
    thread = StoppableWorker(
        count_neighbors_thread, in_queue, logic_queue)
    thread.start()
    threads.append(thread)

for _ in range(5):
    thread = StoppableWorker(
        game_logic_thread, logic_queue, out_queue)
    thread.start()
    threads.append(thread)

def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)

class ColumnPrinter:
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(
                row_count, len(data.splitlines()) + 1)

        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line

                if (i + 1) < len(self.columns):
                    rows[j] += ' | '

        return '\n'.join(rows)


def simulate_phased_pipeline(
        grid, in_queue, logic_queue, out_queue):
    for y in range(grid.height):
        for x in range(grid.width):
            state = grid.get(y, x)
            item = (y, x, state, grid.get)
            in_queue.put(item)  # 팬아웃

    in_queue.join()
    logic_queue.join()  # 파이프라인을 순서대로 실행한다
    out_queue.close()

    next_grid = LockingGrid(grid.height, grid.width)
    for item in out_queue:  # 팬인
        y, x, next_state = item
        if isinstance(next_state, Exception):
            raise SimulationError(y, x) from next_state
        next_grid.set(y, x, next_state)
    return next_grid

grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = simulate_phased_pipeline(
        grid, in_queue, logic_queue, out_queue)

print(columns)

for thread in threads:
    in_queue.close()
for thread in threads:
    logic_queue.close()
for thread in threads:
    thread.join()
~~~
- 코드는 예상대로 작동하지만, 변경할 부분이 아주 많고, 준비 코드도 많이 필요함
- 또한 Queue가 팬아웃과 팬인 문제를 해결해줄 수는 있지만 부가 비용이 아주 높다는 사실도 중요
- Thread를 사용하는 방식 보다는 낫지만, Queue는 파이썬이 제공하는 다른 도구만큼 좋지 못함

#### 기억해야 할 내용
- 작업자 스레드 수를 고정하고 Queue를 함께 사용하면 스레드를 사용할 때 팬인과 팬아웃의 규모 확장성을 개선할 수 있음
- Queue를 사용하도록 기존 소스를 리펙터링하면 상당히 많은 작업이 필요함. 특히 다단계로 이뤄진 파이프라인이 필요하면 작업량이 더 늘어남
- 다른 파이썬 내장 기능이나 모듈이 제공하는 병렬 I/O를 가능하게 해주는 다른 기능과 비교하면, Queue는 프로그램이 활용할 수 있는 전체 I/O의 병렬성 정도를 제한한다는 단점이 있음

### 59-동시성을 위해 스레드가 필요한 경우에는 ThreadpoolExecutor를 사용해라
- 파이선에는 `concurrent.funtures` 라는 내장 모듈이 있음
- 이 모듈은 `ThreadPool Excutor` 클래스를 제공함. `ThreadPoolExcutor`는 Thread와 Queue를 사용한 접근 방법들의 장점을 조합해 생명 게임 예제의 병렬 I/O 문제를 해결함
~~~python
ALIVE = '*'
EMPTY = '-'

class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def get(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def set(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

    def __str__(self):
        output = ''
        for row in self.rows:
            for cell in row:
                output += cell
            output += '\n'
        return output

class LockingGrid(Grid):
    def __init__(self, height, width):
        super().__init__(height, width)
        self.lock = Lock()

    def __str__(self):
        with self.lock:
            return super().__str__()

    def get(self, y, x):
        with self.lock:
            return super().get(y, x)

    def set(self, y, x, state):
        with self.lock:
            return super().set(y, x, state)

def count_neighbors(y, x, get):
    n_ = get(y - 1, x + 0) # 북(N)
    ne = get(y - 1, x + 1) # 북동(NE)
    e_ = get(y + 0, x + 1) # 동(E)
    se = get(y + 1, x + 1) # 남동(SE)
    s_ = get(y + 1, x + 0) # 남(S)
    sw = get(y + 1, x - 1) # 남서(SW)
    w_ = get(y + 0, x - 1) # 서(W)
    nw = get(y - 1, x - 1) # 북서(NW)
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    # 여기서 블러킹 I/O를 수행한다
    #data = my_socket.recv(100)
    return count

def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY # 살아 있는 이웃이 너무 적음: 죽음
        elif neighbors > 3:
            return EMPTY # 살아 있는 이웃이 너무 많음: 죽음
    else:
        if neighbors == 3:
            return ALIVE # 다시 생성됨

    # 여기서 블러킹 I/O를 수행한다
    #data = my_socket.recv(100)
    return state

def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = game_logic(state, neighbors)
    set(y, x, next_state)
~~~
- Grid의 객 셀에 대해 새 Thread 인스턴스를 시작하는 대신, <b>함수를 실행기(executor)에 제출함으로써 팬아웃 할 수 있음. 실행기는 제출받은 함수를 별도의 스레드에서 수행해줌</b>
- 나중에 다음과 같이 팬인하기 위해 모든 작업의 결과를 기다릴 수 있음
~~~python
def simulate_pool(pool, grid):
    next_grid = LockingGrid(grid.height, grid.width)
    futures = []
    for y in range(grid.height):
        for x in range(grid.width):
            args = (y, x, grid.get, next_grid.set)
            future = pool.submit(step_cell, * args) #- 팬아웃
            futures.append(future)

    for future in futures:
        future.result()        #- 팬인

    return next_grid
~~~
- 실행기는 사용할 스레드를 미리 할당함. 따라서 `simulate_pool`을 실행할 때마다 스레드를 시작하는데 필요한 비용이 들지 않음
- 또한 병렬 I/O 문제를 처리하기 위해 Thread를 별 생각 없이 사용하면 memory 문제가 발생할 수 있는데, 이 문제를 해결하기 위해 <b>스레드 풀(pool)에 사용할 스레드의 최대 개수를 지정할 수도 있음</b>
~~~python
class ColumnPrinter:
    def __init__(self):
        self.columns = []

    def append(self, data):
        self.columns.append(data)

    def __str__(self):
        row_count = 1
        for data in self.columns:
            row_count = max(
                row_count, len(data.splitlines()) + 1)

        rows = [''] * row_count
        for j in range(row_count):
            for i, data in enumerate(self.columns):
                line = data.splitlines()[max(0, j - 1)]
                if j == 0:
                    padding = ' ' * (len(line) // 2)
                    rows[j] += padding + str(i) + padding
                else:
                    rows[j] += line

                if (i + 1) < len(self.columns):
                    rows[j] += ' | '

        return '\n'.join(rows)

grid = LockingGrid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
with ThreadPoolExecutor(max_workers=10) as pool:
    for i in range(5):
        columns.append(str(grid))
        grid = simulate_pool(pool, grid)
~~~
- ThreadPoolExecutor 클래스에서 가장 좋은 점은 <b>submit 메서드가 반환하는 Future 인스턴스에 대해 result 메서드를 호출하면 스레드를 실행하는 중에 발생한 예외를 자동으로 전파시켜 준다는 것임</b>
~~~python
def game_logic(state, neighbors):
    ...
    raise OSError('I/O 문제 발생')
    ...

with ThreadPoolExecutor(max_workers=10) as pool:
    task = pool.submit(game_logic, ALIVE, 3)
    task.result()

>>>
Traceback
OSError: I/O 문제발생 
~~~
- `game_logic` 함수와 더불어 `count_neighbors` 함수에 I/O 병렬성을 제공해야 할 때도 `ThreadPoolExecutor`가 `step_cell`의 일부분으로 이 두 함수를 이미 동시에 실행하고 있기 때문에 별도로 프로그램을 변경하지 않아도 됨   
- 심지어 필요하면 같은 인터페이스를 사용해 CPU 병렬성을 달성할 수도 있음
- 하지만 ThreadPoolExecutor가 제한된 수의 I/O 병렬성만 제공한다는 큰 문제점이 남아 있음
- `max_workers` 파라미터를 100으로 설정한다고 해도, 규모를 확장할 수 없음
- `ThreadPoolExecutor`는 비동기적인 해법이 존재하지 않는 상황을 처리할 때는 좋은 방법이지만, 그 외 많은 경우에는 I/O 병렬성을 최대화할 수 있는 더 나은 방법이 존재함

#### 기억해야 할 내용
- `ThreadPoolExecutor`를 사용하면 한정된 리펙터링만으로 간단한 I/O 병렬성을 활성화 할 수 있고, 동시성을 팬아웃해야 하는 경우에 발생하는 스레드 시작 비용을 쉽게 줄일 수 있음
- `ThreadPoolExecutor`를 사용하면 스레드를 직접 사용할 때 발생할 수 있는 잠재적인 메모리 낭비 문제를 없애주지만, `max_workers`의 개수를 미리 정해야하므로 I/O 병렬성을 제한함

### 60- I/O를 할 때는 코루틴을 사용해 동시성을 높여라
- better-way 56~59에서는 생명 게임 예제를 사용해 병렬 I/O 문제를 해결하려 노력했지만 수천 개의 동시성 함수를 다룰 때 다른 접근 방식은 모두 한계가 있음
- <b>파이썬은 높은 I/O 동시성을 처리하기 위해 코루틴을 사용함</b>
- 코루틴을 사용하면 파이썬 프로그램 안에서 동시에 실행되는 것처럼 보이는 함수를 아주 많이 쓸 수 있음
- 코루틴은 `async`와 `await` 키워드를 사용해 구현되며, 제너레이터를 실행하기 위한 인프라를 사용함
- 코루틴을 시작하는 비용은 함수 호출뿐. 활성화된 코루틴은 종료될 때까지 1KB 미만의 메모리를 사용함
- 스레드와 마찬가지로 코루틴도 환경으로부터 입력을 소비하고 결과를 출력할 수 있는 독립적인 함수
- 코루틴과 스레드를 비교해보면, 코루틴은 매 `await` 식에서 일시 중단되고 일시 중단된 대기 가능성이 해결된 다음에 `async` 함수로부터 실행을 재개한다는 차이점이 있음(이는 제너레이터의 yield 동작과 비슷)
- 여러 분리된 `async` 함수가 서로 장단을 맞춰 실행되면 마치 모든 `async` 함수가 동시에 실행되는 것처럼 보이며, 이를 통해 파이썬 스레드의 동시성 동작을 흉내 낼 수 있음
- 하지만 이런 동작을 하는 코루틴은 스레드와 달리 메모리 부가 비용이나 시작 비용, 컨텍스트 전환 비용이 들지 않고 복잡한 락과 동기화 코드가 필요하지 않음
- 코루틴을 가능하게 하는 마법과 같은 매커니즘은 이벤트 루프(event loop)로, 다수의 I/O를 효율적으로 동시에 실행할 수 있고 이벤트 루프에 맞춰 작성된 함수들을 빠르게 전환해가며 골고루 실행할 수 있음
- 코루틴을 통해 생명 게임을 구현해보자. 이전 Thread나 Queue를 사용한 방법에 나타난 문제를 극복하면서 game_logic 함수 안에서 I/O를 발생시키는 것이 그 목표
- 먼저 이를 위해 `def` -> `async def`로 정의하면 `game_logic` 함수를 코루틴으로 만들 수 있음을 알아둬야 함
- 이렇게 `async def`로 함수를 정의하면 그 함수 안에서 I/O에 `await` 구문을 사용할 수 있음
~~~python
ALIVE = "*"
EMPTY = "-"

class Grid:
    ...

def count_neighbors(y, x, get):
    ...

async def game_logic(state, neighbors):
    ...

    #- 여기서 I/O를 수행함
    data = await my_socket.read(50)
~~~
- 비슷한 방식으로 `step_cell`의 정의에 `async`를 추가하고 `game_logic` 함수 호출 앞에 `await`를 덧붙이면 `step_cell`을 코루틴으로 바꿀 수 있음
~~~python
async def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = count_neighbors(y, x, get)
    next_state = await game_logic(state, neighbors)
    set(y, x, next_state)
~~~
- 그리고 simuate 함수도 코루틴으로 만들어야 함
~~~python
async def simulate(grid):
    next_grid = Grid(grid.height, grid.width)

    tasks = []
    for y in range(grid.height):
        for x in range(grid.width):
            task = step_cell(
                y, x, grid.get, next_grid.set)  # 팬아웃
            tasks.append(task)

    await asyncio.gather(*tasks)  # 팬인

    return next_grid
~~~
- `simulate` 함수의 코루틴 버전을 좀 더 자세히 살펴보자
  - `step_cell` 을 호출해도 이 함수가 즉시 호출되지 않음. 대신 step_cell 호출은 나중에 `await` 식에 사용할 수 있는 `coroutine` 인스턴스를 반환함
  - 마치 `yield`를 사용하는 제너레이터 함수를 호출하면 즉시 실행되지 않고 제너레이터를 반환하는 것과 같음
  - 이와 같은 실행 연기 메커니즘이 팬아웃을 수행함
  - `asyncio` 내장 라이브러리가 제공하는 `gather` 함수는 팬인을 수행함. 
  - `gather`에 대해 적용한 `await` 식은 이벤트 루프가 `step_cell` 코루틴을 동시에 실행하면서 `step_cell` 코루틴이 완료될 때마다 `simulate` 코루틴 실행을 재개하라고 요청함
  - 모든 실행이 단일 스레드에서 이뤄지므로 Grid 인스턴스에 락을 사용할 필요가 없음
  - I/O는 asyncio가 제공하는 이벤트 루프의 일부분으로 병렬화됨
- 마지막으로 구동 코드 한 줄만 바꾸면 이 절에서 구현한 생명 게임을 구동할 수 있음
- 새로운 코드는 `asyncio.run` 함수를 사용해 simulate 코루틴을 이벤트 루프상에서 실행하고 각 함수가 의존하는 I/O를 수행함
~~~python
grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    # python 3.7이상에서만 asyncio.run을 제공함
    grid = asyncio.run(simulate(grid)) # 이벤트 루프를 실행한다

print(columns)
~~~
- 결과는 예전과 같다. 스레드와 관련된 모든 부가 비용이 제거됨
- Queue나 ThreadPoolExecutor 접근 방법은 예외 처리에 한계가 있었지만(예외를 스레드 경계에서 다시 발생시켜야 했음), 코루틴에서는 대화형 디버거를 사용해 코드를 한 줄씩 실행시켜볼 수 있음
~~~python
async def game_logic(state, neighbors):
    ...
    raise OSError('I/O 문제 발생')
    ...

asyncio.run(game_logic(ALIVE, 3))
~~~
- 나중에 요구 사항이 변경돼 `count_neighbors`에서 I/O를 수행해야 한다면 Thread나 Queue 인스턴스를 사용할 때 모든 코드의 구조를 변경했던 것과 달리, 기존 함수와 함수 호출 부분에 `async`와 `await`를 붙이면 바뀐 요구 사항을 쉽게 달성할 수 있음
~~~python
async def count_neighbors(y, x, get):
    n_ = get(y - 1, x + 0) # 북(N)
    ne = get(y - 1, x + 1) # 북동(NE)
    e_ = get(y + 0, x + 1) # 동(E)
    se = get(y + 1, x + 1) # 남동(SE)
    s_ = get(y + 1, x + 0) # 남(S)
    sw = get(y + 1, x - 1) # 남서(SW)
    w_ = get(y + 0, x - 1) # 서(W)
    nw = get(y - 1, x - 1) # 북서(NW)
    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    # 여기서 블러킹 I/O를 수행한다
    #data = my_socket.recv(100)
    return count

async def step_cell(y, x, get, set):
    state = get(y, x)
    neighbors = await count_neighbors(y, x, get)
    next_state = await game_logic(state, neighbors)
    set(y, x, next_state)

grid = Grid(5, 9)
grid.set(0, 3, ALIVE)
grid.set(1, 4, ALIVE)
grid.set(2, 2, ALIVE)
grid.set(2, 3, ALIVE)
grid.set(2, 4, ALIVE)

columns = ColumnPrinter()
for i in range(5):
    columns.append(str(grid))
    grid = asyncio.run(simulate(grid)) # 이벤트 루프를 실행한다

print(columns)
~~~
- 코루틴은 코드에서 외부 환경에 대한 명령과 원하는 명령을 수행하는 방법을 구현하는 것을 분리해준다는 점이 멋짐
- 코루틴을 사용하면 원하는 목표를 동시성을 사용해 달성하는 방법을 알아내는 데 시간을 낭비하는 대신, 우리가 만들고 싶은 로직을 작성하는데 초점을 맞출 수 있음

#### 기억해야 할 내용
- `async` 키워드로 정의한 함수를 코루틴이라고 부름. 코루틴을 호출하는 호출자는 `await` 키워드를 사용해 자신이 의존하는 코루틴의 결과를 받을 수 있음
- 코루틴은 수만 개의 함수가 동시에 실행되는 것처럼 보이게 만드는 효과적인 방법을 제공
- I/O를 병렬화하면서 스레드로 I/O를 수행할 때 발생할 수 있는 문제를 극복하기 위해 팬인과 팬아웃에 코루틴을 사용할 수 있음

### 61-스레드를 사용한 I/O를 어떻게 asyncio로 포팅할 수 있는지 알아두라
- 코루틴의 장점을 이해한 뒤에는 코루틴을 사용하고자 기존 코드베이스를 포팅하기가 두려울 수 있음
- 다행히 파이썬의 비동기 지원은 파이썬 언어에 잘 통합돼 있음. 따라서 스레드와 블로킹 I/O를 사용하는 코드를 코루틴과 비동기 I/O를 사용하는 코드로 옮기기 쉬움
- 예를 들어 숫자를 추측해주는 게임을 실행해주는 TCP 기반의 서버를 생각해보자
- 이 서버는 고려할 숫자의 범위를 표현하는 lower와 upper 파라미터를 받음. 그 후 클라이언트가 요청할 때마다 서버는 이 범위 안의 숫자를 반환함
- 마지막으로 서버는 자신이 추측한 숫자가 클라이언트가 정한 비밀의 수에 가까운지(따뜻함), 아니면 먼지(차가움)에 대한 정보를 클라이언트로부터 받음
- 이런 유형의 클라이언트/서버 시스템을 구축하는 가장 일반적인 방법은 블로킹 I/O와 스레드를 사용하는 것
- 그러려면 메세지 송수신을 처리하는 도우미 클래스가 필요함
- 이 경우 서버가 보내거나 받는 메세지 한 줄 한 줄은 처리할 명령을 표현
~~~python
class ConnectionBase:
    def __init__(self, connection):
        self.connection = connection
        self.file = connection.makefile('rb')

    def send(self, command):
        line = command + "\n"
        data = line.encode()
        self.connection.send(data)

    def receive(self):
        line = self.file.readline()
        if not line:
            raise EOFError('Connection closed')
        return line[:-1].decode()
~~~
- 서버는 한 번에 하나씩 연결을 처리하고 클라이언트의 세션 상태를 유지하는 클래스로 구현됨
~~~python
class Session(ConnectionBase):
    def __init__(self, * args):
        super().__init__(*args)
        self._clear_state(None, None)

    def _clear_state(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.secret = None
        self.guesses = []
~~~
- 이 클래스에서 가장 중요한 메서드는 다음 메서드
- 이 메서드는 클라이언트에서 들어오는 메세지를 처리해 명령에 맞는 메서드를 호출해줌
~~~python
    #- 클라이언트에게 들어오는 메세지 처리 함수 : loop
    def loop(self):
        command = self.receive()
        while command:
            parts = command.split(' ')
            if parts[0] == 'PARAMS':
                self.set_params(parts)
            elif parts[0] == 'NUMBER':
                self.send_number()
            elif parts[0] == 'REPORT':
                self.receive_report(parts)
            else:
                raise UnknownCommandError(command)
~~~
- 첫 번째 명령은 서버가 추측할 값의 상한과 하한을 결정함
~~~python
  def set_params(self, parts):
        assert len(parts) == 3
        lower = int(parts[1])
        upper = int(parts[2])
        self._clear_state(lower, upper)
~~~
- 두 번째 명령은 클라이언트에 해당하는 Session 인스턴스에 저장된 이전 상태를 바탕으로 새로운 수를 추측함
- 특히 이 코드는 서버가 파라미터가 설정된 시점 이후에 같은 수를 두 번 반복해 추측하지 않도록 보장함
~~~python
   def next_guess(self):
        if self.secret is not None:
            return self.secret

        while True:
            guess = random.randint(self.lower, self.upper)
            if guess not in self.guesses:
                return guess

    def send_number(self):
        guess = self.next_guess()
        self.guesses.append(guess)
        self.send(format(guess))
~~~
- 세 번째 명령은 서버의 추측이 따뜻한지 차가운지에 대해 클라이언트가 보낸 결과를 받은 후 Session 상태를 적절히 바꿈
~~~python
  def receive_report(self, parts):
        assert len(parts) == 2
        decision = parts[1]
        last = self.guesses[-1]
        if decision == CORRECT:
            self.secret = last

        print(f'서버: {last}는 {decision}')
~~~
- 클라이언트도 상태가 있는 클래스를 사용해 구현됨
~~~python
import contextlib
import math

class Client(ConnectionBase):
    def __init__(self, *args):
        super().__init__(*args)
        self._clear_state()

    def _clear_state(self):
        self.secret = None
        self.last_distance = None
~~~
- 추측 게임의 파라미터를 with 문을 통해 설정함으로써 서버 측의 상태를 제대로 관리하게 만듬
- 다음 메서드는 첫 번째 명령을 서버에게 보냄
~~~python
 @contextlib.contextmanager
    def session(self, lower, upper, secret):
        print(f'\n{lower}와 {upper} 사이의 숫자를 맞춰보세요!'
              f' 쉿! 그 숫자는 {secret} 입니다.')
        self.secret = secret
        self.send(f'PARAMS {lower} {upper}')
        try:
            yield
        finally:
            self._clear_state()
            self.send('PARAMS 0 -1')
~~~
- 두 번째 명령을 구현하는 다른 메서드를 사용해 새로운 추측을 서버에게 요청함
~~~python
  def request_numbers(self, count):
        for _ in range(count):
            self.send('NUMBER')
            data = self.receive()
            yield int(data)
            if self.last_distance == 0:
                return
~~~
- 세 번째 명령을 구현하는 마지막 메서드를 통해 서버가 돌려준 추측이 마지막으로 결과를 알려준 추측보다 더 차갑거나 따뜻한지를 알려줌
~~~python
    def report_outcome(self, number):
        new_distance = math.fabs(number - self.secret)
        decision = UNSURE

        if new_distance == 0:
            decision = CORRECT
        elif self.last_distance is None:
            pass
        elif new_distance < self.last_distance:
            decision = WARMER
        elif new_distance > self.last_distance:
            decision = COLDER

        self.last_distance = new_distance

        self.send(f'REPORT {decision}')
        return decision
~~~
- 소켈에 리슨하는 스레드를 하나 사용하고 새 연결이 들어올 때마다 스레드를 추가로 시작하는 방식으로 서버를 실행함
~~~python
import socket
from threading import Thread


def handle_connection(connection):
    with connection:
        session = Session(connection)
        try:
            session.loop()
        except EOFError:
            pass


def run_server(address):
    with socket.socket() as listener:
        listener.bind(address)
        listener.listen()
        while True:
            connection, _ = listener.accept()
            thread = Thread(target=handle_connection,
                            args=(connection,),
                            daemon=True)
            thread.start()
~~~
- 클라이언트는 주 스레드에서 실행되며 추측 게임의 결과를 호출한 쪽에 돌려줌
- 이 코드는 명시적으로 다양한 파이썬 언어 기능을 활용함
- 앞으로 각 기능을 코루틴으로 어떻게 포팅할 수 있는지 살펴보자
~~~python
def run_client(address):
    with socket.create_connection(address) as connection:
        client = Client(connection)

        with client.session(1, 5, 3):
            results = [(x, client.report_outcome(x))
                       for x in client.request_numbers(5)]

        with client.session(10, 15, 12):
            for number in client.request_numbers(5):
                outcome = client.report_outcome(number)
                results.append((number, outcome))

    return results
~~~
- 마지막으로 지금까지 만든 모든 요소를 하나로 붙여 제대로 작동하는지 확인
~~~python
def main():
    address = ('127.0.0.1', 1234)
    server_thread = Thread(
        target=run_server, args=(address,), daemon=True)
    server_thread.start()

    results = run_client(address)
    for number, outcome in results:
        print(f'클라이언트: {number}는 {outcome}')

main()
~~~
- 이 예제를 async, await, asyncio 내장 모듈을 사용해 변환하려면 얼마나 많은 노력이 필요할까?
- 먼저 ConnectionBase 클래스가 블로킹 I/O대신 send와 receive라는 코루틴을 제공하게 바꿔야 함
- 앞에서 본 코드와 새로운 코드의 차이를 명확히 보여주고자 변경된 부분에 `#변경됨` 이라고 주석을 넣음
~~~python
# python 3.8 이상에서만 실행됨(walus연산자때문)

class EOFError(Exception):
    pass


class AsyncConnectionBase:
    def __init__(self, reader, writer):  # 변경됨
        self.reader = reader  # 변경됨
        self.writer = writer  # 변경됨

    async def send(self, command):
        line = command + '\n'
        data = line.encode()
        self.writer.write(data)  # 변경됨
        await self.writer.drain()  # 변경됨

    async def receive(self):
        line = await self.reader.readline()  # 변경됨
        if not line:
            raise EOFError('연결 닫힘')
        return line[:-1].decode()
~~~


## 용어 정리
- 업스트림, 다운스트림
  - 업스트림: 로컬에서 서버로 전달되는 데이터의 흐름
  - 다운스트림: 서버에서 로컬로 전달되는 데이터의 흐름  
- event loop
  - 
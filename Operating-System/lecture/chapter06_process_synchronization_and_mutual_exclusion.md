# chapter06 Process Synchronization and mutual exclusion
## Process Synchronization (동기화)
- 다중 프로그래밍 시스템
  - 여러 개의 프로세스가 존재
  - 프로세스들은 서로 독립적으로 동작
  - 공유 자원 또는 데이터가 있을 때, 문제 발생 가능
- 동기화(Synchronization)
  - 프로세스들이 서로 동작을 맞추는 것
  - 프로세스들이 서로 정보를 공유하는 것

## Asynchronous and Concurrent P's
- 비동기적(Asynchronous)
  - 프로세스들이 서로에 대해 모름
- 병행적(Concurrent)
  - 여러 개의 프로세스들이 동시에 시스템에 존재
- 병행 수행중인 비동기적 프로세스들이 공유 자원에 동시 접근할 때 문제가 발생 할 수 있음

## Terminologies
- Shared data(공유 데이터)
  - 여러 프로세스들이 공유하는 데이터
- Critical section(임계 영역)
  - 공유 데이터를 접근하는 코드 영역(code segment)
- Mutual exclusion(상호 배제) 
  - 둘 이상의 프로세스가 동시에 critical section에 진입하는 것을 막는 것

![img](https://github.com/koni114/Operating-system/blob/master/img/os_14.JPG)

- 기계어 명령(machine instruction)의 특성
  - 실제로 processor가 실행하는 가장 작은 단위의 명령어
  - Atomicity(원자성), indivisible(분리불가능)의 특성을 가짐
  - 한 기계어 명령의 실행 도중에 인터럽트 받지 않음

- 다음의 그림에서는 크게 두 가지 경우에 따라 sdata의 결괏값이 달라질 수 있음

![img](https://github.com/koni114/Operating-system/blob/master/img/os_15.JPG)

- 위의 그림은 기본적인 기계어 표현법
- 왼쪽 process-P(i)는 sdata의 값을 Register 값 R(j)에 블러오고, 해당 레지스터에 1을 더하고, 다시 sdata에  
  더하라는 3단계로 구성됨. 왼쪽도 마찬가지임
- CPU의 작업은 레지스터에 있는 데이터만 가지고 작업을 수행함. 즉 main memory에 있는 데이터를 register에 가지고 옴
- 상황에 따라 sdata는 1이 될 수도, 2가 될 수 있음  
  why? cpu를 할당받은 상태를 running 상태라고 얘기하는데, 중간에 preemption이 일어날 수 있음  
  1번 단계에서 preemption이 일어났고, B단계에서 preemption이 일어난다면 결과적으로 sdata에 1이 들어감
- 결과적으로 명령 수행 과정에 따라서 값이 달라짐  
  - 1 -> 2 -> 3 -> A -> B -> C, A -> B -> C -> 1 -> 2 -> 3, 결과 2
  - 1 -> 2 -> A -> B -> C, 결과 sdata = 1
- 이렇게 수행 방식에 따라서 결과가 달라지는 것을 race condition 이라고 함

## Mutual Exclusion Methods
- primitives
  - 기본 연산의 의미   
- `enterCS()` primitives
  - Critical section 진입 전 검사
  - 다른 프로세스가 critical section 안에 있는지 검사 
- `exitCS()` primitive
  - Critical section을 벗어날 때의 후처리 과정
  - Critical section을 벗어남을 시스템이 알림 

## ME primitives 수행시 요구사항
- Mutual exclusion(상호배제)
  - Critical section(CS)에 프로세스가 있으면, 다른 프로세스의 진입을 금지
- Progress(진행)
  - CS안에 있는 프로세스 외에는, 다른 프로세스가 CS에 진입하는 것을 방해하면 안됨 
- Bounded waiting(한정대기)
  - 프로세스의 CS진입은 유한시간 내에 허용되어야 함

### ME primitives 
![img](https://github.com/koni114/Operating-system/blob/master/img/os_17.JPG)

- 최초의 턴은 0번 턴
- P0가 while문 전에 죽어버림. 이렇게 되면 P1은 Progress 조건을 위배함  
- P0이 수행하고 난 후에 다시 P0이 들어가려고 할 때 들어갈 수 없음. 즉 두 번 연속 진입 불가  
  progress 요건 위배

![img](https://github.com/koni114/Operating-system/blob/master/img/os_18.JPG) 

- 위의 코드는 flag를 주자! 라는 아이디어에서 출발
- 상대편의 깃발을 보고, 들려있다면 상대편이 들어가 있다라는 의미이므로, 기다려야 함
- 상대편의 깃발이 안들려있다면, 안 들어가 있으므로 들어가게 됨
- 이러한 코드는 위의 3가지 고려사항을 만족할까?   
  NO! while문을 통과하고 preemption이 발생하고 반대편에서 들어오면 ME에 위배됨

![img](https://github.com/koni114/Operating-system/blob/master/img/os_19.JPG) 

- version 2와 다른 점은 먼저 내가 들어갈 것이다! 라고 flag를 주고 while문이 시작되는데,  
  이렇게 되면 Bounded waiting 문제에 위배

## Mutual Exclusion Solutions
- SW solutions
  - Dekkers's algorithm
  - Dijkstra's algorithm
- HW solutions
  - TestAndSet(TAS) instruction
- OS supported SW solution
  - Spinlock
  - Semaphore
  - Eventcount/sequencer
- Language-Level solution
  - Monitor       

## SW solutions - Dekker's algorithm
- Two process ME를 보장하는 알고리즘
![img](https://github.com/koni114/Operating-system/blob/master/img/os_20.JPG) 

~~~c
flag[0] <- false;
flag[1] <- false;
turn <- 0; 

// P0
flag[0] <- true;          // 자신의 깃발을 먼저 듬
while(flag[1]) do         // 만약 상대편이 깃발을 먼저 들었다면. while문으로 들어감
  if(turn = 1) then       // turn --> 1이면, P1이 들어가 있다는 것이므로, flag 내리고 대기
    begin                 
      flag[0] <- false;
      while(turn = 1) do  // trun --> 0이 될때까지 대기. 바뀌면 flag 올리고 CS로 들어감
      endwhile;
      flag[0] <- true;
    end;
endwhile;
[Critical Section]
turn <- 1;
flag[0] <- false;

// P1
flag[1] <- true;
while(flag[0]) do
  if(turn = 0) then
    begin
      flag[1] <- false;
      while(trun = 0) do 
      endwhile;
      flag[1] <- true;
    end;
endwhile;
[Critical Section]
turn <- 0;
flag[1] <- false;
~~~

## SW solutions - Peterson's algorithm
- Dekker 보다 더 간단한 알고리즘
- 핵심은 깃발을 들고 서로 먼저 들어가라고 양보하는 코드를 추가

~~~c
flag[0] <- false;
flag[1] <- false;
turn <- 0;

// P0
flag[0] <- true;
turn <- 1; // P1에게 양보
while(flag[1] and turn = 1) do
endwhile;
[Critical Section]
flag[0] <- false; 

// P1
flag[1] <- true;
turn <- 0; // P0에게 양보
while(flag[0] and turn = 0) do
endwhile;
[Critical Section]
flag[1] <- false;
~~~


![img](https://github.com/koni114/Operating-system/blob/master/img/os_21.JPG) 


## SW solutions - N-preocess Mutual Exclusion

## SW solutions - Dijkstra's algorithm
- 다익스트라
  - 최초로 프로세스 n개의 상호배제 문제를 소프트웨어적으로 해결
  - 실행 시간이 가장 짧은 프로세스에 프로세서 할당하는 세마포 방법, 가장 짧은 평균 대기시간 제공
- 다익스트라 알고리즘의 flag 변수
  - idle : 프로세스가 임계 지역 진입을 시도하고 있지 않을 때
  - want-in : 프로세스의 임계 지역 진입 시도 1단계일 때
  - in-CS : 프로세스 임계 지역 진입 시도 2단계 및 임계 지역 내에 있을 때
- 들어가고 싶다고 의사를 밝힘. 1단계 : 내가 아니면 기다림. 현재 turn인 친구 idle이 끝날 때까지 기다림 
- 2단계는 많이 걸러지고 들어올 것임

![img](https://github.com/koni114/Operating-system/blob/master/img/os_22.JPG)

~~~c
/* 임계 지역 진입시도 1단계  */
flag[i] <- want-in;
while(turn != i) do // 내 턴이 아니면,
  if (flag[turn] = idle) then // CS에 들어가있는 process가 idle이 될 때 까지 기다림
    turn <- i;                // 만약 CS에서 나왔다면, 내 턴으로 바꾸고 2단계 진입
endwhile;
/* 임계 지역 진입시도 2단계  */
flag[i] <- in-CS;
j <- 0
// in-CS라는 공간에서 나혼자만 존재할 경우 CS로 들어감.
// j가 0부터 i까지 for loop를 돌면서, i가 아니거나, flag[j]의 값이 in-cs가 아니면 계속 진행
while((j < n) and (j = i or flag[j] != in-CS)) do
  j <- j + 1;
endwhile;
until(j >= n); // j를 n번 까지 검사하여 아무도 없다면 CS 진입
[Critical Section]
flag[i] <- idle;
~~~

## SW Solutions들의 문제점
- 속도가 느림  
- 구현이 복잡  
- ME primitive 실행 중 preemption 될 수 있음  
  - 공유 데이터 수정 중은 interrupt를 억제 함으로써 해결 가능  
- Busy waiting
  - 자기 차례가 오지 않았으면 계속 while 문에서 뺑뺑 돌아야 함  

## HW solutions
### Synchronization Hardware
- TestAndSet(TAS) instruction
  - Test와 Set을 한번에 수행하는 기계어
  - Machine instruction
    - Atomicity, Indivisible
    - 실행 중 interrupt를 받지 않음 (preemption 되지 않음)
  - Busy waiting
    - Inefficient

### TAS Instruction
~~~c
boolean TestAndSet(boolean *target){
    boolean temp = *target // 이전 값 기록
    *target = true;        // target에 true로 저장
    return temp;           // temp return
} 
~~~
- 위의 문장을 한 번에 수행(Machine instruction)

### ME with TAS Instruction
![img](https://github.com/koni114/Operating-system/blob/master/img/os_23.JPG)
- 시작은 lock = false. TAS function에 들어가면, lock = True로 변경되며, false가 return되면서 while문을 빠져 나감
- 이 때 새로운 녀석이 들어오면 process가 종료될 때까지 while문을 빠져나가지 못하므로, ME 성립
- 3개 process 이상의 경우, Bounded waiting 조건에 위배  
  why? 예를 들어, 여러개의 process가 들어갈 때, 특정 process는 영영 못 빠져 나올 수 있음  
- 아래 코드문에서 n-process 구문 해결 가능  
  - lock : CS안에 process가 있으면 true, 없으면 false
  - waiting[] : 기다리는 녀석이 있는지 확인  
~~~c
do // process P(i)의 진입 영역
{
    waiting[i] = true;
    key = true;
    while(waiting[i] && key)
        key = TestAndSet(&lock); // lock이 false이면, cs내 진입 가능
    waiting[i] = false;
        // 임계 영역
        [Critical Section]
        // 탈출 영역
    j = (i + 1) % n
    while((j != i) && !waiting[j]) // 대기 중인 프로세스를 찾음
        j = (j + 1) % n;
    if(j = i)                      // 대기 중인 프로세스가 없으면
        lock = false;              // cs open
    else                           // 대기 프로세스가 있으면 다음 순서로 임계 영역에 진입
        waiting[j] = false;        // Pj가 임계 영역에 진입할 수 있도록
} while(true);
~~~

## HW Solution
- 장점 : 구현이 간단
- 단점 : Busy waiting
- Busy waiting 문제를 해소한 상호 배제 기법
  - Semaphore --> 대부분의 os들이 사용하는 기법 

## OS supported SW solution
## Spinlock 
- 만약 다른 스레드나 프로세스가 lock을 소유하고 있다면, 그 lock이 반환될 때까지 계속 확인하며 기다리는 것
- 조금만 기다리면 바로 쓸 수 있는데 굳이 context switching으로 부하를 줄 필요가 있나? 라는 아이디어에서 출발
- Lock, Unlock하는 과정이 짧은 경우에 유용
- S는 정수 변수. 특정한 instant 값을 할당할 수 있는 것이 아닌, P(), V()로만 연산 가능
- 초기화, P(), V() 연산으로만 접근 가능
  - 위 연산들은 indivisible(or atomic) 연산. 즉 <b>P(), V() 연산이 preemption하다는 것을 보장</b>
    - OS support 보장
    - 전체가 한 instruction cycle에 반드시 수행 됨
- S는 물건이라고 생각
- P(S) --> 물건을 소비한다
- V(S) --> 물건을 채운다
~~~C
P(S){
    while(S <= 0) do // 물건이 없다면, 생길 때까지 기다려야 함
    endwhile;
    S <- S - 1 ;
}

V(S){
    S <- S + 1;
}
~~~
- 다음의 예시는 두 프로세스 간의 스핀락 예제(스레드가 아님을 유의)
![img](https://github.com/koni114/Operating-system/blob/master/img/os_24.JPG)
- `active` 라는 spinlock 변수가 있다고 생각
- P, V는 preemption이 보장되기 때문에 ME가 쉽게 해결됨
- 그러면, SW Solution으로 왜 이렇게 어렵게 푸느냐? 라고 할 수 있지만, 이러한 과정들이 있었기 때문에  
  쉽게 풀 수 있는 과정들을 찾아 낼 수 있게 됨
- <b>spinlock은 문제가 하나 있는데, 멀티 프로세서인 경우에만 사용 가능</b>  
  why? 두 process는 하나의 CPU에서 동시에 수행되어야 하는데, 그렇게 될 수 없음(둘 다 일을 못함)
- 일반적으로 컴퓨터에서(예를 들어 멀티 프로세서) 100개의 메모장이라는 프로세스를 동시에 실행시킬 수 있는 이유는  
  OS가 매우 빠르게 교체하면서 프로세스를 실행하기 때문
- 또한 현재 P연산과 V연산이 중간의 인터럽트 없이 one-cycle로 실행되도록 OS가 보장하기 때문에 P연산과 V연산을 수행 중에는 동시에 다른 프로세스가 한 프로세서에서 실행될 수 없음 
- busy waiting  
  - 여전히 while문에서 계속 수행되는 문제가 발생 


## Semaphore
- Busy waiting 문제를 해결할 수 있는 Semaphore를 알아보자
- 1965년 Dijkstr가 제안
- 음이 아닌 정수형 변수(S)
  - 초기화 연산, P(), V()만 접근 가능 --> spinlock과 유사
- semaphore는 차단기라는 뜻으로, P()가 차단, V()가 차단기 오픈! 이라는 뜻으로 생각할 수 있지 않나 싶음
- <b>임의의 S 변수 하나에 ready queue 하나가 할당 됨</b> 
- semaphore 를 두가지로 구분 가능
  - binary semaphore
    - S가 0과 1 두 종류의 값만 갖는 경우
    - 상호배제나 프로세스 동기화의 목적으로 사용
  - Counting semaphore
    - S가 0이상의 정수값을 가질 수 있는 경우
    - Producer-Consumer 문제 등을 해결하기 위해 사용
      - 생산자-소비자 문제
- 코드의 구성
  - 초기화 연산 --> S 변수에 초기값을 부여하는 연산
  - P() 연산, V() 연산이 존재(spinlock과 비슷)
~~~c
P(S){
    if(S > 0){
        then S <- S - 1;
        else wait on the queue Q(s); // 물건이 없을 때는 ready queue에 들어가서 기다림. block된 상태
    }
}

V(S){
    if(waiting processes on Q(s)){ // 대기실에 기다리는 애가 있으면 깨우고 나오면 됨
        then wakeup one of them;
        else S <- S + 1;
    }
}
~~~
- 모두 invisible 연산
  - OS support를 보장
  - 전체가 한 instruction cycle에 수행 됨

### Semaphore in OSs
- 실제 Semaphore를 어디서 사용할끼? 
  - windows, Unix/Linux 에서 실제 지원하는 것을 확인할 수 있음

### Semaphore로 해결할 수 있는 문제들
- 상호배제 문제
- 프로세스 동기화 문제
- 생산자-소비자(producer-consumer) 문제
- Reader-writer 문제
- Dining philosopher 문제
- 기타..

### Mutial exclusion 문제
![img](https://github.com/koni114/Operating-system/blob/master/img/os_25.JPG)

- spinlock과 다른 점을 꼭 기억하자 --> ready queue

### Process-synchronization
- process들의 실행 순서를 맞출 수 있음
  - 프로세스들은 병행적이며, 비동기적으로 수행   
![img](https://github.com/koni114/Operating-system/blob/master/img/os_26.JPG)

- P(j)가 수행되고 난 후에 P(i)가 수행되어야 한다고 가정해보자  
  즉 p(j)의 V() 함수 수행 후, P(i)의 P() 함수 수행됨. 또한 lock 변수인 sync(물건이라고 생각하면 편함)  
  를 최초에 P(j)가 먼저 들고 있다고 생각
- P(j)가 V()를 먼저 수행. 수행되고 난 후에 P(i)의 ready queue에 들리지 않고 바로 P()가 수행  
  만약 수행되고 있는 시점에 P(i)가 수행하려고 한다면, sync = 0 이므로, ready queue에서 대기!

### Producer-Consumer problem
- 생산자(Producer) 프로세스
  - 메세지를 생성하는 프로세스 그룹
- 소비자(Consumer) 프로세스
  - 메세지를 전달받는 프로세스 그룹

![img](https://github.com/koni114/Operating-system/blob/master/img/os_27.JPG)

- producer process는 드라이버, 컴파일러, 어셈블러 등의 무언가의 데이터를 생산하려는 녀석들이고, Consumer process는 라인 프린터, 어셈블러, 로더처럼 실제 데이터를 소비하여 행동하는 녀석들임
- 이 때 buffer에 producer가 생성한 녀석들을 담게 되는데, 물건을 놓는 동안에 가져가면 안되고, 물건을 두는 동안에 또 다른 녀석이 물건을 두는 행위가 일어나서는 안됨. 즉 동기화가 필요
- 먼저 간단하게 single buffer 부터 풀어보자!

### sigle buffer Producer-consumer problem
![img](https://github.com/koni114/Operating-system/blob/master/img/os_28.JPG)
- buffer가 single이라는 것은 buffer에 물건을 둘 때 가져가거나 또 둘 수 없고, 가져갈 때 두거나 또 다른 녀석이 가져가는 행위가 안된다는 것
- consumed --> 소비되었다면 1, 소비되지 않았다면 0. 초기값은 1
- produced --> 생산되었다면 1, 생산되지 않았다면 0. 초기값은 0
- Producer Pi 측면
  - message M을 생성해서 buffer에 저장하려고 함
  - buffer 소비가 되었으면(consumed) P() 수행(consumed -> 0으로 바뀜) 
  - buffer에 message 추가
  - 생산이 되었으면(produced) V() 수행(produced -> 1로 바뀜)
- Consumer Cj 측면
  - 생산이 되었으면(produced == 1) P() 수행  
    생산이 안되었다면(produced == 0) ready queue에서 대기
  - m에 buffer 값 저장
  - 소비가 되었으면(consumed) V() 수행

### N-buffers Producer-consumer problem
- circular queue를 이용하여 문제 해결 가능
- 삽입 위치의 포인터(In), 제거 위치의 포인터(Out)
![img](https://github.com/koni114/Operating-system/blob/master/img/os_29.JPG) 
- circular queue를 사용하여 물건을 놓는 지점(in), 물건을 가져가는 지점(out)이 있음을 기억하자

![img](https://github.com/koni114/Operating-system/blob/master/img/os_30.JPG)
- mutexP, mutexC --> 생산자, 소비자 process가 한번에 한명만 쓰라는 의미의 변수
- CS는 Producer 같은 경우는 P(nrempty) - V(nrfull) 구간이 되며, Consumer는 P(nrfull) - V(nrempty)가 됨
- nrfull --> buffer에 차 있는 수
  nrempty --> buffer에 비어 있는 수  
  nrfull + nrempty = 물건의 수(N)      
- Producer
  - 공간이 있는지 확인(P(nrempty)) 
  - 공간이 없으면 공간이 생길때 까지 queue에 대기
  - 공간이 있으면 물건을 buffer에 두고(buffer[in] <- M)
  - 어디에 물건을 두면 되는지 다음 위치를 update(in <- ((in + 1) % mod N))  
  - 나오면서 물건 수 하나 늘려주고 나오면 됨(V(nrfull))
- Consumer
  - 물건이 있는지 확인(P(nrfull))
  - 물건이 없으면 물건이 생길때 까지 queue에 대기
  - 물건이 있으면 물건을 꺼내고(m <- buffer[out])
  - 물건 위치를 갱신해주고(out <- (out+1) % mod N)
  - 나오면서 공간 수 하나 늘려주고 나오면 됨(V(nrempty)) 

~~~c
nrfull = 0;  // buffer에 꽉차 있는 수
nrempty = N; // buffer에 비어있는 수
mutexP = 1;  // 동기화를 위하여 생산자가 동시에 수행하지 못하도록 하는 변수
mutexC = 1;  // 동기화를 위하여 소비자가 동시에 수행하지 못하도록 하는 변수
buffer = []  // message buffer
in, out = 0,N-1; // message를 두는 지점과 가져가는 지점의 위치 인덱스

// Producer Pi
create a new message M;
P(mutexP);
P(nrempty);
buffer[in] <- M;
in <- (in + 1) mod N;
v(nrfull);
v(mutexP); 

// Consumer Cj
P(mutexC);
P(nrfull);
m <- buffer[out];
out <- (out+1) mod N;
V(nrempty);
V(mutexC);
~~~



### Reader-Writer Problem
- Reader
  - 데이터에 대해 읽기 연산만 수행 
- Writer
  - 데이터에 대해 갱신 연산을 수행
- 데이터 무결성 보장 필요
  - Reader들은 동시에 데이터 접근 가능
  - Writer들이 동시 데이터 접근 시, 상호배제(동기화) 필요
  - Reader들이 읽고 있을 때, Writer들은 접근할 수 없음
  - 반대로 Writer들이 쓰고 있을 때, Reader들은 읽을 수 없음
- 해결법
  - reader / writer에 대한 우선권 부여
    - reader preference solution  
      --> 내가 읽고 있을 때, writer와 다른 reader가 접근했을 때, reader에게 우선권이 주어지는 case      
    - writer preference solution      
- 이번 예제는 reader preference solution 예제를 semaphore로 해결해보자

### Redaer-Writer problem(reader preference solution)
![img](https://github.com/koni114/Operating-system/blob/master/img/os_47.JPG)

- Writer Wj
  - writer는 한명만 쓸 수 있기 때문에 간단함
- Reader Ri
  - 전체 코드를 다음과 같이 3단계로 구분해서 보자  
    - P(rmutex) - V(rmutex) 
    - Perform read operations;  
    - P(rmutex) - V(rmutex)
  - 첫 단계는 읽으러 들어가기 전에 <b>사전 작업</b>을 수행
    - 사전 작업은 reader 중 한 명만 할 수 있음
    - 먼저 reader의 수를 check
      - 0명이면 reader에게 우선권을 주기 위하여 writer에 대한 P연산 수행(P(wmutex))
      - 0보다 크다면 누군가 위의 작업을 수행했으므로, 작업할 필요 없음
      - nreaders에 1명 추가(nreaders <- nreaders + 1)
    - 사전 작업 검토를 여러명이 들어와서 수행하면 안되므로, CS로 구분 지음
  - 읽는 것은 동시에 해도 상관이 없음(Perform reads operations)
  - 나갈 때 사후 작업을 하는 영역 수행
    - 일단 내가 나가야 함(nreaders <- nreaders -1)
    - 만약 내가 마지막 reader라면, writer에 대한 mutex를 풀어줌(V(rmutex))    

### Semaphore 장단점
- No busy waitings
  - 기다려야 하는 프로세스는 block(asleep) 상태가 됨
- Semaphore queue에 대한 wake-up 순서는 비결정적
  - Starvation problem   

## Eventcount/Sequencer
- semaphore에서의 queue 순서의 문제를 해결하기 위한 방법
- 은행의 번호표와 비슷한 개념
- Sequencer
  - 정수형 변수
  - 은행에서의 번호표를 뽑아주는 기계라고 생각하면 됨
  - 생성시 0으로 초기화, 감소하지 않음
  - 발생 사건들의 순서 유지
  - ticket() 연산으로만 접근 가능 
- ticket(S)
  - ticket을 뽑는 행위
  - Sequencer의 번호가 뽑혀나옴  
  - 현재까지 ticket() 연산이 호출 된 횟수를 반환
  - Invisible operation   
- Eventcount
  - 은행원이 버튼을 눌러 번호를 부르는 행위 
  - 정수형 변수
  - 생성시 0으로 초기화, 감소하지 않음
  - 특정 사건의 발생 횟수를 기록
  - `read(E)`, `advance(E)`, `await(E, v)` 연산으로만 접근 가능
- read(E)
  - 현재 번호가 몇번인지 보고 있는 행위
  - 현재 Eventcount 값 반환
- advanced(E)
  - 은행원이 띵동 버튼을 누르는 행위 
  - E <- E + 1
  - E를 기다리고 있는 프로세스를 깨움(wake-up)    
- await(E, v)
  - V는 정수형 변수
  - V는 내 번호표, E는 전광판의 번호라고 생각하면 됨
  - 내 번호표 번호가 전광판의 번호보다 크면, 대기실(Q(e))에 프로세스를 전달하여 깨워달라고 CPU scheduler에게 요청(push)
  - if(E < v) E에 연결된 Qe에 프로세스 전달(push) 및 CPU scheduler 호출  

### Mutual exclusion
![img](https://github.com/koni114/Operating-system/blob/master/img/os_31.JPG)

- process 1이 도착
- 번호표를 뽑음(ticket(S)). 뽑음과 동시에 sequence는 2로 증가
- 전광판 번호를 확인하여 내 번호표와 같은지 확인(E == v?) 
- 같으므로 critical section으로 들어감
- process 1이 CS에서 수행하고 있는 중에 process 2가 도착
- 번호표를 똑같이 뽑고 전광판을 확인하는데 내 번호표가 전광판 번호보다 큼(E = 1, v = 2)
- 대기실(Qe)에 들어가 대기
- process 1이 CS에서 수행을 종료함(advance(E)). 전광판 번호가 하나 올라감(E = 2)
- 이 때 대기하고 있는 process 2가 CS로 들어감.
- ....
- 이 방법은 queue의 순서에 따라서 차례로 수행됨

### Producer-Consumer problem
![img](https://github.com/koni114/Operating-system/blob/master/img/os_32.JPG)
- Producer
  - producer는 await(In,t)과 advanced(In)을 짝지어 생각할 수 있음. 그 사이에 있는 코드문들은 CS
  - producer에서 t <- ticket(Pticket); await(In, t)는 P 연산과 동일, advanced(In)은 V 연산과 동일
  - await(Out, t - N + 1)은 공간을 체크하는 구문.  
    즉 공간이 < 1이면 기다려야 하는데, 이 때 공간은 (전체 가능 공간 - 물건을 생산한 수+ 물건을 가져간 수) --> N-t+out과 같음.  
    따라서 다음과 같은 수식으로 표현될 수 있음
- Consumer 
  - consumer는 await(Out, u)와 advanced(Out)를 짝지어 생각할 수 있음
  - u <- ticket(Cticket)과 await(Out, u)는 P 연산과 동일하고, advanced(Out)은 V 연산과 동일
  - await(In, u+1)에서 물건 수가 1개 미만 인 경우 기다려야 하므로, 
    물건수 < 1 --> In - u < 1 --> In < u + 1로 표현 가능

- No busy waiting
- No starvation
  - FIFO scheduling for Qe
- semaphore 보다 더 low-level control이 가능  

## Language-Level solution
- 앞서 배웠던 solution들은 Low-level machanisms
- Low-level machanism들은 flexible하며, Difficult to use, Error-prone  
  Logical error 발생 가능성이 높음
- Monitor는 High-level Mechanism

## High-level Mechanism
- Monitor
- Path expressions
- Serializers
- Critical region, conditional critical region
- Language-level-contructs  
  Language 단위에서 적용 
- Object-Oriented concept과 유사
- 사용이 쉬움

## Monitor
![img](https://github.com/koni114/Operating-system/blob/master/img/os_40.JPG)
- Critical Data와 Critical section을 모아둔 책방이라고 생각할 수 있음
- 책방에는 한 번에 한명만 들어올 수 있음  
  Critical Data는 책, Critical sections는 책방에서 반납/빌리는 연산이라고 생각할 수 있음
- 공유 데이터와 Critical section의 결합
- wait(), signal() operations 이라는 것들이 등장

### Monitor의 구조
- Entry queue(진입큐)
  - 모니터 내의 procedure(function) 수만큼 존재
- Mutual exclusion
  - 모니터 내에는 항상 하나의 프로세스만 진입 가능
  - language가 보장해줌
- Information hiding(정보 은폐)
  - 공유 데이터는 모니터 내의 프로세스만 접근 가능
- Condition queue(조건 큐)
  - 모니터 내의 특정 이벤트를 기다리는 프로세스가 대기
  - 조건 A를 기다리는 경우, 조건 A에 해당하는 큐에 들어감
- Signaler queue(신호제공자 큐)
  - 전화 부스 같은 것. 대기실에 전화를 검 
  - 모니터에 항상 하나의 신호제공자 큐가 존재
  - signal() 명령을 실행한 프로세스가 임시 대기

### 자원 할당 문제
![img](https://github.com/koni114/Operating-system/blob/master/img/os_34.JPG)
- R이라는 자원 1개가 있고, 한 번에 한명만 사용하게 해주는 문제
- 자원을 요청하는 function이 하나 있고, 자원을 반납하는 function 하나 있음
- Monitor 내부에는 공간이 존재하며, condition queue R_Free는 대기실과 같은 역할 수행
- signaler queue는 아까 말한 전화 부스의 역할 

![img](https://github.com/koni114/Operating-system/blob/master/img/os_35.JPG)
- 다음과 같은 자원 할당 문제에서 releaseR(), requestR() function을 직관적으로 짤 수 있음
- requestR --> 책을 빌릴 수 없으면 R_Free에서 대기. 아니면 대여해감
- releaseR --> 책을 반납하고, R_Free에서 대기하고 있는 녀석들에게 signal

### 자원 할당 시나리오
![img](https://github.com/koni114/Operating-system/blob/master/img/os_36.JPG)
- 자원 R 사용 가능. 자원은 monitor 바깥에 있음 --> Monitor 안에 프로세스 없음
- R_Avaliable 은 T/F 역할로 자원 존재 여부

![img](https://github.com/koni114/Operating-system/blob/master/img/os_37.JPG)
- 프로세스 Pj가 모니터 안에서 자원 R을 요청
- requestR()이 비었으므로, Pj는 requestR로 들어감. 들어간 후에 자원 R을 사용하러 나감
- 항상 생각해야 할 것은 monitor안에 최대 max 1명만 들어올 수 있다는 점
- 이 때 Pk, Pm 이 도착함. monitor안에는 아무도 없으니 들어오는데 자원 R은 없으므로, queue R_free에 들어감
- 다음 그림이 위의 process를 수행한 결과

![img](https://github.com/koni114/Operating-system/blob/master/img/os_38.JPG)
- Pj는 할당된 자원을 가지고 일을 수행한 후, releaseR() queue에 들어가서 반납 준비
- Monitor안에 아무도 없으므로, releaseR()에 들어가서 자원 반납
- 그 다음 R_Free에 들어있던 Pm, Pk를 깨워야 하는데, signaler queue에 들어가 잠시 자리를 피해준 후  
  깨우러 가야함

![img](https://github.com/koni114/Operating-system/blob/master/img/os_39.JPG)
- P(j)가 R 반환
- R_Free.signal() 호출에 의해 Pk가 wakeup

![img](https://github.com/koni114/Operating-system/blob/master/img/os_40.JPG)
- Pk가 자원을 빌려 나감
- <b>Pj가 남은일을 처리하러 들어옴</b>

![img](https://github.com/koni114/Operating-system/blob/master/img/os_41.JPG)

### Producer-Consumer Problem
![img](https://github.com/koni114/Operating-system/blob/master/img/os_42.JPG)

![img](https://github.com/koni114/Operating-system/blob/master/img/os_43.JPG)


### Reader-Writer problem
- reader/writer 프로세스들간의 데이터 무결성 보장 기법
- writer 프로세스에 의한 데이터 접근 시에만 상호 배제 및 동기화 필요함
- 모니터 구성
  - 변수 2개
    - 현재 읽기 작업을 진행하고 있는 reader 프로세스 수
    - 현재 writer 프로세스가 쓰기 작업을 진행 중인지 표시 
  - 조건 큐 2개
    - reader/writer 프로세스가 대기해야 할 경우에 사용 
  - 프로시져 4개 
    - reader(writer) 프로세스가 읽기(쓰기)작업을 원할 경우에 호출, 읽기(쓰기) 작업을 마쳤을 때 호출 

![img](https://github.com/koni114/Operating-system/blob/master/img/os_44.JPG)

### Dining philosopher problem
- 5명의 철학자
- 철학자들은 생각하는 일, 스파게티 먹는 일만 반복함
- 공유 자원 : 스파게티, 포크
- 스파게티를 먹기 위해서는 좌우 포크 2개 모두 들어야 함

![img](https://github.com/koni114/Operating-system/blob/master/img/os_45.JPG)

![img](https://github.com/koni114/Operating-system/blob/master/img/os_46.JPG)

### Monitor 장단점
- 장점
  - 사용이 쉽다
  - Deadlock 등 error 발생 가능성이 낮음
- 단점
  - 지원하는 언어에서만 사용 가능
  - 컴파일러가 OS를 이해하고 있어야 함
    - Critical section 접근을 위한 코드 생성  
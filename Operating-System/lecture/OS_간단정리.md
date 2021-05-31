# OS 간단 정리
## chapter01 computer system overview
- Operation System
  - HW를 효율적으로 관리해주는 SW
  - 사용자, application program에게 서비스를 제공하는 SW
- 컴퓨터 하드웨어
  - processor
  - memory
  - 주변장치
- processor
  - 컴퓨터의 두뇌(중앙처리장치)
  - 연산 수행
  - 컴퓨터의 모든 장치의 동작 제어 
- Processor 구성
  - 레지스터 <-> 제어장치 <-> 연산장치 
- 레지스터
  - 프로세서 내부에 있는 메모리
  - 프로세서가 저장할 데이터 저장
  - 컴퓨터에서 가장 빠른 메모리 
- OS는 프로세서를 관리하는 역할을 포함
- memory
  - 저장하는 장치
  - 프로그램을 저장함. ex) os, 사용자 sw, 사용자 데이터 등 
- 레지스터 <- 캐시 <- 메인 메모리 <- 보조기억장치 순으로 빠르고 비쌈 
- memory의 종류
  - 주기억장치(main memory)
    - processor는 메인 메모리까지만 접근하고, Disk는 못감
    - cpu speed는 많이 증가하였으나, disk speed는 큰 변화가 없어, 이 둘 사이의 간극을 채우기 위하여  
      main memory 등장
    - cpu가 일을 하는 동안, disk에서 main memory에 미리 가져다 둠
  - 캐시(cache)
    - cpu 안에 들어가 있으며, processor 옆에 레지스터 보다 더 멀리 있음
    - main memory와 cpu 사이의 병목 현상을 해결해 주기 위하여 존재
    - 캐시의 동작은 HW가 알아서 해결해 줌
    - processor가 우선적으로 캐시에 메모리가 있는지 확인
      - 없으면 main memory에 들려 캐시에 두고 가져감(cache miss)
      - 있으면 캐시에서 가져감(cache hit) 
  - 보조기억장치
    - ex) USB, CD, 등..
    - 프로세서가 직접 접근 할 수 없음. 쓰려면 메인 메모리에 올려놓고 사용해야 함 
    - 실행하려는 프로그램이 20GB인데, 메모리가 8GB인데 어떻게 사용 가능? --> virtual memory 
- 지역성(locality)
  - 지역성 때문에 캐시가 128kb여도 성능을 낼 수 있음
  - 공간적 지역성 : 참조한 주소와 인접한 주소를 참조하려는 특성. ex) 순차적 program
  - 시간적 지역성 : 한번 참조한 주소를 다시 참조하려는 특성. ex) for loop
- 메모리도 운영체제가 관리하는 중요한 녀석 중 하나
- 캐시는 메인 메모리에서 데이터를 가져올 때 특정 한 데이터만 가져오는 것이 아니라 block단위로 가져오기 때문에  
  공간적 지역성을 이해할 수 있음
- <b>시스템 버스(system bus)</b>  
  - 하드웨어들이 데이터 및 신호를 주고받는 통로
  - 데이터 버스, 주소 버스, 제어 버스 등이 있고, 각 개체들을 운반하는 버스라고 생각하면 됨
- 주변장치
  - 프로세서, 메모리를 제외한 하드웨어들
  - 입력장치, 출력장치, 저장장치
  - 장치 드라이버 관리
  - 인터럽트 처리
  - 파일 및 디스크 관리

## chapter02 운영체제 개요
- 운영체제의 역할
  - User Interface
  - Resource management
  - process and thread management
  - system managemneta
- 컴퓨터 시스템의 구성: HW -> reource -> kernel -> system call Interface -> user appilcation
- 사용자가 kernel에 직접 접근하면 문제 발생의 여지가 있으므로, OS에게 필요한 기능을 요청하기 위한 통로가 system call interface임
- 운영체제의 구분
  - 사용자의 수 : signle(PC)/multi(server)
  - 동시 실행의 수 : single/multi
  - 작업 수행 방식 : 순차 처리 / batch system / time sharing system / personal computing / parallel processing system / distributed processing system / realTime system
  - 대부분 system은 time sharing system 사용
- Distributed Processing system
  - network를 이용해서 여러개의 컴퓨터를 묶은 시스템
  - 물리적인 분산, 통신망 이용한 상호 연결
  - 컴퓨터를 노드라고 하는데, 각 노드마다 자기만의 OS를 가지고 있고, 각각의 OS를 잘 관리하게끔 하기 위하여 분산운영체제를 통해 하나의 프로그램, 자원처럼 사용 가능 
  - ex) cluster system, client-server system 등 
- real time system
  - 작업 처리에 deadline을 갖는 시스템 
  - 제한 시간 내에 서비스를 제공하는 것이 자원 활용 효율보다 중요
- parellel processing system vs distributed processing system
  - 병렬 처리 --> 단일 시스템 내 둘 이상의 프로세서
  - 분산 처리 --> 여러개의 서버를 두고 처리(네트워크 기반 병렬 처리)
- 운영체제 구조
  - 커널(kernel) : OS의 핵심부분(메모리 상주), 가장 빈번하게 사용되는 기능들 담당
  - 유틸리티(utility) : 커널 제외 나머지 부분, UI등 서비스 프로그램
  - 단일 구조 / 계층 구조 / 마이크로 커널 구조 
- 운영체제의 기능은 한마디로 관리! SW/HW 관리. processor, process, memory, File management, I/O Management 등
- OS의 역할 - 프로세스 관리
  - 생성/삭제, 상태관리(PCB..?)
  - 자원 할당
  - 프로세스 간 통신 및 동기화
  - 교착상태(deadlock) 해결
- OS의 역할 - Processor 관리
  - 프로세스 스케줄링
  - 프로세스 할당 관리
- OS의 역할 - File management
- OS의 역할 - I/O management  

## chapter03 process management
- Job vs Process
  - Job : program + Data 또는 program 이라고 함. 컴퓨터 시스템에 실행 요청 전 상태
  - Process : 커널에 등록된 작업. 실제 프로그램이 수행되는 주체
  - 시스템 성능 향상을 위해 프로세스는 커널에 의해 관리됨
  - 프로그램이 메모리에 적재되면 프로세스라고 함
- 프로세스의 정의
  - 실행 중인 프로그램
  - 커널에 등록된 Job
  - 능동적인 개체
- 자원(Resource)의 개념
  - 커널의 관리하에 프로세스에게 할당/반납되는 수동적인 개체(passive entity)    
- PCB(Process Control block)
  - 메인 메모리에 존재 
  - 프로세스 생성/관리/제거에 필요한 정보를 모아둔 block
  - 프로세스 생성시 PCB 생성, 커널에 저장됨, OS별로 다름
  - PCB 참조 및 갱신 속도는 OS 성능 중 중요한 요소 중 하나
- 프로세스 상태 : 자원간의 상호작용에 의해 결정
  - create state : 커널에 Job이 할당된 상태
  - ready state : memory 할당 O, CPU 할당 X
  - running state : memory, cpu 할당 O
  - Blocked/Asleep state : running -> I/O 작업 수행을 위한 상태
  - suspended state : process가 memory에 할당받지 못한 상태
  - terminate/zombi state : process 수행이 끝난 상태. 모든 자원 반납후 일부 PCB 정보만 남아 있는 상태
- 프로세스 상태 세부 정리
  - create state
    - Job을 커널에 등록한 상태
    - PCB 할당 및 proces 생성, 가용 메모리 공간 여부에 따라 ready 상태, suspended ready 상태로 감
  - ready state
    - CPU 자원 할당을 기다리고 있는 상태, cpu 자원 할당을 받으면 running 상태로 감. 이를 dispatch라고 함
  - Running state 
    - processor 할당 전부 받은 상태. 해당 상태를 벗어나는 경우는 2가지
      - ready  : ready 상태로 바뀌는 것을 preemption 되었다고 함(주로 processor 자원 상태에 따라..)
      - asleep/block : 다른 이벤트 발생(file IO 발생)하여 잠시 딴 일을 해야할 떄
  - blocked/asleep state
    - running 상태에서 잠시 특정한 일이 발생한 상태. 이떄 일이 해결되면 바로 running으로 가는 것이 아니라, ready 상태로 감
  - suspended state
    - process가 메모리를 할당 받지 못한 상태
    - 지금까지 작업한 정보(memory image)를 swap device(일종의 하드 디스크)에 저장
    - memory를 뺏기는 것을 swap out, swap in 이라고 함
  - terminate/zombi state
    - process가 끝난 상태. 모든 자원 반납 후, PCB 정보만 남아 있는 상태
    - 여길 왜 들리는 걸까? 나중에 kernel이 PCB 정보를 수집해 나중에 기억하려고!
- 인터럽트(interrupt)
  - 예상치 못한, 외부에서 발생한 이벤트
  - 인터럽트 발생시, kernel이 개입해서 해당 프로세스 중단
- 인터럽트 처리 과정
  - 인터럽트 발생 -> 프로세스 중단(커널 개입) -> 인터럽트 처리(interrupt handling) -> 인터럽트 발생 장소, 원인 파악 -> 인터럽트 서비스 여부 결정 -> 인터럽트 서비스 루틴 호출 
- context switching(문맥 교환)
  - Context -> process와 관련된 정보들의 집합. 크게 두군데 저장됨
  - Context Saving -> 현재 프로세스의 register context를 저장하는 작업
  - Context restoring -> Register context를 프로세스로 복구하는 작업
  - Context switching -> 인터럽트가 발생하여 CPU 점유가 바뀌는 경우 context switching이 발생
  - Context switch overhead -> Context switching에 소요되는 비용
- context swithcing process
  - cpu 내에는 register가 있고, 바깥에 main memory가 있는데 이 때 process가 수행될 때 필요한 정보들은 register에 있어야 하고, 이는 Main memory에서 가져와야 함
- 이 때 register에 있는 정보들을 register context라고 함
- 나머지 다양한 정보들(code, data, stack, pcb)는 메인 메모리에 있음
- 인터럽트 발생하여 cpu를 뺏긴다면 지금까지 진행한 정보(register context)를 main memory내 pcb에 저장 --> context saving
- context saving된 정보를 불러오는 것 --> context restoring
- context saving + context restoring --> context switching
- context switching은 overhead가 발생하기 때문에 thread를 사용!
- 용어 기억하기
  - dispatch : ready state -> running state 
  - preemption : running state -> ready state
  - swap in / swap out : suspended state <-> ready / asleep 


## chapter 04 thread management
- 프로세스는 자원을 할당받아 제어를 수행하면서 목적을 달성
- 이 때 제어에 해당하는 부분을 thread
- 하나의 프로세스 안에는 여러 개의 thread가 있을 수 있음
- Resource
  - resource에는 코드, 전역 데이터, heap 등이 있을 수 있음 
  - heap --> 코드를 수행 할 공간
- 제어 영역
  - SP(stack pointer), PC(program counter), 지역 데이터, stack 등이 있음
  - 지역 데이터 --> 지역 변수 등. 지역 데이터는 stack에 저장
  - <b>제어 영역에 해당하는 process를 우리는 thread라고 부름</b>
  - <b>프로세스 안에는 여러 개의 스레드가 있으며, 이는 자원을 공유한다!</b>
- 같은 프로세스의 스레드들은 동일한 주소 공간을 공유함
- 스레드마다 각자의 작업영역을 가짐. thread sp들은 공유되는 자원(코드)를 제어
- 스레드
  - Light weight process(LWP)라고도 부름
  - <b>processor 활용의 기본 단위</b>
  - 스레드 기본 구성요소
    - thread ID
    - Register set(pc, sp 등)
    - stack(local data)   
- single thread vs multi thread
  - single thread : process 내 1개 thread
  - multi thread : process 내 여러개의 thread 
- thread의 장점
  - 자원 공유(효율성 증가) : process에 비해 context switching이 덜 일어남
  - 경제성 : 자원을 공유
  - multi-processor(CPU)의 활용: 병렬처리 가능
  - 사용자 응답성 : multi-thread가 가능하기 때문에 처리가 지연되더라도 다른 thread는 작업 수행 가능
- thread 구현
- 스레드 생성 주체가 thread냐, kernel이냐에 따라서 달라짐
  - user thread
  - kernel thread
- user thread
  - 커널은 스레드의 존재를 모르기 때문에 모드 간의 전환이 없어 overhead가 적음
  - 하나의 스레드가 커널에 의해 block되면 프로세스 전체가 block됨
- kernel thread
  - 커널이 직접 제공해주기 때문에 안정성과 다양한 기능 제공
  - 유저모드와 커널모드의 빈번한 발생 때문에 overhead 발생  
- multi-threading model
  - user thread + kernel thread(n:m model)
  - 두 가지의 모드의 장점만을 취득한 모델
  - 효율적이면서도 유연하지만 복잡하다는 단점이 있음

## chapter05 프로세스 스케줄링(process scheduling)
- 다중 프로그래밍(multi-programming)
  - 여러개의 프로그램이 시스템 내에 존재하는 것을 말함
  - 여러개의 프로그램에 자원을 할당해야 하는데, 이를 스케줄링이라고 함 
- 자원 관리 방법
  - Time sharing : CPU와 같이 한 번에 한명만 들어갈 수 있는 경우 
  - Space sharing : 하나의 자원을 분할하여 동시에 사용
- 스케줄링의 목적
  - 시스템의 성능 향상이 목적
  - 대표적 시스템 성능 지표: 목적에 맞는 지표를 고려하여 스케줄링 기법을 선택해야함
    - 응답시간(response time)
    - 작업처리량(throughout)
    - 자원 활용도  
- 스케줄링 기법이 고려하는 항목들
  - 프로세스 특성: I/O bounded / compute-bounded 
  - 시스템 특성: batch system / interactive system처럼 시스템의 특성에 따라 스케줄링 기준이 달라짐
  - 프로세스의 긴급성 : hard /soft-real time 등에 따라서 달라짐
  - 프로세스 우선순위(priority)
  - 프로세스 총 실행 시간(total service time)
- CPU burst vs I/O burst
  - 프로세스 수행은 cpu를 통한 계산과 I/O의 반복으로 이루어짐
  - compute-bounded process -> cpu기반 계산이 더 많이 수행되는 process
  - I/O bounded process -> I/O를 더 많이 수행하는 process
- scheduling level
  - long-term scheduling : Job-scheduling
  - mid-term scheduling : memory allocation
  - short-term scheduling : process scheduling
- long-term scheduling - Job scheduling
  - 여러 job들 중 순서에 맞게 process로 변환시켜주는 스케줄링
  - kernel에 제출할 job 순서 결정 
  - multi-programming의 degree를 조절 - 시스템 내에 프로세스 수를 결정
  - I/O bounded 와 compute-bounded를 잘 조절해서 선택해야 함
- mid-term scheduling - memory allocation
  - ready - suspended ready 간의 관계에서 어느 것을 우선적으로 memory에 할당할지를 결정하는 스케줄링 
- short-term scheduling
  - 프로세서를 할당할 process 결정
- scheduling policy
  - preemption / non-preemption scheduling
    - preemption : 누가와서 내 것을 빼앗아 갈 수 있다는 의미
    - non-preemption : 누가와서 빼앗아 갈 수 없음   
- non-preemption scheduling
  - context switching overhead가 적음
  - 한 프로세스가 100시간 돌이가면, 다른 프로세스는 그동안 수행 못함
- preemption scheduling
  - context switching overhead가 큼
  - time-sharing, real-time system에 적합
- priority
  - static priority
    - 한번 우선순위가 고정되면 바뀌지 않음 
  - dynamic priority 
    - 언제든지 우선순위가 바뀔 수 있음 

## chapter06 process synchronization and mutual exclusion
- process synchronization(프로세스 동기화)
  - 다중 프로그래밍 시스템
    - 동시에 여러 프로세스 존재
    - 프로세스가 독립적으로 동작하는데, 공유 자원이 존재할 때 문제 발생할 여지가 있음
  - 프로세스 동기화
    - 프로세스들이 서로 정보를 공유하는 것 
- Asynchronous and concurrent P's
  - 비동기적(Asynchronous) : 프로세스들이 서로에 대해서 모름
  - 병행적(concurrent) : 여러 개의 프로세스들이 동시에 시스템에 존재
  - 병행 수행 중인 비동기적 프로세스들이 공유 자원에 동시 접근할 때 문제 발생 여지 있음
- Terminologies
  - shared data : 여러 프로세스들이 공유하는 데이터
  - critical section(cs) : 공유 데이터를 접근하는 코드 영역
  - mutual exclusion -> 둘 이상의 process를 cs 진입을 막는 것   
- machine instruction(기계어 명령 특성)
  - 실제로 processor가 실행하는 가장 작은 실행 단위
  - atomicity(원자성), indivisible(분리 불가능)의 특성을 가짐
  - 한 기계어 명령의 실행 도중 인터럽트 받지 않음     
- race condition
  - 실행 방식에 따라서 결과가 달라지는 것 
- <b>Mutual exclusion 수행시 요구사항</b>
  - mutual exclusion(상호배제)
    - cs에 프로세스가 있으면, 다른 프로세스의 진입 금지 
  - progress(진행)
    - cs안에 있는 프로세스 외에는 다른 프로세스가 cs 진입하는 것을 막아선 안됨 
  - Bounded waiting(한정대기)   
    - 프로세스의 cs 진입은 유한시간 내에 허용되어야 함 
- Mutual Exclusion Solutions
  - SW solutions
    - Dekkers's algorithm
    - Dijkstra's algorithm
  - HW solutions
    - TestAndSet(TAS) instruction --> process 3개 이상인 경우, bounded waiting 조건 위배
  - OS supported SW solution
    - Spinlock
    - semaphore
    - eventcount/sequencer
  - Language-Level solution
    - Monitor        
- HW solutions - TAS instruction
   - 아래 문장을 한 번에 수행(machine instruction) 
~~~c
boolean TestAndSet(boolean *target){
  boolean temp = *target; // 이전 값 기록 
  *target = true;         // target 변수 true
  return temp;            // 이전 값 return
}
~~~ 
- OS supported SW solution - Spinlock 
  - 스레드나 프로세스가 lock을 소유하고 있다면, lock이 반환될 때까지 기다리는 것
  - lock, unlock 과정이 짧은 경우에 유용
  - 조금만 기다리면 바로 쓸 수 있는데 궂이 context switching을 해야 하나? 에서부터 출발
  - P(), V() 연산을 통해 수행. P, V 연산은 OS에 의해 preemption 하다는 것을 보장
  - Spinlock process는 동시에 두 process가 수행되어야 하므로, 멀티 프로세서 이상에서만 수행 가능
~~~c
P(S){
  while(s <= 0) do
  endwhile;
  S <- S - 1
}

V(S){
  S <- S + 1
}
~~~ 
- OS supported SW solution - Semaphore
  - 임의의 S 변수 하나에 ready queue 하나가 할당
  - binary semaphore / counting semaphore
~~~c
P(S){
  if(S > 0){
    then S <- S - 1;
    else wait on the queue Q(s); 
  }
}

V(S){
  if(waiting processes on Q(s)){
    then wakeup one of them;
    else S <- S + 1;
  }
}
~~~
- Semaphore로 해결할 수 있는 문제들
  - ME problem
  - process 동기화 문제
  - 생산자-소비자 문제
  - reader-writer 문제
  - dining-philosopher 문제 

## chapter07 교착상태(deadlock Resolution)
- 교착상태란 어떤 프로세스도 자원을 가져갈 수 없는 상태를 말함
- Blocked/Asleep: 프로세스가 특정 이벤트 때문에 필요한 자원을 기다리는 상태
- deadlock: 프로세스가 발생 가능성이 없는 이벤트를 기다리는 경우  
- deadlock vs starvation
  - deadlock : event가 절대 발생할 수 없음
  - starvation : 운이 나빠 발생을 안함
- 자원의 분류
  - 선점 가능 여부 --> 선점 가능하냐? 
    - preemptible/non-preemptible
  - 할당 단위 --> 쪼갤수 있느냐?
    - Total/Partitioned 
  - 동시 사용 가능 여부 --> shared 가능 여부
    - exclusive/shared 
  - 재사용 여부 --> 쓰고 또 쓰고 가능하냐?
    - serially-reusable/consumable
- 자원의 형태에 따른 deadlock 가능 여부
  - non-preemptible/exclusive..
- Deadlock model
  - Graph-model/State transition model
- <b>deadlock 발생 필요 조건</b>
  - 자원 특성
    - non-preemptible/exclusive use of resources
  - 프로세스 특성
    - hold and wait
    - circular wait    

## chapter 09 가상메모리
- 가상메모리 : non-continuous allocation
- non-continuous allocation
  - 메모리를 여러개의 block 단위로 나눔 
  - 필요한 부분만 메모리에 적재하고, 나머지 block은 swap device에 저장
- non-continuous allocation 기법들
  - paging system 
  - segmentation system
  - Hybrid paging/segmentation system 
- block mapping
  - 간단한 address mapping 
- block mapping 순서
  - virtual v = address(b, d) 
  - process의 BMT(block map table)에 접근
  - BMT에서 block b에 대한 항목(entry) 찾음
  - Residence bit 검사
    - 0 인 경우, 해당 block을 swap device에서 메모리로 가져옴
    - 1 인 경우, 아래 단계 수행
  - BMT에서 read address 값 a 확인
  - 실제 주소 r = a + d 계산
  - r을 이용하여 메모리에 접근   
- paging system
  - 프로그램을 같은 크기의 block 단위로 분할(page)
  - 메모리에서 page 크기에 매핑되는 부분을 page frame이라고 함  
- paging system의 특징
  - 논리적 분할이 아니라, 물리적으로 동일한 크기로 분할
  - No external fragmentation --> page의 크기가 동일
  - Yes internal fragmentation   
- paging system address mapping
  - PMT(Page map table), kernel에 존재 
  - address mapping algorithm
    - Direct mapping
    - Associative mapping
    - Hybrid direct/associative mapping
- Direct mapping 순서
  - 가장 간단한 paging system에서의 address mapping 
  - 해당 프로세스의 PMT가 저장되어 있는 주소 b에 접근
  - 해당 PMT에서 page p에 대한 entry 찾음
    - b(PMT base address) + (p * entrySize)
  - 찾아간 entry의 존재 비트 검사
    - bit가 0이면(page fault), running -> asleep하고, swap device에서 page을 메모리에 적재
    - bit가 1이면 아래 단계 수행
  - entry에서 pagr frame number(p') 확인
  - p'와 가상 주소의 변위 d를 사용하여 실제 주소 r 형성
    - r = p' * pageSize + d
  - 실제 주소 r로 주기억장치에 접근  
- Associate mapping
  - TLB(translation Look-aside Buffer)에 PMT 적재(전용 HW)
  - PMT를 병렬 탐색
- Hybrid Direct/Associative Mapping
  - 두 기법을 혼합하여 사용 
  - Locality를 활용하여 최근에 사용한 page, 근처 page들만 TLB에 저장하고 나머지는 PMT에 저장
- Hybrid Direct/Associative Mapping 순서
  - TLB에 p가 적재되어 있는 경우, residnece bit 검사 후 page frame 확인
  - TLB에 p가 적재되어 있지 않은 경우, PMT에서 page frame 확인
  - 해당 page를 TLB에 적재

## chapter09_2 가상 메모리 관리
- Cost Model for Virtual Mem Sys.
  - Page fault : 메모리에 page가 없는 경우, page fault 발생
  - process가 running -> asleep 상태로 변환되고, 이 때 context switching  발생
- Page reference string(d)
  - 참조한 page들을 문자열로 써 놓은 것
  - 프로세스의 수행 중 참조한 페이지 번호 순서  
- Hardware component
  - Bit vectors: 메모리 상에 page가 가득 찼을 때, 새로운 page를 할당하려고 할 때 활용 
    - reference bit : 해당 page의 참조 여부를 1,0으로 기록한 bit
    - update bit : 갱신 비트 --> page data가 갱신되었는가? 
- reference bit
  - 해당 page의 참조 여부 기록. 
  - 주기적으로 해당 bit를 0으로 초기화 
- update bit
  - Page가 메모리에 적재된 후, 프로세스에 의해 수정되었는지를 표시
  - 프로세스가 page를 변경하면, 데이터 무결성을 위하여 swap-device에도 정보를 알려줘야 함 
- 가상 메모리 성능 향상을 위한 관리 기법들
  - allocation strategies  -> 어떻게 메모리 할당을 할 것인가? 
    - fixed allocation --> 정해진 크기만큼 pf 할당
    - variable allocation --> 동적 크기만큼 pf 할당
  - Fetch strategies       -> 특정 page를 메모리에 언제 적재할 것인가? 
    - demand fetch --> 프로세스가 참조하는 page들만 적재
    - anticipatory fetch --> 가까운 미래에 참조될 가능성이 높은 page를 미리 적재(pre-paging, preFetch등)  
  - placement strategies   -> 어디에 적재할 것인가?
    - paging system에서는 불필요
    - segmentation system --> best/worst/first/next - fit  
  - replacement strategies -> 새로운 page를 어떻게 교체할 것인가? 
    - fixed replacement를 위한 기법
    - variable replacement를 위한 기법
  - clean strategies       -> 변경된 page를 언제 write-back 할 것인가? 
    - demand cleaning : 해당 page에 메모리에서 내려올 때 write-back
    - anticipatory cleaning : 더 이상 변경될 가능성이 없다고 판단 할 때 미리 write-back 
  - load control strategies
    - load : 부하
    - multi-programming degree(수행되는 프로세스 수) 조절  
- thrashing --> 과도한 page fault 현상 발생

## chapter 10 File system
- Disk System : 데이터 영구 저장 장치(비휘발성)
  - Sector : 데이터 저장/판독의 물리적 단위
  - Track : Platter 한 면에서 중심으로 같은 거리에 있는 sector들의 집합 
  - Cylinder : 같은 반지름을 갖는 track들의 집합
  - Platter : 앞뒤 자성의 물질을 입힌 동그란 CD 
  - Surface : Platter 윗면과 아랫면
- Disk Drive
  - HDD의 형태. Disk pack에 데이터를 기록하거나 판독할 수 있도록 구성된 장치
  - Head : Arm 끝부분, platter와 접촉하고 있는 부분
  - Arm : Head를 고정/지탱
  - Positioner : Arm을 지탱 -> Arm을 고정하고 있는 기둥
  - Spindle 
- Disk Address
  - Physical address : sector의 실제 address
  - Logical address : Disk system의 데이터 전체를 block들의 나열로 취급
- Disk Address Mapping
  - OS -> Disk driver -> Disk Controller
  - OS는 block number를 disk driver에게 전달. 전달된 주소를 실제 물리 주소로 변환하여 disk controller에게 전달    
- File System
  - 사용자들이 사용하는 파일들을 관리하는 운영체제의 한 부분
  - File system의 구성
    - File
    - Directory structure
    - Partitions
      - Directory들의 집합을 논리적/물리적으로 구분   
- File concept
  - 보조 기억 장치에 저장된 연관된 정보들의 집합
    - 보조 기억 장치 할당의 최소 단위
    - Sequence of bytes(물리적 정의) 
  - OS는 file operation에 대한 system call을 제공해야 함
  - system call은 os의 기능 중에 사용자가 사용할 수 있는 기능들의 집합
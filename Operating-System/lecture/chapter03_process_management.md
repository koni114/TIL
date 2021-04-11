# chapter03 process management
## 프로세스 관리
- window 작업관리에서 process 관리창을 확인할 수 있음

## Job vs Process
- Job은 program + Data 또는 심플하게 program이라고도 함
- <b>Job은 컴퓨터 시스템에 실행 요청 전 상태</b>
- process는 컴퓨터 시스템(커널)에 등록된 작업
- 시스템 성능 향상을 위해 프로세스는 커널에 의해 관리됨

![img](https://github.com/koni114/Operating-system/blob/master/img/os_3.JPG)

- <b>프로그램이 메모리에 적재되면 프로세스가 됨</b>

## process의 정의
- 실행 중인 프로그램
- 커널에 등록된 Job
- 능동적인 개체

## 자원(Resouce)의 개념
- 커널의 관리하에 프로세스에게 할당/반납하는 수동적 객체(passive entity)

## process control block(PCB)
- 프로세스를 제거하기 위해 모아놓은 block
- OS가 프로세스 관리에 필요한 정보를 저장
- 프로세스 생성시 PCB 생성
- PCB는 커널에 저장됨
- PCB는 OS별로 다름
- PCB 참조 및 갱신 속도는 OS 성능의 중요한 요소 중 하나

## PCB가 관리하는 정보
- PID
- 스케줄링 정보
- 프로세스 상태
- 메모리 관리 정보
- 입출력 상태 정보
- 문맥(context) 저장 영역
- 계정 정보

## 프로세스 상태
- 자원 간의 상호 작용에 의해 결정 

### create state
- Job을 커널에 등록한 상태
- PCB 할당 및 process 생성
- 가용 메모리 공간 여부에 따라 공간이 있으면, ready state로, 아니면 suspended ready 상태로 감

### Ready state
- CPU(processor) 자원 할당을 기다리고 있는 상태
- 메모리 할당은 받았으므로, CPU 할당만 받으면 실행 가능
- 즉시 실행가능 상태라고도 함
- CPU 자원 할당을 받으면 running 상태로 감. <b>이를 dispatch 된다고 함</b>

### Running state
- processor(cpu)와 다른 자원들을 모두 할당받은 상태
- Running 상태를 벗어나는 경우가 두가지 있음
  - ready
  - asleep
- ready 상태로 바뀌는 것을 preemption 이라고 함
  - processor가 없어서 쫒겨나는 경우
  - processor scheduling 인 경우(ex) Time out, priority changes)
- 예를 들어 running 상태에서 IO 작업을 수행해야하는 경우 파일을 메모리에서 가지고 와야함.  
  이 때는 잠시 asleep 상태로 변환(sleep, block 된다고 함)

### Blocked/Asleep state
- asleep 상태에서 I/O 작업이 끝나면 바로 running 상태로 가는 것이 아니라, ready 상태로 되었다가 running으로 감

### Suspended State
- process가 Memory 할당받지 못한 상태를 말함
- process가 지금까지 한 정보를 어딘가에 저장 해야함. 즉 뺏기기 전에 memory image로 저장
- memory image를 swap device(일종의 hard disk)에 저장
- memory를 뺏기는 것을 swap out, 복구하는 것을 swap in 이라고 함

### terminate/zombi state
- process 수행이 끝난 상태
- 모든 자원 반납 후, 커널 내에 일부 PCB 정보만 남아있는 상태
- 왜 여길 들리는 걸까? --> kernel이 PCB 정보를 수집해 나중에 기억하려고!

## Process State transition diagram

![img](https://github.com/koni114/Operating-system/blob/master/img/os_4.JPG)

## process 상태 및 특성

![img](https://github.com/koni114/Operating-system/blob/master/img/os_5.JPG)

## 인터럽트(interrupt)
- 예상치 못한, 외부에서 발생한 이벤트
- 인터럽트의 종류
  - I/O interrupt : 게임에서 마우스를 클릭해서 총을 쏠 때
  - Clock interrupt : CPU에서 Clock event
  - Console interrupt : Console 창에서 입력할때
  - Program check interrupt : 다른 program을 실행할 때
  - Machine check interrupt 
  - inter-process interrupt
  - System call interrupt 

## 인터럽트 처리 과정
- 인터럽트 발생 -> 프로세스 중단(커널 개입) -> 인터럽트 처리(interrupt handling) -> 인터럽트 발생 장소, 원인 파악 -> 인터럽트 서비스 여부 결정 -> 인터럽트 서비스 루틴 호출

![img](https://github.com/koni114/Operating-system/blob/master/img/os_6.JPG)

- Pi라는 프로세스가 수행하고 있음
- 이 때 누군가가 인터럽트를 걸면, kernel이 개입해서 해당 프로세스를 중단시킴. 이 순간 Context Saving이 발생함(책의 책갈피 PCB에 저장)
- kernel이 인터럽트 원인 파악(interrupt handling)
- 만약 인터럽트를 서비스 할지 말지를 결정하고 서비스 함(interrupt service)
- 서비스 하기로 된다면, Ps라는 새로운 프로세스가 실행됨
- Ps라는 프로세스가 종료되면 ready 상태에 있는 애들 중에 차례로 수행함  
  즉 Pj가 들어올 수도 있음
- Pj가 들어오면 Pj에 해당하는 책갈피를 복구하여 자신의 일을 수행함

## Context Switching(문맥 교환)
- Context
  - process와 관련된 정보들의 집합. 크게 두군데에 저장이됨
- Context saving
  - 현재 프로세스의 Register context를 저장하는 작업
- Context restoring
  - Register context를 프로세스로 복구하는 작업
- Context switching
  - 실행 중인 프로세스의 context를 저장하고, 앞으로 실행 할 프로세스의 context를 복구하는 일
  - 커널의 개입으로 이루어짐
- context switching 흐름
  - CPU 내에는 register가 있고, 바깥에 Main memory가 있는데, 이 때 process가 수행될 때 필요한 정보들은 register에 있어야 하고, 이는 Main memory에서 가져와야함(복습)
  - 이 때 register에 있는 정보들을 register context라고 하며, CPU에 있음
  - 이외의 다양한 정보들은(Code, data, Stack, PCB) 메인 메모리에 있음
  - 만약 인터럽트가 발생하여 CPU를 뺏긴다면, 지금까지 진행한 정보(register context)들을 Main memory내 PCB에 저장함 -> 이를 Context saving 이라고 함
  - Context saving된 정보를 다시 불러오는 것을 Context restoring 이라고 함
  - Context saving과 Context restoring을 합쳐 Context switching 이라고 함

## Context switch overhead
- Context switching에 소요되는 비용
  - OS마다 다름
  - context switching이 자주 일어나기 때문에 OS 성능에 큰 영향을 줌
- 불필요한 Context switching을 줄이기 위해 thread를 사용하는 것 등이 있음

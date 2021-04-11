# 프로세스 스케줄링
## 다중프로그래밍(multi-programming)
- 단일 프로세서 상에서 여러 프로그램이 동시에 실행되는 것을 말함
- 실제로 하나의 프로세서에는 하나의 프로세스만 수행 가능하기 때문에 엄연히 틀린 말이고, 짧은 시간 내에 일부 프로그램이 번갈아가면서 수행되기 때문에 동시인 것처럼 보이는 것임
- 여러개의 프로세스가 시스템 내에 존재
- 자원을 할당 할 프로세스를 선택해야 함. 이를 프로세스 스케줄링(Scheduling)이라고 부름
- 자원 관리 방법은 크게 2가지로 볼 수 있음
  - 시간 분할(Time sharing) 관리
    - CPU 같이 한번에 한명만 들어갈 수 있는 경우
    - ex) processor
    - 프로세스 스케줄링(process scheduling). 프로세서 사용시간을 프로세스들에게 분배
  - 공간 분할(space sharing) 관리
    - 하나의 자원을 분할하여 동시에 사용
    - ex) 메모리, 디스크

## 스케줄링(scheduling)의 목적
- 시스템의 성능(Perforamance) 향상이 목적임  
  그렇다면 여기서 말하는 성능이 무엇일까? 애매하므로, 성능에 대한 지표를 정의 해야함
- 대표적 시스템 성능 지표(index)
  - 응답시간(response time)
    - 작업 요청(submission)으로부터 응답을 받을때까지의 시간 
    - interactive system, real-time에서 중요한 지표가 될 것임
  - 작업 처리량(throughout)
    - 단위 시간동안 처리한 작업 수
    - batch systems
  - 자원 활용도
    - 주어진 시간(Tc)동안 자원이 활용된 시간(Tr)  
    - Utilization = Tr / Tc
    - 비싼 장비를 구매한 경우
- 목적에 맞는 지표를 고려하여 스케줄링 기법을 선택해야 함

## 대기시간, 응답시간, 반환시간
![img](https://github.com/koni114/Operating-system/blob/master/img/os_12.JPG)

## 스케줄링 기준(Criteria)
- 스케줄링 기법이 고려하는 항목들
- 프로세스 특성
  - I/O-bounded or compute-bounded
- 시스템 특성
  - batch system 과 interactive system 처럼 시스템의 특성에 따라 스케줄링 기준이 달라짐
- 프로세스의 긴급성
  - Hard, soft-real time 등에 따라서 달라짐
- 프로세스 우선순위(priority)
- 프로세스 총 실행 시간(total service time)

## CPU burst vs I/O burst 
- 프로세스의 수행 단계를 생각해보면, 계산과 I/O의 반복으로 이루어짐  
  이 때 계산은 CPU를 사용하는 것으로 생각할 수 있음
- 프로세스 수행은 CPU 사용 + I/O 대기임
- 어떤 프로그램은 CPU를 더 많이 쓸것이고, 어떤 프로그램은 I/O을 더 많이 쓸텐데, 
  이 때 CPU를 더 많이 쓰는 경우를 compute-bounded process라고 하며, I/O를 더 많이 하는 경우를 I/O bounded process 라고 함
- 결과적으로 Burst time은 스케줄링의 중요한 기준 중 하나

## 스케줄링의 단계(Level)
- 발생하는 빈도 및 할당 자원에 따른 구분
- Long-term scheduling
- Mid-term scheduling
- Short-term scheduling

## Long-term Scheduling
- Job scheduling
  - 여러 Job들 중 순서에 맞게 process로 변환시켜주는 스케줄링
  - 시스템에 제출 할(kernel에 등록 할) 작업(Job) 결정
- 다중프로그래밍의 정도(degree)를 조절
  - 시스템 내에 프로세스 수 조절
  - 시스템 내에 너무 많은 Job이 있으면 관리하기가 어려우므로, 얼마나 많이 Job을 수행할지를 조절해야 함    
- I/O Bounded와 compute-bounded 프로세스들을 잘 섞어서 선택해야함  
- time-sharing system에서는 long-term scheduling이 상대적으로 덜 중요함  
  몇 개가 들어와도 쪼개서 사용하기 때문  

## Mid-term scheduling
- 메모리 할당 결정(memory allocation)
- ready - suspended ready state 관계에서 어떤 것을 우선적으로 memory에 올려줄지를 결정하는 것이 mid-term scheduling임
- Job scheduling보다는 더 자주 빈번히 일어남


## short-term scheduling
- process scheduling
- 프로세서를 할당할 프로세스(process)를 결정
- ready - running state 상태에서의 스케줄링을 말함
- 매우 빈번히 일어나기 때문에 매우 빨라야 함  
- ex) CPU burst 시간이 100ms 이고 스케줄링 decision 시간은 10ms 이면  
  약 9%의 overhead가 발생했다고 할 수 있음

## 스케줄링의 단계 (Level)
- 저번 시간에 보았던 process state에서 다음과 같이 스케줄링의 단계를 추가해 줄 수 있음

![img](https://github.com/koni114/Operating-system/blob/master/img/os_13.JPG)


## 스케줄링 정책(Policy)
- 여기서 정책이라는 것은 방법과 동일한 의미
- 가장 대표적으로 선점 vs 비선점으로 나눌 수 있음
- 어떤 우선순위 방법을 사용할 것이냐에 따라 나눌 수 있음

## Preemptive/Non-preemeptive scheduling
- Preemptive --> 누가와서 내 것을 빼앗아 갈 수 있다는 의미(선점할 수 있다!)
- Non-preemptive --> 누가와서 뺏을 수 없다!

### Non-preemeptive scheduling
- 할당 받을 자원을 스스로 반납할 때까지 사용
  - 예) system call, I/O Etc
- 장점
  - Context switch overhead가 적음
- 단점
  - 한 프로세스가 100시간동안 돌아가면 다른 프로세스는 수행 못함
  - 잦은 우선순위 역전, 평균 응답 시간 증가

### Preemptive scheduling
- 타의에 의해 자원을 빼앗길 수 있음
  - ex) 할당 시간 종료, 우선순위가 높은 프로세스 등장
- Context switch overhead가 큼. 즉 시스템 부하가 크다
- Time-sharing system, real-time system 등에 적합

## Priority
- 프로세스의 중요도

### Static priority(정적 우선순위)
- 한번 우선순위가 고정되면 바뀌지 않음
- 프로세스 생성시 결정된 priority가 유지됨
- 구현이 쉽고, overhead가 적음
- 시스템 변화에 대한 대응이 어려움

### Dynamic priority(동적 우선순위)
- 프로세스 상태 변화에 따라 priority 변경
- 구현이 복잡하고, priority overhead가 큼
- 시스템 환경 변화에 유연한 대응 가능 

### TEST
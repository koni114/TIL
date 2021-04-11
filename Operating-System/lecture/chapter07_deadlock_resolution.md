# chapter07 교착상태(Deadlock Resolution)
- 어느 프로세스도 어느 자원을 가져갈 수 없는 상태

## Deadlock의 개념
- Blocked/Asleep state
  - 프로세스가 특정 이벤트를 기다리는 상태
  - 프로세스가 필요한 자원을 기다리는 상태
- Deadlock state
  - 프로세스가 발생 가능성이 없는 이벤트를 기다리는 경우
    - 프로세스가 deadlock 상태에 있음
  - 시스템 내에 deadlock에 빠진 프로세스가 있는 경우
    - 시스템이 deadlock 상태에 있음
- Deadlock vs Starvation  

![img](https://github.com/koni114/Operating-system/blob/master/img/os_48.JPG)
- deadlock은 asleep 상태에 있는데, event가 발생할 일이 없는 경우
- starvation은 ready state에서 cpu를 기다리고 있는 상태! 발생할 수는 있는데 운이 없어서 발생 안하고 있는 상태
- 즉 기다리고 있는 자원도 차이가 있음

## 자원의 분류
- 일반적 분류
  - Hardware resources vs Software resources
- 다른 분류법
  - 선점 가능 여부에 따른 분류
  - 할당 단위에 따른 분류
  - 동시 사용 가능 여부에 따른 분류
  - 재사용 가능 여부에 따른 분류  

### 선점 가능 여부에 따른 분류
- Preemptible resources
  - 선점 당한 후, 돌아와도 문제가 발생하지 않는 자원
  - Processor, memory 등
- Non-preemptible resources
  - 선점 당하면, 이후 진행에 문제가 발생하는 자원
    - Rollback, restart등 특별한 동작이 필요
  - E.g., disk drive 등  
    무엇을 작성하고 있을 때 usb를 뽑아버리면? --> non-preemptible     

### 할당 단위에 따른 분류
- Total allocation resources
  - 자원 전체를 프로세스에게 할당
  - E.g., Processor(1 core 일 때) 
  - disk drive(한번에 한 명만 사용 가능)
- Partitioned allocation resources
  - 하나의 자원을 여러 조각으로 나누어, 여러 프로세스들에게 할당
  - ex) Memory등

### 동시 사용 가능 여부에 따른 분류
- Exclusive allocation resources
  - 한 순간에 한 프로세스만 사용 가능한 자원
  - ex) processor, memory, disk drive 등
  - memory는 조각내서 사용할 순 있지만, 동일한 조각을 여러 프로세스가 공유할 수 없음
- Shared allocation resource
  - 여러 프로세스가 동시에 사용 가능한 자원 
  - ex) Program(sw), shared data 등  
    워드 프로그램 창을 여러개 띄어놓고 사용할 수 있는 것!, exe 파일 등

### 재사용 가능 여부에 따른 분류
- SR(Serially-reusable Resources)
  - 시스템 내에 항상 존재 하는 자원
  - 사용이 끝나면, 다른 프로세스가 사용 가능
  - ex) Processor, memory, disk drive, program 등 
- CR(consumable Resources)
  - 한 프로세스가 사용한 후에 사라지는 자원
  - ex) signal, message 등 

## Deadlock과 자원의 종류
- Deadlock을 발생시킬 수 있는 자원의 형태
  - Non-preemptible resources  
    한 번 사용하면 끝까지 사용하게 되므로 deadlock 가능성이 있음  
    자원을 빼앗을 수 있으면 문제는 발생 안 할 것임
  - Exclusive allocation resources  
    혼자 자원을 쓰는 경우에 deadlock 발생 가능
  - Serially reusable resources
  - 할당 단위는 영향을 미치지 않음
- CR(consumable Resources)을 대상으로 하는 Deadlock model
  - deadlock이 발생할 수 있지만, 너무 복잡하여 이번 시간에는 제외하기로 하자

## Deadlock 발생의 예
![img](https://github.com/koni114/Operating-system/blob/master/img/os_49.JPG)

- 3번 상태는 deadlock 상태는 아님. 만약 P2가 R1을 반납한다면 정상적인 프로세스 수행 가능
- 4번 상태에서는 P2가 P1이 가지고 있는 자원을 요청함으로써 절대 일어날 수 없는 event 상태가 됐으므로, deadlock 상태가 됨

## Deadlock Model(표현법)
- Graph Model
- State transition Model

### Graph Model
- Node
  - 프로세스 노드(P1, P2), 자원 노드(R1, R2)
- Edge
  - Rj -> Pi : 자원 Rj 이 프로세스 Pi에 할당 됨
  - Pi -> Rj : 프로세스 Pi가 자원 Rj을 요청(대기 중)  

![img](https://github.com/koni114/Operating-system/blob/master/img/os_50.JPG)
- 앞에 했던 deadlock 예제를 그림으로 표현한 것임
- cycle이 상태를 deadlock임을 확인할 수 있음

### State Transition Model
- 예제
  - 2개의 프로세스와 A type의 자원 2개(unit) 존재(Ra 2개)
  - 프로세스는 한번에 자원 하나만 요청/반납 가능
- State는 총 5가지 경우의 수를 가짐
![img](https://github.com/koni114/Operating-system/blob/master/img/os_51.JPG)
- 만약 프로세스가 2개라면 5x5 --> 25가지의 state를 가질 수 있음
![img](https://github.com/koni114/Operating-system/blob/master/img/os_52.JPG)
- 상태가 변하는 것을 edge로 표현
- deadlock이 S33에서 발견됨. 둘 다 하나를 잡고 하나를 요청하게 되면 deadlock임을 알 수 있음

## Deadlock 발생 필요 조건
- 아래 4가지 case를 모두 성립해야 deadlock이라는 얘기!
- 자원의 특성
  - Exclusive use of resources -- 1
  - Non-preemptible resources -- 2 
- 프로세스의 특성
  - Hold and wait(Partial allocation) -- 3 
    - 자원을 하나 hold하고 다른 자원 요청 
  - Circular wait -- 4

## Deadlock 해결 방법
- Deadlock prevention methods 
- Deadlock avoidance method
- Deadlock detection and deadlock recovery methods

## Deadlock Prevention
- 4개의 deadlock 발생 필요 조건 중 하나를 제거
  - Exclusive use of resources
  - Non-preemptible resources
  - Hold and wait(Partial allocation)
  - Circular wait
- Deadlock이 절대 발생하지 않음  
- 모든 자원을 공유 허용
  - Exclusive use of resources 조건 제거
  - 현실적으로 불가능
- 모든 자원에 대해 선점 허용
  - Non-preemptible resources 조건 제거
  - 현실적으로 불가능
  - 유사한 방법
    - 프로세스가 할당 받을 수 없는 자원을 요청한 경우, 기존에 가지고 있던 자원을 모두 반납하고 작업 취소
      - 이후 처음(또는 check-point)부터 다시 시작
    - 심각한 자원 낭비 발생 --> 비현실적      
- 필요 자원 한번에 모두 할당(Total allocation)
  - Hold and wait 조건 제거
  - 자원 낭비 발생
    - 필요하지 않는 순간에도 가지고 있음
  - 무한 대기 현상 발생 가능
- Circular wait 조건 제거
  - Totally allocation을 일반화한 방법
  - 자원들에게 순서를 부여
  - 프로세스는 순서의 증가 방향으로만 자원 요청 가능  
    한 방향으로만 요청하므로 원을 만들어 낼 수 없음 
  - 자원 낭비 발생. 내가 쓸 수 있는 자원이 있는데도 할당 못받음
- 4개의 deadlock 발생 필요 조건 중 하나를 제거
- Deadlock이 절대 발생하지 않지만 심각한 자원 낭비가 발생
- 비현실적임!

## Deadlock Avoidance
- 시스템의 상태를 계속 감시
- 시스템이 deadlock 상태가 될 가능성이 있는 자원 할당 요청 보류  
  --> 시스템을 항상 safe state로 유지
- Safe state
  - 모든 프로세스가 정상적 종료 가능한 상태
  - Safe sequence가 존재하느냐로 판단 가능
    - Deadlock 상태가 되지 않을 수 있음을 보장  
- Unsafe state
  - Deadlock 상태가 될 가능성이 있음
  - 반드시 발생한다는 의미는 아님  
- 가정(1~3 때문에 크게 현실적이지는 않음)
  - 프로세스의 수가 고정됨
  - 자원의 종류와 수가 고정됨
  - 프로세스가 요구하는 자원 및 최대 수량을 알고 있음
  - 프로세스는 자원을 사용 후 반드시 반납
- Not practical    
- Dijkstra's algorithm
  - Banker's algorithm
- Habermann's algorithm   

### Dijkstra's banker's algorithm
- 은행원 알고리즘. 
- Deadlock avoidance를 위한 간단한 이론적 기법
- 가정
  - 한 종류(resource type)의 자원이 여러 개(unit)
- 시스템을 항상 safe state로 유지   

![img](https://github.com/koni114/Operating-system/blob/master/img/os_53.JPG)
- 한 개의 타입의 소스, 총 10개의 소스가 있으며 3개의 프로세스가 있다고 가정
- Max.Claim : 최대 자원 필요 개수. Cur.Alloc : 현재 할당 개수. Additional Need : 앞으로 필요한 개수.
- 내가 10만원을 가지고 있을 때, 1,2,3번이 나한테 돈을 빌려달라고 함  
  현재 1번 만원, 2번 5만원, 3번은 2만원을 빌랴준 상태, 나머지 필요한 금액이 존재  
  가정은 다 믿을 수 있어 돈을 반드시 반납함
- 그렇다면 누구한테 제일 먼저 빌려줄까? 라는 질문이 이 알고리즘의 핵심

- 정답 
  - 내 수중에 있는 2만원을 가지고 P1한테 빌려주면 일을 수행 후 3만원 반납  
    그 다음 3만원을 P3에게 빌려주고, 마지막으로 P2에게 반납  
  - Available resource units : 2
  - 실행 종료 순서 : P1 -> P3 -> P2(Safe seqeunce)
  - 현재 상태에서 안전 순서가 하나이상 존재하면 안전 상태임

![img](https://github.com/koni114/Operating-system/blob/master/img/os_54.JPG)
- State-2에서는 내가 가지고 있는 남은 자원을 가지고 그 누구도 만족시키지 못함 --> unsafe state
- Available resource units : 3
- No Safe sequnce
- 반드시 교착상태는 아님! --> 자원을 빌려달라고 안 할 수도 있기 때문
- 임의의 순간에 세 프로세스들이 모두 세 개 이상의 단위 자원을 요청하는 경우 시스템은 교착상태에 놓이게 됨
- 그렇다면 banker's algorithm은 무엇일까? 

![img](https://github.com/koni114/Operating-system/blob/master/img/os_53.JPG)
- P1이 자원을 1개 더 요청. 그러면 빌려 줄지 말지 정해야 함
- 알고리즘은 줬다고 가정하고 시뮬레이션을 돌려보는 것임. 시뮬레이션을 돌려보면 다음 처럼 됨

![img](https://github.com/koni114/Operating-system/blob/master/img/os_54.JPG)
- P1의 Cur.Alloc을 2로 만들어봄
- 그런 다음 safe-state가 가능한지 확인 해보는 것임. --> 내 자원이 1인 상태에서 P1 -> P3 -> P2하면 됨
- 반대로 P2가 자원을 하나 빌려달라고 한 경우에는 safe sequence가 없음
- 이것이 바로 banker's algorithm

### Habermann's algorithm
- Dijstra's algorithm의 확장
- 여러 종류의 자원 고려
  - Multiple resource types
  - Multiple resource units for each resource type
- 시스템을 항상 safe state로 유지  

![img](https://github.com/koni114/Operating-system/blob/master/img/os_55.JPG)
- 3 types of resources : Ra, Rb, Rc
- Number of resource units for each type : (10, 5, 7)
- 5 processes

![img](https://github.com/koni114/Operating-system/blob/master/img/os_56.JPG)
- Available resource units : (3, 3, 2) 
- Safe sequence : P2 -> P4 -> P1 -> P3 -> P5
- Safe state because there exist a safe sequnce

## Deadlock Avoidance
- Deadlock의 발생을 막을 수 있음
- High overhead
  - 항상 시스템을 감시하고 있어야 함
- Low resource utilization
  - Safe state 유지를 위해, 사용되지 않는 자원이 존재
- <b>Not practical</b>
  - 가정
    - 프로세스 수, 자원 수가 고정
    - 필요한 최대 자원 수를 알고 있음

## Deadlock Detection
- Deadlock 방지를 위한 사전 작업을 하지 않음
  - Deadlock이 발생 가능
- 주기적으로 deadlock 발생 확인
  - 시스템이 deadlock 상태인가?
  - 어떤 프로세스가 deadlock 상태인가?
- Resource Allocation Graph(RAG) 사용    

### Resource Allocation Graph(RAG)
![img](https://github.com/koni114/Operating-system/blob/master/img/os_58.JPG)
- Deadlock 검출을 위하여 사용
- Directed, bipartite Graph(process와 자원의 이분그래프)

![img](https://github.com/koni114/Operating-system/blob/master/img/os_59.JPG)
- Directed graph G = (N, E)
  - N = {Np, Nr} where
    - Np is the set of processes = {P1, P2, ... , Pn}
    - and Nr is the set of resources = {R1, R2, ..., Rm}   

![img](https://github.com/koni114/Operating-system/blob/master/img/os_60.JPG)
- Resource Allocation Graph(RAG)
  - Edge는 Np와 Nr 사이에만 존재
    - e = (Pi, Rj) : 자원 요청
    - e = (Rj, Pi) : 자원 할당   

![img](https://github.com/koni114/Operating-system/blob/master/img/os_61.JPG)
- Rk : k type의 자원
- tk : Rk의 단위 자원 수(Rk에 속하는 자원 개수)
- |(a,b)| : (a,b) edge의 수 

### RAG example
![img](https://github.com/koni114/Operating-system/blob/master/img/os_62.JPG)
- 위 그림의 상태는 deadlock인가? 
- 쉽게 deadlock 여부를 판단할 수 있는 algorithm이 존재 --> Graph reduction

## Deadlock Detection Method
- Graph reduction
  - 주어진 RAG에서 edge를 하나씩 지워가는 방법
  - Completely reduced(다 지워짐)
    - 모든 edge가 제거 됨
    - Deadlock에 빠진 프로세스가 없음
  - Irreducible(다 지울 수 없는 edge가 있음)
    - 지울 수 없는 edge가 존재
    - 하나 이상의 프로세스가 deadlock 상태     
  - Unblocked process
    - unblocked process에 연결된 edge를 다 지움 
    - 필요한 자원을 모두 할당 받을 수 있는 프로세스  
![img](https://github.com/koni114/Operating-system/blob/master/img/os_63.JPG)
- Pi가 요청하는 모든 자원에 대해(LHS)  
- 각각의 자원들의 자원 수에서 해당 자원이 할당한 수를 뺀 값(RHS)보다 작으면 unblocked process 

- Graph reduction procedure
  - Unblocked preocess에 연결 된 모든 edge를 제거
  - 더 이상 unblocked process가 없을 때까지 반복
  - 최종 그래프에서
    - 모든 edge가 제거됨(Completely reduced)
      - 현재 상태에서 deadlock이 없음
    - 일부 edge가 남음(irreducible)
      - 자원을 할당 받을 수 없는 process가 존재한다는 의미 
      - 현재 deadlock이 존재     

- Graph Reduction(example 1)
![img](https://github.com/koni114/Operating-system/blob/master/img/os_64.JPG)

- Graph Reduction(example 2)
![img](https://github.com/koni114/Operating-system/blob/master/img/os_65.JPG)

- Graph Reduction
  - High overhead
    - 검사 주기에 영향을 받음
    - Node의 수가 많은 경우
  - Low overhead deadlock detection methods(Special case)
    - Case-1) Single-unit resources
      - Cycle detection 
    - Case-2) Single-unit request in expedient state 
      - Knot detection

## Deadlock Avoidance vs Detection
- Deadlock avoidance
  - 최악의 경우를 생각
    - 앞으로 일어날 일을 고려
  - Deadlock이 발생 하지 않음
- Deadlock detection
  - 최선의 경우를 생각
    - 현재 상태만 고려
  - Deadlock 발생 시 Recovery 과정이 필요       

## Deadlock Recovery
- Deadlock을 검출 한 후 해결하는 과정
- Deadlock recovery methods
  - Process termination
    - Deadlock 상태에 있는 프로세스를 종료 시킴 
    - 강제 종료된 프로세스는 이후 재시작 됨 
  - Resource preemption 
    - Deadlock 상태 해결 위해 선점할 자원 선택
    - 선정 된 자원을 가지고 있는 프로세스에서 자원을 빼앗음
      - 자원을 빼앗긴 프로세스는 강제 종료됨  
- Process termination
  - Deadlock 상태인 프로세스 중 일부 종료
  - Termination cost model
    - 종료 시킬 deadlock 상태의 프로세스 선택
    - Termination cost
      - 우선순위 / Process priority
      - 종류 / Process type
      - 총 수행시간 / Accumulated execution time of the process
      - 남은 수행 시간 / Remaining time of the process
      - 종료 비용 / Accounting cost
      - Etc.   
  - 종료 프로세스 선택
    - Lowest-termination cost process first
      - Simple
      - Low overhead
      - 불필요한 프로세스들이 종료 될 가능성이 높음 
    - Minimum cost recovery
      - 최소 비용으로 deadlock 상태를 해소 할 수 있는 process 선택
        - 모든 경우의 수를 고려 해야 함
      - Complex
      - High overhead
        - O(2^k)         
- Resource preemption
  - Deadlock 상태 해결을 위해 선점할 자원 선택
  - 해당 자원을 가지고 있는 프로세스를 종료시킴
    - Deadlock 상태가 아닌 프로세스가 종료 될 수 있음
    - 해당 프로세스는 이후 재시작 됨 
  - 선점할 자원 선택
    - Preemption cost model 필요
    - Minimum cost recovery method 사용
      - O(r)      
- Checkpoint-restart-method
  - 위의 recovery 방법들은 지금까지 수행해 온 process들을 불합리하게 종료시켜야 하는 단점이 있음 
  - 프로세스의 수행 중 특정 지점(checkpoint)마다 context를 저장
  - Rollback을 위해 사용
    - 프로세스 강제 종료 후, 가장 최근의 checkpoint에서 재시작  

![img](https://github.com/koni114/Operating-system/blob/master/img/os_66.JPG)
# 메모리 관리(Main memory management)
## 메모리(기억장치)의 종류
![img](https://github.com/koni114/Operating-system/blob/master/img/os_67.JPG)
- 레지스터와 캐시는 HW가 관리
- 메인 메모리와 보조기억장치는 SW가 관리

## 메모리(기억장치) 계층구조
![img](https://github.com/koni114/Operating-system/blob/master/img/os_68.JPG)
- Block 
  - 보조기억장치와 주기억장치 사이의 데이터 전송 단위
  - 보조기억장치에서 1bit만 읽으려고 해도 main memory는 최소 블록 단위로 전송됨
  - Size: 1 ~ 4KB
- Word
  - 주기억장치와 레지스터 사이의 데이터 전송 단위
  - 내 컴퓨터는 64bit야! 라고 하는 것은 '워드' 단위라고 말해도 틀린 말은 아님
  - Size : 16 ~ 64bits   

## Address Binding
- Binding은 묶는다! 라는 뜻, 즉 address를 묶는다?
- 프로그램의 논리 주소(int a)를 실제 메모리의 물리 주소(100, 104..)로 매핑(mapping)하는 작업
- Binding 시점에 따른 구분
  - Compile time binding
  - Load time binding
  - Run time binding
![img](https://github.com/koni114/Operating-system/blob/master/img/os_69.JPG)

![img](https://github.com/koni114/Operating-system/blob/master/img/os_70.JPG)
- 어떤 프로그램을 짰을 때, 실제로 메모리에 실행되기 까지의 과정을 그려 놓은 것
- Compiler가 수행하는 시점에 binding이 일어나면 compile binding
- Load module --> exe를 생각하면 됨. 즉 load module을 만드는 작업을 linking이라고 함
- load module을 더블클릭하면 메모리에 올라감
- 메모리에 올려주는 것을 loader라고 함
- 즉 Linker -> Load module -> Loader 까지의 과정을 Load time, 메모리에 올라가는 시간을 Run time 이라고 함

### Compile time binding
- 프로세스가 메모리에 적재될 위치를 컴파일러가 알 수 있는 경우
  - 위치가 변하지 않음
- 프로그램 전체가 메모리에 올라가야 함

### Load time binding
- 메모리 적재 위치를 컴파일 시점에서 모르면, 대체 가능한 상대 주소를 생성
  ex) u + 100, u - 100... 
- 적재 시점(load time)에 시작 주소를 반영하여 사용자 코드 상의 주소를 재설정
- 프로그램 전체가 메모리에 올라가야 함          
![img](https://github.com/koni114/Operating-system/blob/master/img/os_71.JPG)
- 처음 program code에서 시작 주소가 0번이라고 가정하고 상대 주소 기반으로 수행. ex) 360으로 가라! 1204을 로딩해라! 등.
- loading time에서 할당된 시작 주소가 400번이면, 상대적인 + 400만큼 이동. 이를 <b>relocation이라고 함</b>

### Run-time binding
- Address binding을 수행시간까지 연기
- running 상태가 될 때 address를 할당
  - 프로세스가 수행 도중 다른 메모리 위치로 이동할 수 있음
- HW의 도움이 필요
  - MMU : Memory Management Unit
- 대부분의 OS가 사용 

![img](https://github.com/koni114/Operating-system/blob/master/img/os_72.JPG)

## Dynamic Loading
- 앞서 address binding을 다룰 때는 우리 프로그램이 메모리에 통으로 올라간다고 가정하고 생각함. 하지만 그렇지 못할 경우도 있을 것임. 메모리에 프로그램 전체를 올릴 필요가 없음. 원하는 부분만 올리고 싶음 !  
이 것이 dynamic loading.  
- 모든 루틴(= function)을 교체 가능한 형태로 디스크에 저장
- 실제 호출 전까지는 루틴을 적재하지 않음
  - 메인 프로그램만 메모리에 적재하여 수행
  - 루틴의 호출 시점에 address binding 수행
- 장점
  - 메모리 공간의 효율적 사용   

## Swapping
- 프로세서 할당이 끝나고 수행 완료 된 프로세스는 swap-device로 보내고(Swap-out)
- 새롭게 시작하는 프로세스는 메모리에 적재(Swap-in)

![img](https://github.com/koni114/Operating-system/blob/master/img/os_73.JPG)

## Memory allocation
- 어떻게 메모리가 프로세스에게 자원을 할당해 주느냐?
- Continuous Memory Allocation(연속할당)
  - Uni-programming
  - Multi-programming
    - Fixed partition(FPM)
    - variable partition(VPM)
- Non-continuous Memory Allocation(비연속할당) 
  - Next chapter !    

## Continuous Memory Allocation
- 프로세스(context)를 하나의 연속된 메모리 공간에 할당하는 정책
  - 프로그램, 데이터, 스택 등
- 메모리 구성 정책
  - 메모리에 동시에 올라갈 수 있는 프로세스 수
    - Multiprogramming degree
  - 각 프로세스에게 할당되는 메모리 공간 크기
  - 메모리 분할 방법     
- Uni-programming
  - Multiprogramming degree = 1
- Multi-programming
  - Fixed(static) partition multi-programming(FPM)
    - 고정 분할
  - Variable(dynamic) partition multi-programming(VPM)
    - 가변 분할      

### Uni-programming
- 하나의 프로세스만 메모리 상에 존재
- 만약 Pi라고 하는 프로세스가 있으면 User Program에 올려주기만 하면 됨
- 가장 간단한 메모리 관리 기법
  - kernel
  - User program
  - Wasted Space 
- 문제점
  - 프로그램의 크기 > 메모리 크기  
  해당 문제는 프로그램의 크기를 짤라서 수행하면 되는데 이 일은 OS가 직접 할 수 없고 사용자(프로그램)이 해야 함  
  프로그램이 어디까지는 공통적으로 필요로하고, 나머지는 번갈아가면서 올리면 됨 --> <b>Overlay structure</b>
- 해결법
  - Overlay structure
    - 메모리에 현재 필요한 영역만 적재
    - 사용자가 프로그램의 흐름 및 자료구조를 모두 알고 있어야 짤라서 올리고 내려줄 수 있음

![img](https://github.com/koni114/Operating-system/blob/master/img/os_74.JPG)

![img](https://github.com/koni114/Operating-system/blob/master/img/os_75.JPG)

- 문제점
  - 커널(kernel) 보호  
    커널을 건드리면 프로그램이 죽을 수 있으므로, kernel을 건드리지 않게 해야 함 --> boundary register 사용
  - Low system resource untilization  
    4인석에 고양이가 혼자 앉아있듯이, 메모리 공간의 낭비가 발생 
  - Low system performance
- 해결방법
  - 경계 레지스터(boundary register) 사용   
  - Multi-programming


### Multi-programming - Fixed Partition Multiprogramming
- 메모리 공간을 고정된 크기로 분할
  - 미리 분할되어 있음 
- 각 프로세스는 하나의 partition(분할)에 적재
  - Process: Partition = 1 : 1 --> 한 방에는 한 명의 프로세스만 들어갈 수 있음
- Partition의 수 = K
  - Multiprogramming degree = K 

![img](https://github.com/koni114/Operating-system/blob/master/img/os_76.JPG)

- 커널 및 사용자 영역 보호
- 각 파티션의 경계마다 boundary address를 쓰면 됨
![img](https://github.com/koni114/Operating-system/blob/master/img/os_77.JPG)

#### Fragmentation(단편화) ** 중요
- Internal fragmentation
  - 내부 단편화
  - 각 방의 process를 할당하고 난 후에 남는 memory 자원이 있는 경우
  - Partition 크기 > Process 크기
    - 메모리가 낭비됨
- External fragmentation
  - 외부 단편화
  - (남은 메모리 크기 > Process 크기)지만, 연속된 공간이 아님
    - 메모리가 낭비됨     
- fixed Partition Multiprogramming 요약
  - 고정된 크기로 메모리 미리 분할
  - 메모리 관리가 편함
    - Low overhead
  - 시스템 자원이 낭비 될 수 있음 
  - Internal/external fragmentation    

### Multi-programming - Variable Partition Multiprogramming
- 핵심은 메모리 공간(케익)이 동적으로 분할될 수 있음!
- 초기에는 전체가 하나의 영여 
- 프로세스를 처리하는 과정에서 메모리 공간이 동적으로  분할
- No internal fragmentation

### VPM Example
- State table은 FPM에서와는 다르게 size가 유동적으로 변함
- Memory space: 120MB
- 초기 상태
- 프로세스 A(20MB)가 적재 된 후
- 프로세스 B(10MB)가 적재 된 후
- 프로세스 C(25MB)가 적재 된 후
- 프로세스 D(20MB)가 적재 된 후
- 프로세스 B가 주기억장치를 반납 한 후
- 프로세스 E(15MB)가 적재된 후
- 프로세스 D가 주기억장치를 반납 한 후

![img](https://github.com/koni114/Operating-system/blob/master/img/os_78.JPG)

![img](https://github.com/koni114/Operating-system/blob/master/img/os_79.JPG)

![img](https://github.com/koni114/Operating-system/blob/master/img/os_80.JPG)

- 차례 차례 동적으로 메모리를 할당하면 됨
- 기억해야 할 것은, internal fragmentation이 일어나지 않음

![img](https://github.com/koni114/Operating-system/blob/master/img/os_81.JPG)

- 이번에는 해당 메모리가 Exit함. 이런식으로 exit가 일어나면, 자연스레 빈 공간이 생기게 됨

## 배치 전략(Placement strategies)
- 앞서 본 것처럼 빈 공간이 군데군데 생겨나게 되는데, 이러한 공간에 어떻게 다시 프로세스를 배치할 것이냐?에 대한 전략
- First-fit(최초적합)
  - 위에서 부터 차례차례 SCAN하여 프로세스가 할당 가능한 공간에 바로 할당하는 방법 
  - 충분한 크기를 가진 첫 번째 partition 선택
  - Simple and low overhead --> 할당할 수 있는 제일 처음을 선택하는 것이므로 간단하고 low overhead
  - 공간 활용률이 떨어질 수 있음 --> 프로세스가 12KB인데, 처음만난 공간이 13KB이면 사용할 확률이 낮아지는 등 누굴 만나느냐에 따라 공간활용률이 떨어질 수 있음  
     
![img](https://github.com/koni114/Operating-system/blob/master/img/os_82.JPG)

- Best-fit(최적적합)
  - process가 들어갈 수 있는 partition중 <b>가장 작은 곳 선택</b>
  - 탐색시간이 오래 걸림
    - 모든 partition을 살펴봐야 함
  - 크기가 큰 partition을 유지할 수 있음
  - 작은 크기의 partition이 많이 발생
    - 활용하기 너무 작아짐

![img](https://github.com/koni114/Operating-system/blob/master/img/os_83.JPG)

- Worst-fit(최악 적합)
  - Process가 들어갈 수 있는 partition 중 가장 큰 곳 선택
  - 탐색시간이 오래 걸림
    - 모든 partition을 살펴봐야 함
  - 작은 크기의 partition 발생을 줄일 수 있음
  - 큰 크기의 partition 확보가 어려움
    - 큰 프로세스에게 필요한

![img](https://github.com/koni114/Operating-system/blob/master/img/os_84.JPG)

- Next-fit(순차 최초 적합)
  - 프로세스를 할당한 위치의 다음부터 순차적으로 탐색하는 방법 
  - 최초 적합 전략과 유사
  - State table에서 마지막으로 탐색한 위치부터 탐색
  - 메모리 영역의 사용 빈도 균등화
  - Low overhead 


## Coalescing holes(공간 통합)
- external fragmentation 문제가 발생한 경우의 해결 방법! 
- 인접한 빈 영역을 하나의 partition으로 통합
  - process가 memory를 release하고 나가면 수행
  - Low overhead 
- 하나의 프로세스가 나가고 난 후 빈 공간의 memory를 합치는 것을 coalescing holes 라고 함
- 공간을 합치는 것은 프로세스가 나가고 난 후 바로 합치면 됨(overhead가 적은 일)
![img](https://github.com/koni114/Operating-system/blob/master/img/os_85.JPG)

## Storage Compaction(메모리 압축)
- 공간이 비어있는데, 떨어져 있으면 빈 공간을 위로 쭉 올려서 공간을 만들어내는 것. 이를 공간 압축이라고 함
- 모든 빈 공간을 하나로 통합
- 프로세스 처리에 필요한 적재 공간 확보가 필요 할 때 수행
- High overhead 
  - 모든 process 재배치(Process 중지) --> 전체 위치를 변경해야 하기 때문
  - 일정시간, 일정 기간 요청이 있을 때문 수행해야 함
  - 많은 시스템 자원을 소비 
![img](https://github.com/koni114/Operating-system/blob/master/img/os_86.JPG)

- 이런 것들을 왜 공부해야 할까?   
실제로 메모리를 할당 받는 행위(new ~~)는 속도가 많이 느려지는 행위. 그렇다면 빠르게 하기 위한 방법으로
우리들 만의 memory pool을 만들어 메모리 시스템을 만들 수 있음. 즉 1GB 메모리 공간을 쓴다는 것을 알고 있으면  
OS에게 일단 1GB의 메모리를 할당 받고(동적 할당이 1번만 있음), 그 다음부터는 OS까지 가지 말고, Pointer를 주고 10MB만써! 처럼 포인터에게 전달해 주면 됨. 그렇다면 메모리 할당 방법을 배웠으므로, FPM or VPM 등을 구현하여 적용할 수 있음. --> 이런 방법이 할당 동적 할당을 받는 것 보다 훨씬 빨라 성능의 이슈가 있을 때 이런 전략을 사용할 수 있음  
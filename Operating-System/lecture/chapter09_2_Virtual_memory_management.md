# chapter 09_2 가상 메모리 관리
## Outline 
- Virtual memory management
- Cost model
- Hardware components
- Software components
- Page replacement schemes
  - FA-based schemes
  - VA-based schemes
- Other considerations  

## 가상 메모리 관리
- 가상 메모리를 어떻게 하면 가장 효율적으로 사용할 수 있는가?에 대한 고민
- 가상 메모리(기억장치)
  - Non -continous allocation system
    - 사용자 프로그램을 block으로 분할하여 적재/실행
  - Paging/Segmentation system
- 가상 메모리 관리의 목적
  - 가상 메모리 시스템 성능 최적화  
    - Cost model
    - 다양한 최적화 기법      

## Cost Model for Virtual Mem. Sys.
- Page fault 
  - CPU가 메모리의 page를 찾을 때, 해당 메모리에 page가 없는 경우를 page fault라고 함. page fault가 발생하면, proess 상태에서 running -> asleep 상태로 전환하는데, 이때 context swtiching(overhead)가  발생
- Page fault frequency(발생 빈도)
- Page fault rate(발생률)
- Page fault rate를 최소화 할 수 있도록 전략들을 설계해야 함
  - Context switch 및 kernel 개입을 최소화
  - 시스템 성능 향상 
- Page reference string(d)
  - 참조한 page들을 문자열로 써 놓은 것  
  - 프로세스의 수행 중 참조한 페이지 번호 순서
  - w(page reference string) = r1, r2, r.., rk ... kt
    - ri = 페이지 번호, ri --> {0, 1, 2, ..., N-1}
    - N  = 프로세스의 페이지 수(0 ~ N-1)
  - Page fault rate = F(w)
    - F(w) = Num.of page faults during w / |w|
    - F(w) = page fault 수 / 프로세스가 참조한 전체 페이지 수
  - 왜 Page reference string을 참조를 할까? 
    - 어떤 page를 읽어왔는지에 대한 정보가 있어야 효율성 판단 가능
    - 효율성 판단 기준 

## Hardware Components
- Address translation(변환) device(주소 사상 장치)
  - 주소 사상을 효율적으로 수행하기 위해 사용
    - E.g., TLB(associated memories), Dedicated-page-table register, Cache memories
- Bit vectors
  - Bit vectors 예시 --> [0, 1, 0, 0, 1, 0 ..]
  - 예를 들어 memory에 page Frame에 가득 찼다고 가정하고, 새로운 page를 할당하려고 할 때, 어디다가 할당하는 것이 가장 좋은지 판단하기 위한 무언가가 필요로 함
  - 이 기준으로 활용할 수 있는 것이 bit vectors 
  - Page 사용 상황에 대한 정보를 기록하는 비트들
  - 대표적인 bit 2가지 
  - Reference bits(used bit)
    - 참조 비트 --> 해당 page의 참조 여부를 기록한 bit
  - Update bits(modified bits, write bits, dirty bits)
    - 갱신 비트 --> page data가 갱신되었는가? 
- 아래 그림은 bit vectors에 대한 설명 그림
![img](https://github.com/koni114/Operating-system/blob/master/img/os_98.JPG)
- memory의 page frame 하나마다 update bit와 reference bit가 있다고 생각하자
- bit를 PMT에다가 넣어두고 정보를 관리하겠다! 라는 것임

## Bit vectors
### Reference bit vectors
  - 메모리에 적재된 각각의 page가 최근에 참조되었는지를 표시
  - 운영
    - 프로세스에 의해 참조되면 page의 Ref.bit를 1로 설정
    - 주기적으로 만든 모든 reference bit를 0으로 초기화
  - Reference bit를 확인함으로서 최근에 참조된 page를 확인 가능   

![img](https://github.com/koni114/Operating-system/blob/master/img/os_99.JPG)
- 특정 시점마다 계속 reset을 수행하고, 그 사이에 참조가 됐으면 reference bit를 1로 변경해줌
 
### Update bit vector
  - Page가 메모리에 적재된 후, <b>프로세스에 의해 수정 되었는지를 표시</b>
  - 왜 update 여부를 bit vector에 기록할까?  
    swap-device에 있는 데이터가 memory상에 올라가고 memory에 있는  
    정보가 바뀌면 작업 수행 종료 후 swap-device에도 변경 사항을 알려줘야 함!  
    --> data 무결성 유지
  - 주기적 초기화 없음. 메모리에서 나올 때 초기화 함
  - Update bit = 1
    - 해당 page의 (Main memory 상 내용) != (Swap device의 내용)
    - 해당 paged의 대한 Write-back(to swap device)이 필요  

## Software components
- 가상 메모리 성능 향상을 위한 관리 기법들
  - Allocation strategies(할당 기법)
  - Fetch strategies
  - placement strategies(배치 기법)
  - replacement strategies(교체 기법)
  - Cleaning strategies(정리 기법)
  - Load control strategies(부하 조절 기법) 

### Allocation Strategies
- 각 프로세스에게 메모리를 얼마나 줄 것인가? 
  - Fixed allocation(고정 할당)
    - 프로세스의 실행 동안 고정된 크기의 메모리 할당 
  - Variable allocation(가변 할당) 
    - 프로세스의 실행 동안 할당하는 메모리의 크기가 유동적
- 고려사항
  - 프로세스 실행에 필요한 메모리 양을 예측해야 함
  - 너무 큰 메모리 할당(Too much allocation) -> 메모리 낭비
  - 너무 적은 메모리 할당(Too small allocation) -> 시스템 성능 저하   

### Fetch Strategies
- Fetch? --> 운영체제, 디스크 시스템, 메모리에서는 어떤 데이터를 가져오는 것을 말함
- 특정 page를 메모리에 언제 적재할 것인가? 
  - Demand fetch(demand paging)
    - 프로세스가 참조하는 페이지들만 적재
    - Page fault overhead
  - Anticipatory fetch(pre-paging, preFetch)
    - 참조될 가능이 높은 page 예측
    - 가까운 미래에 참조될 가능성이 높은 page를 미리 적재
    - 예측 성공 시, page fault overhead가 없음
    - 실패 했을 때의 더 큰 overhead 발생
    - Prediction overhead(kernel의 개입), Hit ratio에 민감함    
- 실제 대부분의 시스템은 Demand fetch 기법 사용
  - 일반적으로 준수한 성능을 보여줌
  - Anticipatory fetch
    - Prediction overhead, 잘못된 예측 시 자원 낭비가 큼     
- 내가 만든 프로그램 내부적으로 가상 메모리 시스템을 구현하여 사용 할 수 있겠다!

### Placement Strategies
- Page/segment를 어디에 적재할 것인가?
- Paging system에는 불필요
- Segmentation system에서의 배치 기법
  - First-fit
  - Best-fit
  - Worst-fit
  - Next-fit

### Replacement Strategies
- 새로운 page를 어떤 page와 교체할 것인가?(빈 page frame이 없는 경우)
- Fixed allocation을 위한 교체 기법
- Variable allocation을 위한 교체 기법

### Clean Strategies
- 변경 된 page를 언제 write-back 할 것인가? 
  - 변경된 내용을 swap device에 반영
  - Demand cleaning
    - 해당 page에 메모리에서 내려올 때 write-back 
  - Anticipatory cleaning(pre-cleaning)
    - 더 이상 변경될 가능성이 없다고 판단 할 때, 미리 write-back
    - page 교체 시 발생하는 write-back 시간 절약
    - Write-back 이후, page 내용이 수정되면, overhead!
- 실제 대부분의 시스템은 Demand cleaning 기법 사용
  - 일반적으로 준수한 성능을 보여줌
  - Anticipatory cleaning
    - prediction overhead, 잘못된 예측 시 자원 낭비가 큼       

### Load Control Strategies
- Load : 부하의 의미
- 시스템의 multi-programming degree 조절
- multi-programming degree --> 수행되는 프로세스의 수
  - Allocation strategies 와 연계됨
- 적정 수준의 multi-programming degree를 유지 해야 함
  - Plateau 영역으로 유지
  - multi-programing degree를 낮게 -> 저부하 상태(Under-loaded)
    - 시스템 자원 낭비, 성능 저하
  - multi-programming degree를 높게 -> 고부하 상태(Over-loaded),
    - 자원에 대한 경쟁 심화, 성능 저하
    - Thrashing(스레싱) 현상 발생
      - 과도한 page fault가 발생하는 현상       
- thrashing 현상 경험하기
  - Hwp -> 엔터를 5초이상 계속 눌러보면, 마우스 및 강의들이 버벅거리는 현상이 발생하기 시작함 

![img](https://github.com/koni114/Operating-system/blob/master/img/os_100.JPG)
- 성능 지표 중에 throughput(처리량)이 있음

## Replacement strategies - deeping
### Locality
- 프로세스가 프로그램/데이터의 특정 영역을 집중적으로 참조하는 현상
- 원인
  - Loop structure in program
  - Array, structure 등의 데이터 구조
- 공간적 지역성(Spatial locality) 
  - 참조한 영역과 인접한 영역을 참조하는 특성
- 시간적 지역성(Temporal locality)
  - 한 번 참조한 영역을 곧 다시 참조하는 특성     

### Locality(Example)
- 가정 
  - Paging system
  - Page size = 1000 words  
    --> 1개의 page가 1000개의 word로 구성
  - Machine instruction size = 1 word
  - 주소 지정은 word 단위로 이루어짐
    --> 주소를 지칭할 때, word 단위로 이루어짐
  - 프로그램은 4번 page 에 continuous allocation 됨
  - n = 1000
- 아래 코드가 프로그램으로 생각하며, array의 크기는 1000이고,   
  해당 프로그램은 4번 page에 continuous allocation됨 
~~~c
for <- 1 to n do
    A[i] <- B[i] + C[i];
endfor
~~~

![img](https://github.com/koni114/Operating-system/blob/master/img/os_101.JPG)
~~~c
(R1) <- ONE            // 4, 9
(R2) <- n              // 4, 9
compare R1, R2         // 4, 4
branch geater 4009     // 
(R3)  <- B(R1)         // 4, 7
(R3)  <- (R3) + C(R1)  // 4, 8 
A(R1) <- (R1) + 1      // 6, 4
R(1)  <- (R1) + 1      // 4, 4
branch 4002            
~~~
- 위의 기계어 코드의 실행 시 참조하는 age reference string 임
- 잘 보면, branch 4002 때문에 n(1000)번 반복하게 됨
- w = 494944(474846444)^1000
- 9000번의 메모리 참조 중 5개의 page만을 집중적으로 접근하게 됨  
  4, 6, 7, 8, 9번 --> locality

## Replacement Strategies - algorithm list
- Fixed allocation
  - MIN(OPT, B0) algorithm
  - Random algorithm
  - FIFO(First In First Out) algorithm 
  - LRU(Least Recently Used) algorithm
  - LFU(Least Frequently Used) algorithm
  - NUR(Not Used Recently) algorithm
  - Clock algorithm
  - Second chance algorithm
- Variable allocation
  - WS(Working Set) algorithm
  - PFF(Page Fault Frequency) algorithm
  - VMIN(Variable MIN) algorithm  

### Min Algorithm(OPT algorithm)
- 1966년 Belady에 의해 제시
- Minimize page falut frequency(proved)
  --> 가장 최적의 솔루션으로 증명되었으며, 이론적으로 해당 알고리즘을 사용하면 optimal
- 문제는 미래는 알 수 없음(reference string을 미리 알 수 없음)
  - Optimal solution
- 앞으로 가장 오랫동안 참조되지 않'을' page 교체
  - Tie-breaking rule : page 번호가 가장 큰/작은 페이지 교체
- 실현 불가능한 기법(Unrealizable)
  - Page reference string을 미리 알고 있어야 함     
- 교체 기법의 성능 평가 도구로 사용 됨  
  해당 알고리즘은 구현 불가능하지만, 해당 알고리즘과 다른 알고리즘과 비교 했을 때 최적에 얼마나 근접한지 성능 평가 도구로 활용할 수 있음

![img](https://github.com/koni114/Operating-system/blob/master/img/os_102.JPG)
- MIN Algorithm에서는 y를 교체 대상으로 선정. 가장 오랫동안 참조하지 않기 때문

![img](https://github.com/koni114/Operating-system/blob/master/img/os_103.JPG)

### Random Algorithm
- 무작위로 교체할 page 선택
- Low overhead
- No policy
- 평가에 기준으로 사용할 수 있음. random으로 돌린 것보다 성능이 안좋은지 좋은지 판단 가능


### FIFO Algorithm
- First In First Out
  - 가장 오래된 page를 교체
- Page가 적재된 시간을 알고 있어야 함
- 자주 사용되는 page가 교체될 가능성이 높음
  - Locality에 대한 고려가 없음

![img](https://github.com/koni114/Operating-system/blob/master/img/os_104.JPG)
- 결과적으로 z선택.
 
#### FIFO anomoly(Belady's anomaly)
- page fault를 줄이기 위해서 자원을 더 늘렸는데, 오히려 page fault가 늘어난 현상  
- FIFO 알고리즘의 경우, 더 많은 page frame을 할당 받음에도 불구하고 page fault의 수가 증가하는 경우가 있음     

![img](https://github.com/koni114/Operating-system/blob/master/img/os_107.JPG)

### LRU(Least Recently Used) Algorithm
- 가장 오랫동안 참조되지 않'은' page를 교체
- Page 참조 시 마다 시간을 기록해야 함
- Locality에 기반을 둔 교체 기법
- MIN algorithm에 근접한 성능을 보여줌
- 실제로 가장 많이 활용되는 기법

![img](https://github.com/koni114/Operating-system/blob/master/img/os_105.JPG)
- 위의 그림에서는 언제 참조했는지는 알기 어려움.

- 단점
  - 참조 시 마다 시간을 기록해야 함(Overhead)
    - 간소화된 정보 수집으로 해소 가능
      - 예) 정확한 시간 대신, 순서만 기록
  - Loop 실행에 필요한 크기보다 작은 수의 page frame이 할당 된 경우,  
    page fault 수가 급격히 증가함
    - ex) 1,2,3,4인 page를, 1,2,3인 page frame에 할당해야 할 때
    - 예) loop를 위한 |Ref.string| = 4 / 할당된 page frame 이 3개
    - Allocation 기법에서 해결 해야 함 --> page frame을 늘려주자      

![img](https://github.com/koni114/Operating-system/blob/master/img/os_106.JPG)

### LFU(Least Frequency Used) Algorithm
- 가장 참조 횟수가 적은 Page를 교체
  - Tie breaking rule : LRU
- Page 참조 시 마다, 참조 횟수를 누적 시켜야 함
- Locality 활용
  - LRU 대비 적은 overhead
- 단점
  - 최근 적재된 참조될 가능성인 높은 page가 교체될 가능성이 있음
  - 참조 횟수 누적 overhead     

![img](https://github.com/koni114/Operating-system/blob/master/img/os_107.JPG)

### NUR(Not Used Recently) Algorithm
- LRU approximation scheme
  - LRU보다 적은 overhead로 비슷한 성능 달성 목적
- Bit vector 사용
  - Reference bit vector(r), Update bit vector(m)
  - Reference bit는 참조 여부를 작성한 bit이며, Update bit는 최근에 갱신이 이루어 졌는지 작성한 bit  
    따라서 두 값이 1일수록 최근에 참조를 많이 했다는 이야기.
- 교체 순서
  - (r, m) = (0, 0)
  - (r, m) = (0, 1) --> update bit가 1이면 우선순위가 후순위로 밀려남. write-back을 수행해야 하기 때문 
  - (r, m) = (1, 0)
  - (r, m) = (1, 1) 

![img](https://github.com/koni114/Operating-system/blob/master/img/os_108.JPG)

### Clock Algorithm
- IBM VM/370 OS
- Reference bit 사용함
  - 주기적인 초기화 없음
- Page frame들을 순차적으로 가리키는 pointer(시계바늘)를 사용하여 교체될 page 결정  
- 시침이 돌아가면서 가리키는 page가 교체 대상이 됨
- 교체 대상은 reference bit가 0인 것들이 교체 대상

![img](https://github.com/koni114/Operating-system/blob/master/img/os_109.JPG)
- Pointer를 돌리면서 교체 page 결정
  - 현재 가리키고 있는 page의 reference bit(r) 확인
  - r = 0인 경우, 교체 page로 결정
  - <b>r = 1인 경우, reference bit 초기화 후 pointer로 이동</b >
- 먼저 적재된 page가 교체될 가능성이 높음
  - FIFO와 유사
- Reference bit을 사용하여 교체 페이지 결정
  - LRU(or NUR)과 유사     

![img](https://github.com/koni114/Operating-system/blob/master/img/os_110.JPG)

### Second Change Algorithm
- Clock algorithm과 유사
- Update bit(m)도 함께 고려 함
  - 현재 가리키고 있는 page의 (r, m) 확인
  - 다음과 같은 순서로 우선순위 책정
    - (0,0) : 교체 page로 결정
    - (0,1) : -> (0,0)으로 변경, 이 때 write-back(cleaning)을 해야한다는 기록이 필요하므로,   
      list에 추가 후 이동
    - (1,0) : -> (0,0) 후 이동
    - (1,1) : -> (0,1) 후 이동 
- 중요한 것은 reference bit를 update bit보다 먼저 바꿔야 함

![img](https://github.com/koni114/Operating-system/blob/master/img/os_111.JPG)
- clock algorithm에서 update bit가 붙음

### Other Algorithms
- Additional-reference-bits algorithm
  - LRU approximation
  - 여러 개의 reference bit를 가짐
    - 각 time-interval에 대한 참조 여부 기록
    - History register for each page
- MRU(Most Recently Used) algorithm
  - LRU와 정반대 기법 
- MFU(Most Frequently Used) algorithm  
  - LFU와 정반대 기법

## Replacement Strategies - Variable allocation
- variable allocation은 할당되는 page 수가 3개였다가, 4개였다가 유동적임
- WS(Working Set) algorithm
- PFF(Page Fault Frequency) algorithm
- VMIN(Variable MIN) algorithm

### Working Set(ws) 알고리즘
- 1968년 Denning이 제안
- Working set
  - 지금 일할 때 필요한 page 집합 
  - Process가 특정 시점에 자주 참조하는 page들의 집합
  - 최근 일정시간 동안(delta) 참조된 pages 들의 집합
  - 시간에 따라 변함
  - W(t, delta)  
    - The working set of a process at time t
    - Time interval[t-delta, t] 동안 참조된 pages 들의 집합 
    - delta : window size, system paramter 
- window 안에 있는 page 들을 메모리 상에 올리는 것이 working set
- window 안에는 최소 1개, 최대 delta 개의 page를 볼 수 있음  
  최대 delta개인 이유는 우리가 최대 delta+1 시간 동안에만 볼 수 있기 때문
- Working set memory management
  - Locality에 기반을 둠
  - Working set을 메모리에 항상 유지
    - page fault rate(thrashing) 감소
    - 시스템 성능 향상
  - Window size(delta)는 고정
    - Memory allocation은 가변
      - MA가 고정 and delta가 가변 = LRU algorithm이 됨
    - delta 값이 성능을 결정 짓는 중요한 요소     

- window size와 working set size의 관계?
- 초반에는 window size를 조금만 늘려도 확 늘어남. but 계속 증가할수록 증가율은 줄어듬  
  --> locality 때문!   
![img](https://github.com/koni114/Operating-system/blob/master/img/os_113.JPG)

- working set transition 예시
  - loop-1 동안에는 p0, p1을 참조 
  - ㅣoop-2 동안에는 3개, loop-3은 2개!  
![img](https://github.com/koni114/Operating-system/blob/master/img/os_114.JPG)

- loop-1 -> loop-2로 바뀔 때는 일시적으로 working-set이 증가하는 현상을 보임
- 해당 루프에서 전환하는 딱 그 시점에 두 루프의 프로세스 모두가 필요할 것이므로,
![img](https://github.com/koni114/Operating-system/blob/master/img/os_115.JPG)

- working-set은 window size안에 들어오는 Page의 개수가 계속 달라지는 것을 확인!
- page fault는 5번 일어남. 이것이 좋은 성능일까? 알기가 어려움. 주는 자원의 수가 다르기 때문
![img](https://github.com/koni114/Operating-system/blob/master/img/os_116.JPG)

- 성능 평가 
  - Page fault 수 외 다른 지표도 함께 봐야 함
  - example
    - Time interval[1, 10]
      - '#' of page fault = 5
      - 평균 할당 page frame 수 = 3.2
      - page fault와 page frame 수 두 개만 가지고는 비교가 불가능.  
        page fault 처리에 대한 cost value 또는 page 유지 cost 등을 고려해야 함
  - 평가
    - 평균 3.2개의 page frame을 할당 받은 상태에서 5번의 page fault 발생       
- 특성
  - 적재 되는 page가 없더라도, 메모리를 반납하는 page가 있을 수 있음
  - 새로 적재되는 page가 있더라도, 교체 되는 page가 없을 수 있음
- 단점
  - working set management overhead  
    --> 계속 지속으로 관찰하고 있어야 하므로, overhead 발생
  - Residence set(상주 집합)을 page fault가 없더라도, 지속적으로 관리해야 함   
- Mean number of frames allocated vs page fault rate

![img](https://github.com/koni114/Operating-system/blob/master/img/os_119.JPG)
- window size가 커지면, page의 메모리 유지 비용(lifetime)이 커짐
- 반대로 window size가 커지면, page fault rate는 줄어듬
- 즉 window size는 적당히!

## Page Fault Frequency(PFF) algorithm 
- page fault가 나면 관리를 하자! 라는 아이디어
- Residence set size를 page fault rate에 따라 결정
  - Low page fault rate(long inter-fault time)
    - Process 에게 할당된 PF(page frame) 수를 감소
  - High page fault rate(short inter-fault time)
    - process에게 할당된 PF 수를 증가
- Resident set 갱신 및 메모리 할당
  - Page fault가 발생시에만 수행
  - Low overhead      
- Criteria for page fault rate
  - IFT(Inter Fault Time) > tau : Low page fault rate  
    Inter Fault Time이 tau보다 길다는 것은 긴 기간동안 page fault가 별로 일어나지 않음을 의미
  - IFT(Inter Fault Time) > tau : High page fault rate
  - tau : threshold value
    - system parameter  
- algorithm
  - Page fault 발생 시, IFT 계산
    - IFT = tc - tc-1
      - tc-1 : time of previous page fault
      - tc : time of current page fault
    - IFT > tau(Low page fault rate) 
      - Residence set <- (tc-1, tc] 동안 참조 된 pages들 만 유지
      - 나머지 page들은 메모리에서 내림
        - 메모리 할당('#' of page frames) 유지 및 감소  
    - IFT <= tau(High page fault rate) 
      - 기존 pages들 유지 
      - + 현재 참조된 page를 추가 적재
        - 메모리 할당('#' of page frames) 증가
- 성능 평가
  - Page fault 수 외 다른 지표도 함께 봐야 함
  - Example
    - Time interval[1, 10]
      - '#' of page fault = 5
      - 평균 할당 page frame 수 = 3.7
    - 평가
      - 평균 3.7개의 page frame을 할당 받은 상태에서 5번의 page fault 발생
- 특징
  - 메모리 상태 변화가 page fault 발생 시에만 변화
    - low overhead             

### Variable MIN(VMIN) algorithm
- Variable allocation 기반 교체 기법 중 optimal algorithm
  - 평균 메모리 할당량과 page fault 발생 횟수 모두 고려 했을 때의 Optimal
- 실현 불가능한 기법(Unrealizable)
  - Page reference string을 미리 알고 있어야 함
- 기법
  - [t, t + delta]를 고려해서 교체할 page 선택     
- Algorithm
  - Page r이 t시간에 참조 되면, page r이 (t, t + delta]사이에 다시 참조되는지 확인
  - 참조 된다면, page r을 유지
  - 참조 안 된다면, page r을 메모리에서 내림 
      
![img](https://github.com/koni114/Operating-system/blob/master/img/os_118.JPG)
- 성능 평가
  - Page fault 수 외 다른 지표도 함께 봐야 함
  - Example
    - Time interval[1, 10]
      - '#' of page fault = 5
      - 평균 할당 page frame 수 = 1.6
    - 평가   
      - 평균 1.6개의 page frame을 할당 받은 상태에서 5번의 page fault 발생      
- 최적 성능을 위한 delta는?  
  - delta = R / U  
    - U : 한번의 참조 시간 동안 page를 메모리에 유지하는 비용  
    - R : page fault가 발생 시 처리 비용   
  - R > delta * U,(delta가 작으면)     
    - 처리 비용 > page 유지 비용    
  - R < delta * U,(delta 가 크면)  
    - page fault 처리 비용 < 유지 비용

 ## Other Considerations
 - Page size
 - Program restructuring
 - TLB reach

### Page size
- 시스템 특성에 따라 다름
  - No best answer!
  - 점점 커지는 경향
- 일반적인 page size
  - 2^7(128) bytes ~ 2^22 (4M) bytes
- Small page size
  - Large page table / # of PF
    - High overhead(kernel)
  - 내부 단편화 감소
  - I/O 시간 증가
  - Locality 향상
  - Page fault 증가
- Large page size
  - small page table / # of PF
  - 내부 단편화 증가
  - I/O 시간 감소
  - Locality 저하
  - Page fault 감소  

### Program Restructuring
- 가상 메모리 시스템의 특성에 맞도록 프로그램을 재구성
- 사용자가 가상 메모리 관리 기법(예, paging system)에 대해 이해하고 있다면, 프로그램의 구조를 변경하여  
  성능을 높일 수 있음
- Example
  - Paging system, Page size = 1 KB
  - sizeof(int) = 4 bytes
~~~c
// program 1
int main()
{
  int zar[256][256];
  int i, j;

  for(j = 0;  j < 256; j++)
    for(i = 0; i < 256; i++)
      zar[i][j] = 0;
    
  return 0;
}
~~~  

- Row-major order for array
![img](https://github.com/koni114/Operating-system/blob/master/img/os_120.JPG)

![img](https://github.com/koni114/Operating-system/blob/master/img/os_121.JPG)

- 가상 메모리 시스템의 특성에 맞도록 프로그램을 재구성
- 사용자가 가상 메모리 관리 기법(예, paging system)에 대해 이해하고 있다면, 프로그램의 구조를 변경하여 성능을 높일 수 있음

### TLB Reach
- TLB를 통해 접근 할 수 있는 메모리의 양
- TLB의 hit ratio를 높이려면,
  - TLB의 크기 증가
    - expensive 
  - Page 크기 증가 or 다양한 page size 지원
    - OS의 지원이 필요
      - 최근 OS의 발전 방향    
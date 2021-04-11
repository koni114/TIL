# chapter 09 - 가상 메모리
## Virtual Storage(Memory)
- 가상 메모리란, 메모리를 관리하는 방법 중 하나로, 실제 메모리 주소가 아닌 가상의 메모리 주소를 주는 방식을 말함
- Non-continuous allocation
- 사용자 프로그램을 여러 개의 block으로 분할
- 실행 시, 필요한 block들만 메모리에 적재  
  --> 프로그램을 나눠놓고 필요한 부분만 메모리에 적재
  - 나머지 block들은 swap device에 존재
- 기법들
  - paging system
  - Segmentation system
  - Hybrid paging/segmentation system 

## Address Mapping
- Continuous allocation(복습)
  - Relative address(상대 주소)
    - 프로그램의 시작 주소를 0으로 가정한 주소
- Relocation(재배치)
  - 메모리 할당 후, 할당된 주소(allocation address)에 따라 상대 주소들을 조정하는 작업
![img](https://github.com/koni114/Operating-system/blob/master/img/os_87.JPG)

- Non-continous allocation
  - Virtual address(가상주소) = relative address
    - 만약 메모리가 쪼개진다고 가정하에 프로그래밍을 한다면 고려해야 할 것들이 많아짐  
      프로그래밍 개발자들은 고민하지 말고 연속되어 있다고 가정하고 프로그램 작성 
    - Logical address(논리주소) 
    - 연속된 메모리 할당을 가정한 주소. 실제로는 쪼개져서 메모리에 할당됨
  - Real address(실제주소) = absolute(physical)
    - 실제 메모리에 적재된 주소
    - 실제 프로그램이 메모리에 쪼개져서 올라갔을 때 실제 할당된 주소
  - Address mapping
    - 결국 Address mapping은 virtual address에서 real address로 매핑해 주는 행위다! 라고 기억  
    - Virtual address -> real address  
- 아래 그림은 앞서 설명한 address mapping을 그림으로 설명한 것     
![img](https://github.com/koni114/Operating-system/blob/master/img/os_88.JPG)
- 결과적으로 사용자/프로세스는 실행 프로그램 전체가 메모리에 연속적으로 적재되었다고 가정하고 실행할 수 있음

## Block Mapping
- 간단한 address mapping을 살펴보자 --> Block mapping
- 사용자 프로그램은 기본적으로 block단위로 구분이 가능한데, 이런 block에 대한 address mapping은 어떻게 이루어지는지 알아보자  
- 사용자 프로그램을 block 단위로 분할/관리 
  - 각 block에 대한 address mapping 정보 유지
- Virtual address: v = (b,d)
  - b = block number
  - d = displacement(offset) in a block  
    block number와 virtual address와의 차이  
![img](https://github.com/koni114/Operating-system/blob/master/img/os_89.JPG)
- Block map table(BMT)
  - Address mapping 정보 관리
    - kernel 공간에 <b>프로세스마다 하나의 BMT를 가짐</b>
![img](https://github.com/koni114/Operating-system/blob/master/img/os_90.JPG)
- residence bit : 해당 블록이 메모리에 올라가 있느냐? 여부  
  1 --> 메모리에 올라감
- real address : 메모리에 올라 갔다면, 실제 어디에 올라갔느냐? 
- 아래 그림은 실제 어떻게 주소를 찾아가는지에 대한 설명
![img](https://github.com/koni114/Operating-system/blob/master/img/os_91.JPG)
- block number b는 BMT에서 행의 주소를 매핑해서 찾아감
- 올라가 있다면(residence == 1), 어디 올라가 있는지(real address)를 확인
- a + d(offset)의 위치로 실제 원하는 real address를 찾아갈 수 있게 됨

### Block Mapping 순서
- 프로세스의 BMT에 접근
- BMT에서 block b에 대한 항목(entry)를 찾음
- Residence bit 검사
  - Residence bit = 0 경우,  
    swap device에서 해당 블록을 메모리로 가져 옴  
    BTM 엄데이트 후 아래 단계 수행
  - Residence bit = 1 경우,  
    BMT에서 b에 대한 real address 값 a 확인
- 실제 주소 r 계산(r = a + d)
- r을 이용하여 메모리에 접근

## Paging System
- 프로그램을 같은 크기의 블록으로 분할(Pages)
- Terminologies
  - Pages
    - 프로그램의 분할된 block을 page라고 함
  - Page frame  
    - 메모리의 분할 영역(페이지를 넣는 틀)
    - Page와 같은 크기로 분할됨 
![img](https://github.com/koni114/Operating-system/blob/master/img/os_92.JPG)
- swap device에 page 단위로 분할된 program이 존재(오른쪽 그림)
- 이러한 paged와 mapping된 page frame들이 존재
- paging system 특징
  - 논리적 분할이 아님(일정한 크기에 따른 분할) 
    - Page 공유(sharing) 및 보호(protection) 과정이 복잡함  
      Function 단위로 paging이 되는 것이 아니기 때문에 조금 더 과정이 복잡!
      - segmentation 대비
  - Simple and Efficient
    - Segmentation 대비
  - No external fragmentation  
  동일한 크기의 page  
  why? memory와 program이 같은 크기로 할당. 메모리 공간이 충분한데 못 올라가는 경우는 발생하지 않음  
  - Internal fragmentation 발생 가능  
    언제 발생할까? program을 일정한 크기로 자르다가 마지막에 남는 작은 부분은 메모리 할당시 공간이 남게 됨       

## Paging - Address Mapping(연속)
- Virtual address: v = (p, d)
  - p : page number
  - d : displacement(offset)
- Address mapping 
  - PMT(Page Map Table) 사용
- Address mapping mechanism
  - Direct mapping(직접 사상)
  - Associative mapping(연관 사상)
    - TLB(Translation Look-aside Buffer)
  - Hybrid direct/associative mapping       
- Page Map Table
![img](https://github.com/koni114/Operating-system/blob/master/img/os_93.JPG)
- residence bit : 메모리 올라가 있는지 여부
- secondary storage address : page들은 swap device에 저장이 되어 있는데, 그 위치 주소를 말함

### Direct mapping
  - Block mapping 방법과 유사
  - 가정
    - PMT를 커널 안에 저장
    - PMT entry size = entrySize(PMT의 한 행의 size)
    - Page size = pageSize(page의 크기)   
- Direct Mapping 순서 
  - 해당 프로세스의 PMT가 저장되어 있는 주소 b에 접근
  - 해당 PMT에서 page p에 대한 entry 찾음
    - p의 entry 위치 = b + p * entrySize
    - 찾아진 entry의 존재 비트 검사
      - Residence bit = 0인 경우(<b>page fault</b>),  
        running -> asleep(context switching이 발생, overhead가 큼)
        swap device에서 해당 page를 메모리로 적재  
        PMT를 갱신한 후 3-2 단계 수행
      - Residence bit = 1인 경우,
        해당 entry에서 page frame 번호 p'를 확인
  - p'와 가상 주소의 변위 d를 사용하여 실제 주소 r 형성
    - r = p' * pageSize + d
  - 실제 주소 r로 주기억장치에 접근  
  

![img](https://github.com/koni114/Operating-system/blob/master/img/os_94.JPG)
- 문제점
  - 메모리 접근 횟수가 2배
    - 원하는 데이터에 접근하기 위해서 메모리에 2번 접근함  
      PMT가 kernel에 있기 때문 
    - 성능 저하(perfermance degradation)
  - PMT를 위한 메모리 공간 필요
- 해결방안
  - Associative mapping(TLB) 
  - PMT를 위한 전용 기억장치(공간) 사용
  - Hierarchical paging
  - Hashed page table
  - Inverted page table    

### Associative Mapping
- TLB(Translation Look-aside Buffer)에 PMT 적재
  - Associative high-speed memory(전용 HW)
- PMT를 병렬 탐색
- Low overhead, high speed  
- Expensive hardware
  - 큰 PMT를 다루기 어려움 

![img](https://github.com/koni114/Operating-system/blob/master/img/os_96.JPG)

### Hybrid Direct/Associative Mapping
- 두 기법을 혼합하여 사용
  - HW 비용은 줄이고, Associative mapping의 장점 활용
- 작은 크기의 TLB 사용
  - PMT : 메모리(커널 공간)에 저장
  - TLB : PMT중 일부 entry들을 적재. 최근에 사용된 page들에 대한 entry 저장
  - Locality(지역성) 활용
- 프로세스의 PMT가 TLB에 적재되어 있는지 확인
  - TLB에 적재되어 있는 경우
    - residence bit를 검사하고 page frame 번호 확인
  - TLB치에 적재되어 있지 않은 경우,
    - Direct mapping으로 page frame 번호 확인
    - 해당 PMT entry를 TLB에 적재함   

![img](https://github.com/koni114/Operating-system/blob/master/img/os_97.JPG)

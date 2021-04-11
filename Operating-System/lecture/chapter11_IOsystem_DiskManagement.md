# chapter11 입출력 시스템 & 디스크 관리
## Overviews
- I/O Mechanisms
  - How to send data between processor and I/O device
- I/O Services of OS
  - OS Supports for better I/O perfermance
- Disk Scheduling
  - Improve throughput of a disk
- RAID Architecture
  - Improve the perfermance and reliability of disk system

## I/O System(HW)
- I/O system에서 프로세서가 메인 메모리에 데이터를 가져다 두면, 해당 데이터를 I/O device들이 사용하거나 하는 형태로 될 것임
- 결국 필요한 데이터는 메인 메모리에 올라와야 한다는 것을 알 수 있음
- 
![img](https://github.com/koni114/Operating-system/blob/master/img/os_133.JPG)

## I/O Mechanisms
- 입출력 모듈에서 입출력 장치에 데이터를 내보내고, 받아드리는 방식은 크게 2가지 방식이 있음
  - Processor controlled memory access
  - Direct Memory Access 
- Processor controlled memory access
  - Polling(Programmed I/O)
  - Interrupt
![img](https://github.com/koni114/Operating-system/blob/master/img/os_134.JPG)
- Direct Memory Access(DMA)

## Pooling(Programmed I/O)
- Processor가 주기적으로 I/O 장치의 상태 확인
  - 모든 I/O 장치를 순환하면 확인
  - 전송 준비 및 전송 상태 등
- 장점
  - Simple
  - I/O 장치가 빠르고, 데이터 전송이 잦은 경우 효율적  
    ex)예를 들어, 키보드의 입력은 자주 받으므로, pooling하면 효율적일 수 있음
- 단점
  - Processor의 부담이 큼
    - Pooling overhead(I/O device가 느린 경우)      

## Interrupt
- I/O 장치가 작업을 완료한 후, 자신의 상태를 Processor에게 전달
  - Interrupt 발생 시, Processor는 데이터 전송 수행
- 장점
  - Pooling 대비 low overhead
  - 불규칙적인 요청 처리에 적합
- 단점
  - Interrupt handling overhead 
  - 자주 인터럽트가 발생시에는 process가 지속적으로 확인해야 하므로, overhead가 발생

## Direct Memory Access(DMA)
- Processor controlled memory access 방법
  - Processor가 모든 데이터 전송을 처리해야 함
    - High overhead for the processor
- Direct Memory Access
  - I/O 장치와 memory 사이의 데이터 전송을 Processor 개입 없이 수행 
![img](https://github.com/koni114/Operating-system/blob/master/img/os_135.JPG)
- Processor는 데이터 전송의 시작/종료만 관여
![img](https://github.com/koni114/Operating-system/blob/master/img/os_136.JPG)

## I/O Services of OS
![img](https://github.com/koni114/Operating-system/blob/master/img/os_137.JPG)
- I/O Scheduling
  - 입출력 요청에 대한 처리 순서 결정
    - 시스템 전반적 성능 향상
    - Process의 요구에 대한 공평한 처리
  - E.g, Disk I/O Scheduling
- Error handling
  - 입출력 중 발생하는 오류 처리
  - E.g, disk access fail, network communication error 등
- I/O device information managements
- Buffering
  - I/O 장치와 program 사이에 전송되는 데이터를 Buffer에 임시 저장    
  - 전송 속도(or 단위 처리) 차이 문제 해결
  - 예를 들어 우리가 동영상을 볼 때, 로딩이 안되면 버퍼링 걸렸다! 라는 얘기들을 하는데, 다음과 같이 이해할 수도 있음
- Caching  
  - 자주 사용하는 데이터를 미리 복사해 둠
  - Cache hit시 I/O를 생략 할 수 있음
- Spooling
  - 컴퓨터에서 프린터 요청 할 때, 동시에 프린터 명령을 내릴 때, 프린터 입장에서는 기다리게 했다가 프린트 하게 함 
  - 한 I/O 장치에 여러 program이 요청을 보낼 시, 출력이 섞이지 않도록 하는 기법 
    - 각 program에 대응하는 disk file에 기록(spooling)
    - spooling이 완료되면, spool을 한번에 하나씩 I/O 장치로 전송    

## Disk Scheduling
- Disk access 요청들의 처리 순서를 결정
- Disk system의 성능을 향상
- 평가 기준
  - throughput
    - 단위 시간당 처리량 
  - Mean response time
    - 평균 응답 시간  
  - Predictability
    - 응답 시간의 예측성
    - 요청이 무기한 연기되지 않도록 방지 
- Seek time
  - Disk head를 필요한 cylinder로 이동하는 시간
- Rotational delay
  - 필요한 sector가 head 위치로 도착하는 시간
- Data transmission time
  - 해당 sector를 읽어서 전송하는 시간     
- Optimizing seek times
  - FCFS(First come First service)
  - SSTF(Shortest seek time first)
  - Scan
  - C-Scan(Circular Scan)
  - Look  
- Optimizing rotational delay
  - Sector queueing(SLTF, Shortest Latency Time First)
- SPTF(Shortest Positioning Time First)
      
## First Come First Service(FCFS)
- 요청이 도착한 순서에 따라 처리(선착순 방법)
- 장점
  - Simple
    - Low scheduling overhead
  - 공평한 처리 기법(무한 대기 방지)
- 단점
  - 최적 성능 달성에 대한 고려가 없음
- <b>Disk access 부하가 적은 경우에 적합</b>      
- Example  
  - 총 256개의 cylinder로 구성  
  - Head의 시작 위치 : 100번 cylinder  
  - Access request queue(아래의 왼쪽에서 오른쪽 순서로 Job이 들어온다고 생각하자)
![img](https://github.com/koni114/Operating-system/blob/master/img/os_138.JPG)
- 첫번째 순서가 160번 이므로, 처음 100번에 cylinder에 있는 위치를 60만큼 이동해서 160으로 이동
- 그다음 200번으로 이동(40만큼 이동)
- 그다음 90번으로 이동(110만큼 이동)
- 보면 head의 이동거리 굉장히 많음을 알 수 있음(왔다갔다 많이 함)
- total seek distance = 690

## Shortest Seek Time First(SSTF)
- 현재 head 위치에서 가장 가까운 요청 먼저 처리
- 장점
  - Throughput 높음
  - 평균 응답 시간은 짧아짐
- 단점
  - 거리를 최우선으로 하기 때문에 거리가 긴 job은 언제 실행될 지 모름 
  - Predictability 낮음  
  - Starvation 현상 발생 가능  
- <b>일괄처리 시스템에 적합</b>
![img](https://github.com/koni114/Operating-system/blob/master/img/os_139.JPG)
- 90번을 가장 먼저 봄(10만 이동하면 됨)
- 계속적으로 거리가 가까운 녀석들을 차례로 확인
- 위에서 가장 왼쪽에 있는 20은 starvation 현상이 발생. 이를 해결하기 위하여 scan scheduling 수행 

## Scan scheduling
- 현재 head의 진행 방향에서, head와 가장 가까운 요청 먼저 처리
- 마지막 cylinder 도착 후, 반대 방향으로 진행  
  무조건 전체를 한번 훑기 때문에 starvation 현상은 언젠간 처리 됨
- 장점
  - SSTF의 starvation 문제 해결
  - Throughput 및 평균 응답시간 우수 
- 단점
  - 진행 방향 반대쪽 끝의 요청들의 응답시간 증가
![img](https://github.com/koni114/Operating-system/blob/master/img/os_140.JPG)
- 위의 그림은 왼쪽으로 쭉 진행했다가, 오른쪽으로 진행한다는 것을 알 수 있음

## C-Scan scheduling
- SCAN과 유사
- Head가 미리 정해진 방향으로만 이동
  - 마지막 cylinder 도착 후, 시작 cylinder로 이동 후 재시작
- 장점
  - Scan 대비 균등한 기회 제공   
![img](https://github.com/koni114/Operating-system/blob/master/img/os_141.JPG)

## Look Scheduling
- Elevator algorithm
- Scan(C-Scan)에서 현재 진행 방향에 요청이 없으면 방향 전환
  - 마지막 cylinder까지 이동하지 않음
  -  Scan(C-Scan)의 실제 구현 방법
- 장점
  - Scan의 불필요한 head 이동 제거     
![img](https://github.com/koni114/Operating-system/blob/master/img/os_142.JPG)
- 위의 그림에서 보면 제일 마지막 20까지 도달 한 후 왼쪽 끝까지 가는 것이 아니라, 다시 오른쪽으로 진행 방향이 바뀐 것을 알 수 있음
- 조금 더 효율적인 것을 알 수 있음

## rotation delay - Shortest Latency Time First(SLTF)
- Fixed head disk 시스템에 사용
  - 각 track마다 head를 가진 disk. 각 층의 cylinder마다 head를 가지고 있음
    - drum disk
  - Head의 이동이 없음 
- Sector queuing algorithm
  - 각 sector별 queue 유지
  - Head 아래 도착한 sector의 queue에 있는 요청을 먼저 처리 함     
![img](https://github.com/koni114/Operating-system/blob/master/img/os_143.JPG)
- 각 sector마다 queue가 존재. 예를 들어 head가 돌면서 S4가 head에 도착하면, Q4에 있는 Job을 모두 수행 한 후 다음 stage 진행. 이렇게 되면 회전 수가 줄어듬
- Moving head disk의 경우 
  - 같은 cylinder 또는 track에 여러 개의 요청 처리를 위해 사용 가능
  - Head가 특정 cylinder에 도착하면, 고정 후 해당 cylinder의 요청을 모두 처리 

## Shotest Positioning Time First(SPTF)
- Positioning time = Seek time + rotational delay
- Positioning time 이 가장 작은 요청 먼저 처리
- 장점
  - Throughput 높음, 평균 응답 시간 낮음
- 단점
  - 가장 안쪽과 바깥쪽 cylinder의 요청에 대해 starvation 현상 발생 가능   
- Eschenbach(에센바흐) scheduling
  - Positioning time 최적화 시도
  - Disk가 1회전 하는 동안 요청을 처리할 수 있도록 요청을 정렬
    - 한 cylinder 내 track, sector들에 대한 다수의 요청이 있는 경우, 다음 회전에 처리 됨(overhead)


## RAID Architecture
- Redundant Array of Inexpensive Disks(복수 배열 독립 디스크)
- 여러 개의 물리 disk를 하나의 논리 disk로 사용
  - OS Support, RAID controller
- Disk system의 성능 향상을 위해 사용
  - Performance(access speed)
  - Reliability

## RAID 0
- 속도를 빠르게 하기 위하여 초점을 맞춤
- Disk striping
  - 블록 단위로 각각의 disk에 저장 
  - 논리적인 한 block을 일정한 크기로 나누어 각 disk에 나누어 저장
- 모든 disk에 입출력 부하 균등 분배
  - Parallel access
  - Performance 향상
    - 예를 들어 A, B, C, D를 차례로 읽으려고 할 때, RAID 0는 병렬로 처리가 가능하여 4배 빠르게 처리 
- 한 Disk에서 장애 시, 데이터 손실 발생
  - Low reliability   

## RAID 1
- Disk mirroring
  - 동일한 데이터를 mirroring disk에 중복 저장
- 최소 2개의 disk로 구성
  - 입출력은 둘 중 어느 disk에서도 가능
- 한 disk에 장애가 생겨도 데이터 손실 x
  - High reliability
- 가용 disk 용량 = (전체 disk 용량 / 2)     

## RAID 3
- RAID 0 + parity disk(parity 정보가 있으면 데이터 복구가 가능 
  - Byte 단위 분할 저장(RAID 0은 block 단위로 저장)
  - 모든 disk에 입출력 부하 균등 분배
- 한 disk에 장애 발생 시, parity 정보를 이용하여 복구
- Write 시 parity 계산 필요
  - Overhead
  - Write가 몰릴 시, partity에 데이터를 쓰려고 기다려야 하므로, 병목 현상 발생 가능   
- 데이터를 접근하려면 byte 단위로 나뉘어져 있기 때문에 모든 disk에 접근해야 함

## RAID 4
- RAID 3과 유사, 단 Block 단위로 분산 저장
  - 독립된 access 방법
  - Disk간 균등 분배가 안될수도 있음
  - 한 disk에 장애 발생 시, parity 정보를 이용하여 복구 
  - Write시 parity 계산 필요
  - Overhead / Write가 몰릴 시 병목현상 발생 가능
- 병목 현상으로 성능 저하 가능
  - 한 disk에 입출력이 몰릴 때 

## RAID 5
- RAID 4와 유사. 만약에 parity가 고장나면 발생하는 문제점을 해결
- Parity 정보를 각 disk들에 분산 저장
  - Parity disk의 병목현상 문제 해소 
- 현재 가장 널리 사용되는 RAID level 중 하나
  - High performance and reliability  
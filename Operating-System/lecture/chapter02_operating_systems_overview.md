# 운영체제 개요
- 운영체제에 대한 큰 그림을 그리는 chapter

## 운영체제의 역할
- User Interface(편리성)
  - CUI(Character user interface)
  - GUI(Graphical user interface)
  - EUCI(End-user comfortable Interface)  
    --> 특수 목적을 위한 특화 UI. ex) MP3 player
- Resource management(효율성)
  - HW resource
  - SW resource
- Process and Thread management
- System management(시스템 보호)  
  - 사용자가 불법적인 형태로 사용하려고 할 때 보호하고자 하는 역할

## 컴퓨터 시스템의 구성
![img](https://github.com/koni114/Operating-system/blob/master/img/os_1.JPG)

- 운영체제의 핵심은 kernel
- kernel 위에는 system call interface가 있음  
  사용자가 kernel을 직접 접근한다면 HW 운영하는데 문제가 발생할 수 있음  
  따라서 OS에게 필요한 가능을 요청하기 위한 통로
- 또는 kernel 기능 중에 사용자가 control 할 수 있는 기능들을 모아둔 것들을 system call interface라고 할 수 있음

## 운영체제의 구분
- 동시 사용자 수
  - single-user system
    - 한명의 사용자가 자원 독점
    - 자원관리 시스템 복호 방식이 간단함
  - multi-user system
    - 각종 시스템 자원들에 대한 소유 권한 관리 필요
    - 기본적으로 Multi-tasking 기능 필요
    - os 기능이 상대적으로 복잡
  - 대부분의 운영체제는 혼자 씀. ex) windows, pc ..
  - 동시에 사용하는 경우 ex) Linux, windows server..

- 동시 실행 프로세스 수
  - 단일작업(Single-tasking system)
    - 하나를 다 한 후에 종료시키고, 다른 프로그램 실행
    - 운영체제의 구조가 간단
    - ex) MS-DOS
  - 다중작업(Multi-tasking system)
    - 동시에 여러 작업의 수행 가능
    - 운영체제의 기능 및 구조가 복잡

- 작업 수행 방식 
  - 순차 처리( ~ 1940s)
    - 실행하는 작업 별 순차 처리
    - 운영체제가 존재하지 않음
  - Batch Systems
    - 모든 시스템을 중앙에서 관리 및 운영
    - 사용자의 요청 작업을 일정 시간 모아 두었다가 한번에 처리
    - Java -> C로 전환되는 시간을 줄일 수 있음
    - 시스템 지향적
    - 장점 : 많은 사용자가 시스템 자원 공유. 처리 효율(throughput) 향상
    - 단점 : 생산성 저하. 긴 응답시간(turnaround time)
  - Time Sharing Systems(시분할 시스템)
    - 여러 사용자가 자원을 동시에 사용
    - 시간을 쪼개서 각각 프로그램 수행에 사용
    - 요즘 쓰는 system은 대부분 이 방식을 사용
    - 여러 사용자가 자원을 동시에 사용
    - 대화형(conversational, interactive) 시스템
    - 장점 : 응답시간 단축, 생산성 향상(프로세서 유휴 시간 감소)
    - 단점 : 통신 비용 증가(단말기를 통해 접속했기 때문, 통신선 비용, 보안 문제). 개인 사용자 체감 속도 저하(부하)
  - Personal Computing
    - 개인이 시스템 전체 독점
    - CPU 활용률(utilization)이 고려의 대상이 아님
    - OS가 상대적으로 단순함
    - 다양한 사용자들을 위한 기능 지원
    - 단점 : 성능이 낮음
  - Parallel Processing system(병렬 처리 시스템)
    - 단일 시스템 내에서 둘 이상의 프로세서 사용
    - CPU를 제외한 자원들은 공유(Tightly-coupled system)
    - 사용 목적
      - 성능 향상
      - 신뢰성 향상(하나가 고장나도 정상 동작 가능)
    - 프로세서간 관계 및 역할 관리 필요
  - Distributed Processing System(분산처리시스템)
    - 컴퓨터를 여러개 붙여서 사용하자!
    - 네트워크를 기반으로 구축된 병렬처리 시스템(Loosely-coupled-system)
    - Network를 사용해서 여러개의 컴퓨터를 묶은 시스템
    - 물리적인 분산, 통신망 이용한 상호 연결
    - 컴퓨터를 노드라고 하는데, 붙이기가 쉽고, 자기만의 OS를 가지고 있고, 각각의 OS를 잘 관리하게끔 하기 위하여 분산운영체제를 통해 하나의 프로그램, 자원처럼 사용 가능
    - cluster system, client-server system, P2P 등
    - 장점 : 자원 공유를 통한 높은 성능. 고신뢰성, 높은 확장성
    - 단점 : 구축 및 관리가 어려움
  - Real-time systems(실시간 시스템)
    - 위의 system과 다른 관점의 시스템
    - 작업 처리에 제한 시간(deadline)을 갖는 시스템
    - 제한 시간 내에 서비스를 제공하는것이 자원 활용 효율보다 중요
    - 작업(task)의 종류
      - hard real-time task
        - 시간 제약을 지키지 못하는 경우 시스템에 치명적인 영향
        - 예, 발전소 제어, 무기 제어 등
      - Soft real-time task
        - 동영상 재생 등(--> 1초에 몇백장의 사진을 그려내야함) 

## 운영체제의 구조
- 커널(kernel)
  - OS의 핵심 부분(메모리 상주)
  - 가장 빈번하게 사용되는 기능들 담당(ex) 시스템 관리(processor, memory, Etc) 등)
  - 동의어  
    - 핵, 관리자 프로그램, 상주 프로그램, 제어 프로그램 --> 다 커널
- 유틸리티(Utility)
  - 커널을 제외한 나머지 부분
  - 비상주 프로그램
  - UI등 서비스 프로그램'

### 운영체제 구조 : 단일 구조
![img](https://github.com/koni114/Operating-system/blob/master/img/os_2.JPG)

- 커널에 단일로 모아둔 것
- 예를들어 main 안에 모든 것들이 들어가 있는 것
- 장점 : 커널 내 모듈간 직접 통신. 효율적 자원 관리 사용
- 단점 
  - 커널의 거대화
  - 오류 및 버그, 추가 기능 구현 등 유지보수가 어려움
  - 동일 메모리에 모든 기능이 있어, 한 모듈의 문제가 전체 시스템에 영향

### 운영체제 구조 : 계층 구조
- 기능을 계층적으로 묶는 구조
- 현대 운영체제가 가지고 있는 구조
- 장점
  - 모듈화 : 계층간 검증 및 수정 용의
  - 설계 및 구현의 단순화
- 단점
  - 단일구조 대비 성능 저하

### 운영체제 구조 : 마이크로 커널 구조
- 커널의 크기 최소화
- 필수 기능만 포함하고 기타 기능은 사용자 영역에서 수행

## 운영체제의 기능
- 한마디로 표현하자면 <b>관리</b>

### Process 관리
- 프로세스(process)
  - 커널에 등록된 실행 단위(실행 중인 프로그램)
  - 사용자 요청 처리, 프로그램 수행 주체(entity)
- OS의 프로세스 관리 기능
  - 생성/삭제, 상태관리
  - 자원 할당
  - 프로세스 간 통신 및 동기화(synchronization)
  - 교착상태(deadlock) 해결 
- 프로세스 정보 관리

### Proceesor 관리
- 중앙 처리 장치(cpu)
  - 프로그램을 실행하는 핵심 자원
- 프로세스 스케줄링(scheduling)
- 프로세스 할당 관리

### Memory 관리
- 보통 메모리라고 하면 주기억장치라고 함
- 메모리 할당 방법
- Multi-user, Multi-tasking 시스템 등

### File Management
- 파일: 논리적 데이터 저장 단위

### I/O Management
- 입출력(I/O) 과정 : OS를 반드시 거쳐야 함
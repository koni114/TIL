# chapter10 파일 시스템
## Disk System
- file들은 disk에 저장이 됨
- Disk pack
  - 데이터 영구 저장 장치(비휘발성)
  - 구성
    - Sector
      - 데이터 저장/판독의 물리적 단위 
      - sector에 0이냐, 1이냐 등의 데이터를 저장함
    - Track
      - Platter 한 면에서 중심으로 같은 거리에 있는 sector들의 집합 
    - Cylinder
      - 같은 반지름을 갖는 track의 집합 
    - Platter
      - 앞뒤 자성의 물질을 입힌 동그란 CD 같은거  
      - 양면의 자성 물질을 입힌 원형 금속판
      - 데이터의 기록/판독이 가능한 기록 매체 
    - Surface   
      - Platter의 윗면과 아랫면 
## Disk drive
- HDD의 형태 
- Disk pack에 데이터를 기록하거나 판독할 수 있도록 구성된 장치
- 구성
  - Head
    - Arm 끝부분. platter와 접촉하고 있는 부분. 이부분을 통해 판독  
    - 디스크 표면에 데이터를 기록/판독 
  - Arm
    - Head를 고정/지탱
    - 앞면 뒷면에 모두 붙어있음 
  - Positioner
    - Arm을 지탱 -> Arm을 고정하고 있는 기둥
    - head를 원하는 track으로 이동   
  - Spindle  
    - Disk pack을 고정(회전축)
    - 분당 회전 수(RPM, Revolutions Per Minute) 
## Disk Address
  - Physical disk address
    - 우리가 원하는 sector를 읽으려면, 해당 sector로 접근하기 위한 address를 알아야 함 ---> physical address
    - Cylinder Number, Surface Number, Sector Number
    - Sector(물리적 데이터 전송 단위)를 지정
  - Logical disk address: relative address
    - 위의 3개의 number는 os가 관리를 하는데, os는 모든 HDD를 알수가 없음.  
      A사에서 만든 것, B사에서 만든 것.. 등  
      따라서 os는 이것들을 조금 더 추상화된 형태로 생각을 함. 어떻게?  
      --> Disk system의 데이터 전체를 block들의 나열로 취급  
       B0 -> B1 -> B2 -> ... -> Bn-2 -> Bn-1
    - 따라서 os는 해당 데이터를 B1에다가 저장해 줘! 라는 명령을 내리게 되는데, 이 명령이 relative address임
      - Block에 번호 부여 
      - 임의의 block에 접근 가능
    - Block 번호 -> physical address 모듈 필요(disk driver)
    - <b>relative address를 physical address로 매핑하는 주체가 driver!</b>
- Disk Address Mapping
  - Operating-system --> Disk driver --> Disk controller 
  - OS는 block number를 disk driver에게 전달하고, 전달된 주소를 실제 물리 주소로 변환하여 disk controller에게 전달 
  - disk driver는 hw 벤더사 들이 제공함
## Data Access in Disk System
- Seek time
  - 디스크 head를 필요한 cylinder로 이동하는 시간
- Rotational delay
  - 필요한 sector가 head 위치로 도착하는 시간
- Data transmission time
  - 해당 sector를 읽어서 전송(or 기록)하는 시간
- Seek time + Rotational delay + Data transmission time을 Disk data access time이라고 함

## File System
- 사용자들이 사용하는 파일들을 관리하는 운영체제의 한 부분
- File system의 구성
  - Files
    - 연관된 정보의 집합
  - Directory structure
    - 시스템 내 파일들의 정보를 구성 및 제공
  - Partitions
    - 어떤 partition에 파일을 저장함~ 
    - Directory들의 집합을 논리적/물리적으로 구분      

## File Concept
- 보조 기억 장치에 저장된 연관된 정보들의 집합
  - 보조 기억 장치 할당의 최소 단위
  - Sequence of bytes(물리적 정의)
- 내용의 따른 분류
  - Program file
    - Source program, object program, executable files
- 형태에 따른 분류
  - Text(ascii) file
  - Binary file     
- File attributes(속성)
  - Name
  - identifier
  - Type
  - Location
  - Size
  - Protection
    - access control information
  - User identification(owner)
  - Time, date
    - creation, late reference, last modification      
- File operations
  - create
  - Write
  - Read
  - Reposition(옮기는 것)
  - Delete
  - Etc.
- <b>OS는 file operation들에 대한 system call을 제공해야 함</b>
- system call은 os의 기능 중에 사용자가 사용할 수 있는 기능들의 집합

## File Access Methods
- Sequential access(순차 접근)
  - File을 record(or bytes) 단위로 순서대로 접근
    - E.g, fgetc()
  - Directed access(직접 접근)
    - 원하는 BlocK을 직접 접근
      - E.g lseek(), seek()
  - Indexed access
    - Index를 참조하여, 원하는 block을 찾은 후 데이터에 접근  
    - 비유 ex) arr1[index[1]]  

## File System Organization
- Partitions(minidisks, volumes)
  - disk라고 하는 물리적인 개념의 disk를 논리적으로 나누어 놓은 것을 partition이라고 함 --> virtual disk.. 등으로 명명
  - 하나의 디스크를 나누어서 2개의 파티션으로 만들 수 있고, 반대로 두 개의 디스크를 하나의 파티션으로도 사용 가능
  - Virtual disk
- Directory
  - File들을 분류, 보관하기 위한 개념    
  - Operations on directory
    - Search for a file
    - Create a file
    - Delete a file
    - List a directory
    - Rename a file
    - Traverse the file system 
- Mounting
  - 현재 FS에 다른 FS을 붙이는 것
![img](https://github.com/koni114/Operating-system/blob/master/img/os_122.JPG)

## Directory Structure
- Directoery 구조는 다음과 같이 생각해 볼 수 있음
- Logical directory structure
  - Flast(single-level) directory structure
  - 2-level directory structure
  - Hierarchical(tree-structure) directory structure
  - Acyclic graph directory structure
  - General graph directory structure

### Flat Directory Structure
- FS 내에 하나의 directory만 존재
  - Single-level directory structure
- Issues
  - File naming
  - File protection
  - File management
  - 다중 사용자 환경에서 문제가 더욱 커짐   
![img](https://github.com/koni114/Operating-system/blob/master/img/os_123.JPG)

### 2-Level Directory Structure
- 사용자 마다 하나의 directory 배정
- 구조
  - MFD(Master File Directory)
  - UFD(User File Directory)
- Problems
  - Sub-directory 생성 불가능
    - File naming issue
  - 사용자간 파일 공유 불가     
  - 보안에 대한 이슈도 존재. 디렉토리가 하나기 때문에 하나의 파일을 오픈하기 위해 내가 가지고 있는 모든 파일을 오픈 해야 함
![img](https://github.com/koni114/Operating-system/blob/master/img/os_124.JPG)

### Hierarchical Directory Structure
- Tree 형태의 계층적 directory 사용 가능
- 사용자가 하부 directory 생성/관리 가능
  - System call이 제공되어야 함
  - Terminologies
    - 계층적 directory가 등장하자 나온 용어들 
    - Home directory, Current directory
    - Absolute pathname, Relative pathname
  - 대부분의 OS가 사용  
![img](https://github.com/koni114/Operating-system/blob/master/img/os_125.JPG)

### Acyclic Graph Directory Structure
- Hierarchical directory structure 확장
- root Directory를 만들 수 없음
- Directory 안에 shared directory, shared file를 담을 수 있음
- Link의 개념 사용
- ex) window에서 파일 바로가기는 특정 디렉토리의 파일을 가리킴
  - E.g., Unix system의 symbolic link
  - 결과적으로 하위 디렉토리에서 상위 디렉토리로 link를 통해 이동할 수 있다는 개념
  - 하지만 Acyclic 이므로, cycle을 형성할 수는 없음
![img](https://github.com/koni114/Operating-system/blob/master/img/os_126.JPG)
- 위의 그림에서 하위 노드에서 특정 노드로 연결하여 갈 수 있다는 점이 있음
- 중요한 것은 Acyclic Graph이기 때문에 cycle이 생성되지 않음

### General Graph Directory Structure
- Acyclic Graph Directory Structure의 일반화
  - Cycle을 허용
- Problem
  - File 탐색 시, Infinite loop를 고려해야 함    

## File Protection
- File에 대한 부적절한 접근 방지
  - 다중 사용자 시스템에서 더욱 필요
- 접근 제어가 필요한 연산들  
  - Read(R)
  - Write(W)
  - Execute(X)
  - Append(A) 

### File Protection Mechanism
- 파일 보호 기법은 system size 및 응용 분야에 따라 다를 수 있음
- Password 기법
  - 파일을 확인히려면 Password를 입력 받게끔 하는 것 
  - 각 file들에 PW 부여
  - 비현실적
    - 사용자들이 파일 각각에 대한 PW를 기억해야 함
    - 접근 권한 별로 다른 PW를 부여 해야 함
- Access Matrix 기법

### Access Matrix
- 접근 권한을 2차원 table에 저장을 하겠다는 것
- 범위(domain --> userGroup)와 개체(object--> file)사이의 접근 권한을 명시
- Terminologies
  - Object
    - <b>파일</b> 
    - 접근 대상(file, device 등 HW/SW objects)
  - Domain
    - <b>사용자</b> 
    - 접근 권한의 집합
    - 같은 권한을 가지는 그룹(사용자, 프로세스)
  - Access right
    - <object-name, rights-set>      
![img](https://github.com/koni114/Operating-system/blob/master/img/os_127.JPG)
- Implementation
  - Global table
  - Access list
  - Capability list
  - Lock-key mechanism
 
### Global Table
- 시스템 전체 file들에 대한 권한을 table로 유지
- 권한을 부여하지 않는 녀석들까지도 저장해야 함
   - <domain-name, object-name, right-set> 
- 단점
  - Large table size
![img](https://github.com/koni114/Operating-system/blob/master/img/os_128.JPG)

### Access List
- Access matrix의 열(column)을 list로 표현
- Global table과 비교했을 때, 권한을 부여하지 않은(공백) 애들은 저장 안해도 됨
  - 각 object에 대한 접근 권한을 나열
  - Alist(Fk) = {<D1, R1>, <D2, R2>, ..., <Dm, Rm>}
- Object 생성 시, 각 domain에 대한 권한 부여
- Object 접근 시 권한을 검사
- 실제 OS에서 많이 사용됨
  - UNIX의 예 --> rwx , rwx, rwx
- 단점 : 항상 파일에 접근할 때마다 권한을 확인해야 하는 overhead가 발생

### Capability List
- 일종의 신분증
- Access matrix의 행(row)을 list로 표현
  - 각 domain에 대한 접근 권한 나열
  - Clist(D1) = {<F1, R1>, <F2, R2>, ..., <Fp, Rp>}
- Capability를 가짐이 권한을 가짐을 의미
  - 프로세스가 권한을 제시, 시스템이 검증 승인
- 시스템이 capability list 자체를 보호 해야 함
  - kernel안에 저장  

### Lock-key Mechanism
- Access list와 Capability list를 혼합한 개념 
- Object는 Lock을, Domain은 key를 가짐
  - Lock/key : unique bit patterns
- Domain 내 프로세스가 object에 접근 시,  
  - 자시의 key와 object의 lock 짝이 맞아야 함  
- 시스템은 key list를 관리해야 함     

### Comparison of Implementations
- Global table
  - Simple, but can be large
- Access list
  - Object별 권한 관리가 용이함
  - 모든 접근 마다 권한을 검사해야 함
    - Object 많이 접근하는 경우 -> 느림
- Capability lists
  - List내 object들(localized Info.)에 대한 접근에 유리
  - Object별 권한 관리가 어려움  
    만약 특정 object를 모든 domain에 대해서 read 권한을 부여해야 한다면 모든 domain을 전부 다 찾아서 취소 해야 함(overhead 발생)
- 많은 OS가 Access list와 Capability list 개념을 함께 사용
  - Object에 대한 첫 접근 -> access list 탐색 
    - 접근 허용 시, Capability 생성 후 해당 프로세스에게 전달
      - 이후 접근 시에는 권한 검사 불필요
  - 마지막 접근 후 -> Capability 삭제    

## File System Implementation
- Allocation methods
  - File 저장을 위한 디스크 공간 할당 방법
- Free space management
  - 디스크의 빈 공간 관리   

## File System Implementation
- Allocation methods
  - File 저장을 위한 디스크 공간 할당 방법
- Free space management
  - 디스크의 빈 공간 관리 

### Allocation Methods
- Continuous allocation
- Discontinuous allocation
  - Linked allocation
  - Indexed allocation  

### Continuous Allocation
- 한 File을 디스크읜 연속된 block에 저장
- 장점
  - 효율적인 file 접근(순차, 직접 접근)
- 문제점
  - 새로운 file을 위한 공간 확보가 어려움  
    ex) block 8칸 짜리에 10칸 짜리 파일을 넣어야 할 때 넣을 수 없음
  - External fragmentation
  - File 공간 크기 결정이 어려움
    - 만약 처음 넣은 파일에 더 추가적인 data를 append 해야 한다면? 문제가 발생할 수 있음
    - 결과적으로 최종 공간 크기의 결정이 어려움 
    - 파일이 커져야 하는 경우 고려해야 함    

### Linked Allocation
- File이 저장된 block들을 linked list로 연결
  - ex) FileA는 처음에 5번 block에 할당되고, 5번 block은 11을 가리키고 있으므로, 11번 block으로 이동... 
  - 비연속 할당 가능
- Directory는 각 file에 대한 첫 번째 block에 대한 포인터를 가짐
- Simple, No external fragmentation
- 단점
  - 순차 접근에는 큰 문제가 없지만, 직접 접근에 비효율적(direct에는 문제)
  - 포인터 저장을 위한 공간 필요
  - 신뢰성 문제 
    - 사용자가 포인터를 실수로 건드리는 문제 등    
    - 중간에 끊어버리면 해당 데이터는 아예 사용이 불가함

### Linked Allocation: variation -> FAT
- File Allocation Table(FAT)
  - 실제 linked allocation 방식은 사용되고 있음! 
  - 각 block의 시작 부분에 다음 블록의 번호를 기록하는 방법
- MS-DOS, Windows 등에 사용 됨    

![img](https://github.com/koni114/Operating-system/blob/master/img/os_129.JPG)

### Indexed Allocation
- File이 저장된 block의 정보(pointer)를 Index block에 모아 둠
- 직접 접근에 효율적
  - 순차 접근에는 비효율적  
    항상 index block에서 확인해서 다음으로 넘어가야 함
- File당 Index block을 유지
  - Space overhead
  - Index block 크기에 따라 파일의 최대 크기가 제한됨
- Unix 등에 사용됨    

## 디스크 빈 공간 활용 방법(management)
- Bit vector
- Linked list
- Grouping
- Counting

### Bit vector
- 시스템 내 모든 block들에 대한 사용 여부를 1 bit flag로 표시
- Simple and efficient
- Bit vector 전체를 메모리에 보관해야 함
  - 대형 시스템에 부적합. disk가 커질수록 bitmap 자체도 커져야 하기 때문
![img](https://github.com/koni114/Operating-system/blob/master/img/os_130.JPG)


### Linked list
- 빈 block을 linked list로 연결
- link라는 공간도 필요하고, 탐색하려면 link를 따라가야 하므로, 비효율적
![img](https://github.com/koni114/Operating-system/blob/master/img/os_131.JPG)

### Grouping
- n개의 빈 block을 그룹으로 묶고, 그룹 단위로 linked list로 연결
- Linkedlist보다 link를 여러번 타야하는 문제는 해결할 수 있음
- 연속된 빈 block을 쉽게 찾을 수 있음
![img](https://github.com/koni114/Operating-system/blob/master/img/os_132.JPG)


### Counting
- 연속된 빈 block들 중 첫 번째 block의 주소와 연속된 block의 수를 table로 유지
- Continuous allocation 시스템에 유리한 기법
- 데이터가 어떤 형태로 짜여 있는가?에 따라서 적용 여부를 판단해야 함
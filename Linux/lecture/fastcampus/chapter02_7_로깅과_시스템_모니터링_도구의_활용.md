# chapter07 로깅과 시스템 모니터링 도구의 활용
## 로깅 및 시스템 모니터링 도구
- 로그 파일 
  - 시스템 로그 파일
    - `/var/log/*`
  - 시스템 커널 메세지
    - dmesg
  - 응용 소프트웨어 로그 파일
    - `/var/log/[데몬명]/*`
- 로그 관리 유틸리티
  - logrotate
- 스케쥴 작업 관리
  - cron, anacron
- 시스템 모니터링 유틸리티
  - 프로세서(CPU) 사용량
    - top
    - htop
    - mpstat
  - 메모리 사용량
    - vmstat
    - /proc/meminfo
  - 디스크 IO 사용량
    - iostat
  - 종합 리소스 모니터링
    - sar

## 시스템 로그
- 다양한 시스템 로그 살펴보기 - `/var/log/*`
  - bootstrap.log - 부팅 로그 (시스템 부팅 과정에서 발생하는 성공/실패 로그)
  - dpkg.log - 패키지 설치 로그
  - kern.log - 커널 로그
    - 현재 부팅 후 커널 로그는 커맨드라인 `dmesg` 로 확인(시스템 디바이스 메세지 등)
    - syslog - 애플리케이션 로그 (각종 시스템 소프트웨어, 응용 소프트웨어의 로그)
    - Xorg.O.log - X윈도우 각종 로그(윈도우 애플리케이션의 오류 등)

### 시스템 로그 - 응용 소프트웨어 로그
- 다양한 응용 소프트웨어 로그 살펴보기 - `/var/log/(애플리케이션)/*`
- `apt/history.log`
  - 업그레이드 등에 수행된 명령어 로그 기록
- `pat/term.log`
  - 위 수행된 결과의 로그 기록
- `nginx/access.log`
  - 접속 로그, GET / POST, 요청 URL, 응답값(허용 200, 실패 404 등), 등
- `nginx/error.log`
  - 서버 시스템의 (치명적) 오류
- `apache2/access.log`
  - 접속 로그(상동)
- `apache2/error.log`
  - 서버 시스템의 (치명적) 오류

### 로그 유틸리티
- 시스템 로그의 자동 (용량) 관리 -  logrotated
- 시스템 로그 설정파일
  - `/etc/logrotate.conf`
- 애플리케이션별 로그 관리 옵션
  - `/etc/logrotate.d/*`

## 스케줄 프로세스
- 특정 시간마다 특정 프로세스 실행 - cron, anacron
- cron 이란? 
  - cron = Command Run On
  - 특정 시간마다 반복하여 작업을 수행. 특정 월, 요일, 시간 등의 조건 설정
  - 단 해당 일자에 시스템이 꺼져 있으면 동작하지 않음
  - 시작 위치
    - `/etc/crontab`
- anacron 이란 ?
  - 해당 작업이 정해진 시간 내에 실행된 적이 있는지를 확인하여 없다면 적절한 시점에 실행
  - 시작 위치
    - `/etc/anacrontab` 

### 스케줄 프로세스 - 사용자별 cron
- 실행 데몬 --> crond
- 사용자별 직업
  - 스케줄 작업 만들기
    - `crontab -e`
  - 스케줄 작업 확인
    - `crontab -l`
  - 스케줄 작업 삭제
    - `crontab -r`
  - 저장 공간
    - `/var/spool/cron/crontabs/[사용자명]`

## 시스템 모니터링 - 자원(CPU/Mem) 모니터링
- top 을 사용한 CPU, Memory, Process 모니터링
  - `top -d 1` (갱신 주기, 1초(기본값 2초))
- htop 을 사용한 CPU, Memory, Process 모니터링
  - `sudo apt install htop`
  - `htop -d 5`

### 시스템 모니터링 - 프로세서(CPU) 모니터링
- 프로세스 동작방식 및 모드에 따른 측정 시간
- 사용자 모드와 커널 모드
~~~shell
$ time sleep 5
$ time sudo hdparm -T /dev/sda
~~~
- mpstat 을 사용한 CPU 사용량 조회
  - mpstat [주기][횟수]
  - mpstat 1 (1초 갱신)
  - mpstat 1 10 (1초 갱신, 10회 후 통계)
  - mpstat -P ALL (CPU를 core 별로 표시)
- %usr: 사용자 레벨의 CPU 사용량
- %nice: nice 우선순위가 적용된 CPU 사용량
- %sys: 시스템 레벨(커널)의 CPU 사용량
- %iowait: I/O 처리를 위해 기다리는 CPU 시간
- %irq: H/W 시스템 인터럽트 처리를 위해 사용된 CPU 시간
- %soft: S/W 인터럽트 처리를 위해 사용된 CPU 시간
- %steal: 하이퍼바이저에 의해 대기한 CPU 시간
- %guest: (호스트에서) VM 가상머신에 제공해준 CPU 시간
- %gnice: (호스트에서) nice 가 적용된 guest CPU 시간
- %idle: 대기한(유휴한) CPU 시간 

### 시스템 모니터링 - 메모리 모니터링
- free, /proc/meminfo 를 사용한 메모리 사용량 조회
- 각 유형별 메모리 사용량
  - `free`
  - `cat /proc/meminfo`

### 시스템 모니터링 - 메모리 및 시스템 부하 모니터링
- vmstat 를 사용한 메모리 사용량 조회
- 메모리 + 시스템 통계
  - `vmstat [주기]`
  - `vmstat (1초 단위 갱신)`
- procs
  - r : 현재 동작을 대기하는 프로세스의 수 (waiting to run) 
  - b : sleep상태에있는프로세스수
- memory
  - swpd : 스왑메모리크기
  - free : 작여 메모리 크기 (idle memory, 유휴 메모리)
  - buff : 버퍼 영역으로 사용된 메모리 크기
  - cache : 캐시 영역으로 사용된 메모리 크기
- swap 
  - si/so : 초당 swap in / out한 데이터양 (물리적 메모리가 적을 때 발생)
- io
  - bi / bo : 초당 블럭디바이스로부터 받은 데이터 in/out 양
- system
  - in : 초당 인터럽트 발생 수 (clock 인터럽트 포함)
  - cs : 초당 발생한 컨텍스트 스위칭 수
- cpu
  - us / sy / id / wa / st : CPU % 사용량 (user, system, idle, wait(IO), stolen(VM))

### 시스템 모니터링 - 디스크 IO 모니터링
- iostat 을 사용한 디스크 IO 사용량 조회
- 디바이스 입출력
  - iostat [주기] [디바이스]
  - iostat 1 sda (1초 갱신, sda 디스크)

### 시스템 모니터링 - 종합 모니터링 도구
- sar 를 이용한 프로세스, 메모리 모니터링 : sar = System Activity Report
- 프로세스 모니터링
  - sar [주기] [횟수]
  - sar 1 5
  - sar -P [프로세스] [주기]
  - sar -P ALL 1
- 메모리 모니터링
  - sar -r [주기]
  - sar -r 1
- sudo apt install sysstat (기본 설치)
  - sar
  - mpstat
  - vmstat
  - iostat

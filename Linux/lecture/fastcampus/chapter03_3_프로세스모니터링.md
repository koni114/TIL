# chapter03_3 프로세스 모니터링
## 프로세스 모니터링 도구와 프로세스 분석
- 프로세스 실행하기
  - `bg`
  - `fg`
  - `jobs`
  - `screen`
- 프로세스 확인하기
  - `ps`
    - `/proc/<pid>/`
    - `pstree`
- 프로세스 종료하기
  - `killcd`
  - `killall`
- 프로세스 디버깅
  - 파일/디렉토리 사용 프로세스
    - `lsof`
      - `fuser`
   - 시스템콜 트레이싱
    - `strace`
   - 라이브러리 트레이싱
    - `ltrace`

 ## 프로세스 (백그라운드) 실행하기
- fg(foreground), bg(background), jobs
- 백그라운드로 실행하기
  - 실행 시 결정
    - `tail -f /var/log/syslog` 
      - 앞에서 실행, Foreground
    - `tail -f /var/log/syslog &`
      - 뒤에서 실행, Background
      - 백그라운드를 실행시켜 두면, 실시간으로 떨어지는 log를 확인하면서 cmd를 사용할 수 있음
  - 실행 후 결정
    - `tail -f /var/log/message` : 실행
    - `tail -f /var/log/message <ctrl + z>` : 실행 중, 중단(ctrl + z)
      - `jobs`
        - 중단/백그라운드 실행 중인 프로세스 확인
    - `bg %1`
        - 중단된 프로세스 백그라운드에서 실행
  - 관리 및 foreground 전환
    - `jobs`
    - `fg %1` : 첫 번째 background process를 다시 foreground 로 전환
  - <ctrl + c> 로 종료 - 또는 `kill %1` 으로 강제 종료
~~~shell
 # apache2 의 access.log 에 접속 기록을 확인하기 위해서 2초마다 접근해보기
$ systemctl start apache2
$ while true; do curl localhost > /dev/null; sleep 2; done;
~~~
~~~shell
# apache2 서버가 실행되고 있다고 가정
$ tail -f /var/log/apache2/access.log  # foreground 로 실행 ctrl + z 로 종료할 수 있음
$ bg                                   # background 로 실행
$ jobs                                 # background 확인

# 2개의 background process 를 실행
$ tail -f /var/log/apache2/access.log &
$ tail -f /var/log/syslog &

$ jobs    # 2개의 bg process 확인
$ kill %1 # 첫 번째 background process kill
$ kill %2 # 두 번째 background process kill
~~~

## ps - 프로세스 관리를 위한 all-in-one
### ps 예제
- STATUS(STAT)은 프로세스의 상태를 나타냄. 대부분의 상태는 S 상태로, 이벤트를 기다리고 있는 상태임
~~~shell
$ ps a  # pid, TTY, STATUS(STAT), TIME, COMMAND 확인
~~~
- Ss 는 해당 프로세스의 session leader 를 말하며, 이에 하위 process 를 다음 명령어를 통해 확인 가능.
~~~shell
# user, ppid, pid, pgid, sid, comm, stat 확인
$ ps fo user,ppid,pid,pgid,sid,comm,stat  # 내가 원하는 상태값만 확인 가능
~~~
- `a` 옵션은 모든 사용자 프로세스 보여준다는 의미
- `u` 옵션은 프로세스의 사용자와 소유자를 보여줌
- `x` 옵션은 터미널에 연결되지 않은 백그라운드에서 실행되는 프로세스까지 보여주는 명령어
- kernel task 는 중괄호(`[]`) 로 보여줌
~~~shell
$ ps aux
$ ps aux | egrep "docker"
$ ps aux | egrep "apache2"
~~~

### 프로세스 상태 코드
- `D`: Uninterruptible sleep (usually IO) - IO 대기상태
- `R`: Running - 실행 중 상태
- `S`: Interruptible Sleep(waiting for an event to complete) - 깨울 수 있는 대기 상태
- `T`: Stopped, either by a job control signal or because it is being traced - 중지된 상태(작업 제어 신호나 트레이싱 시그널로 인함)
- `Z`: Defunct("zombie") process, terminated but not reaped by its parent - 좀비 프로세스 상태. 종료 되었으나 부모 프로세스에 의해 처리되지 않음

### ps option
- `<` : high priority
- `N` : log priority
- `L` : pages locked into memory
- `s` : session leader(**)
- `l` : multi-threaded
- `+` : foreground process group(**)

### ps 주요 옵션 조합
- `ps` - 프로세스 디버깅을 위한 주요 명령어
- 모든 프로세스 살펴보기
  - `ps ax`
  - `ps axu`
- 프로세스 트리를 살펴보기
  - `ps -ejH`
  - `ps axjf`
- root 권한으로 실행중인 모든 프로세스 확인(-U: real UID, -u: effective UID)
  - `ps -U root -u root u`
  - 일반적으로는 UID와 EUID가 같으나, setuid bit이 설정되어 있는 경우 한시적으로 root 권한을 가져올 수 있음
- 내 권한으로 실행중인 모든 프로세스 확인
  - `ps -xu`
- 내가 원하는 필드만 출력
  - `ps -eo pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,wchat:14,comm`
  - `ps axo stat,euid,ruid,tty,tpgid,sess,pgrp,ppid,pid,pcpu,comm`
  - `ps -eo pid,tt,user,fname,tmout,f,wchan`
  - `ps -aN --format cmd,pid,user,ppid`
- 내가 원하는 프로세스만 확인 하는 방법
~~~shell
$ ps -ef > tmpfile.txt; egrep 'UID|systemd' tmpfile.txt; rm tmpfile.txt
~~~

## 프로세스 확인 - /proc 파일 시스템
- proc 파일 시스템은 실제로 존재하지 않은 일종의 환영과도 같음
- 해당 파일 시스템은 커널이 메모리 상에 만들어 놓은 것으로, 디스크에는 존재하지 않음
- proc 은 많은 정보를 제공해 주는데, 주로 프로세스에 대한 정보를 제공했기 때문에 proc(process) 이란 이름을 갖게 됨

~~~shell
$ cd /proc/self # bash shell 안으로 들어오게됨

# bash shell 과 process 확인
$ cd fd
$ ls -al

$ systemctl status sshd  
$ pidof sshd              # sshd 가 돌고 있는 process id 를 가져올 수 있음
$ cd /proc/131019         # pid directory 안으로 이동
$ sudo ls -al fd          # 프로세스가 사용중인 File Descriptor 링크와 정보 저장

# 해당 프로세스의 메모리 사용 정보
$ cat statm
~~~

### /proc 하위 디렉토리 정보
- `/proc/<pid>/` - man 5 proc
- `/proc/self` - 현재 실행중인 프로세스의 정보
  - `eg, ls -l /proc/self` : ls 프로세스 그 자체
  - `cd /proc/self` : bash 쉘 프로세스
    - `cat cmdline` : bash 프로세스의 실행 옵션(bash)
- `/proc/<pid>/`
  - `maps`: 프로세스의 메모리 mapping 공간
  - `cmdline`: 프로세스 실행 인자 
  - `cwd` : 프로세스가 사용중인 디렉토리나 파일
  - `environ` : 프로세스의 환경 변수
  - `exe` : 실행중인 프로그램의 이름
  - `fd` : 프로세스가 사용중인 파일 디스크립터
  - `dfinfo` : 파일 디스크립터 정보
  - `net` : 프로세스가 바라보는 네트워크 정보
  - `stat` : 프로세스에 대한 정보 기록(pid, name, status, ppid 등)
  - `statm` : 메모리 사용 정보(size, resident, share, text, lib, data, dt)
  - `status`: 프로세스 상태 정보
- nginx 웹서버 디버깅 - pid of nginx, cd /proc/<pid>
  - `cat cmdline`
    - 내용 확인 및 `systemctl` 의 데몬 실행 명령어와 비교
  - `sudo ls -al fd`
    - 열고 있는 파일 디스크립터 확인
  - `cat statm`
    - 메모리 사용 정보 요약
  - `cat status`
    - 프로세스의 상태 확인

### 프로세스 트리
- pstree 유틸리티
- `pstree -u user1`
  - 나의 권한으로  실행중인 프로세스
  - ps xf 와 동일한 결과

### 프로세스 종료 - 특정 시그널 보내기
~~~shell
$ pidof apache2  # 10039, 10038, 10037
$ kill 10039     # 부모 프로세스를 죽이면 하위 프로세스까지 다 종료됨

$ systemctl restart apache2
$ pidof apache2   
$ killall apache2

$ systemctl restart apache2
$ pidof apache2
$ killall -i -v nginx 
~~~
- kill 명령어를 통한 프로세스 강제 종료 및 신호 보내기
- 모든 시그널은 프로세스 구현자(개발자) 에게 그 개발여부가 달려있음
  - SIGHUP - 종료(Hang-Up)이지만, 주로 이를 통해 설정파일을 다시 불러오게도 쓰임
  - SIGQUIT - 정상적인 종료 후 코어 덤프 생성
  - SIGTERM - 정상적인 종료
  - SIGINT - 강제 종료(ctrl + c)
- 구현자가 특별히 핸들링 할 수 없는 명령어
  - SIGKILL - 강제 종료
- 사용법
  - `kill -HUP <pid>`
    - `kill -INT <pid>`
    - `kill -KILL <pid>`
    - `kill -1 <pid>`
    - `kill -2 <pid>`
    - `kill -9 <pid>`
- `killall` 명령어를 통한 프로세스 종료(SIGTERM) 및 시그널 보내기
- 사용법
  - `killall <프로세스명>`
    - `killall -s <신호> <프로세스명>`
    - `killall -u <사용자> <프로세스명>`
- 실제 사용 예
  - `sudo killall nginx`
    - `killall -i -v bash`
      - `-i : interactive (종료시 확인)`
      - `-v : verbose (실행 결과를 보여줌)`

 ### 프로세스 디버깅 - lsof(list open files)
 ~~~shell
 $ lsof /var/lib/apt/lists/lock
 $ lsof /var/log/syslog 

 $ lsof /var/log/apache2/access.log
 ~~~
- lsof - 파일을 사용중인 프로세스 조회
- lsof /path/to/binary
   - 특정 프로세스가 사용중인 파일시스템 확인 
- lsof -i
   - 네트워크를 이용중인 프로세스 조회
- lsof -u <username>
   - 특정 사용자가 실행한 프로세스가 사용 중인 파일

### 프로세스 디버깅 - fuser
 ~~~shell
 $ fuser /var/log/syslog
 $ fuser /var/log/*
 ~~~
- fuser - 파일/디렉토리를 사용중인 프로세스/사용자 조회
- 사용법
  - `fuser /path/to/file`
- 실 사용 예시
  - `sudo fuser /var/log/nginx/*` : nginx 아래 로그 파일을 사용중인 프로세스 목록
  - `sudo fuser /var/log/*` : 로그파일을 사용중인 프로세스 목록

### 프로세스 디버깅 - strace
- strace - 시스템 콜 트레이싱
  - `strace <cmd>`
  - `strace -t <cmd>` : 출력 결과에 timestamp 표시
  - `strace -tt <cmd>` : 출력 결과에 timestamp.msec 표시
  - `strace -f <cmd>` : fork 프로세스까지 출력

### 프로세스 디버깅 - ltrace
- ltrace - 라이브러리 콜 트레이싱
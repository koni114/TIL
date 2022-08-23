# chapter02_4 응용 프로그램 다루기 - 패키지 설치, 업데이트 및 업그레이드
- 패키지 관리자를 통해 패키지를 설치, 보안 업그레이드 등을 수행하는 방법에 대해서 알아보자

## 패키지란
- 리눅스의 다양한 운영체제에서는, 내가 원하는 프로그램을 실행하기 위해서는 해당 소스코드를 해당 환경에서 컴파일 하여야 함
- 이유는 리눅스는 너무나도 다양한 운영체제 버전과 다른 커널과 다른 라이브러리가 존재하기 때문
- 개발자가 아닌 사람이 소스코드를 컴파일하고, 이 때 발생하는 다양한 이슈(버전 이슈, 라이브러리 및 의존성 라이브러리 이슈)를 해결하기가 어려움
- 따라서 <b>해당 배포판 환경에 맞추어 미리 빌드한 실행파일을 압축한 패키지를 설치함</b>
- windows 에서는 `msi` 또는 `exe` 로 실행하며, 데비안 리눅스는 `.deb`, 레드헷 리눅스는 `.rpm` 으로 패키지가 묶여있음

## 패키지 관리자 - apt(Advanced Package Tool)
- 과거에는 `apt-get` 명령어를 통해서 패키지를 설치했지만, 최근에는 `apt` 명령어를 통해 대부분 수행하며, 권장하고 있음

![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_13.png)

- 우리는 `apt`, `synaptic`(GUI 방식의 패키지 설치 관리자), `aptitude`(terminal에서 ascii 버전의 GUI 방식의 패키지 설치 관리자) 로 설치하지만, 실제 back-end는 apt-get을 통해 실행됨
- 일반적으로 패키지는 우분투를 개발한 캐노니컬이 만든 public-repo 에서 설치되며, 여기에 포함되어 있지 않은 다른 패키지들은 개별 private-repo에서 패키지를 설치함

### apt 기본 명령어
- `apt update`: 리포지토리 내용 가져오기(헷갈리지 말아야 할 것은 저장소 패키지 명령어를 업데이트 해줌!)
- `apt list` : 리포지토리 패키지 목록 출력(로컬 캐쉬)
- `apt list --installed` : 설치된 패키지 목록 출력
- `apt list --upgradeable` : 업그레이드(업데이트) 가능한 목록 출력
- `apt search` : 리포지토리 검색(로컬 캐쉬)
- `apt show`: 패키지 정보 표시
- `apt install`: 리포지토리 내의 패키지 설치
- `apt remove`: 설치된 패키지 삭제(설정은 유지!). 과거에는 특정 패키지를 삭제하는 경우, 영향을 미쳐 다른 프로그램이 실행되지 않는 경우가 발생해 설정은 유지해야하는 케이스가 있기 때문
- `apt purge`: 설치된 패키지 삭제 + 설정파일 삭제
- `apt autoremove`: 더 이상 사용되지 않는 패키지 삭제(업그레이드 이후 dependency 또한 업그레이드되어 더 이상 참조되지 않은 패키지)
- `apt upgrade`: 패키지 업그레이드(보통 우리가 생각하는 특정 패키지 업데이트 하는 경우 사용)
- `apt full-upgrade`: 패키지 업그레이드 과정에서 삭제가 필요하다면 그 또한 수행하며 업그레이드(업데이트) - 잘 사용되지 않음

### 패키지 유틸리티 - GUI 활용하기(참조용)
#### 우분투 소프트웨어 리포지토리 유형
- main: 공식(Official) 지원, 오픈소스 소프트웨어
- universe: 커뮤니티 지원, 오픈소스 소프트웨어
- restricted: 공식(Official) 지원, 캐노니컬 사가 아닌 벤더사에서 지원하는 비-오픈소스 소프트웨어(디바이스 드라이버 등)
- multiverse: 미지원, 비-오픈소스 소프트웨어, 상용 소프트웨어(영상/사진, 음악/DVD 플레이어 등)

#### 업데이트 데몬
- (각종 유형의 업데이트를) 주기적으로 체크하는 데몬들
  - update-manager 데몬(설정/ etc/update-manager/release-upgrades) 
    - aptd 데몬
  - update-notifier 데몬
  - unattended-upgrade  

### 패키지 유틸리티 - CLI를 활용하여 리포지토리 살펴보기
- `/etc/apt/*` 아래에 있는 각종 설정들..

![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_14.png)

- `/etc/apt/sources.list` : 패키지를 가져오기 위한 목록
- `/etc/apt/sources.list.d` : 추가적인 소스 리스트
- `/etc/apt/apt.conf` : APT 설정 파일(메뉴얼)
- `/etc/apt/apt.conf.d` : 추가적인 APT 설정 파일(각종 데몬들이 추가/관리)
- `/var/cache/apt/archives` : 패키지 파일을 가져온 저장소
- `/var/lib/apt/lists`: 상태 저장소

#### 리포지토리 목록 가져오기
- `sudo apt update`: apt update
- 업데이트  된 목록에서 패키지 업그레이드
  - `apt list --upgradable` : 업그레이드 가능한 패키지 확인
  - `apt upgrade <pkgname>` : 해당 패키지만 업그레이드
  - `apt upgrade`: 모든 패키지 업그레이드 
- `sudo apt upgrade`: 일괄적인 업그레이드
- `sudo apt autoremove` : 더이상 사용되지 않는 구버전 삭제

#### 개인 리포지토리 추가
- 인터넷 상에 있는 모든 소프트웨어 패키지들이 완벽하게 내 환경에 맞지 않을 수 있음
- 내가 만든 소프트웨어를 다른 누군가가 원할 수도 있고, 이를 위해 내 레포를 다른 사람들에게 공유해주는 경우가 있음
- 이러한 개인 레포지토리를 PPA(Personal Package Archives) 라고 부름  
  개인 사용자들이 만드는 리포지토리는 https://launchpad.net/ 에 있음
- `sudo add-apt-repository ppa:<PPA_REPO_NAME/PPA>` : 개인 리포지토리 추가
- `sudo add-apt-repository --remove ppa:<PPA_REPO_NAME/PPA>` : 개인 리포지토리 삭제 
- (개인 리포지토리에서) 설치된 패키지와 리포지토리를 모두 삭제
  - `sudo apt install ppa-purge`
  - `ppa-purge ppa:<PPA_REPO_NAME/PPA>`

### 패키지 업데이트 - VM에서 자주 겪게되는 이슈
- 업데이트/설치 커맨드 실행 실패
- 왜 발생할까? 보통 VM은 대부분 꺼둔 상태이며, VM을 켰을 때 자동으로 관련 패키지들이 업그레이드 됨.  
  이는 백그라운드에서 프로세스가 수행되며, 정작 내가 원하는 apt package 작업이 되지 않을 수 있음
- 해결방법 : 프로세스 확인
  - 기다리기(해당 백그라운드 프로세스가 끝날때까지 기다리기(권장) - 오래걸림) 
  - 강제 종료하기(kill)
  - lock이 걸려있는 것이 어떤 것이 있는지 확인 필요
- 패키지는 가능한 한 최신 버전으로 유지하는 것이 좋음
  - 리포지토리 최신 유지
  - 보안패티 등의 업데이트 최신 유지(취약점 등)
  - 각종 일반 패키지 최신 버전으로 유지(버그 등)
- 패키지 보안 업데이트
  - 보통 주기적으로 `unattended` 명령어를 통해 업데이트 되기 때문에 크게 신경쓰지는 않아도 됨
  - `unattended-upgrade --dry-run`: 적용하지 않고, 적용 될 것을 미리 확인
  - `unattended-upgrade`

### 패키지 업데이트 - dpkg(Debian package manager)
- 패키지 파일의 설치, <b>확장자 .deb 또는 .dpkg</b>
- dpkg를 이용한 유틸리티 다운로드, 설치, 삭제
  - `dpkg -i <pkg>` : 설치(Install)
  - `dpkg -r <pkg>` : 삭제(remove)
  - `dpkg -P <pkg>` : 설정파일포함 삭제(purge)
  - `dpkg -l` : 설치된 패키지 목록 출력(list)
  - `dpkg -s <pkg>` : 설치할 패키지 검색(리포지토리로부터 search)
  - `dpkg -S <pkg>` : 설치할 패키지의 설치 위치
  - `dpkg -l <local_pkg>` : 설치할 패키지의 정보 보기(information)
  - `dpkg -c <local_pkg>` : 설치할 파일의 내용물 미리 살펴보기(Contents)
  - `dpkg -x <pkg><location>`: 패키지 파일의 압축 풀기(extract)
  - `dpkg -X <pkg><location>`: 패키지 파일의 압축 내용을 보여주며 풀기(extract)

#### dpkg 를 활용한 다운로드 패키지 설치(ex) google-chrome)
- 구글 크롬 메뉴얼로 설치하기
  - https://google.com/intl/ko_ALL/chrome
  - 운영체제 및 버전 자동 탐지 -> 다운로드
  - 만약 버전이 안 맞으면? 
    - 맨 밑의 Chrome 제품군, 기타 플랫폼 -> 다운로드..
  - `sudo dpkg -i google-chrome-stable_current_amd64.deb`

### 운영체제 시스템 업그레이드 - 다음 LTE 버전으로(16.04 -> 18.04)
- `do-release-upgrade`
 - 현재 배포판 최신 업데이트  
 - 한번에 한 버전의 업그레이드만 지원

## 데몬 서비스 관리하기
- 서비스 관리하기(service, systemctl)
- 서비스 로그 살펴보기(journalctl)
- 나만의 서비스 만들기

### 데몬이란(daemon)
- 사용자가 직접적으로 제어하지 않고, 백그라운드에서 돌면서 여러 작업을 하는 프로그램
- 서비스란(service)
  - 주로 서버/클라이언트 모델에서 출발하여, 사용자의 요청에 응답하는 프로그램(주로 데몬 형태로 구동됨) 
- 다음의 관계를 기억하자
  - 일반적으로 service 는 백그라운드에서 수행되는 데몬일 경우가 많지만 반드시 그런 것은 아님
  - service 와 daemon 은 모두 process
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_15.png)

- 사용예
  - 웹서버나 파일서버는 데몬 형태로 구동되는 서비스 프로그램
  - 웹서버: httpd
  - 파일서버: ftpd
  - 웹프록시: squid
  - 시큐어쉘(원격터미널) - sshd
  - 시스템로깅 - syslogd, rsyslogd
  - 프린터데몬 - cupsd, lpd
  - 네트워크 서비스 - inetd, xinetd 
- 윈도우 같은 경우는 데몬이라는 용어보다는 서비스라는 용어로 사용되고 있음

### 우분투의 데몬
- SystemV 명령어(`service` 를 통한 확인)
- 사실상 우분투 16/18 에서는(기본적으로는) SysV 의 service 를 사용하지 않음
- `service --status-all`, `service <daemon-name> status` 등을 통해 데몬을 확인할 수 있지만, 내부적으로는 모두 `systemctl`로 호출됨
  - `service --status-all`
  - `service <daemon-name> status`
  - `service <daemon-name> start`
  - `service <daemon-name> stop`
  - `service <daemon-name> restart` 
- <b>따라서 앞으로는 `systemctl` 명령어를 반드시 사용할 줄 알아야 함</b>
- systemd 를 사용하는 우분투의 systemctl 을 통한 서비스 확인
  - `systemctl status`
  - `systemctl status|start|stop|restart <daemon-name>`  
    정확히는 `daemon-name.service` 이지만 `.service`는 생략 가능
- sevice 명령어 사용법과는 다르게 systemctl 는 상태가 앞에 오고 service 명이 뒤에 옴

### Systemd 를 통한 서비스 관리
- 데몬 프로세스를 모두 관리하는 프로세스는 우분투 16, 18 같은 경우 모두 `systemd` 라는 데몬이 관리하게 됨
- systemd 는 `/sbin/init` 이라는 프로세스 이름으로 보이기는 하지만, 실제로는 `/lib/system/systemd` 를 호출하게 되어 있음
  - `/sbin/init -> /lib/system/systemd`
- systemd 의 사용 이유
  - 프로세스를 자동으로 병렬로 시작시키면서 의존성 관리를 해줌
  - 프로세스의 갑작스런 종료에 대응(자동으로 재시작해줌)
  - 부팅 옵션(런레벨)에 따른 다른 프로세스 구동
- systemd 를 관리하기 위해 `systemctl` 라는 명령어가 있으며, process 를 모니터링 하고 관리하기 위한 `journalctl` 명령어가 있음

![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_16.png)

### Systemd 디렉토리 구조
- 시스템 서비스 디렉토리
  - `/lib/systemd/system` 
  - 해당 디렉토리에 다양한 서비스 목록과 실행규칙들에 대한 설정 파일들이 들어가 있음
- run-level에 따른 타겟 서비스 목록
  - `/lib/systemd/system/default.target`
  - `/lib/systemd/system/runlevel?.target` 
- 실제 데몬의 구현체는 `/lib/systemd/system` 에 존재하며, 구동시에 링크가 자동으로 생성되면서 `/etc/systemd/system/*.service` 가 생기면서 부팅과정에서 호출됨

### Systemd 유닛 종류
- 목적에 따라 (service를 실행할 것이냐, socket?, mount를 할 것이냐? 등) 다음과 같이 유닛의 종류가 다양함
  - `lib/systemd/system/*.service`
  - `lib/systemd/system/*.socket` 
  - `lib/systemd/system/*.mount` 
  - 모두 다 알필요는 없으므로, service 와 target 만 알아보자


### systemctl 명령어
- Systemctl 을 통한 다양한 데몬/서비스 확인
- `systemctl list-units` : 실행 중인 서비스 목록 확인
  - `systemctl list-units --type=service`
  - `systemctl list-units --type=service --state=running` (state: failed, active, running) 
  - `systemctl list-units --type=target`: 부팅시 선택 가능한 타겟 옵션 확인
  - 여기서 target 은 그룹을 말하며, 하나 이상의 서비스를 묶어 target 이라고 부름
- `systemctl get-default` : 부팅시 기본 옵션
- `systemctl set-default` : 부팅시 기본 옵션 변경(runlevel 변경)
  - `systemctl set-default <target>`
  - `sudo systemctl set-default multi-user.target` : 부팅 시 GUI 로 로그인하지 않고 CLI로 사용 
- Systemctl 을 통한 다양한 데몬/서비스 확인
  - `systemctl status|start|stop|restart|reload|enable|disable|mask|unmask <servicename>.service`
    - reload: 서비스를 restart 시키지 않고, 설정파일만 리로드 하는 명령어임
    - enable: 부팅시 서비스 자동 시작
    - disable: 부팅시 서비스 자동 시작 삭제
    - mask: 서비스 숨기기(시작불가)
    - unmask: 서비스 숨기기 제거  

### 서비스 데몬의 로그 확인
- journalctl 을 통한 다양한 데몬/서비스 로그 확인
- 서비스 로그 확인
  - `journalctl` (전체 로그)
  - `journalctl -b` (부팅 후 로그)
  - `journalctl -f` (최근로그 및 이후 로그 트래킹 대기)
- 특정 서비스의 로그 확인
  - `journalctl -p crit` (크리티컬 속성의 로그 확인)   
- 특정 날짜로 조회하기
  - `journalctl -u <service-name> --since=2020-06-01 --until=today`  
- 로그의 크기 확인
  - `journalctl --disk=usage`
- 로그 디렉토리 위치
  - `/var/log/journal` 

### 나만의 서비스 만들기
- 원하는 프로세스 서비스로 등록
  - 기존 서비스 명령어의 설정파일 살펴보기
   - `systemctl cat <service-name>.service`
   - 예) `systemctl cat sshd.service`, `systemctl cat cups.service`
  - 서비스 명령파일 수정하기
   - `systemctl edit --full <service-name>.service` 
   - `sudo systemctl edit --full sshd.service`
  - 새로운 데몬 서비스가 생성된 경우 그 라이브러리 목록 재 갱신 
   - `systemctl daemon-reload`

#### 프로세스 서비스 등록해보기(예제 -1)
- 내가 만들고자 하는 서비스를 간단하게 shell 로 작성
  - usr/local/sbin/my-script.sh 를 다음과 같이 작성
~~~shell
#!/bin/bash
echo "I'm in $(date + %Y%m%d-%H%M%S)" >> /tmp/mylog.log
~~~
- service 파일을 다음과 같이 작성
- /etc/systemd/system/my-startup.service
~~~shell
[Unit]
Description=My Startup

[Service]
ExecStart=/usr/local/sbin/my-script.sh

[Install]
WantedBy=multi-user.target
~~~
- 다음의 명령어 들을 통해 테스트를 해보면 됨!
  - `systemctl status my-startup.service`
  - `sudo systemctl enable my-startup.service` 
  - `systemctl start my-startup.service`
  - `chmod +x /usr/local/sbin/my-script.sh`
  - `systemctl start my-startup.service`
  - `systemctl status my-startup.service`
- $ 으로 표시되는 것은 사용자 권한, # 으로 표시되는 것은 root 권한임을 기억하자 

#### 프로세스 서비스 등록해보기(예제 -2)
- 이번에는 반복 루프를 통해 데몬 형태로 돌아갈 수 있게끔 script 를 작성해보았음
~~~shell
# /usr/local/sbin/my-daemon.sh

#!/bin/bash
# 필요하면 권한 부여 --> `chmod +x my-daemon.sh`
while true
do
    echo "I'm still in ${date + %Y%m%d-%H%M%S}"
    sleep 10
done
~~~
~~~shell
# /etc/systemd/system/my-daemon.service

[Unit]
Description=My First Daemon
After=network.target

[Service]
ExecStart=/usr/local/sbin/my-daemin.sh
Restart=always  
RestartSec=5
User=user1
Group=user1
~~~
- 다음의 명령어들을 통해 서비스 상태를 확인해보자
  - `systemctl status my-daemon.service`
  - `systemctl start my-daemon.service`
  - `journalctl -u my-daemon -f`
  - `systemctl kill my-daemon.service`

## 용어 정리
- backporting 
  - 최신 버전의 정보들을 구버전에 업데이트 하는 것을 말함 


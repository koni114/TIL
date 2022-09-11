# chapter03_6 보안 및 방화벽
## 보안 기능 및 방화벽(iptables)
- 보안 기능 개요
  - SELinux
- 방화벽
  - iptables
- 접근 차단 유틸리티
  - fail2ban, brute-force ssh 접속 차단

## 보안 기능 개요 - SELinux 소개
- 접근통제(ACL) 기능을 통한 디렉토리, 파일, 네트워크 소켓 등에 대한 자원에 접근 권한을 설정
- 접근 통제 모델
  - 임의적 접근 통제: DAC(Discretionary Access Control)
    - 사용자의 신분(및 그룹)을 통해 제한(uid, gid, setuid 등)
    - 객체(objects)의 사용자(user)에게 소유권(ownership)이 결정 됨
  - 강제적 접근 통제: MAC(Mandatory Access Control)
    - 미리 정해진 정책과 보안 등급에 의거하여 주체(subjects - 사용자, 프로세스, 프로그램)와 객체(파일, 디바이스)에게 허용된 접근 권한 부여
    - 불필요한 부분을 제거하고, 오직 필요한 기능만에 대한 권한을 안전하게 부여
- DAC는 리눅스 계정 권한으로 기본 탑재
- MAC은 SELinux 를 통해 구현
- SELinux(Security-Enhanced Linux)
  - `sudo apt install selinux`(초보자는 비추천)

## 방화벽 - 개요
- 네트워크 트래픽 접근제어 설정
- 방화벽? 
  - 기본 차단(default Deny Rule)
  - 5-Tuple based(SIP / DIP / PROTO / SPORT / DPORT)

![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_21.png)

- 리눅스는 기본적으로 방화벽이 꺼져있으며, ALL ALLOW 정책이 적용되어 있음. 따라서 필요에 따라 DENY 로 설정해 주어야 함

## 방화벽 - 개요(리눅스)
- OSI 계층 구조에 따라서 각각의 방화벽 기능이 존재함
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_22.png)


## 방화벽 - 리눅스 넷필터 아키텍처
- 네트워크 트래픽 접근제어 프레임워크
  - 리눅스에서의 네트워크 필터링
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_23.png)

## 방화벽 - 리눅스 넷필터 아키텍처 정책 설정도구, iptables
### 네트워크 트래픽 접근제어 프레임워크 - 단순화
  - 리눅스에서의 iptables 체인을 사용한 네트워크 패킷 필터링
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_24.png)

### 네트워크 트래픽 접근제어 설정
- iptables 명령어
~~~shell
$ iptables -L
~~~
- docker 가 설치된 경우 docker0 인터페이스로 주고받는 패킷으로 인해 상당히 많은 룰이 있음

### 네트워크 트래픽 접근제어 설정 - iptables 기본 문법
- iptables <옵션> <상세명령> <정책> 
- 옵션
  - `-L` : 목록 출력
  - `-A <Chain>` : 새로 정책 추가 (--append)
  - `-I <Chain> <Prio>` : 특정 위치에 정책 추가 (--insert)
  - `-D <Chain>` : 정책 삭제 (--delete)
  - `-N <Chain>` : 새로운 체인 추가(생성)
  - `-F <Chain>` : 체인 내 규칙 삭제 (--flush)
  - `-X <Chain>` : 체인 삭제 (--delete-chain)
  - `-P <Chain> <Action>` : 체인의 기본 정책 설정 (--policy)
- 상세명령
  - `-s <IP>` : 패킷의 출발지
  - `-d <IP>` : 패킷의 목적지
  - `-p <proto>` : 패킷의 프로토콜
  - `--sport <port>` : 패킷의 출발지 port
  - `--dport <port>` : 패킷의 목적지 port
- 정책
  - `-j` DROP : 패킷 차단
  - `-j` ACCEPT : 패킷 허용
  - `-j` LOG : 패킷 로깅

### 네트워크 트래픽 접근제어 설정 - iptables 활용 예시
- iptables 사용 예
  - 외부 입력 차단
    - `iptables -A INPUT -p tcp --dport -j DROP`
    - `iptables -I INPUT 1 -p tcp --dport 21 -j ACCEPT`
    - `iptables -D INPUT -p tcp --dport 80 -j DROP`
  - 내부 송신 차단 또는 허용/로깅
    - `iptables -A OUTPUT -p icmp -d 8.8.8.8 -j DROP`
    - `iptables -A OUTPUT -p icmp -d 8.8.8.8 -j LOG --log-level 4 --log-prefix “MyLog: ”`
  - 새로운 로깅과 차단 체인 생성
    - `iptables -N LOG_DROP`
    - `iptables -A LOG_DROP -j LOG --log-prefix “INPUT:DROP: “ --log-level 6`
    - `iptables -A LOG_DROP -j DROP`
    - `iptables -A INPUT -p tcp --dport 5555 -j LOG_DROP`
  - 기존 룰 삭제
    - `iptables –F INPUT`

### 네트워크 트래픽 접근제어 설정 - iptables 활용한 다양한 응용 실 사례
- iptables 사용 예
  - `slow down SSH brute-force attack` (연속해서 4번 접속 실패(시도) 시 60초동안 차단)
    - `iptables -I INPUT -p tcp --dport 22 -i eth0 -m state --state NEW -m recent --set`
    - `iptables -I INPUT -p tcp --dport 22 -i eth0 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 -j DROP`
   - PING 요청 차단(DDoS 공격 방지를 위한...)
     - `iptables -A OUTPUT -p ICMP --ICMP-type echo-request -j DROP`
   - HTTP/HTTPS 패킷의 conntrack 관리
     - `iptables -A INPUT -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT`
     - `iptables -A OUTPUT -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT`
     - `iptables -A INPUT -p tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT`
     - `iptables -A OUTPUT -p tcp --sport 443 -m state --state ESTABLISHED -j ACCEPT`
     - `iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT`
     - `iptables -A INPUT -i lo -j ACCEPT`

## 무작위 SSH 접속 차단 유틸리티 - fail2ban
- 특정 시간 내 반복 로그인 실패 시 정해진 시간만큼 해당 호스트의 접속을 차단
- 설치방법
  - `apt install fail2ban`
- 확인/활성화
  - `systemctl status fail2ban`
  - `systemctl enable fail2ban`
  - `systemctl restart fail2ban`
- 설정파일
  - `/etc/fail2ban/jail.conf`
  - `/etc/fail2ban/jail.local`
- 로그파일
  - `/var/log/fail2ban.log`
- fail2ban 의 각종 설정 및 내부 동작
  - 설정파일
    - `/etc/fail2ban/jail.conf`
~~~shell
# /etc/fail2ban/jail.conf
[DEFAULT]
ignoreip = 127.0.0.1/8   #  차단하지 않을 대역
bantime = 600            #  차단 시간
findtime = 600           #  접속 시도 체크 범위
maxretry = 5             #  실패 횟수 => 600초(10분) 동안에 5회 실패 시 600초 간 차단
~~~
- 주의: 차단 시 SSH 접속 시도만이 아닌, 해당 IP 주소의 모든 패킷 차단됨

## iptables 실습
~~~shell
$ iptables -nvL

# 결과 -> 아무것도 setting 되어 있지 않음을 확인 
Chain INPUT (policy ACCEPT 1 packets, 76 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 1 packets, 76 bytes)
 pkts bytes target     prot opt in     out     source               destination    
~~~
- 앞서 방화벽에는 5-Tuple based rule 이 있다고 했는데, 위의 `iptables -nvL` 을 통해서는 INPUT/FORWARD/OUTPUT 만 확인 가능
- 만약 나머지 2가지(PREROUTING, POSTROUTING)도 확인하고 싶은 경우는 `-t nat` 를 통해서 확인 가능
~~~shell
$ iptables -nvL -t nat
~~~
- INPUT은 바깥에서 패킷이 들어와 해당 리눅스 서버의 어플리케이션 쪽으로 요청이 온 것들을 말함. 
- FORWARD은 단일 리눅스 서버에서는 잘 사용되지 않으며, 앞서 main/sub-server 구성시 하나의 리눅스 서버에서 인터페이스를 통해 다른 인터페이스로 패킷을 보내는 경우 등에 사용
- OUTPUT은 현재 리눅스 서버에서 패킷을 생성한 후 바깥으로 보내는 것을 말함
- 만약 `ping 8.8.8.8` 을 수행할 경우, iptable 의 OUTPUT CHAIN 을 거쳐 보내지게 됨
~~~shell
$ ping 172.17.0.2
~~~
~~~shell
# INPUT/ OUTPUT 의 ACCEPT packet 이 증가되는 것을 확인
$ iptables -nvL
Chain INPUT (policy ACCEPT 42 packets, 3304 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain OUTPUT (policy ACCEPT 48 packets, 3784 bytes)
 pkts bytes target     prot opt in     out     source               destination      
~~~
- 이번에는 iptables 에 RULE 을 추가해서 내부에서 외부로 나가지 못하게 막아보자
~~~shell
# -A : append 를 통해 RULE 추가
# -p : protocol 은 icmp
# -j DROP : drop 하겠다는 의미
$ iptables -A OUTPUT -p icmp -j DROP 
~~~
- 위의 명령어 수행시, `ping 8.8.8.8` 이 끊키는 것을 확인할 수 있음
~~~shell 
64 bytes from 172.17.0.2: icmp_seq=9 ttl=64 time=0.058 ms
64 bytes from 172.17.0.2: icmp_seq=10 ttl=64 time=0.054 ms
ping: sendmsg: Operation not permitted
ping: sendmsg: Operation not permitted
ping: sendmsg: Operation not permitted
ping: sendmsg: Operation not permitted
...
~~~
- 다시 해당 rule 을 삭제 할 수 있음
~~~shell
$ iptables -D OUTPUT -p icmp -j DROP 
~~~
- rule 을 정교하게 넣을 수 있음. 예를 들어 ping 8.8.4.4 는 통과시키면서, ping 8.8.8.8 은 막고싶은 경우가 있을 것임
- 다음과 같이 설정 가능
~~~shell
$ iptables -A OUTPUT -p icmp -d 8.8.8.8 -j DROP 
~~~
- 차단되는 패킷을 확인하고 싶은 경우 LOG 를 남길 수 있음
~~~shell
$ iptables -A OUTPUT -p icmp -d 8.8.8.8 -j LOG

# 해당 로그는 kern.log 에 남음
$ tail -F/var/log/kern.log 
~~~
- 만약 DROP 을 하면서 LOG 을 남기고 싶은 경우는 나만의 chain 을 만들어 주면 됨
~~~shell
$ iptables -N LOG_DROP
$ iptables -nvL         # chain 추가 확인

# LOG_DROP 에 RULE 2개 추가
$ iptables -A LOG_DROP -j LOG --log-prefix "MyLog: "
$ iptables -A LOG_DROP -j DROP
~~~
- 외부에서 해당 서버로 들어오는 것을 막고 싶은 경우, 다음과 같이 설정 가능
~~~shell
$ iptables -A INPUT -p tcp --dport 80 -j DROP
~~~
- 만약 LOG를 남기면서 DROP 하고 싶은 경우는 이전에 만들었던 LOG_DROP chain에 넘겨주면 됨  
~~~shell
$ iptables -A INPUT -p tcp --dport 80 -j LOG_DROP
~~~
- 외부에서 접속시 차단된 경우라면, log 에 여러가지 정보(MAC, IP 등)가 적혀있을 것임
- 만약 등록한 다양한 rule 을 모두 삭제하고 싶은 경우 `-F` 사용
~~~shell
$ iptables -F INPUT
$ iptables -F OUTPUT

$ iptables -F LOG_DROP
$ iptables -X LOG_DROP
~~~

## fail2ban 실습
- brute-force 공격을 차단할 수 있는 fail2ban 를 설치해보고 실습해보자
~~~shell
$ apt install fail2ban -y
$ ls -al /etc/fail2ban  # 각종 설정 파일 확인
$ ls -al /var/log/fail  # 각종 로그 파일 확인
~~~
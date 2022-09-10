# chapter03_4 네트워크 모니터링
- 네트워크 설정 확인(기본 유틸리티)
  - ipconfig
  - arp
  - route
  - ip
  - netstat
- 네트워크 기본 테스트(기본 유틸리티)
  - ping
  - traceroute
  - nslookup
- 디버깅도구
  - nmap
  - nc
  - tcpdump
- 네트워크 모니터링 도구(추가 설치)
  - nload
  - iftop
  - iptraf
  - nethogs
  - bmon
  - ...

## 네트워크 설정 기초 - ifconfig
- 네트워크 인터페이스(NIC, network interface card) 의 설정
- host에 존재하는 모든 인터페이스를 살펴볼 수 있고, 필요에 따라 해당 인터페이스를 down(user-off) 할 수도 있음
- ifconfig 명령어를 통해 ip 와 서브넷을 재할당 할 수 있음
- `ifconfig`
  - 인터페이스 확인
  - 참고: `lo` : loop back 의 줄임말로, 자기 자신에게 보내는 데이터를 처리하기 위한 가상 인터페이스 장치 이름
- `ifconfig -a` 
  - 모든 인터페이스 확인
- 사용 예시
  - `ifconfig enp0s3 down` : 인터페이스를 down(use-off)  
  - `ifconfig enp0s3 up` : 인터페이스를 up(use-on)
  - `ifconfig enp0s3 192.168.0.2/24` : ip 와 서브넷을 재할당 
- 네트워크 인터페이스명
  - 고전적: eth0, eth1, eth2 같은 편한 이름을 사용해왔음
- 현재(ubuntu 16.04) : eth0 -> enp0s3
  - 인터페이스 네이밍 기법
    - 펌웨어/바이오스로부터 할당: eno1
    - PCI express 슬롯 번호: ens1
    - 물리적 하드웨어 컨넥터 위치: enp2s0


## 네트워크 설정 기초 - 고정 IP 할당
- 네트워크 인터페이스(NIC) 의 수동 설정
- 인터페이스 설정파일 수정
~~~shell
$ ifconfig            # network Interface 확인

# docker 에서 해당 명령어 수행시 host server 에서 연결한 ssh 연결 끊킴
$ ifconfig eth0 down  # 해당 ip network Interface down
$ ifconfig eth0 up    # 해당 ip network Interface up

$ ifconfig eth0 172.17.0.2/24
~~~

- 인터페이스의 ip 주소를 수동으로 할당하는 방법
- 인터페이스의 카드가 부팅될 때는 `/etc/network/interfaces` 를 참조하게 됨
~~~shell
$ vim /etc/network/interfaces
~~~
~~~shell
# /etc/network/interfaces

auto lo
iface lo inet lookback

# DHCP 수동 설정의 경우, -> inet dhcp
auto enp0s3
iface enp0s3 inet dhcp

# 고정 IP 수동 설정의 경우, -> inet static
auto enp0s3
iface enp0s3 inet static
address 192.168.0.2
netmask 255.255.255.0
gateway 192.168.56.1
dns-nameservers 8.8.8.8 8.8.4.4
~~~
- 설정 후 다음의 명령어로 네트워크 재설정 로딩을 해주어야 함!
~~~shell
$ sudo systemctl restart networking
~~~
- 설정 후 특정 인터페이스만 재설정하는 경우
~~~shell
$ sudo ifdown enp0s3
$ sudo ifup enp0s3
~~~

## 네트워크 설정 기초 - arp
- 인접 디바이스 및 MAC주소 확인
- arp 테이블 조회
  - `arp -an`
- arp 주소 삭제
  - `arp -d <ip주소>`
- arp 주소 고정 추가
  - `arp -s <ip주소> <mac주소>`
~~~shell
$ arp -a
$ arp -an

# arp entry 가 잘못 들어갔거나, 다른 곳에서 ip 충돌이 발생해 ip 주소와 mac 주소가 안맞는 경우
# arp 명령어를 통해 맞춰줄 수 있음

$ arp -d 10.0.2.2   # 해당 엔트리는 사라짐
$ ping 8.8.8.8      # 다시 외부로 패킷을 쏘기 위해서는 gateway 주소를 가져와야 
                    # 하기 떄문에 아래 명령어로 확인시 다시 생김
$ arp -an 
~~~
- 간혹 해커들이 집에 있는 공유기를 해킹을 한다거나 해서 집에 있는 사용자들의 패킷을 해커의 ip 주소로 redirect 시키는 경우가 있는데, 이를 해결하기 위해서 `arp -s` 를 통해 정적으로 mac 주소로 매핑해 줄 수 있음
~~~shell
$ arp -s 172.17.0.100 00:11:22:33:44:55

# 결과 확인
? (172.17.0.100) at 00:11:22:33:44:55 [ether] PERM on eth0
? (172.17.0.1) at 02:42:8f:b9:19:7d [ether] on eth0

# 다시 삭제
$ arp -d 172.17.0.100
~~~

## 네트워크 설정 기초 - route
- route 명령어를 통한 라우팅 테이블 변경
- 일반적으로는 변경할 일이 없지만, 회사 또는 집에서 여러개의 공유기를 사용하려고 할 때 두 공유기 간의 네트워크 통신일 필요할 때 변경할 일이 있을 수 있음
- 각각의 대역에 해당하는 네트워크 대역을 추가해서 통신이 가능하게 하도록 만들어 줄 수 있음
~~~shell
$ route add default gw 10.0.2.50
~~~
- 라우팅 테이블 조회
  - `route -n`
- 라우팅 테이블 추가
  - `route add`
  - `route del`
- 사용 예시
  - 기본 라우팅(default gateway) 추가/삭제
    - `route add default gw 10.0.2.2`
    - `route del default gw 10.0.2.2`
  - 기본 게이트웨이 대역 외에 라우팅 테이블 추가/삭제
    - `route add -net 192.168.0.0 netmask 255.255.255.0 gw 10.0.2.2`
    - `route add -net 192.168.0.0 netmask 255.255.255.0`
  - 특정 서브넷 대역이 아닌 특정 호스트만 추가하고 싶은 경우
    - `route add -host 192.168.1.1 dev enp0s3`
    - `route del -host 192.168.1.1`

## 네트워크 설정 기초 - ip
- 다소 포괄적인 내용을 가지고 있음
- IP 주소 확인/설정 관련 통합 명령어
- 특정 인터페이스 확인
  - `ip link`
  - `ip addr`
  - `ip addr show enp0s3`
- 라우팅 확인
  - `ip route`
- 인접 디바이스 (L2/L3) 확인
  - `ip neigh`
- 라우팅 정책 확인
  - `ip rule`
- 사용 예
  - `ip rule show`
  - `ip route show table main`
  - `ip route get 8.8.8.8`
  - `ip route get 8.8.8.8 from 10.0.2.15`
- PBR(Policy Based Routing) 사용 예(고급)
  - `ip rule add from 192.168.0.0/32 table 1 priority 100`
  - `ip route add default via 10.0.2.15 table 1`
  - `ip route show table 1`
  - `ip route flush cache`

## 네트워크 설정 기초 - ip 명령
- ip 명령어를 통한 IP 주소 셋업 및 라우팅 테이블 변경
- 인터페이스 IP 주소 추가/삭제
~~~shell
$ ip addr add 10.0.2.16/24 dev enp0s3 # secondary IP 추가
$ ip addr del 10.0.2.16/24 dev enp0s3 # IP 삭제
~~~
- `ifconfig` 명령어와 동일하게 특정 인터페이스를 down/up 가능
~~~shell
$ ip link set enp0s3 up
$ ip link set enp0s3 down
~~~
- 라우팅 테이블 변경
  - 기본 라우팅(default gateway) 추가/삭제
    - `ip route add 192.168.0.0/24 via 10.0.2.2 dev enp0s3`
    - `ip route del 192.168.0.0/24`
  - 문법이 떠오르지 않을때, 도움말
    - `ip route help`
    - `map ip route`
- 내가 특정 호스트로 패킷을 보내기 위해서 어떤 라우팅 테이블을 참조해서 패킷을 보내는지 확인
~~~shell
$ ip route get 8.8.8.8
~~~

## 네트워크 설정 기초 - netstat
- 시스템 내 열려있는 포트 확인하거나, 어떤 애플리케이션이 해당 포트를 사용하고 있는지 확인
- 사용법
  - netstat <OPTION>
    - `-a` : 모든 소켓 정보(**)
    - `-r` : 라우팅 정보 출력
    - `-l` : LISTEN 하고 있는 포트를 보여 줌
    - `-n` : 호스트명 대신 IP 주소를 출력(**)
    - `-i` : 모든 네트워크 인터페이스 정보 출력
    - `-s` : 프로토콜별 네트워크 통계
    - `-t` : tcp 로 연결된 포트를 보여줌
    - `-p` : 해당 소켓과 관련된 프로세스 표시(**)
~~~shell
$ netstat -ant | egrep "Proto|LISTEN"

# 결과
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp6       0      0 :::80                   :::*                    LISTEN     
tcp6       0      0 :::21                   :::*                    LISTEN     
tcp6       0      0 :::22                   :::*                    LISTEN           
~~~
- 해더 내용
  - `Proto` : Protocol
  - `Local Address` : 열려 있는 사용자 컴퓨터의 IP/호스트네임과 포트 번호
  - `Foreign Address` : 사용자의 컴퓨터에 접속되어 있는 IP/호스트네임과 포트 번호
- 결과를 보면 80, 21, 22 포트가 열려있는 것을 확인할 수 있고, nginx server 가 80, ssh-server 가 22 포트를 사용하고 있음을 확인 가능
- 상태값은 현재 연결된 상태를 다양한 값으로 표현함
  - `LISTEN` : 연결 요구를 기다리는 상태, 포트가 열려 있음
  - `ESTABLISHED` : 서로 연결되어 있는 상태
  - `CLOSED` : 완전히 연결이 종료된 상태 

- 사용 예
  - 라우팅 테이블 확인
    - `netstat -rn`
  - 인터페이스 통계 표시
    - `netstat -i`
  - 모든 소켓과 프로세스 표시
    - `netstat -anp`
  - 열려있는 TCP 소켓 확인
    - `netstat -ant | grep LISTEN`

## 네트워크 기본 테스트 - ping
- ping은 ICMP 패킷을 통한 네트워크가 죽었는지 살았는지 등을 확인하기 위해서 사용하는 명령어
- 기본적으로 ping 다음에 ip address 를 입력하면, 해당 ip 에 ICMP 패킷을 주게되어 정상적으로 return 되는지 확인 가능
- 사용법
  - `ping <목적지 IP>`
- 사용 예
  - `ping 8.8.8.8`
  - `ping 8.8.8.8 -c 3`  : c(count), 3번 보냄

## 네트워크 기본 테스트 - traceroute
- 네트워크 라우팅 경로 트레이싱 도구
- 해당 목적지까지 다양한 경로가 있을텐테, 어떤 경로가 있는지 트레이싱 해주는 명령어
- traceroute 내부적으로 ICMP protocol 을 통해서 각 home 마다 패킷을 보내 이동경로를 추적하는 것
~~~shell 
$ traceroute www.google.com
$ traceroute 127.0.0.1
~~~
- 사용법
  - `traceroute <목적지 IP>`
- 설치
  - `sudo apt install traceroute`
- 사용 예
  - `traceroute 8.8.8.8`
  - `traceroute www.google.com`
  - `traceroute www.daum.net`
- 참고
  - 중간에 방화벽이 있거나(VM장비 NAT포함)
  - ICMP 응답을 비활성화 해 둔 장비는 응답을 받을 수 없음
  - 응답 속도에 따라 거치는 route 경로가 달라질 수 있음

## 네트워크 기본 테스트 - nslookup
- 호스트 이름을 IP 주소로 변환해 주는 도구
~~~shell
$ nslookup www.google.com

# 결과
Server:		192.168.65.5
Address:	192.168.65.5#53

Non-authoritative answer:
Name:	www.google.com
Address: 172.217.24.68
Name:	www.google.com
Address: 2404:6800:4005:81d::2004

$ nslookup www.naver.com

# 결과
# -> 하나 이상의 domain IP address 가지고 있는 경우도 있음

Server:		192.168.65.5
Address:	192.168.65.5#53

Non-authoritative answer:
www.naver.com	canonical name = www.naver.com.nheos.com.
Name:	www.naver.com.nheos.com
Address: 223.130.195.95
Name:	www.naver.com.nheos.com
Address: 223.130.195.200
~~~
- 사용법
  - `nslookup <도메인명>`
  - `nslookup <도메인명> <질의 네임서버>`
- 사용 예
  - `nslookup www.google.com`
  - `nslookup www.google.com 8.8.8.8`
  - `nslookup www.naver.com`
  - `nslookup www.naver.com 8.8.8.8`
- 참고
  - 기본 도메인 서버 /etc/resolv.conf 참고
  - 설정은 /etc/resolvconf/resolv.conf.d/base
  - 또는 /etc/resolvconf/resolv.conf.d/tail 에 추가 nameserver 8.8.8.8
  - 수정 후 sudo resolvconf -u 로 갱신

## 네트워크 분석 도구 - nmap
- 네트워크 포트 스캔 / IP 검색 등 다양한 네트워크 스캐닝 도구(주의. 공격 도구이기도 함)
- 일반적으로 많이 사용하지는 않음
~~~shell
$ nmap localhost

# 결과
Starting Nmap 7.80 ( https://nmap.org ) at 2022-09-07 20:12 KST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000030s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 996 closed ports
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
3306/tcp open  mysql

$ nmap -sP 172.17.0.0/24 # 해당 대역의 IP list 를 scan 하여 보여줌

# 결과
Nmap scan report for 172.17.0.1
Host is up (0.000042s latency).
MAC Address: 02:42:BF:D6:A6:09 (Unknown)
Nmap scan report for ubuntu (172.17.0.2)
Host is up.
Nmap done: 256 IP addresses (2 hosts up) scanned in 1.98 seconds

$ nmap -O 10.0.2.15

# 결과
# OS 버전이 정확하지는 않지만, 어떤 OS 를 가지고 있는지 확인 가능
Starting Nmap 7.80 ( https://nmap.org ) at 2022-09-07 20:18 KST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000078s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 996 closed ports
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
3306/tcp open  mysql
Device type: general purpose
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6.32
OS details: Linux 2.6.32
Network Distance: 0 hops
~~~
- 사용법
  - `nmap <옵션><목적지 IP>`
    - `-sS`: TCP SYN 스캔
    - `-sT`: TCP 연결 스캔
    - `-sP`: ping 스캔
    - `-sU`: UDP 스캔
    - `-O`: 운영체제 확인 
    - `-v`: 상세 출력
    - `-F`: 빠른 스캔
- 설치
  - `sudo apt install nmap`
- 사용 예
  - 내 호스트(localhost)의 열린 포트 확인 
    - `nmap localhost`
  - 내 네트워크에 존재하는 호스트 확인(ping scan)
    - `nmap -sP 10.0.2.0/24`
  - 10.0.2.2 호스트의 열린 포트 확인(tcp syn scan)
    - `nmap -sS 10.0.2.2`
  - 10.0.2.15 의 운영체제 확인
    - `nmap -O 10.0.2.15`
  - 10.0.2.0/24 네트워크의 호스트에 TCP 연결 빠른 스캔 및 운영체제 확인
    - `nmap -sT -F -O -v 10.0.2.0/24`

## 네트워크 분석 도구 - nc(netcat)
- 네트워크 데이터 매뉴얼(수동) 입력 도구
- 내가 원하는 네트워크 패킷을 입력해 직접 전송해 볼 수 있는 도구
- 설치
  - `apt install nc`
~~~shell
$ nc localhost 22 # 수동으로 22번 port 로 접속

SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
efqiejfpqjewpf     # 내가 원하는 패킷 형태 입력
Ncat: Broken pipe. # 적절한 형태가 아니여서 broken 된 후 종료됨 
~~~
- 다음과 같이 webserver 에 정상적인 패킷(HTTP protocol) 형태로 전송하게 되면 200 이 떨어지는 것을 확인할 수 있음
~~~shell
$ echo -e "HEAD / HTTP/1.0\n\n" | nc localhost 80 

# 결과
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Wed, 07 Sep 2022 11:28:46 GMT
Content-Type: text/html
Content-Length: 612
Last-Modified: Mon, 29 Aug 2022 11:29:50 GMT
Connection: close
ETag: "630ca32e-264"
Accept-Ranges: bytes
~~~
- 다른 역할로 내가 서버의 역할을 해볼 수 있음
- 다음과 같이 1234 포트를 열어 포트 안으로 접속하여 확인 가능
~~~shell
$ nc -l -p 1234
hello
world
~~~
~~~shell
$ nc localhost 1234

# 다음과 같이 찍히는 것을 확인할 수 있음
hello
world
~~~
- 사용 예
  - `nc localhost 22`
  - `nc localhost 80`
  - `echo -e "HEAD /HTTP/1.0/\n\n" | nc localhost 80`
  - 서버 모드
    - `nc -l -p 1234`  
      (다른 커맨드 창에서)`nc localhost 1234`

## 네트워크 분석 도구 - tcpdump
- tcpdump 설치
~~~shell
$ apt install tcpdump
~~~
- 네트워크 트래픽 패킷 덤프 및 분석
~~~shell
$ tcpdump -i eth0

# 결과 -> 주고 받는 패킷이 많다면 계속 확인 가능
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
...

# 주고 받는 패킷의 결과를 100개만 보고 싶은 경우
$ tcpdump -i eth0 -c 100

# 주고 받는 패킷의 최대 100개의 결과를 test.pcap 이라는 파일에 저장
$ tcpdump -i eth0 -c 100 -w test.pcap

# 저장된 결과를 불러와 확인 
$ tcpdump -r test.pcap

# 패킷에 대한 디테일한 정보를 보고 싶은 경우
$ tcpdump -i eth0 -c 10 -vvv
~~~
- 사용법
  - `tcpdump <옵션>`
    - `-i <nic>` : 인터페이스
    - `-w` : 덤프 파일로 저장
    - `-r` : 저장된 덤프 파일 로딩
    - `c <cnt>` : 캡처 할 패킷의 수
    - `s <size>` : 패킷 캡처 길이(-sO 은 모든 길이)
    - `-v -vv, -vvv` : 패킷 상세 정보 표시
    - `-n, -nn` : hostname 및 port 에 대한 resolve 끄기(off)
- 사용 예
  - `tcpdump -i enp0s3`
  - `tcpdump -i enp0s3 -w test.pcap`
  - `tcpdump -i enp0s3 -w test pcap -c 10`
  - `tcpdump -i enp0s3 -sO -nn`

## 네트워크 분석 도구 - tcpdump #2
- 네트워크 트래픽 패킷 덤프 및 분석 - 상세 필터링 옵션
- 너무 많은 패킷들이 존재하는데, 이 중에서 내가 원하는 패킷만 보고 싶은 경우
~~~shell
# 22 번 포트의 패킷은 제외하고 보고 싶은 경우
$ tcpdump -i eth0 not port 22

# icmp 패킷만 보고 싶은 경우
$ tcpdump -i eth0 icmp

# icmp 패킷을 보내는 경우
$ (다른 커맨드 창에서) ping 8.8.8.8 

# 결과
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
20:52:47.480771 IP ubuntu > dns.google: ICMP echo request, id 5, seq 1, length 64
20:52:47.536589 IP dns.google > ubuntu: ICMP echo reply, id 5, seq 1, length 64
20:52:48.484023 IP ubuntu > dns.google: ICMP echo request, id 5, seq 2, length 64
20:52:48.541279 IP dns.google > ubuntu: ICMP echo reply, id 5, seq 2, length 64
20:52:49.486029 IP ubuntu > dns.google: ICMP echo request, id 5, seq 3, length 64
20:52:49.532549 IP dns.google > ubuntu: ICMP echo reply, id 5, seq 3, length 64
20:52:50.489876 IP ubuntu > dns.google: ICMP echo request, id 5, seq 4, length 64
...
~~~
- 필터
  - `tcpdump <옵션><필터>`
    - `host <ip>` : 해당 호스트와의 통신
    - `src <ip>` : 출발지 IP 기준
    - `dst <ip>` : 목적지 IP 기준
    - `net <ip/cidr>` : 해당 네트워크 대역 통신
    - `port <port>` : 특정(출발지/목적지) 포트
    - `portrange <port-port>` : 특정 포트 범위
    - `<proto>` : 특정 프로토콜(icmp, tcp, udp) 
- 사용 예
  - `tcpdump -i enp0s3 host 1.2.3.4`
  - `tcpdump -i enp0s3 src 2.3.4.5`
  - `tcpdump -i enp0s3 dst 3.4.5.6`
  - `tcpdump -i enp0s3 net 1.2.3.0/24`
  - `tcpdump -i enp0s3 port 22`
  - `tcpdump -i enp0s3 portrange 20-21`
  - `tcpdump -i enp0s3 icmp`
  - `tcpdump -i enp0s3 src 1.2.3.4 and dst port 80`
  - `tcpdump dst 192.168.0.2 and src net and not icmp`
  - `tcpdump 'dst 8.8.8.8 and (src net 192.168.0.0/24 or 172.16.0.0/16)'`
  - `tcpdump 'src 8.8.8.8 and (dst port 3389 or 22)'`

## 용어 정리
- DHCP(Dynamic Host Configuration Protocol)
  - IP 주소와 게이트웨어 또는 네임서버의 주소의 정보를 자동으로 할당해주는 프로토콜
  - 일반적인 가정집이나 사무실에서 가장 많이 사용됨
- 
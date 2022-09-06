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
- `ifconfig`
  - 인터페이스 확인
- `ifconfig` -a
  - 모든 인터페이스 확인
- 사용 예시
  - `ifconfig enp0s3 down`
  - `ifconfig enp0s3 up`
  - `ifconfig enp0s3 192.168.0.2/24`
- 네트워크 인터페이스명
  - 고전적: eth0, eth1, eth2
- 현재(ubuntu 16.04) : eth0 -> enp0s3
  - 인터페이스 네이밍 기법
    - 펌웨어/바이오스로부터 할당: eno1
    - PCI express 슬롯 번호: ens1
    - 물리적 하드웨어 컨넥터 위치: enp2s0

## 네트워크 설정 기초 - 고정 IP 할당
- 네트워크 인터페이스(NIC) 의 수동 설정
- 인터페이스 설정파일 수정
~~~shell
$ vim /etc/network/interfaces

# 기본값: 루프백 인터페이스
$ auto lo
$ iface lo inet lookback

# DHCP 수동 설정
$ auto enp0s3
$ iface enp0s3 inet dhcp

# 고정 IP 수동 설정
$ auto enp0s3
$ iface enp0s3 inet static
$ address 192.168.0.2
$ netmask 255.255.255.0
$ gateway 192.168.0.1
$ dns-nameservers 8.8.8.8 8.8.4.4
~~~
- 설정 후 네트워크 재설정
~~~shell
$ sudo systemctl restart networking
~~~
- 설정 후 특정 인터페이스 재설정
~~~shell
$ sudo ifdown enp0s3
$ sudo ifup enp0s3
~~~

## 네트워크 설정 기초 - arp
- 인접 디바이스 및 MAC주소 확인
- arp 테이블 조회
  - `arp-an`
- arp 주소 삭제
  - `arp-d <ip주소>`
- arp 주소 고정 추가
  - `arp -s <ip주소> <mac주소>`

## 네트워크 설정 기초 - route
- route 명령어를 통한 라우팅 테이블 변경
- 라우팅 테이블 조회
  - `route -n`
- 라우팅 테이블 추가
  - `route add`
  - `route del`
- 사용 예시
  - 기본 라우팅(default gateway) 추가/삭제
    - `route add default gw 10.0.2.2`
    - `route del default gw 10.0.2.2`
  - 라우팅 테이블 추가/삭제
    - `route add -net 192.168.0.0 netmask 255.255.255.0 gw 10.0.2.2`
    - `route add -net 192.168.0.0 netmask 255.255.255.0`
    - `route add -host 192.168.1.1 dev enp0s3`
    - `route del -host 192.168.1.1`

## 네트워크 설정 기초 - ip
- IP 주소 확인/설정 관련 통합 명령어
- 인터페이스 확인
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
  - `ip addr add 10.0.2.15/24 dev enp0s3`
  - `ip addr del 10.0.2.15/24 dev enp0s3`
- 인터페이스 링크 Up/Down
  - `ip link set enp0s3 up`
  - `ip link set enp0s3 down`  
- 라우팅 테이블 변경
  - 기본 라우팅(default gateway) 추가/삭제
    - `ip route add 192.168.0.0/24 via 10.0.2.2 dev enp0s3`
    - `ip route del 192.168.0.0/24`
  - 문법이 떠오르지 않을때, 도움말
    - `ip route help`
    - `map ip route`

## 네트워크 설정 기초 - netstat
- 시스템 내 열려있는 포트 확인
- 사용법
  - netstat <OPTION>
    - `-a` : 모든 소켓 정보
    - `-r` : 라우팅 정보 출력
    - `-n` : 호스트명 대신 IP 주소를 출력
    - `-i` : 모든 네트워크 인터페이스 정보 출력
    - `-s` : 프로토콜별 네트워크 통계
    - `-p` : 해당 소켓과 관련된 프로세스 표시
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
- ICMP 패킷을 통한 네트워크 연결 확인
- 사용법
  - `ping <목적지 IP>`
- 사용 예
  - `ping 8.8.8.8`
  - `ping 8.8.8.8 -c 3`

## 네트워크 기본 테스트 - traceroute
- 네트워크 라우팅 경로 트레이싱 도구
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

## 네트워크 기본 테스트 - nslookup
- 호스트 이름의 IP 주소 변환 도구
- 사용법
  - nslookup <도메인명>
  - nslookup <도메인명> <질의 네임서버>
- 사용 예
  - nslookup www.google.cm
  - nslookup www.google.com 8.8.8.8
  - nslookup www.naver.com 
  - nslookup www.naver.com 8.8.8.8
- 참고
  - 기본 도메인 서버 /etc/resolv.conf 참고
  - 설정은 /etc/resolvconf/resolv.conf.d/base
  - 또는 /etc/resolvconf/resolv.conf.d/tail 에 추가 nameserver 8.8.8.8
  - 수정 후 sudo resolvconf -u 로 갱신
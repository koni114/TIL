# chapter 03_5 멀티 테스트 환경 구축하기
## 방화벽 테스트를 위한 환경 구축하기
- VM 들간의 내가 원하는 네트워크 구성하기
- 이번 시간에는 VM1, VM2의 guestOS 를 구성하고, VM1 guestOS 에서만 외부 인터넷 연결하도록 환경 구축해보기
  - VM1 - Ubuntu 16
  - VM2 - Ubuntu 16
  - ...

## 연습 문제
- 다음 환경 구성하기
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_19.png)

- 두 대의 가상 서버를 구축
- 두 개의 guestOS 중 인터넷과 연결할 guestOS 를 main server 라고 지칭하자. 
- 나머지 하나의 guest OS sub-server 라고 부르겠음. 인터넷을 직접적으로 연결하지 못하도록 비활성화 시켜야함. 비활성화 시킨 guest os 는 main guest os 를 통해 인터넷 연결할 예정
- 서버간에 패킷을 주고받게끔 하기 위해서 다양한 환경변수를 설정해 주어야 함

### 실습 - 1 VM 복제 및 네트워크 설정
- 기존의 VM server 를 복제함(완전복제)
- main server 의 네트워크 설정 변경
  - 어댑터1 : NAT
  - 어댑터2 : 호스트 전용 어댑터
  - 어댑터3 : 내부 네트워크(intnet) 설정
- sub-server 네트워크 설정 변경
  - 어댑터1 : 비활성화
  - 어댑터2 : 호스트 전용 어댑터
  - 어댑터3 : 내부 네트워크(intnet) 설정

### 실습 - 2 네트워크 설정 확인
- Main GuestOS server 를 시작한 후 `ifconfig` 명령어를 통해 새롭게 interface 가 생성된 것을 확인할 수 있음  
이 때 위에서 어댑터3에서 설정한 내부 네트워크(intnet)(-> enp0s9)은 내부 네트워크로 설정되어 DHCP가 없기 때문에 아무런 IP를 할당받지 못한 것을 확인. 따라서 수동으로 IP 를 할당해야 함
- why? 해당 내부 네트워크에 IP 를 할당해 주어야 해당 인터페이스로 인터넷과 통신이 가능
- 아래와 같이 IP를 수동 설정 해주자
- main/sub server 에 둘 다 아래와 같이 반영해 주어야 함 

#### 인터페이스 IP 수동 설정 - main-server
- `ifconfig` 명령어를 통해 인터페이스명, IP 주소 및 넷마스크를 할당할 수 있음
~~~shell
$ ifconfig enp0s9 10.0.2.1/24
~~~
- 하지만 위와 같이 설정 후 재부팅을 하게 되면 정보가 다 날아가므로, `/etc/network/interface` 에 수동 IP를 설정해 주어야 함 
~~~shell
$ vi /etc/network/interface 
~~~
~~~shell
# /etc/network/interface 
auto enp0s9
iface enp0s9 inet static
address 10.0.2.1
netmask 255.255.255.0
~~~
- system daemon 에 해당 정보를 올리기 위해 networking restart 를 통해 설정 반영
~~~shell
$ systemctl restart networking
~~~
- 방금 반영한 enp0s9 만 반영하기 위해서는 아래와 같이 설정할 수도 있음
~~~shell
$ ifdown enp0s9
$ ifup enp0s9
$ ifconfig enp0s9
~~~

#### 인터페이스 IP 수동 설정 - sub-server
- 위와 거의 비슷하게 설정하되 인터넷을 연결할 수 있는 main server 를 gateway 로 지정해 주어야 함
~~~shell
# /etc/network/interface 
auto enp0s9
iface enp0s9 inet static
address 10.0.2.2
netmask 255.255.255.0
gateway 10.0.2.1  # main-server 가 인터넷과 연결할 수 있는 유일한 포트이기 때문에 gateway 를 main-server로 설정
dns-nameservers 8.8.8.8 8.8.4.4
~~~
- 마찬가지로 restart 수행
~~~shell
$ systemctl restart networking
$ ifconfig enp0s9
~~~
- 연결이 잘 되는 지 확인
~~~shell
$ ping 10.0.2.1
~~~
- main-server 에서 정상적으로 패킷이 수신이 되는지 확인
~~~shell
$ tcpdump -i enp0s9 icmp
$ tcpdump -i enp0s9 icmp -nn  # ip 로 dump 가 되는 것을 확인하려면 -n 추가
~~~
- 위의 설정 만으로는 패킷이 외부로 나갈 수 없음.
- main-server 에서 인터넷으로 패킷을 전송하려면 enp0s9 -> enp0s3 인터페이스로 전송이 되어야 하는데 그렇지 않은 것을 확인할 수 있음.
~~~shell
$ tcpdump -i enp0s3 icmp -nn 
~~~
- 그 이유는 우분투는 사용자가 쓰기 위한 것이기 때문에 라우터의 기능을 하지 않기 때문
  이를 하도록 설정해 주어야 함

#### 외부 패킷 전송을 위한 라우터 설정
~~~shell
$ cat /proc/sys/net/ipv4/ip_forward   # 기존 forward 확인(docker 에서는 1로 설정되어 있음)
$ sysctl -w net.ipv4.ip_forward=1     # ip 포워딩
~~~
- 다시 dump 를 떠보면 패킷이 외부로 나가는 것을 확인할 수 있음
~~~shell
$ tcpdump -i enp0s3 icmp 
~~~
- 그런데, sub-server 에서 `ping 8.8.8.8` 을 쏘면, 외부로는 나가지만 외부에서 다시 내부로 응답이 들어오고 있지 않음
- virtualbox 에 있는 nat 환경에서 나갔다가 응답이 와야함. 그런데 main-server는 nat 설정이 해당 서버에 되어 있으므로 인지를 하고 응답이 오는 반면, sub-server 에서는 nat 설정이 해당 서버에 하지 않아 router 에 직접적으로 붙어있지 않다보니 IP 역변환을 시켜줄 수 없음
- 결과적으로 main-server 가 router 역할을 수행할 수 있도록 변경해 주어야 함

#### main-server router 역할 등록하기
- `iptables` 명령어를 통해 main-server 를 router 로 등록해 주어야 함
~~~shell
# enp0s3 인터페이스로 나가는 모든 패킷을 MASQUERADE 의 IP 주소로 변환을 시켜주는 명령어 수행 
$ iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE 
~~~
- 위에서 설정한 iptables 설정은 재부팅을 하게되면 삭제가 됨
- 부팅이 되더라도 정상적으로 적용이 되도록 하기 위해 새로운 tool 을 설치해 주어야 함
- ipv4, ipv6 를 둘다 저장해주어야 함
~~~shell
$ apt install iptables-persistent
$ netfilter-persistent save  # ipv4, ipv6 가 save

# sysctl 도 재부팅 이후에 잘 불러오도록 하기 위하여 설정
$ vi /etc/sysctl.conf 
~~~ 

### 라우터 만들기(재확인)
- 우분투 운영체제를 사용한 라우터 환경 구성
- IP 포워딩
  - `sysctl -w net.ipv4.ip_forward=1`
  - 설정 저장을 위해 `/etc/sysctl.conf` 에 삽입
- IP 마스커레이드 - NAT 환경에서의 출발지IP 변환
  - `iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE`
  - 설정 저장을 위해
    - `apt install iptables-persistent`
    - `sudo netfilter-persistent save`
    - `sudo netfilter-persistent reload`


## 용어 정리
- NAT(Network Address Translation)
  - 네트워크 주소 변환의 약자
  - IP 패킷에 있는 출발지 및 목적지의 IP 주소와 TCP/UDP 포트 숫자 등을 바꿔 재기록하면서 네트워크 트래픽을 주고 받게 하는 기술
- NIC(Network Interface Controller)
  - 컴퓨터를 네트워크에 연결하여 통신하기 위해 사용하는 하드웨어 장치
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_20.png)
- Guest OS
  - VM 위에 설치된 OS를 GuestOS 라고 부름
  - 반대로 HostOS는 물리적인 머신 위에 설치된 OS를 지칭함
- MASQUERADE(MASQ, IPMASQ)
  - 리눅스의 NAT 기능으로서 내부 컴퓨터들이 리눅스 서버를 통해 인터넷 등 다른 네트워크에 접속할 수 있도록 해주는 기능
  
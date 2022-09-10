# chapter 03_5 멀티 테스트 환경 구축하기
## 방화벽 테스트를 위한 환경 구축하기
- VM 들간의 내가 원하는 네트워크 구성하기
  - VM1 - Ubuntu 16
  - VM2 - Ubuntu 16
  - VM3 - Ubuntu 18
  - ...

## 연습 문제
- 다음 환경 구성하기
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_19.png)

- 두 대의 가상 서버를 구축
- main guest OS 하나 있고, 나머지 하나의 guest OS 는 직접 인터넷으로 연결하는 것이 아니라, 비활성화 시켜야함. 비활성화 시킨 guest os 는 main guest os 를 통해 인터넷 연결할 예정
- 서버간에 패킷을 주고받게끔 하기 위해서 다양한 환경변수를 설정해 주어야 함

### 실습 - 1 VM 복제 및 네트워크 설정
- 기존의 VM server 를 복제함(완전복제)
- Main GuestOS server 의 네트워크 설정 변경
  - 어댑터1 : NAT
  - 어댑터2 : 호스트 전용 어댑터
  - 어댑터3 : 내부 네트워크(intnet) 설정
- 복제된 Guest OS server 네트워크 설정 변경
  - 어댑터1 : 비활성화
  - 어댑터2 : 호스트 전용 어댑터
  - 어댑터3 : 내부 네트워크(intnet) 설정

### 실습 - 2 네트워크 설정 확인
- Main GuestOS server 를 시작한 후 `ifconfig` 명령어를 통해 새롭게 interface 가 생성된 것을 확인할 수 있음  
이 때 내부 네트워크로 설정되어 DHCP 가 없기 때문에 IP 는 따로 할당되지 않은 것을 확인
- 따라서 수동으로 IP 를 할당해보자
~~~shell
$ ifconfig enp0s9 10.0.2.1/24
$ vi /etc/network/interface 
~~~
- 인터넷과 연결하지 않을 guestOS server 의 해당 파일(`/etc/network/interface`)에 다음과 같이 셋팅
~~~shell
# /etc/network/interface 
auto enp0s9
iface enp0s9 inet static
address 10.0.2.1
netmask 255.255.255.0
~~~
- networking restart 를 통해 설정 반영
~~~shell
$ systemctl restart networking
$ ifdown enp0s9
$ ifup enp0s9
~~~
- main guestOS server 에도 네트워크 설정
~~~shell
# /etc/network/interface 
auto enp0s9
iface enp0s9 inet static
address 10.0.2.2
netmask 255.255.255.0
gateway 10.0.2.1  # main GuestOS 가 인터넷과 연결할 수 있는 유일한 포트이기 때문에 gateway 를 상대방 pc ip로 설정
dns-nameservers 8.8.8.8 8.8.4.4
~~~
~~~shell
$ systemctl restart networking
$ ifconfig enp0s9
~~~
- 연결이 잘 되는 지 확인
~~~shell
$ ping 10.0.2.1
~~~
- 반대 guest server 에서도 정상적으로 패킷이 수신이 되는지 확인
~~~shell
$ tcpdump -i enp0s9 icmp
~~~
- main guestOS 에서 인터넷으로 패킷을 전송하려면 enp0s3 인터페이스로 전송이 되어야 하는데, 그렇지 않은 것을 확인할 수 있음.
- 그 이유는 우분투는 사용자가 쓰기 위한 것이기 때문에 라우터의 기능을 하지 않음.  
  이를 하도록 설정해 주어야 함
~~~shell
$ cat /proc/sys/net/ipv4/ip_forward   # forward 확인
$ sysctl -w net.ipv4.ip_forward=1     # ip 포워딩

$ tcpdump -i enp0s3 icmp  # 바깥으로 패킷이 나가는 것을 확인할 수 있음
~~~
- 중요한 것은 virtualbox 에 있는 nat 환경을 나갔다가 응답이 와야하는데, main guestOS Server는 인지를 하고 응답이 오는 반면, 다른 guestOS server 에서는 router 에 직접적으로 붙어있지 않다보니 변환이 안됨
- 결과적으로 main guestOS 가 router 역할을 수행할 수 있도록 변경해 주어야 함
~~~shell
# enp0s3 인터페이스로 나가는 모든 패킷을 인터페이스 IP 주소로 변환해줌
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


### 라우터 만들기
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
- NIC(Network Interface Controller)
  - 컴퓨터를 네트워크에 연결하여 통신하기 위해 사용하는 하드웨어 장치
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_20.png)

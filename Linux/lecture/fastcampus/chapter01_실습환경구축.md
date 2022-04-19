# chapter01- 실습환경구축
## 가상환경이란
- 하이퍼바이저(Hypervisor) 호스트 컴퓨터에서 다수의 운영 체제(Operating System)를 동시에 실행하기 위한 논리적 플랫폼을 말함

## 가상환경 제공 소프트웨어
- VirtualBox
- vmware
- Microsoft Hyper-V

## VirtualBox 네트워크
- NAT: 가상머신 내부 네트워크에서 HOST PC 외부 네트워크 단방향 연결, (HOST Server에서 게스트OS(guest OS)통신 불가)
- 어댑터에 브리지: 호스트 PC와 동등하게 외부 네트워크와 연결(IP할당 외부로부터 받음)  
  만약 내 노트북이 IPTIME에 연결되어 있다면 해당 가상머신은 별도의 노트북처럼 인지되어 IP가 할당됨
- 내부 네트워크: Virtualbox 내부 guestOS 네트워크와만 통신 가능
- 호스트 전용: 가상 머신과 HOST 와만 통신 가능
- 일반 드라이버: 거의 미사용. (UDP 터널 네트워크 등)
- NAT 네트워크: NAT + Host 내부 네트워크와 통신 가능
- 연결되지 않음 : 네트워크 미사용(Link down)


## VirtualBox 네트워크 구성
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_02.png)

## VirtualBox 네트워크 - 어댑터에 브리지
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_03.png)

- 호스트PC와 동등하게 외부 네트워크와 연결(IP할당 외부로부터 받음)

## VirtualBox 네트워크 - 내부 네트워크
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_04.png)

- VirtualBox 내부 guestOS 네트워크와만 통신 가능

## VirtualBox 네트워크 - 호스트 전용 어댑터
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_05.png)

- VirtualBox 내부 guestOS 네트워크와만 통신 가능
## VirtualBox 네트워크 정리
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_06.png)


## NAT 상세 설정 - 포트 포워딩
- NAT 같은 것을 사용하면 가상 서버에서 웹서버를 띄었을 떄 외부에서 접근이 불가한데, 이 때 접근하도록 하기 위한 방법
- 포트 포워딩 규칙을 추가할 수 있으며, 호스트 포트와 게스트 포트를 매핑해주면 됨

## VM 원격 접속환경 구축하기
- '1. VM에 설치한 ubuntu에 터미널을 띄어 ssh daemon 을 설치해야함
~~~shell
$ sudo service sshd status        # not-found 인 경우 sshd 설치 필요
$ sudo apt install openssh-server # ssh-daemon 설치  
$ sudo service sshd start         # 아무 반응이 없으면 실행 된 것
~~~
- `ifconfig` 명령어를 통해 원격으로 접속할 주소를 확인  
  --> 10.0.2.15로 접속이 되지 않음!
- 그 이유는 NAT network를 사용하고 있기 때문에 바깥에서 우분투 시스템으로 접속은 불가능한 상태
- `route print` 명령어를 통해서 라우팅 테이블을 확인해보면 `10.0.0.0`의 대역 자체가 없는 것을 확인할 수 있음

### NAT network 환경에서 원격 접속 문제 해결 방법 
#### '1. NAT 내부망 내로 접속하기(포트 포워딩)
- virtualbox 네트워크 환경에서 포트 포워딩 추가  
  이름은 `SSH`, 호스트 포트와 게스트 포트를 22로 설정 
- macOS 에서 기본 터미널에서 원격 접속 방법  
~~~shell
$ ssh koni114@127.0.0.1 -p 22
~~~
#### '2. 호스트 전용 어댑터로 접속하기
- virtualbox -> ubuntu16.04 -> 설정 -> 네트워크 -> 어댑터2 -> 호스트 전용 어댑터를 선택한 후 어댑터를 선택  
(해당 작업은 우분투 가상 서버가 종료되어 있는 상태어야 함)
- 우분투 가상 서버 재시작 후  `ifconfig` 명령어로 새로 설정된 호스트 전용 서버의 ip 주소로 접속하면 됨
~~~shell
# host server 에서 해당 명령어로 접속
$ ssh koni114@192.168.56.103 
~~~

### 확장팩 설치하기
- virtualbox download 홈페이지에서 `Extension Pack` 설치 후 실행하여 확장 기능을 설치
  (실행하면 자동으로 반영됨)

## 운영체제 구조와 특징
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_01.png)

- ubuntu 에서는 root 사용자의 접속을 막아버림  
  필요하다면 활성화는 가능하지만, 위험성이 있어 막았다는 사실은 기억해야함
- 관리자와 사용자가 명확하게 구분되어 있음
- 나는 사용자이고, 필요하다면 sudo 커맨드를 통해 권한을 빌려서 사용
- <b>`suduer`는 권한을 빌려갈 수 있는 그룹을 말함</b>

## AWS 원격 접속환경 구축하기
### AWS 가상환경 구축하기
- VPC - 생략
  - 서브넷, 라우팅 테이블, 인터넷 게이트웨이, NAT 게이트웨이 등
  - 모두 기본값으로 Default VPC 사용
- EC2 생성
  - Ubuntu Server 16.04 LTS(HVM)
  - t2.micro(1 CPU, 1G RAM)
  - 10GB SSD
  - SG: SSH(TCP/22)
  - Keypair: fc_linux.pem 

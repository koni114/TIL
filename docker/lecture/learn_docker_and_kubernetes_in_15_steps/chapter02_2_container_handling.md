# 컨테이너 다루기
## 대화형 모드로 컨테이너 기동 및 정지
- 도커도 컨테이너에서 셸을 실행할 수 있음

### 대화형 모드로 컨테이너 기동(docker run -it)
- 대화형 모드로 컨테이너를 기동하기 위해서는 `docker run -it 리포지터리명:태그 셸` 과 같이 명령어 실행
  - `-i` : 키보드의 입력을 표준 입력으로 셸에 전달
  - `-t` : 유사 터미널 디바이스(pts)와 셸을 연결   
- 셸은 터미널과 접속되어 있다고 인식하여 셸의 프롬포트를 출력하게 됨
- 우분투나 centos는 bash 를 지정할 수 있고, Alpine, BusyBox 에서는 sh 지정 가능
~~~shell
$ docker run -it --name test1 centos:7-git bash
[root@baa18e7f6f08 /]#
~~~
- @ 이후의 문자열은 해당 컨테이너 ID 이자 컨테이너의 호스트명
- `--name` 명령어를 생략하면 자동으로 랜덤으로 container 명이 생성되어 지정됨
- 컨테이너명을 지정할 때 CONTAINER ID 대신에 이 일므을 사용할 수 있음 

### 대화형 모드에서 컨테이너 정지
- 셸에서 `exit`를 입력하면 됨. 그러면 셸이 종료되면서 컨테이너도 종료됨

## 컨테이너 조작 및 이미지 작성
- 레지스트리에 등록된 공식 이미지 우분투와 CentOS를 기동한 후 소프트웨어 패키지를 설치한 뒤 이미지로 보존해보기
- 실행 중인 컨테이너는 IP 주소를 할당받고 이를 바탕으로 컨테이너 간 통신을 수행할 수 있음
- 우분투는 `apt`, CentOS는 `yum`을 통해 다운로드 가능
~~~shell
# ubuntu 
$ apt-get update && apt-get install -y iputils-ping net-tools iproute2 dnsutils curl
$ ipconfig eth0

# 결과
# inet --> 172.17.0.3
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.3  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 02:42:ac:11:00:03  txqueuelen 0  (Ethernet)
        RX packets 10  bytes 796 (796.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

~~~
~~~shell
# centOS
$ yum update -y && yum install -y iputils net-tools iproute bind-utils
$ ifconfig eth0

# 결과
# inet --> 172.17.0.2
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.2  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 02:42:ac:11:00:02  txqueuelen 0  (Ethernet)
        RX packets 30419  bytes 44675263 (44.6 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 13950  bytes 766276 (766.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
~~~
- 위의 두개의 컨테이너 모두 image 로 생성해보자  
  `docker commit 컨테이너ID | 컨테이너명 리포지터리명[:태그]`를 수행시, 이미지가 만들어져 리포지터리에 보관됨  
  두 개의 컨테이너를 모두 이미지로 보관
~~~shell
$ docker commit centos my-centos:0.1
$ docker commit ubuntu my-ubuntu:0.1

$ docker images | grep my
# 결과 확인
my-ubuntu                  0.1       f61e914431da   About a minute ago   168MB
my-centos                  0.1       ccada7dfbfc2   About a minute ago   724MB
~~~
- 위의 방법을 사용하여 이미지를 만들면 이미지에 어떤 도구를 설치했는지 어렵다는 단점이 있음  
  그래서 실행한 컨테이너로부터 이미지를 만들지 않는 것이 좋다는 의견도 있음
- 실행 중인 컨테이너의 IP 주소는 도커 커맨드로 확인 가능.   
  `docker inspect [옵션] 컨테이너 ID | 컨테이너명`을 실행하면 컨테이너의 상세 정보를 JSON 형식으로 표시해줌
~~~shell
$ docker inspect ubuntu -f="{{ range.NetworkSettings.Networks }}{{.IPAddress}}{{end}}" 
~~~

## 여러 터미널에서 조작하기
- 2개 이상의 터미널에서 하나의 컨테이너에 접속하여 작업 수행도 가능
- 터미널1에서는 옵션 `--name` 으로 이름을 지정하여 컨테이너를 기동하며 셸을 실행함
- 터미널2에서는 `docker exec -it 컨테이너명 bash`를 실행하여 같은 컨테이너에 접속

![img](https://github.com/koni114/TIL/blob/master/docker/img/docker_09.jpeg)

### 대화형 컨테이너로 셀 기동
~~~shell
$ docker run -it --name my-centos my-centos:0.1
~~~

### 실행 중인 컨테이너에 접속(docker exec -it)
- `docker exec -it 컨테이너명 | 컨테이너 ID 셸`을 실행하여 컨테이너 `my-centos` 를 기동
~~~shell
$ docker exec -it my-centos bash
~~~
- 이처럼 같은 컨테이너에 여러 터미널이 접속하여 작업하는 것이 가능. 인증 과정도 없기 때문에 가상 서버보다 편리하게 사용 가능
- 보안을 위해 호스트 외부에서의 접속은 막혀 있음. 또한 컨테이너 내에서는 외부에서 로그인하기 위한 sshd를 기동시키지 말아야한다는 의견도 있음

### 로그인을 관리하지 않는 컨테이너
- 리눅스 서버에서는 `w` 명령어로 동시에 로그인한 다른 유저의 정보를 얻을 수 있음
- 하지만 컨테이너에서는 `w` 커맨드를 실행해도 아무것도 출력되지 않음
- 컨테이너에는 로그인을 통한 유저 인증 기능도 없고, 유저 자체를 관리하지 않기 때문  
  <b>리눅스는 기본적으로 멀티 유저용으로 개발되었지만 컨테이너는 싱글 유저용으로 만들기 위해 해당 기능을 제거함</b>  
- 컨테이너 내에서 `ps` 커맨드 결과를 보면, `TTY` 열을 보면 유사 터미널 `pts/1`에 연결되어 있는 것을 확인 가능
- `tty` 커맨드로 확인해 봐도 `/dev/pts/1` 이 표시됨. 이는 `docker run`의 `-t` 옵션에 의해 서버에 로그인하는 것과 비슷하게 유사 터미널이 셸에 접속했기 때문
~~~shell
# my-centus container 환경에서 명령어 수행
[root@820f72f51d78 /]#  ps ax
  PID TTY      STAT   TIME COMMAND
    1 pts/0    Ss     0:00 bash
   46 pts/1    Ss+    0:00 bash
   60 pts/0    R+     0:00 ps -ax
~~~
- 컨테이너를 일종의 가상 서버로 생각하기 쉬운데, 사실을 그렇지 않다  
  컨테이터는 <b>목표로 하는 프로세스만을 실행할 수 있도록 고안된 실행 환경인 것임</b>

## 호스트와 컨테이너의 관계
- 여기서 말하는 호스트란, 컨테이너를 실행하는 리눅스 서버를 말함  
  호스트와 컨테이너의 관계를 알기 위해 호스트의 운영체제에서 컨테이너의 실행 상태를 관찰해보자 
- 여기서 `vagrant up`을 실행하여 가상 머신 기동  
  그리고 미니쿠베를 실행하지 않은 상태에서 3개의 터미널을 열어 각각 `vagrant ssh`로 로그인
- 먼저 터미널 1에서 대화형 컨테이너를 기동해서 `sleep` 커맨드 실행
- 터미널 2로부터 같은 컨테이너에 접속하여 프로세스 목록을 출력
- 터미널 3에서는 컨테이너가 아닌 호스트의 프로세스 목록을 관찰  
~~~shell
# vagrant up 수행 --> github의 cd 15_DantK/vagrant-minikube 에서 해당 명령어 수행
$ vargrant up

# terminal 1
$ vagrant ssh
vagrant@minikube: docker run -it --name lucy centos:7 bash
$ sleep 321

# terminal 2
$ vagrant ssh
$ docker exec -it lucy bash
$ ps axf

# 결과
PID TTY      STAT   TIME COMMAND
16 pts/1    Ss     0:00 bash
32 pts/1    R+     0:00  \_ ps axf
1  pts/0    Ss     0:00 bash
15 pts/0    S+     0:00 sleep 321

# terminal 3
$ vagrant ssh
$ ps axf

# 결과
1343 ?        Ss     0:00 /usr/sbin/sshd -D
10583 ?        Ss     0:00  \_ sshd: vagrant [priv]
10625 ?        S      0:00  |   \_ sshd: vagrant@pts/0
10626 pts/0    Ss     0:00  |       \_ -bash
10693 pts/0    Sl+    0:00  |           \_ docker run -it --name lucy centos:7 bash
10854 ?        Ss     0:00  \_ sshd: vagrant [priv]
10889 ?        S      0:00  |   \_ sshd: vagrant@pts/1
10890 pts/1    Ss     0:00  |       \_ -bash
10906 pts/1    Sl+    0:00  |           \_ docker exec -it lucy bash
10961 ?        Ss     0:00  \_ sshd: vagrant [priv]
10996 ?        S      0:00      \_ sshd: vagrant@pts/2
10997 pts/2    Ss     0:00          \_ -bash
11013 pts/2    R+     0:00              \_ ps axf
 3369 ?        Ss     0:00 /usr/sbin/uuidd --socket-activation
 6090 ?        Ss     0:00 /sbin/rpcbind -f -w
 8331 ?        Ssl    0:07 /usr/bin/dockerd -H fd://
 8340 ?        Ssl    0:09  \_ docker-containerd --config /var/run/docker/containerd/containerd.toml
10783 ?        Sl     0:00      \_ docker-containerd-shim -namespace moby -workdir /var/lib/docker/containerd/daemon/io.containerd.runtime.v1.linux/
10800 pts/0    Ss     0:00          \_ bash
10853 pts/0    S+     0:00          |   \_ sleep 321
10929 pts/1    Ss+    0:00          \_ bash
~~~

- 터미널 2에서 동일한 컨테이너로 접속하여 프로세스 목록을 출력. 이때 TTY 열의 pts/0 은 앞서 실행한 터미널 1에 연결된 프로세스
- pts/1이 터미널 2에 대응하는 프로세스. 이렇게 보면 가상 서버처럼 단독으로 동작하는 리눅스처럼 보임
- 터미널 3에서 호스트의 상태를 살펴보면, 컨테이너 호스트의 리눅스에 접속한 상태에서 가상 머신에서 동작하는 데몬 중 관련 있는 것만 선발해서 확인
- TTY 열에서, 터미널 1은 `pts/0`, 터미널 2는 `pts/1`, 터미널 3은 `pts/2`와 연결되어 있음
- 중요한 것은 <b>컨테이너의 실체는 호스트의 프로세스임. 컨테이너는 하나의 독립적인 운영체제처럼 보이지만, 실은 호스트의 커널을 공유하여 동작하는 리눅스 프로세스임</b>



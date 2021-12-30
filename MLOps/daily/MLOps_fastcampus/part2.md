## Docker 와 Kubernetes 
### MLOps에서 쿠버네티스가 필요한 이유 
- Reproducibility
  - 실행 환경의 일관성 & 독립성 
- Job Scheduling
  - 스케줄 관리, 병렬 작업 관리, 유후 작업 관리
- Auto-healing & Auto-scaling
  - 장애 대응, 트래픽 대응
- 도커와 쿠버네티스를 활용하면 다음과 같은 기능들을 쉽게 구현이 가능

### Containerization & Container란 무엇일까
- Containerization
  - 컨테이너화 하는 기술
- Container
  - 격리된 공간에서 프로세스를 실행시킬 수 있는 기술
- 지금은 나의 ML code를 independent 하도록 정보를 모두 담은 실행 환경 자체를 하나의 패키지로 만드는 기술로 이해해도 무방

### Container Orchestration
- 수많은 도커 컨테이너를 어떤 역할을 하는 컨테이너는 어디에 배치할 것인가를 지휘하는 것을 말함
- kubernetes 가 container orchestration의 거의 대세가 됨
- Container Orchestration 기술은 여러 명이 함께 서버를 공유하며 각자 모델 학습을 돌리고자 할 때, GPU가 남았는지 매번 확인하거나, 학습이 끝나면 서버 자원을 깔끔하게 정리하고 나오거나, 이러한 귀찮은 일들을 할 필요없이 수많은 컨테이너 들을 정해진 룰에 따라서 관리해 주는 것이라고 이해해도 됨

### Docker의 기본 개념
- Build Once, Run Anywhere
- 도커에서 제공하는 패키징 방식을 통해, 하나의 어플리케이션을, 이 어플리케이션이 dependent한 것 들을 하나로 묶은 docker image 형태로 build 함으로써 어떤 OS, 환경에서 사용 가능
- docker image로 만드는 것을 dockerize 한다라고 말하자
- ML 모델의 제품화 서비스를 고려해야 할 때, docker는 필수

### Docker 실습 환경 준비
- docker는 linux container 기반의 기술이기 때문에 MacOS나 windows 위에서 수행되려면 VM 위에서 돌아가야 함
- VirtualBox 를 사용해 VM을 하나 띄우고, ubuntu 로 띄운 다음에 여러가지 실습을 진행할 예정
- VirtualBox 설치
  - 6.1.26 버전 설치
- ubuntu 20.04 설치
  - Desktop image download  
  - .iso 로 생성되는 파일이 download 됨
  - 다운 받는데 5분 이상 걸릴 수도 있음
- virtualBox 를 켜서 새로 만들기 버튼 클릭
- 종류는 linux, 버전은 ubuntu(64-bit로 고정)
- 메모리 크기는 8GB로 선택
- 하드 디스크 -> 지금 새 가상 하드 디스크 만들기 선택
- 하드 디스크 종류 -> VDI 선택
- 물리적 하드 드라이브에 저장 -> 동적 할당 선택
- 파일 위치 및 크기 -> 10.00GB 
- 완료 후 시작 버튼 클릭 후, 우측 버튼 아이콘을 선택한 후, 추가 버튼 클릭 후, 다운로드 경로를 찾아서 ubuntu 파일 선택하면, ubuntu가 실행됨 
- 이후 ubuntu 기본 설치 작업을 차례차례 진행하면, 완료

### Docker 실습 1, 2 - 설치와 기본 명령어
#### Docker 설치
- 공식 문서
  - https://docs.docker.com/engine/install/ubuntu/
  - 여러가지 install 방법 중, Install using the repository 방법으로 진행

1) Set up the repository
- `apt` 라는 패키지 매니저 업데이트
~~~shell
$ sudo apt-get update
~~~  
- 그리고, docker의 prerequisite(전제조건) package 들을 설치
~~~shell
$ sudo apt-get install \
       apt-transport-https \
       ca-certificates \
       curl \
       gnupg \
       lsb-release
~~~
- Docker 의 GPG key 추가
~~~shell
$ curl - fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
~~~
- 그 다음 stable 버전의 repository 를 바라보도록 설정
~~~shell
$ echo \
  "deb [arch=amd64 signed by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
~~~

#### Install Docker Engine
2) Docker 엔진의 최신 버전을 설치
~~~shell
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cil containerd.io
~~~
- 특정 버전의 Docker 버전 설치 필요시, 메뉴얼 참고

3) 정상 설치 확인
- docker container 를 실행시켜, 정상적으로 설치되었는지 확인
~~~shell
$ sudo docker run hello-world
~~~  
- 다음과 같이 출력시, 정상적으로 설치 된 것을 확인 가능
~~~shell
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
b8dfde127a29: Pull complete
Digest: sha256:0fe98d7debd9049c50b597ef1f85b7c1e8cc81f59c8d623fcb2250e8bec85b38 Status: Downloaded newer image for hello-world:latest
Hello from Docker!
This message shows that your installation appears to be working correctly.
To generate this message, Docker took the following steps:
1. The Docker client contacted the Docker daemon.
2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
(amd64)
3. The Docker daemon created a new container from that image which runs the
executable that produces the output you are currently reading.
4. The Docker daemon streamed that output to the Docker client, which sent it
to your terminal.
To try something more ambitious, you can run an Ubuntu container with: $ docker run -it ubuntu bash
Share images, automate workflows, and more with a free Docker ID: https://hub.docker.com/
For more examples and ideas, visit: https://docs.docker.com/get-started/
~~~

#### Docker 권한 설정
- 현재는 모든 docker 관련 작업이 root 유저에게만 권한이 있기 때문에, docker 관련 명령을 수행하려면 `sudo`를 앞에 붙여주어야만 가능
- 예를 들면
  - `docker ps` 수행 시, 다음과 같이 Permission denied 라는 메세지 출력
~~~shell
Got permission denied while trying to connect to the Docker daemon socket at uni x:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.40/containers/j son?all=1: dial unix /var/run/docker.sock: connect: permission denied
~~~  
- 따라서, root 유저가 아닌 host 의 기본 유저에게도 권한을 주기 위해 다음과 같은 명령을 <b>새로 띄운 터미널에서 수행해 주어야 함</b>
~~~shell
$ sudo usermod -a -G docker $USER
$ sudo service docker restart 
~~~
- 그 다음, VM을 로그아웃 한 다음에 다시 로그인하면 다음과 같이 정상적으로 출력되는 것을 확인 가능
~~~shell
CONTAINERID IMAGE COMMAND CREATED STATUS PORTS NAMES
~~~

#### Docker의 기본적인 명령
1) Docker pull

- docker image repository 부터 Docker image를 가져오는 커멘드
~~~shell
$ docker pull --help
~~~
- 예시)
~~~shell
$ docker pull ubuntu:18.04
~~~
- docker.io/library 라는 이름의 repository 에서 ubuntu:18.04 라는 image를 우리 노트북에 다운로드 받게 됨
- 추후 docker.io 나 public 한 docker hub와 같은 repository 대신에, 특정 private한 repository 에서 docker image 를 가져와야 하는 경우: docker login 을 통해 특정 repository를 바라보도록 한 뒤, docker pull을 수행하는 형태로 사용

2) Docker images
- 로컬에 존재하는 docker image 리스트를 출력하는 커맨드
~~~shell
$ docker images --help
~~~
- 예시
~~~
$ docker images
~~~

3) Docker ps
- 현재 실행중인 도커 컨테이너 리스트를 출력하는 커맨드
~~~shell
$ docker ps --help
~~~
- 예시
~~~
$ docker ps
# docker ps -a
~~~

4) Docker run
- 도커 컨테이너를 실행시키는 커맨드
~~~shell
$ docker run --help
~~~
- 예시
~~~shell
$ docker run -it --name demo1 ubuntu:18.04 /bin/bash
~~~
- `-it`: `-i` 옵션 + `-t` 옵션
  - container 를 실행시킴과 동시에 interactive 한 terminal 로 접속시켜주는 옵션 
- `--name` : name
  - 컨테이너 id 대신, 구분하기 쉽도록 지정해주는 이름
- `/bin/bash` 
  - 컨테이너를 실행시킴과 동시에 실행할 커맨드로, `/bin/bash` 는 bash 터미널을 사용하는 것을 의미

5) Docker exec
- Docker 컨테이너 내부에서 명령을 내리거나, 내부로 접속하는 커맨드
~~~shell
$ docker exec --help
~~~
- 예시)
~~~shell
$ docker run -it -d --name demo2 ubuntu:18.04
$ docker ps
~~~ 
- `-d` : 백그라운드에서 실행시켜서, 컨테이너에 접속 종료를 하더라도, 계속 실행 중이 되도록 하는 커맨드
~~~shell
$ docker exec -it demo2 /bin/bash
~~~
- 아까와는 동일하게 container 내부에 접속할 수 있는 것을 확인하는 기능

6) Docker logs
- 도커 컨테이너의 log를 확인하는 커맨드
~~~shell
docker logs --help
~~~
- 예시)
~~~shell
$ docker run --name demo3 -d busybox sh -c "while true; do $(echo date); sleep 1; done"
~~~
- demo3 라는 이름의 busybox 이미지를 백그라운드에서 도커 컨테이너로 실행하여, 1초에 한 번씩 현재 시간을 출력하는 커맨드
~~~shell
$ docker logs demo3
$ docker logs demo3 -f
~~~
- `-f` 옵션: 계속 watch 하며 출력

7) Docker stop
- 실행 중인 도커 컨테이너를 중단시키는 커맨드
~~~shell
$ docker stop --help
~~~
- 예시)
~~~shell
$ docker stop demo3
$ docker stop demo2
$ docker stop demo1
~~~ 

8) Docker rm
- 도커 컨테이너를 삭제하는 커맨드
~~~shell
$ docker rm --help
~~~
- 예시)
~~~shell
$ docker rm demo3
$ docker rm demo2
$ docker rm demo1 
~~~
- docker ps, docker ps -a 에서 모두 출력되지 않는 것을 확인

9) Docker rmi
- 도커 이미지를 삭제하는 커맨드
~~~shell
$ docker rmi --help
~~~
- 예시)
~~~shell
$ docker images
$ docker rmi ubuntu
~~~


### 리눅스 명령어 참고
- `curl` : 사용자 상호 작용 없이 작동하도록 설계된 서버에서 또는 서버로 데이터를 전송하기 위한 명령줄 유틸리티
- `echo` : 인수로 전달되는 텍스트 / 문자열을 표시하는 데 사용됨  
  이 명령어는 쉘 스크립트와 배치 파일에서 주로 현재 상태를 화면이나 파일로 출력하는데 사용되는 내장 명령어
  - `echo [option][string]` : 텍스트나 문자열을 보여줌
  - `echo -e` 백슬래시 이스케이프 해석 가능
    - `\b` 텍스트 사이의 모든 공백을 제거
  - `echo -e "Geeks \cfor Geeks"` : \c 뒤의 텍스트는 인쇄되지 않으며 세 줄 끝에서 생략
  - `\n` : 이 옵션은 사용되는 곳에서 새 줄을 만듬
  - `\t` : 가로 탭 공간 생성
  - `\r` : 출력할 위치 지정. 해당 명령어 뒤의 문자만 출력
  - `\v` : 이 옵션은 세로 탭 공간을 만드는 데 사용
  - `\a` : 이 옵션을 사용하면 경고음이 울림
  - `echo * ` : Is command 와 유사하며 모든 파일 / 폴더를 <b>한 줄로</b> 출력
  - `-n` : 후행 줄 바꿈 생략
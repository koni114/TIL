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
- 이후 ubuntu 기본 설치 작업을 차례차례 진행한 후에 reboot 수행하면 ubuntu 설치 완료
- 추가 작업사항
  - terminal에서 root passwd를 지정해야 함
  - root user의 비밀번호를 지정하는 것
  - `sudo passwd` 수행 후에 password update 수행
- 중간에 VM을 사용하지 않는 경우는 전원을 끈 상태로 유지해야 함

#### ubuntu 해상도 변경 방법
- 다음과 같은 명령어를 통해 VirtualBox Guest Addictions를 설치해 해상도 관련 기능 추가
- 게스트 도구를 이용하면 VM의 창의 크기를 조절할 수 있고, 호스트 운영체제(VirtualBox를 돌리는 운영체제)와 클립보드를 공유해서 복사, 잘라내기, 붙여넣기 등을 할 수 있음
- 게스트 도구는 Ubuntu package repository 에 저장되어 있음
~~~shell
sudo apt-get install -y virtualbox-guest-dkms
~~~
- 해당 명령어를 통해 설치 후, reboot 진행
- 이후 시스템 설정 -> 디스플레이 -> 해상도 변경


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
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
~~~
- 그 다음 stable 버전의 repository 를 바라보도록 설정  
  이 때 해당 cpu가 arm64 인지 amd64인지 확인해서 `arch=arm64` 또는 `arch=amd64` 로 설정
- 다음의 명령어를 통해 확인 가능
~~~shell
dpkg --print-architecture
~~~
~~~shell
echo \
"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] http
s://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
~~~

#### Install Docker Engine
2) Docker 엔진의 최신 버전을 설치
~~~shell
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
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
  - `-a`를 붙이면 실행되었던 컨테이너가 출력됨 
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

### Docker Image
#### Docker Image
- Docker Image 
  - 어떤 애플리케이션에 대해서, 애플리케이션 + dependent 한 모든 것을 함께 패키징한 데이터
- Dockerfile
  - 사용자가 도커 이미지를 쉽게 만들 수 있도록, 제공하는 탬플릿 

#### Dockerfile
1. Dockerfile 만들기
  - `Dockerfile` 이라는 이름으로 빈 file을 하나 만들어봄   
~~~shell
# home 디렉토리 이동
$ cd $HOME

# docker-practice 라는 이름의 폴더 생성
$ mkdir docker-practice

# Dockerfile 이라는 빈 파일을 생성
$ touch Dockerfile

# 정상적으로 생성되었는지 확인
$ ls
~~~

2. 기본 명령어
- Dockerfile 에서 사용할 수 있는 기본적인 명령어에 대해서 하나씩 알아보기
- `FROM`
  - Dockerfile 이 base image 로 어떠한 이미지를 사용할 것인지를 명시하는 명령어
~~~shell
FROM <image>[:<tag>] [AS <name>]d

# 예시
FROM ubuntu
FROM ubuntu:18.04
FROM ubuntu:latest AS ngx
~~~

- `COPY`
  - <src> 의 파일 혹은 디렉토리를 <dest> 경로에 복사하는 명령어
~~~shell
COPY <src>... <dest>

# 예시
COPY a.txt /some-directory/b.txt
COPY my-directory /some-directory-2
~~~

- `RUN`
  - 명시한 커맨드를 도커 컨테이너에서 실행하는 것을 명시하는 명령어 
~~~shell 
RUN <command>
RUN ["executable-command", "parameter1", "parameter2"]

# 예시
RUN pip install touch
RUN pip install -r requirements.txt
~~~

- `CMD`
  - 명시한 커맨드를 도커 컨테이너가 <b>시작될 때</b>, 실행하는 것을 명시하는 명령어    
  - 비슷한 역할을 하는 명령어로 `ENTRYPOINT` 가 있지만, 구분하기 어려울 수 있음
  - 하나의 Docker Image 에서는 하나의 CMD만 실행할 수 있다는 점에서 RUN 명령어와 다름
~~~shell
CMD <command>
CMD ["excutable-command", "parameter1", "parameter2"]
CMD ["parameter1", "parameter2"]

# 예시
CMD python main.py
CMD
~~~

- `WORKDIR`
  - 이후 작성될 명령어를 컨테이너 내의 어떤 디렉토리에서 수행할 것인지를 명시하는 명령어 
  - 해당 디렉토리가 없으면 생성
~~~shell
WORKDIR /path/to/workdir

# 예시
WORKDIR /home/demo
~~~

- `ENV`
  - 컨테이너 내부에서 지속적으로 사용될 environment variable 의 값을 설정하는 명령어임
~~~shell
ENV <key> <value>
ENV <key>=<value>

# 예시
# default 언어 설정
RUN locale-gen ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

- `EXPOSE`
  - 컨테이너에서 뚫어줄 포트/프로토콜을 지정할 수 있음
  - protocol을 지정하지 않으면 TCP 가 디폴트로 설정됨
~~~shell 
EXPOSE <port>
EXPOSE <port>/<protocol>

# 예시
EXPOSE 8080
~~~

3. 간단한 dockerfile 작성해보기
- `vi Dockerfile` 혹은 vscode 등 본인이 사용하는 편집기로 `Dockerfile`을 열어 다음과 같이 작성
~~~shell
# base image 를 ubuntu 18.04 로 설정
FROM ubuntu:18.04

# apt-get update 명령을 실행
RUN apt-get update 

# DOCKER CONTAINER 가 시작될 때, "Hello Campus"를 출력
CMD ["echo", "Hello FastCampus"]
~~~

#### Docker build from Dockerfile
- `docker build` 명령어로 Dockerfile 로부터 Docker Image 를 만들어 봄
~~~shell
docker build --help 
# 자세한 옵션들에 대한 설명은 생략 

# Dockerfile 이 있는 경로에서 다음 명령을 실행
docker build -t my-image:v1.0.0 .
~~~
- 설명
  - `.`(현재 경로에 있는 Dockerfile 로부터)
  - my-image 라는 이름과 v1.0.0 이라는 태그로 이미지를 빌드하겠다는 명령어
- 정상적으로 이미지 빌드되었는지 확인
~~~shell
# grep : my-image가 있는지를 확인하는 명령어 
docker images | grep my-images
~~~
- 이제 빌드한 my-images:v1.0.0 이미지로 docker 컨테이너를 run 해보자
~~~shell
docker run my-image:v1.0.0

# Hello FastCampus 가 출력되는 것 확인
~~~

#### Docker Image 저장소
1) Docker Registry
- 공식 문서
  - https://docs.docker.com/registry/
- 간단하게 도커 레지스트리를 직접 띄어본 뒤에, 방금 빌드한 my-image:v1.0.0 을  
  도커 레지스트리에 push
- Docker Registry는 이미 잘 준비된 도커 컨테이너가 존재하므로, 쉽게 사용 가능
- docker registry 띄어보기
~~~shell
docker run -d -p 5000:5000 --name registry registry

docker ps
# 정상적으로 registry 이미지가 registry 라는 이름으로 생성되었음을 확인할 수 있음
# localhost:5000 으로 해당 registry 와 통신 가능
~~~
- my-image를 방금 생성한 registry 를 바라보도록 tag 함
~~~shell
docker run -d -p 5000:5000 --name registry registry

docker ps
# 정상적으로 registry 이미지가 registry 라는 이름으로 생성되었음을 확인 가능
# localhost:5000 으로 해당 registry 와 통신 가능
~~~
- my-image 를 방금 생성한 registry를 바라보도록 tag 함
~~~shell
docker tag my-image:v1.0.0 localhost:5000/my-image:v1.0.0

docker images | grep my-image
# localhost:5000/my-image:v1.0.0 로 새로 생성된 것을 확인할 수 있음
~~~
- my-image 를 registry 에 push 함(업로드 함)
~~~shell
docker push localhost:5000/my-image:v1.0.0
~~~
- 정상적으로 push 되었는지 확인
~~~
# localhost:5000 이라는 registry 에 어떤 이미지가 저장되어 있는지 리스트를 출력하는 명령
curl -X GET http://localhost:5000/v2/_catalog

# 출력 : {"repositories": ["my-image"]}

# my-image 라는 이미지 네임에 어떤 태그가 저장되어있는지 리스트를 출력하는 명령
curl -X GET http://localhost:5000/v2/my-image/tags/list

# 출력 :  {"name":"my-image", "tags":["v1.0.0"]}
~~~

2) Docker Hub
- 다양한 사람들이 만들어둔 docker 등을 다운로드 받거나 할 수 있는 public hub
- 회원 가입
  - hub.docker.com
- Choose a Plan
  - Free 
- 이메일 인증
~~~shell
docker login

# username, password 입력
# Login Succeeded ! 
~~~
- Docker Hub 를 바라보도록 tag 생성
~~~shell
docker tag my-image:v1.0.0 fastcampusdemo/my-image:v1.0.0

# docker tag <image_name>:<tag_name> <user_name>/<image_name>:<tag>

docker push fastcampusdemo/my-image:v1.0.0

# docker push <user_name>/<image_name>:<tag>
~~~
- Docker hub의 본인 계정에서 업로드한 이미지 확인
  - https://hub.docker.com/repositories

### kubernetes 기본 개념
- 쿠버네티스는 운영 및 설치하기가 쉽지 않고, 운영, 모니터링하면서 장애 해결도 어려운 일이며, 기술적인 challenge를 요구함
- Public cloud service 에서는 Amazon EKS, Google Kubernetes Engine, Azure Kubernetes Service(AKS)를 제공함
- 나만의 작은 쿠버네티스를 노트북에 설치하고 삭제할 수 있는 open source project 들이 존재  
  - minikube
  - MicroK8s
  - K3s 
- 우리는 미니큐브를 사용해서 kubernetes 실습을 진행할 예정

#### 쿠버네티스의 컨셉 - 선언형 인터페이스와 Desired State
- 명령형 인터페이스
  - A를 이렇게 저렇게 해서 하나 만들어줘 
  - ex) 에어컨의 냉매는 어떤걸 쓰고 .. 압축한 다음.. 어떻게 순환시켜서..
- 선언형 인터페이스
  - A가 하나 있었으면 좋겠어(Desired state)
  - 작업을 일일히 명령하는 것이 아니라, 최종 결과만 선언을 해서 되게 만들어줘! 라고 선언하는 방법 

#### 쿠버네티스의 컨셉 - Master Node & Worker Node
- master/worker 역할을 하는 노드가 분리되어 있음
- kubernetes cluster는 하나 이상의 서버를 묶어서 만드는데, 클러스터를 구성하게 되면 물리적으로 여러 대의 서버가 분리되어 있어도  
  사용자 입장에서는 한번 가상화가 되어서(HW의 SW화가 됨) 여러 대의 서버를 마음껏 사용하게 됨
- master 역할을 하는 Control Plane 으로 구성
- Control Plane node는 여러개의 worker 노드를 관리하고 모니터링 하면서 client로부터 요청을 받게 되고, 요청을 받게 되면  
  해당 노드로 전달하는 역할 수행
- 요청을 받는 서버 이름이 API Server 이며, 사용자가 보낸 요청에 Key-value DB가 etcd임
- API Server 가 전달해준 요청을 실제 worker node 가 수행해야 하는데, 이러한 역할 수행하는 것이 kubelet임

### 쿠버네티스 실습 1 - YAML
#### YAML 이란?
- 데이터 직렬화에 쓰이는 포맷/양식 중 하나
- 데이터 직렬화란? 
  - 서비스 간에 Data 를 전송할 때 쓰이는 포맷으로 변환하는 작업  
    ex) 쿠버네티스 마스터에게 요청을 보낼 때 사용
  - 다른 데이터 직렬화 포맷
    - XML, JSON   
- 파일 포맷
  - `.yaml`, `.yml` 


#### YAML 특징
- 가독성
  - YAML 은 사람이 읽기 쉽도록 고안한 디자인 
- YAML 포맷
~~~YAML
apiVersion: v1
kind: Pod
metadata:
  name: example
spec:
  containers:
    - name: busybox
      image: busybox:1.25
~~~
- JSON 포맷
~~~JSON
{
  "apiVersion": "v1",
  "kind": "Pod",
  "metadata": {
    "name": "example"
  },
    "spec": {
      "containers": [
      {
        "name": "busybox", 
        "image": "busybox:1.25"
      } 
    ]
  } 
}
~~~
- Widely-use
  - kubernetes manifests 명세
  - docker compose 명세
  - ansible playbook 명세
  - github action workflow 명세 
- Strict-Validation
  - 줄 바꿈
  - 들여쓰기
    - `tab` vs `Space` 

#### YAML 문법
- Key-Value
  - Recursive 한 key-value pair 의 집합 
~~~YAML
apiVersion: v1
kind: Pod
metadata: 
  name: example
spec:
  containers:
    - name: busybox
      image: busybox:1.25
~~~
- 주석
  - `#` 를 줄의 맨 앞에 작성하면 주석 처리됨  
~~~YAML
# kubernetes pod example 입니다.
apiVersion: v1
kind: Pod
metadata:
  name: example

# 중간에 작성해도 됨
spec:
  # 여기에 주석을 달 수 있음
  containers:
    - name: busybox
      image: busybox:1.25
~~~
- 자료형 - string
~~~YAML
# 일반적인 문자열은 그냥 작성해도 되고,  따옴표로 감싸도 됨
example: this is 1st string
example: "this is 1st string"

# 반드시 따옴표로 감싸주어야 하는 경우 :
# 1) 숫자로 문자열 타입으로 지정하고 싶은 경우
example: 123
example: "123"

# y, yes, true 등의 YAML 예약어와 겹치는 경우
example: "y"

# :, {, }, ,, #, *, =, \n 등의 특수 문자를 포함한 경우
example: "a : b"
example: "a#bc*"
~~~
- 자료형 - integer
~~~YAML
# integer type
example: 123

# hexadecimal type: 0x 로 시작
example: 0x1fff
~~~
- 자료형 - float
~~~YAML
# float type
example: 99.9

# exponential type
example: 1.23e+03 # 1.23 x 10^3 = 1230
~~~
- 자료형 - boolean
~~~YAML
# true
example: true
example: yes
example: on

# False
example: false
example: no
example: off
~~~
- 자료형 - List
~~~YAML
# - 를 사용하여 list 를 명시할 수 있음
examples:
  - ex_one: 1
  - ex_two: 2

# [ ] 로 입력해도 됩니다.
examples: ["1", "2", "3"]

# list 의 원소는 어떤 자료형이든 가능합니다.
spec:
  containers:
    - name: busybox
      image: busybox:1.25
    - name: ubuntu
      image: ubuntu
      commands:
        - sleep
        - 3600
    - name: python
    - image: python:3.9 
~~~
- 자료형 - Multi-line strings
- `|` : 중간에 위치한 빈 줄을 `\n`으로 처리하며, 문자열의 맨 마지막에 `\n`을 붙임
~~~YAML
example: |
  Hello
  Fast
  Campus.
# "Hello\nFast\nCampus.\n" 으로 처리
~~~
- `>` : 중간에 위치한 빈줄을 제외하고, 문자열의 맨 마지막에 `\n`을 붙임
~~~YAML
example: >
  Hello
  Fast
  Campus.
# "Hello Fast Campus. \n" 으로 처리
~~~
- `|-`, `>-`
  - 각각 `|`, `>`와 동일하되 문자열의 맨 마지막에 `\n`이 추가되지 않음
- 자료형 - Multi-document yaml
  - `---` 라는 구분선을 통해 하나의 yaml 파일에 여러 개의 yaml document 를 작성 가능
~~~YAML
apiVersion: v1
kind: Pod
metadata:
  name: one 
---
apiVersion: v1
kind: Service
metadata:
  name: two 
---
apiVersion: v1
kind: Deployment
metadata:
  name: three
~~~
- 3 개의 yaml document 로 인식

#### Pod 의 명세를 작성한 yaml 예시
~~~YAML
# key-value pairs
apiVersion: v1
kind: Pod
metadata:
  name: example
  labels: 
    hello: bye 
spec:
  containers:
  # list
  - name: busybox
    image: busybox:1.25
    # list
    ports:
    - containerPort: 80
  - name: another-container 
    image: curlimages/curl
~~~
- 선언형 인터페이스를 위해서, Desired State 를 명시하는 용도로 사용

### 쿠버네티스 실습 2 - minikube 설치
#### Prerequisite
- References
  - minikube
    - https://minikube.sigs.k8s.io/docs/start/
  - kubectl
    - https://kubernetes.io/ko/docs/tasks/tools/install-kubectl-linux/
- 최소사양
  - CPU: 2 core 이상
  - Memory: 2GB 이상
  - Disk: 20GB 이상
  - 가상화 tool: Docker, Hyperkit, Hyper-V, ... 
- VM 스펙 업그레이드 필요
  - VM 생성 이후 demo 용 머신 우클릭 -> 설정 -> 시스템 -> 프로세서 -> cpu 3개 이상으로 변경 
- Disk: 40 GB 이상
  - VM 생성 단계에서 Disk 크기 조절 후 재생성 필요    

#### Let's Install Minikube
- minikube 의 최신 버전 (v1.22.0) 바이너리를 다운받고, 실행할 수 있도록 변경
  - 이하의 모든 커맨드는 amd 기반의 CPU를 기준으로 함
~~~shell
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

sudo install minikube-linux-amd64 /usr/local/bin/minikube
~~~
- 정상 다운로드 확인
~~~shell
minikube --help
~~~
- 터미널에 다음과 같은 메시지가 한글 or 영어로 출력된다면 정상적으로 설치된 것임
~~~shell
minikube는 개발 워크플로우에 최적화된 로컬 쿠버네티스를 제공하고 관리합니다.

Basic Commands:
  start          로컬 쿠버네티스 클러스터를 시작합니다.
  status         로컬 쿠버네티스 클러스터의 상태를 가져옵니다.
  stop           실행 중인 로컬 쿠버네티스 클러스터를 중지합니다.
  delete         로컬 쿠버네티스 클러스터를 삭제합니다. 
~~~
- minikube version 을 확인합니다.
~~~shell
minikube version
~~~


#### Let's Install Kubectl
- kubectl 은 kubernets cluster(server)에 요청을 간편하게 보내기 위해 널리 사용되는 client tool
- kubectl 은 v1.22.1 로 다운로드 
~~~shell
curl -LO https://dl.k8s.io/release/v1.22.1/bin/linux/amd64/kubectl
~~~
- kubectl 바이너리를 사용할 수 있도록 권한과 위치를 변경함
~~~shell
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
~~~
- 정상적으로 설치되었는지 확인
~~~shell
kubectl --help
~~~
- 터미널에 다음과 같은 메세지가 한글 or 영어로 출력된다면 정상적으로 설치된 것
~~~shell
kubectl controls the Kubernetes cluster manager.
Find more information at: https://kubernetes.io/docs/reference/kubectl/overview/
Basic Commands (Beginner):
  create        Create a resource from a file or from stdin
  expose        Take a replication controller, service, deployment or pod and
expose it as a new Kubernetes service
  run           Run a particular image on the cluster
  set           Set specific features on objects
~~~
- kubectl version 을 확인
~~~shell
kubectl version
~~~
- 터미널에 다음과 같은 메세지가 한글 or 영어로 출력된다면 정상적으로 설치된 것임
~~~shell
Client Version: version.Info{Major:"1", Minor:"22", GitVersion:"v1.22.1", GitCommi t:"632ed300f2c34f6d6d15ca4cef3d3c7073412212", GitTreeState:"clean", BuildDate:"202 1-08-19T15:45:37Z", GoVersion:"go1.16.7", Compiler:"gc", Platform:"linux/amd64"} The connection to the server localhost:8080 was refused - did you specify the righ t host or port?
~~~
- `The connection to the server localhost:8080 was refused - did you specify the
right host or port?` 메세지는 에러를 의미하는 것이 맞음
- 하지만 `kubectl version` 은 client의 버전과 kubernetes server 의 버전을 모두 출력하는 명령어이며, 현재 kubernetes server 를 생성하지 않았기 때문에 client 의 버전만 정상적으로 출력

#### Minikube 시작하기
- minikube start 
  - minikube 를 docker driver 를 기반으로 하여 시작  
~~~shell
minikube start --driver=docker
~~~
- 필요한 docker image 들을 다운받게 되고, 다운로드가 완료되면 이를 기반으로 minikube 를 구동
- 정상적으로 `minikube start`가 완료되면 다음과 같은 메세지가 출력됨
- minikube status
  - 정상적으로 생성되었는지 minikube 의 상태 확인
~~~shell
minikube status
~~~
- 터미널에 다음과 같은 메세지 출력되어야 함
~~~shell
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
~~~

#### kubectl get pod -n kube-system
- kubectl 을 사용하여 minikube 내부의 default pod 들이 정상적으로 생성되었는지 확인
~~~shell
kubectl get pod -n kube-system
~~~
- 터미널에 다음과 같은 메세지가 출력되어야 함
~~~shell
NAME
READY   STATUS    RESTARTS   AGE
1/1     Running   0         3m40s
1/1     Running   0         3m46s
1/1     Running   0         3m46s
1/1     Running   0         3m53s
1/1     Running   0         3m40s
1/1     Running   0         3m46s
1/1     Running   1         3m51s
~~~

#### Minikube 삭제하기
- minikube delete
   - 다음 명령어로 간단하게 삭제 가능
~~~shell
minikube delete
~~~


### 쿠버네티스 - POD
#### POD 란? 
- Pod(파드)는 쿠버네티스에서 생성하고 관리할 수 있는 배포 가능한 가장 작은 컴퓨팅 단위
  - https://kubernetes.io/ko/docs/concepts/workloads/pods
- 쿠버네티스는 Pod 단위로 스케줄링, 로드벨런싱, 스케일링 등의 관리 작업 수행
  - 쿠버네티스에 어떤 어플리케이션을 배포하고 싶다면, 최소 Pod 으로 구성해야 한다는 의미 
- 조금 어렵다면 Pod 는 Container를 감싼 개념이라고 생각할 수 있음
  - 하나의 Pod 는 한 개의 Container 혹은 여러 개의 Container로 이루어져 있을 수 있음 
  - Pod 내부의 여러 Container 는 자원을 공유함
- Pod는 Stateless 한 특징을 가지고 있으며, 언제든지 삭제될 수 있는 자원이라는 점


#### Pod 생성
- 간단한 Pod의 예시
~~~shell
apiVersion: v1 # kubernetes 의 resource이 API version
kind: Pod      # kubernetes resource name
metadata: # 메타 데이터 : name, namespace, labels, annotations 등을 포함
  name: counter
spec:     # 메인 파트 : resource 의 desired state 를 명시
  containers:
  - name: count      # container 의 이름
    image: busybox   # container 의 image
    args: [/bin/sh, -c, 'i=0; while true; do echo "$i: $(date)"; i=$((i+1)); sleep 1; done']
    # 해당 image 의 entrypoint 의 args 로 입력하고 싶은 부분
~~~
- 위의 스펙대로 Pod 하나 생성
~~~shell
vi pod.yaml # 위의 내용을 복사 붙여넣기
kubectl apply -f pod.yaml
~~~
- `kubectl apply -f <yaml-file-path>` 를 수행하면, `<yaml-file-path>`에 해당하는  
  kubernetes resource 를 생성 또는 변경할 수 있음
  - kubernetes resource 의 desired state 를 기록해놓기 위해 항상 YAML 파일을 저장하고, 버전 관리하는 것을 권장
  - `kubectl run` 명령어로 YAML 파일 생성 없이 pod를 생성할 수도 있지만, 이는 kubernetes 에서 권장하는 방식은 아니므로 생략
- 생성한 Pod 의 상태 확인  
~~~shell
kubectl get pod
# ContainerCreating

kubectl get pod
# 시간이 지난 후 Running 으로 변하는 것을 확인 가능
~~~

#### Pod 조회
- 방금 current namespace 의 Pod 목록을 조회하는 명령 수행
  - 조회 결과는 Desired state 가 아닌, Current State를 출력 
~~~shell
kubectl get pod
~~~
- namespace 란?
  - namespace 는 kubernetes 에서 리소스를 격리하는 가상의 단위 
  - `kubectl config view --minify | grep namespace:` 로 current namespace 가 
    어떤 namespace 로 설정되었는지 확인할 수 있음
  - 따로 설정하지 않았다면 `default` namespace 가 기본으로 설정되어 있을 것임
- 특정 namespace 혹은 모든 namespace 의 pod 를 조회할 수 있음
~~~shell
kubectl get pod -n kube-system
# kube-system namespace 의 pod 를 조회

kubectl get pod -A
# 모든 namespace 의 pod 조회
~~~
- pod 하나를 조회하는 명령어는 다음과 같음
  - `<pod-name>`에 해당하는 pod 조회
~~~shell
kubectl get pod <pod-name>
~~~
- pod 하나를 조금 더 자세히 조회하는 명령어는 다음과 같음 
  - <pod-name> 에 해당하는 pod 을 자세히 조회
~~~shell
kubectl describe pod <pod-name>
~~~
- 기타 유용한 명령을 소개
~~~shell
kubectl get pod -o wide
# pod 목록을 보다 자세히 출력

kubectl get pod <pod-name> -o yaml
# <pod-name>을 yaml 형식으로 출력

kubectl get pod -w
# kubectl get pod 의 결과를 계속 보여주며, 변화가 있을 때만 업데이트 수행
~~~

#### Pod 로그
- pod의 로그를 확인하는 명령어는 다음과 같음
~~~shell
kubectl logs <pod-name>

kubectl logs <pod-name> -f
# <pod-name> 의 로그를 계속 보여줌
~~~
- pod 안에 여러 개의 container 가 있는 경우에는 다음과 같음
~~~shell
kubectl logs <pod-name> -c <container-name>

kubectl logs <pod-name> -c <container-name> -f
~~~

#### Pod 내부 접속
- pod 내부에 접속하는 명령어는 다음과 같음
~~~shell
kubectl exec -it <pod-name> -- <명령어>
~~~
- pod 안에 여러 개의 container 가 있는 경우에는 다음과 같음
~~~shell
kubectl exec -it <pod-name> -c <container-name> -- <명령어>
~~~
- docker exec 와 비슷한 명령임을 확인

#### Pod 삭제
- pod 를 삭제하는 명령어는 다음과 같음
~~~shell
kubectl delete pod <pod-name>
~~~
- 혹은 다음과 같이 리소스 생성시, 사용한 YAML 파일을 사용해 삭제 가능
~~~shell
kubectl delete -f <YAML-파일-경로>
~~~
- 위 명령어는 꼭 pod 이 아니더라도 모든 kubernetes resource 에 적용 가능


### 쿠버네티스 - Deployment
#### Deployment 란 ? 
- Deployment는 Pod와 Replica-set에 대한 관리를 제공하는 단위
  - https://kubernetes.io/ko/docs/concepts/workloads/controllers/deployment/
- 관리라는 의미는 Self-healing, Scaling, Rollout(무중단 업데이트) 과 같은 기능을 포함
- 조금 어렵다면 Deployment 는 Pod 을 감싼 개념이라고 생각할 수 있음
  - Pod 을 Deployment 로 배포함으로써 여러 개로 복제된 Pod, 여러 버전의 Pod 을 안전하게 관리할 수 있음  


#### Deployment 생성
- 간단한 Deployment 의 예시
~~~shell
apiVersion: apps/v1   # kubernetes resource API Version
kind: Deployment      # kubernetes resoure name
metadata:             # meta-data : name, namespace, labels, annotation 등
  name: nginx-deployment
  labels:
    app: nginx
spec:                 # main part : resource 의 desired state 를 명시
  replicas: 3         # 동일한 template 의 pod 를 3 개 복제본으로 생성
  selector:
    matchLabels:
      app: nginx
  template:           # Pod 의 template 을 의미
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx          # container 의 이름
        image: nginx:1.14.2  # container 의 image
        ports:
        - containerPort: 80  # container 의 내부 Port
~~~
- 위의 스펙대로 Deployment 를 하나 생성
~~~shell
vi deployment.yaml
# 위의 내용을 복사 후 붙여넣음

kubectl apply -f deployment.yaml
~~~

#### Deployment 조회
- 생성한 Deployment 의 상태를 확인
~~~shell
kubectl get deployment
# 다음과 같은 메세지가 출력
# NAME             READY UP-TO-DATE AVAILABLE   AGE 
# nginx-deployment  0/3      3          0       10s 

kubectl get deployment, pod
~~~
- 시간이 지난 후, deployment 와 함께 3 개의 pod 이 생성된 것을 확인할 수 있음
~~~shell
kubectl describe pod <pod-name>
~~~
- pod 의 정보를 자세히 조회하면 `Controlled By`로 Deployment 에 의해 생성되고 관리되고 있는 것을 확인 가능


#### Deployment Auto-healing
- pod 하나를 삭제해보겠습니다
~~~shell
kubectl delete pod <pod-name>
~~~
- 기존 pod 이 삭제되고, 동일한 pod 이 새로 하나 생성된 것을 확인할 수 있음
~~~shell
kubectl get pod
~~~

#### Deployment Scaling
- replica 개수를 늘려보겠습니다
~~~shell
kubectl scale deployment/nginx-deployment --replicas=5
kubectl get deployment 
kubectl get pod
~~~
- replica 개수를 줄여보겠습니다
~~~shell
kubectl scale deployment/nginx-deployment --replicas=1
kubectl get deployment
kubectl get pod
~~~

#### Deployment 삭제
- deployment 를 삭제
~~~shell
kubectl delete deployment <deployment-name>
kubectl get deployment
kubectl get pod
~~~
- Deployment 의 Control 을 받던 pod 역시 모두 삭제된 것을 확인할 수 있음
- 혹은 `-f` 옵션으로 YAML 파일을 사용해서 삭제할 수도 있음
~~~shell
kubectl delete -f <YAML-파일-경로>
~~~

### 쿠버네티스 - Service
#### Service 란?
- Service 는 쿠버네티스에 배포한 애플리케이션(Pod)를 외부에서 접근하기 쉽게 추상화한 리소스
  - https://kubernetes.io/ko/docs/concepts/services-networking/service/
- Pod는 IP 를 할당받고 생성되지만, 언제든지 죽었다가 다시 살아날 수 있으며, 그 과정에서 IP는 항상 재할당받기에 고정된 IP로 원하는 Pod에 접근할 수는 없음
- 따라서 클러스터 외부 혹은 내부에서 Pod에 접근할 때는, Pod의 IP가 아닌 Service 를 통해서 접근하는 방식을 거침
- Service 는 고정된 IP를 가지며, Service는 하나 혹은 여러 개의 Pod와 매칭
- 따라서 클라이언트가 Service 의 주소로 접근하면, 실제로는 Service 에 매칭된 Pod에 접속할 수 있게 됨

#### Service 생성
- 지난 시간에 생성한 Deployment 를 다시 생성
~~~shell
kubectl apply -f deployment.yaml
~~~
- 생성된 Pod의 IP를 확인하고 접속 시도
~~~shell
kubectl get pod -o wide
# Pod 의 IP 를 확인

curl -X GET <POD-IP> -vvv
ping <POD-IP>
# 통신 불가능
~~~
- 할당된 <POP-IP> 는 클러스터 내부에서만 접근할 수 있는 IP 이기 때문에 외부에서는 Pod에 접속 불가능
- minikube 내부로 접속하면 통신이 되는지 확인
~~~shell
minikube ssh
# minikube 내부로 접속

curl -X GET <POD-IP> -vvv
ping <POD-IP>
# 통신 가능
~~~
- 그럼 이제 위의 Deployment 를 매칭시킨 Service 를 생성해보자
~~~shell
apiVersion: v1
kind: Service
metadata:
  name: my-nginx
  labels:
    run: my-nginx
spec:
  type: NodePort # Service 의 Type 을 명시하는 부분
  ports:
  - port: 80
    protocol: TCP
  selector:      # 아래 label 을 가진 Pod 를 매핑하는 부분
    app: nginx
~~~
- Service 를 생성
~~~shell
vi service.yaml
# 파일을 열어 위의 내용을 복사 붙여넣기 함

kubectl apply -f service.yaml

kubectl get service 
# PORT 80:<PORT> 숫자 확인

curl -X GET $(minikube ip):31971
# 클러스터 외부에서도 정상적으로 pod 에 접속할 수 있는 것을 확인
~~~
- NodePort 를 사용하면, node의 IP 를 그대로 사용하되, PORT 는 다르게 사용하는 방식이라고 기억
- *Service 의 Type 이란? 
  - <b>NodePort</b> 라는 type 을 사용했기 때문에, minikube 라는 kubernetes cluster 내부에 배포된 서비스에 클러스터 외부에서 접근할 수 있었음 
    - 접근하는 IP는 pod 가 떠있는 노드(머신)의 IP를 사용하고, Port는 할당받은 Port를 사용 
  - <b>LoadBalancer</b> 라는 type을 사용해도, 마찬가지로 클러스터 외부에서 접근할 수 있지만, LoadBalancer 를 사용하기 위해서는 LoadBalancing 역할을 하는 묘듈이 추가적으로 필요
  - <b>ClusterIP</b> 라는 type 은 고정된 IP, PORT를 제공하지만, 클러스터 내부에서만 접근할 수 있는 대역의 주소가 할당됨. 해당 주소로는 외부에서 접근 불가능
  - 실무에서는 주로 kubernetes cluster 에 MetalLB와 같은 LoadBalancing 역할을 하는 모듈을 설치한 후, <b>LoadBalancer</b> type 으로 서비스를 expose 하는 방식을 사용
    - NodePort 는 Pod 가 어떤 Node 에 스케줄링될 지 모르는 상황에서, Pod 가 할당된 후 해당 Node 의 IP 를 알아야 한다는 단점이 존재

### 쿠버네티스 - PVC
#### PVC 란 ? 
- Persistent Volume(PV), Persistent Volume Claim(PVC)는 stateless 한 Pod 에 영구적으로(persistent) 데이터를 보존하고 싶은 경우 사용하는 리소스
- 도커에 익숙한 경우 `docker run`의 `-v` 옵션인 도커 볼륨과 유사한 역할을 한다고 이해 할 수 있음 
- PV는 관리자가 생성한 실제 저장 공간의 정보를 담고 있고, PVC는 사용자가 요청한 저장 공간의 스펙에 대한 정보를 담고 있는 리소스
- Pod 내부에서 작성한 데이터는 기본적으로 언제든지 사라질 수 있기에, 보존하고 싶은 데이터가 있다면 Pod에 PVC를 Mount 해서 사용해야 한다는 것만 기억
- PVC를 사용하면 여러 pod 간 data 공유도 쉽게 가능

#### PVC 생성
- minikube 를 생성하면, 기본적으로 minikube 와 함께 설치되는 storageclass 가 존재함
  - `kubectl get storageclass` 를 통해 이미 설치된 storageclass 를 확인
  - PVC 를 생성하면 해당 PVC 의 스펙에 맞는 PV를 그 즉시 자동으로 생성해준 뒤, PVC와 매칭시켜준다고만 이해하면 됨(dynamic provisioning 지원하는 storageclass)   
- PVC 생성
~~~shell
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:               # pvc 정보 입력
  accessModes:
    - ReadWriteMany # ReadWriteOnce, ReadWriteMany 옵션 선택
  volumeMode: Filesystem
  resources:
    requests:
      storage: 10Mi           # storage 용량 설정
  storageClassName: standard  # 방금 전에 확인한 storageclass의 name 입력
~~~
~~~shell
vi pvc.yaml
kubectl apply -f pvc.yaml

kubectl get pvc,pv
# pvc 와 동시에 pv 까지 함께 생성된 것을 확인 가능
~~~

#### Pod 에서 PVC 사용
- Pod 를 생성
  - volumeMounts, volumes 부분이 추가됨 
~~~shell
apiVersion: v1 
kind: Pod      
metadata: 
  name: mypod
spec:     
  containers:
  - name: myfrontend 
    image: nginx
    volumeMounts:
    - mountPath: "/var/www/html" # mount 할 pvc 를 mount 할 pod 의 경로 작성
      name: mypd # 어떤 이름이든 상관없으나, 아래 volumes[0].name 과 일치해야 함
  volumes:
    - name: mypd # 어떤 이름이든 상관없으나, 위의 volumeMounts[0].name 과 일치해야 함
      persistentVolumeClaim:
        claimName: myclaim    # mount 할 pvc 의 name 을 적음
~~~
~~~shell
vi pod-pvc.yaml

kubectl apply -f pod-pvc.yaml
~~~
- pod 에 접속하여 mount 한 경로와 그 외의 경로에 파일 생성
~~~shell
kubectl exec -it mypod -- bash
touch hi-fast-campus
cd /var/www/html
touch hi-fast-campus
~~~
- pod 를 삭제
~~~shell
kubectl delete pod mypod
~~~
- pvc 는 그대로 남아있는지 확인
~~~shell
kubectl get pvc,pv
~~~
- 해당 pvc 를 mount 하는 pod 를 다시 생성
~~~shell
kubectl apply -f pod-pvc.yaml
~~~
- pod 에 접속하여 아까 작성한 파일들이 그대로 있는지 확인
~~~shell
kubectl exec -it mypod -- bash

ls
# hi-fast-campus 파일이 사라진 것을 확인 
cd /var/www/html

ls 
# hi-fast-campus 파일이 그대로 보존되는 것을 확인
~~~


### 리눅스 명령어 참고
- `curl` : 사용자 상호 작용 없이 작동하도록 설계된 서버에서 또는 서버로 데이터를 전송하기 위한 명령줄 유틸리티
  - 리눅스에서 curl 이라는 http 메시지를 쉘상에서 요청하여 결과를 확인하는 명령어
  - curl 명령어는 http를 이용하여 경로의 데이터를 가져옴
  - `curl [옵션][URL...]`
  - POST 메소드 사용
    - `curl -d "req=12312" "http://102.168.0.222:8080/service_CHOA.jsp"`
  - GET 메소드 사용  
    - `curl "http://102.168.0.222:8080/service.jsp?req=7777"` 
  - 문서 or 파일을 서버에서 가져옴
    - 지원 프로토콜은 HTTP, HTTPS, FTP, FILE, IMAP, GOPHER, DICT, TELNET, LDAP 등 

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
- `usermod`
  - 사용자 계정에 대한 다양한 정보들을 변경하는 명령어
  - root 계정만 사용 가능 
  - 사용자가 누구누구 있는지 관리파일을 확인하고 싶으면 /etc/passwd 파일을 확인해 보면 됨
  - 사용자 ID 변경할 때 --> `usermod -l <새로운계정> <기존계정>`
- busybox
  - 리눅스 상에서 자주 사용되는 명령어들만 모은 압축파일

#### 리눅스 vi 에디터 사용법 정리
- 명령모드와 입력모드의 차이가 있음
- <b>입력모드</b>는 메모장처럼 텍스트를 자유롭게 편집하는 모드이며, 명령모드는 다양한 명령을 내리는 모드
- 명령모드에서 입력모드로 전환
  - a: 커서 다음(오른쪽)에 입력
  - A: 행 마지막 부분에 입력
  - i: 커서 앞(왼쪽)에 입력
  - l: 행 처음 부분에 입력
  - o: 커서 밑에 빈 행을 추가하여 입력
  - O: 커서 위에 빈 행을 추가하여 입력
  - s: 커서에 있는 글자를 지우고 입력
- 입력모드에서 명령모드로 전환
  - ESC 키 누름 
- 저장, 종료하기
  - 명령모드에서 :(콜론)을 이용하여 다양한 작업 가능 
  - `:q` : 종료
  - `:q!` : 저장하지 않고 강제 종료
  - `:w` : 저장
  - `:wq`: 저장하고 종료
  - `:wq 파일이름` : 저장할 때 파일이름 지정 가능
- 커서 이동
  - `w`: 다음 단어의 첫 글자로 이동
  - `b`: 이전 단어의 첫 글자로 이동
  - `G`: 마지막 행으로 가기
  - `:숫자`: 지정한 숫자 행으로 이동. ex) :5 
- 삭제
  - `x`: 커서에 있는 글자 삭제
  - `X`: 커서 앞에 있는 글자 삭제 
  - `dw`: 커서를 기준으로 뒤에 있는 단어 글자 삭제
  - `db`: 커서를 기준으로 앞에 있는 단어 글자 삭제
  - `dd`: 커서가 있는 라인(줄) 삭제
- 복사
  - `yw`: 커서를 기준으로 뒤에 있는 단어 글자 복사(커서 포함)
  - `yb`: 커서를 기준으로 앞에 있는 단어 글자 복사
  - `yy`: 커서가 있는 라인(줄) 복사
- 붙여넣기
  - `p`: 커서 다음에 붙여넣기
  - `P`: 커서 이전에 붙여넣기
- 찾기
  - `/문자열`: 앞에서 부터 문자열을 찾음
  - `?문자열`: 뒤에서 부터 문자열을 찾음
  - `n`: 뒤로 검색
  - `N`: 앞으로 검색 
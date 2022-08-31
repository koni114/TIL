# chapter02_6 개발환경 구축하기
## 나의 개발환경 구축하기
- 개발언어
  - C
  - Python
  - Java
- 개발 환경 설정하기
  - 버전 선택/확인을 위한 각종 유틸리티
    - alternates, which, whereis
  - anaconda
  - docker
- 개발 도구 설정하기(IDE)
  - jupyter notebook

## C 언어 컴파일 환경 구축하기
~~~shell
$ apt install build-essential  # 설치되어 있음
$ apt install binutils         # 설치되어 있음

# 아래 명령어가 기본적으로 적용되는 것을 확인할 수 있음
$ gcc
$ g++
$ make

# 버전 확인
$ gcc --version
$ g++ --version
$ make --version
~~~
- `apt show` 를 통해 해당 패키지 설치시 depends 패키지가 어떤 것들이 있는지 확인 가능
~~~shell
$ apt show build-essential

Package: build-essential
Version: 12.8ubuntu1.1
Priority: optional
Build-Essential: yes
Section: devel
Origin: Ubuntu
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Original-Maintainer: Matthias Klose <doko@debian.org>
Bugs: https://bugs.launchpad.net/ubuntu/+filebug
Installed-Size: 21.5 kB
Depends: libc6-dev | libc-dev, gcc (>= 4:9.2), g++ (>= 4:9.2), make, dpkg-dev (>= 1.17.11)
Task: ubuntu-mate-core, ubuntu-mate-desktop
Download-Size: 4664 B
APT-Manual-Installed: yes
APT-Sources: http://archive.ubuntu.com/ubuntu focal-updates/main amd64 Packages
Description: Informational list of build-essential packages
~~~
- `dpkg -L [패키지명]` 을 통해서 바이너리 파일이 어디 어떻게 설치가 되어있는지 확인 가능
~~~shell
$ dpkg -L binutils

/.
/usr
/usr/bin
/usr/lib
/usr/lib/compat-ld
/usr/lib/gold-ld
/usr/lib/x86_64-linux-gnu
/usr/share
/usr/share/bug
/usr/share/bug/binutils
/usr/share/bug/binutils/presubj
/usr/share/doc
/usr/share/doc/binutils
...
~~~
- 간단하게 c 코드를 컴파일해보자. 아래 코드를 hello.c 에 저장
~~~shell
$ vi hello.c
~~~
~~~shell
# hello.c
#include <stdio.h>
int main() {
    printf("hello world!");
}
~~~
~~~shell
$ gcc -o hello hello.c
$ ./hello
hello world!
~~~

## python 환경 구축하기
- 기본적으로 linux 에는 python2, python3 가 설치되어 있음
- 주의해야할 점은 python3 는 자유롭게 설치하거나 해도 상관없지만, python2 를 삭제하는 경우에는 시스템에 영향을 줄 수 있으므로 왠만하면 건들지 말자
~~~shell
$ apt install pip
$ apt install python3
~~~
### anaconda 설치
~~~shell
# curl 를 통해 설치 
$ curl -O https://repo.anaconda.com/archive/Anaconda-1.4.0-Linux-x86_64.sh

# 용량이 부족할 수 있으므로, 확인 필요
$ df -h | grep /dev/sd

Filesystem      Size  Used Avail Use% Mounted on
overlay          59G  8.2G   48G  15% /
tmpfs            64M     0   64M   0% /dev
shm              64M     0   64M   0% /dev/shm
/dev/vda1        59G  8.2G   48G  15% /etc/hosts
tmpfs           786M   72K  786M   1% /run
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           786M     0  786M   0% /run/user/1000

# 해당 파일이 binary file 임을 확인
$ file Anaconda-1.4.0-Linux-x86_64.sh
Anaconda-1.4.0-Linux-x86_64.sh: Bourne-Again shell script executable (binary data)

# shell 을 실행시켜 설치. 둘 중에 하나 선택하여 설치하면 됨
$ bash Anaconda-1.4.0-Linux-x86_64.sh
$ sh Anaconda-1.4.0-Linux-x86_64.sh

# /root/anaconda/bin 에 자동 설치됨
# -b 옵션을 주면 질문을 받지 않고 자동으로 설치해줌
$ bash Anaconda-1.4.0-Linux-x86_64.sh -b

# anaconda 초기화 수행
$ bin/conda init

# 초기화 시킨 것을 읽기 위하여 수행
$ source ~/.bashrc

# conda 가상환경 생성
$ conda create --name my_env35 --name my_env35 python=3.5

# conda 가상환경 실행
$ conda activate my_env35 

(my_env35) root@ubuntu:~# python --version

# conda 가상환경 빠져나오기
$ conda deactivate
~~~

## 주피터 노트북 설치
~~~shell 
# 주피터 노트북 데몬 실행
$ jupyter notebook --allow-root --ip=0.0.0.0 --no-browser

# 주피터 노트북 암호 생성
$ jupyter notebook password

# 주피터 노트북 설정 파일 만들기
$ jupyter notebook --generate-config
$ jupyter notebook --allow-root --config=~/.jupyter/jupyter_notebook_config.py --no-browser

# 터미널이 닫혀도 백그라운드에서 실행되는 프로세스로 실행하기
$ nohup jupyter notebook &
~~~

### Jupyter notebook 을 부팅 서비스로 만들어 자동 실행하기
- root 계정으로 container 에서 실행하려면 
~~~shell
$ sudo vi /lib/systemd/system/jupyter.service
~~~
~~~shell
# jupyter.service
[Unit]
Description=Jupyter Notebook Server

[Service]
Type=simple
PIDFile=/run/jupyter.pid
ExecStart=/data/anaconda/bin/jupyter-notebook --allow-root --config=/home/<username>/.jupyter/jupyter_notebook_config.py
WorkingDirectory=/data/anaconda
User=<username>
Group=<username>
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
~~~
- ~/.jupyter/ 디렉토리에 `jupyter_notebook_config.py` 설정 파일 수정
~~~shell
c.NotebookApp.ip='*'
c.NotebookApp.notebook_dir='/data/workspace'
c.NotebookApp.open_browser=False
~~~
- service 등록 후 서비스 실행
~~~shell
$ systemctl daemon-reload
$ systemctl enable jupyter
$ systemctl start jupyter
$ systemctl status jupyter
~~~

## java 개발 환경 구축하기
- JRE, JDK 설치
~~~shell
$ apt show default-jdk   # default 로 jdk 11 이 설치됨
$ sudo apt install default-jdk
~~~ 
- jdk 12 를 별도로 설치해보자
~~~shell
$ mkdir /data
$ cd /data
$ curl -O https://download.java.net/java/GA/jdk12.0.2/e482c34c86bd4bf8b56c0b35558996b9/10/GPL/openjdk-12.0.2_linux-x64_bin.tar.gz
$ tar xvfz openjdk-12.0.2_linux-x64_bin.tar.gz
~~~

### 개발도구 버전관리 유틸리티 - which, whereis
~~~shell
$ which gcc
$ which python
$ which java

$ whereis gcc
$ whereis python
$ whereis java
~~~
- `ls -al /usr/bin/java*` 명령어를 통해 java를 확인해보면, /etc/alternatives 를 통해 실행되는 것을 확인 할 수 있음

### 다중 java version 관리
~~~shell
$ update-alternatives --list java  # java version 확인
$ ls -al /usr/bin/java
$ ls -al /etc/alternatives/java*
~~~
- 신규 버전 등록
~~~shell
# jdk 12 버전 등록 
$ update-alternatives --install "/usr/bin/java" "java" "/data/jdk-12.0.2/bin/java" 1  
$ update-alternatives --install "/usr/bin/javac" "javac" "/data/jdk-12.0.2/bin/javac" 1  

# update-alternatives 명령어로 java version 변경
$ update-alternatives --config java
$ update-alternatives --config javac
~~~

## docker 환경 구성하기
### 설치 방법 - 1 ubuntu 에서 공식적으로 지원하는 docker 설치
- ubuntu 버전이 16.04인 경우는 docker 최신 버전이 지원되지 않음. 따라서 2, 3번 방법을 사용하여 설치해야 함
~~~shell
$ apt search docker.io
$ apt install docker.io
~~~

### 설치 방법 - 2 docker의 repo 를 이용해 third-party repo 를 추가, 설치하는 방법
- 공식적인 우분투 repo가 아닌 docker의 repo 를 이용해 third-party repo 를 추가하고 설치하는 방법
- 이는 인증서(apt-key) 를 받아 반영한 후 docker-ce, docker-cel-cli 를 설치하면 됨
~~~shell
$ add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ apt-key fingerprint 0EBFCD88
$ apt update
$ apt install docker-ce-ce-cli
~~~

### 설치 방법 - 3 자동 설치 스크립트를 docker site에서 받아 shell 실행
- 공식 사이트로부터 자동 설치 스크립트를 다운로드 받아 설치
~~~shell
# -fs : 에러 발생시 출력하지 않고 넘어가기 위한 옵션
# -L : 대문자 L로 location을 지정  
$ curl -fsSL https://get.docker.com | sudo sh

# sudo 라는 root 권한으로 실행하기 불편하므로, 사용자를 docker group 에 추가하면 안해도 됨.
$ sudo usermod -a -G docker user1 # 다시 로그인해야 그룹권한이 부여됨.
~~~
### docker 이미지/컨테이너 디렉토리 변경 
- docker 기본적으로 root 디렉토리 아래에서 image 파일을 받아서 동작함.
- 해당 파일이 저장되는 위치를 변경해보자
~~~shell
$ sudo lsof | grep /var/lib/docker
$ sudo systemctl stop docker
~~~
- 디렉토리 변경 설정파일 추가
~~~shell
$ sudo vi /lib/systemd/system/docker.service
$ ExecStart=...--data-root=/data/docker_dir
~~~
- 기존 도커 디렉토리 용량 확인
~~~shell
$ sudo su -sh /var/lib/docker
~~~
- 도커 재시작
~~~shell
$ sudo systemctl start docker
~~~
- 변경된 디렉토리 용량 확인
~~~shell
$ sudo du -sh /data/docker_dir
~~~
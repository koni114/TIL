# 컨테이너 첫걸음
## hello-world 실행
- `docker run hello-world` 명령어 실행을 하면 다음과 같이 4가지 process가 진행
  - 도커 클라이언트가 도커 데몬에 접속  
    데몬을 **도커 엔진** 이라고 부르기도 함
  - 도커 데몬이 `hello-world` 이미지를 도커 허브에 다운로드 받음(amd64)
  - 다운로드 받은 이미지를 바탕으로 컨테이너 생성.  
    컨테이너상의 프로세스가 메세지를 표준 출력에 쓰기 시작함
  - 도커 데몬이 출력을 도커 클라이언트에게 보내면 터미널에 전달됨

### 용어 체크
- **이미지** : 운영체제와 소프트웨어를 담고 있는 컨테이너 실행 이전 상태  
  이미지는 `리포지터리:태그` 로 식별
- **리포지터리** : 이미지 보관소. 리포지터리의 이름에 버전 등을 의미하는 태그를 붙여서 각각의 이미지를 구별하여 보관 가능  
  태그를 생략하면 latest 가 사용됨
- **레지스트리** : 도커에서는 리포지터리 집합체로서 리포지터리를 제공하는 서버를 말함

## 컨테이너의 생명 주기와 도커 커맨드
![img](https://github.com/koni114/TIL/blob/master/docker/img/docker_08.jpeg)
    
### 이미지 다운로드)(`docker pull`)
- 원격 리포지터리로부터 이미지를 다운로드함
 
### 컨테이너 실행(`docker run`)
- docker run [옵션] 리포지터리명:태그 [커맨드] [인자] 는 지정한 이미지를 모형으로 컨테이너 기동
- 지정한 이미지를 모형으로 컨테이너 기동. 로컬에 없으면 default로 docker hub에서 다운로드 받음. 클라우드에서 제공하는 프라이빗 레지스트리 서비스를 이용할수도 있음

| 옵션  | 특징  |
| --- | --- |
| -i  | 키보드 입력을 컨테이너의 표준 입력에 연결하여 키보드 입력을 컨테이너의 셸 등에 보냄 |
| -t  | 터미널을 통해 대화형 조작이 가능하게 함 |
| -d  | 백그라운드로 컨테이너를 돌려 터미널과 연결하지 않음 |
| --name | 컨테이너에 이름을 설정. 시스템에서 유일한 이름이어야 하며, 옵션을 생략하면 자동으로 만들어진 이름이 부여됨 |
| --rm | 컨테이너가 종료하면 종료 상태의 컨테이너를 자동으로 삭제 |

### 컨테이너의 상태 출력(`docker ps`)
- `docker ps [옵션] 은 실행 중이거나 정지 상태에 있는 컨테이너 목록을 출력
- 옵션을 생략한 경우에는 실행 중인 컨테이너만 출력하며 `-a` 를 추가하면 정지 상태인 컨테이너도 출력됨
- `STATUS`가 `Exit(0)`이면 정상 종료됐음을 확인할 수 있음

### 로그 출력(docker logs)
- 정지 상태인 컨테이너는 삭제될 때까지 남아 있으며, 실행 중 발생한 표준 출력과 표준 에러 출력을 간직하고 있음
- 명령어 `docker logs [옵션] 컨테이너ID | 컨테이너명` 으로 확인 가능
- 옵션 `-f` 를 사용하면 실시간으로 발생하는 로그 확인 가능

### 컨테이너 정지(docker stop, docker kill)
- 실행 중인 컨테이너를 정지하는 방법은 다음과 같이 3가지 방법이 있음
  - 컨테이너 `PID=1`인 프로세스가 종료 
  - `docker stop 컨테이너 ID | 컨테이너명` 을 실행
  - `docker kill 컨테이너 ID | 컨테이너명` 을 실행
- `docker run hello-world` 를 통해 이미지를 별다른 커맨드 지정 없이 실행하였고, 실행하자마자 바로 종료되는데, 그 이유는 PID=1인 셸이 종료했기 때문
- 아래 예에서는 컨테이너를 기동할 때 커맨드로 셸을 지정. PID 값이 1인 bash가 기동되었음을 ps 명령어를 통해 확인한 후 exit를 입력하여 컨테이너 종료
~~~linux
$ docker run -it --name test1 hello-world bash
root@1badd7e4f51c: /# ps -ax
root@1badd7e4f51c: exit
$ docker ps -a
# 해당 process 가 종료됨을 확인 가능
~~~
- 행 중인 컨테이너를 다른 터미널에서 `docker stop` 명령어로 정지시킬 수 있음
- 실행 중이던 컨테이너는 `exit`을 출력하면서 종료되고 호스트의 프롬포트로 돌아옴
- 이처럼 실행중인 컨테이너를 다른 터미널에서 정지시킬수도 있음   
  예를 들어 컨테이너 내의 프로세스가 비정상적인 상태에 빠져 강제 종료(ctrl+c)로 정지할 수 없는 경우 등
- 별도의 터미널에서는 `docker kill`을 실행하여 컨테이너를 정지시키고 있음  
  이는 강제종료 한 것이며, `docker ps -a` 수행 시, `STATUS(137)` 로 종료된 것으로 나옴  
  이는 `docker stop`을 할 수 없는 경우에만 사용하는 것이 좋음

### 컨테이너 재기동(docker start)
- 정지 상태인 컨테이너는 `docker start [옵션] 컨테이너 ID | 컨테이너명` 으로 재기동 가능
- 옵션으로 `-i` 를 붙이면 컨테이너가 터미널의 입력을 받아 표준 출력과 표준 에러를 터미널에 표시
~~~shell
docker start -i 0599550eaedb

[root@0599550eaedb /]#  --> docker container process 안으로 들어옴
~~~
~~~
$ docker ps 
CONTAINER ID   IMAGE      COMMAND       CREATED         STATUS              PORTS     NAMES
0599550eaedb   centos:7   "/bin/bash"   3 minutes ago   Up About a minute             test1
~~~

### 컨테이너의 변경 사항을 리포지터리에 저장(docker commit)
- 기동한 컨테이너의 리눅스에서도 가상 서버에서처럼 필요한 패키지를 설치하거나 업데이트 할 수 있음
- 아래 예에서는 CentOS의 컨테이너에서 yum update 를 실행하여 git을 설치하고 있음
~~~linux
$ docker start -i 0599550eaedb 
[root@0599550eaedb /]# yum update -y
[root@0599550eaedb /]# yum install -y git
~~~
- `docker commit [옵션] 컨테이너ID | 컨테이너명 리포지터리명[:태그]` 를 실행하면 현재 컨테이너의 상태를 이미지로 만들어 리포지터리 보관 가능
- 아래 예에서는 컨테이너를 로컬 레포지토리에 보관하고 있음  
  컨테이너 실행 중에도 이미지를 만들 수 있으나, 기본적으로 이미지를 쓰는 동안은 컨테이너가 일시정지함
- 보관할 이미지의 태그는 버전이나 기타 의미있는 문자열을 사용하여 다른 이미지와 구별하도록 함
~~~linux
heojaehun@jaebigui-MacBookPro ~ % docker commit 0599550eaedb centos:7-git 
heojaehun@jaebigui-MacBookPro ~ % docker images | grep centos 
centos                     7-git     0c3dd1907c87   42 seconds ago   552MB
centos                     7         eeb6ee3f44bd   5 months ago     204MB
~~~

### 이미지를 원격 리포지터리에 보관(docker push)
- 이미지를 원격 리포지터리에 등록하는 것은 쿠버네티스에서 컨테이너를 돌리기 위해 반드시 해야하는 작업
- 여기서는 도커 허브, IBM, 구글이 관리하는 리포지터리에 이미지를 등록하는 방법을 알아보자
- 이미지를 원격 리포지터리에 등록하는 명령어는 동일한데 유저 인증 방법이 서로 다름

#### 도커 허브 리포지터리를 사용하는 경우
- 도커 허브에 가입하여 도커 ID 취득
- 명령어 `docker login`으로 도커 ID와 비밀번호를 입력하여 로그인
- 명령어 `docker tag`로 로컬의 이미지에 태그를 부여함
- 명령어 `docker push`를 사용하여 이미지를 원격 리포지터리에 업로드
- 도커 허브에 접속하여 등록된 것을 확인하고 필요에 맞게 설명 기재
~~~linux
$ docker login # 도커 허브에 로그인
~~~
- 도커 허브의 웹페이지에 로그인하여 확인. 도커 허브에 로그인하면 초기 화면에 본인의 레포지터리 목록이 표시될 것임
- 도커 허브 유저의 리포지터리 이름은 도커 ID로 시작. 도커 ID는 koni114 이므로, 리포지터리들은 `koni114/` 로 시작됨
- 로컬 레포 이름과 태그가 `centos:7-git`이므로, 도커 허브의 리포지터리 이름과 태그는 `koni114/centos:7-git`이 됨
- 다음은 로컬의 이미지에 원격 리포지터리의 alias 를 만듬. 
~~~linux
docker tag centos:7-git koni114/centos:7-git

$ docker images
koni114/centos             7-git     0c3dd1907c87   21 minutes ago   552MB
centos                     7-git     0c3dd1907c87   21 minutes ago   552MB
centos                     7         eeb6ee3f44bd   5 months ago     204MB
~~~
- `docker push`를 통해 이미지가 도커 허브에 등록됨
~~~
$ docker push koni114/centos:7-git
~~~

### 종료한 컨테이너 제거(docker rm)
- `docker rm 컨테이너 ID | 컨테이너명`을 실행하면 컨테이너가 삭제됨
- 컨테이너가 삭제되면 로그도 지워지고 더 이상 재기동할 수 없게 됨
~~~Linux
docker rm 0599550eaedb
docker logs 0599550eaedb
# Error: No such container: 0599550eaedb
~~~

### 필요 없어진 이미지를 로컬 리포지터리에서 삭제(docker rmi)
- 필요 없어진 로컬 레포에서 삭제하고자 할 때는 `docker rmi 이미지ID`를 실행

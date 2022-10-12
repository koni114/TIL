# 컨테이너 API
- 컨테이너 API는 컨테이너를 블랙박스처럼 다룰 수 있게 해주는 인터페이스. 이는 쿠버네티스 환경에서도 사용됨
- 인터페이스란, 원래 하드웨어 간 접속을 위한 규격이나 케이블 연결 사양을 의미함  
  소프트웨어에서도 이와 비슷하게 서로 다른 팀이 개발한 프로그램들을 연결하기 위해 서로 지켜야 하는 규격을 말함
- 도커 컨테이너에 API가 있다면 컨테이너 내부 프로그램에 대해 잘 알지 못해도 간단하게 재이용 하는 것이 가능함

## 컨테이너 API의 종류와 개요
![img](https://github.com/koni114/TIL/blob/master/container/docker/img/docker_13.jpeg)

### 컨테이너 기동
- 컨테이너 내의 애플리케이션은 기동 시에 환경 변수나 실행 인자를 읽어서 그에 맞게 동작하게 만들 수 있음

### 헬스 체크(쿠버네티스 환경)
- <b>준비 완료 프로브</b>는 컨테이너의 애플리케이션이 초기화가 완료되어 외부로부터의 요청을 받을 수 있게 되었음을 알리는 인터페이스
- 로드밸런서가 컨테이너에 요청을 전달하기 시작해도 될지 확인하기 위한 목적으로 사용됨 
- <b>활성 프로브</b>는 애플리케이션의 기동 상태(정상/비정상)을 알리는 인터페이스  
  비정상이 감지되면 쿠버네티스가 컨테이너를 재기동하여 복구를 시도함

### 컨테이너 종료
- 컨테이너 내의 애플리케이션은 종료 요청 시그널(SIGTERM)에 대한 종료 처리를 구현하는 것이 좋음
- 종료 처리란 메모리의 값을 보존하거나 데이터베이스와의 세션을 종료한 뒤 정상 종료하는 것을 말함
- 강제 종료 시그널(SIGKILL)은 제한 시간 내에 종료 처리가 완료되지 않은 경우 컨테이너를 강제 종료하기 위해 사용됨  
  애플리케이션이 강제 종료를 막을 수 있는 방법은 없음

### 서비스
- 컨테이너 위에 돌아가는 서버 애플리케이션은 특정 포트를 통해 클라이언트로부터의 요청을 받아드림
- 특정 포트번호로 클라이언트로부터의 요청을 받고, 처리 결과를 반환하는 역할 수행
- 컨테이너의 포트를 호스트의 IP 주소에 포트 포워딩을 하여 외부에서의 요청을 받아드려야 함
- 쿠버네티스에서는 컨테이너를 담는 파드에 포트를 열어 클라이언트로부터의 요청을 받음

### 로그
- 마이크로서비스 아키텍처를 사용하고 규모가 커지게 되면 보통 수많은 컨테이너를 돌리게 됨
- 그러면 로그의 양도 늘어나게 되는데 , 도커나 쿠버네티스에서는 로그를 일관되게 관리하여 컨테이너의 표준 출력(STDOUT)과 표준 오류(STDERR)를 로그로 간직함
- 컨테이너의 애플리케이션은 로그를 파일에 쓰는 것이 아니라, 표준 출력이나 표준 오류에 쓰면 됨

### 후크(쿠버네티스 환경)
- 컨테이너는 후크에 의해 실행될 스크립트, 혹은 HTTP 요청 처리를 구현해야 함
- Dockerfile의 ENTRYPOINT 나, CMD로 지정한 명령어와 후크는 비동기적으로 실행되어 실행 순서가 보장되지 않음

### 퍼시스턴트 볼륨
- 컨테이너에서 퍼시스턴트 볼륨을 사용하는 대표적인 경우는 <b>설정 파일을 외부에서 주입하는 경우</b>와 <b>발생 데이터를 보존하는 경우</b> 두 가지가 있음
- 애플리케이션이 읽어 들일 설정 파일을 외부에서 주입하는데, 그러면 설정 파일을 바꾸기 위해 이미지를 다시 빌드하지 않아도 되어 재사용성이 높아짐
- 주입하는 방법은 설정 파일을 담은 디렉터리를 컨테이너의 특정 디렉터리에 마운트하면 됨
- 인증서와 같이 민감한 데이터의 경우에도 리포지터리에 등록해서는 안됨. 이러한 경우에도 PV를 사용하여 외부에서 컨테이너를 주입해야 함
- 쿠버네티스에서는 보안에 민감한 데이터를 다루기 위한 <b>시크릿</b>과 일반적인 설정을 다루는 <b>컨피그맵</b>이 있음
- 컨테이너가 삭제되면 데이터도 삭제되기 때문에 보관이 필요한 데이터를 컨테이너의 파일 저장 시스템에 저장해서는 안됨

### 종료 상태
- PID가 1인 프로세스의 Exit 코드가 컨테이너의 종료 코드로 설정됨
- 쿠버네티스에서는 컨테이너가 종료 코드 0으로 종료하면 정상 종료로 취급하고, 그 외의 값인 경우는 비정상 종료로 취급함

## 환경 변수 API 구현 예
- `d5` 라는 디렉터리를 만들고, `Dockerfile`, `my_daemon`이라고 하는 2개 파일을 바탕으로 컨테이너 개발
~~~
d5
|--- Dockerfile
|--- my_daemon
~~~
- Dockerfile 구성을 확인해보자
~~~dockerfile
FROM alpine:latest
RUN apk update && apk add bash
ADD ./my_daemon /my_daemon
CMD ["/bin/bash", "/my_daemon"]
~~~
- 아래 파일 `my_daemon`은 컨테이너가 기동되면 실행되는 shell script.  
  해당 shell script는 환경 변수 INTERVAL 이 없는 경우에는 3초 단위로 현재 시간과 카운터를 표준 출력으로 출력
~~~shell
# 카운터 초기화
COUNT = 0

# 환경 변수가 없으면 default 5 설정
if [ -z "$INTERVAL" ]; then
    INTERVAL=3
fi

# main loop
while [ ture ];
do
    TM=`date|awk '{print $4}'`
    printf "%s : %s \n" $TM $COUNT
    let COUNT=COUNT+1
    sleep $INTERVAL
done
~~~
- 컨테이너 빌드 전 유닛 테스트 수행
~~~shell
$ LANG=C ./my_daemon  # date 명령어가 영어로 출력되게 함. 3초 간격 출력
$ LANG=C;INTERVAL=10 ./my_daemon # 10초 간격으로 메세지 출력
~~~
- 해당 셸을 실행하는 container image를 빌드하자. Dockerfile이  있는 디렉토리에서 다음의 명령어를 수행하면 됨
~~~shell
$ docker build --tag my_daemon:0.1 . 
$ docker images

REPOSITORY                 TAG       IMAGE ID       CREATED         SIZE
my_daemon                  0.1       047118e9f306   4 minutes ago   10MB
~~~
- 컨테이너 실행 후, 다른 터미널에서 해당 컨테이너를 종료하면 다음의 2가지 문제점 발생
  - 종료 명령어 수행 후, 종료까지 9초 이상 지연 발생
  - 컨테이너 명을 지정하여 재실행했지만, COUNT 가 0으로 초기화 됨
 
## 종료 요청 API 구현 예
- 쿠버네티스는 컨테이너를 언제든지 종료할 수 있는 일시적인 존재로 다룸
- 예를들어, 하드웨어 점검을 위해 컨테이너를 다른 서버에 옮기도록 종료 요청 시그널을 보내는 경우가 빈번하게 발생
- 애플리케이션의 버전을 업데이트 할 때도 종료 요청 시그널을 보내 컨테이너를 종료시킴 
- 쿠버네티스에서 돌아가는 컨테이너를 개발할 때는 종료 요청 시그널 처리를 구현하는 것이 좋음
- 파이썬은 시그널을 받아서 처리하는 시그널 핸들러 함수를 설정해야 함
- 시그널은 유닉스 계열의 운영체제에서 프로세스에게 이벤트를 비동기적으로 전달하기 위해 존재
- 커널로부터 시그널을 받은 프로세스는 인터럽트됨  
  미리 시그널 처리 루틴을 등록해 두면 시그널을 받았을 때 필요한 처리를 수행할 수 있음

![img](https://github.com/koni114/TIL/blob/master/docker/img/docker_14.png)
- `docker stop` 명령어는 컨테이너의 PID가 1인 프로세스에게 시그널 `SIGTERM`을 전달하여 종료 처리를 요청  
  도커의 경우, 이 시그널을 보내고 10초를 기다린 뒤 강제 종료
- `docker kill` 명령어를 사용하면 컨테이너 상의 PID가 1인 프로세스가 `SIGKILL` 시그널을 받고 강제 종료
- 다음은 my_daemon2 file 본문 내용
~~~shell
COUNT=0

# 환경 변수 INTERVAL이 없으면 설정
if [-z "%INTERVAL"]; then     # INTERVAL 값이 null, 길이가 0이면 true
  INTERVAL=3
fi

# 재기동/기동시 

# SIGTERM(종료) 시그널이 발생하면, 현재 COUNT 값을 save.dat 에 저장
save(){
  echo $COUNT > save.dat
  exit=0
}
trap save TERM ## 시그널 핸들러 정의, SIGTERM을 받으면 save() 수행 

# 메인 루프
while [ture];
do
  TM=`date|awk '{print $4}'`
  printf "%s : %s \n" $TM $COUNT
  let COUNT=COUNT+1
  sleep INTERVAL
done
~~~
- 해당 셸을 `my_daemon2` 에 저장하고, Dockerfile을 수정한 Dockerfile2를 빌드하여 이미지 생성
- `ADD` 에사 `./my_daemon2` 를 지정하도록 수정함
~~~dockerfile
FROM alpine:latest
RUN apk update && apk add bash
ADD . /my_daemon2 /my_daemon
CMD ["/bin/bash", "/my_daemon"]
~~~
- `docker build --tag my_daemon:0.2 -f Dockerfile2 . ` 을 통해 버전 0.2의 dockerfile 생성  
  중간에 stop 했다가 다시 start 하면 저장된 데이터가 호출되면서 시작됨
~~~shell
$ docker build --tag my_daemon:0.2 -f Dockerfile2 . 
13:41:15 : 0 
13:41:18 : 1 
13:41:21 : 2 
13:41:24 : 3 
13:41:27 : 4 
13:41:30 : 5  # <-- docker stop myd2 실행
$ docker start -i myd2
13:42:17 : 9 
13:42:20 : 10 
13:42:23 : 11 
13:42:26 : 12 
13:42:29 : 13 
13:42:32 : 14 
13:42:35 : 15 
13:42:38 : 16 
13:42:41 : 17 
...
~~~
- 여전히 한가지 문제점이 있는데, <b>컨테이너 안에 파일로 보존한 데이터는 컨테이너가 지워지면 삭제됨</b>  
  정식으로 운영하는 서비스에서는 커다란 문제의 소지가 될 수 있음

## 퍼시스턴스 볼륨 API 구현 예
- 컨테이너를 지워도 데이터를 잃지 않기 위해서는 퍼시스턴트 볼륨을 사용해야 함
- 여기서는 퍼시스턴트 볼륨으로 호스트의 디렉터리 사용
~~~shell
# 카운터 초기화
COUNT=0

# 퍼시스턴트 볼륨
PV=/pv/save.dat

# 환경변수가 없으면 설정
if [ -z "$INTERVAL" ]; then
    INTERVAL=3
fi

# 기동 시 상태 취득 
if [ -f $PV ]; then
   COUNT=`cat $PV`
   rm -f $PV
fi

# SIGTERM 시그널 처리
save() {
  echo $COUNT > $PV
  exit
}
trap save TERM


# 메인 루프
while [ ture ];
do
    TM=`date|awk '{print $4}'`
    printf "%s : %s \n" $TM $COUNT
    let COUNT=COUNT+1
    sleep $INTERVAL
done
~~~
~~~dockerfile
FROM alpine:latest
RUN apk update && apk add bash
ADD ./my_daemon3 /my_daemon
CMD ["/bin/bash", "/my_daemon"]
~~~
- 앞서 동일하게 컨테이너의 이미지를 빌드. 이미지의 태그는 버전 3을 의미하도록 `my_daemon:0.3`으로 지정
~~~shell
$ docker build --tag my_daemon:0.3 -f Dockerfile3 . 
~~~
- 호스트 상의 마운트할 디렉토리를 만듬
~~~shell
$ mkdir data
~~~
- 컨테이너 실행시, 옵션 `-v`를 사용하여 `호스트의 절대 경로:컨테이너_경로`와 같이 지정
- 호스트의 디렉터리는 절대 경로로 지정하기 때문에 실행 예 11에서는 pwd를 사용하여 현재 경로로 치환하도록 함
~~~shell
$ docker run -it --name myd -v `pwd`/data:/pv my_daemon:0.3 # 를 data 디렉토리가 있는 위치에서 실행!
~~~
- docker 를 삭제 후(`docker rm`) 다시 run 해도 데이터가 초기화되지 않는 것을 확인 가능

## 로그와 백그라운드 기동
- 컨테이너를 백그라운드로 돌리기 위해서는 `-d` 옵션 사용  
  그러면 표준 출력이나 표준 오류가 터미널에 출력되지 않고 로그에만 기록됨
- 컨테이너가 터미널로부터 분리된 상태로 기동함. 이때는 로그를 통해 컨테이너 내 애플리케이션의 동작을 확인하게 됨
~~~shell
$ docker run -d --name myd -e INTERVAL=10 -v `pwd`/data:/pv my_daemon:0.3
$ docker logs myd -f # myd container의 Log를 tail -f 로 확인

$ docker attach --sig-proxy=false myd # 백그라운드에서 동작하는 컨테이너를 포그라운드로 전환
~~~
- 옵션 `--sig-proxy=false` 는 터미널에서 ctrl+c 를 눌렀을 때, 컨테이너 자체를 종료하지 않고 터미널과 분리하기 위해서 사용


## 용어 정리
- 퍼시스텀트 볼륨(PV)
  - 물리 저장 장치(volume)를 표현하는 쿠버네티스의 자원 
  - PV를 파드에 연결해 사용하려면 퍼시스턴트 볼륨 클레임(PVC) 객체가 필요
- .dat파일
  - Data file. DAT 파일 유형은 주로 Data와 관련되어 있음
  - 텍스트, 그래픽 또는 이진 데이터 등 모든 것이 가능함. .DAT 파일에는 특정한 구조가 없음 
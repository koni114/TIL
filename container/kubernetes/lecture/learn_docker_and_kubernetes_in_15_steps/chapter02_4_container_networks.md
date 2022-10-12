# 컨테이너와 네트워크
![img](https://github.com/koni114/TIL/blob/master/container/docker/img/docker_12.jpeg)

- 실행 중인 컨테이너는 IP 주소를 할당받아 컨테이너 간 통신이 가능
- 왼쪽과 같이 호스트 내에서 접근 가능한 전용 네트워크를 통해 애플리케이션과 데이터베이스를 연결하는 것이 가능
- 오른쪽과 같이 컨테이너를 호스트의 외부 네트워크에 공개하는 것도 가능
- 이와 같이 컨테이너 간의 연결을 이용하는 애플리케이션 이미지가 도커 허브에는 다수 등록되어 있음  
  이들 애플리케이션은 컨테이너를 기동하는 것만으로 사용할 수 있음
  ex) Rocket.chat, owncloud, Redmine, WordPress ...

## 컨테이너 네트워크
- `docker network` 커맨드를 사용하여 컨테이너 네트워크를 만들거나 지울 수 있음
- 관련 기능들을 아래 표에 정리

|     |     |
| --- | --- |
| 컨테이너 네트워크 커맨드 | 설명  |
| docker network ls | 컨테이너 네트워크를 리스트로 표시 |
| docker network inspect | 네트워크명을 지정해서 자세한 내용을 표시 |
| docker network create | 컨테이너 네트워크를 생성 |
| docker network rm | 컨테이너 네트워크를 삭제 |
| docker network connect | 컨테이너를 컨테이너 네트워크에 접속 |
| docker network disconnect | 컨테이너를 컨테이너 네트워크에서 분리 |

- 다음은 `docker network ls` 로 컨테이너 네트워크의 목록을 출력
~~~shell
$ docker network ls
NETWORK ID     NAME               DRIVER    SCOPE
29d37f22641a   03-kafka_default   bridge    local
bcc8aec747fd   bridge             bridge    local
a9f9a186241a   host               host      local
d198e84c09e1   none               null      local
~~~
- DRIVER 열에 있는 값이 `bridge`인 경우는 외부 네트워크와 연결되어 있는 네트워크
- 이 네트워크에 연결된 컨테이너는 외부의 리포지터리에 접근할 수 있으며, `-p` 옵션으로 외부에 포트를 공개할 수도 있음
- 컨테이너를 기동할 때 명시적으로 네트워크를 지정하지 않으면 이 네트워크에 연결됨
- 다음의 예에서는 `docker network create 네트워크명` 으로 전용 네트워크를 만들고 있음  
  만들어지는 네트워크는 별도의 IP 주소 범위가 지정되어 다른 네트워크와 격리됨
~~~shell
$ docker network create my-network
~~~
- 컨테이너를 기동할 때 `docker run` 커맨드 옵션으로 `--network my-network`를 지정하면 `my-network` 에 연결된 컨테이너가 기동됨
- 이렇게 기동된 컨테이너는 같은 네트워크에 연결된 컨테이너와만 통신이 가능
- 다음 예시에서는 웹 서버인 `Nginx`를 `my-network`에 연결하여 기동시키는 명령어
~~~shell
$ docker run -d --name webserver01 --network my-network nginx:latest

## 컨테이너 포트번호 표시
$ docker ps

# 결과 
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS     NAMES
78f4b583fb52   nginx:latest   "/docker-entrypoint.…"   4 seconds ago   Up 3 seconds   80/tcp    webserver01
~~~
- 다음 실행 예에서는 또 다른 컨테이너를 기동하여 `nslookup`으로 방금 만든 컨테이너 이름에 대한 IP 주소를 조사하고, `curl`로 HTTP 요청을 전송하고 있음
- 명령을 실행하는 컨테이너는 스탭 02에서 작성한 커스텀 이미지 `my-ubuntu:0.1`을 사용
~~~shell
$ docker run -it --rm --name net-tool --network my-network my-ubuntu:0.1 bash

root@daf030c69348:/# nslookup webserver01

# 결과
Server:		127.0.0.11
Address:	127.0.0.11#53

Non-authoritative answer:
Name:	webserver01
Address: 172.19.0.2

## 컨테이너 이름으로 접속 테스트
root@daf030c69348:/# curl http://webserver01

# 결과
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
...
~~~
- 이번에는 기본으로 지정되는 bridge 네트워크에 연결된 컨테이너에서 폐쇄 네트워크에 접속을 시도
- 아래 예를 보면 bridge에 연결된 컨테이너에서는 `nslookup`으로 `webserver01`의 도메인 이름 분석에 실패하는 것을 확인
- IP 주소로 역조사해도 실패하며, IP 주소로 직접 접속을 시도해도 응답은 오지 않음. 이를 통해 `my-network` 는 기본 네트워크로부터 분리되어 있음을 확인
~~~shell
## bridge 네트워크에 연결한 컨테이너 기동
$ docker run -it --rm --name net-tool --network bridge my-ubuntu:0.1 bash

## 내부 DNS 주소 해결 리스트
root@9e66cec3a97e:/# nslookup webserver01 

# 결과
Server:		192.168.65.5
Address:	192.168.65.5#53

server cant find webserver01: NXDOMAIN

## 내부 DNS 역 이름 해결 테스트
root@9e66cec3a97e:/# nslookup 172.18.0.2
** server cant find 2.0.18.172.in-addr.arpa: NXDOMAIN

## HTTP 접속 시험
root@9e66cec3a97e:/# curl http://172.18.0.2

... 응답 없음
~~~

## 외부에 포트를 공개하기
- 이번에는 컨테이너의 포트를 호스트의 IP 주소로 공개하는 방법을 살펴보자
- 컨테이너 기동 시 `docker run [옵션] 리포지터리[:태그] 커맨드 인자` 의 옵션으로 `-p 공개_포트번호:컨테이너_내_포트번호`를 지정하면 컨테이너 내 포트를 호스트의 IP 주소상의 포트번호로 매핑
~~~shell
$ docker run -d --name webserver01 -p 8080:80 nginx:latest

$ curl http://localhost:8080/

# 결과
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...

## IP 주소로 접근 테스트(ifconfig 등으로 확인)
$ curl http://192.168.1.25:8080/

# 결과
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
~~~
- 작성한 컨테이너 네트워크는 `docker network rm my-network` 혹은 `docker network prune`으로 삭제 가능
## AP 컨테이너와 DB 컨테이너의 연동 예
- 이번 예제에서는 MySQL 컨테이너(DB 컨테이너)와 PHP 컨테이너(AP 컨테이너)를 컨테이너 네트워크로 연결한 모습

![img](https://github.com/koni114/TIL/blob/master/container/docker/img/docker_19.png)

### 컨테이너 네트워크 작성
- 컨테이너 간 통신을 위한 전용 네트워크 `apl-get`을 만들자.
~~~shell
$ docker network create apt-get
~~~

### MySQL 서버 기동
- 여기서 사용하는 MySQL 공식 이미지는 컨테이너 기동 시 환경 변수를 통해 설정 정보를 전달받음
- 이처럼 환경 변수를 사용하도록 컨테이너를 개발하면 이미지의 재사용성이 좋아짐
- 이를 컨테이너 API라고 함
- 아래 예시에서 `-e`에 이어 환경 변수 `MYSQL_ROOT_PASSWORD`를 지정한 것도 컨테이너 API의 하나로 MySQL 서버의 root 패스워드를 지정하고 있음
- 이외에도 다양한 환경 변수가 있는데, 자세한 내용은 MySQL 공식 리포지터리 참고
~~~shell
$ docker run -d --name mysql --network apl-net -e MYSQL_ROOT_PASSWORD=qwerty mysql:5.7
~~~

### 애플리케이션 컨테이너 개발
- 다음은 MySQL 서버에 접속하여 화면을 표시하는 PHP 애플리케이션을 만들어 이미지로 빌드
- 먼저 이미지를 만들기 위한 디렉터리를 만들고 Dockerfile과 PHP 코드를 작성
~~~
$ mkdir Step04
$ cd Step04
$ tree
.
|-- Dockerfile
'-- php
    '-- index.php
~~~
- `index.php`는 MySQL에 접속하고 그 결과를 메세지로 출력하는 단순한 프로그램 
- MySQL에 접속하기 위한 정보는 환경 변수로부터 취득하도록 기술하고 있어 컨테이너 기동 시  `-e`로 환경변수를 지정해야함
- 다음은 Dockerfile scirpt
  - 첫번째 줄의 FROM 에서 지정한 `php:7.0-apache`는 PHP 공식 이미지
  - RUN 으로 시작하는 두 번째 ~ 다섯번째 줄은 `mysql-client`와 같이 MySQL에 접속하기 위한 필요한 모듈 설치
  - 마지막 줄에서 COPY는 php 디렉터리를 Apache의 디렉터리 (/var/www/html/) 에 복사
- 해당 Dockerfile 에는 컨테이너 기동 후 실행할 커맨드를 지정하는 CMD가 없음
- 이는 베이스 이미지에 설정되어 있기 때문
~~~Dockerfile
FROM php:7.0-apache
RUN apt-get update && apt-get install -y \
    && apt-get install -y libmcrypt-dev mysql-client \
    && apt-get install -y zip unzip git vim
RUN docker-php-ext-install pdo_mysql session json mbstring
COPY php/ /var/www/html/
~~~ 

### 컨테이너 이미지 빌드
- `docker build [옵션] 리포지터리:[:태그] 경로` 를 실행하여 PHP 애플리케이션이 포한된 컨테이너의 이미지를 빌드
- PHP 기능 확장 모듈의 컴파일로 인해 빌드 시간이 좀 오래걸림
- 만약 도중에 컴파일 에러가 발생한다면 출력되는 에러 메세지를 추적하여 에러의 원인을 제거하고 진행
~~~shell
$ docker build -t php-apl:0.1 .  
~~~
- 빌드가 무사히 끝났으면 `docker images`를 실행하여 이미지 `php-apl:0.1`이 만들어진 것을 확인

### 컨테이너 실행
- 빌드한 이미지를 컨테이너로 실행
~~~shell
$ docker run -d --name php --network apl-net -p 8081:80 -e MYSQL_USER=root -e MYSQL_PASSWORD=qwerty php-apl:0.1
~~~
- 기동 후에 실습 중인 컴퓨터의 웹 브라우저에서 `http://localhost:8081`으로 접속하면 접속 됨

![img](https://github.com/koni114/TIL/blob/master/container/docker/img/docker_20.png)

- 웹 서버의 접속 로그는 `docker logs 컨테이너 명 | 컨테이너ID`를 통해 출력 가능
~~~shell
$ docker logs php
~~~
- 데이터베이스는 MySQL의 공식 이미지를 사용했고, 환경 변수로 사용자와 비밀번호를 설정하여 컨테이너 기동
- 데이터베이스에 접속하는 애플리케이션은 PHP 공식 이미지를 사용해서 개발
- 동일한 컨테이너 네트워크를 사용해서 두 컨테이너를 연동했고, 포트 포워딩을 설정하여 호스트의 IP 주소로 애플리케이션 공개
- 컨테이너 네트워크는 컨테이너 간의 서로 통신할 수 있는 통로와도 같음. 쿠버네티스에는 비슷한 역할을 수행하는 클러스터 네트워크가 있음
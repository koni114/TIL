# 컨테이너와 네트워크
![img](https://github.com/koni114/TIL/blob/master/docker/img/docker_12.jpeg)

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

# 결과
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...

## IP 주소로 접근 테스트(ifconfig 등으로 확인)
$ curl http://192.168.1.25:8080/
~~~
- 작성한 컨테이너 네트워크는 `docker network rm my-network` 혹은 `docker network prune`으로 삭제 가능

## AP 컨테이너와 DB 컨테이너의 연동 예

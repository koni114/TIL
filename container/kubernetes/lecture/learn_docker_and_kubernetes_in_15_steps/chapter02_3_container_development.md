# 컨테이너 개발
- 간단한 애플리케이션의 이미지를 빌드하고 컨테이너로 실행하는 실습 진행
- 이미지 빌드를 위해 `docker build`라는 명령어 사용

## 이미지 빌드 개요 
![img](https://github.com/koni114/TIL/blob/master/container/docker/img/docker_10.jpeg)

### (1) 베이스 이미지 선택
- 이미지를 만들 때 바탕이 되는 이미지를 <b>베이스 이미지</b>라고 함
- 베이스 이미지에는 리눅스 공유 라이브러리, 동적 링크나 로드에 필요한 기초적인 파일들이 포함되며, 이를 기반으로 사용자의 이미지를 만들게 됨

### (2) 소프트웨어 패키지 설치
- Dockerfile에 설치 스크립트를 기재하면 베이스 이미지 위에 소프트웨어 패키지가 설치됨 

### (3) 애플리케이션 소스 코드
- 깃헙 또는 로컬에 있는 소스 코드를 이미지에 복사

### (4) Dockerfile
- 이미지를 빌드하는 스크립트가 기재된 파일로서, 다음의 내용을 담고 있음
  - 베이스 이미지의 리포지터리
  - 설치할 패키지
  - 애플리케이션 코드와 설정 파일
  - 컨테이너 기동 시 실행될 명령어 

## 빌드 실행 순서
- 이미지를 빌드하기까지의 흐름은 다음의 5단계로 구성.
  - 디렉터리를 준비하여 이미지에 포함시킬 파일들을 모음
  - Dockerfile을 작성
  - 컨테이너에서 실행할 애플리케이션 코드를 작성하고 유닛 테스트를 실행
  - 이미지를 빌드
  - 컨테이너를 실행하고 동작을 확인
- 먼저 컨테이너에 포함시킬 파일들을 담을 `Step03` 이란 디렉터리를 만들고 이동  
  message 라는 이름의 파일에 있는 문자열을  아스키 아트(ASCII ART)로 변환하여 출력하는 컨테이너를 만들어보자
~~~
$ mkdir Step03
$ cd Step03
~~~
- 베이스 이미지, 이미지에 포함시킬 파일, 컨테이너에서 실행될 명령어가 기술된 dockerfile을 작성
~~~dockerfile
FROM alpine:latest
RUN  apk update && apk add figlet
ADD  ./message /message
CMD  cat /message | figlet
~~~
- `FROM alpine:latest` 
  - 베이스 이미지 지정
  - 이미지가 로컬에 없으면, 도커 허브에서 다운로드
  - `alpine` 는 리눅스의 기본적인 커맨드만 설치되어있는 경량 이미지
- `RUN  apk update && apk add figlet`
  - 리눅스 패키지 및 추가 모듈 설치를 기술
  - `alpine`의 패키지 매니저인 `apk`를 업데이트하고 `figlet`이란 커맨드 설치
  - `figlet`은 아스키 아트를 출력하는 커맨드
  - `&&` 를 사용하면 왼쪽의 커맨드가 정상적으로 수행 후, 오른쪽의 커맨드가 실행됨
- `ADD  ./message /message`
  - 컨테이너 파일 시스템에 파일을 추가
  - 현재 디렉터리에 있는 `message` 라는 파일을 컨테이너의 루트 디렉터리에 배치하고 있음
- `CMD  cat /message | figlet` 
  - 컨테이너 기동 시 실행할 커맨드를 지정
  - `cat message`의 결과를 `figlet` 커맨드의 표준 입력으로 전달
- message 파일에 적당한 메세지를 기록하고 이미지를 빌드해 보자
~~~shell
$ echo "Hello World" > message
$ cat message
# Hello World
~~~
- 아래 실행은 빌드를 실행하고 완료될 때까지 출력되는 메세지.  
  `docker build --tag 리포지터리명[:태그] 경로` 를 실행하면 Dockerfile에 따라 이미지 빌드  
  `--tag` 는 빌드된 이미지의 리포지터리 이름과 태그를 지정  
- 마지막에 추가된 점(`.`) Dockerfile의 경로를 지정하기 위한 것으로 현재 디렉터리에 Dockerfile이 있음을 의미
- <b>점 앞에 반드시 공백을 넣어야 함을 주의</b>
~~~
$ docker build --tag hello:1.0 .   

[+] Building 6.2s (9/9) FINISHED                                                                                                                    
 => [internal] load build definition from Dockerfile                                                                                           0.0s
 => => transferring dockerfile: 393B                                                                                                           0.0s
 => [internal] load .dockerignore                                                                                                              0.0s
 => => transferring context: 2B                                                                                                                0.0s
 => [internal] load metadata for docker.io/library/alpine:latest                                                                               3.4s
 => [auth] library/alpine:pull token for registry-1.docker.io                                                                                  0.0s
 => [1/3] FROM docker.io/library/alpine:latest@sha256:21a3deaa0d32a8057914f36584b5288d2e5ecc984380bc0118285c70fa8c9300                         0.6s
 => => resolve docker.io/library/alpine:latest@sha256:21a3deaa0d32a8057914f36584b5288d2e5ecc984380bc0118285c70fa8c9300                         0.0s
 => => sha256:c059bfaa849c4d8e4aecaeb3a10c2d9b3d85f5165c66ad3a4d937758128c4d18 1.47kB / 1.47kB                                                 0.0s
 => => sha256:59bf1c3509f33515622619af21ed55bbe26d24913cedbca106468a5fb37a50c3 2.82MB / 2.82MB                                                 0.4s
 => => sha256:21a3deaa0d32a8057914f36584b5288d2e5ecc984380bc0118285c70fa8c9300 1.64kB / 1.64kB                                                 0.0s
 => => sha256:e7d88de73db3d3fd9b2d63aa7f447a10fd0220b7cbf39803c803f2af9ba256b3 528B / 528B                                                     0.0s
 => => extracting sha256:59bf1c3509f33515622619af21ed55bbe26d24913cedbca106468a5fb37a50c3                                                      0.1s
 => [internal] load build context                                                                                                              0.0s
 => => transferring context: 46B                                                                                                               0.0s
 => [2/3] RUN   apk update && apk add figlet                                                                                                   2.0s
 => [3/3] ADD   ./message /message                                                                                                             0.0s 
 => exporting to image                                                                                                                         0.0s 
 => => exporting layers                                                                                                                        0.0s 
 => => writing image sha256:b1c9ed59fcd5d68797213baaf35f9c8da940a6ab3d15367b364af298ee4e2118                                                   0.0s 
 => => naming to docker.io/library/hello:1.0  
~~~
- 빌드가 완료된 후 `docker images`를 실행하면 방금 빌드한 이미지가 표시
~~~shell
heojaehun@jaebigui-MacBookPro step03 % docker images | grep hello 

# 결과
hello                      1.0       b1c9ed59fcd5   5 minutes ago   8.56MB
~~~
- 다음과 같이 컨테이너를 실행해 보자
~~~shell
$ docker run hello:1.0 

# 결과
 _   _      _ _        __        __         _     _ 
| | | | ___| | | ___   \ \      / /__  _ __| | __| |
| |_| |/ _ \ | |/ _ \   \ \ /\ / / _ \| '__| |/ _` |
|  _  |  __/ | | (_) |   \ V  V / (_) | |  | | (_| |
|_| |_|\___|_|_|\___/     \_/\_/ \___/|_|  |_|\__,_|                                                   
~~~
- 종료한 컨테이너는 `docker ps -a`로 확인 가능.  
  `docker logs 컨테이너ID` 실행하면 실행 중에 표준 출력으로 출력한 메세지 확인 가능

## Dockerfile 작성법
- Dockerfile 에서 사용할 수 있는 키워드는 이 책에서 소개하는 것 외에도 많음
- 아래 표 3에 비교적 자주 사용하는 커맨드와 그 의미를 정리함

![img](https://github.com/koni114/TIL/blob/master/container/docker/img/docker_11.jpeg)

## Dockerfile 작성 모범 사례
- dockerfile 작성에 관한 모범 사례를 
- 도커의 경우 Dockerfile에 운영체제와 의존 패키지를 기술하여 이미지를 만들면 굉장히 짧은 시간에 컨테이너를 기동/교체/종료할 수 있음
- 이미지에는 운영체제와 패키지가 이미 모두 포함되어 있으므로 배포 시 추가적인 시간이 발생하지 않아 짧게 사용하고 폐기한다는 사고방식이 유효함
- 애플리케이션에 변경 사항이 있는 경우 Dockerfile을 변경하여 이미지를 다시 만들면 그만임
- 이런 컨테이너의 특징은 다음과 같은 운영상의 장점으로 작용함
  - 프로젝트에 새롭게 참가한 개발자가 개발 및 실행 환경에 대해 학습해야 할 시간과 노력을 줄여줌
  - 소프트웨어의 의존 관계를 컨테이너에 담아서 실행 환경 사이의 이동을 쉽게 해줌 
  - 서버 관리나 시스템 관리의 부담을 줄여줌 
  - 개발 환경과 운영 환경의 차이를 줄여서 지속적 개발과 릴리즈를 쉽게 해줌
  - 같은 이미지를 사용하는 컨테이너 수를 늘림으로써 쉽게 처리 능력을 높일 수 있음
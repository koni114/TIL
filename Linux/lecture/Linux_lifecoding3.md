### 강의 44
#### Linux - Web server 1 (apache) : intro
![img](https://github.com/koni114/TIL/blob/master/Linux/img/client_server.JPG)
* 인터넷은 크게 client, server로 이루어져 있음
* client는 server에게 요청(request)하고, server는 다시 client에게 response 함
* client로 사용하기 위해서는 web browser가 깔려 있어야 함
* server로 사용하기 위해서는 web server 프로그램이 깔려 있어야함
* server를 사용하기 위해서는 apache, nginx 등을 깔아서 설치하면 된다는 이야기

### 강의 45
#### Linux - Web server 2 (apache) : install
* apache 설치
~~~
sudo apt-cache search apache
sudo apt-get update
sudo apt-get install apache
~~~
* apache2 실행
~~~
sudo service apache2 start
~~~
* apache2 실행 확인
~~~
sudo htop
~~~
* apache2 가 켜있는 것을 확인할 수 있음
* 엄청 많은 process가 켜져 있는데, 그 이유는 web server의 특성상
많은 사용자가 들어올 수 있으므로, 분산 처리하고자 여러개의 process가 켜져 있음

##### shell에서 직접 web server로 접속해보기
* 특정한 IP를 가지고 접근해서 seb server에 접근하는 것은 현실적인 이유로 난관이 존재
* 가장 간단한 방법은 shell에서 직접 web server에 접속하는 것
* shell에서 web browing을 할 수 있는 것들이 여러가지가 있는데 그 중 elinks 를 직접 설치해보자
~~~
sudo apt-get install elinks
elinks -
~~~
* URL를 물어보는 화면이 나옴
* google.com 이라고 치면 창 하나가 나오는데, web browsing이 가능하다는 것을 확인
* q키를 누르면 빠져나옴

~~~
ip addr(ip 확인)
elinks http://10.0.2.15
~~~
* elinks 뭐시기라고 나오면 성공적으로 web server를 띄었다는 것을 의미함
* 자신의 컴퓨터에 접속하는 또다른 방법 : localhost
* 실습을 하는 경우, client와 web server를 둘 다 설정해서 하는 경우가 많음  
이러한 경우에 WB는 WS가 같은 컴퓨터이므로, localhost로 접속이 가능

### 강의 46
#### Linux - apache 웹서버 3 - configuration
##### Web Server는 어디서 index.html file을 읽어오는 것일까?
* etc 디렉토리에 여러가지 프로그램의 동작 방법이 저장되어 있음
* etc/apache2/ 디렉토리 밑에 apache2.conf file을 열어보자
* 해당 file에는 <b/>IncludeOptional sites-enabled/*.conf</b> 라고 되어 있는데 이 말은 sites_enabled file을 모두 읽겠다라는 의미  
* sites-enabled file에 들어가보면, 000-default.conf 라는 링크를 확인할 수 있음
* 해당 링크를 들어가면, Document var/www/index 디렉토리가 있다고 나오는데 여기에 다시 들어간다
* 들어가면, index.html file이 있는 것을 확인!
* 이 file 이름을 바꾸고, elinks http://127.0.0.1/index 라는 명령어를 수행하면 not found라고 나옴
* nano index.html 명령어를 통해 새로운 index.html file을 생성하고 다시 위의 명령어를 수행하면  새로 만든 html file이 나옴을 확인할 수 있다
* 즉, WB(web browser)가 localhost로 index.html를 호출하면, WS(Web Server)는 설정 파일을 참고해서 index.html file을 읽어드려오는 형식을 가짐
* <b/>설정 파일을 바꾸면 실행하는 방식 자체를 바꿀 수 있다는 것을 기억하자</b>
* web browser가 사용자가 요청한 파일을 찾는 최상위 디렉토리를 <b/>document root</b> 라고 함
##### 간단 용어
* SSD(Solid State Drive)  
반도체 메모리에 데이터를 기록하는 기록 장치, 즉 반도체로 된 저장장치

### 강의 47
#### Linux - apache 웹서버 4 - log
* 전 시간에 우리는 index.html file을 읽어 올 수 있는 이유가, etc/apache2/sites-enabled/000-default.conf 라고 적혀 있었기 때문인 것을 알았다
* 마찬가지로, 000-default.conf file 내에서  ErrorLog, CustomLog file이 var/log/apache2 디렉토리에 귀치함
~~~
cd var/log/apache2
~~~
* 해당 디렉토리에 errorlog, access file이 존재함을 확인

##### access.log file 사용하기
~~~
tail -f access.log
~~~
* tail -f 명령어는 해당 파일을 실시간으로 계속 읽어들이겠다! 라는 의미
* curl이나 elinks 명령어를 통해 localhost로 접속하면 access.log file에 log가 남는다는 것을 볼 수 있음
* server 프로그램이 공통적으로 가지고 있는 것!

### 강의 48
#### Linux - 원격제어 ssh 1
* 오늘날 linux가 큰 부분을 차지하고 있는 이유는 데스크탑에서 많이 사용되는 것이 아니라, server 시장에서 압도적 다수를 사용하고 있기 때문에 linux가 중요함
* 또한 IOT에서도 linux가 많이 사용됨
* 우리는 멀리 있는 server 컴퓨터를 <b/>원격 제어</b>를 해야함
* 그 때 우리는 <b/>SSH</b>를 사용
##### SSH 사용 방법
* 우리가 원격 제어를 하고자 하는 server 컴퓨터에는 SSH server가 깔려 있어야 함
* 우리 컴퓨터에는 SSH client가 깔려 있어야 함
* SSH client 에 명령어를 입력하면 SSH server가 설치되어 있는 컴퓨터를 제어하게 됨
* 이러한 process는 WB, WS 관계와 거의 유사
* 대부분의 unix 계열 시스템에서는 SSH system이 설치 되어있음

### 강의 49
#### Linux - 원격제어 ssh 2
##### 기존에 설치되어 있는 SSH program 삭제 후 다시 설치해보기
* 잘못 삭제하면 문제 생길 수도 있으므로 눈으로만 따라하자
~~~
sudo apt-get remove openssh-server openssh-client(약한 삭제)
sudo apt-get purge openssh-server openssh-client(강한 삭제)
~~~
* 삭제됨
~~~
sudo apt-get install openssh-server openssh-client
~~~
* openssh는 ssh라고 하는 방식을 통해 컴퓨터를 원격 제어하기 위해서는 ssh와 관련된 많은 프로그램이 필요한데 이것들이 다 포함되어 있음
* openssh-client가 지금 실습에서는 필요 없지만, 나중에 실제로 다른 컴퓨터의 ssh를 원격제어 하기 위해서는 반드시 필요
~~~
sudo service ssh start
~~~
* ssh start
~~~
sudo ps aux | grep ssh
~~~
* ssh가 정상적이게 실행되는지 확인
##### 다른 컴퓨터에서 ssh로 원격 제어해보기
~~~
ssh egoing@192.168.0.65
~~~
* ssh : ssh-client 프로그램을 실행시키는 명령어
* 해당 명령어를 실행시키면 원격 제어를 통해 ssh-server에 접속되게 됨
* 이 순간부터 명령어들은 원격 컴퓨터를 대상으로 실행됨

### 강의 50
#### Linux - 포트(port) 1 - 포트란 무엇인가?
![img](https://github.com/koni114/TIL/blob/master/Linux/img/port.JPG)
* 보통 domain name을 입력할 때 뒤에 :를 붙이고 숫자를 입력하는데, 이를 <b/>PORT</b> 라고 함
* 일반적으로 0 ~ 1024까지가 알려진 포트 번호
* 22 : SSH, 80 : web 의 고정된 PORT 번호
* 만약에 변경하고 싶으면, config file을 수정해서 PORT 번호를 수정하면 됨

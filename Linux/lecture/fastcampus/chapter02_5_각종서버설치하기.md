# chapter02_5 각종 서버 설치하기
- 웹 서버 구축하기
  - 웹 서비스 설치하기
    - nginx 설치하기
    - apache 설치하기
  - 웹 서비스 설정하기
  - 웹 서비스 올리기
- 파일 서버 구축하기
  - 파일 서비스 설치하기
    - vsftpd 설치하기 
  - 파일 서비스 권한 설정하기
- DB 서버 구축하기
  - DB 서비스 설치하기
    - mysql 설치하기
    - postgresql 설치하기
  - DB 서비스 설정하기는 생략

## 웹 서버 구축하기
- 웹 서버의 선택, apache vs nginx
  - 점유율은 apache 43.3% , nginx 42.2% 로 거의 비슷함
  - nginx 는 우리나라에서 많이 사용됨
  - Apache 는 RedHat/Fedora 계열은 httpd 를 설치를 하고, Debian 계열은 apache2 를 설치 
  - Nginx 는 모두 nginx 를 설치하면 됨
- apache 를 사용한 웹 서버 구축하기
- 웹 서비스 설치하기
  - `sudo apt install apache2`
  - apt 명령어를 통해 install 과정을 거치면, 매뉴얼, 각종 바이너리 실행 파일들이 여기저기 흩어져서 실행되게 됨
- 웹 서비스 (기본) 설정 보기
  - `/etc/apache2/apache2.conf`
- 웹 서비스 사이트별 설정 보기(내가 운영하고자 하는 사이트를 말함)
  - `/etc/apache2/site-available/*`
  - `/etc/apache2/site-enabled/*`

![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_17.png)
- 위의 그림에서 보면, 다양한 site 들이 준비가 되어있는데, 서버 운영과 유지보수, 기능 추가로 인해 config 파일을 지우게 되면 굉장히 번거롭게 됨
- 그래서 접속 가능한 site 를 `site-available` 이라는 디렉토리 안에 넣어두고 필요에 따라 symbolic link 를 통해 넣어두게 되면 활성화를 시키게 되면서 필요한 site 에만 접속하거나 접속하지 못하게 할 수 있음
- 웹 서비스 재 실행하기
  - `sudo systemctl restart apache2.service` 
  - `sudo systemctl restart apache2`(service 는 생략가능)
- 웹 서비스 만들기
  - 실제 정적인 데이터들이 존재하는 디렉토리인 `/var/www/html/` 에 index.html 이라는 파일을 통해 웹서비스가 구동됨 
- 웹 서비스 로그
  - `/var/log/apache2/*`

![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_18.png)

- apache 웹 서버 상태보기
  - `systemctl status apache2`
  - enabled 상태라면, 해당 서버를 부팅할 때 실행한다는 의미
  - vender preset 은 패키지 설치할 때의 기본값을 말함. 오른쪽에 enabled 이므로 기본적으로 패키지가 설치될 때 자동으로 enabled 되는 것을 확인할 수 있음
  - 아래는 현재 Active 상태를 확인할 수 있고, 아래 추가적인 정보를 확인할 수 있으며, 만약 자세한 내용을 알고싶다면 `journalctl -u` 명령어를 통해 확인 가능
- apache 웹 서버 제어하기
  - `systemctl disable apache2` : 서비스를 중단하지는 않지만, 다음 부팅 시 아파치를 실행하지 않음
  - `systemctl status apache2`
  - `systemctl stop apache2` : 서비스를 바로 중단(다음 부팅 시 영향을 주지는 않음)
  - `systemctl enable apache2` : 서비스를 시작하지는 않지만, 다음 부팅 시 아파치를 자동으로 실행
  - `systemctl start apache2` : 지금 바로 서비스를 시작
- nginx 를 사용한 웹 서버 구축하기
  - 웹 서비스 설치하기
    - `sudo apt install nginx`
  - 웹 서비스(기본) 설정 보기 
    - `/etc/nginx/nginx.conf`
  - 웹 서비스 사이트별 설정 보기
    - `/etc/nginx/site-available/*`
    - `/etc/nginx/site-enabled/*`
  - 웹 서비스 재실행하기
    - `sudo systemctl restart nginx.service`
    - `sudo systemctl restart nginx`
  - 웹 서비스 만들기
    - `/var/www/html`
  - 만약 위에서 apache2 서비스가 실행되고 있다면, 같은 80 포트를 사용하고 있어 충돌이 나 실행이 안되기 때문에 만약 nginx 웹서버를 구동하고 싶은 경우에는 apache2 서버를 disabled 하고 실행시켜야 함

## 웹 서버 구축하기 - 2
- 이번에는 기본 웹 서비스에 기능을 추가해보자
- nginx 는 기본적으로 static contents 만을 표시할 수 있기 때문에, html, css, javascript 와 같은 기본적인 탬플릿 만을 제공 가능함 
- 동적인 dynamic contents 는 php, java, python 과 같은 다른 언어를 통해서 back-end 서비스가 구현이 되어야 함
- php를 추가적으로 설치하는 방법에 대해서 알아보자
- nginx 를 사용한 php 연동 웹 서버 구축하기(FastCGI Process Manager, daemon)
- nginx 가 받은 요청을 FastCGI를 통해서 php 로 전달을 하게되고, 응답결과를 Socket으로 받아 다시 nginx 를 통해 사용자에게 전달하는 구조로 되어 있음
- 웹 서비스에 php 연동하기 
  - `sudo apt install php7.2-fpm`
- 설정파일 찾기
  - `locate php.ini(바로 안나오면 sudo updatedb)`
  - `vi /etc/php/7.2/fpm/php.ini`
- 바꾼 내용이 있다면 재시작(없음)
  - `systemctl restart php7.2-fpm`
- nginx 설정파일 수정
  - `vi /etc/nginx/site-available/default`
  - 위의 설정파일을 수정해서 웹 서비스가 index.php 파일을 읽도록 변경해주어야 함
  - 확장자가 php 파일인 경우에는 우리가 연동한 php fpm 으로 보내주어야 하기 때문에 아래와 같이 정규표현식을 통해서 설정을 변경해줌
  - 이 때 php FPM과 연동하는 방식이 linux domain socket 도 있으며, tcp 소켓 통신으로도 할 수 있게끔 설정 할 수 있음
~~~shell
server {
  listen 80 default_server
  ...
  index index.php index.html index.htm;
  ...
  location ~\.php$ {
    include snippets/fastcgi.php.conf;
    fastcgi_pass unix:/var/run/php/php7.2-fpm.sock;
  }
}
~~~
- nginx 재시작
  - `sudo systemctl restart nginx`
  - 재시작을 수행한 후에 오류가 있는 경우, 바로 서비스가 뜨지 않고 종료됨
  - 이러한 경우는 불필요한 서비스의 다운타임을 유발할 수 있음
  - 따라서 설정파일을 테스트를 먼저 해주어야 함
  - `nginx -t` (설정파일 테스트)

## 파일서버 구축하기
### vsftpd 를 사용한 파일 서버 구축하기
- 요즘은 HTTP가 편리하기 때문에 HTP protocol은 잘 사용은 안함 
- FTP 서비스 설치하기
  - `sudo apt install vsftpd`(Very secure ftp의 약자)
- FTP 서비스 설정 보기
  - `/etc/vsftpd.conf`
- FTP 접속 테스트하기
  - `ftp 127.0.0.1`
  - user1(id)
  - qwe123(pw)

### vsftpd 를 사용한 익명사용자 읽기전용 파일 서버 구축하기
- 모든 사람들에게 매번 해당 서버를 사용하는 사용자에게 계정을 만들어줄 수는 없음
- 따라서 익명으로 서비스를 사용하는 기능도 필요로 하게 됨(보안 주의! -> 아무나 들어와서 파일을 가져갈 수 있음)
- FTP 서비스 설정 수정
  - `/etc/vsftpd.conf`
    - `ananymous_enable=YES` (기본값 NO)(기본 계정 = anonymous, ftp)
  - `systemctl restart vsftpd`
- FTP 익명 공유 디렉토리
  - `/srv/ftp`
- FTP 접속 테스트하기
  - `ftp 127.0.0.1`
    - `ftp` <enter> 또는 `anonymous` <enter>

### vsftpd 를 사용한 파일 서버 (제대로) 구축하기
- FTP 서비스 설정 수정하기
  - sudo vi /etc/vsftpd.conf
    - 익명 사용자 비허용
      - `anonymous_enabled=NO`
    - 로컬 사용자 계정 허용
      - `local_enabled=YES`
    - 사용자 HOME 디렉토리 탈출 금지
      - `chroot_local_users=YES`
      - `allow_writeable_chroot=YES`
    - 로컬 FTP(공유) 루트 디렉토리 설정
      - `local_root=/srv/ftp`
    - 업로드 가능
      - `write_enable=YES`
    - `systemctl restart vsftpd` 를 통해 데몬 재시작(reload 써도 됨)
    - 사용자 계정 만들기(home/shell 있는 사용자)
      - 내가 ftp 서비스를 올리게 되면 시스템에 존재하는 모든 사용자가 ftp 서비스를 사용하게 되는데 보안상 원치 않을 수 있음. 따라서 PAM 모듈을 통해서 접근제어 수행
      - `sudo adduser ftpuser1`
    - PAM 모듈을 통한 접근제어(허용된 사용자만 FTP 접근)
      - `sudo vi /etc/pam.d/vsftpd`
        - `sense=allow`  
          `file=/etc/ftpusers_permit`
    - 사용자 접근제한(disallow)
      - `/etc/ftpusers`(기본값)
    - 사용자 접근제한(allow)
      - `/et/ftpusers_permit`(직접만듬)

## DB 서버 구축하기
### mysql 을 사용한 DB 구축하기
- DB 서비스 설치하기
  - `sudo apt install mysql-server`
- DB 서비스 설정하기
  - `sudo mysql_secure_installation`
- DB 접속 테스트(우분투 16.04)
  - `mysql -u root -p`
- DB 접속 테스트(우분투 18.04)
  - `sudo mysql`

### mysql 을 사용한 DB 구축하기 #2
- `systemctl status mysql`

### postgres 을 사용한 DB 구축하기
- DB 서비스 설치(Ubuntu 16.04 -> Postgresql v9.5)
  - `sudo apt install postgresql`
- DB 서비스 설치하기(Ubuntu 18.04 -> Postgresql v10.0)
  - `sudo apt install postgresql`
- 만약 내가 더 상위 버전을 설치하기를 원한다면 어떻게 해야할까?   
  이를 위해서는 아래와 같이 리포지토리를 별도로 추가해 주어야 함
- DB 서비스 설치하기 Postgresql-11
  - 리포지토리 추가
    - `vi /etc/apt/sources.list.d/pgdg.list`
    - `deb http://apt.postgresql.org/pub/repos/apt/bionic-pgdg main`
  - 해당 리포지토리를 신뢰하기 위한 샤이닝 키 추가
    - `wget --quiet -O -https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -`
  - 리포지토리 갱신 및 설치
    - `sudo apt update`
    - `sudo apt install postgresql-11`
  - 확인
    - `ls -al /usr/lib/postgresql/11/bin/`

- postgres 을 사용한 DB 구축하기
  - 설치 확인
    - `dpkg -l | grep postgres`
    - `cat /etc/passwd | grep postgres`
  - 접속 테스트
    - `sudo -u postgres psql`
    - `\l`
    - `\q`

## 용어 정리
- 이벤트 처리방식
- MPM(Multi-Processing-Module)
- 비동기 처리
- 동적 contents 처리
- FPM 
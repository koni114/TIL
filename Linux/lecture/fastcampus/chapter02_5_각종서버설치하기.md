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
  - Apache 는 RedHat/Fedora 계열은 httpd, Nginx 는 모두 nginx 를 설치하면 됨
- apache 를 사용한 웹 서버 구축하기
- 웹 서비스 설치하기
  - `sudo apt install apache2`
- 웹 서비스 (기본) 설정 보기
  - `/etc/apache2/apache2.conf`
- 웹 서비스 사이트별 설정 보기(내가 운영하고자 하는 사이트를 말함)
  - `/etc/apache2/site-available/*`
  - `/etc/apache2/site-enabled/*`

![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_17.png)
- symbolic link 를 통해서 여러개의 운영하는 사이트 중에 접속하고자 하는 사이트와 그렇지 않은 사이트를 구분해서 적용 가능

- 웹 서비스 재 실행하기
  - `sudo systemctl restart apache2.service`
  - `sudo systemctl restart apache2`
- 웹 서비스 만들기
  - `/var/www/html/*` (<- index.html)
- 웹 서비스 로그
  - `/var/log/apache2/*`

- apache 웹 서버 상태보기
  - `systemctl status apache2`
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

## 웹 서버 구축하기 - 2
- nginx 를 사용한 php 연동 웹 서버 구축하기(FastCGI Process Manager)
- 웹 서비스에 php 연동하기 
  - `sudo apt install php7.2-fpm`
- 설정파일 찾기
  - `locate php.ini(바로 안나오면 sudo updatedb)`
  - `vi /etc/php/7.2/fpm/php.ini`
- 바꾼 내용이 있다면 재시작(없음)
  - `systemctl restart php7.2-fpm`
- nginx 설정파일 수정
  - `vi /etc/nginx/site-available/default`
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
  - `nginx -t` (설정파일 테스트)
- nginx 재시작
  - `sudo systemctl restart nginx`

## 파일서버 구축하기
### vsftpd 를 사용한 파일 서버 구축하기
- FTP 서비스 설치하기
  - `sudo apt install vsftpd`
- FTP 서비스 설정 보기
  - `/etc/vsftpd.conf`
- FTP 접속 테스트하기
  - `ftp 127.0.0.1`
  - user1(id)
  - qwe123(pw)

### vsftpd 를 사용한 익명사용자 읽기전용 파일 서버 구축하기
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
    - 사용자 계정 만들기(home/shell 있는 사용자)
      - `sudo adduser ftpuser1`
    - PAM 모듈을 통한 접근제어(허용된 사용자만 FTP 접근)
      - `sudo vi /etc/pam.d/vsftpd`
        - `sense=allow`  
          `file=/etc/ftpusers_permit`
    - 사용자 접근제한(disallow)
      - `/etc/ftpusers` (기본값)
    - 사용자 접근제한(allow)
      - `/et/ftpusers_permit` (직접만듬)

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
- DB 서비스 설치하기 Postgresql-11
  - 리포지토리 추가
    - `vi /etc/apt/sources.list.d/pgdg.list`
    - `deb http://apt.postgresql.org/pub/repos/apt/bionic-pgdg main`
  - 샤이닝 키 추가
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
  
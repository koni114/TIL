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
- apache 를 사용한 웹 서버 구축하기
- 웹 서비스 설치하기
  - `sudo apt install apache2`
- 웹 서비스 (기본) 설정 보기
  - `/etc/apache2/apache2.conf`
- 웹 서비스 사이트별 설정 보기 
  - `/etc/apache2/site-available/*`
  - `/etc/apache2/site-enabled/*`
- 웹 서비스 재 실행하기
  - `sudo systemctl restart apache2.service`
  - `sudo systemctl restart apache2`
- 웹 서비스 만들기
  - `/var/www/html/*` (<- index.html)
- 웹 서비스 로그
  - `/var/log/apache2/*`
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_17.png)

- apache 웹 서버 상태보기
  - `systemctl status apache2`
- apache 웹 서버 제어하기
  - `systemctl disable apache2` : 서비스를 중단하지는 않지만, 다음 부팅 시 아파치를 실행하지 않음
  - `systemctl status apache2`
  - `systemctl stop apache2` : 서비스를 바로 중단(다음 부팅 시 영향을 주지는 않음)
  - `systemctl enable apache2` : 서비스를 시작하지는 않지만, 다음 부팅 시 아파치를 자동으로 실행
  - `systemctl start apache2` : 지금 바로 서비스를 시작
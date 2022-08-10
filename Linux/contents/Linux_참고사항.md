# Linux 참고사항
## linux ssh-server 설치 방법
~~~shell
$ sudo apt update
$ sudo apt install openssh-server

# SSH Server 실행
# 다음 명령어를 통해 SSH가 실행 중인지 확인 가능
# active (running) 가 보이면, 실행 중인 상태임
$ sudo systemctl status ssh

# 만약 실행 중이 아니라면, 다음 명령어로 실행
$ sudo systemctl enable ssh
$ sudo systemctl start ssh

# 방화벽 사용시, ssh를 허용
$ sudo ufw allow ssh
$ sudo ufw status

# Ubuntu 는 기본적으로 SSH Client 가 설치되어 있음
# 없다면, 다음의 명령어로 설치
$ sudo apt-get install openssh-client

# 접속 확인
$ ssh username@ip_address  
~~~
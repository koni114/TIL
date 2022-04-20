## chapter02 - 리눅스 쉘과 CLI 명령어
### 기본 명령어 - 파일 시스템 구조
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_07.png)

- link의 유형 개념
- 하드링크  
  - 용량을 두배로 차지하지도 않고, 실수로 파일을 삭제하더라도 원본은 삭제되지 않음
  - 사용 사례가 그렇지 많지는 않음. 백업의 경우에 간간히 사용
- 소프트링크(심볼릭 링크)
  - 직접적으로 파일을 바라보는 것이 아니라, 파일을 가리키는 포인터가 만들어지게 됨
  - 파일의 불필요한 복사를 방지하여 파일 시스템을 유연하게 활용하거나 여러 디렉토리에서 동일한 라이브러리를 요구할 경우 등 사용

### 기본 명령어 - 파일 시스템 구조(inode 맛보기)
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_08.png)

- inode 초간단 개념
- inode --> 리눅스에서 파일을 관리하는 구조체
- 우리는 리눅스에서 `hello.txt` 라는 파일을 명령어 등을 통해서 접근하는데, 실제로는 중간에 inode를 거쳐서 접근함
- hellolink 라는 하드 링크가 있다면, 이는 hello.txt와 동일한 inode의 주소값을 가리키게 되고, 이는 다시 파일 DATA를 가리키게 됨 
- hellosymlink(소프트 링크)는 hello.txt와 다른 inode를 카리킴 이 inode는 다시 hello.txt의 inode를 가리킴

## 사용자, 그룹 및 권한(명령어)
### 사용자 계정 - superuser 와 user
- 슈퍼유저란? 
  - 시스템 운영 관리자 계정으로 일반적으로 리눅스 운영체제에서는 루트(Root) 유저를 말함
  - 관리자 권한을 이반 사용자 권한과 구분하며 사용자의 부주의로 발생하는 시스템 손상과 바이러스, 악성코드의 침입에 의한 피해를 보호 
- `whoami` - 내가 누구인지 내 계정 확인
- `id` - 내가 갖고있는 권한(포함된 그룹) 확인

### 사용자 계정 - 권한의 대여 - sudoer
- `sudo visudo`  
  슈퍼유저의 권한을 편집
- 설정파일을 통한 변경
  - 사용자 권한
  - %그룹 권한
~~~shell
$ sudo cat /etc/suduers
~~~
- 특정 사용자 별로 권한을 줄 수도 있음.
- 특정 사용자만 sudo 명령어를 사용하게 하거나, 특정 명령어만 sudo를 사용하게 할 수 있음.
- 해당 설정파일을 통한 변경은 되도록이면 자제하는 것이 좋음  
  보안 등에 취약해질 수 있음
- 이럴 때는 사용자를 sudo 권한에 추가하는 것을 추천
  - `useradd -aG user1 sudo`  # Ubuntu
  - `useradd -aG user1 wheel` # Amazon AMI

### 사용자 계정 - 권한의 대여 - su
- 위의 `sudo`를 사용하면, 항상 할때마다 sudo 명령어를 통해 접근해야하는 불편함이 있는데, 이 때 `su`를 사용하면 로그인을 한 것과 같은 효과를 가짐
- `su[username]`
  - 사용자의 권한을 대여(즉, 사용자로 로그인 한 것과 같은 효과)
  - 언제 사용하느냐? 관리자가 사용자 계정을 관리하고 이슈/장애를 분석할 때 
- 사용방법
  - `su user2`  
    user2의 id로 로그인 한다(user2의 pw 필요)
  - `su -user2`  
    user2의 id로 로그인 한다(user2의 home 디렉토리 사용)
  - `su`, `su root`  
    root의 id로 로그인한다. (root의 pw 필요. 하지만 우분투는 root 암호 비활성화 -> 접속할 수는 없음) 

#### 리눅스에서 root로 접속하는 방법
- `sudo su`  
  - 내 권한을 상승하여 root 사용자의 권한으로 로그인함(현재 디렉토리 사용)
- `sudo su -`
  - 내 권한을 상승하여 root 사용자 권한으로 홈 디렉토리 사용(root의 home)
- `sudo su - user2`  
  - user2 사용자의 권한으로 홈 디렉토리 사용(sudoer(user01)의 pw 필요, user2 의 home)

### 사용자 계정과 그룹 계정
- `cat /etc/passwd` : 사용자 계정 확인
- `cat /etc/shadow` : 사용자 암호
- `cat /etc/group` : 사용자 그룹 확인

#### 사용자 계정과 그룹 계정 - /etc/passwd

![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_09.png)

- 사용자 계정은 보통 uid가 1000번 부터 시작함. 꼭 그런것은 아니지만, ubuntu는 그러함
- 기본적으로 웹 서비스는 `www-data` 라는 권한으로 실행되며, <b>특정 프로세스를 사용하기 위해서 사용하는 계정을 서비스 계정</b>이라고 함. 여기서 `www-data`는 서비스 계정임
- 특정 프로세스를 실행하기 위해서 필요한 계정일 뿐, 사용자가 로그인 할 필요는 없음  
  따라서 로그인 쉘이 `/usr/sbin/nologin` 로 되어 있음
- 리눅스 계정 uid 할당 번호
  - 0: root
  - 1~99: predefined
  - 100~999: administrative and system accounts
  - 1000: user
- 과거에서는 해당 passwd 파일에서 암호화된 패스워드를 볼 수 있었기 때문에 passwd 인데, 최근에는 컴퓨팅 파워가 좋아지면서 hash 값을 crack할 수 있기 때문에 해커들이 쉽게 접근해서 탈취할 수 있기 있음
- 이 때문에 분리해서 `shadow` 파일로 옮겨짐

#### 사용자 계정과 그룹 계정 - /etc/shadow
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_10.png)

- 해당 파일에서 암호 같은 것들이 저장됨
- `최종수정일`이 의미하는 것은 1970년 1월 1일을 기점으로 얼마나 시간이 흘렀는지를 의미  
  이를 액셀에서 계산해보면 확인 가능
- `패스워드` 필드는 root 계정은 패스워드가 `!`로 되어있는데, 이는 잠김 계정을 의미함
- 사용자 계정(user01)에서는 패스워드에 `$6$`가 붙어있는 것을 확인할 수 있는데, 이 암호파일이 어떠한 알고리즘으로 암호화가 되어있는지를 확인할 수 있음
- `www-data`는 따로 터미널을 통해 접속을 하지 않는 계정이므로, 패스워드가 `*`로 되어 있음

## 파일의 권한
![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_11.png)

- 사용자 접근 권한의 부분
- 소유자(User) / 그룹(Group) / 그외(Other) 
- 링크 같은 경우는 디렉토리의 경우 나자신과 재 상위 디렉토리는 반드시 자기 자신을 거쳐서 가기 때문에 최소 링크수는 2개

## 파일의 생성 권한(umask - user mask)
- 파일/디렉토리 생성 권한의 확인
- 소유자(User) / 그룹(Group) / 그외(Other)
- 리눅스의 기본 파일 권한: 666
- 리눅스 기본 디렉토리 권한: 777   
  이 말은, umask 가 0일 경우 새로 생성되는 파일의 권한은 666, 디렉토리 권한은 777을 갖게 됨
- 여기서 umask가 2(혹은 0002)일 경우에는  
  파일 기본권한 666에서 002를 빼면 
  - 110 110 110 = 666
  - 000 000 010 = 002
  - 110 110 100 = 664, 즉 rw-rw-r--로 생성됨

## 파일의 권한 - 권한 변경(chmod - change mode)
- `chmod [Options] [MODE] file`  
  파일 디렉토리 권한의 변경
- 소유자(User) / 그룹(Group) / 그외(Other)

## 파일의 권한 - 소유권 변경(chown - change owner, chgrp - change group)
- `chown [Option] ... [USER][:GROUP] FILE`  
  파일/디렉토리의 소유자/그룹 변경
~~~shell
$ chown user2 hello.txt        # 해당 파일(hello.txt)의 소유자를 user2로 변경
$ chown user2:user2 hello.txt  # 해당 파일(hello.txt)의 소유자와 그룹을 모두 user2 로 변경
$ chown:user2 hello.txt        # 해당 파일(hello.txt)의 그룹을 user2 로 변경
~~~ 
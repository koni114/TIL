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
- 소프트링크의 장점
  - 원본 파일이 변경되거나 다른 파일로 변경되어도 링크는 그대로 사용할 수 있어 편리함 

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
  - 관리자 권한을 사용자 권한과 구분하며 사용자의 부주의로 발생하는 시스템 손상과 바이러스, 악성코드의 침입에 의한 피해를 보호 
- `whoami` - 내가 누구인지 내 계정 확인
- `id` - 내가 갖고있는 권한(포함된 그룹) 확인

### 사용자 계정 - 권한의 대여 - sudoer
- `sudo visudo`  
  슈퍼유저의 권한을 편집
- 설정파일을 통한 변경
  - 사용자 권한
  - %그룹 권한
~~~shell
$ sudo cat /etc/sudoers
~~~
- 특정 사용자 별로 권한을 줄 수도 있음.
- 특정 사용자만 sudo 명령어를 사용하게 하거나, 특정 명령어만 sudo를 사용하게 할 수 있음.
- 해당 설정파일을 통한 변경은 되도록이면 자제하는 것이 좋음  
  보안 등에 취약해질 수 있음
- 이럴 때는 사용자를 sudo 권한에 추가하는 것을 추천
  - `useradd -aG user1 sudo`  # Ubuntu
  - `useradd -aG user1 wheel` # Amazon AMI
- sudo 권한을 부여받은 계정 확인
  - `sudo users` 


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
- 과거에서는 해당 passwd 파일에서 암호화된 패스워드를 볼 수 있었기 때문에 passwd 인데, 최근에는 컴퓨팅 파워가 좋아지면서 hash 값을 crack할 수 있기 때문에 해커들이 쉽게 접근해서 탈취할 수 있음
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

## 리눅스 쉘(shell) 이란 ? 
- 운영체제와 통신하기 위한 사용자 인터페이스
- 사용자 명령어 및 프로그램을 실행할 수 있는 공간

## 리눅스 쉘(shell)의 종류
- 두 개의 메인 타입
  - Bourne shell - 특징 $ 프롬프트(Prompt)
  - C shell - 특징 % 프롬프트
- Bourne Shell 의 변천사
  - Bourne shell -> sh
  - Korn shell -> ksh
  - Bourne Again shell -> bash
  - POSIX shell -> sh
- `cat /etc/shells` 을 통해 사용하능한 shell을 확인 가능
- `cat /etc/passwd | grep user --color=none` 을 통해 해당 계정 로그인시 사용되는 shell 확인 가능

## 리눅스 쉘(shell) - 프롬프트(prompt)
- 사용자와 인터렉티브(interactive)한 입력을 주고 받을 수 있는 명령 대기 표시자
- 우분투 기본 프롬프트  
  [username@hostname]<directory>$
- 환경변수 PS1에 기록됨(PS1 = Prompty Statement One)
- 프롬프트 구성은 내가 원하는대로 구성을 변경할 수 있음.

## 기본 명령어 - 출력(echo)
- 화면에 글자를 출력,(에코는 메아리라는 뜻. 즉 내가 작성한 글씨를 다시 출력해줌!)
- `echo [OPTION] [STRING]`
- 옵션
  - -n : 뉴라인 제외
  - -e : Escape 코드 지원
  - -E : Escape 모드 미지원(기본값)

## 기본 명령어 - 리다이렉션(>, >>, 2>, 2>&)
- 결과물을 다른 장치로 보냄(Output, append, error, merge)
- `>` : Output
- `>>` : append
- `2>` : error
- `2>&1` : error 를 output 으로 redirection(--> &)
~~~shell
$ echo "hello" > hello.txt            # 파일로 출력
$ echo "hello another" > hello.txt    # 기존 파일을 덮어씀
$ echo "Hello again" >> hello.txt     # 기존 파일에 누적
$ ls > file.txt                       # 출력 결과물을 파일로 출력(단, stdout만)
$ aaa > file.txt                      # 아무런 내용도 기록되지 않음
$ aaa 2> file.txt                     # 실패한 결과물을 파일로 출력
~~~
- 출력 장치의 유형
  - stdout : 표준출력, 장치번호 1
  - stderr : 에러출력, 장치번호 2 
  - stdin : 입력장치, 장치번호 0
- 복합 사용 예시
  - `ls /tmp/* > result.txt 2>&1`  
    출력 결과물의 성공값을 `result.txt` 로 보내고 에러값을 1번과 같은 곳으로 보내라     
    `ls /tmp/* &> result.txt`: 줄여쓰는 표현법  

## 기본 명령어 - 재지향(리다이렉션)(<, <<)
- 입력값 리다이렉션(표준 입력 - stdin) 및 delimiter
- echo 명령어에 stdin 을 받아 화면에 출력하고 싶지만, echo는 interactive 하게 주고 받을 수는 없음
- 사용 예시
  - `echo "Hello" > hello.txt` : 파일로 출력
  - `echo < hello.txt` : 입력값을 받고 싶으나 동작하지 않음. stdin 입력 지원여부  
  - `cat < hello.txt`  
- Delimiter 사용 예시
  - `cat << end`  
    커맨드 창으로부터 입력받음  
    입력으로부터 마지막으로 end 값이 들어오게되면 화면에 출력되면서 종료
  - `cat << end > hello.txt`  
    표준입력으로부터 end 값이 들어올떄까지 입력 결과를 파일로 출력  

## 기본 명령어 - 파이프 (|)
- 출력값 프로세스간 전달
  - `ls -l | grep hello` : 출력값 내에서 검색
  - `ls -l | wc -l`      : 출력값 내에서 줄 개수 확인
  - `ls -l | grep hello | wc - l` : 다중 파이프 활용
  - `cat hello.txt | more` : 출력값 내에서 페이징 처리 
 
## 기본 명령어 - history
- 쉘에서 입력한 명령어들의 기록(몇 개나? 최대 1000개, 파일에 총 2000개)
~~~shell
$ echo $HISTSIZE       # 1000
$ echo $HISTFILESIZE   # 2000

$ history 10  # 최근 10개의 히스토리 보기
$ history -c  # 히스토리 버퍼 삭제(clear)

$ !18         # 15번째 라인 다시 실행
$ !!          # 바로 이전 명령어 다시 실행
~~~
## 환경변수 - PATH
- 명령어 실행(어디에?)
- 배포판에 따라 현재 디렉토리를 가장 1순위로 하여 실행하는 배포판도 있으나, 우분투는 그렇지 않음
- `echo $PATH`  
  `export PATH=$PATH:<추가할디렉토리>`
- 환경변수 확인 순서
  - '1. PATH 디렉토리 확인
  - '2. PATH 디렉토리가 있으면 실행권한 확인
    - 2.1. 권한이 없으면 SetUID 확인 
  - '3. 권한이 있으면 명령어를 해당 사용자ID 로 실행
    - 3.1 안되면 해당 명령어의 소유주 권한으로 명령어 실행
- 바이너리 실행파일은 PATH의 순차적으로 검색이 되어 실행됨

## 환경변수 - PATH - which
- `which [FILENAME]`  
  내가 실행하는 바이너리가 어디에서 실행되는가? 
~~~shell
$ which ls  
$ which python 
~~~

## 환경변수 - printenv, env
- `printenv` : 다양한 환경변수 확인
- 주요 환경변수

![img](https://github.com/koni114/TIL/blob/master/Linux/lecture/fastcampus/img/linux_12.png)

- 확인방법 및 변경방법
  - `echo $환경변수`
  - `환경변수 = 값`(해당 터미널에서만) 
  - `export 환경변수  = 값`(전체 터미널에서)

## 환경변수  - LANGUAGE / LANG
- 언어(LANGUAGE) 및 언어셋(LANG) 활용
- 환경변수 활용방법:
  - echo $LANGUAGE
  - echo $LANG
- 언어 (한시적으로) 변경
  - `LANGUAGE=en COMMAND [ARGS]`
- 언어셋 (한시적으로) 변경
  - `LANG=c COMMAND  [ARGS]`
- 영구적으로 변경 시에는
  - `export LANGUAGE=en`
       
## 환경변수 - LANG - locale
- 언어와 언어셋(케릭터셋), 그리고 다양한 지역 설정값을 확인(= 로케일)
- 현재 로케일(locale) 정보 확인
  - `locale`
  - `localectl(status)` 
- 설정 가능한 모든 로케일(locale) 정보 확인
  - `locale -a`
- 누락된 로케일(locale)을 새로 활성화 하라면? 
  - `/etc/locale-gen` : 주석처리 확인
  - `locale-gen` : 로케일 재빌드 
~~~shell
$ date
$ LC_TIME=en_US date
$ LC_TIME=en_ZM date
~~~

## 단축명령어(alias)
- bash 쉘의 장점 - 축약어 가능(alias)
- 자주 쓰는 긴 명령어를 짧게 요약
  - ls 명령어는 이미 `ls --color=auto` 의 축약어
  - ll 명령어는 이미 `ls -alF`의 축약어 
- alias 기능은 매번 실행할 때마다 사라짐

## 쉘 부팅(시작) 시퀀스(.profile, .bashrc 등)
~~~
$ ls -al .profile
$ ls -al .bash*
~~~
- BASH의 interactive shell 시작 시퀀스
- '1. `/etc/profile` 수행(공통 수행 - 환경 설정 등)
  - '1.1. `/etc/profile.d/*.sh` 수행(공통 수행)
  - '1.2. `/etc/bash.bashrc` (공통 수행 - 시스템 alias 등)
- '2. `~/.profile` 수행 (사용자별 디렉토리 - 시작 프로그램 등)
  - '2.1 `~/.bashrc` 수행 (사용자별 디렉토리 - alias 등)
  - '2.2 `~/.bash_aliases` (이 파일을 추가적으로 있다면 수행 - 기본은 없음)
- BASH 의 종료 시퀀스
  - `~/.bash_logout`


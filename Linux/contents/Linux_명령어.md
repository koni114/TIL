# Linux 명령어 간단 정리
- DB Connection 개수 보고 싶은 경우
  - `netstat -an | grep tcp | grep 5630 | wc -l`
- Common 접속 후 다른 계정으로 접속
  - `sudo -i`
  - `su - ruser01` 후 ruser01 접속
- root directory 이동
  - `ls ~` 
- mac 스크린샷 저장 경로 변경

~~~shell
$ defaults write com.apple.screencapture location
~~~

- git 해당 디렉토리 밑에 특정 이름으로 된 파일 전부 삭제

~~~shell
$ find . -name .DS_Store -print0 | xargs -0 git rm --ignore-unmatch
~~~


## ls 명령어
- 현재 위치의 파일목록 조회
~~~shell
$ ls -l   # 파일들의 상세정보 출력
$ ls -a   # 숨어있는 파일들도 표시
$ ls -t   # 파일들을 생성된 시간별로 표시
$ ls -rt  # 파일들을 오래된 시간부터 표시
$ ls -F   # 파일을 표시할 때 마지막에 유형을 나타내는 파일명을 끝에 표시
~~~

## find 명령어
~~~shell
$ find [PATH]             # PATH에 있는 파일 및 디렉토리 리스트 표시
$ find . -name  "FILE_1"  # 현재 디렉토리 아래 모든 파일 및 디렉토리 검색
$ find / -name "FILE_1"   # root 디렉토리에서 파일 이름으로 검색.
$ find . -name "STR*"     # 지정된 문자열로 시작하는 파일 검색.
$ find . -name "*STR*"    # 지정된 문자열이 포함된 파일 검색. 
$ find . -name "STR*"     # 지정된 문자열로 끝나는 파일 검색.
$ find -empty             # 빈 디렉토리 또는 크기가 0인 파일 검색
$ find . -name TMP -empty # TMP라는 이름의 빈 디렉토리 또는 크기가 0인 파일 검색
$ find . -name "*.EXT" -delete # 확장자 검색 후 파일 삭제.
$ find . -name [FILE] -print0  # 검색한 결과를 줄 바꿈 없이 출력
$ find . -name "*.ipynb" -exec basename {} \; # 해당 디렉토리에 해당 파일명을 디렉토리는 제외하고 출력

# usr directory 밑에 있는 50MB 보다 큰 파일들을 /tmp 밑에 복사.  
# 이 때 error 발생나는 경우는 출력 안함(2>/dev/null )
$ find /usr -size +50M -exec cp {} /tmp \; 2>/dev/null
~~~
- 파일 또는 디렉토리만 검색하기
  - b : block special
  - c : character special
  - d : directory
  - f : regular file
  - l : symbolic link
  - p : FIFO
  - s : socket
~~~shell
$ find . -name build -type f  # build 라는 이름의 일반 파일 검색
$ find . -name PROJ -type d   # PROJ라는 이름의 디렉토리만 검색
~~~
- 파일 크기를 사용하여 파일 검색
~~~shell
$ find . -size +1024c # 파일 크기가 1024 바이트보다 큰 파일 검색.
$ find . -size -1024c # 파일 크기가 1024 바이트보다 작은 파일 검색.
~~~
- 검색한 파일에 대한 상세 정보 출력
~~~shell
$ find . -name "*.log" -exec ls -ls {} \;
~~~
- 검색한 파일에서 문자열 검색(find + grep)
~~~shell
$ find . -name "*.log" -exec grep "main" {} \;
~~~
- 하위 디렉토리 검색하지 않기
~~~shell
$ find / -maxdepth 1 -name "sys"
~~~

## 프로세스 확인하기
~~~shell
$ ps       # 프로세스 목록확인
$ ps -f    # 프로세스 목록확인 - 자세한 정보
$ ps -e    # 모든 프로세스 리스트 확인
$ ps -ef   
$ ps -aux  # 프로세스 목록 배열 및 시스템 자원 사용률 확인
~~~
- 프로세스 상태를 나타내는 STAT 항목
  - R(Runable) : 실행 대기 상태
  - S(Sleeping) : 수면 상태
  - D(inDlskwait) : 입출력을 기다리는 상태
  - T(sTopped) : 멈춰 있거나 흔적이 남아있는 상태
  - Z(Zombie) : 죽었지만 프로세스에 남아 있는 상태(자원 낭비)

## tar(Tape Archiver)
- 여러 개의 파일을 하나의 파일로 묶거나 풀 때 사용하는 명령어
~~~shell
$ tar cvf T.tar *         # 현재 디렉토리를 tar로 묶고 gzip으로 압축하기
$ tar cvf T.tar [PATH]    # 대상 디텍로티를 포함한 모든 파일과 디렉토리를 tar 아카이브로 묶기
$ tar xvf T.tar           # tar 아카이브를 현재 디렉토리에 풀기
$ tar xvf T.tar -C [PATH] # tar 아카이프를 지정된 디렉토리에 풀기
$ tar tvf T.tar           # tar 아카이브의 내용 확인하기
$ tar zcvf T.tar.gz *     # 현재 디렉토리를 tar로 묶고 gzip으로 압축하기
$ tar zxvf T.tar.gz       # gzip으로 압축된 tar 아카이브를 현재 디렉토리에 풀기
$ tar jcvf T.tar.bz2      # 현재 디렉토리를 tar로 묶고 bzip2로 압축하기
$ tar jxvf T.tar.bz2      # bzip2로 압축된 tar 아카이브를 현재 디렉토리에 풀기
$ tar cvfw T.tar *        # tar 아카이브 묶거나 풀 때 파일 별 진행 여부 확인하기
~~~

## User(사용자)
- 사용자변경
~~~shell
$ su
$ su root   # 비밀번호를 물어보며, super user 계정일 때는 항상 조심해야 함
$ sudo passwd -u root # root 사용자 unlock
$ sudo passwd -l root # root 사용자 lock

# 
$ sudo useradd -m Jaebig # 명령을 실행한 사람의 password 임력
$ su - Jaebig            #  
$ sudo passwd Jaebig     # 
$ sudo usermod -a -G sudo Jaebig # Jaebig 계정에 sudo 명령을 줌 
~~~

## 기타 명령어
~~~shell
$ touch example   #- example file 생성
$ cat fileName    #- 파일 내용을 출력하는 명령어 --> 파일 내용이 길면 스크롤 생김
$ more fileName   #- 파일 내용을 출력하는 명령어 --> 화면 단위로 내용 출력
$ less fileName   #- more와 동일
$ tail fileName   #- 파일 뒷부분 출력
$ cp fileName1 fileName2 #- 파일 복사
$ mv -i            #- 이동할 위치에 해당 파일이 있으면 덮어쓸 것인지 물어봄
$ rm -i            #- 정말 삭제할 것인지 물어봄 
~~~
- more 명령어
  - j : 한줄씩 다음 행으로 넘어감
  - k : 한줄씩 이전 행으로 넘어감
  - Space, Ctrl + f : 다음화면으로 넘어감
  - Ctrl + b : 이전 화면으로 되돌아감 

## crontab basic
- `crontab -e` : crontab 등록을 위한 명령어
- `crontab -l` : 표준 출력으로 크론탭 내용이 나오게 됨
- `crontab -r` : 크론탭을 지우고 싶은 경우

### 주기 결정
- *(분 0-59) *(시간 0-23) *(일 1-31) *(월 1-12) *(요일 0-7)
- 요일에서 0과 7은 일요일
- 매분 실행
~~~shell
# 매분 test.sh 실행
* * * * * /home/script/test.sh
~~~

- 특정 시간 실행
~~~shell
# 매주 금요일 오전 5시 45분에 test.sh 실행
45 5 * * 5 /home/script/test.sh
~~~

- 반복 실행
~~~shell
# 매일 매시간 0분, 20분, 40분에 test.sh 를 실행
0,20,40 * * * * /home/script/test.sh
~~~

- 범위 실행
~~~shell
# 매일 1시 0분부터 30분까지 매분 test.sh 를 실행
0-30 1 * * * /home/script/test.sh
~~~

- 간격 실행
~~~shell
# 매 10분마다 test.sh 를 실행
*/10 * * * * /home/script/test.sh
~~~

### 크론 사용 팁
- 한 줄에 하나의 명령만 사용해야 함
- 주석은 `#` 를 통해 달면 됨

### 크론 로깅(cron logging)
- 크론탭을 사용해서 정기적으로 작업을 처리하는 것은 좋지만,  해당 처리 내역에 대해서 로그를 남기고 싶은 경우 다음과 같이 사용
~~~shell
* * * * * /home/script/test.sh > /home/script/test.sh.log 2>&1

# append 하고 싶은경우
* * * * * /home/script/test.sh >> /home/script/test.sh.log 2>&1
~~~

## 크론탭 백업(crontab backup)
- 혹시라도 `crontab -r` 를 쓰거나 실수로 crontab 디렉토리를 날려버려서 기존 크론 내역들이 날아갔을 때, 크론탭 백업 필요
~~~shell
crontab -l > /home/bak/crontab_bak.txt

# 크론탭 내용을 txt 파일로 만들어 저장해 둠.
50 23 * * * crontab -l > /home/bak/crontab_bak.txt
~~~

## chkconfig 명령어
~~~shell
$ chkconfig sshd on
~~~
- 리눅스 시스템 부팅시 특정 데몬의 자동시작여부를 결정하고 제어할 수 있는 명령어

## ssh 명령어 
- `ssh server_name -p port_number -l login_id`
~~~shell
ssh server208.web-hosting.com -p 21098 -l my_username
~~~

## 데이터 확인
- csv file 의 head 몇 줄만 확인하고 싶은 경우
~~~shell
head -3 test.csv
~~~

## 파일 링크(ln - link)
- `ln [OPTION] ... [TAEGET][LINKNAME]`  
  파일에 하드링크/소프트링크(심볼릭 링크) 민들기
- 사전 준비  
  `touch hello.txt`  
- 소프트링크(심볼릭 링크)  
  `ln -s hello.txt hellosymlink`  
- 하드링크  
  `ln hello.txt hellolink`  
- 파일 링크 확인  
  `ls -ali`  

## 기본 명령어 - 파일 속성 보기(file)
- `file [OPTION] ... [FILE]`  
  파일의 속성 보여주기  
- `file hello`  
  `file /etc/passwd`  
  `file dir1`  
  `file /usr/bin/file`  
  `file hellosymlink`   

## 기본 명령어 - 시스템 종료(reboot, poweroff, shutdown)
- 시스템이 돌아가고 있는 상황에서 전원을 갑자기 꺼버리는 상황은 위험할 수 있음
- `reboot`, 재부팅
- `poweroff`, 종료, reboot, poweroff 두 명령어 모두 바로 적용되니 사용시 주의
- `shutdown [OPTION] [TIME]`  
  주어진 시간에 종료 (기본값+1, -1분후)
  - `shutdown -P now`, `shutdown -r now`

## 권한 관련 명령어
- `whoami`: 내가 누군지 확인하는 명령어. 리눅스는 앞에 내 계정명이 나오므로 궂이 사용할 필요는 없음
- `id`: 내 계정에 대한 상세 정보 확인.
- `sudo`: 슈퍼유저의 권한을 수행(do) 한다.  
  - `sudo cat /etc/shadow`
  - root 권한으로 아무 파일이나 실행하고 수정하게 된다면 보안 취약화됨. (습관적으로 사용해서는 안됨)

## 사용자 추가(adduser - add user)
- `adduser [options][--home DIR][--shell SHELL][--disabled-password][--disabled-login] user`
- 관리자만 사용자 추가가 가능(sudo)
~~~shell
$ sudo adduser user2
~~~

## 사용자 추가(useradd)
- ubuntu 16 버전 이하에서는 useradd 추가시, default로 `/bin/sh`로 보이는데, 이는 원래 `/bin/bash`로 적용됨  
  이는 오래된 버그 중 하나
~~~shell
$ sudo useradd user3           # 사용자 user3 추가
$ sudo useradd -D              # 사용자 생성 기본값 확인
$ sudo useradd -D -b /usr      # 사용자 기본 홈 디렉토리 /usr 로 변경
$ sudo useradd -D -s /bin/bash # 사용자 기본 쉘 bash 로 변경
$ sudo useradd -e 2022-12-31   # 사용자 계정 만료일 설정
~~~

## 사용자 암호 정책 변경 / 암호 변경(chage -change age / passwd)
- `chage [option] user`: 사용자 암호 정책 변경
- `passwd [options] user` : 암호 변경
- `passwd -l user` : 계정 잠금
- `passwd -u user` : 계정 잠금 해제
- `passwd -S user` : 계정 상태 확인
- `passwd -n <mindays> user` : 암호 최소 기간
- `passwd -x <maxdays> user` : 암호 최대 기간
- `man passwd`
~~~shell
$ chage user2    # 암호 정책 변경
$ chage -l user2 # 암호 정책 확인
$ chage -E 2020-12-31 -m 1 -M 90 -W 7 user2 
~~~

## 사용자 삭제(deluser - delete user)
- 사용자 계정 삭제시, 해당 사용자의 파일을 삭제하지는 않음
- 남아있는 파일들을 다른 계정을 생성할 때 userId가 중복된다면 기존 파일을 다시 매핑시킬수도 있음
- 따라서 확실하게 삭제하려면 home 디렉토리도 함께 삭제해야 함
- 삭제된 파일은 다시 살릴 수는 없음
~~~Shell
$ sudo deluser user2               # user2 계정 삭제
$ sudo deluser user2 --remove-home # 해당 계정 home 디렉토리도 삭제
$ userdel user                     # non-interative 모드로 모두 삭제
$ userdel user2                    # 사용자 계정 삭제(홈 삭제) 
$ userdel -f user2                 # 로그인 중이더라도 삭제
~~~

## 그룹 생성(addgroup - add group)
- `addgroup [options] group`  
  그룹계정 생성. 회사 내에서 그룹을 만들어서 같은 자원을 공유하게 만들기 위함
- group에는 primary group과 secondary group이 있음. 사용자 내가 포함된 그룹을 primary group,   
  내가 포함되지 않은 그룹이면서 접근 권한을 받은 경우는 secondary group 이라고 함
~~~shell
$ sudo addgroup developers
$ cat /etc/group | grep devleopers
~~~

## 그룹삭제(delgroup - delete group)
~~~shell
$ sudo delgroup developers
~~~

## 그룹 계정 / 사용자 할당(또는 사용자 정보 수정)(usermod - user mod)
- `usermod [options] user`
- 사용자 정보 수정 (moduser 는 없음 (interactive 방식인))
- 사용자를 그룹에 추가
~~~shell
$ usermod -c user2        # 사용자 이름 수정
$ usermod -a -G sudo user # user2 를 sudo 그룹에 추가
$ deluser user2 sudo      # user2 를 sudo 그룹에서 제거(실행 후 결과 번역 오류) 
~~~

## 파일의 권한
- 사용자 접근 권한의 부분
- 소유자(User) / 그룹(Group) / 그외(Other) 

## 필요한 컬럼만 확인하기 - awk
~~~shell
$ ls -al | awk '{print $1}' # 첫 번째 컬럼만 출력
$ ls -al | awk '{sum += $5} END {print sum}' # 파일의 size를 모두 더해 출력
$ cat /etc/passwd | awk -F":" '{print $1}'   # passwd text에서 : 를 구분자로 첫 번째 컬럼만 출력
~~~

## 특정 텍스트의 단어를 대체 - sep 's/원본단어/대체단어/g'
~~~shell
$ cat /usr/share/doc/vim/copyright | sed 's/book/books/g' > mycopyright
~~~

## 디렉토리의 용량 파악 - du
~~~shell
$ du --max-depth=1 -h 2>/dev/null
~~~

## egrep 
- grep 의 확장판. grep 이 하나의 문자열을 찾는 것과는 달리, 여러개의 문자열을 동시에 찾을 수 있음
- grep 에서 활용할 수 있는 메타문자 이외에 추가 정규표현식 메타문자를 지원함

### egrep 에서 사용하는 정규표현식 메타문자
- `+`: 앞의 정규표현식이 1회 이상 나타남
- `?`: 앞의 정규표현식이 0 또는 1회 나타남
- `|`: 문자열 간의 OR 연산자
- `()`: 정규 표현식을 둘러 쌈

### egrep 예제
- `egrep 'NW|EA' datafile` 
  - NW나 EA가 포함된 행을 출력. NW와 EA 사이에 파이프
- `egrep '3+' datafile`
  - 숫자 3이 한 번 이상 등장하는 행을 출력
- `egrep '2.?[0-9]' datafile`
  - 숫자 2 다음에 마침표가 없거나 한 번 나오고, 다시 숫자가 오는 행을 출력
- `egrep '(no)+' datafile`
  - 패턴 no 가 한 번 이상 연속해서 나오는 행을 출력

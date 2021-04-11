# Linux 명령어 간단 정리
- DB Connection 개수 보고 싶은 경우
  - `netstat -an | grep tcp | grep 5630 | wc -l`
- Common 접속 후 다른 계정으로 접속
  - `sudo -i`
  - `su - ruser01` 후 ruser01 접속
- root directory 이동
  - `ls ~` 
- mac 스크린샷 저장 경로 변경
~~~
$ defaults write com.apple.screencapture location
~~~
- git 해당 디렉토리 밑에 특정 이름으로 된 파일 전부 삭제
~~~
$ find . -name .DS_Store -print0 | xargs -0 git rm --ignore-unmatch
~~~

## find 명령어
~~~linux
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
~~~
- 파일 또는 디렉토리만 검색하기
  - b : block special
  - c : character special
  - d : directory
  - f : regular file
  - l : symbolic link
  - p : FIFO
  - s : socket
~~~linux 
$ find . -name build -type f  # build 라는 이름의 일반 파일 검색
$ find . -name PROJ -type d   # PROJ라는 이름의 디렉토리만 검색
~~~
- 파일 크기를 사용하여 파일 검색
~~~linux
$ find . -size +1024c # 파일 크기가 1024 바이트보다 큰 파일 검색.
$ find . -size -1024c # 파일 크기가 1024 바이트보다 작은 파일 검색.
~~~
- 검색한 파일에 대한 상세 정보 출력
~~~linux
$ find . -name "*.log" -exec ls -ls {} \;
~~~
- 검색한 파일에서 문자열 검색(find + grep)
~~~linux
$ find . -name "*.log" -exec grep "main" {} \;
~~~
- 하위 디렉토리 검색하지 않기
~~~linux
$ find / -maxdepth 1 -name "sys"
~~~

## 프로세스 확인하기
~~~linux
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
~~~linux
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
~~~linux
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
# 파일시스템 살펴보기
## 파일시스템 살펴보기
- bin, home, tmp, usr       --> 사용자 권한으로 접근하고 사용할 수 있는 디렉토리
- etc, lib, root, sbin, var --> 관리자 권한으로 접근하고 사용할 수 있는 디렉토리
- dev, media, mnt, proc     --> 시스템 파일 디렉토리
- <b>etc, var 디렉토리는 시스템을 운영하거나 관리하면서 가장 많이 보게될 디렉토리</b>

### 파일시스템 상세
- `bin` : 기본적인 명령어
- `boot` : 부트로더 디렉토리
- `dev` : 시스템 디바이스(장치파일)
- `etc` : 각종 설정파일
- `home` : 사용자의 홈 디렉토리
- `lib` : 라이브러리(및 커널모듈)
- `media` : 외부 저장소(cdrom, usb 등)
- `mnt` : 외부 저장소 또는 파일시스템 마운트포인트
- `proc` : 시스템 설정들의 가상파일시스템(pseudo-file 시스템)
- `root` : 루트 사용자의 홈 디렉토리
- `sbin` : 시스템(관리자용) 명령어
- `tmp` : 임시 저장소
- `usr` : 일반 사용자들 공통파일
- `var` : 시스템 운용중에 생성되는 임시 데이터 저장소

### 파일 시스템 주요 디렉토리 /boot
- grub 및 커널, initrd, 멀티 부팅 시 메모리 테스트를 위한 memtest 도구
- 업그레이드를 종종하게 되는데, 새로운 커널 버전과 boot file system 이 쌓이게 됨  
  오래된 boot file system은 update 명령어를 통해 삭제도 할 수 있음

### 파일 시스템 주요 디렉토리 /home
- 사용자별로 고유의 영역을 가지고 있지만, 접근 가능

### 파일 시스템 주요 디렉토리 - /etc
- 시스템 프로세스의 각종 설명파일들

#### /etc/*-release
- 운영체제 정보를 갖고 있는 파일들. 
- 대부분의 운영체제는 해당 디렉토리에 *-release 형태로 파일을 가지고 있음
  - `os-release`
  - `centos-release`
  - `redhat-release` 
- `cat /etc/*-release` 명령어로 확인 가능!

### 파일시스템 주요 디렉토리 - /var 및 /var/log
- 시스템 프로세스의 각종 임시 파일들 및 로그 파일들
- 가장 대표적인 것이 log file, pid, process 동기화하기 위한 세마포어 등의 동기화 파일 등

## 파일 시스템 명령어 - 검색 (find)
- `find [OPTIONS][PATH][EXPRESSION]`  
  원하는 파일의 검색
~~~shell
$ find *.txt                    # 내 현재 디렉토리에서 확장자가 .txt인 파일을 찾는 법
$ find . -name  "*.txt"         # 내 현재 디렉토리서부터 확장자가 .txt인 파일을 찾는 법 
$ find . -name "hello*" -type f # 내 현재 디렉토리에서 파일명이 hello로 시작하는 "파일"만 찾는 법 
$ find . -name "dir*" -type d   # 내 현재 디렉토리에서 디렉토리명이 dir로 시작하는 "디렉토리"만 찾는 법

# 내 현재 디렉토리에서 용량이 100M 보다 큰 파일 찾는법
$ find . -size +100000000c        # <-- 100000000c 대신 100000k 또는 100M 사용 가능

# 최근 생성된 파일만 찾아보기(2020년 5월 15일 이후 변경된 파일)
$ find -newerct "15 May 2020" -ls # <-- newerct 대신 newermt 로 할 경우 최근 변경된 
                                  # 최근 2일에서 5일 사이에 변경된 파일 찾기 

# 최근 2일에서 5일 사이에 변경된 파일 찾기 
$ find . -mtime +2 -a -mtime -5 -ls
~~

## 파일 시스템 명령어 - 속성(stat)
- `stat [OPTIONS] [FILE]`  
  원하는 파일의 속성(주로 시간) 확인
- 시간의 유형(atime, mtime, ctime)
  - `Access`: 파일에 최근 접근 시간(고전적으로는 read 시에도 올라갔으나 지금은 다소 변경됨)
  - `Modify`: 파일의 내용 변경 시간  
  - `Change`: 파일의 수정 시간(inode 관점에서의 변화 시간 - 생성, 변경, 속성수정 등) 
~~~shell
$ stat hello.txt

# 결과
File: 'hello.txt'
Size: 386       	Blocks: 8          IO Block: 4096   regular file
Device: 801h/2049d	Inode: 544397      Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/ koni114)   Gid: ( 1000/ koni114)
Access: 2022-04-25 22:54:28.675808891 +0900
Modify: 2022-04-23 08:50:50.901705729 +0900
Change: 2022-04-23 08:50:50.901705729 +0900
~~~
- ls 명령어에서의 시간 확인
  - `ls -l` : 기본값(mtime)
  - `ls -l -u` : atime
  - `ls -l -c` : ctime 

## 파일 시스템 명령어 - 검색 (find) advanced
- 루트 디렉토리로부터 파일 사이즈가 100M 이상인 파일을 찾아서 ls 로 상세 표시하기  
  `find / -size 100M -exec ls -l {} \; 2>/dev/null`
- 루트 디렉토리로부터 txt 파일을 찾아서 그 안에 "HELP"라는 글자가 포함된 파일과 내용 표시  
  `find / -name "*.txt" -exec grep "HELP" {} \; -print 2>/dev/null`
- 루트 디렉토리로부터 특정 [조건]의 파일 찾아서 특정 [디렉토리]로 복사하기  
  `find / [조건문] -print -exec cp {} [경로] \; 2>/dev/null`

## 검색 명령어 - 필터링(grep)
- `grep [OPTION] PATTERN [FILE]`  
  특정 패턴 검색(또는 정규표현식 패턴 검색)
- 파일 내에서 usage 라는 단어 검색
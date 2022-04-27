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
  `grep "usage" [FILE]`
- 파일 내에서 "vim" 또는 "Vim" 이라는 단어 각각 찾는 법(대소문자 구분 없이)  
  `grep "vim" [FILE]`  
  `grep "Vim" [FILE]`  
  `grep -i "vim" [FILE]` (대소문자 무시) 
- 하위 디렉토리 모두 검색    
  `grep -r "vim" [PATH]`

## 검색 명령어 - 필터링(grep) advanced 정규표현식
- 기본 정규 표현식(Basic Regular Expression)
- 실습: `grep -n "PATTERN" /usr/share/doc/vim/copyright`
  - `^s` : 문장의 시작이 s로 시작하는 줄 
  - `e$` : 문장의 끝이 e로 끝나는 줄
  - `..e$` : 문장의 끝의 3글자에서 끝이 e로 끝나는 줄
  - `app*` : 문장의 시작/중간/끝이 ap와 p의 "0개혹은 그 이상"의 개수를 가지고 있는 줄
  - `^[at]`: 문장의 시작 첫 단어가 a 또는 t로 시작하는 줄
  - `[0-9]`: 문장의 중간에 숫자 0~9 까지를 포함하고 있는 줄
- 확장 정규 표현식(Extended Regular Expression)
  - 실습: `grep -E "PATTERN" /usr/share/doc/vim/copyright`  
    - `[p]{2}` : 문장 내 p라는 글자가 연속 두번 나오는 경우
    - `^[a-zA-Z0-9]{3,9}` : 문장의 시작이 소문자/대문자/숫자로 시작하는 3~9길이 

## 검색 명령어 - 필터링(grep) 응용
- 더 일반적인 활용 사례
  - 파이프로 연결한 grep의 응용
- 파일 목록에서 특정 단어 검색
  - `ls -al | grep txt`
- 로그 파일에서 경고만 검색
  - `cat /var/log/syslog | grep -i "warn"`
- 프로세스 목록에서 특정 단어 검색(및 특정 단어 예외)
  - `ps x | grep "/bin"`
  - `ps x | grep "/bin" | grep -v "grep"`
- 특정 포트가 열려 있는지 확인       
  - `netstat -a | grep 80`
  - `netstat -a | grep ":80"` 

## 정렬 명령어 - 소팅(sort)
- `sort [OPTION][FILE]`  
  파일의 내용을 특정 순서(옵션)로 정렬(그러나 현실적으로는 FILE 보다는 PIPE와 더 많이 연동)
- 디렉토리 목록을 소팅(기본값 : 첫 번째 컬럼)  
  `ls -l | sort`
- 디렉토리 목록을 두번째 컬럼으로 소팅(기본값: 캐릭터 소팅)  
  `ls -l | sort -k 2`
- 디렉토리 목록을 두번째 컬럼으로 숫자로 소팅  
  `ls -l | sort -k 2 -n`(또는 -k2n 붙여써도 무방)
- 디렉토리 목록을 파일 사이즈별로 소팅(기본값: 오름차순)  
  `ls -l | sort -k 5 -n`
- 디렉토리 목록을 파일 사이즈별로 역순 소팅(내림차순)  
  `ls -l | sort -k 5 -n -r`
- 두 개 이상의 키로 소팅(두 번째 컬럼(숫자) & 다섯번째 컬럼)    
  순차적으로 적용됨
  `ls -l | sort -k2n -k5`
- 파이프 외에 인풋 리디렉션도 가능  
  `sort -k 2 | -k 5 < dir.txt`

## 내용 검색/편집 명령어(awk)
- 패턴 검색 및 텍스트 프로세싱
- 독자적으로 awk 를 사용하기보다는 shell programming 등에 함께 사용됨
- 디렉토리 목록 중 첫번째 컬럼만 출력  
  `ls -l | awk '{print $1}'`
- 디렉토리 목록 중 파일명과 사이즈만 출력 (아홉번째 컬럼, 다섯번째 컬럼)  
  `ls -l | awk '{print $9, $5}'`  
  `ls -l | awk '{print "FILENAME:"$9, "SIZE: $5"}'`
- 디렉토리 목록 중 사이즈를 모두 더해서 결과만 출력  
  `ls -l | awk '{sum += $5} END {print sum}'`
- 디렉토리 목록 중 파일 사이즈별로 소팅해서 10000 바이트보다 큰 것만 출력  
  `ls -l | sort -k 5 | awk '$5 >= 10000 {print}'`
- 암호 파일에서 콜론(:)을 구분자로 잘라서 첫번째 컬럼만 출력  
  `cat /etc/passwd | awk -F":" '{print $1}'`

## 내용 검색/편집 명령어(sed)
- sed's/패턴/변환/g'  
  스트림라인 편집기(search and replace)
- 파일 내의 모든 book을 books로 변경  
  `cat /usr/share/doc/vim/copyright | sed's/book/books/g`
- (글자가 있는) 모든 줄의 맨 끝을 ! 표로 끝나도록 변경  
  `cat /usr/share/doc/vim/copyright | sed 's/.$/!/g'`  
- 출력 결과를 소문자에서 대문자로 변경  
  `ls -l | sed 's/[a-z]/\U&/g`
- 출력 결과를 대문자에서 소문자로 변경  
  `cat /etc/passwd | sed's/[A-Z]/\L&/g`

## 기타 명령어 - 분석(uniq / wc)
- 중복제거 유틸(uniq) 및 단어분석(word-count)
- 파일 내에 중복되는 줄 제거   
  `cat hello.txt | uniq`
- 파일 내의 "라인수/단어수/문자수" 출력  
  - `wc hello.txt` 또는 `cat hello.txt | wc`
  - `wc -l hello.txt` (라인수만 출력)

## 파일 시스템 주요 명령어(디스크 용량) -du (disk usage)
- `du [OPTION] [FILE]`  
  파일 용량 출력
- 현재 디렉토리로부터 사용된 용량 확인  
  `du` 
- 사용 예시
  - `du -S | sort -n` : 디렉토리별 용량을 오름차순으로 소팅해서 출력
  - `du / -h 2>/dev/null | grep [0-9]G` : 디렉토리별 누적 용량을 출력하여 GB이상의 디렉토리 출력
  - `du --max-depth=1` : 디렉토리 용량을 최대 1 디렉토리 depth 까지만 출력 

## 파일시스템 주요 명령어(묶음/압축) - tar (tape archive)
- `tar [OPTION][FILE][PATH]`  
  파일 묶음
- 각종 옵션
  - `c`: create
  - `x`: extract(해지)
  - `v`: verbose(디테일한 상황 보고 - 실행 중 파일 목록 출력)
  - `f`: file(저장될 파일명 지정하기 위해)
  - `t`: list(목록 확인)
  - `z`: zip(압축)
  - `j`: bzip2(압축) 
- 활용 예시
- `tar cvf myzip.tar dir1`: tar 아카이브 만들기
- `tar tf myzip.tar`: tar 아카이브 내용 확인
- `tar xvf myzip.tar`: tar 아카이브 풀기
- `tar cvfz myzip.tgz dir1`: tar.gz 아카이브 만들기
- `tar tf myzip.tgz` : tar 아카이브 내용 확인
- `tar xvfz myzip.tgz`: tar 아카이브 풀기 

## 파일 시스템 주요 명령어(묶음/압축) - gz, bz2, xz
- `gzip [OPTION] [FILE]`: 파일 압축
- 다양한 압축 유틸리티들(시대의 변화에 따라, 압축 알고리즘의 발전에 따라..)  
  `gzip`, `bzip2`, `xz`
- 압축 용량(작은게 좋음) : `xz` < `bzip2` < `gzip`
- 압축 시간(작은게 좋음) : `gzip` < `bzip2` << `xz`
- 압축 해지 시간(작은게 좋음) : `gzip` < `xz` < `bzip2`

## 사용 방법 - 압축하기
- `gzip filename`, `bizp2 filename`, `xz filename`  
  각각 filename.gz, filename.bz2, filename.xz 형태로 압축됨
- 압축풀기  
  gzip -d filename  
  gzip2 -d filename  
  xz -d filename  
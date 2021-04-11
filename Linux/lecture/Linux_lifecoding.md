# 리눅스 생활 코딩 강좌
### 강의 1
#### 설치 없이 리눅스 사용하기
* codeonweb site에서 무료로 쉘 스크립트 - 리눅스 사용 가능

### 강의 2
####  설치없이 리눅스 사용하기 - cloud9
* 리눅스 설치를 하는 것은 굉장히 까다로운데, 이를 온라인에서 해볼 수 있도록 하는 서비스 제공
* http://c9.io

### 강의 3
#### Linux - install : OSX terminal
* 맥의 운영체제인 linux10은 unix 계열이라고 하는 공통 조상을 가지고 있기 때문에 궂이 linux를 깔지 않아도 mac에서 사용 가능

### 강의 4
#### 가상 머신(virtual machine)
* 하드웨어를 소프트웨어적으로 구현해서 그 위에서 운영체제가 작동하도록 하는 기술
* 가상 머신이라고 하는 프로그램 위에 운영체제가 설치 되는 것

#### 가상 머신을 사용해야 하는 이유
* 다른 운영체제를 사용해야 하는 경우(맥OS에서 윈도우, 윈도우에서 리눅스)
* 독립된 다른 공간이 필요한 경우(바이러스 회피, 백업)
* 하나의 머신에서 여러개의 운영체제를 제공
* 가상 머신을 사용하게 되면 여러개의 운영체제를 사용자에게 제공 가능
* VirtualBox : 무료, 가상머신 솔루션
* 기타 솔루션 : VMWare, VirtualPC

### 강의 5
#### Linux - file & directory 1
* 터미널을 이용해서 리눅스를 제어하기 위해서는 2가지가 중요
  * 명령어를 통해서 제어한다(Command Line Interface)
  * 내리는 명령은 현재 머물고 있는 디렉토리를 대상으로 적용된다
~~~
* pwd   : 현재 디렉토리를 보여줌
* mkdir : 디렉토리 생성
* touch : file 만들기
ex) touch file.txt
* ls -l : 해당 위치의 모든 file 등을 보여줌  
제일 앞에 d가 있으면, folder. d가 아니면 file  
~~~

### 강의 6
#### Linux - file & directory 2
~~~
* cd : change directory의 약자. 보통 file을 입력할 때 절반만 입력하고 tab 키를 누르면 완성형 형태가 나옴   
이 때 복수개가 있다면 해당 문자가 겹치는 여러개의 파일 리스트를 보여줌
~~~

* 상대경로와 절대 경로
  * 상대경로  
    * 부모 경로로 이동
    * 현재 디렉토리
  * 절대경로
    * 최상위 디렉토리를 기준으로 경로를 표현하는 것을 의미
    * 최상위 디렉토리를 root 디렉토리라고 함
    * cd . : 최상위 디렉토리로 이동
* 명령어 앞에 '-'를 붙이면 동작 방법을 바꿈
~~~
rm    : remove. paramter를 붙이지 않으면 file만 삭제됨
rm -r : 해당 디렉토리 삭제
ex) rm -r hello_linux/
~~~  
* 명령어 --help를 사용하면 도움말 확인 가능
* recursively : 재귀적으로 동작한다. 예를들어 rm -r 명령어도 재귀적으로 동작한다고 되어 있는데, 디렉토리 안에 디렉토리를 지우고 ..처럼 볼 수 있음

### 강의 7
#### Linux - help & man
~~~
* man : 해당 명령어 뒤에 궁금한 명령어를 입력하면, 상세한 화면설명서가 화면에 표시됨
help와의 차이는 man은 전용 페이지로 이동. help 해당 디렉토리에서 메뉴얼을 보여줌
키보드 위, 아래를 누르면 script가 움직임
** 만약 여기서 무언가를 찾아보려고 하면, /'찾고자 하는 단어' 를 통해 확인 가능
** 알파벳 q를 누르면, 밖으로 빠져 나가게 됨
ex) /sort -> sort 단어가 들어간 문구들을 하이라이트해서 확인 가능
이때 알파벳 N키를 누르면, sort 단어가 들어간 곳으로 단계 단계 이동시켜줌
 ~~~
* 명령어 사용설명서를 읽는 방법
  * Usage : 사용법. 기본적인 동작방법 설명
  * 대부분의 명령들이 version이라는 것을 가지고 있음

~~~
* mkdir-p : 부모 디렉토리가 필요하면 생성하는 param
            일반적으로 작대기가 1개면 param 2개면 full Name
* ls -a : 있는 모든 목록들을 보여줌
          숨켜저 있는 것까지 보여줌
          숨켜저 있는 파일은 앞에 .가 붙음
* ls -al : 감쳐진 파일과 감쳐지지 않은 파일을 모두 보고 싶을 때
           해당 명령어 사용
~~~
* 다양한 명령어들은 man, help를 이용해서 계속 확인해보자

### 강의 8
#### Linux - 필요한 명령을 검색으로 찾는 법
~~~
* cp : '파일위치 및 파일이름' (한칸 띄고) '목적지 및 파일이름'
* mv : 파일 이동, 이름 수정을 할 때도 이용
  ex) mv rename.txt rename2.txt
~~~

### 강의 9
#### Linux - sudo
* sudo(super user do)
* 유닉스 계열의 운영체제들의 중요한 특징 중 하나는, 다중 사용자 시스템이라는 것(과거에는 컴퓨터가 굉장히 비쌌기 때문에)
* 다중 사용자가 있기 때문에 사용자마다 할 수 있는 일과 할 수 없는 일을 구분하기 위해 permission이라는 체계를 고z안함
* 예를 들어 ubuntu라는 가정하에 apt-get install git 이라고 하면 sudo 권한으로 git을 설치 할 수 있게 됨

### 강의 10
#### Linux - file edit(nano)
  * 명령어 기반의 시스템에서도 편집기가 있음(nano, vi 등..)
  * nano : 초급자, vi : 중,고급자들이 많이 사용함
두 개의 편집기는 대부분의 유닉스 계열에는 다 들어가 있음

### 강의 11
#### Linux manager
* 여기서의 package는 앱, 어플리케이션을 말함
* ls, mkdir도 package 중 하나라고 볼 수 있음
* 오늘날 unix는 package manager를 제공
모바일, 앱스토어 같은 역할을 수행
* package manager 사용 방법
  * 리눅스에서 대표적인 package manager는 apt와 yum 이 있음
* apt 설명
  * apt를 사용하기 위해서 apt를 통해 설치할 수 있는 목록을 최신화 하여야 함
  * apt-get update를 치면 권한이 없다고 나옴
  -> sudo apt-get update : apt를 다운받을 수 있는 서버에서 다운받아 최신상태로 update 해줌(목록을 다운받는 것)
  * sudo apt-cache htop -> htop 이라는 프로그램 search
* htop이 무엇인가?
  * 기본적으로 리눅스에는 top이라고 하는 프로그램이 설치되어 있음(window 작업관리자 같은 것)  
  * top 프로그램은 알아먹기가 조금 어려운데, 좀더 직관적으로(graphical하게) 보고 싶을 때 htop 프로그램 사용

* sudo apt-get install htop -> htop 진행
* 설치되어 있는 program을 update 하고 싶은 경우,
  * sudo apt-get upgrade htop - > htop upgrade
  * sudo apt-get upgrade -> 모든 프로그램 upgrade
* 설치되어 있는 프로그램 삭제
  * sudo apt-get remove htop

### 강의 12
#### Linux - 맥 사용자를 위한 homebrew
* Homebrew
  * 일종의 installer. 앱스토어와 같은 역할을 함
  * 주로 프로그래머들이 사용하는 명령행에서 명령을 통해서 컴퓨터를 제어하는 방식에 사용되는 프로그램을 설치해주는 installer  

* Homebrew 사용하기
  * 먼저 설치를 해야함(MAC에서 하는 방법임)
    * brew.sh 라고하는 주소로 접속
    * 중앙에 있는 코드를 copy
    * 돋보기를 눌러서 terminal이라고 입력
    * 위의 복사한 code를 붙여넣기 해서 설치
    * 원한다면 help 명령어를 통해 확인
    * search 명령어를 이용해서 내가 설치할 수 있는 프로그램이 있는지 확인!

* brew list -> 해당 명령어를 통해 brew를 통해 설치한 프로그램 목록 list를 볼 수 있음
* brew uninstall ~~ 를 이용해서 삭제하면 됨
* update vs upgrade
  * update : upgrade 할 수 있는 목록을 최신화
  * upgrade : 인스톨된 프로그램을 upgrade 시켜 줌

### 강의 13
#### Linux - wget
* 명령어 기반 파일 다운로드 방법
* 보통 GUI에서는 화면에서 다운로드 버튼을 눌러서 파일을 다운로드 받음
* wget 프로그램을 통해 URL을 통한 파일 다운로드가 가능함
* wget을 통한 다운로드 방법
  * 화면에서 우클릭 한 후 Copy link address 를 통해 주소를 알 수 있음
  * wget 'copy link address를 눌러 복사된 주소' 를 입력하면 다운로드 됨
  * 이때 download라는 이름으로 저장이 되는데, mv를 통해 이름 변경

### 강의 14
#### Linux - Source download - git
##### git
 * 버전 관리 시스템 중 하나
 * git은 리눅스에서만 쓸 수 있는게 아니라, 윈도우에서도 쓸 수 있음
 * git을 통해서 프로그램을 만들지 않는다고 할지라도, git을 아는 것이 매우 중요

* github에서 대부분 오픈 소스를 관리하고 있음
* 그래서 오픈소스로 제작된 프로그램은 10 중 9은 github라고 하는 링크가 있음

##### github에 업로드 되어 있는 open source를 자신의 리눅스 컴퓨터로 다운로드 받는 방법
* 1. 그냥 다운로드 받는다
* 2. 버전 관리 프로그램을 IO
*  다운로드 받는 방법이 있음
  * clone or download 라고 하는 버튼 클릭하면 URL이 나옴
    * 이 페이지는 기존 URL과는 다름
    * 이 페이지는 오픈 소스 프로젝트의 소스 코드 URL임(혼동 주의)
    * 해당 URL를 복사를 하고, git 이라는 프로그램을 통해서 해당 소스를 설치 해야함
    * git을 실행시켜봐서 기존에 있는지 확인
    * sudo apt-get install git 으로 설치
    * git clone '복사한 URL 입력 ' '디렉토리'-> 해당 오픈소스를 복제한다는 의미
      * 여기서의 복제는 지금까지 version별로 관리해왔던 모든 소스를 복제한다는 의미

### 강의 15
#### Linux - IO Redirection : output
##### IO
* input, output의 약자
* redirection은 방향을 바꾼다는 뜻을 가지고 있음
* 만약 ls -l 명령어를 이용해서 나온 list를 파일에다가 저장하고 싶으면 어떻게 할까?
  * ls -l 의 결과를 result.log 라는 txt에 저장하고 싶을 때, '>'를 이용하자(redirection)
  * ex) ls -l > result.log
  * 위의 명령어를 치면 아무 결과도 나오지 않는다. 해당 log에 저장되어 있음
  * cat result.log라고 치면 확인 가능

* 화면으로 출력되는 것이 기본인데, 출력 방향을 돌려서 다른 곳에다가 저장 함  
<b/>이를 redirection 이라고 함</b>  
* 해당 이미지 참조**
![img](https://github.com/koni114/TIL/blob/master/Linux/img/Linux_IO.JPG/Linux_IO.JPG)
* 우리가 실행시킨 Unix Process의 결과가 standard output으로 나옴
* unix에서 어떤 프로그램이 실행되면, 그것을 processor라고 하는데, 이 processor가 출력하는 결과를 크게 2가지로 나눔
  * 1. standard output
  * 2. standard error : 프로그램이 어떤 오류가 있을 때, 중요한 정보이기 때문에 별도의 출력으로 보여줌
    * ex) 유효하지 않는 명령어를 날리게 되면 error 문구를 날림
    * ex) rm rename2.txt > result.log 라고 하면 error문구가 txt에 저장될까?  
    결과적으로는 x. output이 redirection이 안됨
    * '>'를 쓰는 것은 standard output을 redirection 했기 때문에 그럼
    * 1> : standard output redirection 을 의미
    * 2> : error output redirection 을 의미
    * 결과적으로 rm rename2.txt 2> result.log 라고 하면 error 문구가 저장됨
    * 두 개다 저장하는 방법은,  
    ex) rm rename2.txt 1> result.txt 2> result.log 라고 하면 됨 !

### 강의 16
#### Linux - IO Redirection2 : input
##### Input 에 대한 내용 설명
~~~
* cat
ex) cat hello.txt
해당 txt 내에 내용을 보여줌
ex) cat
아무것도 보이지 않음. 이때 hi 라고 입력하면 hi 라는 output 출력
ctrl + d 를 눌러 나올 수 있다
~~~
* 하고자 하는 이야기는, cat 이라고 하는 processor는 keyboard 입력을 input으로 받아 standard output으로 출력
* 그렇다면, input 을 redirection 해서 file로 입력 받을 수 있다!
~~~
ex) cat < result.txt
cat에 result.txt를 입력으로 받겠다는 의미
~~~
* cat result.txt vs cat < result.txt
  * cat result.txt는 cat 프로그램에 result.txt라는 인자를 전달 한 것(Command-line Arguments)
  * cat < result.txt는 standard input 으로 cat에게 input을 시킨다는 의미
~~~
* head '보고자하는text'
해당 text의 앞 일부분만 화면에 출력해줌
~~~
* 이러한 Input/output 흘러나가는 형국을 <b/>'IO Stream'</b> 이라고 함

### 강의 17
#### Linux - IO Redirection3 : append
* '>>' 를 쓰면, 기존의 txt에 append되서 redirection 됨
* tip : 명령 실행을 하고 싶지 않으면 ctrl + C를 누르면 됨
* '<<' 여러개의 명령어를 하나로 합친다는 의미
~~~
* ls -al > dev/null
unix에서 dev/null은 쓰레기통 같은 역할
따라서 출력도 하고 싶지않고, 저장도 하고 싶지 않을 때 사용
~~~

### 강의 18
#### Linux - Shell
* Shell vs Kernel
  * Shell : 껍데기라는 의미가 있음
  * Kernel : 핵심, 알맹이라는 의미가 있음

* Shell은 무엇이고, Kernel은 무엇인가?
![img](https://github.com/koni114/TIL/blob/master/Linux/img/Linux_IO.JPG/shell_kernel.JPG)
* hardware : 컴퓨터의 기계적인 부분들. ex) SSD, CPU 등..
* Kernel : hardware를 감싸고 있는데, 물리적인 부분을 직접적으로 제어하는, 가장 중심이 되는 core
* Shell : 사용자가 리눅스에서 어떤 명령어를 입력하면, shell이 입력받아 다시 kernel이 이해할 수 있게끔 해석해줌  
kernel에게 직접 명령하는 것은 굉장히 어렵기 때문에 shell을 통해서 명령함

* 그렇다면 왜 kernel 과 shell을 분리한 것일까?
  * shell이라고 하는 것은 사용자가 입력한 명령을 해석하는 프로그램.   
  kernel과 분리하면 여러가지 shell이 생길 수가 있음. 우리가 선호하는 쉘 프로그램을 선택해서 사용 가능
* 몇가지 종류의 서로 다른 shell을 써보면, kernel과 shell을 구분하기 좋음

### 강의 19
#### Linux - Shell 2 : bash vs zsh
~~~
* echo "hello"
echo는 뒤에 들어오는 문자를 출력하는 명령어
echo $0
shell 중에서 구체적인 제품 중에 하나인 bash를 사용하고 있다는 의미
~~~

* bash vs zsh
  * bash
    * 가장 기본적으로 탑재되어 있음
  * zsh
    * bash가 가지고 있지 않은 추가적인 기능들을 가지고 있기 때문에 좀 더 편리하다 라는 평가를 받고 있음
    * cd + tab키를 누르면 숨김 파일은 안보임
    * 절대경로로 이동할 때 첫번째 알파벳을 각각 치고 tab을 누르면 자동 완성이 됨
* 각각의 사용자들이 취향에 맞는 shell를 선택해서 접근 가능!
* shell이 무엇인지 알게되면, 내가 원하는 shell 을 선택해서 좀 더 최적화된 환경을 구성할 수 있음

### 강의 20
#### Linux - Shell Script 1 : intro
* 여러개의 명령어를 순차적으로 실행해서, 하나의 업무가 이루어 질 수도 있음
* 순차적으로 실행 해야하는 각본, script를 <b/>shell script</b> 라고 함
* 자주 실행하는 명령어들을 하나로 묶어 script로 해놓으면 편리!
* 결과적으로 shell script를 통해 자동화된 프로세스를 처리할 수 있다!라는 결론

##### 예시  
* .log라는 모든 파일을 bak라는 파일에 모두 백업을 받아두고 싶은 경우
  * 명령어 하나하나 실행해보기
~~~
touch a.log b.log c.log
mkdir bak
cp *.log bak (*를 표시하면 확장자가 log 하는 모든 파일을 지칭 : wildcard)
ls -l bak
~~~

### 강의 21
#### Linux - Shell Script 2 : example
* 실제 예시를 직접 작성해보기
~~~
echo $0 -> echo 명령어를 통해 shell 확인
nano backup
 #!/bin/bash
if ! [ -d bak ] then
      mkdir bak
cp *.log bak
~~~
* bash라는 프로그램은 어디있을까? -> ls /bin
bin 디렉토리 밑에 있는데, unix에 기본적으로 탑재되어있는 프로그램들이 들어가 있음
-> 운영체제는 밑에 작성되는 코드들이 bin 밑에 있는 bash 라는 프로그램을 통해 해석되어야 한다는 사실을 말함
* nano memo에서 해당 script를 생성시키고 저장을 한 뒤 실행 시키면 permission denied라고 나옴  
~~~
* chomd : 권한 변경
chmod +x backup
** x : excutable (실행가능한)
~~~

### 강의 22
#### Linux - Directory structure 1
* 명령어 시스템에서는 디렉토리라고 하는 것이 굉장히 중요
* 이번 시간에는 최상위 디렉토리(root) 밑에 있는 기본 디렉토리의 기능을 알아보자
* bin
  * User binaries
  * bash, nano, chmod, pwd, ps, rm 등 여러가지 프로그램들이 존재
  * 컴퓨터에서는 실행 가능한 프로그램을 줄여서 <b/>binary, bin</b> 이라고도 함
* sbin
  * system binaries
  * reboot, shutdown .. 등
  * 컴퓨터를 재부팅하거나, 시스템 관리자, root user 들이 사용하는 프로그램들이 들어가 있음  
* etc
  * Configuration(설정) files
  * 여기서 말하는 설정은 어떤 프로그램이 있을 때, 그 프로그램이 동작하는 방식을 바꾸고 싶을 때 설정을 바꿈
  * 리눅스에서 설정을 바꾸는 것은 UI에서 설정을 바꾸는 것이 아니라, file을 바꾸는 것임
  * 만약 내가 설치한 프로그램 설정을 바꾸고 싶을 때, etc file에 있을 것이다! 라고 생각할 수 있음
* dev
  * Device files
* proc
  * process information  
* var
  * Variable(바뀔수 있는) Files
  * 해당 디렉토리 밑에 있는 파일들은 프로그램이 동작하는 과정에서 error가 발생하거나, 누군가가 접속을 하면 내용이 바뀜
  *
* tmp
  * Temporary files
  * 임시 파일들. 컴퓨터가 reboot가 되면 자동으로 내용이 삭제됨

### 강의 22
#### Linux - Directory structure 2
* home
  * 사용자들의 디렉토리
  * home 밑에 사용자의 파일들이 저장되는 디렉토리
  * '~' 를 사용하면 home 위치의 디렉토리를 말함
* lib
  * bin, sbin의 실행을 도와주는 library file이 저장되어 있는 디렉토리
* opt
  *  optional add-on Applications
  * 소프트웨어를 설치할 때, apt-get 같은 경우는 자동으로 적당한 directory에 위치하게 됨
  * 경우에 따라서 특정 디렉토리를 지정해야 하는 경우도 있음
  * opt 밑에 설치하는 것도 좋은 방법
* usr
  * User systems
  * 해당 디렉토리 밑에는 bin, sbin, lib, local이라고 하는 디렉토리 존재
  * usr/bin 디렉토리는 우리가 설치하는 프로그램들은 usr 밑에 설치가 되고, 기본적으로 unix 계열에 설치가 되어서 bundle 형식으로 사용자에게 제공되는 프로그램들은 bin 밑에 설치된다 라고 생각하자

### 강의 23
#### Linux - File find 1: locate, find
* file에 대해서 좀 더 깊게 이해해보기
* file의 2가지 용도
  * 데이터를 보관하기 위한 용도
  * 해야할 일에 대한 명령을 보관하고 있는 용도(실행파일)
* file을 찾는 방법
~~~
* locate [찾고자하는 파일의 이름]
ex) locate *.log
컴퓨터에 존재하는 모든 log 파일을 출력해 줌
locate 명령어는 디렉토리를 뒤지지 않고 DB를 뒤짐
따라서 훨씬 더 빠르게 파일을 찾아올 수 있음
여기서 DB를 <b/>mlocate</b> 라고 부름
sudo updatedb 를 통해 리눅스 컴퓨터에 대한 여러가지 정보들이 update 할 수 있는데
보통 하루에 한번씩 정기적으로 update 됨
~~~
~~~
* find
디렉토리를 뒤져서 파일을 찾음
현재 상태를 가져올 수 있지만, 다소 느릴 수 있음
다양한 사용법이 있기 때문에 좋음
사용법이 굉장히 복잡하기 때문에 따로 공부를 해야함. 몇가지만 알아보자
ex) find . -type f -name tecmint.php
. : 현재 디렉토리에 있는 파일을 찾음
type f : 파일의 확장자를 지정.  file을 찾는다는 의미
ex) find . -type f name "tecmint.txt" -exec rm -f {} \;
해당 이름의 file을 찾아 삭제해라
{} : 앞에서 검색한 파일의 이름이 위치하게 됨
~~~
### 강의 24
#### Linux - File find 2 : whereis, $PATH
*  whereis 명령 사용방법
~~~
* whereis
원하는 파일을 찾아주는데, 실행 파일을 찾아줌
ex) whereis ls
result : /bin/ls /usr/share/man/man1/ls.1.gz
ls라고 하는 실행파일의 위치를 찾아줌
/bin/ls : ls 프로그램이 해당 위치에 존재
/usr/share/man/man1/ls.1.gz : 해당 위치에 매뉴얼이 존재
~~~
* whereis 메뉴얼에서, whereis locates the binary, source and manual files for the specified command names. 라고 되어 있음
* 이 때 파일 전체를 뒤지는게 아니라, $path, $manpath 를 뒤짐
##### PATH
* 우리가 ls라는 명령어를 실행할 때, 해당 프로그램을 실행하는 것인데, 해당 디렉토리에 ls라는 프로그램이 없어도 실행되는 이유는 PATH라고 하는 변수 때문
* PATH는 변수고, 변수에는 데이터가 들어가 있는데, echo $PATH 라고 치면 데이터가 보인다.
* 데이터를 보면 :를 기준으로 연결되어 있는데, 이것들은 경로임
* $PATH는 리눅스에서 내장되어 있는 변수임
* 우리가 ls 명령어를 사용하면, PATH안에 담겨있는 경로에 ls가 있는지 차례대로 뒤짐
* 해당 명령어가 발견되면 실행됨
* PATH를 수정해서 경로를 추가한다면, 해당 경로에 있는 프로그램도 명령어만으로 호출해서 실행시킬 수 있음
* 이런 변수를 <b/>환경변수</b> 라고 함

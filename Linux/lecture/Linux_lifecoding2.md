### 강의 27
#### Linux - process 1 : Computer structure
* process가 무엇인가?
  * command, rm, mkdir,top 같은 것들은 명령어인데, 명령어들은 bin, sbin 파일 형태로 스토리지에 존재  
  이를 프로그램이라고 함
  * 이 프로그램이 실행되면 메모리에 적재되고, 이를 CPU가 처리. 이때 메모리에 띄어져 있는 프로그램을 process라고 함  
* Hardware에 대한 얘기를 해보자
![img](https://github.com/koni114/TIL/blob/master/Linux/img/processor.JPG)
  * SSD, HDD 라고 하는 것들이 있는데, 이는 저장장치임 -> 스토리지라고 함
  * RAM 같은 것들은 memory라고 함
  * CPU는 processor라고 함
* memory나 storage는 공통적으로 데이터를 저장한다는 것에 있음
* 이러한 저장장치가 다르게 공존하는 이유는 최고의 memory를 만드는 것을 인류가 도달하지 못하였기 때문
* 스토리지 vs 메모리
  * 스토리지
    * 가격이 싸고, 용량이 크고, 속도가 매우 느림
    * 프로그램은 스토리지에 깔려있음
  * 메모리
    * 가격이 비싸고, 용량이 작고, 속도가 매우 빠름
* CPU가 동작할 때 굉장히 빠르게 동작하는데, 스토리지가 가지고 있는 처리속도로는 CPU 처리속도를 따라올 수없음
* 프로그램은 스토리지에 깔려있는데, 이 프로그램을 읽어서 메모리에 적재 시킴. 그리고 실행되지 않는 프로그램은 적재 시키지 않음
* 메모리에 올려있는 프로그램을 CPU가 읽어서 동작한다음에 데이터를 처리

### 강의 28
#### Linux - process 2 : ps top htop
~~~
* ps
프로세스 리스트를 보여줌
ex) ps aux
백그라운드에서 돌아가고 있는 모든 프로세스를 보고 싶을 때 사용
ex) ps aux | grep apache
apache 라고 하는 텍스트를 포함하고 있는 프로세스 출력
ex) sudo kill 22142
22142 라고 하는 PID를 강제로 죽임
** PID : process ID
~~~
##### top/htop program
* MEM% : 물리적인 메모리 크기
* RES : 실제적인 메모리 크기
* COMMAND : 해당 프로세스를 실행 시키는 명령어
* CPU core 수 등을 확인 가능
* Load average : CPU 점유율과 관련된 것
  * 첫 번째 자리 : 1분간의 CPU 점유율
    * ex) 8 : 총 7개의 processor가 대기를 하고 있다는 의미
  * 두 번째 자리 : 5분간의 CPU 점유율
    * ex) 위와 동일한데 5분간의 통계
  * 세 번째 자리 : 10분간의 CPU 점유율
    * ex) 위와 동일한데 10분간의 통계
* core가 4개인데 위의 load average 숫자가 4개면 잘 사용하고 있다!는 의미
  core가 4개인데 위의 load average 숫자가 1개이면 코어 4개 중 1개만 일을 하고 있다는 의미


### 강의 29
#### Linux - background execute (Ctrl + Z, &)
* 독특한 실행 방법에 대해서 설명
* 2개의 창이 있다고 하자. 왔다갔다 하면서 수행을 할 수 있는데, 이를 <b/>멀티 테스킹</b>이라고 함
##### ctrl + z
* 우리가 예를 들어 nano에서 html file을 작성하고, 다른 작업을 수행하고 싶을 때
나갔다가 다시 들어오면 불편하므로, ctrl + z 를 누르면 프로그램을 종료하지 않고 다른 작업을 수행 할 수 있음
~~~
fg
background에 있는 프로세스가 foreground로 수행 됨
fg %2
background에 있는 2번 프로세스가 수행 됨
jobs
background로 수행되고 있는 process가 보임
jobs 에서 + 로 표시된 프로세스가 fg 명령어 수행시 foreground로 나오는 프로세스
-로 표시된 프로세스는 + 프로세스가 종료된 다음 foreground 로 나오는 프로세스를 의미!
kill %4
정상적으로 종료하는 방법. 종료가 안될 수도 있음
kill -9 %4
더 강력한 종료 방법. killed 라고 뜸
ls -R
현재 디렉토리 밑에 있는 모든 파일과 디렉토리를 보여줌
ls -alR / 1> result.txt 2> error.log &
프로그램을 실행 할 때부터 background로 보내고 싶은 경우 제일 뒤에 & 를 쓰면 바로 다음 명령어 수행 가능
이 때 jobs를 수행하면 running 이라고 표기
~~~
### 강의 30
#### Linux - daemon 1: intro
* 항상 실행되고 있는 프로그램을 <b/>daemon 프로그램</b>이라고 말함
* ls, mkdir, rm 이런 것들은 데몬 프로그램이 아님
* 비유하기 : 냉장고 vs TV
  * 냉장고 : 항상 틀어져 있어야 함. daemon 프로그램과 비슷 ex) server
  * TV : 필요할 때만 키면 됨 ex) ls, mkdir, pwd 등

### 강의 31
#### Linux - service와 자동 실행
* daemon 중 하나로써 web server를 설치해보자
* 가장 대표적인 web server로는 <b/>apache tomcat</b> 이 있음
##### web server 설치 예제
~~~
sudo apt-get install apache
~~~
* 우선적으로 apache 설치
* apache는 etc/init.d에 설치되어 있음
* etc directory는 daemon의 프로그램들이 설치되어 있는 디렉토리
* 해당 프로그램을 켜고 끄는 것은 일반적인 프로그램과 다름
~~~
sudo service apache2 start
~~~
* apache2 daemon 프로그램 시작 명령어
~~~
ps aux | grep apache2
~~~
* apache2 서버 실행 확인
~~~
sudo service apache2 stop
~~~
* apache2 서버 실행 정지
* daemon으로 실행되는 모든 프로그램은 전부 start, stop으로 키고 끌 수 있음
* daemon들 중 일부분은 컴퓨터가 실행 될 때 자동으로 실행되어야 하는 것들이 있음
  * ex) web server
  * etc/r(OS에 따라 rc.d 일수도 있음)/rc0.d, rc1.d ... 등 디렉토리가 보이는데
      * rc3.d : CLI인 경우
      * rc5.d : GUI인 경우
* 들어가서 ls -l을 해보면 리스트가 보임
  * 리스트에는 우리가 설치한 apache2도 보임
  * 제일 앞에 l 이라고 되어 있음
  * S02apache2라는 링크가 있고, 이 링크는 오른쪽 ../init.d/apache2가 있다는 의미
* S02apache2
  * S : 컴퓨터가 실행될 때 자동으로 실행
  * K : 자동으로 실행
  * 02 : 우선 순위
* 따라서 만약에 daemon 프로그램이 자동으로 부팅됐을 때 실행하고 싶은 경우
/etc/rc3.d 내 해당 프로그램 링크를 걸면 됨

### 강의 32
#### Linux - Time based job shedule cron 1 : usage
* cron에 대해서 알아보자  
  정기적으로 명령을 실행해주는 소프트웨어
* 우리가 하다보면 정기적으로 일을 처리해야할 필요성이 있음
ex) 정기적으로 data를 백업한다던지.. 등
* cron을 사용
  * crontab -e : 사용하고자 하는 일을 정의할 수 있음
  * m(실행되는 분의 주기 ex) 10 : 매시간 10분)
  * h(실행되는 시간의 주기)
  * dom(day of month, 1달 중 며칠인지)
  * dom(요일)
##### 메모장(nano) cron을 이용해서 log 남겨보기
~~~
*/1 * * * * date >> date.log
~~~
* 1분 단위로 date batch 등록
~~~
crontab -e
~~~
* 현재 실행되고 있는 정기 batch job을 확인 가능
~~~
tail -f date.log
~~~
* date.log file의 마지막 몇 부분만 확인
~~~
*/1 * * * * date >> date.log 2>&1
~~~
* 표준 error를 표준 출력으로 바꿈(&를 붙여주어야함)

### 강의 33
#### Linux - Time based job shedule cron 2 : example
##### 사례설명
* 웹을 사용하는 사용자가 어떤 작업을 수행한 후 100,000명에게 메일을 보내야 하는 process가 있다고 하자
* 일반적인 경우 사용자는 100,000명에게 메일이 보내는 작업이 끝날때까지 기다려야 함
* 이 때 saved라는 작업 process를 cron이 주기적으로 갱신이 됐는지 확인하면서 메일을 보내는  
background를 만들어두면 사용자는 불편하게 기다리지 않아도 다음 process를 진행할 수 있음

### 강의 34
#### Linux - Startup script bashrc
* shell이 실행됐을 때 특정 명령어가 자동으로 실행되게끔 하는 방법 설명
  * shell의 startup 설정이라고 부름
~~~
* alias
* alias l='ls -al'
~~~
* l 이라고 입력하면 ls -al 명령어가 수행됨
##### shell 실행 시, 특정 명령어 수행 방법
* shell 실행 시 bashrc code를 실행하도록 약속되어 있음
* bash 문법에 따라서 작성된 코드
* 이 소스 제일 하단에 'Hi bash'를 입력
~~~
bash
~~~
* Hi, bash가 뜨는 것을 확인 할 수 있음
~~~
exit
~~~
* 종료
* 그 외에 할 수 있는 것들
  * prompt 정보 형태 변경
  * PATH 값을 변경한다던지, 이런 것들을 시작 할 때 자동으로 setting해 줄 수 있음

### 강의 35
#### Linux - Multi user 1 : intro
* 다중 사용자
* 각자의 ID로 사용하게 되면 trade-off 현상 발생
  * 단점
  시스템의 복잡도는 훨씬더 높아짐  
  어떤 행위에 대해서 누군가가 해도 되는지   
  하면 안되는지에 대한 권한 체크가 들어가기 때문
* 리눅스는 기본적으로 다중 사용자의 개념이 들어가 있기 때문에 어느정도 알고 있어야 함

### 강의 36
#### Linux - Multi user 2 : id, who
~~~
id
~~~
* uid : user Id
* gid : group Id
* 보통 prompt 제일 앞에 나오는 문자가 일반적으로 ID에 사용됨
~~~
who
~~~
* 이 시스템에 누가 접속되어 있는지 알 수 있음

### 강의 37
#### Linux -Root user
#####  super(root) user vs user
* root user는 강력한 사용자, user는 일반 사용자
* super user 라는 구체적인 사용자도 존재한다
* 일반적으로 super user는 root 라는 이름을 가지고 있음
* prompt에 $ 표시가 있으면 일반 user라는 의미를 내포하고 있음
  * super user는 #으로 표기
* ubuntu 같은 경우 일반적으로 super user가 되는 방법이 막혀있음
~~~
su
~~~
* a라고 하는 사용자에서 b라는 사용자로 변경하거나,  
super user가 되고 싶을때 해당 명령어 사용  
~~~
su - root
~~~
* 비밀번호 물어봄
* 항상 super user 계정일 때는 항상 조심해야함. 특히 서버인 경우 더욱더 조심해야함
~~~
exit
~~~
* 다시 이전 사용자로 변경
##### root 사용자 rock 푸는 방법
~~~
sudo passwd -u root
~~~
* -u : unlock의 약자
* 한번도 root 사용자를 사용하지 않은 경우, passwd를 2번 입력해야함
*  다시 rock을 걸고 싶은 경우
~~~
sudo passwd -l root
~~~
*  root 사용자로 접속했을때, dir이 /root
* 일반 사용자의 dir은 /home/ 에 위치

### 강의 38
#### Linux -Add user
~~~
sudo useradd -m duru
~~~
* 명령을 실행한 사람의 password 입력
* home 밑에 duru dir 생성
~~~
su - duru
sudo passwd duru
~~~
* passwd 입력
~~~
sudo pwd
~~~
* sudoers file에 존재하지 않는다고 나옴
* egoing 계정에서 duru 계정을 sudo 명령을 주자
~~~
sudo usermod -a -G sudo duru
~~~

### 강의 39
#### Linux - Permission 1: basic
##### File & Directory
* 파일과 디렉토리에 대해서 읽기, 쓰기, 실행에 대한 권한을 지정할 수 있음   
-> Permission  
* 다음의 출력문을 알아보자
* -rw-rw-r-- 1 egoing egoing 0 Dec  4 23:19 perm.txt
  * -: type. -   : 가장 기본적인 파일, d : 디렉토리, l : link 등
  * rw-rw-r--  : access mode
  * rw- : owner의 권한, 읽고(r) 쓸 수(w) 있다는 의미
  * rw- : group의 권한
  * r--  : other의  권한
  * r : read, w : write, x : execute
  * egoing : owner
  * egoing : group



### 강의 40
#### Linux - Permission 2 : chmod
##### 권한을 변경하는 방법 - chmod(change mode)
~~~
chmod o-r perm.txt
~~~
* perm.txt의 other 권한의 read 를 빼고 싶은 경우 명령어
* 해당 명령어 수행 후 소유자가 아닌 other가 수행하면 permission denied 발생
~~~
chmod o+r perm.txt
~~~
* perm.txt file에 other에 read 권한을 추가하겠다는 의미
~~~
chmod o+w perm.txt
~~~
* perm.txt file에 other가 수정할 수 있게끔 한다는 의미
~~~
chmod u-r perm.txt
~~~
* 소유자의 read 권한을 제거

### 강의 41
#### Linux - 실행의 개념과 권한 설정 - execute
##### 실행이 무엇인가
* x : execute, 파일에 대해서 실행가능한 파일로 할 것인지를 결정하는 요소
##### 실습
~~~
nano hi-machine.sh
~~~
* hi-machine 이라는 shell script  생성
~~~
#!/bin/bash
echo 'hi hi hi hi'
~~~
* script 내에 간단한 문구 넣기
~~~
ls -l
~~~
* hi-machine.sh이 생성된 것을 확인
~~~
./hi-machine.sh
~~~
* 해당 스크립트 실행하면 permission denied
* 만약 /bin/bash hi-machine.sh 를 수행하면 정상적이게 되지만, hi-machine.sh가 있는 디렉토리에서 ./를 이용해서 실행하면 error가 발생
* 어떤 특정 프로그램(해석기, parser)를 통해 프로그래밍 언어를 실행시키는 것은 아무런 제약은 없지만 행문을 통해서 실행하려면 e 권한을 주어야 함
~~~
chmod u+x hi -machine.sh
~~~
* 초록색으로 표기되면 실행가능하다는 것을 의미

### 강의 42
#### Linux - permission 4 : directory
~~~
mkdir perm
chmod o-r perm
ls -l perm
~~~
* 결과적으로 permission denied 발생
* 해당 디렉토리의 권한 중 write 권한이 없으면, 내부에 새로운 file 생성이 안됨
* file의 이름 변경도 안됨
* 실행권한은 cd 와 같은 명령어를 통해 들어갈 수 있느냐 없느냐와 관련이 있음
~~~
chmod -R o+w perm
~~~
* 디렉토리 밑에 있는 모든 file의 권한 변경 원하는 경우
* R : recursive의 의미

### 강의 42
#### Linux - group 1 : intro
* 사용자가 아닌 특정 사용자에게 권한을 주고 싶을 수 있음
* 권한을 주고 싶은 사람에게 group으로 묶는다
* Group : developer, designer 등 이름을 주고 , file에 group을 부여함
* group은 중요하지 않음. linux는 다중 사용자이기 때문에 group 개념이 있지만 자주 사용되지 않음
##### 실습
* 그룹에 속한 사람들은 특정 파일을 수정할 수 있도록 하고, 아닌 사람들은 못하게 하는 실습해보자
* group을 developer 로 지정하도록 해보자
~~~
cd var
mkdir developer
sudo echo 'hi, egoing' > egoing.txt (denied)
~~~
* 개발자들이 사용하는 디렉토리를 생성하려고 하면 denied
why? 현재 디렉토리 권한은 root에게 있기 때문
~~~
sudo mkdir developer
cd developer/
~~~
* file 생성시 root 권한이 필요한데, root라고 잡혀있는 group을 변경해보자
~~~
groupadd developer(denied)
sudo !!
~~~
* !! : 직전에 명령했던 명령어를 지칭함
~~~
nano etc/group
~~~
* 해당 script 내 developer가 추가되었음을 확인
~~~
usermod -a -G developer egoing
sudo !!
sudo -a -G developer k8820
~~~
* usermod(modify) : 사용자를 수정
* a(append) : 추가한다는 의미
* G(group) : group
~~~
cd /var/developer/
~~~
* group을 만들었으므로, developer로 이동
* 해당 dir의 권한을 보면 root 권한을 가지고 있음
~~~
sudo chown root:developer .
~~~
* chown : change file owner and  group
* 현재 디렉토리의 소유자가 developer로 바뀐 것을 확인 가능
~~~
sudo chomd g+w .
echo 'hi,egoing' > egoing.txt
~~~
### 강의 43
#### Linux - internet 1
* 주소창에 입력하는 주소 -> domain name이라고 함  
이 때 IP address를 통해서도 접속이 가능
~~~
ping google.com
~~~
* google.com 의 IP address를 알 수 있음
* 즉 구글에 접속하기 위해선 2가지 방법 모두 사용가능
* DNS Server : domain name이 어떤 ip와 mapping되어 있는지 저장되어 있는 거대한 server
* 즉, 우리가 google.com 이라고 치면 DNS Server에 접속해 ip address를 응답받고 이를 호출

### 강의 44
#### Linux - internet 2
* 특정 컴퓨터를 서버로 사용하곳 싶다면 우선적으로 자신의 ip를 알아야 함
~~~
* ip
ip addr
~~~
*  inet의 문자가 있는 부분을 찾아보면 자신의 ip addr를 알 수 있음
* ipinfo.io 에 접속하면 우리의 ip addr를 알려줌
~~~
* curl
curl ipinfo.io/ip
~~~
* shell 환경에서 ip addr를 아는 방법 -> curl 명령어 이용
* ip addr 과, curl 의 결과가 다를 수 있음
  * ip addr은 컴퓨터가 실질적으로 가지고 있는 ip가 무엇인지 알아내는 방법
  * curl : 온라인 서비스 입장에서 접속된 결과적인 ip가 무엇인지 알아내는 방법
  * 즉 다를 수도 있고 같을 수도 있음
  * 같다면, 내부와 외부 접속 ip가 서로 같다는 의미
  * 많은 경우에 두 가지가 다르다
*   public address / private address

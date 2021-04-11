## chapter22 - branch 정보확인
- 상당한 복잡성을 가지고 있음.
~~~
git log --branches --decorate
~~~
- branch 사이의 차이점 파악 방법.
  - git log --branches
    - checkout 되어있는 branch 말고 저장소에 있는 모든 branch를 보여줌
  - --decorate
    - -> HEAD가 있는 곳이 checkout 되었다는 의미
    - -> HEAD라는 file에 checkout 위치가 기록되어 있음.

~~~
git branch --graph
~~~
- --graph 명령어를 뒤에 붙이면, log 에서 조상이 어딘지를 알 수 있음
  - git log --branches --decorate --graph  
   --> oneline 형태로 log를 확인할 수 있음.

- git 사용시 command line을 사용하는 이유는 가치가 있기 때문

- stree GUI tool
  - 현재 디렉토리의 저장소가 sourcetree GUI tool로 실행됨.
  - command line 에서 확인하기 힘든 graph 를 GUI로 잘 보여줌~
~~~
git diff master..exp
~~~
- version 과 version 사이의 차이 확인  
- master에는 있고, exp는 없는 차이를 확인 가능.
~~~
git diff master..exp -p
~~~

- -p를 붙이면 source code의 차이를 알 수 있음.


## chapter23 - branch 병합 - merge
- exp의 내용을 master로 옮기는 방법(master 내용을 exp로 옮기는 것이 아님)
  - master로 checkout을 한 후, merge 명령어 수행
~~~
git merge exp
~~~
  - 위의 명령어를 수행하면, Merge branch 'exp' 라는 명령어와 함께 commit 명령어가 뜸
  - graph에서 확인해보면, master의 최신 commit이 됨.

~~~
git branch -d exp
~~~
- branch를 지우는 방법  
  --> exp branch가 삭제가 됨.  


## chapter24 - branch 수련
- branching 방식은 상황에 따라 여러 방식 존재
  - past forward
  - non-past forward
~~~
git checkout -b iss53 
~~~
- iss53이라는 branch 생성과 동시에 checkout  

- fast forward(빨리 감기)  
  - master branch에서 hotfix가 독립한 이후에, master branch는 어떠한 commit도 만들지 않음  
  - 중요한건, 별도의 commit을 생성하지 않고, master가 가리키는 commit이 hotfix로 변경됨  
  - 이 떄 hotfix를 지움  
  - 다음으로 issue53을 수정하고, master branch로 merge하려고 함
    - 이 때는 fast forward를 할 수 없음. master branch는 변경되었기 때문
    - 이 떄는 iss53과 master branch의 공통 조상을 찾음
    - 두 개를 합쳤다라는 정보를 담고있는 별도의 commit 을 담고 있음
- 결과적으로 fast forward는 commit id를 생성하지 않음
- non-fast forward는 commit id를 생성함.

## chapter25 - stash
- stash는 감추다, 숨겨두다 라는 뜻을 가지고 있음
- 내가 특정 branch에서 수정을 하고 있는데, 수정을 다 마치지 않은 상태에서   
  다른 branch로 checkout을 해서 작업을 해야하는 경우가 발생  
- 바로 checkout을 하게 되면 경고 문구가 뜸
- 이 때 stash를 사용하여 숨겨둘 수 있음.  
  그렇게 되면 가장 최신의 commit 상태로 적용하여 깔끔하게 branch 상태를 만들어낼 수 있음

- 실습 예제
- 파일 수정 후, 다른 branch로 이동
~~~
vim test.txt         # test.txt file 생성
git checkout -a exp  # exp로 branch 이동 
vim test.txt         # exp * 인 상태에서 test.txt 수정
git checkout master  # master로 checkout
git status           # master로 이동했음에도 불구하고, test.txt가 수정되었다고 메세지 뜸 
~~~
- git stash 예제
~~~
git stash + [내가 행하고자 하는 일의 명령어]
~~~
- exp branch에서 git stash 명령어 수행하면,
  - Saved working directory and index state WIP(working in process) on exp: ~~~  
  --> exp 에 작업중인 변경사항들의 정보들이 save됨을 알 수 있음. 
- 이후에 commit 을 해보면, 다른 message가 안뜨는 것을 알 수 있음.

~~~
git stash apply 
~~~
- stash로 감춰두었던 파일을 다시 복원  
~~~  
git reset --hard HEAD 
~~~
- 가장 최신 commit 상태로 working 상태를 복원.  
- git status 를 해보면, 아무것도 안나오는 것을 확인.  
  그렇다면, stash 내용까지 다 없어진걸까? --> NO! 
~~~
git stash list
~~~ 
- git stash list 명령어를 통해 확인할 수 있고, apply 를 통해 다시 복원 가능  
- git stash list --> stash한 내용을 확인할 수 있고  
  git stash apply 하면 없어짐  

- 즉, 내가 stash 명령어를 통해 숨겨둔 파일 내역은 내가 직접 삭제하지 않는이상, 항상 살아있음  

- 이 떄 내가 한번더 파일을 수정해서 stash를 하면,  
  stash list에 가장 상단에 있는것이 가장 최신에 명령한 stash임  

- git stash apply 명령어를 날리면    
  가장 위의 stash를 복원함.  

- git stash drop --> 가장 최신 stash가 삭제됨.  
- ; 를 붙이면 command line 을 한줄에 여러개 사용 가능.  

~~~
git stash pop
~~~
- apply + drop 까지 되는 명령어!  
- git stash 라는 명령어는 최소한 version 관리가 되고 있는 파일에 한해서만 적용됨.  
  즉 working directory 에 file이 올라와 있어야함(add)


## chapter27 - branch 원리
- HEAD 파일 - git init시 최초로 생성되며, 디렉토리는 refs/heads/master 라고 하는 directory가 명시되어 있음.
- 해당 directory는 commit 수행시 해당 directory 가 생성되고, 그 안에는 commit object id가 들어가 있음.
- master branch에서 commit을 수행하면, HEAD 내에 object Id도 마찬가지로 바뀜.

- 즉, HEAD를 통해 commit의 최신 버전을 알 수 있음.  
- branch 명령어를 통해 또다른 branch 생성시, refs/heads/exp 라는 directory가 생성됨.  
  --> 이를 지우면, branch 는 사라짐.  
- 파일은 바이너리가 아니라, 일반 텍스트임!  

- branch가 바뀌면? 
  - HEAD 파일이 바뀜 --> exp를 가리킴  

## chapter27 - branch 충돌 해결
- 각각의 branch에 같은 이름의 파일을 새로 생성한 경우 문제가 발생함.
 - ex) common.txt라는 파일을 exp와 master branch에서 각각 다른 부분을 수정한 경우,
 
   -> 각 branch 수정한 부분이 다른 경우, 자동으로 merge가 됨
   -> 각 branch에서 수정한 부분이 같은 경우, 
     - conflict (content) : Merge conflict in common.txt
     - git status 수행시, Unmerged paths: ~~ 라고 나옴.

- ======= 를 기준으로, <<<<<<<< HEAD 라고 되어 있는 부분은 내가 지금 checkout되어 있는 branch의 수정사항
- '>>>>>>> exp' 라고 되어 있는 부분은 checkout 되어 있지 않은 branch의 수정사항임.  
   -> 즉, git은 자동으로 merge 할 수 없는 부분에 대해서 우리에게 위임함  
   -> 이 부분을 바탕으로 병합을 잘 수정해야한다는 것임.   
   -> 수정을 한 후 다시 commit 하면 정상적이게 merge가 됨!  

 
## chapter28 - reset checkout
- checkout을 통해 과거로 돌아가는법을 알아보자.
- ex) 내가 version 3에 해당되는 commit으로 돌아가고 싶다면? 
~~~
git reset --hard "version 3에 해당하는 commit id 명"
~~~

- 해당 명령어를 내렸을 때, 어떤 변화가 있는지 살펴보자
  - refs/headers/master file이 수정  
    version 3의 commit이 master로 되어 있음
- reset을 한다는 것은 checkout 이 가리키고 있는 최신 commit을 바꾸는 행위
- 만약 reset을 취소하고 싶다면?
  - ORIG_HEAD file : 우리가 삭제한 4번을 가리키고 있음  
  git은 위험한 명령을 내렸을 때 해당 file에 기록을 해둠
  - logs/refs/headers/master : 우리가 삭제한 commit id가 최신 commit id가 되었다는 history 정보가 담겨있음

- 그렇다면, reset 명령어를 취소해보자
~~~
git reset --hard ORIG_HEAD 
~~~
- log에는 ORIG_HEAD 보다 log에 더 자세한 정보가 담겨있음
~~~
git reflog
~~~
- 내가 했던 행위들의 log가 기록되어 있음
- 내가 만약 reset을 취소하려면, log 정보의 code나 Head@{n}를 이용하면됨
- git commit 명령어 뒤에 commit id를 붙일 수도 있음
~~~
git commit [commit id명] # HEAD file에는 commit id가 직접 작성됨
git checkout master # HEAD file에는 ref directory가 작성됨
~~~
- HEAD의 commit id가 바뀌었음을 확인 가능
- HEAD file에는 commit id가 직접 적혀있음. --> detached 된 상태
  
## chapter29 - GIT_원리: working copy&index&repository
- git reset 명령시 option은 여러가지가 있음
- reset의 option(hard, mixed, soft)들은 어떤 의미를 가지는 것인지를 먼저 살펴보자
 ![img](https://github.com/koni114/git-from-the-hell/blob/master/img/reset.JPG)
  - git reset --soft : repository 에 있는 내용만 reset
  - git reset --index : repository, index에 있는 내용만 reset
  - git reset --hard : repository, index, working tree에 있는 내용 모두 reset
- 개념만 확실히 인지하고, 익숙한 것 하나만 사용하면 됨
- 가장 중요한 것은 working copy vs index vs repository 간의 관계는 매우 중요!

## chapter30 - GIT_원리: merge & conflict
- conflict라는 현상이 발생했을 때, git은 내부적으로 어떤 일을 하는지 알아보자
- conflict를 해결하는 방법인 3-way merge 기법이 어떻게 동작하는지도 알아보자
~~~
# exp 라는 branch를 만들고, master와 exp에 동일한 소스 내용을 각각 다르게 수정
git init
vim text.txt # 해당 text file 생성
git commit -am "1"

git branch exp
vim text.txt # 해당 text file 수정
git commit -am "common -> exp"

git branch master
vim text.txt # 해당 text file 수정
git commit -am "common -> master"  

git merge exp # auto merge error
~~~
* 이런 충돌이 일어날 때 git에서는 어떤 일이 일어나는지 확인해보자
* index file 살펴보기
  * 1,2,3 이라는 숫자가 붙은 t1.txt file을 볼 수 있는데  
  각 내용을 확인해보면  
  1 --> common  
  2 --> master  
  3 --> exp  
  로 구성되어 있음. 이를 통해 3-way merge 방법이 이루어짐
* 3개의 종류에 따라 git은 자동으로 병합 작업을 수행
* MERGE_HEAD : merge가 될 대상의 최신 commit
* ORIG_HEAD  : merge 이전으로 돌아가기 위한 file 
* 충돌이 일어난 file에 대한 내용이 적혀있음

* 병합을 전문적으로 해주는 도구를 사용해보자  
--> kdiif3 라는 open source
  * 화면에서 A,B,C 중 하나를 선택하거나, 수정하여 저장할 수 있게 함
  * file이 자동으로 'add' 됨
  * f1.txt.orig file이 자동으로 생성되는데, 지우면 됨
~~~
git config --global merge.tool kdiff3 # setting 방법은 운영체제마다 다름
git mergetool # 충돌난 file에 대해서 merge tool을 이용해서 병합하도록 명령
~~~

## chapter31 - GIT_원리: 3 way merge
- 이미지 참고
![img](https://github.com/koni114/git-from-the-hell/blob/master/img/3_way_merge.JPG)
- merge방법에는 2-way merge 방법과 3-way merge 방법이 존재
  - 2-way : base를 제외한 Me와 Other만 비교
  - 3-way : base, Me, Other 3개를 비교
- 3-way merge같은 경우는 내가 수정하지 않고 다른 사람이 수정했을 경우는 충돌 안남!

## chapter32 - 원격 저장소
- remote repository라고 함 
- local repository랑은 대비되는 개념
- 원격 저장소는 중요한 두가지 개념을 가짐
  - 내 버전을 백업함
  - 다른사람과 협업을 함
- 만약 혼자 project를 진행한다면, dropbox나 google drive를 사용하면 됨.

## chapter33 - 원격 저장소 생성
- 원격 저장소 생성 방법에 대해 알아보자
- 일단, 혼자 project 하는 것 처럼 해보자
~~~
git init local # local 이라는 이름의 저장소 생성
cd local       # local로 이동

vim f1.txt
git commit am "1"
~~~
- 실제로 인터넷에 원격 저장소를 생성하는 것은 다소 복잡하기도 하고,  
이 복잡성 때문에 응용력이 떨어질 수 있으므로  
한 대의 컴퓨터 안에서 다른 디렉토리 안에다가 원격 저장소를 만들고  
원격 저장소에 commit 하는 예제를 진행해보자

~~~
cd .. 
git init --bare remote # bare는 작업을 할수 없고 저장소의 기능만 할 수 
                       # 있는 저장소를 만드는 옵션 
                       # remote directory가 생성됨
~~~
- bare 명령어를 사용하여 directory를 생성하면 .git 디렉토리에  
있던 파일들이 전부 들어가 있는 것을 확인 가능
- 내가 직접 원격 저장소를 만들 때는 반드시 bare 명령어를 붙여야 함
- 어떠한 작업도 하지 못하게 하기 위함
- 원격 저장소를 만들때는 bare를 넣는다! 라고 생각하자
- local 에서 remote라는 원격 저장소에 local 저장소의 내용을 저장해보자
~~~
cd local
git remote add origin "원격 저장소 경로" # origin은 항상 경로를 치기 귀찮기  
                                         # 때문에 alias 같은 개념
git remote -v # origin 이라고 하는 별명은 해당 저장소 이다! 라는 의미
git push  
~~~
- git push 명령어를 수행하면, matching 방식과 simple 방식에 대한 message가 나옴
  - matching : git이 암시적으로 알아서 해줌 
  - simple : 사용자가 지정해서 어디서 어디로 push 하겠다는 option
- 새버전부터는 matching 방식에서 simple 방식으로 변경됨
- 우리는 쉽게 simple 방식으로 한다고 생각하면 됨!
~~~
git config --global push.default simple
git push 
~~~
- git push --set -upstream origin master 라는 메세지가 뜨는데,  
  origin 이라는 directory에 master branch로 upload 했다는 의미!
- --set upstream 은 앞으로 git push를 할 경우 자동으로 origin master로 push 하겠다는 의미

## chapter34 - GitHub 소개
- 원격저장소를 제공해주는 여러가지 서비스가 있음  
가장 유명한 www.github.com 이 있음
- 이미 존재하는 project를 끌고와서 사용하는 방법을 알아보자
- github.com/git/git 의 메인화면 분석

- contributor : 이 소스코드에 접근 가능한 인원을 말함
- Fork : 해당 버튼을 누르면 해당 project가 나의 것이 됨  
  내가 마음대로 수정 가능하게 됨(단 복제된 소스코드를 말함)
  license에 따라 수정 가능할 수도 아닐 수도 있음!
  fork 옆에 있는 숫자는 복제해 간 project의 수
  자신에 대한 평판을 의미하기도 함
- 개발자들의 open source의 문화의 한 측면이라고 볼 수 있음
- git의 원격 저장소에서 local 저장소로 source 복사하기
~~~
git clone "원격 저장소 URL" "복사하고자 하는 directory 경로"
~~~
- 로그인이 필요없이 clone이 가능

## chapter35 - 원격 저장소 만들기(Github)
- 내가 로컬에서 작성한 소스를 a라는 원격 저장소, b라는 원격 저장소에  
  각각 전송할 수 있음
- 예시
~~~
git remote add origin https://github.com/koni114/git
git remote add friend https://github.com/koni114/git2
~~~
- 일반적으로 기본 원격저장소 명은 'origin'으로 사용
- 다시 friend 삭제
~~~
git remote remove friend
~~~

- 로컬 저장소 입장에서 원격 저장소로 보낼때, push 사용
- -u는 한번만 쓰면 됨


## chapter36 - 동기화 방법(Github)
- 하나의 원격 저장소를 중심으로 두 개의 지역 저장소를 동기화 하는 방법
  - 여러 대의 컴퓨터를 쓰는 경우
  - 협업을 하는 경우
- 원격 저장소 자원을 두 개의 로컬 저장소로 만들어 보자
~~~
git clone https://github.com/koni114/git git_home
git clone https://github.com/koni114/git git_office
~~~

- commit message 를 변경하고 싶은 경우,
~~~
git commit --amend
~~~

- 지역 저장소 입장에서 원격 저장소를 가져오고 싶으면,
~~~
git pull
~~~

## chapter37 - ssh를 이용해서 로그인없이 원격 저장소 사용하기 (Github)
- ssh : Secure Shell
- github은 HTTPS 와 Use SSH 두 개의 option을 제공하고 있음
- HTTPS는 복잡한 개념이나 뭘 입력하지 않아도 push할 수 있음  
  push할 때마다 id와 password를 입력해야 함
- ssh라는 다른 통신방법을 이용해서  
  할 때마다 로그인하지 않고 전송하는 방법을 알아보자
- 실제로 ssh는 자동으로 로그인을 해주는 것이지 ssh와 https는 동일한 level의 통신 방법이라는 것을 잊지 말자

####  ssh 적용 예제

- (1). 내 컴퓨터에 ssh key 생성
~~~
ssh-keygen # 입력 후 경로를 잘 기억
           # 계속 엔터를 치면 ssh를 통해서 다른 컴퓨터로 접속할 수 있는 비밀번호가 생김  
           # 기계적으로 굉장히 복잡한 비밀번호가 생김
# 해당 명령어를 입력하면, /c/Users/koni1/.ssh/ 라는 diretory가 생성됨
~~~
          
- /c/Users/koni1/.ssh/ 디렉토리로 이동하면 두 개의 파일이 있는 것을 확인
  - id_rsa : private key. 비공개된 정보가 들어있다
  - id_rsa.pub : public key. 공개된 정보가 들어있다
- <b/>ssh 통신을 할 때는 private key는 내 컴퓨터에 저장되고, public key는  
  내가 접속하고자 하는 컴퓨터에 일정한 디렉토리에 넣어주면 됨</b>
- 이렇게 되면 id_rsa 파일이 들어있는 컴퓨터에서 id_rsa.pub 라는 파일이 설치된  
컴퓨터로 접속할 때, 아이디 비밀번호를 치지 않아도 접속이 가능
- private key는 절대로 노출되면 안됨
- 서버 컴퓨터에 id_rsa.pub file을 어떠한 규칙에 따라서 저장만 해주면 됨  
우리가 사용하고 하는 원격 저장소는 github를 사용하고 있기 때문에  
ssh public key를 저장하면 됨

- (2). github 계정에 ssh 등록  
  - github.com site에서 settings -> SSH and GPG keys 클릭
  - 여기서 public key를 등록할 수 있음
  - title에는 지역 저장소 이름 작성
  - copy한 값을 Key에 넣어줌
  - 등록 완료
- 이 행위는 Web을 통해서 github에 public key를 저장해 둔 것임

- (3) github에 remote repository 생성
  - 평소 만들던대로 repository를 생성함

- (4) 내 컴퓨터에 clone하여 repository 땡겨오기
  - 이 때 우리는 평소에 HTTPS라는 통신방식으로 했지만, 이제는 SSH로 적용 가능
~~~
# git_fth_ssh directory에 생성
git clone git@github.com:koni114/git-from-the-hell.git git_fth_ssh 
~~~


## chapter38 - 자기 서버에 원격 저장소 만들기(My server)
- 지역 저장소에서 원격 저장소를 생성한 후,   
  인터넷을 통하여 업로드 하는 방법, 내가 직접 구축한 서버, ssh로 통신하는 방법에 대해서 알아보자.
- 내 컴퓨터 vs 원격 저장소가 생성될 컴퓨터에서 실행 한다고 가정해보자


1. 지역 저장소 생성
~~~
git init local
vim f1.txt
git add f1.txt
git commit -m "1"
~~~
 
2. 원격 저장소 생성  
~~~
git init --bare remote # remote 라는 원격 저장소가 생성됨
~~~

3. 같은 컴퓨터가 아니라, 다른 컴퓨터에 있는 원격 저장소에 ssh 방법을 이용하여 접근
~~~
git remote add origin ssh://git@13.124.42.13/home/git/git/remote/
# ssh 라는 통신 방식으로, git 이라는 이름의 13.124.42.13 주소로 접속하겠다! 라는 의미
# 저장소의 이름은 origin
# 경로는 /home/git/git/remote/ (끝에다가 /를 붙이면 directory 안에 있는 내용이라는 의미)

git push
git push --set-upstream origin master 
~~~

## chapter39 - pull & push(my server)
- 두 대의 컴퓨터가 원격 저장소를 중심으로 주고 받는 방법을 알아보자
~~~
git pull 
~~~
- 원격 저장소의 내용을 지역 저장소로 땡겨올 때 사용하는 명령어
- push를 하기 전에 반드시 pull을 해야함
  집에서 작업을 하고 push 를 하고, 회사에서 pull을 안하고  
  수정한 후 push를 하면 rejected 되었다고 확인 가능
- git pull을 하는게 어떻겠냐고 hint를 주고 있음
- 이 때 pull을 하면 작업한 내용과 merge가 됨
- 병합 작업이 끝나면 다시 push 하면 됨
- 분산 버전 관리 시스템 : 지역 저장소에서 버전을 가지고 있고, 원격 저장소로 동기화 시키는 시스템
- 충돌이 났을 때 책임을 다른사람에게 넘기는 방법이, push를 자주 하는 것

## chapter40 - 자동 로그인(My server)
- 자동으로 로그인이 이루어지도록 하는 방법

~~~
cd ~ # .ssh 라는 directory가 보임
mv .ssh .ssh_backup # 혹시 모르니까 백업 해둠
ssh-keygen -t rsa   
# t는 type을 의미하고, 이때 사용할 암호화 방식인 rsa 를 사용하겠다는 의미
~~~
- .ssh 라는 숨김 디렉토리가 보이는데,  
  ssh 라는 방식을 통해 서버 컴퓨터를 원격 제어하는 필요한 정보들이 저장되어 있음
- id_rsa, id_rsa_pub는 일종의 비밀번호  
  우리가 다루는 서버는 보안이 굉장히 중요하고, server를 통해서 수많은 사람들이 영향을 받을 수 있으므로
  보안이 굉장히 중요  
  즉, keygen을 통해서 비밀번호가 들어있고 굉장히 복잡한 비밀번호가 들어있다고 생각하면 됨
- id_rsa : 열쇠, id_rsa.pub : 자물쇠

~~~
# 원격 저장소에서 다음과 같은 명령어 수행
mk .ssh
~/.ssh vim authorized_keys # 해당 file에 rsa.pub 의 내용을 정확하게 저장
                           # authorized_keys 라는 명칭은 약속된 이름

# 더 쉽게 ssh.pub 등록하는 방법
ssh-copy-id git@13.124.42.13
~~~
- id_rsa.pub은 전부 read권한이 있는데, id_rsa는 소유자에 대해서만 읽기와 쓰기가 있어야 함  
  이것보다 더 많은 권한이 부여되어 있으면 읽히지 않을 것임.
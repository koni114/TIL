## chapter08_지옥에서 온 Git : 버전 만들기(commit)
- 모든 변화를 version이라고 하지 않음.
- version은 의미있는 변화를 지칭함.
  - 내가 의미있는 변화라고 지정해 주어야함.(add.)
- 앞으로 버전을 갱신 할 때, 버전을 갱신한 사람이 나라는 것을 알려주기 위해 이름을 setting 해야함
  (한 번만 해주면 됨)
~~~
git config --global user.name jaebig
git config --global user.email koni114@gmail.com
~~~

- 이상태에서 git commit을 하게 되면 commit 됨
~~~
git commit
~~~
- 커밋 후에 vim이 실행됨
- 이 때 commit에 대한 메세지를 작성(commit 내용에 대한 메세지 입력)
- 수정 방법(순서)
  - i 를 눌러서 insert 
  - 글자 입력
  - esc를 누르면 insert 종료
  - :wq 를 입력(write, quit)

- 버전 확인 방법
~~~
git log
~~~
- 새로운 파일이 생성되었을 때 git에게 버전 관리 명령을
  수행 할 때 add 명령어 사용

## chapter09_git stage area
- 왜 git은 add 라는 과정을 포함하고 있는가?
  - 보통 commit은 하나의 작업 과정이 추가될때 마다
    수행하는 것이 보통인데,
    거의 대부분 그 타이밍을 놓침.
    그러면 보통 10~20개 작업이 수행된 후에야 commit을 해야하는데,
   이 때 add는 내가 원하는 파일만 commit  시킬 수 있음!

- add를 한 file만이 commit 이 됨
- 선택적으로 commit이 가능.

- stage 상태
  - git commit 대기 상태를 말함
  - git add 하면 stage 상태로 올라감

- repository
  - commit된 결과가 저장되는 곳.


## chapter10_ 변경 사항 확인하기(log & diff)
- 차이점 확인하기.
~~~
git log
git log -p # -p를 붙이면 각각의 commit 과 commit 사이의 소스의 차이점 확인
~~~
- 마이너스(-)는 이전버전의 소스 내용, 플러스(+)가 붙은 것들은 최신(이후)버전의 소스 내용
~~~
git diff id1..id2 # git commit id 간의 차이를 보여줌.
~~~
- git diff 명령어
  - 소스의 차이를 통해서 어떤 작업을 했는지 알 수 있음.
  - commit을 하기 전에 작업 내용의 마지막 리뷰를 제공해줌.
  - commit을 해주면 비교안됨.

## chapter11_과거로 돌아기기(reset)
- commit을 취소하는 명령, 주의해서 해야함.
- 사고를 방지하기 위해서는 cp 명령어를 통해 다른 디렉토리에 저장해두고,  
  잘못 reset시 백업해둔 폴더를 다시 복원하면 크게 문제될 일 없음!

- reset vs revert
  - reset
    - 일반적으로 특정 commit 위치로 돌아가고 싶을 때 reset 사용
    - commit의 경계를 잘 생각해야함.
    - ex) version 3의 상태로 돌아가고 싶을때 ,
      --> git reset (version3의 commit Id 입력) -- hard
    - 일반적으로 git은 어떠한 정보도 삭제를 안함.
    - reset 명령어를 통해 지운것처럼 보이지만, 실제로는 남아있음.
    - 필요하면 복구 가능. --> git의 원리를 이해해야함.
    - 자원을 원격저장소에 공유하고 있는 경우에는 절대로! reset을 하면 안됨
  - revert

- 중요한 것은 version을 되돌릴 수 있다!

## chapter12_스스로 공부하는 법
- git에서 어떤 명령어가 많이 사용되는지? 통계는 없음..
- 명령어가 얼마나 많은 검색 결과가 있는가?
  - commit > push > pull > clone > checkout > add > branch...

- 메세지에 대한 도움말 확인 방법
  - --help 입력!
  - 화살표키를 위아래로 누르면 scroll이 됨
~~~
git commit -a 
~~~
- 삭제하거나 추가된 파일을 자동으로 stage에 올려줌. -> add 명령어 생략 가능

## chapter13_git의 원리 소개
- git의 원리를 알아야 하는 이유.
  - 영감을 얻을 수 있음.
  - 명령어들의 수행을 훨씬 더 오래 기억할 수 있음.
  

## chapter14_분석도구 gistory 소개.
- 원리를 파악하는 방법?
  - 리눅스 토발츠가 처음으로 git을 세상에 내놓은 첫 버전을 분석하는 방법
  - 어떠한 명령을 내렸을 때, .git에서 어떠한 일이 일어나는가?   
   --> 이번 강의를 통해 알아보는 것.  

- 이고잉 아저씨가 .git 폴더의 변경사항을 좀 더 쉽게 알기 위하여,  
  gistory라는 프로그램을 만들었다고 함.

## chapter15_GIT : 원리 - git add.
- 파일을 추가한 것에 대해서 .git은 변화가 없음(add가 아님)

- git add f1.txt 명령어 수행시, 2가지가 바뀜
  - index file 수정
    - 변화된 파일의 파일명이 저장되어 있음
  - objects/78/9819~~ file이 추가
    - 들어가서 확인해보면, 내가 add 한 file의 내용이 추가되어 있음

- git은 파일을 저장할 때, 파일의 이름이 달라도,
  파일 안의 내용이 같으면, 같은 object를 가리킨다!  
  -> 아무리 많은 파일이 있다고 하더라도, 그 내용이 같으면 disk를 잡아먹지 않음.

## chapter16_GIT 원리: objects 파일명의 원리
- 내용이 같으면, 파일의 이름이 같다!   
  --> 내용을 기반으로 해서 파일의 이름이 결정되는 매커니즘이 존재

- sha1 online site를 접속해보자.
- 결과적으로 git은 내용을 sha1 이라고 하는 hash algorithm을 통과시켜서 file의 object name명을 만들어냄.
 - 이때 만들어진 hash code의 앞의 두글자 명의 directory를 만들어내고,  
 세번째글자 ~ 마지막글자 명으로 파일명으로 생성함.
 - git은 순수하게 파일 내용을 sha1 알고리즘을 통과시키는 것이 아니라,   
 부가적으로 뒤에 뭔가를 추가시켜 sha1 알고리즘을 통과시킴.  

## chapter17_GIT 원리 - commit의 원리
- commit 수행시
  - 기본적으로 commit은 tree 형태의 구조를 가짐
  - objects 디렉토리 안에 commit message가 저장되어 있음
  - terminal node가 최신 commit 정보
    - commit message 내용
      - 누가 커밋 했는지,
      - tree + object 가 적혀있음. -> f1, f2, f3.txt의 파일의 내용이 적혀있음.
      - commit을 한번 더 하면, 해당 디렉토리에 parent가 생김
        -> 이는 이전 commit의 내용임을 알 수 있음.  
        -> 중요한 것은 해당 커밋 객체들의 tree object가 다르다는 것임.  
        당연하다! 내용 자체가 달라졌기 때문.
    - 각각의 버전은 그 시점의 snapshot을 찍어내는데, 이는 tree라는 구조로 표현.

- object file에는 크게 3가지가 존재  
  - blob : file의 내용이 담겨있는 디렉토리  
  - tree : 디렉토리의 파일명과 파일명에 해당되는 내용(blob)을 담고 있는 것  
  - commit : commit 정보의 object id  

## chapter18_GIT 원리 - status의 원리
- index라는 파일이 무엇인가?   
- git status 명령어를 사용했을 때, 어떻게 git은 status를 알 수 있을까?
  - index file과 commit 시 생성되는 object file을 비교하면, commit할 것이 있는지 없는지 알 수 있음.
  - 즉 file을 수정했을 때, hash name의 차이를 보고 status를 출력해줌.
 - index 과 최신 commit의 tree가 가리키고 있는 값이 다르다면, add는 되었고, commit 대기 상태라는 것을 알 수 있음

- 이미지 참고  
 ![img](https://github.com/koni114/TIL/blob/master/git/lecture/git-from-the-hell/img/workspace_repository.png)
- workspace (add) index (commit) local repository (push) remote repositoy
- working directory - index, staging area, cache - repository


## chapter19_GIT 원리 - branch 소개.
- branch : 나무의 가지에 의미를 가지고 있음.
  - branch를 만든다 --> 분기되는 과정을 가진다.(client용과 update용을 따로 만든다 ! 등 ..)
  - branch 작업을 하였던, 하지 않았던 하나의 branch를 쭉 가지고 있었다고 생각할 수 있음
- branch라는 기능은 이전까지 있어 왔는데,  
  예전까지는 쓸만하지 않았다라고 생각하기 쉬움!  
  git 가지고 온 혁신 중에 하나는 branch 기능을 쓸만한 수준까지 끌고 왔다! 라고 판단할 수 있음
- git은 모든 것이 내부적으로 branch의 개념을 가지고 있기 때문에
  꼭 알고 있어야 함

## chapter20 - branch 만들기
~~~
git commit -am
~~~
- 한번도 add가 되지 않은 파일은 자동으로 add 안됨
- branch를 사용하는 경우
  - 고객사용 source를 따로 준비하는 경우
  - 기능을 만들텐데, 쓸모없어질 것 같은 경우
  - 기능을 server에 올려 test 하는 경우

~~~
git branch
~~~ 
  - master라는 branch를 사용하고 있다는 의미.
  - git을 사용하는 순간부터 기본 branch를 사용하는데, master라는 branch를 사용.
  - 일반적인 branch 명칭
    - exp : test용, 실험용
    - feature : 특정 기능 추가시 
  - '*' 가 표시되어 있는 branch는 해당 branch에 들어가 있다는 의미
~~~
git branch exp
~~~
- exp 라는 branch 생성 
~~~
git checkout exp
~~~
- exp branch로 들어감
 


## chapter41 - Git - 원격 저장소의 원리
- git은 사용자가 내부 매커니즘이 어떻게 돌아가는지 안다는 전제하에 설계된 프로그램이기 때문에  
  원리를 잘 이해하면 좀 더 쉽게 이해가 됨
- (1) 지역 저장소를 만들고, (2) github에 원격 저장소를 만들고, (3) 두 개를 연결하고 내부에서 어떤 일이  일어나는가 하나하나 짚어가보자

### (1) 지역 저장소 생성
~~~
git init repo
cd repo
vim f1.txt # source 생성
git add f1.txt
git commit -m "2"
~~~

### (2) 원격 저장소(github) 생성
* homepage에서 repository 생성
~~~
git remote add origin git@github.com:egoing2/repo.git
~~~
* 변경 사항
  * config라는 파일 하나만 수정됨
  * origin이라고 하는 remote 정보가 기록이 되어 있음
    * url과 fetch 정보가 저장되어 있음

### (3) 원격 저장소에 push 하기
~~~
git push
~~~
* 해당 명령어 수행시, 다음과 같은 fatal message를 불 수있음  
  fatal : The current branch master has no upstream branch  
  --> 로컬 저장소의 branch에 연결된 원격 저장소 branch가 존재하지 않는다는 의미
* 이후, 다음과 같은 명령어를 사용하라고 guide해줌

~~~
git push --set-upstream origin master
~~~
* 해당 명령어 수행시, 원격 저장소와 연결하는 작업이 첫번째, source를 업로드 하는 것이 두번째 작업  

* 변경 사항
  * config 파일 수정됨
    * branch "master"가 새로 생성됨
    * 즉, 원격 저장소의 master branch와 로컬 저장소의 master branch가 서로 연결됐다는 것을 의미함
  * refs/remotes/origin/master file 생성
    * push 한 내용의 commit object 정보들이 저장되어 있음
    * refs/heads/master 는 지역저장소의 commit 내용. 위와는 다름!

~~~
git log --decorate --graph
~~~
* 해당 명령어를 수행하면, master와 origin/master가 동일한 commit 내용을 가지고 있음을 확인 가능

~~~
vim f1.txt # f1.txt 수정
git commit -am "2"
vim f1.txt # f1.txt 한번 더 수정
git commit -am "3"
git log --decorate --graph 
~~~
* HEAD 는 version 3의 master를 바라보고 있고, origin/master는 1에 그대로 머물러 있음을 확인
* 이 정보를 알 수 있는 이유는,   
  아래 두 개의 commit 내용이 다름에서 오는 차이를 확인하고 있기 때문 
  - refs/heads/master  
  - refs/remotes/origin/master  


## chapter42 - Git - pull vs fetch의 원리
* git에서 원격 저장소의 내용을 지역 저장소로 가져올 때 두 가지 방식이 있음
  * pull
  * fetch
* git의 원리를 알면 두 가지 차이를 쉽게 알 수 있음
* 예시를 통해서 알아보자

### 예시
* home, office라는 지역저장소가 있고, 같은 원격저장소를 바라보는 예시
* 둘 저장소에서 pull fetch를 해보면서 차이점을 알아보자
* 일반적으로는 pull을 쓰면 됨
~~~
git pull
git log --decorate --all --oneline # 모든 branch에 대한 decorate를 보여줌
~~~
* master branch와 origin/master branch가 동일한 버전을 가리키고 있음
* pull 할 때 변경된 사항
  * refs/heads/master          : local 저장소의 master branch 의 commit 내용이 바뀜
  * refs/remotes/origin/master : remote 저장소의 master branch도 변경. 위의 내용과 동일한 commit을 바라봄  
  * ORIG_HEAD : 과거 버전을 가리키고 있음. 즉 과거로 되돌릴 수 있다는 의미

* f1.txt file을 수정하고 fetch를 했을 때는? 
~~~
vim f1.txt 
git commit -am "7"
git fetch
git log --decorate --all -oneline
~~~
* 변경 사항
  * origin/master만 7로 변경됨  
    --> 원격 저장소의 master가 로컬 저장소의 master를 앞서고 있는 상황
  * refs/remotes/origin/master : 최신 커밋 7번을 가리키고 있음
  * refs/heads/master : 6번을 가리키고 있음
* <b/>즉 fetch 명령어는 지역 저장소에 다운로드는 받았지만, 아직 commit 등에 영향을 미치지 않은 상태라는 의미.</b>
* 원격 저장소의 내용이 지역 저장소의 내용에 아직 commit되지 않은 상태이므로,  
  다음과 같이 비교가 가능
~~~
git log --decorate --all --oneline
git diff ~~
~~~ 
* git diff 를 통해 확인 가능
* 확인하고 난 다음은 merge를 통해서 병합 해야함
~~~
git merge origin/master
~~~
* pull을 사용하면 자동으로 병합을 해주기 때문에 일반적으로 pull 을 사용!

## chapter43 - Git - 2 tag 1(기본 사용법)
- tag라는 주제에 대해서 알아보자. branch라는 것과 비슷한듯 다름!
- github 홈페이지에서 git project를 살펴보자

### github 에서 git project 살펴보기
- release : 사용자들에게 각각 의미있는 version별 프로그램 제공  
  버전별로 git을 다운로드 할 수 있음  
 ![img](https://github.com/koni114/TIL/blob/master/git/lecture/git-from-the-hell/img/release.JPG)
- release를 들어가보면, 버전 별로 commit id가 있는 것을 확인 가능
- 즉, 해당 버전의 commit id는 변경되면 안된다는 의미

- branch : commit id가 항상 바뀐다.   
- tag : commit id가 바뀌지 않는다.

### 예제를 통해 tag 살펴보기
~~~
git init
vim f1.txt 
git commit -am "2"
git log --decorate # commit이 2개임을 확인 가능 
~~~
- 해당 commit 버전을 사용자들에게 다운로드 받게 하고 싶으면?  
  version 1을 release 했다라고 하면, 해당 버전이 어떤 commit에 해당되는지를 알고싶을 것임  
  --> 이때 tag를 씀  

~~~
git tag 1.0.0 
~~~
- HEAD가 가리키고 있는 commit id가 1.0.0이라는 tag를 갖게 됨
- log를 확인해보면 tag가 옆에 붙음!

~~~
vim f1.txt 
git commit -am "3"
git log --decorate
~~~
- 우리가 만들었던 tag는 여전히 해당 commit을 가리키고 있음
~~~
git checkout 1.0.0 
~~~
- tag의 이름을 checkout 함으로써 해당 commit으로 돌아갈 수 있음
- tag 에 대한 설명을 자세한 설명을 붙이고 싶다면?  
  다른 형태의 tag를 사용해야함

#### anotated tag 예시
~~~
annotated tag 
~~~
- annotated : 주석을 단다 라는 의미. 가볍지 않은 주석임
- version 1.1.0의 anotated tag를 달아보자

#### light weighted tag 예시 
~~~
git tag -a 1.1.0 -m "bug fix" # 이 태그에 대한 설명을 적을 수 있음
git tag -v 1.1.0  # tag에 대한 자세한 내용이 보임.
                  # 누가 만들었는가?
                  # tag에 대한 설명들이 추가되어 있음
~~~

### 만들어진 tag를 원격저장소로 보내기
(1) 새로운 원격 저장소 생성
~~~
git remote add origin git@github.com:egoing2/tag.git
git push -u origin master
git push --tags # --tags option을 추가해야만 원격 저장소로 추가됨
~~~
* 2개의 release 가 생성된 것을 알 수 있음
* tag의 이름은 이무렇게나 상관 없음
* 만약 사용자들에게 release version의 자세한 내용을 주고 싶다면,  
  github에서 -> edit tag -> 내용 추가 하면 됨
* github에서 Semantic versioning 2.0.0 이라는 것이 있음
  * version을 작성할 때 어떠한 기준으로 version을 작성할 것인가에 대한 내용이 적혀 있음

### tag 삭제 방법
~~~
git tag -d 1.1.1
~~~

## chapter44 - Git - tag 원리
- tag 명령어를 통해서 tag를 주었을 때 어떤 변화가 있는지 확인해보자

### light weighted tag
- 하나의 파일만 바뀜
  - refs/tags/1.1.2 : object id를 가지고 있음. -> commit message
- 즉 tag를 준다는 것은 단순히 refs/tags 디렉토리 밑에 파일이 생성될 뿐이라는 것
- 직접 tag를 만들 수도 있음
~~~
cd ./.git/refs/tags 
vim 1.1.3.txt # 안에 commit id를 적으면 됨
git tag       # 1.1.3 tag가 생성됨을 확인
~~~

### annotated tag
~~~
git tag -a 1.1.3 -m "bug fix"
~~~ 
* 2개의 파일이 생성
  * object file : 특정한 object를 가리키고 있고, commit에 대한 object, tag설명 등..
  * refs/tags/1.1.4 : annotated tag의 object file을 가리키고 있음

* tag와 branch의 원리는 거의 동일하다는 것을 알 수 있음

## chapter45 - Git - Rebase 1/3
- rebase는 merge와 비슷하나 좀 더 어렵다  
  초심자라면 merge를 쓰는 것을 추천!  
![img](https://github.com/koni114/TIL/blob/master/git/lecture/git-from-the-hell/img/rebase.JPG)  
- master branch에서 feature라는 branch를 생성    
  그 후에 각각 commit을 한 상태   
- rebase vs merge 공통점  
  - feature와 master가 합쳤다는 것  
- rebase vs merge 차이점  
  - merge : 병렬로 존재. history를 알기가 어렵  
  - rebase : 직렬로 존재. history가 알 수 있음  
~~~
git checkout feature
git rebase master
~~~
- git rebase master 명령어를 수행하는 순간, master의 최신 commit이 base로 변환
- feature branch의 commit history는 temp에 잠시 저장되고,  
  base 뒤에 feature commit history가 붙는 개념
- rebase는 비교적 어렵고, 복구가 어렵다

## chapter46 - Git - Rebase 2/3
- rebase 실습
- 화면을 3개로 나눔
~~~
# 화면1

git init .
vim f1.txt
git commit -am "1"
git checkout -b rb

vim re.txt
git add re.txt
git commit -am "R1"

vim re.txt
git commit -am "R2"

git checkout master
vim master.txt
git add master.txt
git commit -m "M1"

vim master.txt # 수정
git commit -am "M2"

# rebase
git checkout rb 
git rebase master 
git log --decorate --all --oneline --graph 
# 조상이 달라짐을 확인!

git checkout master
git merge rb # fast-forward로 commit branch(HEAD)가 변경됨
~~~

## chapter47 - Git - Rebase 3/3
- rebase는 다른 사람들과 commit 하지 않은 상태에서 rebase 해야 함
- 각각 같은 부분을 수정한 branch(master, rb)가 있다고 해보자  
  merge를 하면 충돌이 날 것임  
~~~
git rebase master
~~~
- rebase를 하는 순간 임시저장소에 base source와 R1 source의 차이만을 저장한 fetch 내용을 저장
- R1-R2, R2-R3의 fetch도 각각 저장
- rebase 하는 순간, confilct가 났다는 메세지를 주면서 수정하라고 얘기함
~~~
git status # conflict 확인
vim f1.txt # 충돌 난 부분을 수정
git add .
git status # 충돌 부분을 수정했으므로, git rebase --continue를 하라고 되어 있음
git rebase --continue # R2와 충돌남

vim f1.txt
git add . 
git rebase # R3와 충돌남

vim f1.txt # 충돌 수정
git add .
git rebase --continue # rebase success

git log --decorate --all --graph --oneline # 가지치기 없이 깔끔하게 보여준다는 것!
~~~
- 프로젝트의 복잡도에 따라서 적절한 도구를 사용하는 것이 중요함

## chapter48 - Git을 이용한 프로젝트의 흐름(Git Flow) 1
- git을 '잘' 사용하는 방법에 대한 가이드를 알아보자
- 이것은 주관적이기 때문에 스스로 맥락적으로 채택할지, 하지 않을지 판단해라
- 여러가지 모델중 git flow라는 모델을 소개  
![img](https://github.com/koni114/TIL/blob/master/git/lecture/git-from-the-hell/img/git_flow.png)  

- 가장 중요한 branch가 master와 develop branch
- 두 개의 역할 분담을 하고 있는 것이 가장 중요한 포인트
- master에서 파생된 develop이라는 branch에서 실질적으로 개발이 이루어짐
- 특정한 기능을 개발해야 하는 경우가 생겼을 때, feature 라고 하는 branch 생성 후 개발
- 만약 두 개의 기능을 만들어야 한다면, 2개의 feature로 시작하는 branch를 각각 만듬
- feature 작업 한 내용을 다시 develop으로 병합
- 어떤 특정한 속하지 않은 애매한 변경 사항들은(ex) bug) develop을 통해서 해나감
- 사용자들에게 결과를 배포하는 것은 새로운 branch를 따는데 release 라는 branch로 만듬
- release 이후에 발생하는 문서 업데이트, 버그 수정은 release branch 안에서 해나감
- develop branch에 틈틈히 merge를 해서 적용
- master branch에 병합하면서, tag라는 형식(기능)으로 기록함  
  server다가 upload, 사용자가 download 한다거나..  
- 결과적으로 master branch는 사용자에게 제공되는 프로그램, 또는 시스템 버전이 되는 것  
- release branch는 master branch로도 병합되지만, 계속 개발을 해야하므로 develop branch로도 병합 됨  
- hotfix는 긴급하게 버그가 생길 가능성을 염두한 branch  
  문제 해결 후, master branch로 병합을 한 다음에 master branch에 버전을 기록하고 사용자들에게 제공  








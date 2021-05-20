## chapter10 - 협업
- 파이썬은 API를 잘 정의하고 인터페이스 경계를 명확히 하고 싶을 때 도움이 되는 언어 기능을 제공함
- 파이선 프로그래머들과 쉽게 협업할 수 있는 매커니즘을 이해해야함

### 82-커뮤니티에서 만든 모듈을 어디서 찾을 수 있는지 알아두라
- 파이썬에는 프로그램에 설치하고 사용할 수 있는 모듈을 모아둔 중앙 저장소가 있음(http://pypi.org)
- 이런 모듈은 우리와 같은 사람들로 이뤄진 파이썬 커뮤니티에 의해 만들어지고 유지 보수됨
- 어려운 문제에 직면했을 때는 문제를 해결하는데 필요한 코드를 파이썬 패키지 인덱스(PyPI)에서 찾아보면됨
- 패키지 인덱스를 사용하려면 `pip` 라는 명령줄 도구를 사용해야 함
- `python3 -m pip`를 사용해 pip를 호출하면 패키지가 시스템에 설치된 파이썬 버전에 맞게 설치되도록 보장할 수 있음
- pip를 사용하면 새로운 모듈을 쉽게 설치할 수 있음
- 프로젝트에 설치된 패키지들을 지속적으로 추적하도록 pip를 venv라는 내장 모듈과 함께 사용하는 것이 가장 유용함
- 또한 PyPI 패키지를 직접 만들고 파이썬 커뮤니티와 공유하거나 pip에서 사용하기 위해 비공개 패키지 저장소를 만들 수도 있음
- PyPI에 들어 있는 각 모듈은 서로 다른 라이선스로 제공됨. 대부분의 패키지, 특히 유명한 패키지들은 보통 자유로운 오픈 소스 라이선스로 제공됨

#### 기억해야 할 내용
- 파이썬 패키지 인덱스(PyPI)에는 파이썬 커뮤니티가 개발하고 유지하는 풍부한 공통 패키지가 들어 있음
- pip는 PyPI에 있는 패키지를 설치하고 사용할 때 쓸 수 있는 명령줄 도구
- PyPI 모듈의 대다수는 자유 소프트웨어이거나 오픈 소스 소프트웨어임

### 83- 가상 환경을 사용해 의존 관계를 격리하고 반복 생성할 수 있게 해라
- 크고 복잡한 프로그램을 만들다 보면 파이썬 커뮤니티가 제공하는 다양한 패키지에 의존하게 되는 경우가 많음
- `python3 -m pip` 명령줄 도구를 사용해 `pytz, numpy` 등의 다양한 패키지를 자주 설치할 것임
- 문제는 pip가 새로운 패키지를 기본적으로 모든 파이썬 인터프리터가 볼 수 있는 전역 위치에 저장하는데 있음
- 이로 인해 우리 시스템에서 실행되는 모든 파이썬 프로그램이 설치한 모듈의 영향을 받게 됨
- 이론적으로는 이런 일이 문제가 되서는 안됨. 어떤 패키지를 설치했다 해도 import 하지 않는다면, 이 패키지는 우리 프로그램에 영향을 미칠 수 없음
- 또한 추이적(transive) 의존 관계에 문제가 생길 수 있음. 추이적 의존 관계는 설치한 패키지가 다른 패키지에 의존하는 경우를 말함
- 예를 들어 Sphinx를 설치한 후 pip를 통해 이 패키지가 의존하는 다른 패키지 목록을 볼 수 있음
~~~python
$ python3 -m pip show Sphinx
Name: Sphinx
Version: 4.0.1
Summary: Python documentation generator
Home-page: http://sphinx-doc.org/
Author: Georg Brandl
Author-email: georg@python.org
License: BSD
Location: /Users/heojaehun/gitRepo/TIL/effectivePython/venv/lib/python3.7/site-packages
Requires: sphinxcontrib-serializinghtml, alabaster, setuptools, Jinja2, sphinxcontrib-devhelp, packaging, sphinxcontrib-jsmath, snowballstemmer, docutils, requests, sphinxcontrib-applehelp, MarkupSafe, sphinxcontrib-htmlhelp, imagesize, Pygments, babel, sphinxcontrib-qthelp
~~~
- 이런 패키지들은 시간이 지남에 따라 서로 달라지므로 의존 관계 충돌이 발생할 수 있음. 현재는 두 패키지가 모두 똑같은 jinja2 버전에 의존할 것임. 하지만 6개월이나 1년 후에 jinja2가 기존 버전을 사용하는 코드가 제대로 컴파일되거나 동작하지 못하게 하는 새로운 버전을 릴리스할 수도 있음 
- <b>이런 식으로 프로그램이 깨지는 이유는 파이썬에서 전역적으로는 어떤 모듈을 단 한 버전만 설치할 수 있기 때문</b>
- 설치한 패키지 중 일부는 새로운 버전을 사용해야 하고 다른 일부는 예전 버전을 사용해야 한다면 시스템이 제대로 작동하지 못하게 함
- 이런 상황을 일컬어 의존 관계 지옥(dependency hell)이라고 부름
- 패키지 관리자들이 릴리스 사이의 API 호환성을 최대한 유지하기 위해 노력해도 이런 식의 고장이 생길 수 있음 
- 새로운 버전의 라이브러리가 해당 라이브러리의 API에 의존하는 코드 동작을 크게 바꿀 수 있음
- 시스템 사용자들이 패키지를 새 버전으로 바꿨는데, 다른 패키지는 업그레이드하지 않는다면 의존 관계가 개질 수 있음
- 추가적으로 협업의 경우에도 이런 경우가 발생할 수 있음
- <b>이 문제를 해결하는 방법으로 venv라는 도구를 사용하는 것</b> venv라는 가상 환경을 제공함. 파이썬 3.4부터 파이썬 설치시 pip와 venv 모듈을 디폴트로 제공하기 시작함
- venv를 사용하면 특정 버전의 파이썬 환경을 독립적으로 구성할 수 있고, 한 시스템 안에 같은 패키지의 다양한 버전을 서로 충돌 없이 설치할 수 있음. 한 컴퓨터 안에서 여러 다른 프로젝트 작업을 진행하면서 프로젝트마다 각각 다른 도구를 활용할 수 있다는 의미
- ven는 각 버전의 패키지와 의존 관계를 완전히 별도의 디렉터리 구조로 저장함으로써 이런 기능을 제공
- 이렇게 하면 venv를 사용해 여러분의 코드가 제대로 동작하는 파이썬 환경을 반복해서 생성해낼 수 있음
- venv는 예기치 못한 프로그램 고장을 방지하는 신뢰할 만한 방법

#### command line에서 venv 사용하기
- venv를 효과적으로 사용하는 방법을 소개함
- venv 도구를 사용하기 전에 `python3` 명령어의 의미에 대해서 알고 있어야 하는데, 예를 들어 해당 명령어의 의미는 `/usr/local/bin` 디렉터리에 있고 버전 3.7.7을 수행한다는 의미
~~~shell
$ which python3
$ python3 --version
$ python3 -c 'import ptyz'  #- pytz 패키지 임포트 여부 확인
$ python3 -m venv myproject #- venv를 이용해 myproject라는 가상환경을 만듬
$ cd myproject 
$ ls                        #- venv 디렉토리 밑에 해당 디렉토리 확인 가능
bin             include         lib             pyvenv.cfg
$ source bin/activate       #- 가상환경 사용. activate는 모든 환경 변수를 가상환경에 맞춰줌
                            #- 명령줄 프롬프트를 가상 환경 이름(myproject)를 포함하도록 바꿈

#- 가상 환경을 실행시키면 python3 명령줄 도구가 가상 환경 디렉터리 안의 도구 경로로 바뀜
$ which python3
$ ls -l /tmp/myproject/bin/python3  
~~~
- 이렇게 해서 가상 환경 외부 시스템이 가상 환경으로부터 영향을 받지 않게 됨
- 외부 시스템이 디폴트 파이썬 버전을 3.9로 업그레이드한다고 해도 가상 환경은 여전히 파이썬 3.8을 명시적으로 가리킴
- 여기서 venv로 만든 가상 환경은 pip와 setuptools를 제외한 어떤 패키지도 설치되지 않은 환경
- 가상 환경 밖의 시스템에 전역으로 설치된 pytz 패키지를 사용하려고 시도하면 가상 환경 안에 pytz 패키지가 없으므로 오류가 발생함
- 가상 환경 안에서 pip를 이용해 pytz 모듈을 가상 환경에 설치할 수 있음
~~~shell
$ python -m pip install pytz
$ python -c "import pytz"

#- 가상 환경에서 필요한 작업을 마치고 기본 시스템으로 돌아가고 싶다면 deactivate 명령어 사용
$ deactivate
$ which python3
~~~
- 다시 myproject 환경에서 작업을 해야 한다면 앞에서 했던 것처럼 `source bin/activate`를 실행하면 됨

#### 의존 관계 재생성하기
- 우리의 작업 환경을 다른 곳으로 복사해야함. 예를 들어 내 개발 컴퓨터에서 사용하던 환경을 데이터 센터의 서버에 똑같이 만들고 싶거나, 다른 사람의 디버깅을 도와주기 위해 이 사람의 환경을 내 컴퓨터로 가져오고 싶을 수도 있음
- venv를 사용하면 쉽게 할 수 있음. `python3 -m pip freeze` 명령을 사용해 현재 명시적으로 의존하는 모든 의존 관계를 파일에 저장할 수 있음(이때 파일 이름은 관례적으로 requirement.txt임)
~~~shell
$ python3 -m pip freeze > requirement.txt
$ cat requirement.txt   

>>>
pytz==2021.1
~~~
- 이제 myproject 환경과 똑같은 다른 가상 환경을 만들고 싶다고 하자. 먼저 venv를 사용해 새 가상 환경 디렉터리를 만들고 activate로 활성화해야함 
~~~shell
$ python3 -m venv otherobject
$ cd otherobject
$ source bin/activate
~~~
- 새 환경에는 아무 패키지도 설치돼 있지 않음
~~~shell
$ python3 -m pip list
$ python3 -m pip install -r /tmp/project/requirement.txt
~~~
- 이 명령을 실행하면 첫 번째 환경을 재생성하는데 필요한 모든 패키지를 내려받아 설치해야 하므로 약간 시간이 걸림
- 명령 실행이 끝나면, 두 번째 가상 환경에 설치된 패키지의 목록을 얻어 첫 번째 가상 환경의 의존 관계 목록과 같은지 비교할 수 있음
~~~shell
$ python3 -m pip list
~~~
- requirement.txt는 버전 관리 시스템을 사용해 다른 사람과 협업할 때 이상적임
- 우리가 변경한 코드를 커밋(commit)할 때 우리 패키지 의존 관계 목록도 갱신 할 수 있음
- <b>하지만 우리가 사용하는 구체적인 파이썬 버전은 requirement.txt 파일에 들어가지 않는다는 점에 유의 </b> 따라서 파이썬 버전은 별도 관리해야 함
- 가상 환경을 사용할 때 빠질 수 있는 함정으로, 가상 환경 디렉토리를 통째로 옮기면 모든 요소가 깨져버림
- python3 등의 명령줄 도구 경로가 하드코딩돼 있기 때문
- 하지만 결과적으로 이는 문제가 되진 않음. 가상 환경을 사용하는 목표는 설정된 환경을 쉽게 재생성하는 것
- 따라서 가상 환경 디렉터리를 직접 이동하는 대신, 새로운 디렉터리에 가상 환경을 만든 후 원래 디렉터리에서 `python3 -m pip freeze`를 실행해 얻은 requirement.txt 파일로 모든 모듈을 재설치하면 됨

#### 기억해야 할 내용
- 가상 환경을 사용하면 한 컴퓨터 안에서 pip를 사용해 패키지의 여러 버전을 충돌 없이 설치할 수 있음
- `python -m venv` 명령으로 가상 환경을 만들고 `source bin/activate`로 가상 환경을 활성화하며, deactivate로 비활성화함
- `python -m pip freeze`를 사용해 어떤 환경 안의 모든 의존 관계를 덤프할 수 있음. `python3 -m pip install -r requirements.txt`를 사용해 환경을 다시 만들어낼 수 있음
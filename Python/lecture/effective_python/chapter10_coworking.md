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

### 84- 모든 함수, 클래스, 모듈에 독스트링을 작성해라
- 파이썬은 언어 자체의 동적인 특성으로 인해 문서화가 특히 중요함. 파이썬은 코드 블록에 문서를 첨부하는 기능을 기본으로 제공함
- 다른 여러 언어와 달리 파이썬에서는 프로그램을 실행하는 중에 프로그램 소스 코드의 문서에 직접 접근할 수 있음
- 예를 들어 함수 def문 바로 다음에 독스트링을 사용해 문서를 추가할 수 있음
~~~python
def palindrome(word):
    """주어진 단어가 회문인 경우 True를 반환함"""
    return word == word[::-1]

assert palindrome('tacocat')
assert not palindrome('banana')
~~~
- 파이썬 프로그램에서 독스트링을 가져오려면 __doc__ 특별 애트리뷰트를 사용하면 됨
~~~python
print(repr(palindrome.__doc__))

>>>
'주어진 단어가 회문인 경우 True를 반환함'
~~~
- 또 명령줄에서 내장 pydoc 모듈을 사용해 로컬 웹 서버를 실행할 수 있음. 이 서버는 우리가 작성한 모듈을 비롯해 인터프리터에서 찾을 수 있는 모든 파이썬 문서를 제공함
~~~shell
$ python3 -m pydoc -p 1234
Server ready at http://localhost:1234/
Server commands: [b]rowser, [q]uit
server> b 
~~~
- 독스트링을 함수, 클래스, 모듈에 첨부할 수 있음. 첨부하는 작업은 파이썬 프로그램을 컴파일하고 실행하는 과정의 일부분임
- 파이썬의 독스트링과 __doc__ 애트리뷰트 지원은 다음 세가지 효과를 가져옴
  - 문서에 항상 접근할 수 있으므로, 대화식 개발이 쉬워짐. help 내장 함수를 통해 함수, 클래스, 모듈의 내부 문서를 살펴볼 수 있음. 이로 인해 우리가 알고리즘을 개발하거나 API를 테스트하거나 작은 코드를 작성할 때 파이썬 대화식 인터프리터나 IPython 노트북 같은 도구를 즐겁게 사용 할 수 있음
  - 코드 문서화를 정의하는 표준이 있으므로 문서 본문을 더 보기 좋은 형태(HTML 등)로 바꿔주는 도구를 쉽게 만들 수 있음. 이로 인해 파이썬 커뮤니티 안에서 스핑크스 같은 훌륭한 문서 생성 도구가 여럿 생김(https://www.sphinx-doc.org). 또한 오픈 소스 파이썬 프로젝트들의 보기 좋은 문서들을 무료로 호스팅해주는 리드더독스 같은 사이트도 생김
  - 파이썬이 제공하는 훌륭하고, 접근하기 쉽고, 보기 좋은 문서들로 인해 사람들이 자극받고 더 많은 문서를 작성하게 됨. 파이썬 커뮤니티 구성원들은 문서화가 중요하다고 확신함. 파이썬 커뮤니티에는 '좋은 코드'란 문서화가 잘된 코드라는 가정이 존재함. 대부분의 파이썬 오픈소스 라이브러리들이 좋은 문서를 제공할 것으로 기대해도 좋다는 뜻임
- 이렇게 훌륭한 문서화 문화에 동참하기 위해 독스트링을 작성할 때 따라야 할 몇 가지 지침이 있음 
- 전체 지침은 온라인 PEP 257에서 볼수 있음. 여기서는 몇 가지 모범 사례를 소개함

#### 문서 모듈화하기
- 각 모듈에는 최상위 독스트링이 있어야 함. 이 최상위 문자열은 세 개의 큰따옴표(""")로 시작함
- 이 독스트링의 목적은 모듈과 모듈 내용을 소개하는 것
- 독스트링의 첫 줄은 모듈의 목적을 설명하는 한 문장이어야 함. 다음에 오는 단락에는 모듈 사용자들이 모듈의 동작에 대해 알아둬야 하는 세부 사항을 적어야 함
- 모듈 독스트링은 모듈에서 찾을 수 있는 중요한 클래스와 함수를 강조해 알려주는 모듈 소개이기도 함
- 모듈 독스트링의 예는 다음과 같음
~~~python
# words.py
#!/usr/bin/env python3
"""단어의 언어 패턴을 찾을 떄 쓸 수 있는 라이브러리.

여러 단어가 서로 어떤 연관관계가 있는지 검사하는게 어려울 때가 있다!
이 모듈은 단어가 가지는 특별한 특성을 쉽게 결정할 수 있게 해준다.

사용 가능 함수:
- palindrome: 주어진 단어가 회문(palindrome, 앞으로 읽어도 뒤부터 읽어도 똑같은 경우)인지 결정한다.
- check_anagram: 주어진 단어가 어구전철(anagrams, 똑같은 글자들로 순서만 바뀐 경우)인지 결정한다.
...
"""
~~~
- 모듈이 command line 용도라면, 도구를 실행해 사용하는 방법을 독스트링에 제공하면 좋음

#### 클래스 문서화하기
- 각 클래스는 클래스 수준의 독스트링을 포함해야 함
- 클래스 수준 독스트링은 모듈 수준 독스트링과 거의 비슷한 패턴을 만듬
- 첫 줄은 클래스 목적을 알려주는 한 문장. 뒤에 오는 단락들은 클래스의 동작 세부 사항 중 중요한 부분을 설명함
- 독스트링은 클래스에서 <b>중요한 공개 애트리뷰트와 메서드를 강조해 표시</b>해둬야 함. 그리고 이 클래스를 상위 클래스로 상속하는 하위 클래스가 보호 애트리뷰트나 메서드와 상호 작용하는 방법을 안내 해야함
- 다음은 클래스 독스트링의 예
~~~python
class Player:
 """게임 플레이어를 표현한다
    
    하위클래스는 `tick` 메서드를 오버라이드해서 플레이어의 파워 레벨 등에 맞는
    움직임 애니메이션을 제공할 수 있다
    
    공개 애트리뷰트:
    - power: 사용하지 않은 파워업들(0과 1사이의 float)
    - coins: 현재 레벨에서 발견한 코인 개수(integer)
    """
    ...

~~~

### 함수 문서화하기
- 모든 공개 함수와 메서드에는 독스트링을 포함시켜야 함. 함수나 메서드의 독스트링도 클래스 독스트링과 같은 패턴을 가짐. 첫 줄은 함수가 하는 일을 설명. 다음 단락부터는 함수 인자나 함수의 동작에 대해 구체적으로 설명함
- 반환 값이 있으면 이에 대해서도 설명해야 함. 함수의 인터페이스에 속해 있으며 함수를 호출하는 쪽에서 꼭 처리해야 하는 예외도 설명해야함.
- 다음은 함수 독스트링 예제
~~~python
def find_anagrams(word, dictionary):
    """주어진 단어의 모든 어구전철을 찾는다.
    이 함수는 '딕셔너리' 컨테이너의 원소 검사만큼 빠른 속도로 실행된다.
    
    Args:
        word: 대상 단어. 문자열.
        dictionary: 모든 단어가 들어있는 collections.abc.Container 컬렉션.
    
    Returns:
        찾은 어구전철들로 이뤄진 리스트. 아무것도 찾지 못한 경우 Empty.
    """
    ...
~~~
- 함수 독스트링을 작성할 때 몇 가지 중요한 규칙을 고려해야 하는데, 그중에서 알아둬야 할 내용은 다음과 같음
  - 함수에 인자가 없고 반환 값만 있다면 설멸은 한 줄로도 충분할 것임
  - 함수가 아무 값도 반환하지 않는다면 'returns None'이나 'None을 반환함'을 쓰는 것보다 아예 안쓰는게 나음
  - 함수 인터페이스에 예외 발생이 포함된다면, 발생하는 예외와 예외가 발생하는 상황에 대한 설명을 함수 독스트링에 반드시 포함시켜야 함
  - 일반적인 동작 중에 함수가 예외를 발생시키지 않을 것으로 예상한다면 예외가 발생하지 않는다는 사실을 적지 말라
  - 함수가 가변 인자나 키워드 인자를 받는다면, 문서화한 인자 목록에 *args, **kwargs를 사용하고 각각의 목적을 설명해라
  - 함수에 디폴트 값이 있는 인자가 있다면 디폴트 값을 언급해야 함
  - 함수가 제너레이터라면, 독스트링에는 이 제너레이터를 이터레이션할 때 어떤 값이 발생하는지 기술해야 함
  - 함수가 비동기 코루틴이라면, 독스트링에 언제 이 코루틴의 비동기 실행이 중단되는지 설명해야 함

#### 독스트링과 타입 애너테이션 사용하기
- 여러 가지 이유로 인해 파이썬도 이제 타입 애너테이션을 지원함ㄴ
- 타입 애너테이션이 제공하는 정보는 전형적인 독스트링이 제공하는 정보와 중복될 수 있음
- 예를 들어 다음은 타입 애너테이션을 붙인 `find_anagrams` 함수 시그니처임
~~~python
from typing import Container, List

def find_anagrams(word:str,
                  dictionary: Container[str])  List[str]:
~~~
- 더 이상 독스트링에서 word가 문자열이라고 설명할 필요는 없음
- 타입 애너테이션이 이런 정보를 이미 포함하기 때문. `dictionary` 인자가 `collections.abc.Container`라는 설명도 마찬가지임
- 반환 타입이 리스트라는 사실도 이미 명확하게 적혀 있기 때문에 굳이 독스트링에 이를 명시할 필요가 없음
- 그리고 어구전철(anagram)을 찾지 못해도 반환 값은 여전히 리스트일 것이고, 반환 값이 없을 때 그 리스트에 아무 값도 들어 있지 않을 것이라는 사실을 쉽게 유추할 수 있으므로 독스트링에 이 사실을 설명할 필요도 없음
- 이에 따라 이 함수의 독스트링을 줄여서 다시 쓴 코드는 다음과 같음
~~~python
def find_anagrams(word: str,
                  dictionary: Container[str]) -> List[str]:
    """주어진 단어의 모든 어구전철을 찾는다.
    이 함수는 '딕셔너리' 컨테이너의 원소 검사만큼 빠른 속도로 실행된다.
    Args:
        word: 대상 단어.
        dictionary: 모든 단어가 들어있는 컬렉션.
    Returns:
        찾은 어구전철들.
    """
    ...
~~~
- 인스턴스 필드, 클래스, 애트리뷰트, 메서드 등에서도 마찬가지로 타입 애너테이션과 독스트링의 정보 중복을 피해야 함. 타입 정보는 가능하면 어느 한쪽을 몰아서 유지하는 것이 가장 좋음
- 실제 구현과 문서가 달라질 위험성을 줄일 수 있기 때문

#### 기억해야 할 내용
- 독스트링을 사용해 모든 모듈, 클래스, 메서드, 함수에 대해 문서를 작성해라. 코드를 변경할 때마다 독스트링을 최신 상태로 유지해라
- 모듈의 경우: 모듈의 내용과 사용자가 알아야 하는 중요한 클래스나 함수를 독스트링에 소개해라
- 클래스의 경우: 동작, 중요한 애트리뷰트, 하위 클래스 동작 등을 class 문 뒤에 나오는 독스트링에 문서화해라
- 함수와 메서드의 경우: 모든 인자, 반환 값, 발생하는 예외, 기타 세부적인 동작 등을 def 문 바로 뒤에 오는 독스트링에 설명해라
- 타입 애너테이션을 사용하는 경우: 타입 애너테이션에 들어 있는 정보를 독스트링에 기술하지말라. 불필요한 중복 작업임

### 85-패키지를 사용해 모듈을 체계화하고 안정적인 API를 제공해라
- 프로그램 코드베이스가 늘어나면 자연스럽게 코드 구조를 체계화, 즉 다시 조직하게 됨
- 큰 함수를 여러 작은 함수로 나누고, 데이터 구조를 도우미 클래스로 리펙터링하며, 기능을 나눠서 서로 의존적인 여러 모듈에 분산시킴
- 어느 시점이 되면 모듈이 너무 많아 코드를 이해하기 어려우므로, 다른 계층을 추가로 도입해서 코드를 좀 더 이해하기 쉽도록 바꾸게 됨. 이런 경우에 대비해 파이썬은 패키지를 제공함
- 패키지는 다른 모듈들을 포함하는 모듈
- 대부분의 경우 `__init__.py` 라는 빈 파일을 디렉터리에 추가함으로써 패키지를 정의함. `__init__.py`가 있는 디렉터리가 있다면, 이 디렉터리에 있는 다른 파이썬 파일은 `__init__.py`가 있는 디렉터리를 기준으로 상대적인 경로를 통해 임포트해서 사용할 수 있음
- 예를 들어 프로그램 디렉터리 구조가 다음과 같다고 하자
~~~python
main.py
mypackage/__init__.py
mypackage/models.py
mypackage/utils.py
~~~
- `utils.py` 모듈을 import 하려면 패키지 디렉터리 이름이 포함된 절대적인 모듈 이름을 사용하면 됨
~~~python
# main.py
from mypackage import utils
~~~
- 이 패턴은 다른 패키지 안에 패키지 디렉터리가 있는 경우에도 적용할 수 있음
- 파이썬에서 패키지 기능은 주로 두 가지 역할을 담당함

#### 이름 공간
- 패키지의 첫 번째 역할은 모듈을 별도의 이름 공간(namespace)으로 분리하는 것. 패키지를 사용하면, <b>파일 이름은 같지만 서로 다른 절대 유일한 경로를 통해 접근 할 수 있는 모듈을 여럿 정의할 수 있음</b>
- 예를 들어 다음은 `utils.py` 라는 같은 이름의 모듈로부터 애트리뷰트를 임포트하는 프로그램임
~~~python
# main.py
from analysis.utils import log_base2_bucket
from frontend.utils import stringify

bucket = stringify(log_base2_bucket(33))
~~~
- 패키지 안에 정의된 함수, 클래스, 하위 모듈의 이름이 같으면 이런 접근 방법을 사용할 수 없음
- 예를 들어 `analysis.utils` 와 `frontend.utils`에 있는 inspect 함수를 함께 사용하고 싶다고 하자. 이 애트리뷰트를 직접 임포트하면 두 번째 import 문이 현재 영역의 inspect 값을 덮어 쓰기 때문에 두 함수를 함께 사용할 수 없음
~~~python
# main#2#.py
from analysis.utils import inspect
from frontend.utils import inspect
~~~
- 해결 방법은 import문에 as 절을 사용해 현재 영역에 임포트한 대상의 이름을 변경하는 것
~~~python
# main#3#.py
from analysis.utils import inspect as analysis_inspect
from frontend.utils import inspect as frontend_inspect

value = 33
if analysis_inspect(value) == frontend_inspect(value):
    print("인스펙션 결과가 같음!")
~~~
- as 절을 사용하면 import로 가져온 대상이 무엇이든 관계없이 이름을 마음대로 바꿀 수 있음
- 심지어 임포트한 모듈 이름을 바꿀 수도 있음. 이 기능을 사용하면  이름 공간에 들어 있는 코드에 편하게 접근할 수 있고, 이름 공간에 속한 대상을 사용할 때 어떤 것에 접근하는지 더 쉽게 식별할 수 있음
- 임포트한 이름이 충돌하지 않게 막는 다른 방법은 최상위 모듈 이름을 항상 붙여서 사용하는 것임. 이는 앞 예제에서 import from 대신 기본적인 import를 사용한다는 뜻
~~~python
# main4.py
import analysis.utils
import frontend.utils

value = 33
if (analysis.utils.inspect(value) == frontend.utils.inspect(value)):
    print("인스펙션 결과가 같음!")
~~~
- 이 접근방법을 사용하면 as 절을 사용하지 않아도 됨. 또한, 코드를 처음 읽는 사람도 이름이 비슷한 함수가 어떤 모듈에서 왔는지 아주 명확하게 알 수 있음

#### 안정적인 API
- 파이썬 패키지의 두 번째 역할은 엄격하고 안정적인 API를 외부 사용자에게 제공하는 것임
- 오픈 소스 패키지처럼 널리 사용될 API를 작성할 경우에는 릴리스할 때 변경되지 않는 안정적인 기능을 제공하고 싶을 것임. 이런 안정적인 기능을 제공하려면 외부 사용자로부터 내부 코드 조직을 감춰야 함
- 그렇게 해야 외부 사용자의 코드를 깨지않고 우리 패키지의 내부 모듈을 리펙터링하고 개선할 수 있음
- <b>파이썬에서는 모듈이나 패키지의 `__all__` 특별 에트리뷰트를 통해 API 소비자에게 노출할 표면적을 제한할 수 있음</b>
- __all__의 값은 모듈에서 외부로 공개된 API로 익스포트(export)할 모든 이름이 들어 있는 리스트임
- `from foo import *`를 실행한 소비자 코드는 foo로부터 foo.__all__에 있는 애트리뷰트만 임포트 할 수 있음. foo에 __all__ 정의가 들어있지 않으면 공개 애트리뷰트(이름 앞에 밑줄이 붙어 있지 않은 애트리뷰트)만 임포트됨
- 예를 들어 움직이는 발사체의 충돌을 계산하는 패키지를 제공한다고 하자. 다음 코드는 mypackage의 models 모델에 발사체에 대한 표현을 정의함
~~~python
# models.py
__all__ = ['Projectile']

class Projectile:
    def __init__(self, mass, velocity):
        self.mass = mass
        self.velocity = velocity
~~~
- 그리고 발사체 사이의 충돌 시뮬레이션과 같은 Projectle 인스턴스에 대한 연산을 mypackage 밑의 utils 모듈에 정의함
~~~python
# utils.py
from . models import Projectile

__all__ = ['simulate_collision']

def _dot_product(a, b):
    ...

def simulate_collision(a, b):
    ...
~~~
- 이제 API에서 공개적인 부분을 전부 mypackage 모듈의 애트리뷰트로 제공하고 싶음
- 이렇게 하면 이 API를 사용하는 사용자들이 mypackage.models 나 mypackage.utils를 임포트하지 않고 mypackage에서 직접 필요한 요소를 임포트 할 수 있음
- 그리고 mypackage 내부 구성을 변경해도(예를 들어 models.py를 삭제해도) 외부 사용자의 코드는 전혀 문제없이 작동함
- 파이썬 패키지로 이런 동작을 수행하려면 mypackages 디렉터리에 있는 __init__.py 파일을 변경해야 함
- 이 파일은 mypackage를 임포트할 때 실제 패키지 내용으로 인식되는 파일임. 따라서 이 __init__.py 안에 우리가 외부에 공개할 이름만 제한적으로 임포트해 넣으면 mypackage의 외부 API를 명시적으로 지정할 수 있음
- 모든 내부 모듈에 이미 __all__을 지정했으므로, 이 __init__.py 안에 내부 모듈의 모든 내용을 임포트하고(mypackage의) __all__ 내용을 적절히 변경하기만 하면 mypackage의 공개 인터페이스를 노출시킬 수 있음
~~~python
# __init__.py
__all__ = []

from . models import *
__all__ += models.__all__

from .utils import *
__all__ += utils.__all__
~~~
- 다음 내부 모듈 대신 mypackage로 부터 직접 임포트하는 API 사용자 코드임
~~~python
# api_cosumer.py
from mypackage import *

a = Projectile(1.5, 3)
b = Projectile(4, 1.7)
after_a, after_b = simulate_collision(a, b)
~~~
- 코드를 보면 알 수 있듯이 mypackage.utils.__dot_product와 같은 내부 전용 함수는 __all__에 들어 있지 않으므로 함수를 사용할 수 없음
- __all__에서 제외됐다는 말은 `from mypackage import *` 명령으로 임포트해도 임포트되지 않는다는 뜻
- 따라서 결과적으로 내부 전용 이름만 외부에서 볼 수 없게 감춰짐
- 명시적이고 안정적인 API를 제공하는 것이 중요할 때 이런 접근 방법이 매우 효과적임
- 하지만 작성 중인 모듈 사이에 공유돼야 하는 API를 만들고 있다면 __all__ 기능이 불필요하거나, 아예 사용하지 말아야 할 수도 있음
- 일반적으로 대규모 코드를 작성하면서 협업하는 프로그래머 팀 내부에서는 패키지가 제공하는 이름 공간에서 어느 정도 타당한 인터페이스 경계를 유지하는 것으로 충분한 경우가 많음

#### Warning import *를 조심해라
- `from x import y` 같은 임포트 문을 쓰면, x 패키지나 모듈로부터 y를 임포트한다고 명시하므로 x가 어디서 비롯됐는지 명확히 알 수 있음
- 와일드카드(wildcard) 임포트인 `from foo import *`도 유용함
- 특히 대화식으로 파이썬을 사용하는 세션에서 이런 와일드카드 임포트가 꽤 쓸모 있음
- 하지만 와일드카드를 사용하면 코드를 이해하기 어려워짐
- `from foo import *` 를 사용하면 코드를 처음 보고 어떤 이름이 어디서 비롯됐는지 알지 못하게됨
- 어떤 모듈 안에 import * 문이 여럿 들어가 있다면, 어떤 이름이 들어 있는 모듈을 찾기 위해 와일드카드 임포트 문이 참조하는 모든 모듈을 뒤져야 함
- `import *` 로 가져온 이름이 현재 모듈에 있는 이름과 겹치면 기존 이름을 덮어 쓰게 됨
- 여러 import * 문을 사용해 이름을 가져와서 사용할 때 이런 식으로 이름이 겹치는 경우에는 우리의 코드와 겹친 이름으로 인해 이상한 문제가 발생할 수 있음
- 가장 안전한 접근 방법은 코드를 작성할 때 `import *` 를 사용하지 않고 from x import y 스타일을 써서 명시적으로 이름을 임포트하는 것임

#### 기억해야 할 내용
- 파이썬 패키지는 다른 모듈을 포함하는 모듈임. 패키지를 사용하면 서로 분리돼 충돌이 일어나지 않는, 유일한 절대 모듈 경로를 사용하는 이름 공간으로 코드를 나눌 수 있음
- 다른 소스 파일이 들어 있는 디렉터리에 __init__.py 파일을 추가하면 간단한 패키지를 만들 수 있음
- 소스 파일들은 디렉터리로 인해 생긴 패키지의 자식 모듈이 됨. 패키지 디렉터리에는 다른 패키지가 들어갈 수도 있음
- 모듈 외부에서 볼 수 있게 허용할 이름을 __all__ 특별 애트리뷰트에 지정해 공개 API를 제공할 수 있음 
- 패키지의 __init__.py 파일에 외부에 공개할 이름만 임포트하거나 패키지 내부에서만 사용할 이름 앞에 _를 붙임으로써 패키지 내부에서만 사용할 수 있는 이름을 감출 수 있음
- 단일 코드베이스나 단일 팀 안에서 협업을 진행한다면 아마도 __all__로 API를 명시할 필요가 없을 것임

### 86-배포 환경을 설정하기 위해 모듈 영역의 코드를 사용해라
- 배포 환경은 프로그램이 실행될 설정을 뜻함. 모든 프로그램에는 배포 환경이 적어도 하나는 있음. 바로 프로덕션 환경인데, 프로그램을 작성하는 궁극적인 목표는 프로덕션 환경에서 프로그램을 실행해 원하는 결과를 얻어내는 것임
- 프로그램을 작성하고 수정하려면 우리가 프로그램을 개발할 때 사용하는 컴퓨터상에서 프로그램을 실행할 수 있어야 함. 우리의 개발 환경은 프로덕션 환경과 많이 다를 수 있음. 예를 들어 슈퍼컴퓨터에서 실행될 프로그램을 작은 기판 하나짜리 컴퓨터에서 개발할 수도 있음 
- venv 같은 도구를 쓰면 모든 환경에 똑같은 파이썬 패키지가 설치되게 할 수 있음. 문제는 프로덕션 환경의 경우 개발 환경에서 재현하기 힘든 외부 가정이 많을 수 있다는 점임
- 예를 들어 웹서버 컨테이너 안에서 프로그램을 실행시키되 프로그램이 데이터베이스에 접근할 수 있도록 허용하고 싶다고 하자. 프로그램 코드를 변경할 때마다 서버 컨테이너를 실행하고, 데이터베이스 스키마를 적절히 갱신해주어야 함
- 또 데이터베이스 접근에 필요한 암호를 프로그램이 알고 있어야 함. 프로그램에서 한 줄만 변경한 뒤 제대로 동작하는지 검증하고 싶을 뿐인데, 이 모든 작업을 다시 해야 한다면 비용이 너무 비쌈
- 이러한 문제를 우회하는 가장 좋은 방법은 프로그램을 시작할 때 프로그램 일부를 오버라이드해서 배포되는 환경에 따라 다른 기능을 제공하도록 만드는 것임
- 예를 들어 프로덕션과 개발 환경에 따라 두 가지 __main__ 파일을 사용할 수도 있음
~~~python
# dev_main.py
TESTING = True

import db_connection

db = db.connection.Database()

# prod.main.py
TESTING = False

import db_connection
db = db_connection.Database()
~~~
- 두 파일의 차이는 TESTING 상수의 값이 다르다는 점. 프로그램의 다른 모듈들은 __main__ 모듈을 임포트해서 TESTING의 값에 따라 자신이 정의하는 애트리뷰트 값을 결정할 수 있음
~~~python
# db_connection.py
import __main__

class TestingDatabase:
    ...

class RealDatabase:
    ...

if __main__.TESTING:
    Database = TestingDatabase
else:
    Database = RealDatabase
~~~
- 여기서 알아둬야 할 핵심은 모듈 영역에서 실행되는 코드가 일반적인 파이썬 코드일 뿐이라는 점
- if문을 모듈 수준에서 사용하면 모듈 안에서 이름이 정의되는 방식을 결정할 수 있음
- 이를 통해 더 쉽게 다양한 배포 환경에 맞춰 모듈을 구성할 수 있고, 데이터베이스 설정처럼 비용이 많이 드는 가정이 불필요한 배포 환경이라면 아예 이런 설정을 제외시킬 수 있음
- 대화식 개발을 편하게 해주는 로컬 구현이나 가짜 구현을 주입할 수도 있고, mock을 구현해서 넣을 수도 있음
- 배포 설정 환경이 복잡해지면, config 파일 등으로 옮겨야 함. configparser 내장 모듈 같은 도구를 사용하면 프로덕션 설정을 코드로부터 분리해 유지 보수 할 수 있음. 
- 특히 제품을 운용하는 팀이 따로 있는 경우에는 협업할 때 설정과 코드를 구분하는 것이 중요
- 이런 접근 방법은 외부 환경에 대한 가정을 우회하기 위한 것 이상의 용도로 사용될 수 있음. 예를 들어 프로그램이 호스트 플랫폼에 따라 다르게 작성해야 한다는 것을 안다면 모듈에서 최상위 모듈을 정의하기 전에 sys 모듈을 살펴보면 됨
~~~Python
# db_connection.py
import sys

class Win32Database:
    ...

class PosixDatabase:
    ...

if sys.platform.startswith('win32'):
    Database = Win32Database
else:
    Database = PosixDatabase
~~~
- 비슷한 방식으로 `os.environ`에서 얻은 환경 변수를 모듈 정의에 참조할 수도 있음

### 기억해야 할 내용
- 고유한 가정과 설정이 있는 다양한 배포 환경에서 프로그램을 실행해야 하는 경우가 많음
- 모듈 영역에서 일반적인 파이썬 문을 사용하면 각 배포 환경에 맞게 모듈의 내용을 조정할 수 있음
- 모듈 내용은 모든 외부 조건에 따라 달라질 수 있는 결과물. 외부 조건에는 sys나 os 모듈을 사용해 알아낸 호스트 인트로스펙션 정보가 포함됨

### 87-호출자를 API로부터 보호하기 위하여 최상위 Exception을 정의해라
- 모듈 API에서는 모듈 내에 우리가 정의한 함수 또는 클래스만큼이나 우리가 발생시킬 예외에도 API의 일부분으로서 중요함
- 파이썬 언어와 표준 라이브러리에는 이미 예외 계층 구조가 내장돼 있음. 우리가 직접 정의한 예외 타입을 사용해 오류를 보고하는 것이나 내장 예외 타입을 사용해 오류를 보고하는 것은 비슷함. 예를 들어 직접 만든 모듈의 함수에 잘못된 파라미터가 전달되면 ValueError 예외를 던질 수 있음
~~~python
# my_module.py
def determine_weight(volume, density):
    if density <= 0:
        raise ValueError('밀도는 0보다 커야 합니다')
    ...
~~~
- 경우에 따라 ValueError를 사용하는 편이 타당할 때도 있지만, <b>API의 경우 새로운 예외 계층 구조를 정의하는 편이 훨씬 강력함</b>
- 모듈에 최상위 Exception을 정의하고 모듈이 발생시키는 다른 모든 예가 이 최상위 예외를 상속하게 만듦으로써 API에서 발생하는 예외의 계층 구조를 만들 수 있음
~~~python 
# my_module.py
class Error(Exception):
    """이 모듈에서 발생할 모든 예외의 상위 클래스."""


class InvalidDensityError(Error):
    """밀도 값이 잘못된 경우."""


class InvalidVolumeError(Error):
    """부피 값이 잘못된 경우."""


def determine_weight(volume, density):
    if density < 0:
        raise InvalidDensityError('밀도는 0보다 커야 합니다')
    if volume < 0:
        raise InvalidVolumeError('부피는 0보다 커야 합니다')
    if volume == 0:
        density / volume
~~~
- 어떤 모듈 안에 최상위 예외가 있으면 API 사용자들이 이 모듈에서 발생한 모든 오류를 더 쉽게 잡아낼 수 있음. 예를 들어 우리가 정의한 API를 사용하는 사용자가 함수를 호출하면서 try/except 문을 사용함으로써 최상위 예외를 잡아낼 수 있음
~~~python
import my_module
import logging

try:
    # 오류가 나야 함
    weight = my_module.determine_weight(1, -1)
except my_module.Error:
    logging.exception('예상치 못한 오류')

>>>
ERROR:root:예상치 못한 오류
Traceback (most recent call last):
  File "<input>", line 6, in <module>
  File "/Users/heojaehun/gitRepo/TIL/effectivePython/my_module.py", line 15, in determine_weight
    raise InvalidDensityError('밀도는 0보다 커야 합니다')
my_module.InvalidDensityError: 밀도는 0보다 커야 합니다
~~~
- 여기서 `logging.exception` 함수가 잡아낸 예외의 전체 스택 트레이스를 출력하기 때문에 더 쉽게 이 상황을 디버깅할 수 있음
- `try/except` 문을 사용하면 우리 모듈에서 발생한 예외가 모듈을 호출하는 코드로부터 아주 멀리 전달돼 프로그램이 깨지는 상황을 방지할 수 있음
- 이런 식으로 최상위 예외가 있으면 우리가 제공하는 API로부터 호출하는 코드를 보호할 수 있음
- 이런 보호로 인해 세 가지 유용한 효과가 나타남
- 첫 번째 효과는 최상위 예제가 있으면 API를 호출하는 사용자가 API를 잘못 사용한 경우에 더 쉽게 이해할 수 있다는 점임. 호출자가 API를 제대로 사용한다면 API에서 의도적으로 발생시킨 여러 예외를 잡아내야만 함
- 사용자가 이런 예외를 잡아내지 않으면, 우리가 만든 모듈의 최상위 예외를 잡아내는 방어적인 except 블록까지 예외가 전달됨
- 이 블록은 API 사용자의 주의를 환기시키고, 사용자가 깜빡한 예외 타입을 제대로 처리할 기회를 제공함
~~~python
import my_module
import logging

try:
    # 호출 코드 버그로 인한 오류가 나야 함
    weight = my_module.determine_weight(-1, 1)
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error:
    logging.exception('호출 코드에 버그가 있음')

>>>
ERROR:root:호출 코드에 버그가 있음
Traceback (most recent call last):
  File "<input>", line 6, in <module>
  File "/Users/heojaehun/gitRepo/TIL/effectivePython/my_module.py", line 17, in determine_weight
    raise InvalidVolumeError('부피는 0보다 커야 합니다')
my_module.InvalidVolumeError: 부피는 0보다 커야 합니다
~~~
- 두 번쨰 효과는 API 모듈 코드의 버그를 발견할 때 도움이 된다는 점. 우리가 작성한 모듈 코드는 의도적으로 모듈 내에서 정의한 예외 계층에 속하는 예외만 발생시킬 수 있음
- 이 경우 우리 모듈에서 다른 타입의 예외가 발생한다면, 이 예외는 우리가 의도하지 않은 것. 즉 우리가 구현한 API 코드에 버그가 있다는 뜻임
- 앞에서 설명한 모듈의 최상위 예외를 잡아내는 try/except문이 모듈의 버그로부터 API 소비자들을 보호하지는 못함
- 그러므로 호출하는 쪽에서 파이썬의 기반 Exception 클래스를 잡아내는 다른 except 블록을 추가해야 함  
- 이렇게 두 가지 except문을 사용하면 API 소비자가 API 모듈에 수정해야 할 버그가 있는 경우를 쉽게 알 수 있음. 다음 예제의 출력은 `logging.exception`이 출력한 메세지와 파이썬 Exception을 다시 발생시켰으므로 인터프리터가 출력한 디폴트 예외 메세지를 모두 보여줌
~~~python
import my_module
import logging

try:
    # API 코드 버그로 인한 오류가 나야 함
    weight = my_module.determine_weight(0, 1)
except my_module.InvalidDensityError:
    weight = 0
except my_module.Error:
    logging.exception('호출 코드에 버그가 있음')
except Exception:
    logging.exception('API 코드에 버그가 있음!')
    raise # 예외를 호출자쪽으로 다시 발생시킴

>>>
ERROR:root:API 코드에 버그가 있음!
Traceback (most recent call last):
  File "<input>", line 6, in <module>
  File "/Users/heojaehun/gitRepo/TIL/effectivePython/my_module.py", line 19, in determine_weight
    density / volume
ZeroDivisionError: division by zero
Traceback (most recent call last):
  File "<input>", line 6, in <module>
  File "/Users/heojaehun/gitRepo/TIL/effectivePython/my_module.py", line 19, in determine_weight
    density / volume
ZeroDivisionError: division by zero
~~~
- 세 번째 효과는 미래의 API를 보호해준다는 점. 시간이 지남에 따라 API를 확장해 특정 상황에서 더 구체적인 예외를 제공하고 싶을 때가 있음
- 예를 들어 밀도가 음수인 경우를 오류 조건으로 표시해주는 Exception 하위 클래스를 추가할 수 있음
~~~python
# my_module2.py
class Error(Exception):
    """이 모듈에서 발생할 모든 예외의 상위 클래스."""


class InvalidDensityError(Error):
    """밀도 값이 잘못된 경우."""


class InvalidVolumeError(Error):
    """부피 값이 잘못된 경우."""


#- 새로운 exception 모듈 추가
class NegativeDensityError(InvalidDensityError):
    """밀도가 음수인 경우."""


def determine_weight(volume, density):
    if density < 0:
        raise NegativeDensityError('밀도는 0보다 커야 합니다')
    if volume < 0:
        raise InvalidVolumeError('부피는 0보다 커야 합니다')
    if volume == 0:
        density / volume
~~~
- 모듈을 호출하는 코드는 코드를 변경하지 않아도 똑같이 잘 작동함. InvaildDensityError 예외를 이미 처리하기 때문
- 나중에 호출하는 코드에서 새로운 타입이 예외를 더 처리하기로 결정하면, 그에 따라 처리 동작을 수정할 수 있음
~~~python
# NegativeDensityError를 정의한 모듈의 이름을 편의상 my_module2로 바꿈.
import my_module2
import logging


try:
    #
    weight = my_module2.determine_weight(1, -1)
except my_module2.NegativeDensityError as exc: #- 예외 처리 추가
    raise ValueError('밀도로 음수가 아닌 값을 제공해야 합니다') from exc
except my_module2.InvalidDensityError: 
    weight = 0
except my_module2.Error:
    logging.exception('호출 코드에 버그가 있음')
except Exception:
    logging.exception('API 코드에 버그가 있음!')
    raise # 예외를 호출자쪽으로 다시 발생시킴
~~~
- 최상위 예외 바로 아래에 폭넓은 예외 상황을 표현하는 다양한 오류를 제공하면 미래의 코드 변경에 대한 보호를 더 강화할 수 있음
- 예를 들어 무게 계산 관련 예외, 부피 계산 관련 예외, 밀도 계산 관련 예외를 추가하는 경우가 있을 수 있음
~~~python
class Error(Exception):
    """이 모듈에서 발생할 모든 예외의 상위 클래스."""

class WeightError(Error):
    """무게 계산 관련 예외의 상위 클래스"""

class VolumeError(Error):
    """부피 계산 관련 예외의 상위 클래스"""

class DensityError(Error):
    """밀도 계산 관련 예외의 상위 클래스"""
~~~
- 구체적인 예외는 이런 일반적인 예외를 상속함. 각각의 중간 단계 예외는 각각 최상위 예외 역할을 함
- 이렇게 하면 API 코드로부터 API를 호출하는 코드를 보호하는 계층을 쉽게 추가할 수 있음
- 모든 호출 코드가 구체적인 Exception 하위 클래스 예외를 일일이 처리하게 하는 것보다 이런 식의 예외 계층 구조를 채택하는 편이 훨씬 나음

#### 기억해야 할 내용
- 모듈에서 사용할 최상위 예외를 정의하면 API 사용자들이 자신을 API로부터 보호할 수 있음
- 최상위 예외를 잡아내면 API를 소비하는 코드의 버그를 쉽게 찾을 수 있음
- 파이썬 Exception 기반 클래스를 잡아내면 API 구현의 버그를 쉽게 찾을 수 있음
- 중간 단계의 최상위 예외를 사용하면, 미래에 새로운 타입의 예외를 API에 추가할 때 API를 사용하는 코드가 깨지는 일을 방지할 수 있음

### 88-순환 의존성을 깨는 방법을 알아두라
- 다른 사람들과 협업하다 보면 불가피하게 모듈들이 상호 의존하는 경우가 생김
- 이는 심지어 한 프로그램의 여러 부분을 홀로 작업할 때도 발생할 수 있음
- 예를 들어 GUI 애플리케이션에서 문서 저장 위치를 선택할 수 있는 대화창을 띄우고 싶음. 대화창이 표시하는 정보는 이벤트 헨들러의 인자를 통해 구체적으로 전달됨
- 하지만 대화창이 사용자 선호 설정 등과 같은 전역 상태를 읽어야 자기 자신을 화면에 바로 그릴 수 있음
- 다음 코드는 전역 선호도 설정에서 디폴트 문서 저장 위치를 가져오는 대화창을 정의함
~~~python
import app


class Dialog:
    def __init__(self, save_dir):
        self.save_dir = save_dir


save_dialog = Dialog(app.prefs.get('save_dir'))


def show():
    pass
~~~
- 문제는 `prefs` 객체가 들어 있는 app 모듈이 프로그램 시작 시 대화창을 표시하고자 앞에서 정의한 dialog를 임포트 한다는 점
~~~python
import dialog


class Prefs:

    def get(self, name):
        pass


prefs = Prefs()
dialog.now()
~~~
- 이로 인해 순환 의존 관계가 생김. app 모듈을 메인 프로그램에서 임포트하려고 시도하면
~~~python
import app
~~~
- 다음과 같은 예외가 발생함
~~~
>>>
AttributeError: module 'app' has no attribute 'prefs'
~~~
 - 여기서 어떤 일이 벌어졌는지 이해하려면 파이썬의 임포트 기능이 일반적으로 어떻게 작동하는지 알아야함 
 - 모듈이 임포트되면 파이썬이 실제로 어떤 일을 하는지 깊이 우선순위로 나타냄
   - `sys.path`에서 모듈 위치를 검색
   - 모듈의 코드를 로딩하고 컴파일되는지 확인
   - 임포트할 모듈에 상응하는 빈 모듈 객체를 만듬
   - 모듈을 `sys.modules`에 넣음
   - 모듈 객체에 있는 코드를 실행해서 모듈의 내용을 정의함
- 순한 의존 관계에서 문제는 어떤 모듈의 애트리뷰트를 정의하는 코드(5단계)가 실제로 실행되기 전까지는 모듈의 애트리뷰트가 정의되지 않는다는 점
- 하지만 모듈 자체는 import 문을 사용해서 sys.modules에 추가되자마자(4단계) import 문을 사용해 로드할 수 있음  
(다시 말하면, 순환 의존 관계에서는 import문을 사용해 로드하는데, 정의되어 있지는 않음)
- 위 예제에서 app 모듈은 다른 모든 내용을 정의하기 전에 dialog 모듈을 import 함
- 그 후 dialog 모듈은 app을 임포트함. app이 아직 실행되지 않았기 때문에 app 모듈은 비어있음(4단계)
- 따라서 prefs 애트리뷰트를 정의하는 코드가 아직 실행되지 못했기 때문에 Attribute 에러 발생
- 이 문제를 해결하는 가장 좋은 방법은 코드를 리펙터링해서 prefs 데이터 구조를 의존 관계 트리의 맨 밑바닥으로 보내는 것임
- 이렇게 변경하고 나면 app과 dialog가 모두 (prefs가 들어있는) 같은 유틸리티 모듈을 임포트하고 순환 임포트를 피할 수 있음
- 하지만 리펙터링이 너무 어려워 노력할 만한 가치가 없거나 아예 이런식의 명확한 구분이 불가능한 경우가 있음
- 순환 임포트를 깨는 3가지 방법이 있음

#### 임포트 순서 바꾸기
첫 번째 접근 방법은 임포트 순서를 바꾸는 것임. 예를 들어 app의 모든 내용이 모두 실행된 다음, 맨 뒤에서 dialog 모듈을 임포트하면 AttributeError가 사라짐
~~~python
class Prefs:

    def get(self, name):
        pass


prefs = Prefs()
import dialog
dialog.show()
~~~
- 이런 코드가 제대로 작동하는 이유는 dialog 모듈이 나중에 로딩될 때 dialog 안에서 재귀적으로 임포트한 `app`에 `app.pref`가 이미 정의돼 있기 때문(app에 대해 5단계가 거의다 수행됨)
- 이런 방식이 AttributeError를 없애주기는 하지만, PEP 8 스타일 가이드에 위배됨. 스타일 가이드는 항상 파이썬 파일의 맨 위에 임포트를 넣으라고 제안함
- 그리고 임포트가 맨 앞에 있어야 우리가 의존하는 모듈이 우리 모듈 코드의 모든 영역에서 항상 사용 가능할 것이라 확신함
- 파일의 뒷부분에 임포트를 넣으면 깨지기 쉽고, 코드 순서를 약간만 바꿔도 망가질 수 있음
- 순환 임포트 문제를 해결하기 위해 임포트 순서를 바꾸는 것은 권하지 않음

#### 임포트, 설정, 실행
- 순환 임포트 문제에 대한 두 번째 해결 방법으로는 임포트 시점에 부작용을 최소하한 모듈을 사용하는 것
- 모듈이 함수, 클래스, 상수만 정의하게 하고, 임포트 시점에 실제로 함수를 전혀 실행하지 않게 만듬
- 그 후 다른 모듈이 모두 임포트를 끝낸 후 호출할 수 있는 `configure` 함수를 제공
- `configure`의 목적은 다른 모듈들의 애트리뷰트에 접근해 모듈 상태를 준비하는 것
- 다른 모든 모듈을 임포트한 다음에(다른 모듈의 5단계가 끝난 후) configure를 실행하므로 configure가 실행되는 시점에는 항상 모든 애트리뷰트가 정의돼 있음
- 다음 코드는 `configure`가 호출될 때만 `prefs` 객체에 접근하도록 `dialog` 모듈을 재 정의함
~~~python
import app


class Dialog:
    def __init__(self, save_dir):
        self.save_dir = save_dir


save_dialog = Dialog()


def show():
    pass

def configure():
    save_dialog.save_dir = app.prefs.get('save_dir')
~~~
- 또한 app 모듈도 임포트 시 동작을 수행하지 않게 다시 정의함
~~~python
import dialog

class Prefs:
    pass

prefs = Prefs()

def configure():
    pass
~~~
- 마지막으로 main 모듈은 모든 것을 import 하고, 모든 것을 configure하고, 프로그램의 첫 동작을 실행하는 세 가지 단계를 거침
~~~python 
import app
import dialog
app.configure()
dialog.configure()

dialog.show()
~~~
- 이런 구조는 대부분 잘 작동하며 의존 관계 주입 같은 다른 패턴을 적용할 수 있음 
- 하지만 코드 구조를 변경해서 명시적인 configure 단계를 분리할 수 없을 때도 있음
- <b>단점: 모듈 안에 서로 다른 단계가 둘 이상 있으면, 객체를 정의하는 부분과 객체를 설정하는 부분이 분리되기 때문에 코드를 읽기가 더 어려워짐</b>

#### 동적 임포트
- 순환 임포트에 대한 세 번쨰 해결 방법은 import 문을 함수나 메서드 안에서 사용하는 것
- 프로그램이 처음 시작하거나 <b>모듈을 초기화하는 시점이 아니라 프로그램이 실행되는 동안 모듈 임포트가 일어나기 때문에 이를 동적 임포트</b>라고 함
- 다음 코드는 동적 임포트를 사용해 dialog 모듈을 재정의함. dialog 모듈이 초기화될 때 app을 임포트하는 대신, dialog.show 함수가 실행 시점에 app 모듈을 임포트 함
~~~python
# dialog.py
class Dialog:
    def __init__(self):
        ...
    
save_dialog = Dialog()
    
def show():
    import app # 동적 임포트
    save_dialog.save_dir = app.prefs.get('save_dir')
    ...
~~~
- 이제 app 모듈은 맨 처음 예제 코드와 같음. app 모듈은 dialog를 맨 위에서 임포트하고 맨 아래에서 `dialog.show`를 호출함
~~~python
import app


class Dialog:
    def __init__(self, save_dir):
        self.save_dir = save_dir


save_dialog = Dialog()


def show():
    pass

def configure():
    save_dialog.save_dir = app.prefs.get('save_dir')
~~~
- 이런 접근 방법은 앞에서 본 임포트, 설정, 실행 단계를 사용하는 방식과 비슷한 효과를 나타냄
- 차이가 있다면 동적 임포트 방식에는 모듈을 정의하고 임포트하는 방식을 구조적으로 변경하지 않아도 된다는 점. 단지 순환적인 임포트를 실제로 다른 모듈에 접근해야만 하는 시점으로 지연시켰을 뿐
- 이 시점에서는 모든 다른 모듈이 이미 초기화됐다는 것을 충분히 확신할 수 있음
- 일반적으로 이런 동적 임포트는 피하면 좋음. import 문의 비용이 무시하지 못할 만큼 크며, 특히 자주 빠르게 반복되는 루프 안에서 임포트를 사용하면 악영향이 커짐
- 동적 임포트를 사용하면 임포트 실행을 미루기 때문에 실행 시점에 예기치 못한 오류로 인해 놀랄 수도 있음
- 예를 들어 프로그램이 시작되고 실행된 다음에 한참 있다가 SyntaxError가 발생하는 등의 일이 벌어질 수 있음
- 하지만 이런 단점을 감수하는 것이 프로그램 전체 구조를 바꾸는 경우보다 나은 일이 많음

#### 기억해야 할 내용
- 두 모듈이 임포트 시점에 서로를 호출하면 순환 의존 관계가 생김. 순환 의존 관계가 있으면 프로그램이 시작되다가 오류가 발생하면서 중단될 수 있음
- 순한 의존 관계를 깨는 가장 좋은 방법은 상호 의존 관계를 의존 관계 트리의 맨 아래에 위치한 별도의 모듈로 리펙터링 하는 것
- 동적 임포트는 리펙터링과 복잡도 증가를 최소화하면서 모듈 간의 순환 의존 관계를 깨는 가장 단순한 해법임

### 89- 리펙터링과 마이그레이션 방법을 알려주기 위해 warning을 사용해라
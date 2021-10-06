## python 기본환경설정

### python 가상 환경
- 각 프로젝트별 버전관리를 용이하게 하기 위함  
  ex) 머신러닝, 데이터 파이프라인.. 등
- 가상환경 설정(mac) 방법
~~~shell
# mac
python3 -m venv p_study # p_study라는 가상 환경 생성
cd p_study
source /bin/activate   # 가상환경 활성화
source /bin/deactivate # 가상환경 비활성화

# package 설치
pip list # package list 확인

# datetime 계산을 쉽게 계산하게 해주는 굉장히 유명한 라이브러리
# 동시에 의존성 있는 패키지들을 함께 설치됨
pip install pendulum 

# pytest package 설치
pip install pytest
~~~

### VSCode 환경 설정(MacOS)

#### 간단 명령어를 통한 VSCode 실행을 위한 설정
- 기본 MacOS는 python이 2.x가 설치되어 있음
- 기본적으로 python 2.x를 global로 적용하는 것이 나음
- `command +-` 로 폰트 크기 조절 가능
- `View` 메뉴에서 `Command Palette` 가 있는지 확인
- `Command Palette`를 클릭하고, `shell command`라고 입력한 후, command에서 `code`라고만 입력해도 vscode가 실행됨

#### extention을 통한 python 설치
- `View` 메뉴에서 `extention` 클릭

#### 가상환경 설정
- terminal에서 
- 파이썬에서 가상환경은 굉장히 많음. pyenv.. 등이 있는데 똑같은 기능을 함
~~~shell
python3 -m venv p_study  
ls bin/
source ./activate  # 가상환경 활성화
~~~
- 가상환경의 상위 폴더(document)를 열어야 함
- `Command Palette`를 클릭 후 `python intepreter` 클릭
- p_study란 venv를 찾을 수 있음
- `pip install`로 다양한 package를 설치할 수 있음
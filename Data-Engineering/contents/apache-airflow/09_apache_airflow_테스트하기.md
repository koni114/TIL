# chapter09 테스트하기
- 이번 장에서는 개발한 코드가 실제 서비스에 배포되기 전에 Airflow 테스트에 대해서 설명함
- 일반적으로 Airflow 은 비교적 많은 타 시스템과의 통신이 발생하며, 오케스트레이션 시스템의 특성도 가지고 있음.  
- 로직을 실제로 수행하는 태스크를 시작하고 종료하는 역할을 하지만, airflow 자신은 어떤 로직도 수행하지 않음
- 이러한 환경에서 정상적으로 작동하지 않은 Airflow 로직을 어떻게 확인할 수 있는지 알아보자

## 테스트 시작하기
- 테스트는 다양한 단계에서 적용할 수 있는데, 각 모듈 별로 적용하는 개별 테스크 단위로 테스트를 진행하거나 여러 구성 요소의 동작을 함께 검증하는 통합 테스트를 작성할 수 있음
- 테스트 과정에서 통합 테스트 이후에는 승인 테스트(비즈니스 로직을 검증하는 테스트)를 진행
- 이번 장에서는 `pytest`라는 테스트 프레임워크를 사용하여 검증해볼 예정. 
- 이번 장에서 설명하는 코드는 Github 에 있으므로, GitHub에서 지원하는 CI/CD 시스템인 Github Action(`https://github.com/features/actions`)을 사용하여 테스트 과정에 대해서 연습해 볼 수 있음
- <b>GitLab, Bitbucket, CircleCI, Travis CI 등과 같이 널리 사용되는 모든 CI/CD 시스템은 프로젝트 디렉터리의 루트에 YAML 형식으로 파이프라인을 정의하여 작동함</b>

### 모든 DAG에 대한 무결성 테스트
- Airflow 관점에서 테스트를 위한 첫 번쨰 단계는 DAG 무결성 테스트임
- 이는 모든 DAG의 무결성(ex) DAG에 사이클이 포함되어 있지 않은지 확인 등)을 테스트함
- 다음의 DAG는 t1 > t2 > t3 > t1 으로 돌아가는 주기가 있어 UI에 오류를 표시함
~~~python
t1 = DummyOperator(task_id='t1', dag=dag)
t2 = DummyOperator(task_id='t2', dag=dag)
t3 = DummyOperator(task_id='t3', dag=dag)

t1 >> t2 >> t3 >> t1
~~~

#### pytest 설치 및 directory 구성
- pytest 를 설치하면, pytest CLI 유틸리티를 사용할 수 있음
- pytest [file/directory]로 테스트를 실행할 수 있는 구조를 만들어보자
- <b>일반적으로 테스트 영역을 구성하는 방법은 프로젝트의 최상단 디렉터리에 별도의 tests/ 디렉터리를 생성하여 검사 대상 코드를 그대로 복사하여 구성함</b> 
- 프로젝트 구조가 아래의 표시된 것과 같이 구성되어 있다면,  
```
├── dags
    ├── dag1.py
    ├── dag2.py
    ├── dag3.py
├── mypackage
    ├── airflow
        ├── hooks
            ├── __init__.py
            ├── movielens_hook.py
        ├── operators
            ├── __init__.py
            ├── movielens_operator.py
        ├── sensors
            ├── __init__.py
            ├── movielens_sensors.py
    ├── movielens
        ├── __init__.py
        ├── utils.py
```
- `tests/` 디렉터리 구조는 아래와 같이 구성됨
```
├── dags
├── mypackage
├── tests
    ├── dags
        ├── test_dag_integrity.py
    ├── mypackage
        ├── airflow
            ├── hooks
                ├── test_movielens_hook.py
            ├── operators
                ├── test_movielens_operator.py
            ├── sensors
                ├── test_movielens_sensor.py
        ├── movielens
            ├── test_utils.py 
```
- 모든 테스트 대상 파일은 파일 이름을 그대로 따르고 `test_` 접두사를 붙임
- Pytest 프레임워크를 사용하는 경우에도 `test_` 접두사가 필요함. 
- Pytest는 주어진 디렉터리를 스캔하고 `test_` 접두사 또는 `_test` 접미사 파일을 검색함  
  또한 tests/ 디렉터리에는 `__init__.py` 파일이 없음
- 이제부터 `test/dags/test_dag_integrity.py` 라는 파일을 만들어보자
~~~python
# test_dag_integrity.py
import glob
import importlib.util
import os
import pytest
from airflow.models import DAG

DAG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dags/**/*.py"
)

DAG_FILES = glob.glob(DAG_PATH, recursive=True)


@pytest.mark.parametrize("dag_file", DAG_FILES)
def test_dag_integrity(dag_file):
    module_name, _ = os.path.splitext(dag_file)
    module_path = dag_file
    mod_spec = importlib.util.spec_from_file_location(module_name, module_path)

    module = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(module)

    dag_objects = [var for var in vars(module).values() if isinstance(var, DAG)]
    
    assert dag_objects        #- test 1
    for dag in dag_objects:   #- test 2
        dag.test_cycle()
~~~
- 위의 코드를 부분적으로 뜯어보면서 파악해보자
~~~python
DAG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dags/**/*.py"
)
~~~
- `__file__`은 현재 실행되는 script 의 Fullpath + py script name 을 나타냄
- `/**/` 는 Recursive 하게 파일을 탐색함. 예를 들어 `dags/dir1/dir2/dir3/mydag.py` 의 파일도 탐색함  
  (`glob.glob` 함수에 recursive=True 로 지정하면 탐색 가능!)
~~~python
@pytest.mark.parametrize("dag_file", DAG_FILES)
def test_dag_integrity(dag_file):
    ... 
~~~ 
- decorator `@pytest.mark.parametrize` 는 DAG_FILES 에 들어있는 모든 list 값을 해당 함수에 넣어 test 수행함  
- DAG_FILES 의 값들을 한 개씩 dag_file 에 넣어 수행
~~~python
module_name, _ = os.path.splitext(dag_file)
module_path = dag_file
mod_spec = importlib.util.spec_from_file_location(module_name, module_path)

module = importlib.util.module_from_spec(mod_spec)
mod_spec.loader.exec_module(module)
~~~
- dag_file 에 들어있는 모듈(.py)들을 실행하고 난 후의 결과를 module 변수에 저장
~~~python
dag_objects = [var for var in vars(module).values() if isinstance(var, DAG)]
~~~
- 파일에서 객체로 DAG 가 존재하면 dag_object 에 list 형태로 저장
- `vars` 함수는 python 내장함수로, 해당 모듈 내에 지역변수 값들을 dictionary 형태로 반환해줌
~~~python
assert dag_objects

for dag in dag_objects:
    dag.test_cycle()
~~~
- 위의 코드에서 2가지 검사를 수행.
  - `assert` 로 dag_objects 로 파일에서 DAG 객체를 성공적으로 찾았는지 확인
  - `test_cycle()`로 DAG에 대한 순환주기검사를 수행 
- Airflow 1.10.0 버전에서는 DAG의 구조가 변경될 떄마다 순환 주기의 문제가 없는지 확인했지만, 이는 변경 시점마다 검사하게되어 작업에 부담이 되어 DAG 주기 검사는 DAG를 파싱한 후 한 번만 수행되도록 변경됨
- 명령 줄에서 `pytest`를 실행함
~~~shell
$ pytest tests/
~~~

### CI/CD 파이프라인 설정하기
- <b>CI/CD 파이프라인을 한 마디로 정의하면, 코드 저장소를 통해 코드가 변경될 떄 사전 정의된 스크립트를 실행하는 시스템</b>
- 지속적 통합(Continuous integration)은 변경된 코드가 코드 표준과 테스트 조건을 준수하는지 확인하고 검증하는 것을 말함
- 지속적 배포(Continuous Deployment)는 사람의 간섭 없이 완전히 자동화된 코드를 프로덕션 시스템에 자동으로 배포하는 것을 말함
- CI/CD 시스템은 매우 다양하며, 이번 장에서는 github action 을 다룸
- 대부분의 CI/CD 시스템은 파이프라인이 정의된 YAML 구성 파일로 시작함. 
- 성공한 파이프라인만 마스터에 병합(only merge to master with a successful pipeline) 과 같은 규칙을 정할 수 있음
- github Action 에는 .github/workflows 디렉터리에 저장된 YAML 파일이 필요함
- 임의로 airflow-tests.yaml 이라는 파일을 만들어보자
~~~YAML
name: python static checks and tests

on: [push]

jobs:
  testing:
    runs-on: ubuntu-18.04
    steps:
      - uses: actions/checkout@v1
      - name: Setup Python
        uses: actions/setup-python@v1
        with:
          python-version: 3.6.9
          architecture: x64

      - name: Install Flake8
        run: pip install flake8
      - name: Run Flake8
        run: flake8

      - name: Install Pylint
        run: pip install Pylint
      - name: Run Pylint
        run: find . -name "*.py" | xargs pylint --output-format=colorized

      - name: Install Black
        run: pip install black
      - name: Run Black
        run: find . -name "*.py" | xargs black --check

      - name: Install dependencies
        run: pip install apache-airflow pytest

      - name: Test DAG integrity
        run: pytest tests/
~~~
- Github 가 push 를 수신할 떄마다 전체 CI/CD 파이프라인을 실행하도록 지시
- 완전히 자동화된 CD 시스템에는 마스터 뿐만 아니라, 특정 브랜치에도 파이프라인이 설정되어 있음. 

### 단위 테스트 작성하기
- 이번에는 Airflow 코드를 좀 더 자세히 살펴보고 개별 단위 테스트를 시작해 보도록 하자
- 8장에서 설명한 커스텀 컴포넌트를 다시한번 살펴보자  
  예를 들어 8장의 `get_ratings()` 메서드를 가진 `MovielensHook`을 살펴보자
- `get_ratings` 함수는 여러 인자를 받는데, 그 중에 `batch_size` 가 있으며, 이는 배치 크기를 제어함  
  중요한 것은 음수가 들어오면 안됨. 음수가 들어오는 경우 400 또는 422 같은 HTTP 오류를 반환함
- 이를 해결하는 방법 중 하나는 사용자의 입력 값을 바로 전달하기 전 해당 값이 유효한지를 먼저 판단하는 절차를 구성하는 것
- 예시를 위해 주어진 두 날짜 사이의 상위 N개의 인기 영화를 반환하는 오퍼레이터인 `MovielensPopularityOperator`를 구현해 보자
- `MovielensPopularityOperator` 의 정확성에 대해서 단독으로 테스트하기 위해서는 몇가지 `pytest` 컴포넌트가 필요함
~~~python

~~~

## Pytest 프로젝트 구성하기
- `pytest` 사용시 <b>script에 접두사로 `test_` 가 붙어야 함</b>  
  이 파일 안에 테스트로 호출할 함수를 만듬
~~~python
# BashOpertor를 테스트하는 예제 함수
def test_example():
  task = BashOperator(
    task_id="test",
    bash_command="echo 'hello!'",
    xcom_push=True,
  )
result = task.execute(context={})
assert result == "hello!"
~~~
- 위의 예제에서는 `BashOperator`를 인스턴스화하고 빈 context 가 주어지고 `execute()` 함수를 호출함
- `Airflow` 가 실제 운영 설정에서 오퍼레이터를 실행하면, 템플릿 변수를 확인하고 태스크 인스턴스 콘텍스트를 설정하여 오퍼레이터에게 제공하는 등 여러 가지 작업을 실행 전후에 수행하게 됨
- <b>위의 테스트는 실제 운영 설정에서 실행하지 않고 `execute()` 메서드를 직접 호출함</b>  
  이는 오퍼레이터를 실행하기 위해 호출할 수 있는 가장 낮은 수준의 함수
- 위의 `BashOperator`는 context 가 필요 없지만, 만약 필요한 경우 key-value의 dict를 인자로 넣어야 함
- 이제 이러한 형식으로 `MovielensPopularityOperator` 에 적용해보자
~~~python
# MovielensPopularityOperator 를 테스트하는 테스트 함수의 예

def test_movielenspopularityoperator():
  task = MovielensPopularityOperator(
    task_id="test_id",
    start_date="2015-01-01",
    end_date="2015-01-03",
    top_n=5,
  )
  result = task.execute(context={})
  assert len(result) = 5
~~~
- 위의 테스트 함수를 실행하면, 필수 인수 `conn_id` 가 누락되었다고 나오는데, 이러한 경우 직접 데이터베이스를 이용해 전달하는 방법은 권장하지 않고, <b>목업(mocking)을 이용해 해결함</b>
- `Pytest` 는 mockup 과 같은 개념을 사용할 수 있도록 `pytest-mock` 패키지를 제공함 
- <b>이를 사용하려면 `mocker` 라는 인수를 테스트 함수의 인자로 전달해야 함</b>  
  이 인수는 `pytest-mock` 패키지를 사용하기 위한 시작점
~~~python
def test_movielenspopularityoperator(mocker):
  mocker.patch.object(        # 목업 객체로 객체의 속성을 패치함
    MovielensHook,            # 패치할 객체
    "get_connection",         # 패치할 함수
    return_value=Connection(    # 반환되는 값
      conn_id="test",
      login="airflow",
      password="airflow",
    ),
  )

  task = MovielensPopularityOperator(
    task_id="test_id",
    conn_id="test",
    start_date="2015-01-01",
    end_date="2015-01-03",
    top_n=5,
  )

  result = task.execute(context=None)
  assert len(result) = 5
~~~
- MovielensHook 에서의 `get_connection()` 호출은 몽키패치(monkey-patch)이며, 테스트 실행시 미리 정의된 예상 연결 객체(`mocker.patch.object` 선언부)를 반환함 
- 테스트 시 실제로 목업 객체가 호출되었는지 확인하려면, `mocker.patch.object` 결과를 변수에 할당하여 확인가능
~~~python
mock_get = mocker.patch.object(        # 목업 객체로 객체의 속성을 패치함
    MovielensHook,                     # 패치할 객체
    "get_connection",                  # 패치할 함수
    return_value=Connection(            # 반환되는 값
      conn_id="test",
      login="airflow",
      password="airflow",
    ),
  )
...
assert mock_get.call_count == 1          # 한 번만 호출된 것인지 확인
mock_get.assert_called_with("testconn")  # 예상되는 conn_id 로 호출된 것을 확인
~~~
- `assert mock_get.call_count == 1` 는 실제 운영 환경에서 Airflow 메타스토어를 실수로 여러 번 호출하지 않았는지 확인 
- `mock_get` 에는 동작을 검증하기 위해 사용할 수 있는 여러 속성이 포함되어 있음

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_34.png)

- 조심해야 할 것은 목업을 구현하는 곳은 선언부가 아닌 호출부  
- `get_connection` 의 예로 BaseHook 에 정의되어 있고, MovielensHook 에서 호출되므로, MovielensHook.get_connection 을 호출해 야함

### 디스크의 파일로 테스트하기
- <b>파이썬에서는 임시 저장소와 관련된 작업을 위한 temfile 모듈이 있음</b>
- pytest는 tmp_dir 및 tmp_path 라는 tempfile 모듈에 대한 편리한 사용 방법을 제공함  
  tmp_path 를 사용하는 예를 살펴보자
~~~python
from pathlib import Path
from airflowbook.operators.json_to_csv_operator import JsonToCsvOperator

def test_json_to_csv_operator(tmp_path: Path):  # tmp_path 는 고정으로 사용
  input_path = tmp_path / "input.json"          # 경로를 정의
  output_path = tmp_path / "output.csv" 

  input_data = [
    {"name": "bob", "age": "41", "sex": "M"},
    {"name": "alice", "age": "24", "sex": "F"},
    {"name": "carol", "age": "60", "sex": "F"}, 
  ]

  with open(input_path, "w") as f:
    f.write(json.dumps(input_data))

  operator = JsonToCsvOperator(
    task_id="test",
    input_path=input_path,
    output_path=output_path,
  )

  operator.execute(context={})  # JsonToCsvOperator 실행

  # 출력 파일 읽기
  with open(output_path, "r") as f:
    reader = csv.DictReader(f)
    result = [ dict(row) for row in reader ]
  
  # 테스트 후 tmp_path 와 콘텐츠는 제거
  assert result == input_data  # 내용 확인을 위한 assert

~~~
- 테스트가 시작되면 임시 디렉토리가 생성되는데, 실제로 `tmp_path` 인수는 각 테스트 시 호출되는 함수를 나타냄  
  `pytest` 에서는 이를 <b>픽스처(fixture)라고 함</b>
- 픽스처는 기본적으로 모든 테스트 영역에서 적용 가능
- 경로를 출력하며 서로 다른 테스트를 실행하거나, 동일한 테스트를 두 번 실행하면 이를 확인할 수 있음
~~~python
print(tmp_path.as_posix())
~~~

## 테스트에서 DAG 및 태스크 콘텍스트로 작업하기


## 용어 정리
- 코드 스니펫(code snippet)
  - 재사용 가능한 작은 소스코드를 의미함
- 몽키패치(monkey-patch)
  - 런타임 시에 기능을 대체하여 Airflow 메타스토어를 쿼리하는 대신 지정된 객체를 반환함 
- 픽스처(Fixture)
  - 테스트 수행을 위해 필요한 부분들을 혹은 조건들을 미리 준비해놓은 리소스 혹은 코드
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
- `tests/` 디렉터리에는 `__init__.py` 파일이 없음. 그 이유는 test 디렉터리는 모듈로 동작하는 구조가 아니기 때문에 테스트 작업은 서로 의존적이지 않으며 독립적으로 실행할 수 있어야 함
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
    assert dag_objects

    for dag in dag_objects:
        dag.test_cycle()
~~~
- 위의 코드에서 2가지 검사를 수행.
  - `assert` 로 dag_objects 로 파일에서 DAG 객체를 성공적으로 찾았는지 확인
  - `test_cycle()`로 DAG에 대한 순환주기검사를 수행 


## 용어 정리
- 코드 스니펫(code snippet)
  - 재사용 가능한 작은 소스코드를 의미함    
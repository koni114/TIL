## 나의 첫 번째 데이터 파이프라인 구축하기
### NFT 파이프라인 프로젝트 소개
- 데이터 파이프라인을 DAG 형식으로 제작할 예정

#### 프로젝트 소개
- OpenSea 사이트의 NFT 데이터를 추출해 테이블에 저장하기
  - NFT는 소유권을 가지게 할 수 있도록 하는 블록체인 프로젝트 
  - OpenSea 는 소유권을 사고 팔 수 있도록 해주는 사이트
- 데이터 파이프라인
  - 테이블 생성(sqlLite engine 사용) -> API 확인(senser 이용) -> NFT 정보 추출(HTTP simple operator) -> NFT 정보 가공(python operator) -> NFT 정보 저장(bash operator)
- api.opensea.io 를 사용하여 NFT 하나에 데이터 하나를 받아 올 수 있음 

### DAG Skeleton
- 먼저 airflow webserver 및 scheduler 를 열어서 실행
~~~shell
airflow webserver
airflow scheduler
~~~
- $HOME 의 airflow directory 로 이동하면 다음과 같은 디렉토리들이 존재
  - `airflow-webserver`
  - `airflow.cfg`
  - `airlfow.db`
  - `logs`
  - `webserver_config.py`
- 해당 디렉토리에서 DAG를 담기위한 디렉토리를 추가
~~~shell
mkdir dags  # dags directory 
~~~
- 해당 디렉토리 안에 pipeline 에 필요한 skeleton 생성
- `dag_id` 는 UI 에 보일 dag id 입력
- `schedule_interval` 은 해당 스케줄러 주기를 입력  
  - `@daily` 는 매일 돌아감  
- `default_args` 는 스케줄링에 필요한 default args 값 입력
  - `start_date` --> 시작 시간
- 해당 파일 정보가 airflow UI 에 적용되는데 약 30초 정도 걸림
~~~python
from datetime import datetime
from airflow import DAG

default_args = {
    'start_date': datetime(2021, 1, 24)
}

with DAG(dag_id='nft-pipeline',
         schedule_interval='@daily',
         default_args=default_args,
         tags=['nft'],
         catchup=False) as dag:
    pass
~~~


### Operators
- BashOperator, PythonOperator, Email Operator 등이 있음
- Actopn Operator 는 액션을 실행함
- Trasfer Operator 는 데이터를 옮길때 사용
- Sensors 는 조건이 맞을때까지 기다렸다가 조건이 충족되면 실행됨

#### 외부 Provider
- 외부 provider는 airflow 와 다른 프레임워크와 연결할 수 있는 브릿지를 뜻함
- 매우 다양한 provider 들이 있을 수 있는데(ex) MySQL, apache spark..), 결국 action, transfer, sensor 세 가지로 압축될 수 있음

### Table 만들기
- 데이터를 담을 Table을 만드는 예제 수행
- sqlLite engine 을 사용하여, 테이블 만드는 예제
~~~python
from datetime import datetime
from airflow import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator

default_args = {
    'start_date': datetime(2021, 1, 23)
}

with DAG(dag_id='nft-pipeline',
         schedule_interval='@daily',
         default_args=default_args,
         tags=['nft'],
         catchup=False) as dag:

    creating_table = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        # create table 수행 시, 기존에 생성된 table 이 있는 경우는 생성 문을 날리면
        # 오류가 발생하므로, 방지를 위해 IF NOT EXISTS 추가
        sql="""
            CREATE TABLE IF NOT EXISTS nfts (
                token_id TEXT PRIMARY KEY, 
                name TEXT NOT NULL, 
                image_url TEXT NOT NULL
            )
        """
    )
~~~

#### connection id 생성 방법
- connection id 는 UI 상에서 만들 수 있는데, `Admin` 탭 -> `Connection` 
- 왼쪽 상단의 `+` 버튼을 눌러 새로운 connection id 생성
- 다음과 같이 입력
  - `Connection id` : db_sqlite 
  - `Connection Type` : Sqllite 선택. 뜨지 않는 경우 pip install 을 통해 설치 필요
  - `Host` : /Users/heojaehun/airflow/airflow.db
  - 나머지 것들은 공란으로 둬도 됨

#### airflow task test 방법
~~~shell
airflow tasks test nft-pipeline creating_table 2021-01-23

# 실제 sqlite.db 에서 확인
cd $HOME
cd airflow
sqlite3 airflow.db

.table  # nfts 확인
~~~

### Sensor로 API 확인하기
- Sensor Operator 를 사용해서 외부 API가 존재하는지 확인하는 방법 구현
- HTTP sensor를 이용

#### API Conection id 생성 방법
- connection id 는 UI 상에서 만들 수 있는데, `Admin` 탭 -> `Connection` 
- 왼쪽 상단의 `+` 버튼을 눌러 새로운 connection id 생성
- 다음과 같이 입력
  - `Connection id` : opensea_api
  - `Connection Type` : HTTP
  - `Host` : https://api.opensea.io/

#### airflow task test 
~~~shell 
airflow tasks test nft-pipeline is_api_available 2021-01-23
~~~

### HttpOperator로 데이터 불러오기
~~~python
extract_nft = SimpleHttpOperator(
        task_id='extract_nft',
        http_conn_id='opensea_api',
        endpoint='api/v1/assets?collection=doodles-official&offset=0&limit=1',
        method='GET',
        response_filter=lambda res: json.loads(res.text),  # endpoint 로 받는 데이터를 어떻게 처리할 것인지
        log_response=True
    )
~~~

### PythonOperator로 데이터 처리하기
- `airflow.operators.python` 의 `PythonOperator` 를 사용
- airflow 내장 라이브러리이기 때문에 providers 가 없음
- `python_callable` 에 원하는 파이썬 전처리 함수를 입력(`processing_nft`)
- `processing_nft` 함수에 입력받을 데이터를 선언하기 위하여 `ti.xcom_pull(task_ids=[''])` 를 입력받음
~~~python
from airflow.operators.python import PythonOperator 

def processing_nft(ti):  # task instance
    assets = ti.xcom_pull(task_ids=['extract_nft'])
    if not len(assets):
        raise ValueError("assets empty")
    nft = assets[0]["assets"][0]

    processed_nft = pd.json_normalize({
        'token_id': nft['token_id'],
        'name': nft['name'],
        'image_url': nft['image_url']
    })

    processed_nft.to_csv('/tmp/processed_nft.csv', index=False, header=False)

process_nft = PythonOperator(
        task_id='process_nft',
        python_callable= processing_nft
    )
~~~
~~~shell
airflow tasks test nft-pipeline process_nft 2021-01-23
~~~


### BashOperator로 데이터 저장하기
- `bash_command` 는 terminal 에서 bash shell 에 입력하는 명령어를 사용할 수 있음
~~~python
store_nft = BashOperator(
        task_id='store_nft',
        bash_command='echo -e ".separator ","\n import /tmp/precessed_nft.csv nfts" | sqlite3 /Users/heojaehun/airflow/airflow.db'
    )
~~~
~~~shell
airflow tasks test nft-pipeline store_nft 2021-01-23
~~~

### task 간 의존성 만들기
- 지금까지 작업한 task 별 의존성을 만들어 주어야 함
~~~python
creating_table >> is_api_available >> extract_nft >> process_nft >> store_nft
~~~
- 해당 정보를 airflow UI 에서 확인이 가능
- ** 주의. error 가 날 수 있는데, sqlite table(nfts) 에 key가 중복될 수 있기 때문

### Backfill
- 매일 주기적으로 돌아가는 파이프라인을 멈췄다가 몇일 뒤 실행시키면 어떻게 될까? 
- 다음과 같은 일별 파이프라인이 있다고 가정해보자
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_24.png)

- 예를 들어 1월 1일에는 정상적으로 작동했으며, 1/2일 장애 발생 1/3일 복구 작업, 1/4일에 재기동 되었다고 가정해보자
- 그렇다면 1/4일날 돌린 배치는 언제 배치일까? 이는 1/2일 배치일 수도있고, 1/4일 파이프라인일 수 있음
- 이를 컨트롤 하는 방법에 대해서 알아보자
- 이를 컨트롤 하지 못하면 원하지 않은 DagRun이 돌아감
- `catchup` 이라는 Field 로 작업이 가능함. 해당 값을 `True`로 설정 해두게 되면 1/2 ~ 1/4까지 차례로 실행됨


### 용어 정리
- skeleton
  - 더미 프로젝트
  - 고급 프로그램 구조 기반의 컴퓨터 프로그래밍 스타일의 하나
  - dummy code 라 부름. 수도 코드와 유사하지만 구문 분석, 컴파일, 코드 테스트를 허용
  - 탬플릿 메소드 디자인 패턴에서 이용됨

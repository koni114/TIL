# chapter08 - 커스텀 컴포넌트 빌드
- 어떤 경우에는 Ariflow가 지원하지 않는 시스템에서 태스크를 실행해야 하는 경우도 있음
- 또한 어떤 태스크 중에서는 `PythonOperator` 를 사용하여 구현할 수는 있지만 수많은 단순 반복적인 코드가 필요하여, 여러 DAG에서 재사용하기 힘든 때도 있음
- 이러한 경우를 대비하여 <b>Airflow에서는 커스텀 오퍼레이션을 직접 쉽게 구현해 생성할 수 있음</b>
- 이 장에서는 사용자가 자신만의 오퍼레이터를 빌드하고 DAG에서 이를 사용하는 방법을 설명해보고, 이 커스텀 컴포넌트를 파이썬 패키지로 패키징하여 여러 환경에 설치하거나 재사용할 때 편리하게 하는 방법을 살펴보자

## PythonOperator로 작업하기
- 커스텀 컴포넌트를 빌드하기 전에 PythonOperator를 사용하는 방법을 다시 한 번 살펴보자
- 영화 평점 데이터는 API를 통해 제공되며, 특정 기간의 영화 평점이 제공됨
- 데이터를 일별로 가져오는 프로세스를 구축. 인기 순서로 영화 랭킹을 생성하도록 하는 예제를 구축해보자

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_33.png)


### 영화 평점 API 시뮬레이션하기
- 25M MovieLens 데이터 세트(https://grouplens.org/datasets/movielens)를 사용할 예정
- 데이터세트는 62,000개의 영화에 대해 162,000 명의 유저가 평가한 2천5백만 개의 평점 데이터이며 무료로 사용됨  
  flat file(csv 등과 같이, 같은 형식의 레코드들의 모임)로 제공
- 여러 앤드포인트(endpoint)에 데이터를 부분별로 제공하는 REST API를 Flask 를 사용하여 구현
- API의 서빙을 위해 docker-compose file을 제공(총 2개)
  - REST API 를 위한 것
  - Airflow 실행을 위한 것 
- 컨테이너 구동 후 localhost의 5000번 포트로 영화 평점 API에 접근 가능(`http://localhost:5000`)
- `http://localhost:5000/ratings` 호출 후 인증 화면에 아이디/패스워드(airflow/airflow) 입력
- 자격 인증정보(credentials)를 입력하면, 영화 평점의 초기 리스트를 가져옴  
  평점 데이터는 JSON 포맷으로 되어 있음
- 쿼리한 결과를 페이지별로 처리할 때 API의 파라미터 중 `offset` 을 사용할 수 있음  
  예를 들어 다음 100개의 레코드를 가져올 때 offset 파라미터 값을 100으로 추가하여 사용  
  `http://localhost:5000/ratings?offset=100`
- 쿼리에서 한 번에 가져오는 레코드 수를 늘리려면 `limit` 사용  
  `http://localhost:5000/ratings?limit=1000`
- 기본적으로 영화 평점 앤드포인트는 전체 평점 데이터를 반환하는데, 만약 특정 기간 동안의 평점 데이터를 가져오려면 `start_date`와  `end_date` 파라미터를 사용하여 주어진 시작/종료 날짜 사이의 평점 데이터를 가져올 수 있음  
`http://localhost:5000/ratings?start_date=2019-01-01&end_date=2019-01-02`
- 이러한 필터링 방식을 사용하면 전체 데이터 세트를 다 로드할 필요없이 증분(incremental) 방식으로 데이터 로드 가능

### API 에서 평점 데이터 가져오기
~~~python
# 01_python.py

import os
import requests

# os 환경 변수에서 API 의 설정 정보 수집
MOVIELENS_HOST = os.environ.get("MOVIELENS_HOST", "movielens")
MOVIELENS_SCHEMA = os.environ.get("MOVIELENS_SCHEMA", "http")
MOVIELENS_PORT = os.environ.get("MOVIELENS_PORT", "5000")

# 환경 변수에서 사용자 이름/ 비밀 번호 가져오기
MOVIELENS_USER = os.environ.get("MOVIELENS_USER", "airflow")
MOVIELENS_PASSWORD = os.environ.get("MOVIELENS_PASSWORD", "airflow")


def _get_session():
    """ Movielens API 를 위한 request session build"""

    session = requests.Session()
    session.auth = (MOVIELENS_USER, MOVIELENS_PASSWORD)

    schema = MOVIELENS_SCHEMA
    host = MOVIELENS_HOST
    port = MOVIELENS_PORT

    base_url = f"{schema}://{host}:{port}"
    return session, base_url


def _get_with_pagination(session, url, params, batch_size=100):
    """
        API 결과의 페이지 처리 함수
        API 결과를 검사, 결과 레코드의 끝까지 도달할 때까지 페이지를 반복적으로 요청하는 코드

    """
    offset = 0
    total = None
    while total is None or offset < total:
        response = session.get(
            url,
            params={
                **params,
                **{"offset": offset, "limit": batch_size}
            }
        )  # 신규 페이지를 가져올 때 주어진 오프셋에서 시작.
        response.raise_for_status()
        response_json = response.json()  # 결과 상태를 확인하고, 결과를 JSON 을 파싱(parse) 함

        yield from response_json["result"]

        offset += batch_size
        total = response_json["total"]


def _get_ratings(start_date, end_date, batch_size=100):
    session, base_url = _get_session()  # API 요청 세션(requests session, 인증 정보 포함)과 기본 URL을 가져오기

    # 레코드들의 집합을 명확하게 가져오기 위해 페이지 처리 함수를 만들어 사용
    yield from _get_with_pagination(
        session=session,
        url=base_url + "/ratings",  # 평점 API 의 앤드포인트에 대한 URL 생성
        params={"start_date": start_date, "end_date": end_date}, # 시작, 종료 날짜 지정
        batch_size=batch_size,  # 한 페이지의 레코드 개수를 제한하기 위한 batch_size 지정
    )
~~~

### 실제 DAG 구축하기
- `_get_ratings` 함수를 `PythonOperator` 로 호출함으로써 스케줄 간격마다 평점 데이터를 가져오기
- 평점 데이터를 JSON 출력 파일로 덤프 할 수 있는데, 이때 날짜별로 파티션함
- 이렇게 하면 데이터의 재수집이 필요한 경우, 필요한 부분만 가져올 수 있음
- 이를 위해 날짜를 입력받고, 이 기간 동안의 평점 데이터를 만들어 출력하는 작은 래퍼 함수를 만들어보기
~~~python
def _fetch_ratings(templates_dict, batch_size=1000, **_):
    logger = logging.getLogger(__name__)

    start_date = templates_dict["start_date"]
    end_date = templates_dict["end_date"]
    output_path = templates_dict["output_path"]

    logging.info(f"Fetching ratings for {start_date} to {end_date}")
    ratings = list(
        _get_ratings(
            start_date=start_date,
            end_date=end_date,
            batch_size=batch_size
        )
    )

    logger.info(f"Fetched {len(ratings)} ratings")
    logger.info(f"Writing ratings to {output_path}")

    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w") as file_:
        json.dump(ratings, fp=file_)


_fetch_ratings = PythonOperator(
    task_id="fetch_ratings",
    python_callable=_fetch_ratings,
    templates_dict={
        "start_date": "{{ds}}",
        "end_date": "{{next_ds}}",
        "output_path": "/data/python/ratings/{{ds}}.json",
    }
)
~~~
- 평점 데이터를 가져온 후 영화의 랭킹을 만들기 위해 `rank_movies` 라는 단계를 추가하여 적용함
- 해당 단계에서는 `PythonOperator`에 `rank_movie_by_rating` 이라는 함수를 적용
~~~python
# dags/custom/ranking.py
def _fetch_ratings(templates_dict, batch_size=1000, **_):
    logger = logging.getLogger(__name__)

    start_date = templates_dict["start_date"]
    end_date = templates_dict["end_date"]
    output_path = templates_dict["output_path"]

    logging.info(f"Fetching ratings for {start_date} to {end_date}")
    ratings = list(
        _get_ratings(
            start_date=start_date,
            end_date=end_date,
            batch_size=batch_size
        )
    )

    logger.info(f"Fetched {len(ratings)} ratings")
    logger.info(f"Writing ratings to {output_path}")

    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w") as file_:
        json.dump(ratings, fp=file_)


fetch_ratings = PythonOperator(
    task_id="fetch_ratings",
    python_callable=_fetch_ratings,
    templates_dict={
        "start_date": "{{ds}}",
        "end_date": "{{next_ds}}",
        "output_path": "/data/python/ratings/{{ds}}.json",
    },
)


def _rank_movies(templates_dict, min_ratings=2, **_):
    input_path = templates_dict["input_path"]
    output_path = templates_dict["output_path"]

    ratings = pd.read_json(input_path)
    ranking = rank_movies_by_rating(ratings, min_ratings=min_ratings)

    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    ranking.to_csv(output_path, index=True)


rank_movies = PythonOperator(
    task_id="rank_movies",
    python_callable=_rank_movies,
    templates_dict={
        "input_path": "/data/python/ratings/{{ds}}.json",
        "output_path": "/data/python/ratings/{{ds}}.csv",
    },
)

fetch_ratings >> rank_movies
~~~

## 커스텀 훅 빌드하기
- 앞서 구현한 '데이터 가져오기 -> 랭킹 만들기' 는 API 연동과 관련이 있으며, API 주소 or 인증 정보를 가져오기, 세션 생성 및 페이지 처리와 같은 API 결과 세부 처리 기능을 직접 코드로 구현함
- 위의 API 연동과 같이 복잡한 작업의 처리 방법 중 하나는 <b>코드를 캡슐화하고 재활용 가능한 Airflow 훅으로 만드는 것</b>
- 이 작업으로 모든 API 전용 코드를 한 곳에 보관하고, DAG의 여러 부분에서는 이 훅을 간단하게 사용 가능
- 그러면 유사한 용도로 영화 평점 데이터를 가져오려고 할 때, API 연동에 대한 노력을 줄여줄 수 있음
~~~python
# MovielensHook 을 사용하여 평점 가져오기
hook = MovielensHook(conn_id="movielens")           # 훅 생성
ratings = hook.get_ratings(start_date, end_date)    # 생성된 훅을 사용하여 특정 작업 수행
hook.close()                                        # 훅을 닫고(close), 사용된 리소스 해제
~~~
- 훅을 사용하면 <b>Airflow의 데이터베이스와 UI를 통해 자격 증명(credentials)과 연결된 관리 기능을 사용할 수 있음</b>  
  API의 자격 증명 정보를 DAG에 수동으로 넣지 않아도 됨

### 커스텀 훅 설계하기
- <b>Airflow에서 모든 훅은 추상 클래스(abstract class)인 BaseHook 클래스의 서브클래스로 생성</b>
~~~python
from airflow.hooks.base_hook import BaseHook

class MovielensHook(BaseHook):
    ...
~~~
- 훅을 구현하기 위해서는 훅 연결(필요한 경우)과 훅에 필요한 다른 추가적인 인수를 지정하는 `__init__` 메서드를 정의해야 함
- 이 경우에서는 훅이 특정 연결에서 연결 세부 정보를 가져와야 하지만, 다른 추가 인수는 필요하지 않음
~~~python

from airflow.hooks.base import BaseHook


class MovielensHook(BaseHook):
    def __init__(self, conn_id):
        super().__init__()
        self.conn_id = conn_id
~~~
- 대부분의 `Airflow` 혹은 `get_conn` 메서드를 정의하는데, 이 메서드는 외부 시스템과의 연결 설정을 책임짐
- 여기에서는 앞에서 정의한 `_get_session` 메서드의 대부분을 재사용함
- `get_conn` 개념을 구현하면 다음과 같음
~~~python
class MovielensHook(BaseHook):
    ...

    def get_conn(self):
        session = requests.Session()
        session.auth = (MOVIELENS_USER, MOVIELENS_PASSWORD)

        schema = MOVIELENS_SCHEMA
        host = MOVIELENS_HOST
        port = MOVIELENS_PORT

        base_url = f"{schema}://{host}:{port}"
        return session, base_url
~~~
- 자격 증명 정보를 보다 안전하고 쉽게 관리하려면, <b>Airflow 자격 인증 저장소에서 가져오는 것이 더 좋음</b>
- 이를 위해 Airflow 메타스토어에 연결 정보를 먼저 추가해야 함.  
  Airflow 웹 UI의 `Admin` > `Connection` 항목에서 `Create to add a new connection` 을 클릭하여 작업 수행 가능

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_34.png)

- Add Connection 화면에 영화 평점 API의 연결 세부 정보를 넣어야 함
  - Conn id : `movielens`
  - Conn Type : HTTP
  - Host : 앞에서 사용한 docker-compose 설정에 있는 영화 평점 API의 HOST 입력. `movielens`
  - Scheme : http
  - Login/Password: airflow/airflow 
  - Port: 5000
- 연결 생성 후 메타스토어에서 연결 세부 정보를 가져오기 위하여 `get_conn` 메소드를 수정해야함
- `BaseHook` 클래스에서 get_connection 이라는 편리한 메서드를 제공함
- 이 메서드는 메타스토어에서 커넥션 ID에 대한 연결 세부 정보를 가져옴
~~~python
config = self.get_connection(self._conn_id)
~~~
- config 객체를 사용하여 host/port, user/password 를 가져올 수 있음
~~~python
schema = config.schema or self.DEFAULT_SCHEMA
host = config.host or self.DEFAULT_HOST
port = config.port or self.DEFAULT_PORT

base_url = f"{schema}://{host}:{port}/"
~~~
- 메타스토어에서 가져온 정보로 API의 기본 URL을 가져왔으므로, 이제 세션에 인증정보를 설정해야 하는 일만 남음
~~~python
if config.login:
    session.auth = (config.login, config.password)
~~~
- 위의 사항을 `get_conn` 에 다음과 같이 적용하여 구현함
~~~python
# hooks.py
class MovielensHook(BaseHook):
    DEFAULT_HOST = "movielens"
    DEFAULT_SCHEMA = "http"
    DEFAULT_PORT = 5000

    def __init__(self, conn_id):
        super().__init__()
        self._conn_id = conn_id

    def get_conn(self):
        config = self.get_connection(self._conn_id)
        schema = config.schema or self.DEFAULT_SCHEMA
        host = config.host or self.DEFAULT_HOST
        port = config.port or self.DEFAULT_PORT

        base_url = f"{schema}://{host}:{port}"
        session = requests.Session()

        if config.login:
            session.auth = (config.login, config.password)

        return session, base_url
~~~
- 이 구현 방법은 단점은 `get_conn` 함수를 호출할 때마다 Airflow 메타스토어에 작업 요청한다는 것임
- 왜냐하면 `get_conn` 함수가 데이터베이스에서 자격 증명 정보를 가져오기 때문
- 이 단점을 해결하기 위해 인스턴스에 `session` 과 `base_url` 을 `protected` 변수에 캐싱(caching) 할 수 있음
~~~python
class MovielensHook(BaseHook):
    ...

    def __init__(self, conn_id):
        ...
        self._session = None
        self._base_url = None

    def get_conn(self):

        if self._session is None:
            config = self.get_connection(self._conn_id)
            schema = config.schema or self.DEFAULT_SCHEMA
            host = config.host or self.DEFAULT_HOST
            port = config.port or self.DEFAULT_PORT

            self._base_url = f"{schema}://{host}:{port}"
            self._session = requests.Session()

            if config.login:
                self._session.auth = (config.login, config.password)

        return self._session, self._base_url
~~~
- `get_conn` 함수가 처음 호출될 때 `self.session`이 None 이므로, 메타스토어에 연결 세부 사항을 가져와 기본 URL과 세션을 인스턴스 내부에 저장함
- 이 객체들을 각각 인스턴스 변수 `_session` 과 `_base_url`에 저장하고 캐싱하여 나중에 다시 호출될 때 재사용할 수 있음
- `get_conn`의 구현을 완료했으니, 이제부터 영화 평점 API에 대해 인증된 커넥션을 만들 수 있음  
  이 메서드를 이용하여 영화 평점 API 연동에 필요한 메서드를 빌드하고 훅에 넣을 수 있게 됨
- 영화 평점 데이터를 가져오기 위해 이전에 구현한 코드를 재사용함
~~~python
import os

import requests
from airflow.hooks.base import BaseHook


class MovielensHook(BaseHook):
    DEFAULT_HOST = "movielens"
    DEFAULT_SCHEMA = "http"
    DEFAULT_PORT = 5000

    def __init__(self, conn_id):
        super().__init__()
        self._conn_id = conn_id

        self._session = None
        self._base_url = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_conn(self):

        if self._session is None:
            config = self.get_connection(self._conn_id)
            schema = config.schema or self.DEFAULT_SCHEMA
            host = config.host or self.DEFAULT_HOST
            port = config.port or self.DEFAULT_PORT

            self._base_url = f"{schema}://{host}:{port}"
            self._session = requests.Session()

            if config.login:
                self._session.auth = (config.login, config.password)

        return self._session, self._base_url

    def close(self):
        if self._session:
            self._session.close()

        self._session = None
        self._base_url = None

    def get_ratings(self, start_date=None, end_date=None, batch_size=100):

        yield from self._get_with_pagination(
            endpoint="/ratings",
            params={"start_date": start_date, "end_date": end_date}, # 시작, 종료 날짜 지정
            batch_size=batch_size,  # 한 페이지의 레코드 개수를 제한하기 위한 batch_size 지정
        )

    def _get_with_pagination(self, endpoint, params, batch_size=100):
        session, base_url = self.get_conn()
        url = base_url + endpoint

        offset = 0
        total = None
        while total is None or offset < total:
            response = session.get(
                url,
                params={
                    **params,
                    **{"offset": offset, "limit": batch_size}
                }
            )  # 신규 페이지를 가져올 때 주어진 오프셋에서 시작.
            response.raise_for_status()
            response_json = response.json()  # 결과 상태를 확인하고, 결과를 JSON 을 파싱(parse) 함

            yield from response_json["result"]

            offset += batch_size
            total = response_json["total"]
~~~
- MovieLens API 에 대한 커넥션을 처리하는 Airflow 기본 훅을 완성함. 그리고 추가적으로 메소드를 구현하여 간단하게 기능을 추가할 수 있음
- 새로 만든 훅의 장점은 여러 DAG에서 사용하기 쉽도록 MovieLens API 연동에 필요한 로직을 단일 클래스에 캡슐화하여 제공한다는 것

### MovielensHook 로 DAG 빌드하기
- 위에서 만든 영화 평점 데이터 수집 훅을 사용하여 DAG을 빌드해보자
- 먼저 이 훅 클래스를 DAG에서 불러올 수 있도록 어딘가에 저장해야 하는데, 한 가지 방법은 DAG 폴더와 같은 디렉터리 안에 패키지를 생성하고, 이 패키지 안에 있는 `hook.py` 라는 모듈에 훅을 저장하는 것
```
├── dags
    ├── custom   # custom 이란 이름의 패키지
        ├── __init__.py
        ├── hooks.py    # 커스텀 훅 코드를 담고 있는 모듈
    ├── 01_python.py
    ├── 02_hook.py
├── docker-compose.yml
├── ...
```
- 커스텀 훅 코드를 포함하는 새로운 커스텀 패키지를 생성 후에 해당 패키지에 훅을 불러올 수 있음
~~~python
from custom.hooks import MovielensHook
~~~
- 훅을 호출한 후에 평점 데이터를 가져오는 일은 다음과 같이 수행하면 됨
~~~python
hook = MovielensHook(conn_id=conn_id)
ratings = hook.get_ratings(
    start_date=start_date,
    end_date=end_date,
    batch_size=batch_size
)
~~~
- DAG에 훅을 사용하기 위해서는 훅 호출 코드를 `PythonOperator`에 래핑해야 함
- 래핑하는 코드는 DAG 실행에 필요한 시작/종료 날짜를 만들어 입력하고, 영화 평점 데이터를 적절한 출력 파일로 저장하는 코드
- 아래 코드는 초기 DAG에서 정의했던 `_fetch_ratings` 함수를 변경해서 사용
- 변경해야 하는 부분은 `_get_ratings`에 대한 호출 부분인데, 이 부분을 새로 만든 훅을 호출하도록 변경
~~~python
import datetime as dt
import logging
import json
import os

from airflow import DAG
from airflow.operators.python import PythonOperator

from custom.hooks import MovielensHook


with DAG(
    dag_id="02_hook",
    description="Fetches ratings from the Movielens API using a custom hook.",
    start_date=dt.datetime(2019, 1, 1),
    end_date=dt.datetime(2019, 1, 10),
    schedule_interval="@daily",
) as dag:

    def _fetch_ratings(conn_id, templates_dict, batch_size=1000, **_):
        logger = logging.getLogger(__name__)

        start_date = templates_dict["start_date"]
        end_date = templates_dict["end_date"]
        output_path = templates_dict["output_path"]

        logger.info(f"Fetching ratings for {start_date} to {end_date}")
        hook = MovielensHook(conn_id=conn_id)
        ratings = list(
            hook.get_ratings(
                start_date=start_date, end_date=end_date, batch_size=batch_size
            )
        )
        logger.info(f"Fetched {len(ratings)} ratings")

        logger.info(f"Writing ratings to {output_path}")

        # Make sure output directory exists.
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w") as file_:
            json.dump(ratings, fp=file_)

    PythonOperator(
        task_id="fetch_ratings",
        python_callable=_fetch_ratings,
        op_kwargs={"conn_id": "movielens"},
        templates_dict={
            "start_date": "{{ds}}",
            "end_date": "{{next_ds}}",
            "output_path": "/data/custom_hook/{{ds}}.json",
        },
    )
~~~

## 커스텀 오퍼레이터 빌드하기
- `MovielensFetchRatingsOperator` 처럼 커스텀 오퍼레이터를 빌드하여, 영화 평점 데이터를 가져오는 전용 오퍼레이터를 클래스로 사용할 수 있음

### 커스텀 오퍼레이터 정의하기
- Airflow 의 모든 오퍼레이터는 <b>`BaseOperator` 클래스의 서브 클래스로 만들어야 함</b>
~~~python
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class MovielensFetchRatingsOperator(BaseOperator):
    @apply_defaults  # 기본 DAG 인수를 커스텀 오퍼레이터에게 전달하기 위한 데코레이터
    def __init__(self, conn_id, **kwargs):  # BaseOperator 에게 추가 인수를 전달
        super().__init__(self, **kwargs)
        self._conn_id = conn_id
        ...
~~~ 
- 커스텀 오퍼레이터에서만 사용되는 변수들을 `__init__` 에서 받아 사용할 수 있음  
  어떤 변수를 받는지는 개발자마다 다르긴 하지만, 일반적으로 원격 접속 오퍼레이터인 경우 connection 객체(conn_id)와 오퍼레이터 작업에 필요한 세부정보가 있음
- `BaseOperator` 에는 오퍼레이터의 일반적인 동작을 정의하는 제네릭(generic) 인수를 많이 포함하고 있음.  
  예를 들어 오퍼레이터가 생성한 태스크`task_id`)나, 스케줄에 영향을 미치는 `retries`, `retry_delay` 등이 있음
- 이러한 인수들을 나열해서 선언하지 않게 하도록 `**kwargs` 로 선언해서 사용
- 앞선 DAG를 선언하여 사용했을 때, 기본적인 인수들은 `default_args` 의 인수에 선언해서 사용했었음
~~~python
default_args = {
    "retries": 1,
    "retry_delay": timedelta(minute=5),
}

with DAG(
    ...
    default_dags=default_args
) as dag:
    MyCustomOperator(
        ...
    )
~~~
- 커스텀 오퍼레이터의 기본 인수들이 정상적으로 반영되었는지 확인하기 위해 `apply_defaults` 라는 데코레이터를 사용할 수 있는데, 이 데코레이터는 반드시 사용해야함
- 그렇지 않으면 이 커스텀 오퍼레이터에 대한 Airflow 동작이 의도치 않게 중단될 수 있음
- <b>커스텀 오퍼레이터가 실제로 작업하는 부분은 `execute` 메소드에 선언하여 사용</b>
- DAG 안에서 실행되는 오퍼레이터의 메인 메서드가 됨
~~~Python
class MovielensFetchRatingsOperator(BaseOperator):
    def __init__(self, conn_id, **kwargs):
        ...
    
    def execute(self, context):  # 커스텀 오퍼레이터를 실행할 때 호출되는 메서드
        ...
~~~
- execute 메서드에서 `context` 변수는 dict 객체로서 Airflow의 모든 context 변수를 담고 있음

### 평점 데이터를 가져오기 위한 오퍼레이터 빌드하기
- 우리가 만들 오퍼레이터는 이전에 만든 DAG의 `_fetch_ratings` 와 유사하며,  
  시작/종료 날짜 사이의 영화 평점 데이터를 MovieLens API에서 가져와 JSON 파일로 저장하는 오퍼레이터
- 먼저 오퍼레이터에 필요한 시작/종료날짜, API에 대한 컨넥션, 평점 데이터를 저장할 경로 등이 포함됨
- `execute` 메소드 구현
  - `MovielensHook` 함수를 통한 hook 생성
  - logger 사용을 `self.log` 속성을 사용(`BaseOperator` 내부) 
  - `get_ratings`가 실패하더라도 정상적으로 종료하기 위하여 몇가지 예외 처리를 추가함
~~~python
import json
import os

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from custom.hooks import MovielensHook


class MovielensFetchRatingsOperator(BaseOperator):

    @apply_defaults
    def __init__(
        self,
        conn_id,
        output_path,
        start_date,
        end_date,
        batch_size=1000,
        **kwargs,
    ):
        super(MovielensFetchRatingsOperator, self).__init__(**kwargs)

        self._conn_id = conn_id
        self._output_path = output_path
        self._start_date = start_date
        self._end_date = end_date
        self._batch_size = batch_size

    # pylint: disable=unused-argument,missing-docstring
    def execute(self, context):
        hook = MovielensHook(self._conn_id)

        try:
            self.log.info(
                f"Fetching ratings for {self._start_date} to {self._end_date}"
            )
            ratings = list(
                hook.get_ratings(
                    start_date=self._start_date,
                    end_date=self._end_date,
                    batch_size=self._batch_size,
                )
            )
            self.log.info(f"Fetched {len(ratings)} ratings")
        finally:
            # Make sure we always close our hook's session.
            hook.close()

        self.log.info(f"Writing ratings to {self._output_path}")

        # Make sure output directory exists.
        output_dir = os.path.dirname(self._output_path)
        os.makedirs(output_dir, exist_ok=True)

        # Write output as JSON.
        with open(self._output_path, "w") as file_:
            json.dump(ratings, fp=file_)
~~~
- 해당 오퍼레이터의 사용방법은 기존 오퍼레이터와 유사하게 오퍼레이터의 인스턴스를 만들고, 이를 DAG에 포함시키면 됨
~~~python
fetch_ratings = MovielensFetchRatingsOperator(
    task_id="fetch_ratings",
    conn_id=movielens,
    start_date="2020-01-01",
    end_date="2021-01-02",
    output_path="/data/2020-01-01.json"
)
~~~
- 위 구현의 단점은 시작 날짜와 종료 날짜를 미리 지정해야한다는 점이며, <b>탬플릿 형태(ex) `{{ds}}`)를 사용하려면 `template_field` 클래스 변수에 해당 변수명을 지정하여 Airflow에 알려주어야 함</b>
~~~python
class MovielensFetchRatingsOperator(BaseOperator):
    ...
    
    # 커스텀 오퍼레이터에서 탬플릿화할 인스턴스 변수들을 Airflow에게 알려줌 
    template_fields = ("_start_date", "_end_date", "_output_path")

    @apply_defaults
    def __init__(
        self,
        conn_id,
        output_path,
        start_date="{{ds}}",
        end_date="{{next_ds}}",
        batch_size=1000,
        **kwargs,
    ):
        super(MovielensFetchRatingsOperator, self).__init__(**kwargs)

        self._conn_id = conn_id
        self._output_path = output_path
        self._start_date = start_date
        self._end_date = end_date
        self._batch_size = batch_size
~~~
- 위의 `__init__` 메소드에서 `start_date` 와 `end_date` 처럼 jinja 탬플릿을 사용하면 Airflow는 `execute` 메서드를 호출하기 전에 이 값들을 탬플릿화함
- 그 결과 다음 리스트와 같이 탬플릿화된 인수를 사용하는 오퍼레이터를 사용가능
~~~python
from custom.operators import MovielensFetchRatingsOperator

fetch_ratings = MovielensFetchRatingsOperator(
    task_id="fetch_ratings",
    conn_id="movielens",
    start_date="{{ds}}",
    end_date="{{next_ds}}",
    output_path="/data/custom_operator/{{ds}}.json"
)
~~~

## 커스텀 센서 빌드하기
- 센서의 빌드는 오퍼레이터의 빌드와 매우 유사하며, `BaseOperator` 대신에 `BaseSensorOperator`를 상속받는 것만 다름
- `BaseSensorOperator`는 센서에 대한 기본 기능을 제공하며, 오퍼레이터의 `execute` 메서드 대신 <b>`poke` 메서드를 구현해야 함</b>
- `execute` 메서드와는 다르게 `poke` 메서드는 반환값이 bool값.(True/False)  
  False 인 경우 대기상태로 들어가며, True 가 되거나 Timeout 될때까지 지속됨
- Airflow에는 내장 센서가 많이 있지만, 특정 유형의 상태를 체크하는 별도의 센서가 필요할 수 있음
- 앞선 예제의 경우 DAG를 계속 실행하기 전에 주어진 날짜의 평점 데이터를 사용 가능한지 체크하는 센서가 필요할 수 있음
- 커스텀 센서인 `MovielensRatingsSensor`를 빌드하기 위해서는 먼저 커스텀 센서 클래스의 `__init__` 메서드를 정의해야 함
~~~python
class MovielensFetchRatingsSensor(BaseSensorOperator):

    template_fields = ("_start_date", "_end_date")

    @apply_defaults
    def __init__(self, conn_id, start_date="{{ds}}", end_date="{{next_ds}}", **kwargs):
        super().__init__(** kwargs)
        self._conn_id = conn_id
        self.start_date = start_date
        self.end_date = end_date
~~~
- 생성자를 만든 후에는 `poke` 메소드를 구현하기만 하면 됨
- 기존의 `MovielensHook`을 사용하여 next 함수를 실행시켰을 때, `StopIteration`이 발생하면 False, 아니면 True 를 반환하는 bool 함수를 선언
~~~python
def poke(self, context):
        hook = MovielensHook(self._conn_id)

        try:
            next(
                hook.get_ratings(
                    start_date=self._start_date, end_date=self._end_date, batch_size=1
                )
            )

            self.log.info(
                f"Found ratings for {self._start_date} to {self._end_date}, continuing!"
            )
            return True
        except StopIteration:
            self.log.info(
                f"Didn't find any ratings for {self._start_date} "
                f"to {self._end_date}, waiting..."
            )

            return False
        finally:

            hook.close()
~~~
이제 이 센서 클래스를 사용하여 DAG의 나머지를 계속 실행하기 전에, 새로운 평점 데이터가 해당 기간에 있는지를 체크하고 새로운 데이터가 들어올 때까지 대기하도록 할 수 있음
~~~python
import datetime as dt

from airflow import DAG

from custom.operators import MovielensFetchRatingsOperator
from custom.sensors import MovielensRatingsSensor

with DAG(
    dag_id="04_sensor",
    description="Fetches ratings from the Movielens API, with a custom sensor.",
    start_date=dt.datetime(2019, 1, 1),
    end_date=dt.datetime(2019, 1, 10),
    schedule_interval="@daily",
) as dag:
    wait_for_ratings = MovielensRatingsSensor(
        task_id="wait_for_ratings",
        conn_id="movielens",
        start_date="{{ds}}",
        end_date="{{next_ds}}",
    )

    fetch_ratings = MovielensFetchRatingsOperator(
        task_id="fetch_ratings",
        conn_id="movielens",
        start_date="{{ds}}",
        end_date="{{next_ds}}",
        output_path="/data/custom_sensor/{{ds}}.json",
    )

    wait_for_ratings >> fetch_ratings
~~~

## 컴포넌트 패키징하기
- 지금까지 DAG에 커스텀 컴포넌트를 DAG 디렉토리 내에 있는 서브 패키지까지 포함함
- 하지만 이 방식은 컴포넌트를 다른 프로젝트에 사용하거나 다른 사람들에게 공유할 경우, 컴포넌트 테스트의 경우는 바람직한 방법이 아님
- 컴포넌트를 배포하는 더 좋은 방법은 <b>파이썬 패키지에 코드를 넣는 것</b>  
  이 방법을 사용하면 기존의 다른 패키지와 비슷한 방법으로 작업할 수 있다는 장점이 있음
- 추가적으로 DAG과 별도로 소스코드를 유지함으로써, 커스텀 코드에 대한 CI/CD 프로세스를 구성할 수 있고 다른 사람과 이 코드를 더 쉽게 공유하고 협업할 수 있음

### 파이썬 패키지 부트스트랩 작업하기
- 파이썬 패키징은 여러가지 방법이 있지만, 여기서는 `setuptools` 를 사용하여 간단한 파이썬 패키지를 구현해보자
- 예제의 목적은 앞서 구현한 훅, 오퍼레이터, 센서 클래스를 포함하는 `airflow_movielens`라는 패키지를 생성하는 것
- 패키지 빌드를 위해 다음과 같이 구성
```
$ tree airflow-movielens
airflow-movielens
├── setup.py
└── src
    └── airflow_movielens
        └── __init__.py
        └── hooks.py
        └── operators.py
        └── sensors.py
```
- `src/airflow_movielens` 디렉터리 안에 `hooks.py`, `sensors.py`, `operators.py`를 생성하고 앞 절에서 구현한 훅, 센서, 오퍼레이터 클래스 소스를 각 파일에 복사해서 넣음
- `setup.py` 파일은 다음 리스트와 같은 모양으로 만듬
~~~python


#!/usr/bin/env python

import setuptools

requirements = ["apache-airflow", "requests"]

extra_requirements = {"dev": ["pytest"]}

setuptools.setup(
    name="airflow_movielens",
    version="0.1.0",
    description="Hooks, sensors and operators for the Movielens API.",
    author="Anonymous",
    author_email="anonymous@example.com",
    install_requires=requirements,
    extras_require=extra_requirements,
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/example-repo/airflow_movielens",
    license="MIT license",
)
~~~

### 패키지 설치하기
- 앞서 기본적인 패키지를 작성해 보았고, 패키지 `airflow-movielens`를 파이썬 환경에 설치해보자
- `pip` 명령어를 통해 파이썬 패키지 설치
~~~shell
$ python -m pip install ./airflow-movielens
~~~
- Airflow 환경에 패키지를 배포하는 작업은 Airflow 의 파이썬 환경에 패캐지를 설치하는 것보다 특별히 더 어렵지는 않음  
  <b>작업 환경에 따라 패키지와 종속 라이브러리가 Airflow가 사용하는 모든 환경(스케줄러, 웹서버, 워커의 환경)에 설치되어야 함</b>


## 용어 정리
- MVP(Minimum Viable Product)
  - 프로토타입보다는 조금 더 앞에서 사용하는 용어. 
- Polling(풀링)
  - 어플리케이션에서 엔드포인트에 이벤트가 발생했는지 주기적으로 확인하는 방법 
- Hook(훅)
  - 엔드포인트에서 발생한 이벤트가 우리의 어플리케이션에 수신되는 형태 
  - web hook은 서버에서 특정 이벤트가 발생했을 때, 클라이언트를 호출하는 방식을 말함.
- 
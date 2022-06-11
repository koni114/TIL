# chapter04 Airflow 콘텍스트를 사용하여 태스크 템플릿 작업하기
- 템플릿을 사용하여 런타임 시에 변수 할당하기
- PythonOperator 및 다른 오퍼레이터를 사용해 변수 탬플릿 작업하기
- 디버깅을 위해 템플릿 변수 할당하기
- 외부 시스템에서 태스크 수행하기

## Airflow로 처리할 데이터 검사하기
- 이번 장에서는 StockSence라는 감성 분석이 적용된 주식 시장 예측 도구를 사용하여 오퍼레이터의 몇 가지 구성 요소를 알아보자
- 이 예에서는 회사의 페이지 뷰 증가가 긍정적인 감성을 나타내고 회사의 주식이 증가할 가능성이 있다는 원칙을 적용하려 함

### 증분 데이터를 적재하는 방법 결정하기
- 위키미디어 재단은 2015년 이후의 모든 페이지 뷰를 기계가 읽을 수 있는 형식으로 제공하고 있음
- 페이지 뷰는 gzip 형식으로 다운로드할 수 있으며, 페이지당 시간별로 집계됨
- 각 시간당 덤프는 gzip으로 압축된 크기는 약 50MB이고, 압축을 푼 크기는 200 ~ 250MB 임
- 크고 작은 모든 데이터는 구조가 복잡할 수 있으며, <b>파이프라인을 구축하기 전 접근 방식에 대한 기술적 계획을 세우는 것</b>이 중요
- <b>데이터를 후애 처리 할 것인지, 데이터(예) 빈도, 크기, 형식, 소스 유형)을 어떻게 수신할 것인지, 데이터로 무엇을 구축할 것인지</b>물어보아야 함
- 매 시간 덤프 하나를 다운로드하고 데이터를 직접 검사해보자. 데이터 파이프라인을 개발하기 위해서는 데이터를 증분 방식으로 적재하는 방법과 데이터를 다루는 방법을 이해해야 함
- URL이 고정된 패턴을 따르며, 데이터를 일괄로 다운로드 시에 사용할 수 있음. 
- 실험과 데이터 검증을 위해 7월 7일 10:00 ~ 11:00 에 가장 일반적으로 사용되는 도메인 코드가 무엇인지 확인해 보자 
~~~shell
$ wget https://dumps.wikimedia.org/other/pageviews/2019/2019-07/pageviews-20190707-230000.gz
$ gunzip pageviews-20190707-230000.gz
$ head pageviews-20190707-230000

aa Wikipedia:Community_Portal 3 0
aa.d Main_Page 3 0
aa.d Special:CreateAccount 1 0
aa.m Main_Page 1 0
aa.m.d Main_Page 2 0
ab 1 1 0
ab 1187 1 0
ab 1203 1 0
ab 1264 1 0
ab 1278 1 0

# 1. 도메인 코드(aa, ab ..)
# 2. 페이지 제목
# 3. 조회수
# 4. 응답 크기(byte)
# 예를 들어, en.m American_Bobtail 6.0 은 특정 시간에 https://en.m.wikipedia.org/wiki/American_Bobtail(고양이 종)의 6개의 페이지 뷰를 나타냄
~~~
~~~shell
$ awk -F' ' '{print $1}' pageviews-20190707-230000 | sort | uniq -c | sort -nr | head

# uniq -c : 중복된 line 의 개수를 count
# sort -nr : numerically reverse sort : -nr
# head : 상위 10개 출력

# 결과
1147978 en.m
1129920 en
276589 es.m
257877 nl
207038 ja.m
190786 de.m
189849 fr.m
174806 es
164656 it.m
160232 de
~~~
- 상위 결과인 1147978 en.m, 1129920 en 을 보면 7월 7일 22:00 ~ 23:00 사이에 가장 많이 조회된 도메인이 'en' 및 'en.m' 임을 알 수 있음

## 태스크 콘텍스트와 Jinja 템플릿 작업
- 위의 모든 것들을 모아 위키피디아 페이지 뷰 수를 가져오는 DAG의 첫 번째 버전을 만들어보자
- 데이터 다운로드 -> 추출 -> 데이터 읽는 것으로 간단하게 만들어 볼 것임
- 최초 가설을 검증하기 위해 5개 회사(Amazon, Apple, Facebook, Google, Microsoft)를 선택
- 첫 번째 단계는 주기마다 압축 파일을 다운로드 하는 것. URL은 날짜와 시간을 동적 바인딩해서 만들 수 있음
~~~
https://dumps.wikimedia.org/other/pageviews/{year}/{year}-{month}/pageviews-{year}{month}{day}{hour}0000.gz
~~~

### 오퍼레이터의 인수 탬플릿 작업
- 먼저 BashOperator 를 사용하여 위키피디아 페이지 뷰를 다운로드하자
~~~python
# stock_sense_v01.py

import datetime as dt
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag=DAG(
    dag_id="stock_sense_01",
    start_date=dt.datetime(2019, 7, 7, 22, 0, 0),
    schedule_interval="@hourly",
)

get_data = BashOperator(
    task_id="get_data",
    bash_command=(
        "curl -o /data/wikipageviews.gz "
        "https://dumps.wikimedia.org/other/pageviews/"
        "{{ execution_date.year }}/"
        "{{ execution_date.year }}-"
        "{{ '{:02}'.format(execution_date.month) }}/"
        "pageviews-{{ execution_date.year }}"
        "{{ '{:02}'.format(execution_date.month) }}"
        "{{ '{:02}'.format(execution_date.day) }}"
        "{{ '{:02}'.format(execution_date.hour) }}0000.gz"
    ),
    dag=dag,
)
~~~
- 이중 중괄호는 Jinja 탬플릿 문자열을 나타내며, Jinja 탬플릿을 사용하면, 런타임 시점에 동적으로 변수를 할당하여 사용 가능
- Airflow 에는 태스크 콘텍스트에서 런타임시 사용할 수 있는 여러 변수가 있음. 이러한 변수 중 하나가 `execution_date`임
- Aiflow는 날짜 시간에 `Pendulum` 라이브러리를 사용하며, `execution_date` 는 이러한 Pendulum의 `datetime` 객체
- 네이티브 파이썬의 `datetime` 의 호환 객체이므로, 파이썬에 적용할 수 있는 모든 메서드를 Pendulum 에도 적용할 수 있음
~~~python
from datetime import datetime
import pendulum
print(datetime.now().year)
print(pendulum.now().year)
~~~
- 위키피디아 페이지 뷰 URL은 빈 앞자리를 0으로 채우는 월, 일, 시간 값이 필요하여, 패딩 문자열 형식을 적용
~~~python
{{ '{:02}'.format(execution_date.hour) }}
~~~
- <b>모든 오퍼레이터 인수가 탬플릿이 될 수 있는 것은 아님.</b> 모든 오퍼레이터는 탬플릿으로 만들 수 있는 속성의 허용 리스트를 유지함
- 이는 airflow documentation 에서 template fields 항목을 확인해보면 됨

### 템플릿에 무엇이 사용 가능한가?
- 템플릿화를 위해 사용할 수 있는 변수는 어떤 것들이 있을까? (ex) execution_date 같은 것들.. )
- 아래 코드로 `_print_context` 함수를 선언하여 `PythonOperator`를 실행하면 태스크 콘텍스트에서 사용 가능한 모든 변수가 출력됨
~~~python
import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator

dag=DAG(
    dag_id="chapter4_print_context",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
)


def _print_context(**kwargs):
    print(kwargs)


print_context = PythonOperator(
    task_id="print_context",
    python_callable=_print_context,
    dag=dag,
)
~~~

#### 모든 태스크 콘텍스트 변수
- `ds` : %Y-%m-%d 형식의 execution_date,    ex) "2019-01-01"
- `ds_nodash`: %Y%m%d 형식의 execution_date ex) "20190101"
- `execution_date`: 태스크 스케줄 간격의 시작 날짜/시간
- `Inlets`: task.inlets의 약어. 데이터 계보에 대한 입력 데이터 소스를 추적하는 기능
- `macros`: airflow.macros 모듈
- `next_ds`: %Y-%m-%d 형식의 다음 스케줄 간격
- `next_ds_nodash`: %Y%m%d 형식의 다음 스케줄 간격
- `next_execution_date`: 태스크의 다음 스케줄 간격의 시작 datetime(=현재 스케줄 간격의 끝)
- `outlets`: task.outlets 의 약어, 데이터 계보(lineage) 에 대한 출력 데이터 소스를 추적하는 기능
- `params`: 태스크 콘텍스트에 대한 사용자 제공 변수
- `prev_ds`: %Y-%m-%d 형식의 이전 스케줄 간격의 execution_date
- `prev_ds_nodash`: %Y%m%d 형식의 이전 스케줄 간격의 execution_date
- `prev_execution_date`: 태스크 이전 스케줄 간격의 시작 datetime 
- `prev_execution_date_success`: 동일한 태스크의 마지막으로 성공적으로 완료된 실행의 시작 datetime(과거에만 해당)
- `prev_start_date_success`: 동일한 태스크의 마지막으로 성공적으로 시작된 날짜와 시간(과거에만 해당)
- `run_id`: DagrRun의 run_id (일반적으로 접두사 + datetime 으로 구성된 키)
- `task`: 현재 오퍼레이터
- `task_instance`: 현재 TaskInstance 객체
- `task_instance_key_str`: 현재 TaskInstance의 고유 식별자({dag_id}__{task_id}__{ds_nodash})
- `templates_dict`: 태스크 콘텍스트에 대한 사용자 제공 변수
- `test_mode`: Airflow 가 테스트 모드에서 실행 중인지 여부
- `ti`: task_instance 와 동일한 현재 TaskInstance 객체
- `tomorrow_ds`: ds(실행 시간)에서 1일을 더함
- `tomorrow_ds_nodash`: ds_nodash(실행 시간)에서 1일을 더함
- `ts`: ISO8601 포맷에 따른 execution_date 
- `ts_nodash`: %Y%m%dT%H%M%S 형식의 execution_date 
- `ts_nodash_with_tz`: 시간 정보가 있는 ts_nodash
- `var`: Airflow 변수를 처리하기 위한 헬퍼 개체
- `yesterday_ds`: ds(실행시간)에서 1일을 뺌
- `yesterday_ds_nodash`: ds_nodash 1일을 뺌

### PythonOperator 템플릿
- PythonOperator 는 `python_callable` 인수를 사용
- 위의 BashOperator 를 사용하여 리스트 4.1에 표시된 대로 위키피디아 페이지 뷰를 다운로드 하는 코드를 PythonOperator 로 구현해 보겠음
~~~python
def _get_data(execution_date):
    year, month, day, hour, *_ = execution_date.timetuple()
    url=(
        "https://dumps.wikimedia.org/other/pageviews"
        f"{year}/{year}-{month:0>2}/"
        f"pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )
    output_path="/tmp/wikipageviews.gz"
    request.urlretrieve(url, output_path)


get_data=PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    dag=dag
)
~~~
- `PythonOperator`의 python_callable 인수에 callable 을 제공함. 즉 어떤 함수라도 실행 시 PythonOperator 는 호출 가능하도록 수행함
- 다른 모든 오퍼레이터상 문자열이 아니라 함수이기 때문에 함수 내의 코드를 자동으로 탬플릿화할 수는 없음
- 대신 <b>태스크 컨텍스트 변수를 제공</b>하기 때문에 이를 이용할 수 있음
- 파이썬은 함수에서 키워드 인수를 받을 수 있음. 여기에는 주로 제공되는 키워드 인수를 사전에 알지 못하는 경우, 또는 예상되는 키워드 인수를 모두 명시적으로 작성할 필요 없는 다양한 사용 사례가 있음
~~~python
def _print_context(** context):
    print(context)

print_context=PythonOperator(
    task_id="print_context",
    python_callable:_print_context,
    dag=dag,
)
~~~
- `context` 변수는 모든 `context` 변수의 집합이며, 현재 실행되는 태스크의 시작 및 종료 날짜시간 등을 받아 사용할 수 있음
~~~python
def _print_context(** context):
    start=context["execution_date"]
    end=context["next_execution_date"]
    print(f"Start: {start}, end: {end}")
~~~

### PythonOperator 변수 제공
- PythonOperator 는 함수(`python_callable`)에서 파라미터 인자를 지정해서 사용가능
- 예를 들어 `output_path`를 파라미터로 지정해 함수 내에서 사용가능
~~~python
def _get_data(output_path, execution_date):
    year, month, day, hour, *_ = execution_date.timetuple()
    url=(
        "https://dumps.wikimedia.org/other/pageviews"
        f"{year}/{year}-{month:0>2}/"
        f"pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )
    request.urlretrieve(url, output_path)
~~~
- `output_path`의 값은 두 가지 방법으로 제공 가능. 첫 번째는 `op_args` 인수를 사용하는 것
~~~python
get_data=PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    op_args=["/tmp/wikipageviews.gz"],  # op_args 제공
    dag=dag
)
~~~
- 오퍼레이터를 실행하면 op_args 에 제공된 리스트의 각 값이 호출 가능한 함수에 전달됨  
  (`_get_data("/tmp/wikipageviews.gz")`) 함수를 직접 호출하는 것과 동일한 결과 도출
- 두 번째 방법은 다음 리스트에 표시된 `op_kwargs` 인수를 사용하는 것
~~~python
get_data=PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    op_kwargs={"output_path": "/tmp/wikipageviews.gz"},  # op_kwargs 에 주어진 명령어가 호출 가능한 키워드 인수로 전달됨
    dag=dag
)
~~~

### 탬플릿의 인수 검사하기
- Airflow UI는 템플릿 인수 오류를 디버깅하는 데 유용함
- 작업을 실행한 후, 그래프 또는 트리보기에서 선택하고 'Rendered Template' 버튼을 클릭하여 탬플릿 인수 값을 검사할 수 있음
- Airflow CLI를 통해서 작업을 실행하지 않아도 datetime 에 대한 탬플릿 값을 확인할 수 있음  
  CLI를 사용하면 메타 스토어에 아무것도 등록되지 않으므로 간편하게 확인 가능
~~~shell
$ airflow tasks render [dag id] [task id] [desired execution date]
$ airflow tasks render stocksense get_data 2019-07-19T00:00:00
~~~

## 다른 시스템과 연결하기
- 다음의 두 오퍼레이터는 저장소에서 추출하고 압축을 푼 파일을 스캔한 후, 지정된 페이지 이름에 대한 페이지 뷰 카운트를 선택해 처리
- 그런 다음 결과가 로그에 출력됨
~~~python
extract_gz=BashOperator(
    task_id="extract_gz",
    bash_command="gunzip --force /data/wikipageviews.gz",
    dag=dag,
)


def _fetch_pageviews(page_names):
    result = dict.fromkeys(page_names, 0)
    with open(f"/data/wikipageviews", "r") as f:
        for line in f:
            domain_code, page_title, view_counts = line.split(" ")
            if domain_code == "en" and page_title in page_names:
                result[page_title] = view_counts

    print(result)


fetch_pageviews=PythonOperator(
    task_id="fetch_pageviews",
    python_callable=_fetch_pageviews,
    op_kwargs={"page_names": {
        "Google",
        "Amazon",
        "Apple",
        "Microsoft",
        "Facebook",
    }},
    dag=dag,
)
~~~
- 위의 결과를 자체 DB에 기록하여 SQL로 쿼리하려면 어떻게 해야할까?
- 시간별 페이지 뷰를 저장하기 위한 Postgres DB 가 있다고 가정하고, 데이터를 보관할 테이블에는 리스트 4.16 과 같이 3개의 열이 있음
~~~SQL
CREATE TABLE pageview_counts (
    pagename VARCHAR(50) NOT NULL,
    pageviewcount INT NOT NULL,
    datetime TIMESTAMP NOT NULL
)

-- INSERT QUERY
INSERT INTO pageview_counts VALUES ('Google', 333, '2019-07-17T00:00:00')
~~~
- PythonOperator 는 현재 결과를 출력하지만 DB에 직접 쓰지 않기 때문에 결과를 DB에 저장하려면 두 번째 작업이 필요함
- Airflow 는 태스크 간 데이터를 전달하는 방법으로 두 가지가 있음
  - Airflow metastore 를 사용하여 태스크 간 결과를 쓰고 읽음. <b>이를 XCom이라고 함</b>
  - 영구적인 위치(Disk or DB)에 태스크 결과를 기록
- Airflow는 XCom 이라는 기본 매커니즘을 제공하여 Airflow 메타스토어에서 pickle 객체를 저장하고 나중에 읽을 수 있음
- <b>크기가 작은 오브젝트일 때, XCom을 이용한 피클링이 적합함</b>. Airflow 의 메타스토어는 크기가 한정되어 있고 피클링된 객체는 메타 스토어의 블롭(blob)에 저장되기 때문에 일반적으로 문자열 몇 개와 같은 작은 데이터 전송 시에 적용하는 것이 좋음 
- 만약 Postgres 를 사용한다면 `PostgresOperator` 를 사용해 데이터를 입력하도록 함
- 먼저 프로젝트에서 `PostgresOperator` 클래스를 가져오기 위한 추가 패키지를 설치함
~~~shell
pip install apache-airflow-providers-postgres
~~~
- `PostgresOperator`는 사용자가 작성환 쿼리를 실행함. `PostgresOperator`는 CSV 데이터로부터 입력하는 기능을 지원하지 않으므로 먼저 SQL 쿼리를 임시 데이터로 작성함
~~~python
def _fetch_pageviews(page_names, execution_date, **_):
    result = dict.fromkeys(page_names, 0)  # 0 으로 모든 페이지 뷰에 대한 결과를 초기화함
    with open(f"/data/wikipageviews", "r") as f:
        for line in f:
            domain_code, page_title, view_counts = line.split(" ")
            if domain_code == "en" and page_title in page_names:
                result[page_title] = view_counts  # 페이지 뷰 저장

    with open(f"/tmp/postgres_query.sql", "w") as f:
        for page_name, page_view_count in result.items():
            f.write(
                "INSERT INTO pageview_counts VALUES ("
                f"'{page_name}', {page_view_count}, '{execution_date}'"
                ");\n"
            )

fetch_pageviews=PythonOperator(
    task_id="fetch_pageviews",
    python_callable=_fetch_pageviews,
    op_kwargs={"page_names": {
        "Google",
        "Amazon",
        "Apple",
        "Microsoft",
        "Facebook",
    }},
    dag=dag,
)
~~~
- 쿼리 생성 후 연결하는 마지막 작업을 수행
~~~python
dag=DAG(
    dag_id="stock_sense_01",
    start_date=dt.datetime(2019, 7, 7, 22, 0, 0),
    schedule_interval="@hourly",
    template_searchpath="/tmp"  # sql 파일 탐색 경로
)

write_to_postgres=PostgresOperator(
    task_id="write_to_postgres",
    postgres_conn_id="my_postgres",  # 연결에 사용할 인증 정보의 식별자
    sql="postgres_query.sql",        # SQL 쿼리 또는 쿼리를 포함하는 파일의 경로ㄴ
    dag=dag,
)
~~~
- PostgresOperator 는 Postgres DB 에 대해 쿼리를 실행하기 위해 두 개의 인수만 입력하면 됨
- DB에 대한 연결 설정 및 완료 후 연결 끊기 같은 복잡한 작업은 내부에서 처리됨
- CLI 를 이용해 Airflow 에 my_postgres 연결을 추가해보자
~~~sh
airflow connections add \
    --conn-type posgres \
    --conn-host localhost \
    --conn-login postgres \
    --conn-passwords mysecretpassword \
    my_postgres  # 연결 식별자
~~~
- 그러면 UI에 연결이 표시됨. Admin > Connections 로 이동하여 Airflow 에 저장된 모든 연결을 확인
- 여러 DAG 가 실행이 완료되면 Postgres 데이터베이스에는 다음과 같은 몇 가지 카운트 기록이 저장됨
- .sql 파일은 `/tmp` 에 저장했기 때문에 Jinja가 해당 파일을 찾을 수 없음. Jinja가 검색할 경로를 추가하기 위해 DAG에서 `template_searchpath` 인수를 설정하면 Jinja는 기본 경로와 추가된 경로를 함께 검색함
- 다양한 외부 시스템과 연계하기 위해서는 여러 의존성 패키지를 설치해야 하는데, 이는 대부분의 오케스트레이션 시스템의 특성 중 하나
- `PostgresOperator`를 실행하면 여러 가지 작업이 수행됨. `PostgresOperator`는 Postgres와 통신하기 위해 훅(hook)이라고 불리는 것을 인스턴스화 함. 인스턴스화 된 훅은 연결 생성, 쿼리 전송, 연결에 대한 종료 작업을 처리함
- 오퍼레이터는 사용자의 요청을 훅으로 전달하는 작업만 담당
- 이와 같은 파이프라인을 구축할 때, 훅은 오퍼레이터 내부에서 동작하기 때문에 신경 쓸 필요가 없음

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_09.png)

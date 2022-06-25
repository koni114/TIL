# chapter06 워크플로 트리거
- 특정 조건을 센서에 만족하도록 대기하기
- 서로 다른 DAG의 태스크간 의존성 실행하기
- CLI 및 REST API를 통해 워크플로 실행하기
- 지금까지 시간 간격을 기준으로 Airflow의 워크플로를 예약하는 방법에 대해서 살펴보았는데, 예를들어 `@daily`, timedelta 객체, cron 문자열로 지정하는 방법에 대해서 알아봄
- 이번 챕터에서는 특정 태스크를 수행 후에 워크플로를 트리거하는 케이스를 알아보자  
  예를 들어, 공유 드라이브에 파일이 업로드되거나 개발자가 코드를 리포지터리로 푸시하거나, Hive table에 파티션이 있는 경우에 해당됨

## 센서를 사용한 폴링 조건
- 워크플로를 시작하는 일반적인 사례는 새로운 데이터가 도착하는 경우임
- 다음의 사례를 살펴보자
  - 인기있는 모바일 쿠폰 앱을 개발하고 있음
  - 프로모션을 쿠폰 앱에 매일 전시하기 위해 모든 슈퍼마켓 브랜드와 접촉하고 있음 
  - 대부분의 프로모션 프로세스가 수작업으로 되어 있어, 슈퍼마켓은 다양한 요소를 분석하고 정확한 프로모션을 진행하기 위해 가격 분석가를 고용하고 있음
  - 일부 프로모션만 몇 주 전에 미리 계획하고, 일부는 즉흥적인 일일 반짝 세일임
  - 가격 분석가는 경쟁사를 주위 깊게 리서치한 후 밤늦게 프로모션을 집행함. 때문에 일일 프로모션 데이터는 종종 비정규적인 시간에 도착함
  - 데이터는 하루 중 언제든지 도착할 수 있지만, 다음날 16:00 ~ 02:00 사이에 공유 저장소에 들어오는 것을 확인함
- 위의 사례를 위한 초기 로직은 다음과 같음
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_17.png)

- 슈퍼마켓 1~4 에서 제공한 데이터를 raw storage에 복사하며 항상 재현 가능함(`copy_to_raw_supermarket_1~4`)
- 앱에서 데이터를 읽을 수 있도록 raw 데이터를 변환하고 저장함(`process supermarket_1~4`)
- 추가적인 분석을 위해 프로모션에 대한 다양한 지표를 계산 및 집계(`create_metrics`) 
- 슈퍼마켓의 데이터가 다양한 시간에 도착하기 때문에 이 워크플로의 타임라인은 다음과 같음

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_18.png)

- 위의 워크플로는 2:00까지 데이터가 전달되므로, 2:00 에 워크플로를 시작하는 DAG을 구성했지만, 이는 대기 시간이 많이 소요됨
- 이 문제를 해결하기 위해 <b>Airflow 오퍼레이터의 특수 타입(서브 클래스)인 센서(sensor)의 도움을 받을 수 있음</b>  
  센서는 특정 조건이 true 인지 지속적으로 확인하고 true 라면 성공함
- 만약 false 인 경우 센서는 상태가 true 가 될 때까지 또는 타임아웃이 될 때까지 게속 확인함
~~~python
from airflow.sensors.filesystem import FileSensor

wait_for_supermarket_1 = FileSensor(
    task_id="wait_for_supermarket_1",
    filepath="/data/supermarket1/data.csv",
)
~~~
- 위의 `FileSensor`는 `/data/supermarket1/data.csv` 파일이 존재하는지 확인하고 파일이 있으면 true를 반환하고, 그렇지 않으면 false 를 반환한 후 해당 센서는 지정된 시간(기본값은 60초)동안 대기했다가 다시 시도함
- 오퍼레이터(센서 또한 오퍼레이터임)와 DAG는 모두 타임아웃의 설정이 가능하며, 센서 오퍼레이터는 제한 시간에 도달할 때까지 상태를 확인하며 대기함
- 태스크 로그에서 센서의 출력 내용을 확인할 수 있음

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_19.png)
- 여기서 대략 1분에 한 번씩(`poke_interval` 인수로 설정) 센서는 주어진 파일이 있는지 포크(poke)함. `Poking`은 센서를 실행하고 센서 상태를 확인하기 위해 Airflow에서 사용하는 이름임
- 워크플로에 Sensor를 적용하려고 하는 경우, 워크플로의 시작시간을 아까 02:00에 셋팅했던 것과는 다르게 시작시간(16:00)에 배치

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_20.png)

- 해당 DAG는 각 슈퍼마켓의 데이터 처리 시작 부분에 태스크(`FileSensor`)를 추가해서 아래와 같이 표시됨

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_21.png)

- 위의 그림에서는 DAG가 시작 시 추가되었고, 예상되는 데이터 전달 전에 `schedule_interval` 이 시작되도록 설정됨
- 이로 인해 DAG 시작 시, 센서는 데이터 가용성을 지속적으로 확인하고 조건 충족시 다음 태스크 수행

### 사용자 지정 조건 풀링
- `FileSensor`는 `data-*.csv` 와 같이 패턴과 일치하는 와일드카드 형식을 지원함
- 이런 와일드 카드를 사용하여 여러 파일을 처리할 때 주의할 점은 `data-1.csv` 가 공유 스토리지에 업로드되는 동안 다른 파일 데이터가 제공되면 `FileSensor`는 True 를 반환하게 됨. 이렇게 되면 원치않은 결과를 만들어냄
- 이를 위한 해결 방안으로 제일 마지막 파일에는 _SUCCESS 라는 접미사를 붙이고, 데이터 팀은 `data-*.csv`와 `_SUCCESS`라는 파일 이름을 확인하기로 결정
- `FileSensor` 는 글로빙을 사용해 파일 또는 디렉토리 이름과 패턴을 일치시킬 수 있음
- 하지만 위의 글로빙보다는 `PythonSensor`로 두가지 조건을 확인하는 것이 좀 더 가독성이 좋음
- <b>`PythonSensor`는 PythonOperator 와 유사하게 파이썬 콜러블을 지원하며, 성공적으로 조건을 충족됐을 경우 True, 실패했을 경우 False를 반환</b>
~~~python
from pathlib import Path
from airflow.sensors.python import PythonSensor


def wait_for_supermarket(supermarket_id):
    supermarket_path = Path("/data/" + supermarket_id)
    data_files = supermarket_path.glob("data-*.csv")
    success_file = supermarket_path / "_SUCCESS"
    return data_files and success_file.exists()


wait_for_supermarket_1 = PythonSensor(
    task_id="wait_for_supermarket_1",
    python_callable=wait_for_supermarket,
    op_kwargs={"supermarket_id": "supermarket1"},
    dag=dag
)
~~~

### 원할하지 않은 흐름의 센서 처리
- 만약 슈퍼마켓 데이터가 더 이상 제공되지 않는다면, 기본적으로 센서는 다른 오퍼레이터와 마찬가지로 실패함 
- 센서는 최대 실행 허용 시간(초)를 지정하는 `timeout` 인수를 허용함  
  다음 포크의 시작시 실행 시간이 timeout 설정값보다 초과된다면 센서는 실패를 반환함

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_22.png)

- 기본적으로 Sensor의 timeout은 7일로 설정되어 있음.
- <b>만약 timeout이 7일로 설정되어 있는 상태에서 schedule_interval이 하루에 한 번 실행되도록 설정되어 있다면, 이는 문제를 발생시킴</b>
- supermarket_2, 3, 4 는 timeout 이 지난 7일 후에 실패로 나타나게 될텐데, 이 전에는 매일 3개의 태스크가 계속 쌓여서 풀링(대기)하게됨
- airflow는 이렇게 많은 태스크가 동시에 실행되는 것을 제한하기 위해 `DAG` 의 파라미터로 `Concurrency`라는 인자에 숫자 값을 지정하여 최대 태스크 실행 수를 제한할 수 있음
- 다음은 DAG에서 최대 동시 태스크 수를 설정하는 예제
~~~python
dag = DAG(
  dag_id="couponing_app",
  start_date=datetime(2019, 1, 1),
  schedule_interval="0 0 * * *",
  concurrency=50,
)
~~~
- 문제는 이렇게 7일 전까지 풀링되는 태스크 수가 증가하는 것을 <b>데드 락(deadlock)</b> 현상이라고 함
- 다른 DAG의 태스크는 실행할 수 있지만, 슈퍼마켓 DAG는 실행할 수 있는 최대 태스크 수에 도달해 차단(block)됨
- <b>Airflow 전역 설정의 최대 태스크 제한에 도달하면 전체 시스템이 정지 될 수 있음</b>
- 센서 클래스는 `mode` 파라미터에 `poke` 또는 `reschedule` 값을 지정하여 설정할 수 있는데, 기본 default 값은 `poke`이며 이는 최대 태스크 제한에 도달하면 새로운 태스크가 차단됨
- `reschedule` 는 포크 동작을 실행할 때만 슬롯을 차지하며, 대기 시간 동안은 슬롯을 차지하지 않음

## 다른 DAG을 트리거하기
- 이제는 슈퍼마켓들이 `create_metrics` 의 결괏값을 활용해 통찰력을 얻고자 함
- 현재는 `supermarket_{1, 2, 3, 4}` 태스크의 성공 여부에 따라 `create_metrics` 단계가 끝나는 마지막 시점에 하루에 한번만 실행됨
- 분석 팀은 모든 결괏값이 끝나고 난 뒤 결과값을 제공받는 것이 아니라, 각 슈퍼마켓의 데이터 처리 직후 계산된 통계 지표를 사용할 수 있기를 원함
- 한가지 해결방안은 <b>모든 process_supermarket_*</b> 태스크 실행 후에 `create_metrics` 작업을 다운스트림 작업으로 설정할 수 있음(아래 그림)

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_23.png)

- `create_metrics` 태스크가 여러 태스크로 확장되어 DAG의 구조가 더욱 복잡해짐. 결과적으로 더 많은 반복 태스크가 발생하게됨

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_24.png)

- <b>비슷한 기능의 태스크 반복을 피하는 한가지 옵션은 DAG을 분리해 DAG1이 DAG2를 여러번 호출하게 하는 것</b>

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_25.png)

- 이러한 방법의 장점은, 단일 DAG에서 중복된 태스크를 가지고 있지 않고, DAG1 이 DAG2를 여러 번 호출할 수 있다는 것
- 이 방법의 사용은 여러 상황에서 사용될 수 있는데, 예를 들어 <b>스케줄 완료를 기다리지 않고 언제든지 수동으로 트리거할 수 있는 통계 지표를 생성하는 경우에 사용됨</b>
- 이런 시나리오에서는 `TriggerDagRunOperator`를 이용하여 다른 DAG을 실행할 수 있음
~~~python
import airflow.utils.dates
from airflow import DAG

from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

dag1 = DAG(
    dag_id="ingest_supermarket_data",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="0 16 * * *",
)

for supermarket_id in range(1, 5):
    trigger_create_metrics_dag = TriggerDagRunOperator(
        task_id=f"trigger_create_metrics_dag_supermarket_{supermarket_id}",
        trigger_dag_id="create_metrics",
        dag=dag1,
    )

    dag2 = DAG(
        dag_id="create_metrics",
        start_date=airflow.utils.dates.days_ago(3),
        schedule_interval=None,
    )
~~~
- <b>`TriggerDagRunOperator` 의 `trigger_dag_id` 인수에 제공되는 문자열은 트리거할 DAG의 `dag_id`와 일치해야 함</b>
- 결과적으로 슈퍼마켓에서 데이터를 수집하기 위한 DAG와 데이터의 통계 지표를 계산하기 위한 DAG로 두 개가 됨
- 트리 뷰의 두 가지 상세 내역을 통해 스케줄에 따라 실행/수동 실행 여부를 확인할 수 있음
  - 태스크 인스턴스에 검은색 테두리는 스케줄된 실행 상태, 테두리가 없는 태스크는 트리거(수동)된 상태를 나타냄
  - DAG 실행은 `run_id` 필드가 있으며, 다음 중 하나로 실행되기 때문에 해당 인자값을 확인할 수 있음
    - `schedule__`: 스케줄되어 DAG 실행이 시작되었음을 나타냄
    - `backfill__`: 백필 태스크에 의해 DAG 실행이 시작되었음을 나타냄
    - `manual__`: 수동으로 DAG 실행이 시작되었음을 나타냄
- 아래 그림처럼 원 위로 마우스를 가져가면 `run_id` 값의 툴팁이 표시됨

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_26.png)

### TriggerDagRunOperator로 백필 작업
- process_* 태스크의 일부 로직을 변경하고 변경된 부분부터 DAG를 다시 실행하려면 <b>단일 DAG</b>에서는 process_* 및 해당 다운스트림 태스크의 상태를 삭제하면 되지만 <b>또 다른 DAG 안에서 `TriggerDagRunOperator` 의 다운스트림 태스크는 지워지지 않음</b>
- `TriggerDagRunOperator`를 포함한 DAG에서 태스크를 삭제하면 이전에 트리거된 해당 DAG 실행을 지우는 대신 <b>새 DAG 실행이 트리거됨</b>

### 다른 DAG의 상태를 폴링하기
- 앞선 예제(DAG1, DAG2가 있는 예제)와 달리, 아래 그림의 중간과 같이 <b>해당 DAG에 대해 각각 TriggerDagRunOperator 태스크를 수행하거나</b> 오른쪽 그림과 같이 <b>여러 다운스트림 DAG를 트리거</b>하는 TriggerDagRunOperator 사용 가능

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_27.png)

- 그렇다면 다른 DAG가 실행되기 전에 여러 개의 트리거 DAG가 완료되어야 한다면 어떻게 해야할까?  
  예를 들어 DAG 1, 2, 3이 각각 작업을 수행하고 세 개의 DAG가 모두 완료된 후에 집계된 지표의 데이터 세트를 계산하는 DAG 4를 실행하려면 어떻게 해야 할까?
- <b>Airflow는 단일 DAG 내 태스크 간의 의존성을 관리하지만, DAG 간의 의존성을 관리하는 방법은 제공하지 않음</b>
- 위의 상황에서는 `ExternalTaskSensor`를 사용해야하는데, 이 방법은 아래와 같이 `wait_for_etl_dag` 에서처럼 태스크가 마지막으로 report 태스크를 실행하기 전 세 개의 DAG가 모두 완료된 상태를 확인하는 프락시 역할을 수행

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_28.png)

- `ExtractTaskSensor`의 작동 방식은 다른 DAG의 태스크를 지정하여 해당 태스크의 상태를 확인하는 것

~~~python
import airflow.utils.dates
from airflow import DAG

from airflow.operators.dummy import DummyOperator
from airflow.sensors.external_task import ExternalTaskSensor

dag1 = DAG(dag_id="ingest_supermarket_data", schedule_interval="0 16 * * *")
dag2 = DAG(schedule_interval="0 16 * * *", ...)

DummyOperator(task_id="copy_to_raw", dag=dag1) >> DummyOperator(task_id="process_supermarket", dag=dag1)

wait = ExternalTaskSensor(
    task_id="wait_for_process_supermarket",
    external_dag_id="ingest_supermarket_data",  # 위의 ingest_supermarket_data dag_id 입력.
    external_task_id="process_supermarket",     # 위의 process_supermarket task_id 입력.
    dag=dag2,
)

report = DummyOperator(task_id="report", dag=dag2)
wait >> report
~~~

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_29.png)

- 앞서 말한 것처럼, Airflow는 DAG가 다른 DAG를 고려하지 않음. 기술적으로 기본 메타데이터(ExternalTaskSensor가 수행하는 작업)를 쿼리하거나 디스크에서 DAG 스크립트를 읽어서 다른 워크플로의 실행 세부 정보를 추론할 수 있지만, Airflow와 직접적으로 결합되지는 않음
- <b> `ExternalTaskSensor`를 사용하는 경우, `ExternalTaskSensor` 가 자신과 정확히 동일한 실행 날짜를 가진 태스크에 대한 성공만 확인하는 것을 반드시 기억하자</b>
- 예를 들어, `ExternalTaskSensor`의 실행 날짜가 2019-10-12 18:00 인 경우, Airflow 메타스토어에 2019-10-12 18:00 인 태스크를 쿼리해 확인함

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_30.png)

- 스케줄 간격이 맞지 않는 경우는 `ExternalTaskSensor` 가 다른 태스크를 검색할 수 있도록 offset 간격을 설정할 수 있음
- 이 오프셋은 `ExternalTaskSensor`의 `execution_delta` 인수로 설정함
- <b>timedelta 설정값 입력을 조심해야하는데, 양수로 입력했다면, 이는 execution_date 에서 뺌. 즉 hours=4를 입력했다면 4시간을 거슬러 올라가는 것을 의미함</b>

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_31.png)


## REST/CLI를 이용해 워크플로 시작하기
- <b>다른 DAG에서 DAG을 트리거하는 방법 외에도 REST API, CLI를 통해 트리거 할 수 있음</b>
  - ex1) CI/CD 파이프라인의 일부로 airflow 외부에서 워크플로를 시작하려는 경우
  - ex2) AWS S3 버킷에 임의 시간에 저장되는 데이터를 확인하기 위해 Airflow sensor대신 AWS Lambda 함수를 사용하여 DAG 트리거하는 경우
- Airflow CLI를 사용하여 다음과 같이 DAG를 트리거할 수 있음
~~~shell
$ airflow dags trigger dag1
~~~
- 위처럼 실행하면, 실행 날짜가 현재 날짜 및 시간으로 설정된 dag1을 트리거함
- DAG run id 에 수동 또는 Airflow 외부에서 트리거되었다는 것을 나타내기 위해 "manual__"이라는 접두사가 붙게 됨
- CLI는 트리거된 DAG에 대한 추가 구성 설정이 가능함
~~~shell
airflow dags trigger -c '{"supermarket_id": 1}' dag1
airflow dags trigger --conf '{"supermarket_id": 1}' dag1
~~~
- 위와 같은 방법은 task context 변수를 통해 실행된 DAG의 모든 태스크에서 사용 가능
~~~Python
import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator

dag1=DAG(
    dag_id="print_dag_run_conf",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval=None,
)


def print_conf(**context):
    print(context["dag_run"].conf)  # task context에서 트리거되는 DAG에 접근할 때 제공되는 구성 파일


process = PythonOperator(
    task_id="process",
    python_callable=print_conf,
    dag=dag1,
)
~~~
- Airflow 인스턴스에 HTTP 접근으로 REST API를 사용해도 동일한 결과를 얻을 수 있음
~~~
# URL is /api/v1

curl \
-u admin:admin \ # 평문(paintext)으로 사용자 이름과 비밀번호를 보내는 것은 바람직하지 않음. 다른 인증 방법은 Airflow API 인증 문서 참고
-X POST \
"http://localhost:8080/api/v1/dags/print_dag_run_conf/dagRuns" \
-d "{conf: {}}"  # 추가 구성 설정이 제공되지 않은 경우에도 엔드포인트에는 데이터가 필요
~~~
~~~
curl \
-u admin:admin \
-X POST \
"http://localhost:8080/api/v1/dags/print_dag_run_conf/dagRuns" \
-H "Content-Type: application/json" \
-d '{conf: {"supermarket": 1}}' 
~~~

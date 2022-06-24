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
- 
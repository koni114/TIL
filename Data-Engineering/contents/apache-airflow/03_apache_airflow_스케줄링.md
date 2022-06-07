# chapter03 Airflow 의 스케줄링
- 이번 장에서는 스케줄 간격으로 증분 데이터를 처리하는 방법을 확인해보자
- 웹 사이트의 사용자 이벤트를 분석하는 간단한 사례를 소개하고 DAG을 구성해 정기적으로 사용자 이벤트를 분석하는 예제 수행 

## 예시: 사용자 이벤트 처리하기
- 웹 사이트에서 사용자 동작을 추적하고 사용자가 웹 사이트에서 액세스한 페이지(IP 주소로 식별)를 분석할 수 있는 서비스가 있다고 가정해보자
- 마케팅의 목적으로, 사용자들이 얼마나 많은 다양한 페이지에 접근하고 그들이 방문할 동안 얼마나 많은 시간을 소비하는지 알고 싶음
- 시간이 지남에 따라 사용자 행동이 어떻게 변하는지 알기 위해, 우리는 이 통계량을 매일 계산하려고 함
- 이를 통해 매일 또는 특정 기간의 변화를 비교할 수 있음
- 외부 추적 서비스는 실용성을 이유로 30일 이상 데이터를 저장하지 않음. 하지만 우리는 더 오랜 기간 동안 과거 데이터를 보존하고 싶기 때문에, 직접 이 데이터를 모아 저장해야 함
- 일반적으로 raw 데이터가 매우 클 수 있기 때문에 아마존의 S3나 구글 Cloud Storage 서비스와 같은 클라우드 스토리지 서비스에 데이터를 저장하는 것이 합리적임. 하지만 이번 예제에서는 단순 구현을 위해 로컬에 데이터를 저장
- 이 예제를 시뮬레이션하기 위해 간단한 API를 제작했다고 가정해보자. 다음 API를 호출하면 지난 30일 동안 모든 이벤트 목록이 반환됨
~~~shell
curl -o /tmp/events.json http://localhost:5000/events
~~~
- 두 가지 태스크로 나눌 수 있음.
  - 사용자 이벤트를 가져옴
  - 통계 및 계산
- 이벤트 데이터는 `BashOperator`, 통계 및 계산은 `PythonOperator`를 사용해 데이터 로드 후 groupby 및 aggregation 을 사용
- 이는 다음과 같은 DAG 제공
~~~python
import datetime as dt
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag=DAG(
    dag_id="01_unscheduled",
    start_date=dt.datetime(2022, 4, 17),
    schedule_interval=None,
)

fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p / data &&"
        "curl -o /data/events.json"
        "https://localhost:5000/events"
    ),
    dag=dag,
)


def _calculate_stats(input_path, output_path):
    """이벤트 통계 계산하기"""
    events=pd.read_json(input_path)
    stats=events.groupby(["date", "user"]).size().reset_index()
    Path(output_path).parent.mkdir(exist_ok=True)
    stats.to_csv(output_path, index=False)


calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    op_kwargs={
        "input_path": "/data/events.json",
        "output_path": "/data/stats.csv",
    },
    dag=dag,
)

fetch_events >> calculate_stats
~~~

## 정기적으로 실행하기
- `schedule_interval` 인수를 사용하여 정기적으로 실행이 가능
~~~python
dag=DAG(
    dag_id="02_daily_schedule",
    schedule_interval="@daily",
    start_date=dt.datetime(2019, 1, 1),
    end_date=dt.datetime(2019, 1, 5),
) 
~~~
- `schedule_interval` 외에도 `start_date` 에 날짜를 지정하여 DAG를 언제부터 시작할지 지정해야함
- <b>중요한 것은 시작 날짜를 기준으로 첫 번째 DAG의 실행을 스케줄(시작 날짜 + 간격)함</b>  
  예를 들어 `start_date` 를 01-01-2019 라고 준 후, `schedule_interval`을 @daily 라고 준다면 자정이 될 때까지 작업이 이루어지지 않음
- `end_date`를 지정하여 종료 날짜도 지정 가능


### Cron 기반의 스케줄 간격 설정하기
- Airflow 는 더 복잡한 스케줄 간격 설정을 지원하기 위해 cron과 동일한 구문을 사용해 스케줄 간격을 정의할 수 있음
- cron 구문은 5개의 구성 요소가 있으며, 다음과 같이 정의됨
~~~
*  *  *  *  *
분 시간 일 월 요일
분   --> (0 ~ 59)
시간 --> (0 ~ 23)
일   --> (1 ~ 31)
월   --> (1 ~ 12)
요일  --> (0 ~ 6) (일요일 ~ 토요일. 일부 시스템에서 7은 일요일임..)
~~~
- cron job은 시간/날짜가 해당 필드의 값과 시스템 시간이 일치할 때 실행됨
- 숫자 대신 * 로 신경쓰지 않는 다는 것을 표시할 수 있음
- 다음과 같이 매시, 매일, 매주 간격을 정의할 수 있음
~~~
0 * * * *  = 매시간(정시에 실행)
0 0 * * *  = 매일(자정에 실행)
0 0 * * 0  = 매주(일요일 자정에 실행)
~~~
- 또한 cron 식을 사용하면 콤마(쉼표, ',')를 사용하여 값의 리스트를 정의하거나 대시('-')를 사용하여 값의 범위를 정의하는 값의 집합을 지정할 수 있음
~~~
0 0 * * MON, WED, FRI = 매주 월, 화, 금요일 자정에 실행
0 0 * * MON-FRI = 매주 월요일부터 금요일 자정에 실행
0 0,12 * * * = 매일 자정 및 오후 12시에 실행
~~~
- Airflow는 스케줄 간격을 의미하는 약어를 사용한 몇 가지 매크로 지원
  - `@once` : 1번만 실행하도록 지원
  - `@hourly`: 매시간 변경 시 1회 실행
  - `@daily`: 매일 자정에 1회 실행
  - `@weekly`: 매주 일요일 자정에 1회 실행
  - `@monthly`: 매월 1일 자정에 1회 실행
  - `@yearly`: 매년 1월 1일 자정에 1회 실행
- cron 식은 기능이 좋지만 헷갈릴 수 있으므로, Airflow를 적용하기 전, 작성된 태스크에 대해서 테스트 하는 것이 좋음  
  https://crontab.guru 에서 테스트 가능

### 빈도(frequency) 기반의 스케줄 간격 작성하기
- cron 식의 제약은 특정 빈도(frequency) 마다 스케줄을 정의할 수 없다는 것  
  예를 들어 3일에 한 번씩 실행하는 cron 식은 어떻게 정의해야 할까요? 매월 1, 4, 7, ...로 표현 할 때 이번 달 31일과 다음 달 1일을 포함해 생각하면, 다음 달에 원하는 결과를 얻을 수 없음
- Airflow는 이런 상대적인 시간 간격으로 스케줄 간격을 정의할 수 있도록 지원함.  
  빈도 기반 스케줄을 사용하려면 `timedelta`(표준 라이브러리인 datetime 모듈에 포함된) 인스턴스를 사용하면 됨
~~~python
dag=DAG(
    dag_id="04_time_delta",
    schedule_interval=dt.timedelta(day=3),  # timedelta 는 빈도 기반 스케줄을 사용할 수 있는 기능을 제공
    start_date=dt.datetime(year=2019, month=1, day=1),
    end_date=datetime(year=2019, month=1, day=5),
)
~~~
- 이렇게 설정하면 DAG가 시작 시간으로부터 3일마다 실행됨(2019년 1월 4일, 1월 7일 ..)

## 데이터 증분 처리하기
- `@daily` 로 설정시, DAG가 매일 사용자 이벤트 카탈로그 전체에 대해 다운로드하고 계산하는 작업은 효율적이지 못함

### 이벤트 데이터 증분 가져오기
- 이런 문제를 해결하는 방법은 데이터를 순차적으로 가져올 수 있도록 DAG를 변경하는 것
- 스케줄 간격에 해당하는 일자의 이벤트만 로드하고 새로운 이벤트만 통계를 계산
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_04.png)
- 이러한 증분 방식(incremental approach)는 스케줄된 하나의 작업에서 처리해야 할 데이터 양을 크게 줄일 수 있기 때문에, 전체 데이터 세트를 처리하는 것보다 훨씬 효율적
- 날짜별로 분리된 단일 파일로 저장하고 있기 때문에 API가 제한하고 있는 30일간의 내용을 하나로 저장하지 않고 시간이 지남에 따라 매일 순차적으로 파일을 저장할 수 있음
- 워크플로에서 증분 데이터 처리를 구현하려면 DAG를 수정하여 특정 날짜의 데이터를 다운로드함  
- 시작 및 종료 날짜 매개변수를 함께 정의하여 해당 날짜에 대한 이벤트 데이터를 가져오도록 API 호출을 조정할 수 있음
~~~shell
curl -O http://localhost:5000/events?start_date=2019-01-01&end_date=2019-01-02
~~~
- 두 날짜 매개변수는 이벤트 데이터의 시간 범위를 나타내며, <b>예제에서 `start_date`는 포함되는 날짜, `end_date`는 포함하지 않는 날짜</b>
- 두 날짜를 포함하도록 배시 명령을 변경하여 DAG에서 증분 데이터를 가져오도록 구현할 수도 있음
~~~python
fetch_events=BashOperator(
    task_id="fetch_events",
    bash_command=(
    "mkdir -p /data && "
    "curl -o /data/events.json "
    "http://localhost:5000/events?"
    "start_date=2019-01-01&"
    "end_date=2019-01-02"
    ),
    dag=dag, 
)
~~~

### 실행 날짜를 사용하여 동적 시간 참조하기
- Airflow는 태스크가 실행되는 특정 간격을 정의할 수 있는 추가 매개변수를 제공함
- 이런 매개변수 중 가장 중요한 매개변수는 DAG가 실행되는 날짜와 시간을 나타내는 `execution_date` 임
- <b>execution_date 는 DAG를 시작하는 시간의 특정 날짜가 아니라 `schedule_interval`로 실행하는 시작 시간을 나타내는 타임스탬프임</b>  
  아래 그림을 보면서 설명
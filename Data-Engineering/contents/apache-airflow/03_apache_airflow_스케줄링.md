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


## Cron 기반의 스케줄 간격 설정하기
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


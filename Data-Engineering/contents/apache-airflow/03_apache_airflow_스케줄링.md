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
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_05.png)
- 위의 그림에서 보면 현재 시점을 기준으로 `schedule_interval`이 실행된 시작시간은 2019-01-03 00:00 이며, 이 시간이 `execution_date`가 됨
- 다음 실행일(2019-01-04 00:00)이 `next_execution_date`며, 이전 실행 시간(2019-01-02 00:00)이 `previous_execution_date` 매개변수임
- Airflow 에서는 이러한 실행 날짜를 오퍼레이터에서 참조하여 사용할 수 있음. 예를 들어 BashOperator 에서 Airflow 의 탬플릿 기능을 사용하여 배시 명령이 실행될 날짜를 동적으로 포함할 수 있음
~~~python
fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /data && "
        "curl -o /data/events.json "
        "http://localhost:5000/events?"
        "start_date={{execution_date.strftime('%Y-%m-%d')}}"
        "&end_date={{next_execution_date.strftime('%Y-%m-%d')}}"
    ),
    dag=dag,
)
~~~
- {{variable_name}} 구문은 Airflow 의 특정 매개변수 중 하나를 참조하기 위해 Airflow의 Jinja 탬플릿 구문을 사용하는 예
- `execution_date` 매개변수는 종종 날짜를 형식화된 문자열로 참조하여 사용되기 때문에 Airflow 는 일반적인 날짜 형식에 대한 여러 유형의 축약 매개변수(shorthand parameters)를 제공함
- 예를 들어 `ds` 및 `ds_nodash` 매개 변수는 각각 YYYY-MM-DD 및 YYYYMMDD 형식으로 된 execution_date 의 다른 표현임
- `next_ds`, `next_df_nodash`, `prev_ds`, `prev_ds_nodash`는 각각 다음, 이전 실행 날짜에 대한 축약 표기법
- 축약 표기법을 사용하여 다음과 같이 증분 데이터를 가져올 수 있음
~~~python
fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /data && "
        "curl -o /data/events.json "
        "http://localhost:5000/events?"
        "start_date={{ds}}"       # ds 는 YYYY-MM-DD 형식의 execution_date 를 제공
        "&end_date={{next_ds}}"   # next_ds 는 next_execution_date 에 대해 동일하게 제공
    ),
    dag=dag,
)
~~~

### 데이터 파티셔닝
- 위의 BashOperator 의 경우, 새로운 스케줄한 간격으로 점진적인 이벤트 데이터를 가져와 전일의 데이터를 덮어쓰게 됨  
  (events.json 파일명이 동일하기 때문)
- 한가지 방법은 events.json 파일에 새 이벤트를 추가하는 것. 하지만 이는 JSON 파일에 모든 데이터를 작성할 수 있음  
  그러나 이 방법의 단점은, 특정 날짜의 통계 게산을 하려고 해도 전체 데이터 세트를 로드하는 다운스트림 프로세스 작업이 필요
- 또한 파일이 손상될 위험이 있음
- 이를 해결하는 다른 방법은 태스크의 출력을 해당 실행 날짜의 이름이 적힌 파일에 기록함으로써 데이터 세트를 일일배치로 나누는 것임
~~~python
fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /data && "
        "curl -o /data/events/{{ds}}.json " # 반환된 값이 탬플릿 파일 이름에 기록됨
        "http://localhost:5000/events?"
        "start_date={{ds}}"      
        "&end_date={{next_ds}}"  
    ),
    dag=dag,
)
~~~
- 데이터 세트를 더 작고 관리하기 쉬운 조각으로 나누는 작업은 데이터 저장 및 처리 시스템에서 일반적인 전략임  
  이러한 방법을 일반적으로 <b>파티셔닝(partitioning)</b>이라고 함
- 파티셔닝 전략은 이후에 데이터 전처리 및 통계값 편성시에 전체 데이터를 로드하지 않아도 되는 이점을 가지고 있음
~~~python
def _calculate_stats(** context):
    """Calculates event statistics"""
    input_path=context["template_dict"]["input_path"]    # template_dict 에서 template 값 검색 
    output_path=context["templates_dict"]["output_path"] 
    Path(output_path).parent.mkdir(exist_ok=True)

    events=pd.read_json(input_path)
    stats=events.group_by(["date", "user"]).size().reset_index()
    stats.to_csv(output_path, index=False)

calculate_stats=PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats
    templates_dict={
        "input_path": "/data/events/{{ds}}.json" 
        "output_path": "/data/stats/{{ds}}.json"
    },
    dag=dag,
)
~~~
- `templates_dict` 매개변수를 사용하여 탬플릿해야 하는 모든 인수를 전달해야하며, Airflow에 의해 `_calculate_stats` 함수에 전달된 콘텍스트 개체에서 함수 내부의 탬플릿 값을 확인할 수 있음
- Airflow 1.10.x 버전에서는 PythonOperator 에 추가 인수 `provide_context=True`를 전달해야 함  
  그렇지 않으면 `_calculate_stats` 함수가 콘텍스트 값을 수신하지 않음

## Airflow의 실행 날짜(execution_date) 이해
### 고정된 스케줄 간격으로 태스크 실행
- `execution_date`는 DAG가 실제 실행되는 순간이 아니라, 예약 간격의 시작 날짜임을 잊지말자
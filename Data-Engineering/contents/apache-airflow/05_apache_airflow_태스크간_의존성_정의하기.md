# chapter05 태스크 간 의존성 정의하기
- 트리거 규칙을 사용하여 조인을 구현하는 방법
- XCom을 이용하여 태스크 사이의 상태 공유 방법 
- Airflow 2 의 TaskFlow API 를 사용해 파이썬을 많이 사용하는 DAG를 단순화하는 방법

## 기본 의존성 유형
- 다양한 태스크 의존성 패턴에 대해서 살펴보자
- 태스크의 선형 체인(linear chain) 유형과 팬아웃/팬인(fan-out / fan-in) 유형이 모두 포함됨
- <b>팬아웃/팬인(fan-out/fan-in)유형은 하나의 태스크가 여러 다운스트림 태스크에 연결되거나 그 반대의 동작을 수행하는 유형임</b>   

### 선형 의존성 유형
- 지금까지 진행했던 예제들은 단일 선형 태스크 체인으로 구성된 DAG에 초점을 맞추어 설명함
- 예를 들어, 2장에서 DAG를 가져오는 로켓 발사 사진은 세 가지 태스크의 체인으로 구성되어 있음
- `>>` 연산자를 통해 의존성을 정의하였고, 즉 이러한 태스크 의존성을 통해 Airflow 는 업스트림 의존성이 성공적으로 실행된 후에 지정된 다음 태스크를 시작할 수 있음
- 태스크 의존성을 명시적으로 지정하면 얻는 한 가지 이점은 <b>여러 태스크에서 순서를 명확하게 정의한다는 것</b>
- 이를 통해 의존성이 충족된 경우에만 태스크를 스케줄 할 수 있으며, 이는 Cron 을 사용하여 개별 태스크를 차례로 스케줄하고, 두 번째 태스크가 시작될 때 이전 태스크가 완료되기를 기다리는 것보다 확실하게 처리할 수 있음

### 팬인/팬아웃(Fan-in/Fan-out) 의존성
- 예를 들기 위하여 1장의 우산 사용 사례를 생각해보자
- 일기예보를 기반으로 다가오는 몇 주 동안 우산 수요를 예측하기 위해 머신러닝 모델을 학습시키려고 함
- Umbrella DAG의 주요 목적은 서로 다른 두 소스에서 매일 날씨 및 판매 데이터를 가져와 데이터 결합 후 모델을 학습시키는 것

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_10.png)

- 날씨 데이터 가져오기/정제하기는 판매 데이터와 무관하기 때문에 두 작업 간의 상호 의존성은 존재하지 않음
- 즉 다음과 같이 데이터 가져오기 및 정제 태스크에 대한 의존성을 정의할 수 있음
~~~python
fetch_weather >> clean_weather
fetch_sales >> clean_sales
~~~
- <b>두 가져오기 태스크의 업스트림에 DAG의 시작을 나타내는 더미 태스크를 추가할 수도 있음</b>
- 이 태스크는 반드시 필요한 것은 아니지만, `fetch_weather` 및 `fetch_sales` 작업이 모두 시작되는 DAG 시작 시 발생하는 암묵적인 팬아웃(fan-out)(여러 개의 입력 태스크 연결 수 제한)을 설명하는 데 도움이 됨
- 이러한 팬아웃 종속성(한 태스크를 여러 다운스트림 태스크에 연결하는 것)은 다음과 같이 정의할 수 있음
~~~python
from airflow.operators.dummy import DummyOperator

start=DummyOperator(task_id="start")
start >> [fetch_weather, fetch_sales]
~~~
- 두 데이터(날씨, 판매)가 결합된 데이터를 가져오기 위해서는 `clean_weather`, `clean_sales` 태스크 모두에 의존성을 가지며, 이러한 업스트림 태스크가 모두 성공적으로 완료된 후에만 활성화할 수 있음
- <b>하나의 태스크가 여러 업스트림 태스크에 영향을 받는 구조를 팬인(fan-in) 구조라고 함</b>
- 팬인 구조는 다음과 같이 정의 가능
~~~python
[clean_weather, clean_sales] >> join_datasets
~~~
- `join_datasets` 이후는 태스크 체인으로 구성
~~~python
join_datasets >> train_model >> deploy_model
~~~
- 태스크를 결합하면 다음과 같은 결과를 얻을 수 있음

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_11.png)

- DAG을 실행하면 Airflow가 먼저 시작 태스크를 실행함
- 시작 태스크가 완료되면 `fetch_sales` 및 `fetch_weather` 태스크가 병렬로 실행됨(여러 작업 실행이 가능하도록 Airflow가 설정되어 있다고 가정)
- 데이터를 가져오는 태스크 중 하나가 완료되면 해당 데이터 정제 태스크가 시작됨
- 이후 작업은 순차적으로 수행됨

## 브랜치하기
- 만약 DAG 에서 판매 데이터 수집 작업을 완료했을 때, 회사 동료로부터 새로운 소식을 들었다고 가정해보자
- 관리자는 ERP 시스템 전환을 결정해, 판매 데이터가 1~2주 내에 다른 소스에서 제공될 예정. 이러한 변경이 있더라도 모델 학습이 중단돼서는 안됨
- 또한 향후 분석에서 과거 판매 데이터를 계속 사용할 수 있도록 이전 시스템과 새로운 시스템 모두 정상 동작하기를 바람

### 태스크 내에서 브랜치하기
- 첫 번째 접근 방식은 수집 태스크를 다시 작성하여 실행 날짜를 통해 판매 데이터 수집 및 처리를 위한 두 개의 개별 코드로 분리 가능
~~~python
def _clean_sales(** context):
    if context["execution_date"] < ERP_CHANGE_DATE:
        _clean_sales_old(**context)
    else:
        _clean_sales_new(**context)

clean_sales_data=PythonOperator(
    task_id="clean_sales",
    python_callable=_clean_sales,
)
~~~
- 이렇게 코드를 작성하면, 두 함수의 결과가 호환되는 한,(열, 데이터 유형 등) 나머지 두 ERP 시스템 간 차이로 DAG는 변경하지 않아도 됨
- 마찬가지로, 초기 수집 단계도 두 ERP 시스템과 호환되도록 만들 수 있음
~~~python
def _fetch_sales(** context):
    if context["execution_date"] < ERP_CHANGE_DATE:
        _fetch_sales_old(** context)
    else:
        _fetch_sales_new(** context)
~~~
- <b>이 접근 방식의 장점은 DAG 자체의 구조를 수정하지 않고도 DAG에서 약간의 유연성을 허용할 수 있다는 점</b>
- 그러나 이 접근 방식은 코드로 분기가 가능한 유사한 태스크로 구성된 경우에만 가능
- 만약 새로운 데이터 소스가 완전히 다른 태스크 체인이 필요하면 어떻게 해야할까? 이 경우에는 데이터 수집을 두 개의 개별 태스크 세트로 분할하는 것이 나을 수 있음
- 이 접근 방식의 단점은 특정 DAG 실행 중에 Airflow 에서 어떤 코드 분기를 사용하고 있는지 확인하기 어렵다는 점

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_12.png)

### DAG 내부에서 브랜치하기
- 두 번째 방법은 두 개의 개별 태스크 세트(각 시스템에 하나씩)를 개발하고 DAG가 이전 또는 새로운 ERP 시스템에서 데이터 수집 작업 실행을 선택할 수 있도록 하는 것
- 두 가지 태스크 세트를 구축하는 것은 어렵지 않음. 적절한 오퍼레이터를 사용하여 각 ERP 시스템에 대한 태스크를 별도로 생성하고 각 태스크들을 연결하면 됨

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_13.png)

~~~python
fetch_sales_old = PythonOperator (...)
clean_sales_old = PythonOperator (...)

fetch_sales_new = PythonOperator (...)
clean_sales_new = PythonOperator (...)

fetch_sales_old >> clean_sales_old
fetch_sales_new >> clean_sales_new
~~~
- Airflow 는 다운스트림 태스크 세트 중 선택할 수 있는 기능을 `BranchPythonOperator` 를 통해 제공함
- 이 오퍼레이터는 이름을 통해서 알 수 있듯이 `PythonOperator`와 같이 파이썬 호출 가능 인수를 사용할 수 있음

~~~python
def _pick_erp_system(** context):
    if context ["execution_date"] < ERP_CHANGE_DATE:
        return "fetch_sales_old"
    else:
        return "fetch_sales_new"

pick_erp_system=BranchPythonOperator(
    task_id="pick_erp_system",
    python_callable=_pick_erp_system,
)

pick_erp_system >> [fetch_sales_old, fetch_sales_new]
~~~
- `BranchPythonOperator`에 전달된 호출 가능한 인수(위에서 `_pick_erp_system`)는 작업 결과로 다운스트림 태스크의 ID를 반환
- 반환된 ID는 브랜치 태스크 완료 후 실행 할 다운 스트림 태스크를 결정함  
- 태스크 ID 리스트를 반환하는 경우도 있으며, 이 경우 Airflow는 참조된 모든 태스크를 실행함
- 이를 통해 DAG의 실행 날짜에 따라 적절한 task_id 를 반환 후 호출 가능한 인수 기능을 사용하여 ERP 시스템 선택 기능을 구현할 수 있음
- 이전 시작 태스크와 `_pick_erp_system` 태스크 간 의존성을 추가
~~~python
start_task >> pick_erp_system
~~~
- 두 데이터 정제 태스크 연결은 정제 작업과 데이터 세트 결합(`join_datasets`)과 연결하여 작업해주면 됨
~~~python
[clean_sales_old, clean_sales_new] >> join_datasets
~~~
- 하지만 이 작업 뒤에 DAG를 실행하면, <b>join_datasets 태스크 실행 시 Airflow는 모든 다운스트림 작업을 건너뛰게 됨</b>
- 원인은 기본적으로 Airflow가 태스크 자체를 실행하기 전에 지정된 업스트림(`clean_sales_old`, `clean_sales_new`, `clean_weather`) 태스크가 성공적으로 완료되어야 하는데, `clean_sales_old`, `clean_sales_new` 둘 중 하나는 무조건 성공하지 못하는 상황이 만들어졌기 때문
- 결과적으로 Airflow 는 join_datasets 태스크를 건너뛰어 실행하지 않음
- Airflow는 <b>트리거 규칙에 의해 태스크 실행 시기를 제어함.</b> 모든 오퍼레이터에게 전달할 수 있는 `trigger_rule` 인수를 이용해 개별 태스크에 대해 트리거 규칙을 정의할 수 있음
- 기본적으로 모든 상위 태스크가 성공해야 다음 태스크를 실행할 수 있는 인수인 `all_success`로 설정되어 있음  
  이 때문에 `join_datasets` 이후에 실행이 되지 않음

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_14.png)

- 이 문제를 해결하기 위해서는 `join_datasets` 트리거 규칙을 변경하여 업스트림 태스크 중 하나를 건너뛰더라도 계속 트리거가 진행되도록 할 수 있음. <b>방법 중 한가지는 트리거 규칙을 `none_failed` </b>로 변경함
- 이를 통해 모든 상위 항목이 실행 완료 및 실패가 없을 시에 즉시 작업이 실행됨
~~~python
join_datasets=PythonOperator(
    ...,
    trigger_rule="none_failed",
)
~~~
- 이 접근 방식의 한가지 단점은 `join_datasets` 태스크에 연결되는 태스크가 3개라는 것임
- 본래 판매/날씨 데이터를 가져온 다음, 두 데이터 소스를 join_datasets 태스크에 입력하는 플로우 특성이 잘 보이지 않게 됨
- 이런 이유로 DAG에 서로 다른 브랜치를 결합하는 더미 태스크를 추가하여 브랜치 조건을 명확하게 함

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_15.png)

- Airflow에서 제공하는 내장 DummyOperator를 사용하여 더미 작업을 DAG에 추가할 수 있음
~~~python
from airflow.operators.dummy import DummyOperator

join_branch=DummyOperator(
    task_id="join_erp_branch",
    trigger_rule="none_failed"
)

[clean_sales_old, clean_saled_new] >> join_erp_branch
join_erp_branch >> join_datasets
~~~

## 조건부 태스크
- Airflow는 특정 조건에 따라 DAG에서 특정 태스크를 건너뛸 수 있는 다른 방법도 제공함
- 이를 통해 <b>특정 데이터 세트를 사용할 수 있을 때만 실행하거나 최근에 실행된 DAG인 경우만 태스크 실행 가능</b>
- 예를 들어 Umbrella DAG에는 학습하는 모든 모델을 배포하는 태스크가 있음
- 누군가가 데이터 정제 코드를 일부 변경 후, 백필을 이용해 변경 사항을 전체 데이터세트에 적용하면 모델 또한 필요한 인스턴스에 배포되어야 함

### 태스크 내에서 조건
- 가장 최근 실행된 DAG에 대해서만 모델을 배포하도록 DAG을 변경하여 이 문제를 해결할 수 있음
- 이렇게 하면 모델의 한 버전, 즉 가장 최근 데이터 세트에 대해 학습된 모델 중 특정 버전만 배포가 가능함
- 이를 수행하는 한가지 방법은 `PythonOperator`를 사용하여 배포를 구현하고 배포 함수 내에서 DAG 의 실행 날짜를 명시적으로 확인하는 것
~~~python
def _deploy(**context):
    if context["execution_date"] == "~~":
        deploy_model()

deploy=PythonOperator(
    task_id="deploy_model",
    python_callable=_deploy,
)
~~~
- 이렇게되면 동작은 하지만 배포 로직 조건이 혼용되고, PythonOperator 이외의 다른 기본 제공 오퍼레이터를 사용할 수 없음
- 또한 <b>Airflow UI에서 태스크 결과를 추적할 때 혼란스러울 수 있음</b>

### 조건부 태스크 만들기
- 조건부 배포를 구현하는 또 다른 방법은 배포 태스크 자체를 조건부화 하는 것
- 즉 미리 정의된 조건에 따라서만 실행됨
- Airflow에서는 해당 조건을 테스트하고 조건이 실패할 경우 모든 다운스트림 작업을 건너띄는 태스크를 DAG에 추가하여 태스크를 조건부화 할 수 있음
~~~python
def _latest_only(** context):
    ...
    latest_only=PythonOperator(
        task_id="latest_only",
        python_callable=_latest_only
    ) 

latest_only >> deploy_model
~~~
- 아래 DAG가 그림 5.12와 같이 `train_model` 태스크가 새 태스크에 연결되고, deploy_model 태스크가 이 새로운 태스크의 다운스트림에 연결됨

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_16.png)

- 다음으로 `execution_date`가 가장 최근 실행에 속하지 않는 경우, 다움스트림 작업을 건너뛰도록 `_latest_only` 함수를 작성
- 이를 위해 실행 날짜를 확인하고 필요한 경우 `AirflowSkipException` 함수를 실행
- 이 함수는 Airflow 가 조건과 모든 다운스트림 태스크를 건너뛰라는 것을 나타냄
~~~python
from airflow.exceptions import AirflowSkipException

def _latest_only(**context):
    left_window=context["dag"].following_schedule(context["execution_date"])  # 실행 윈도우에서 경계를 확인
    right_window=context["dag"].following_schedule(context[left_window])
    
    now = pendulum.now("UTC")  # 현재 시간이 윈도우 안에 포함되는지 확인
    if not left_window < now <= right_window:
        raise AirflowSkipException("Not the most recent run!")
~~~
- `AirflowSkipException` 이 발생 후 건너뛴 상태로 표시되며 태스크가 종료됨. Airflow 는 다운스트림 태스크의 트리거의 규칙을 살펴보고 트리거 여부를 판단함
- 기본 트리거 규칙 `all_success` 가 설정된 하나의 다운 스트림 태스크만 있기 때문에 skip 됨

### 내장 오퍼레이터 사용하기
- 가장 최근 실행한 DAG만 실행하는 예를 구현할 때, Airflow의 내장 클래스인 `LastOnlyOperator` 클래스를 사용할 수 있음
- 이 오퍼레이터는 `PythonOperator` 를 기반으로 동일한 작업을 가능하게 함. 
- `LatestOnlyOperator`를 사용하면 조건부 배포를 구현하기 위해 복잡한 로직을 작성할 필요가 없음

~~~python
from airflow.operators.lastest_only import LatestOnlyOperator

latest_only = LatestOnlyOperator(
    task_id="latest_only",
    dag=dag
)

join_datasets >> train_model >> deploy_model
latest_only >> deploy_model
~~~
- 더 복잡한 경우에는 PythonOperator 기반으로 구현하는 것이 더 효율적

## 트리거 규칙에 대한 추가 정보
- 근본적으로 Airflow는 DAG를 실행할 때 각 태스크를 지속적으로 확인하여 실행 여부를 확인
- 태스크 실행이 가능하다고 판단되면 그 즉시 스케줄러에 의해 선택된 후 실행을 예약함
- 결론적으로 Airflow에 사용 가능한 실행 슬롯이 있다면 즉시 태스크가 실행됨
- Airflow는 트리거 실행 시기를 결정하기 위해 트리거 규칙이 필요함

### 트리거 규칙이란? 
- 트리거 규칙은 태스크의 의존성 기능과 같이 Airflow 가 태스크가 실행 준비가 되어 있는지 여부를 결정하기 위한 필수적인 조건
- 기본 트리거 규칙은 `all_success`이며, 태스크를 실행하려면 모든 의존적인 태스크가 모두 성공적으로 완료되어야 함을 의미








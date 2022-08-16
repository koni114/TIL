# chapter02 Airflow DAG의 구조
- Airflow를 실행한 후 예제 워크플로를 통해 기본 컴포넌트를 사용해보는 chapter
- 로켓 애호가 사례를 통해 Airflow 를 이용하여 어떻게 해당 작업을 수행할 수 있는지 살펴보자

## 다양한 소스에서 데이터 수집
- John은 모든 로켓에 대한 뉴스를 한곳에 수집하길 원함
- 모든 로켓 발사에 대한 정보를 자동으로 수집하여 최신의 로켓 발사에 대해 간파할 수 있도록 하는 프로그램을 작성하고자 함
- 간단하게 시작하기 위해 로켓 이미지를 수집하기로 함

### 데이터 탐색
- 데이터 수집을 위해, 다양한 자료로부터 과거 및 예정된 로켓 발사 데이터를 수집하는 온라인 저장소인 Launch Library 2(https://thespacedevs.com/llapi)를 사용함
- Launch Library 2는 누구나 사용할 수 있는 오픈 API임(단 하루 요청 수 제한있음)
- John은 곧 있을 로켓 발사에만 관심이 있음. Launch Library 2는 해당 정보만 제공하는 다음과 같은 API가 있음  
  https://ll.thespacedevs.com/2.0.0/launch/upcoming  
- 해당 URL은 예정되어 있는 10개의 로켓 발사에 대한 데이터와 로켓 이미지에 대한 URL을 제공함
- 다음은 이 URL이 반환하는 데이터의 일부임
~~~shell
$ curl -L "https://ll.thespacedevs.com/2.0.0/launch/upcoming"

# 결과값은 JSON 도큐먼트로 되어 있음
# - 대괄호는 결괏값의 리스트를 나타냄
# - 중괄호 안의 값은 로켓 발사 1회 내용을 나타냄
{
"count":256,
"next":"https://ll.thespacedevs.com/2.0.0/launch/upcoming/?limit=10&offset=10",
"previous":null,
"results":[
{
"id":"f058ecca-bda7-4797-ae47-b5c450b1bd78",
"url":"https://ll.thespacedevs.com/2.0.0/launch/f058ecca-bda7-4797-ae47-
       ...
       ...
~~~
- 데이터는 JSON 형식으로 되어 있으며, 로켓 ID, 이름, 이미지 URL 과 같은 로켓 발사 정보를 제공함
- 다음 작업으로는 이미지를 수집하는 것
- 다음 이미지는 이번 챕터에서 진행할 다운로드 프로세스
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_02.png)

### 첫 번째 Airflow DAG 작성
- Airflow의 장점은 하나 이상의 단계로 구성된 대규모 작업을 개별 테스크로 분리하고 DAG 로 형성할 수 있다는 것
- 다중 태스크를 병렬로 실행할 수 있고 서로 다른 기술을 사용할 수 있음  
  예를 들어, 처음 테스크는 bash 스크립트로 실행할 수 있고, 다음 태스크는 파이썬 스크립트로 실행할 수 있음
- 위의 mental model을 3가지 논리적인 태스크로 분류할 수 있음

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/contents/apache-airflow/img/airflow_03.png)

- 위의 그림의 워크플로 코드는 다음과 같음

~~~python
import json
import os
import pathlib

import airflow
import requests
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def _get_pictures(path="/tmp/images"):
    """
    - path 경로 확인
    - launches.json 파일에 있는 모든 그림 파일 다운로드
    """

    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)

    with open("/tmp/launches.json") as f:
        launches = json.load(f)
        image_urls = [launch["image"] for launch in launches["results"]]
        # image_url = image_urls[0]
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"/tmp/images/{image_filename}"
                with open(target_file, "wb") as f:
                    f.write(response.content)
                print(f"Download {image_url} to {target_file}")
            except requests_exceptions.MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            except requests_exceptions.ConnectionError:
                print(f"Could not connect to {image_url}")


# dag 작성
dag = DAG(  # 객체의 인스턴스 생성(구체화) - 모든 워크플로의 시작점
    dag_id="download_rocket_launches",            # DAG 이름
    start_date=airflow.utils.dates.days_ago(14),  # DAG 처음 실행 시작 날짜
    schedule_interval=None,                       # DAG 실행 간격, None --> 자동으로 실행되지 않음을 의미
                                                  # Airflow UI 통해 수동으로 실행
                                                  # @daily 입력시, 매일 자정 수행됨
)


download_launches = BashOperator(  # BashOperator 를 이용해 curl 로 URL 결괏값 다운로드
    task_id="download_launches",   # 태스크 이름
    bash_command="curl -o /tmp/launches.json -L "
                 "'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",
    dag=dag
)

# task 정의
get_pictures = PythonOperator(
    task_id="get_pictures",
    python_callable=_get_pictures,
    dag=dag
)

notify = BashOperator(
    task_id="notify",
    bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images."',
    dag=dag,
)

# task 순서 지정
download_launches >> get_pictures >> notify
~~~

### 태스크와 오퍼레이터의 차이점
- Airflow operator 는 단일 작업 수행 역할을 함. 몇몇 오퍼레이터는 BashOperator 및 PythonOperator 와 같이 일반적인 작업을 수행하며, EmailOperator 또는 SimpleHTTPOperator 와 같이 좀 더 특수한 목적을 위해 사용됨
- DAG는 오퍼레이터 집합에 대한 실행을 오케스트레이션(orchestration) 하는 역할을 함
  오퍼레이터의 시작과 정지, 오퍼레이터가 완료되면 연속된 다음 태스크의 시작, 그리고 오퍼레이터 간의 의존성 보장이 포함됨
- Airflow 문서 전반에 걸쳐 오퍼레이터와 태스크라는 용어를 같은 의미로 사용하고 있음. 사용자 관점에서 모두 같은 의미이며 종종 두 용어를 혼용해서 사용함
- 하지만 두 용어의 차이점이 있는데 Airflow의 태스크는 작업의 올바른 실행을 보장하기 위한 오퍼레이터의 래퍼(wrapper) 또는 매니저(manager)로 생각해 볼 수 있음

### 임의 파이썬 코드 실행
- PythonOperator 는 파이썬 코드 실행을 담당하는데 다음 두가지 사항을 항상 적용해야함
  - 오퍼레이터 자신(`get_pictures`)를 정의해야 함
  - `python_callable` 은 인수에 호출이 가능한 일반 함수(`_get_pictures`)를 가리킴
- 편의를 위해 변수 이름(`task_id`)을 python_callable 과 동일하게 함

## airflow에서 DAG 실행하기
- Airflow 를 시작하고 실행하기 위해, 파이썬 환경에서 설치하거나 도커 컨테이너를 구동해 사용함

### 파이썬 환경에서 Airflow 실행
- PyPi를 통해 Airflow 를 설치하고 실행하기 위해서 다음을 수행
~~~shell
pip install python-airflow
~~~
- Airflow를 설치한 후 메타스토어를 초기화하고, 사용자를 만들고, 로켓 발사 DAG를 DAG 디렉터리에 복사한 후 스케줄러와 웹 서버를 시작함
~~~shell
$ airflow db init
$ airflow users create --username admin --password admin --firstname Anonymous --lastname Admin --role Admin --email admin@example.org
$ cp download_rocket_launches.py ~/airflow/dags/
$ airflow webserver
$ airflow scheduler
~~~
- 스케줄러와 웹 서버는 모두 터미널에서 실행되는 프로세스이므로, airflow webserver 백그라운드에서 실행하거나 별도의 터미널 창을 열어 스케줄러와 웹 서버를 실행해 두어야 함

### 도커 컨테이너에서 Airflow 실행하기
- 도커 컨테이너를 실행하기 위해서는 도커 엔진을 컴퓨터에 설치해야 함. 다음 명령어를 사용해 Airflow 를 실행할 수 있음
~~~linux
docker run \ 
docker run -it -p 8080:8080 \
    -v /path/to/dag/download_rocket_launches.py:/opt/airflow/dags/download_rocket_launches.py \ 
    --entrypoint=/bin/bash \
    --name airflow \
    apache/airflow:2.0.0-Python3 \
    -c '( \
        airflow db init && \
        airflow users create
        --username admin \
        --password admin \
        --firstname Anonymous \
        --lastname Admin
        --role Admin
        --email admin@example.org \
    ); \
airflow webserver & \
airflow scheduler \ 
'
~~~


## 용어 정리
- mental model
  - 정의된 범위 안에서 특별한 목적을 달성하기 위해 생각과 행동을 다이어그램으로 표현하는 것을 말함



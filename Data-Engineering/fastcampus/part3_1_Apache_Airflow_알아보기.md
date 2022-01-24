## part3-1 Apache Airflow 알아보기
### 워크플로우 관리를 위한 에어플로우
#### Apache Airflow가 무엇일까
- 에어비엔비에서 개발한 워크플로우 스케줄링, 모니터링 플랫폼
- 실제 데이터의 처리가 이루어지는 곳은 아님

#### Apache Airflow
- Airbnb 개발
- 2016년 아파치 재단 incubator program
- 현재 아파치 탑레벨 프로젝트
- Airbnb, Yahoo, Paypal, Intel, Stripe 등 사용

#### 워크플로우 관리 문제
- 매일 10시에 주기적으로 돌아가는 데이터 파이프라인을 만드려면? 
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_14.png)

- 위와 같이 외부 API를 통해 download 하고, Spark Job 을 통해 Process 수행 후 DB에 저장하는 로직이 있다고 하자
- 이를 CRON Script 를 통해 수행시키면 다음과 같은 문제점이 존재
  - 실패 복구 - 언제 어떻게 다시 실행할 것인가? Backfill ? 
  - 모니터링 - 잘 돌아가고 있는지 확인하기가 어려움
  - 의존성 관리 - 데이터 파이프라인간 의존성이 있는 경우 상위 데이터 파이프라인이 잘 돌아가고 있는지 파악이 어려움
  - 확장성 - 중앙화해서 관리하는 툴이 없기 때문에 분산된 환경에서 파이프라인들을 관리하기 힘듬
  - 배포 - 새로운 워크플로우를 배포하기 힘듬

#### airflow가 필요한 이유
- 아래와 같이 이런 파이프라인이 수십개가 있을 때, 이 중 하나가 에러가 발생한다면 기존 cron script로는 찾기가 어려움. 이럴 때 airflow를 사용할 수 있음 
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_15.png)
- Airflow는 워크플로우를 작성하고 스케줄링하고 모니터링하는 작업을 프로그래밍 할 수 있게 해주는 플랫폼
  - 파이썬으로 쉬운 프로그래밍 가능
  - 분산된 환경에서 확장성이 있음
  - 웹 대시보드(UI)
  - 커스터마이징이 가능 

#### Workflow
- 의존성으로 연결된 작업(task) 들의 집합
- DAG(Directed Acyclic graph) --> 방향성이 있고 순환이 없는 그래프를 말함

#### Airflow는 무엇으로 이루어져 있을까
- 웹서버 - 웹 대시보드 UI
- 스케줄러 - 워크플로우가 언제 실행되는지 관리
- Metastore - 메타 데이터 관리
- Executor - 테스크가 어떻게 실행되는지 정의
- Worker - 테스크를 실행하는 프로세스

#### Operator
- Operator는 작업(task)를 정의하는 데 사용
- Action Operators: 실제 연산을 수행
- Transfer Operators: 데이터를 옮김
- Sensor Operators: 테스크를 언제 실행시킬 트리거를 기다림
- Operator를 실행시키면 하나의 Task가 됨
- Task = Operator Instance

#### Airflow 유용성
- 데이터 웨어하우스
- 머신러닝
- 분석
- 실험
- 데이터 인프라 관리

### Airflow 의 구조
- Airflow 의 실행 환경은 크게 2가지로 구분되는데, 하나의 서버에서 실행되는 one-node Architecture 와 분산된 환경에서 실행되는 multi-node Architecture 로 구분됨

#### Airflow one-node Architecture
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_16.png)
- one node Architecture 는 크게 4가지로 구분해 볼 수 있음
  - Web Server
  - Scheduler
  - Meta store
  - Exec 
- meta store 에서 DAG에 대한 정보를 담고 있기 때문에, 이에 대한 정보를 Web Server 와 Scheduler가 정보를 읽어옴
- 읽어온 정보를 기반으로 executor 에서 실제 작업을 수행
- task instance 는 다시 meta store에 상태를 업데이트 함
- 다시 web server 와 scheduler 가 meta store 에 있는 상태를 읽어와서 완료를 확인함
- Executor 에는 queue 가 존재하여 task의 순서를 정하게 됨

#### Airflow multi-node Architecture
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_16_1.png)

- one-node architecture 와 다른 점은 queue 의 위치라고 할 수 있는데, 위의 그림에서 Celery Broker 가 queue 라고 할 수 있음
- 크게 왼쪽에 있는 Airflow UI 와 Scheduler 가 있는 왼쪽 파트, 오른쪽에 worker node 가 있는 파트와 바깥에 queue 와 SQL Store 가 있는 파트 3개로 나누어 볼 수 있음
- Airflow UI 와 Scheduler 가 SQL Store 에 있는 DAG 정보를 읽어와 순차적으로 Celery Broker 인 queue 에 저장하게 되고, 이를 순차적으로 worker node 에 실행시키는 방식
- worker node 에서 완료된 결과를 celery Broker 를 지나 SQL meta-store 에 저장하게 됨
- 완료된 정보를 다시 Airflow UI 와 Scheduler 가 읽어오게 됨

#### Airflow 동작방식
- DAG를 작성하여 Workflow를 만든다. DAG는 Task로 구성되어 있음
- Task는 Operator가 인스턴스화 된 것 
- DAG를 실행시킬 때 Scheduer는 DagRun 오브젝트를 만듬
- DAGRun 오브젝트는 Task Instance를 만듬
- Worker 가 Task 를 수행 후 DagRun 의 상태를 "완료"로 바꿔 놓음 

#### DAG 생성과 실행
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_17.png)

- 유저가 새로운 DAG를 작성 후 Folder DAGs 안에 배치
- Web server 와 Scheduler 가 DAG를 파싱
- Scheduler 가 Metastore 를 통해 DagRun 오브젝트를 생성
- DagRun 은 사용자가 작성한 DAG의 인스턴스  
  DagRun status: Running
- Scheduler 는 Task Instance 를 스케줄링 하며, 이는 DagRun 의 Instance 
- Task Instance를 Executor 로 보냄
- Scheduler 는 DAG 실행이 완료됐나 확인하고, 완료되었으면 DagRun status 를 Completed로 변경
- Meta store 의 정보를 웹서버가 다시 읽어드림

### Airflow 설치
- Airflow 는 flask 기반으로 웹 서버를 구동시킴

~~~shell
pip --version # 버전 확인 3.6 이상 필요
pip install apache-airflow  # apache-airflow 설치

airflow # 정상 실행되는지 확인

# home dir 안에 airflow dir 이 생김
airflow db init  

# initialize 된 DB 를 기반으로 Web server 구동
airflow webserver -p 8080 # p는 port 를 뜻함

# localhost:8080 을 통해 airflow 로그인 화면 확인 !
# 아직 아이디가 없음 -> user 만들기

airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin

# airflow UI 접속 가능
~~~

### Airflow CLI
#### 명령어 확인 및 web server 구동
- `-h` 명령어를 통해 airflow command 에 대해서 알아볼 수 있음
~~~shell
airflow -h  
~~~
- `webserver` 명령어를 통해 airflow UI 서버를 구동시킬 수 있음
- Host 서버를 확인하여, 잡속. Host: 0.0.0.0:8080 이므로, localhost:8080 으로 접속
~~~shell
airflow webserver
~~~

#### 계정 생성
- user-name 과 password 를 만들어야함
~~~shell
airflow users -h  # help 확인

# 다음의 명령어를 사용하여 계정 생성
airflow users create -u admin2 -p admin2 -f Jaehun -l Huh -e admin2@admin.com 
~~~

#### airflow 스케줄러 기동
~~~shell
airflow scheduler 
~~~

#### airflow db
- airflow database(metadata store) 에 기본 파이프라인 생성
- 초기화가 되는 것이기 때문에 조심히 써야 함
~~~shell
airflow db init
~~~

#### airflow dag, task 실행(trigger 실행)
~~~shell
airflow dags list                # 현재 돌아가는 dag 들 출력
airflow tasks list example_xcom  # example_xcom dag 안의 task 확인
airflow dags trigger -e 2022-01-01 example_xcom  # 해당 example_xcom 를 2022-01-01 날짜로 dag 실행
~~~
- 위의 마지막 명령어 수행시, airflow UI 에서 queue 가 생성된 것을 확인 가능  
  이는 UI에서 자유롭게 삭제할 수 있음

### airflow UI
#### airflow 첫 화면에서 로그인 후 메인 화면
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_18.png)

- DAGs 라는 list가 보이며, database 상에 존재하는 list를 출력
- DAGs의 컬럼 별로 기능을 알아보자
  - `Pause/Unpause DAG` : 해당 DAG 을 실행/중지 시키는 기능
  - `DAG` : DAG의 이름, example, example2 라는 tag를 확인  
    프로젝트 별로 tag를 별도로 지정 가능
  - `Owner` : 해당 프로젝트를 누가 관리하는지 확인 가능
  - `Runs` : 현재 실행 중인 DAG의 상태(queued, success, running, failed)
  - `Schedule` : 해당 DAG의 schedule 정보 확인(crontab)  
    crontab.guru 사이트에서 쉽게 crontab 에 대해서 확인 가능 
  - `Last Run` : DAG의 마지막 상태를 확인 가능
  - `Next Run` : 다음 run 이 언제 스케줄링 되는지 확인 가능
  - `Recent Tasks` : 실행된 테스크 들의 상태 확인 가능  
    - up_for_retry : 실패해서 다시 실행 중
    - upstream_failed : 의존성이 있는 상태에서 위에 있는 task가 실패된 것을 의미
  - `Actions` : 지금 바로 실행/삭제 시킬 수 있는 버튼  
    지운다는 의미는 DAG meta 정보 자체를 DB에서 삭제하는 것이 아니라, Instsance 만 삭제
  - `Links` : 여러가지 상세 정보를 확인하기 위한 기능 제공

#### DAG View 확인 화면 - Tree
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_19.png)
- Tree View 가 보이고, 밑에 보면 workflow 확인 가능
- 해당 task 들의 상태 확인 가능  
- refresh를 해보면 현재 진행되고 있는 task 들의 상태를 확인 가능

#### DAG View 확인 화면 - Graph
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_20.png)
- `Graph` View 는 해당 task 들의 의존성을 확인 가능 
- 해당 task 를 클릭하면 modal 창이 뜨는 것을 확인 가능

#### DAG View 확인 화면 - calander
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_21.png)
- 해당 task 들이 날짜 별로 정상적으로 수행이 됐는지 확인 가능

#### DAG View 확인 화면 - Gantt
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_22.png)

- 각각의 task 가 얼마나 task 를 소비했는지 확인 가능  
  bottle neck 구간을 확인 가능
- task 들이 병렬 처리가 정상적으로 됐는지를 확인 가능(같은 시간대에 겹쳐 있을 것임)
- 전체적인 DAG의 시간을 효율화할 수 있게 됨

#### DAG View 확인 화면 - Graph Modal 창 확인
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_23.png)
- 각각의 `Task` 를 `control` 할 수 있음  
  예를 들어, task 가 망가졌을 때, `clear` ,  `run` 을 누르면 재 실행 가능
- `Mark Failed` 는 강제로 실패했다고 표시하고 싶은 경우
- 상단의 `Log` 버튼을 눌러, 해당 task 가 발생하는 로그를 확인 가능

### 용어 정리
- Backfill
  - 우선순위가 높은 작업(top job)의 작업 시작 시간에 방해되지 않는 선에서 후순위 작업을 먼저 실행 시키는 정책 
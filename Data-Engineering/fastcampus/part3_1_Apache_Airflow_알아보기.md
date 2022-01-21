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



### 용어 정리
- Backfill
  - 우선순위가 높은 작업(top job)의 작업 시작 시간에 방해되지 않는 선에서 후순위 작업을 먼저 실행 시키는 정책 
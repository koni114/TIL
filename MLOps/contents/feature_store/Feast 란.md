# Feast 란?

작성일시: November 11, 2022 2:34 PM
최종 편집일시: November 11, 2022 4:30 PM

### Overview

- Feast 는 ML 을 위한 open source feature store 임
- Feast 는 모델 학습 / 온라인 추론을 위하여 분석 데이터를 빠르게 생산하고 관리해줌
- Feast 를 통해 ML Platform 팀은 다음을 수행할 수 있음
    - offline store (model training 을 위한 feature 처리, scale out batch scoring ) / online store (실시간 예측 지원) 을 기반으로 feature 를 관리하여 training / prediction 에 feature 를 관리해줌
    - 현재 시점의 feature 를 generating 함으로써 data leakage 를 방지하여 data scientist 들이 feature engineering 에 집중할 수 있게 함
    → 이렇게 하면 미래의 feature 값 들이 학습에 포함되지 않게 함
    - feature storage 를 추상화하는 single data access layer 를 제공하여 data infrastructure 로 부터 ML 를 분리하고, training model 에서 serving model 로, batch model 에서 realtime model 로의 이식성을 증가시킴

### Feast architecture

![Untitled](Feast%20%E1%84%85%E1%85%A1%E1%86%AB%20a180ae72b7e140f687417830ccdc3f60/Untitled.png)

- Feast 는 real-time model 들을 DevOps 기반으로 productionize 경험이 있는 ML Platform 팀에 적절함
- 또한 Feast 는 data engineer 와 data scientist 간의 협업을 향상시키기 위한 feature platform

### Feast 는 다음의 도구가 아님

- ETL/ ELT system : 데이터 변환 또는 파이프라인 시스템에 목적에는 적합하지 않음
upstream data 변환을 관리하는 용도로는 dbt 가 적절할 수 있음
- a data orchestration tool : 복잡한 workflow DAGs 를 오케스트레이션하는 tool 은 아님
feature value 를 생성하거나 upstream data pipeline 을 관리하는 경우에는 Apache Airflow 와 통합하여 사용
- a data warehouse :  data warehouse 를 대체하는 용도는 아님. 특히 변환된 데이터를 전부 저장하는 용도가 아니며, Feast 는 기존 Data Warehouse 의 데이터를 production 의 모델에 제공할 수 있는 light-weight downstream layer 라고 볼 수 있음
- a database : Feast 는 database 가 아니며, 데이터가 저장된 data store (ex) BigQuery, Snowflake, DynamoDB, Redis) 를 활용하여 feature 를 관리할 수 있게 해줌

### Feast 는 아래 문제들을 완벽하게 해결해 주지 않음

- reproducible model training / model backtesting / experiment management
    - Feast 는 model 또는 metadata 를 capture 해 주지만, data versioning , train, test split  해주지는 않음
    - 위의 기능들은 DVC, MLflow, Kubeflow 가 더 적절할 수 있음
- batch + streaming feature engineering
    - Feast 는 이미 변환된 feature value 를 처리함. 사용자는 일반적으로 Feast 를 upstream system(ex) ETL/ELT Pipeline) 과 통합하여 사용함
    - Tecton 위의 요구사항들을 fully 제공하는 feature platform 임
    - [https://www.tecton.ai/](https://www.tecton.ai/)
- native streaming feature integration
    - Feast 는 사용자가 streamming feature 들을 push 하는 것은 가능하지만, streamming source에서 pull 은 안됨
    - Tecton 은 end to end streaming pipelines 기능을 제공하는 feature platform
- feature sharing
    - Feast 는 feature metadata 를 검색하고 카탈로그화 할 수 있는 feast web UI(alpha) 를 제공함
    - Tecton 은 위의 기능들을 좀 더 robust 하게 제공
- lineage
    - Feast 는 feature value 와 model version 을 연결하는데 도움을 주지만, raw data 와 model version 의 end-to-end lineage 를 모두 capture 해서 연결해주는 솔루션은 아님
    - Feast community 에는 DataHub 나 Amundsen 과 같은 플러그인을 활용해 보완 가능함
    - Tecton 은 feature 변환 뿐만 아니라 end-to-end 를 전부 capturing 해주는 feature platform
- data quality / drift detection
    - Feast 는 data drift 나 data quality 문제를 해결하기 위해 제작된 것은 아님
    - Feast 는 Great Expectation 과 통합되어 있기는 함. 하지만 보다 정교한 데이터 파이프라인, 레이블 및 model version 에 걸쳐 보다 정교한 모니터링이 필요함
    - [https://greatexpectations.io/](https://greatexpectations.io/)

### 용어 정리

- upstream data
    - 로컬 기기에서 서버로 전송되는 데이터를 말함
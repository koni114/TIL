# part1 - ML을 Service화하기 위한 기술 - MLOps 
- MNIST 데이터 분류 중 성능이 가장 좋았던 모델의 정보를 기억하고 있나요?
  - 성능이 첫번째, 두번째, 세번째...
- 학습 환경과 배포 환경은 같지 않음
- 여러명이 함께 협업해야 한다면 어떻게 해야할까?
  - 단순하게 나 혼자 개발해야 한다면, directory를 잘 구성하거나, excel이나 notion을 이용해서 정리할 수 있음
  - 하지만 100, 10000명이 함께 개발하는 AI 프로젝트라면 이는 쉽지 않음
- 컴퓨터를 공유해야 한다면?
  - 데이터가 너무 커서, 또는 많은 양의 GPU를 필요해서, 2~3대의 서버를 공유해야 한다면?

### 빅테크 기업에서 정의한 MLOps
- MLOps는 ML 시스템 개발(Dev)과 ML 시스템 운영(Ops)를 통합하는 것을 목표로하는 ML 엔지니어링 문화 및 방식
- MLOps를 수행하면 통합, 테스트, 출시, 배포, 인프라 관리를 비롯하여 ML 시스템 구성의 모든 단계에서 자동화 및 모니터링을 지원할 수 있음

### MLOps 의 구성요소
- 데이터, 모델, 서빙으로 나눌 수 있음
- 데이터
  - 데이터 수집 파이프라인
    - sqoop, Flume, Kafka, Flink, Spark Streamming, Airflow 
  - 데이터 저장
    - MySQL, Hadoop, Amazon S3, MinIO 
  - 데이터 관리 
    - TFDV, DVC(데이터 버전 관리), Feast(Feature Store), Amundsen(Feature Store)
- 모델
  - 모델 개발
    - Jupyter Hub, Docker, Kubeflow, 
    - (hyper parameter tuning, 병렬 학습) Optuna, Ray, katib 
  - 모델 버전 관리
    - Git, MLflow, Github Action, Jenkins
  - 모델 학습 스케줄링 관리
    - Grafana, Kubernetes
- 서빙 
  - 모델 패키징
    - Docker, Flask, FastAPI, BentoML, Kubeflow, TFServing, seldon-core
  - 서빙 모니터링
    - Prometheus, Grafana, Thanos
  - 파이프라인 매니징
    - Kubeflow, argo workflows, Airflow
- 위의 기능들을 대부분 제공해주고 있는 Saas 가 있음
  - Aws SageMaker
  - GCP Vertex AI
  - Azure Machine Learning
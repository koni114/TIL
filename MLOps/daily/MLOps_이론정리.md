# MLOps 정리

## 머신러닝 프로세스
- 머신러닝 프로세스는 크게 Research와 Production으로 나눌 수 있음

### 머신러닝 프로세스(Research)
- 연구, 테스트 단계를 Research로 정의
- 머신러닝의 큰 프로세스
  - 문제 정의
    - 어떤 문제를 풀 것인가?
    - 어떤 데이터가 필요한가? 
    - 어떤 방식으로 문제를 풀 수 있는가? ex) 이미지 분석, 자연어 처리, 전통적인 ML 사용 등 
  - EDA
    - 데이터에 어떤 컬럼들이 있는가? 
    - 컬럼의 분포들은 어떠한가?
    - Target Value와 어떤 관계가 있는가?  
  - Feature 생성 
  - 모델 학습
  - 예측  
- 특징
  - 보통 자신의 컴퓨터(로컬이라고 표현) 또는 서버에서 실행
  - 고정된(Static, Fixed) 데이터를 사용해 학습

### 머신러닝 프로세스(Production)
- 머신러닝 모델을 실제 서비스화하는 과정을 Production으로 정의
- 실제 환경: Production, Real World
  - 실제 환경의 예시: 모바일 앱 서비스 또는 웹 서비스에서 모델을 사용해 예측하는 경우
- 실제 production 적용시, 고려해야 할 사항
  - 데이터가 안정적으로 들어온다는 생각을 해서는 안됨
  - 모델을 API 형태 등으로 배포해야 함(쉽게 배포, 롤백 가능해야 함)
  - Input Data가 학습할 당시에 동일한 범위 안에 있는지, 동일한 타입으로 들어오는지 확인 필요
  - 새로 배포한 모델의 성능을 지속적으로 확인해야 함  
    ex) Research 단계에서는 좋았던 모델이 Production 환경에서는 더 안좋을 수 있음
  - Research 단계에서 만든 Feature가 사실상 실제 서비스할 경우엔 사용할 수 없을 수 있음  
    - ex) 준 실시간으로 예측해야 하는 모델인데, 날씨 데이터를 API로 받을 수 없는 경우
    - ex) 잘못해서 data leakage 된 모델을 만든 경우 등
- 위의 상황은 머신러닝 전체 프로세스가 머신러닝 모델 개발(development)와 모델 운영(Model Operation)으로 나뉘기 때문
  - 모델 운영시 고려해야 할 부분이 매우 많기 때문
- 이러한 상황을 해결하기 위해 MLOps라는 분야가 생겼고, 계속 발전하고 있음 

### MLOps란? 
- ML + Ops = MLOps
- 머신러닝 모델 개발과 머신러닝 운영 Workflow의 간극을 줄이기 위한 분야
- Model Development와 Model Prediction으로 나누는 관점으로도 볼 수 있음

### 운영해야할 모델이 많아지면 생기는 이슈들 
- 데이터의 복잡도 증가
  - 데이터를 가공하는 workflow가 많음
  - 데이터가 중앙에서 표준화되게 관리되지 않고, 갑자기 수정될 수 있음(기록은 없음)
  - 이런 Flow의 복잡성을 관리하는게 힘들어짐
- 사람마다 선호하는 Framework가 다름
  - Tensorflow, R, Spark, Keras, PyTorch, MXNet 등  
- 모델을 배포하는 Serving은 점점 복잡해짐
  - 환경마다 실행이 달라지고, 라이브러리나 파이썬 버전 등에 민감
  - 모델을 배포한 후, 만약 좋지 않으면 과거 버전으로 롤백하는 과정도 복잡할 수 있음
- 추적이 힘듬
  - 데이터의 문제인지, 모델의 문제인지 추적이 어려움 

### MLOps의 목표
- 머신러닝 모델 개발(ML Dev)과 머신러닝 모델 운영(Ops)에서 사용되는 문제의 반복을 최소화하면서 비즈니스 가치를 창출하는 것
- 모델링에 집중할 수 있도록 안정된 인프라를 만들고 자동으로 운영하는 것
- 빠른 시간에 적은 Risk로 프로덕션까지 진행할 수 있도록 기술적 마찰을 줄이는 것

### MLOps 고려시 중요 사항
- Reproducibility(재현성)
  - Research 단계에서 만든 모델이 Production 환경에도 재현되어야 함
  - 데이터도 유사한 분포를 가져야 함 
- Orchestration(오케스트레이션)
  - 서비스의 자동화된 설정, 관리, 조정 등
  - 만약 예측하려는 요청이 많은 경우 내부적으로 서버를 증설해야 함

### Research ML vs Production ML의 비교
- Research ML
  - 데이터 : 고정(Static)
  - 중요 요소 : 모델 성능(Accuracy, RMSE 등)
  - 도전 과제 : 더 좋은 성능을 내는 모델, ,새로운 구조의 모델
  - 학습 : (데이터는 고정) 모델 구조, 파라미터 개반 재학습
  - 목적 : 논문 출판
  - 표현 : Offline
- Production ML
  - 데이터 : 계속 변함(Dynamic - Shifting)
  - 중요 요소 : 모델 성능, 빠른 Inference 속도, 해석 가능함 등
  - 도전 과제 : 안정적인 운영, 전체 시스템 구조
  - 학습 : 시간의 흐름에 따라 데이터가 변경되어 재학습
  - 목적 : 서비스에서 문제 해결
  - 표현 : Online

### 대표적인 MLOps Component
- Serving
- Experiment, Model Management
- Feature Store
- Data Validation
- Continuous Trainings
- Monitoring 
- GPU Infra Management
- AutoML

## 참고
- 변성윤님 블로그 : https://zzsza.github.io/mlops/2018/12/28/mlops/
  
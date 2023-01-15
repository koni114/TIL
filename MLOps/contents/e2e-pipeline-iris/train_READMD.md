# 학습 파이프라인 탬플릿 작성 가이드
- 아래 가이드는 posml 에서 학습 파이프라인으로 활용하기 위한 학습 파이프라인 탬플릿 다운로드, 작성 방법, 등록을  
위한 가이드임

## 1. 학습 파이프라인 탬플릿 작성 환경 구성
- 학습 파이프라인 탬플릿을 다운로드 및 작성하고자 하는 환경에 다음이 필수 설치되어 있어야 함
```
python >= 3.7 (필수)
git (필수)
```
- 하단 <b>[참고] 학습 파이프라인 탬플릿 작성 예시</b>를 실행하고 싶은 경우, 다음의 파이썬 패키지가 추가 설치되어 있어야 함
```
mlflow >= 2.0.1 
sklearn >= 1.2.0 
pandas >= 1.4.3
impyla >= 0.17.0
workbenchPy 
```

## 2. 학습 파이프라인 탬플릿 다운로드
- 학습 파이프라인 탬플릿을 다운로드 받기 위한 방법은 크게 2가지가 있음 아래 2개의 가이드 중 하나를 선택하여 작성

### 2.1 gitlab URL에 접속하여 직접 다운로드
- ex) [http://192.168.31.81:9091](http://192.168.31.81:9091/) 접속 후 등록된 과제 repository 선택 후 다운로드

### 2.2.  `git clone` 명령어로 다운로드
- terminal 또는 powershell 에서 내가 다운로드 받고자 하는 폴더 또는 디렉토리로 이동 후 아래 명령어를 입력하여 학습 파이프라인 탬플릿을 다운로드
- 이 때 해당 환경에 git 이 설치되어 있어야 함
```shell
$ git clone [Clone with HTTP/Clone with SSH]
```
- 다음은 사용 예시
```shell
# clone with HTTP
$ git clone <http://192.168.31.81:2225/root/e2e-pipeline-iris.git>

# clone with SSH
$ git clone ssh://git@192.168.31.81:2225/root/e2e-pipeline-iris.git
```

## 2. 과제 정보 등록 및 학습 파이프라인 스케줄링 정보 등록
- posml 에 학습 파이프라인 스케줄링 등록을 위하여 `PROJ_NAME/src` 디렉토리 아래에 있는 `config.yaml` 파일 내 과제 정보와 파이프라인 스케줄 정보를 입력해 주어야 함
- 아래 탬플릿은 작성해야 할 `src` 디렉토리 밑에 있는 `config.yaml` 스크립트 원본임
```YAML
# common
proj_name:
model_name:

# Data Management
mart_id:

# workflow management
time_zone:
date_format:

train_start_date:
train_schedule_interval:

train_trigger_start_date:
train_trigger_schedule_interval:

# train management
mlflow:
  target_metric:
```
- <b>만약 local 환경 또는 테스트를 위한 서버에서 실행하는 경우, 시스템 운영자에게 문의 후 아래의 내용을 추가하여 `config.yaml` 파일 작성</b>
```YAML
# train management
mlflow:
  tracking_uri:
  experiment_name: 
  register_model:
```

- 아래와 같은 예시 방법으로 입력하면 되며, 각 config 별 parameter 정보는 하단 상세 내용을 참조
```YAML
# common
proj_name: e2e-pipeline-iris
model_name: e2e-pipeline-iris

# Data Management
mart_id: dm_f_20085_2212_142

# workflow management
time_zone: Asia/Seoul
date_format: "%Y-%m-%d %H:%M:%S"

train_start_date: "2023-01-09 00:00:00"
train_schedule_interval: "@daily"

train_trigger_start_date: "2023-01-09 00:00:00"
train_trigger_schedule_interval: "@daily"

# train management
mlflow:
  target_metric: accuracy_score
```

### [참고] config.yaml parameter 별 입력 정보
**[common]**
- `proj_name`
  - 학습 파이프라인을 등록 할 과제 명
- `model_name`
  - 학습 파이프라인 수행시 생성되는 모델 명
  - 한 과제에 여러 개의 모델일 존재하는 경우, 다음과 같이 입력
```YAML
- model_name:
  - model_name_1: "knn_model_1"
  - model_name_2: "knn_model_2"
  - ...
```
**[Data Management]**
- `mart_id`
  - posml Datamart 를 통해 데이터 파이프라인을 구성하는 경우, posml Data Management 에서 편성한 mart id 명 입력(선택)

**[workflow management]**
- `time_zone`
  - 재학습 파이프라인 스케줄링 설정시 적용되는 time zone 입력
  - 사용가능 한 time zone 확인 필요 시, 아래와 같이 실행하여 확인 가능
```python
import pendulum
print(pendulum.timezones)
```
- `date_format`
  - 학습 파이프라인 및 학습 파이프라인 트리거 시작 시간 입력시 사용할 날짜형 포맷
  - 다음과 같이 문자열 형태로 입력 ex) '%Y-%m-%d %H:%M:%S'
  - 날짜형 포맷 참조 : [https://strftime.org/](https://strftime.org/)
- `train_start_date`
  - 학습 파이프라인의 <b>최초 시작 날짜</b> 입력
  - 날짜 입력시 `date_format` 에 입력한 날짜형 포맷 형태로 입력해야 함
    ex) date_format = "%Y-%m-%d %H:%M:%S" 인 경우, 2023-01-09 00:00:00 로 입력해야 함
- `train_schedule_interval`
  - 학습 파이프라인의 스케줄 간격 입력
  - 위에서 입력한 최초 날짜(`train_start_date`)를 기준으로 특정 간격마다 학습 파이프라인을 수행시키는 경우 입력
  - 학습 파이프라인의 스케줄 간격은 다음 2가지 방식 중 한가지를 선택하여 입력할 수 있음
    - 약어를 사용한 스케줄 간격 입력
      - `@once`: 1번만 실행(특정 간격마다 스케줄 하지 않는 경우)
      - `@hourly`: 매 시간 1회 실행
      - `@daily`: 매일 자정에 1회 실행
      - `@weekly`: 매주 일요일 자정에 1회 실행
      - `@monthly`: 매월 1일 자정에 1회 실행
      - `@yearly`: 매년 1월 1일 자정에 1회 실행
    - cron 기반의 스케줄 간격 설정
      - 복잡한 스케줄 간격 설정을 위해 cron과 동일한 구문을 사용해 스케줄 간격 지정 가능
      - 다음은 간단한 예시 중 하나
        - `0 * * * *` 매 시간(정시에 실행)
        - `0 0 * * *` 매일(자정에 실행)
        - `0 0 * * 0` 매주(일요일 자정에 실행)
        - 다음 사이트에서 cron 문법을 테스트 해볼 수 있음  
          -> [https://crontab.guru/](https://crontab.guru/)
- `train_trigger_start_date`
  - 학습 파이프라인의 호출 트리거의 최초 시작 날짜 입력
  - 날짜 입력시 `date_format` 에 입력한 날짜형 포맷 형태로 입력해야 함
  - ex) date_format = "%Y-%m-%d %H:%M:%S" 인 경우, 2023-01-09 00:00:00 로 입력해야 함
- `train_schedule_interval`
  - 학습 파이프라인 호출 트리거의 스케줄 간격 입력
  - 입력 방법은 `train_schedule_interval` 에 작성된 내용과 동일함

**[train management]**
- 학습 파이프라인 수행시 모델 결과를 확인하기 위한 MLFLow parameter 입력
- `target_metric`
  - 학습 파이프라인 수행시 모델의 성능 측정 기준이되는 metric 입력
  - MLFLow 에서 제공하는 metric 선택. 아래 metric 은 modeling framework(ex) sklearn, pytorch..) 에 관계없이 선택할 수 있는 metric list 임
    - `accuracy_score`
    - `f1_score`
    - `log_loss`
    - `precision_score`
    - `recall_score`
    - `roc_auc`
    - `training_accuracy_score`
    - `training_f1_score`
    - `training_log_loss`
    - `training_precision_score`
    - `training_recall_score`
    - `training_score`
    - `mean_squared_error`
    - `r2_score`
    - model framework 별 상세 metric 내용은 다음의 documentation 참조하여 입력   
      -> [https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html]
      (https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html)

## 3. 학습 파이프라인 탬플릿 작성
- 아래에 작성된 제약 사항들을 준수하여 `src` 디렉토리 안에 학습 파이프라인을 위한 python script 를 자유롭게 작성 가능

### 3.1 학습 파이프라인 작성 필수 사항
<b>[1] `src/train.py` 작성</b>

- `src/train.py` 에 학습 파이프라인 작성. 작성 시 아래와 같은 작성 조건을 지켜주어야 함

[1-1]. `train.py` script 명은 변경되면 안됨
- `train.py` 라는 script 명은 시스템에서 호출되므로, 변경되면 안됨

[1-2]. `SRC_HOME` Path 설정 구문 추가
- 먼저 `train.py` 를 포함하여 <b>`train.py` 에 관여되는 모든 python script 의 상단에는 다음과 같은 구문이 포함되어야 함.</b> 이는 향후에 airflow workflow Job 으로 등록하여 사용하기 위함
```python
import os
import sys

SRC_HOME = os.path.dirname(os.path.realpath(__file__))
if SRC_HOME not in sys.path:
    sys.path.append(SRC_HOME)
```

[1-3]. `if __name__ == "__main__"` 를 통한 메인 함수 호출
- `train` 이라는 함수명은 변경해도 되지만, `train.py` 의 가장 아래 부분에 `if __name__ == "__main__"` 를 통해 학습 파이프라인의 메인 함수가 호출이 되어야 함
- 다음은 `train` 함수를 작성 후 `train.py` script 의 가장 하단에 호출하는 예시 구문임
```python
# train.py
...
if __name__ == "__main__":
    train()
```

## 4. 학습 파이프라인 테스트
- 자신이 속한 위치(local PC, Server 등) 의 terminal 에서 `train.py` 를 실행하여 정상적으로 작동하는 지 확인
```shell
$ python ./src/train.py
```

## 5. 학습 파이프라인 배포
- 테스트 완료 후, 작성한 학습 파이프라인을 gitlab 과제 repository 에 업로드
- 이 때 아래 명령어 수행 위치는 <b>1. 학습 파이프라인 탬플릿 작성 환경 구성</b>시 다운로드 받았던 디렉토리에서 수행
- 과제 신청시 제공 받았던 계정/비밀번호를 입력하여 최종 업로드
```shell
$ git push
```

### [참고] 학습 파이프라인 탬플릿 작성 예시
- 다음은 학습 파이프라인 탬플릿을 작성한 예시.
- iris data 를 기반으로 종(Species) 을 예측하는 KNN 모델을 생성하는 학습 파이프라인을 구성하는 예제.
- 학습 파이프라인 구성을 위한 데이터 추출(`load_data.py`), 데이터 전처리(`preprocess.py`), 모델링(`modeling.py`), 모델 평가(`model_evaluate.py`) 부분을 코드로 작성하고,  
작성된 코드를 최종 `train.py` 에 호출하여 학습 파이프라인 탬플릿을 구성
- 디렉토리 구성은 다음과 같음
```
├── src
  ├── config.py              # user config 구성을 dict object 로 호출하기 위한 script
  ├── config.yaml            # user config 구성
  ├── load_data.py           # 데이터 추출을 위한 script
  ├── preprocess.py          # 데이터 전처리를 위한 script
  ├── modeling.py            # 학습 모델을 위한 script
  ├── model_evaluate.py      # 학습 모델 평가를 위한 script
  ├── train.py               # 학습 파이프라인을 위한 main script
```

### [1] `src/load_data.py` 작성
- posML 에서 제공하는 `workbenchPy` package 내 `GetMartData` 함수를 사용하여 등록된 Data Mart 의 데이터를 로드
- 해당 함수를 실행하려면, workbenchPy package 가 선행으로 설치되어 있어야 함
```python
# load_data.py
import os
import sys

SRC_HOME = os.path.dirname(os.path.realpath(__file__))
if SRC_HOME not in sys.path:
    sys.path.append(SRC_HOME)

import pandas as pd
from config import config as conf
from workbenchPy import GetMartData

def load_data():

    martData = GetMartData(conf['mart_id'])

    x_columns = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    y_columns = ["variety"]

    x = martData[x_columns]
    y = martData[y_columns]

    data = pd.concat([x, y], 1)

    return data
```

### [2] `src/preprocess.py` 작성
- `load_data` 에서 로드한 데이터의 간단한 전처리를 진행
- sklearn 의 `preprocessing` 함수를 활용하여 종속 변수의 label 을 수치형으로 encoding
```python
import os
import sys

SRC_HOME = os.path.dirname(os.path.realpath(__file__))
if SRC_HOME not in sys.path:
    sys.path.append(SRC_HOME)

import pandas as pd
from sklearn import preprocessing

def preprocess(data: pd.DataFrame):

    y_col_name = ["variety"]

    label_encoder = preprocessing.LabelEncoder()
    data[y_col_name] = pd.DataFrame(label_encoder.fit_transform(data[y_col_name]), columns=y_col_name)

    y = data[y_col_name]
    x = data.drop(y_col_name, axis=1)

    return x, y
```

### [3] `src/modeling.py` 작성
- 전처리된 데이터를 기반으로 총 3개의 knn model 생성(k = 3, 4, 5)
- 이 중에서 가장 성능(accuracy_score)이 높은 모델을 선택한 후, MLfLow API 를 활용하여 활용 모델을 MLFlow 에 등록
- MLFlow 에 모델을 등록하는 방법은 다음과 같음
- `import mlflow` 명령어를 통해서 mlflow 라이브러리를 import 함
```python
import mlflow
```
- MLFlow 내 모델을 등록하기 위해 posML system config 에 등록되어 있는 `tracking_uri`, `experiment_name` 을 할당(set)하는 부분이 우선적으로 선언되어 있어야 함  
  해당 정보는 탬플릿 내에서 확인할 수 없으며, 구체적인 정보 확인이 필요하다면 시스템 운영자에게 문의하여 확인 
```python
tracking_uri = conf["mlflow"]["tracking_uri"]
experiment_name = conf["mlflow"]["experiment_name"]
```
- 모델 성능 평가를 위하여 user config 에서 설정하였던 `target_metric` 정보를 가져와 target_metric 변수에 저장
```python
target_metric = conf["mlflow"]["target_metric"]
```
- 학습된 모델을 MLFlow 에 저장하기 위하여 time_format + K의 수를 조합한 모델 학습 수행 명(run_name)을 선언하고,
- `mlflow.sklearn.log_model` API 를 활용하여 모델 저장
```python
run_name = f"sklearn_knn_k_{str(k)}_{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
mlflow.set_tag("mlflow.runName", run_name)
mlflow.sklearn.log_model(sk_model=knn, artifact_path="models")
```
- test dataset 을 통한 모델 평가를 위하여 `mlflow.evaluate` API 를 활용  
  해당 API 활용시, MLFlow 에서 제공하는 다양한 모델 평가 metric 측정 값을 자동으로 제공받을 수 있음 
- 이 때 `mlflow.evaluate` API 의 parameter 로 지정해 주어야 하는 것들은 다음과 같음  
  자세한 내용은 MLFlow API python API documentation 참조 -> https://mlflow.org/docs/latest/python_api/mlflow.html?highlight=mlflow%20evaluate#mlflow.evaluate
  - `models`: mlflow 에 등록된 model 의 uri
  - `data`: 평가하고자 하는 데이터셋
  - `targets`: 평가 데이터셋의 종속변수 컬럼 명
  - `model_type`: 모델 타입(분류, 회귀 등) 
```python
candidate_model_uri = mlflow.get_artifact_uri("models")

result = mlflow.evaluate(
                models=candidate_model_uri,
                data=eval_data,
                targets="variety",
                model_type="classifier"
            )
```
- 최종적으로 3개의 KNN 모델을 MLFlow 에 저장하고, 해당 모델 중 가장 성능이 좋은 모델의 run_id 와 model_uri 를 리턴하는 modeling 함수를 작성한 코드 예제는 다음과 같음
```python
# modeling.py
import os
import sys
from datetime import datetime

SRC_HOME = os.path.dirname(os.path.realpath(__file__))
if SRC_HOME not in sys.path:
    sys.path.append(SRC_HOME)

import mlflow
import pandas as pd
from config import config as conf
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def modeling(x: pd.DataFrame, y: pd.DataFrame):

    tracking_uri = conf["mlflow"]["tracking_uri"]
    experiment_name = conf["mlflow"]["experiment_name"]
    target_metric = conf["mlflow"]["target_metric"]

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2022)

    eval_data = pd.concat([x_test, y_test], axis=1)

    best_model_run_id = ""
    best_model_uri = ""
    best_model_metrics = 0

    k_range = list(range(2, 5))

    # k = 1
    for k in k_range:
        with mlflow.start_run():
            mlflow.autolog()
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(x_train, y_train)

            # save experiment model in mlflow
            run_name = f"sklearn_knn_k_{str(k)}_{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            mlflow.set_tag("mlflow.runName", run_name)
            mlflow.sklearn.log_model(sk_model=knn, artifact_path="models")

            print("Model run: ", mlflow.active_run().info.run_uuid)

            candidate_model_uri = mlflow.get_artifact_uri("models")
            print("candidate_model_uri :", candidate_model_uri)

            # Evaluate the logged model
            result = mlflow.evaluate(
                candidate_model_uri,
                eval_data,
                targets="variety",
                model_type="classifier",
                evaluators=["default"],
            )

            # save best models and metrics
            if best_model_metrics < result.metrics[target_metric]:
                best_model_run_id = mlflow.active_run().info.run_uuid
                best_model_uri = candidate_model_uri
                best_model_metrics = result.metrics[target_metric]

        mlflow.end_run()

    return best_model_run_id, best_model_uri

```

### [4] `src/model_evaluate.py` 작성
- MLFlow 에서 학습 파이프라인 수행시 생성된 모든 모델은 <b>experiment 환경</b>에 저장되며, 이 중 내가 관리하고 싶은 모델은 <b>models</b> 환경에 저장되어 관리됨  
  이는 MLFlow 화면에서 experiment 탭과 models 탭에서 registered_model 을 통해 확인할 수 있음
- `modeling.py` 에서 만들어진 성능이 가장 좋다고 판단된 최종 모델의 run_id 와 uri 를 통해 기존 MLFlow-models 등록되어있는(registered_model) 최신 버전의 모델과의 성능을 최종 비교하여 현재 생성된 모델의 성능이 더 좋은 경우, models 환경에 version 을 update 하여 새로 등록함.
- 만약 models 환경에 등록되어 있는 모델이 하나도 없는 경우는 version 1 로 새로 등록함
- 먼저 MLFlow 에서 models 환경에 등록된 모델(registered_model)을 가져오기 위해 posML system config 에 등록되어 있는 `tracking_uri`, `experiment_name` 을 할당(set)하는 부분이 우선적으로 선언되어 있어야 함
```python
tracking_uri = conf["mlflow"]["tracking_uri"]
experiment_name = conf["mlflow"]["experiment_name"]

 # set mlflow conf
mlflow.set_tracking_uri(tracking_uri)
mlflow.set_experiment(experiment_name)
```  
- modeling.py 에서 등록한 최고 성능의 model의 artifact 를 `mlflow.get_run` MLFlow API 와 `run_id`를 통해 가져옴
```python
candidate_model_artifact = mlflow.get_run(run_id=best_model_run_id)
```
- 가져온 model artifact 를 통해 저장된 모델 성능 metric 값을 가져옴
```python
candi_target_metric_value = candidate_model_artifact.data.metrics[target_metric]
```
- MLFlow 의 models 환경에 등록된 모델(registered model) 을 가져옴
```
mv = client.get_latest_versions(register_model, stages=["None"])
```
- 만약 등록된 모델이 하나도 없는 경우, models 환경에 최초로 등록
```python
if len(mv) < 1:
  desc = "first create register model"
  mv = client.create_model_version(register_model, best_model_uri, best_model_run_id, description=desc)
```
- 등록된 모델이 있는 경우, 모델의 성능 metric 값과 비교하여 현재 모델의 성능이 더 좋은 경우, 새로운 버전으로 등록함
```python
else:
  registered_latest_model_artifact = mlflow.get_run(run_id=mv[0].run_id)
  registered_model_metric_value = registered_latest_model_artifact.data.metrics[target_metric]

  if candi_target_metric_value > registered_model_metric_value:
    # Create a new version of the rfr model under the registered model name
    desc = "A new version of the model"
    client.create_model_version(register_model, best_model_uri, best_model_run_id, description=desc)s
```
- 최종적인 `evaluate.py` 스크립트 코드는 다음과 같음
```python
#!/usr/bin/env python
import os
import sys

SRC_HOME = os.path.dirname(os.path.realpath(__file__))
if SRC_HOME not in sys.path:
    sys.path.append(SRC_HOME)

import mlflow
from config import config as conf
from mlflow import MlflowClient

def model_evaluate(best_model_run_id: str, best_model_uri: str):

    tracking_uri = conf["mlflow"]["tracking_uri"]
    experiment_name = conf["mlflow"]["experiment_name"]
    target_metric = conf["mlflow"]["target_metric"]
    register_model = conf["mlflow"]["register_model"]

    print(f"best_model_uri={best_model_uri}, best_model_run_id={best_model_run_id}")

    # set mlflow conf
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    # get best_model info
    candidate_model_artifact = mlflow.get_run(run_id=best_model_run_id)
    candi_target_metric_value = candidate_model_artifact.data.metrics[target_metric]

    # get latest registered model info
    client = MlflowClient()

    mv = client.get_latest_versions(register_model, stages=["None"])

    # If it is registered for the first time but is not registered as a version, it is registered immediately.
    if len(mv) < 1:
        desc = "first create register model"
        mv = client.create_model_version(register_model, best_model_uri, best_model_run_id, description=desc)
    else:
        registered_latest_model_artifact = mlflow.get_run(run_id=mv[0].run_id)
        registered_model_metric_value = registered_latest_model_artifact.data.metrics[target_metric]

        if candi_target_metric_value > registered_model_metric_value:

            # Create a new version of the rfr model under the registered model name
            desc = "A new version of the model"
            client.create_model_version(register_model, best_model_uri, best_model_run_id, description=desc)
```
### [5] `src/train.py` 작성
- 앞서 작성한 4개의 python script 를 최종 호출하여 실행하는 `train` 함수를 작성하여 탬플릿 작성 완료
```python
#!/usr/bin/env python
import os
import sys

SRC_HOME = os.path.dirname(os.path.realpath(__file__))
if SRC_HOME not in sys.path:
    sys.path.append(SRC_HOME)

from load_data import load_data
from model_evaluate import model_evaluate
from modeling import modeling
from preprocess import preprocess

def train():

    # 1. load data
    data = load_data()

    # 2. data preprocessing
    x, y = preprocess(data=data)

    # 3. modeling
    best_model_run_id, best_model_uri = modeling(x=x, y=y)

    # 4. model evaluate
    model_evaluate(best_model_run_id=best_model_run_id, best_model_uri=best_model_uri)

if __name__ == "__main__":
    train()
```

### [6] `src/train.py` 실행 점검
- 정상적으로 실행되는지 terminal(or powershell)에서 `python train.py` 명령어로 확인
```shell
$ python train.py
```

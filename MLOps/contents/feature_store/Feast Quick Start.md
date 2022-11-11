# Feast Quick Start

작성일시: November 11, 2022 4:30 PM
최종 편집일시: November 11, 2022 8:41 PM

### Feast Tutorial 해보기

- Parquet file 의 offline store 와 Sqlite 의 online store 의 local feature store 를 배포해보기
- Parquet file 로 부터 시계열 feature 들을 사용하여 training dataset 을 Build 해보기
- batch feature 들과 (”materialization”) streaming feature 들을 online store 에 주입해보기
- batch scoring 을 위해 offline store 로부터 가장 최근의 feature store 를 읽어보기
- real-time inference 를 위해 online store 로부터 가장 최근의 feature store 를 읽어보기
- Feast UI 경험해보기

### Step 1 : Install Feast

- feast 설치

```bash
$ pip install feast
```

### **Step 2: Create a feature repository**

```bash
$ feast init feature_repo
$ cd feature_repo
```

```bash
# output
Creating a new Feast repository in /home/user/feature_repo.
```

- repo 생성 후 아래와 같은 demo repo 구조 확인
    - `data/`   : parquet 형식의 raw data 가 들어있음
    - [`example.py`](http://example.py)  : demo feature definition script 가 들어있음
    - `feature_store.yaml`  : data source 관련 config 정보가 들어있는 demo yaml
    
    ```bash
    # feature_store.yaml
    
    project: my_project
    registry: data/registry.db
    provider: local
    online_store:
        path: data/online_store.db
    ```
    
    ```python
    # example.py
    
    from google.protobuf.duration_pb2 import Duration
    
    from feast import Entity, Feature, FeatureView, FileSource, ValueType
    
    # data source 를 load 함.
    # 튜토리얼에서는 parquet file 을 load 하지만, production 에서는 내가 선호하는 DWH 선택할 수 있음
    
    driver_hourly_stats = FileSource(
        path="/content/feature_repo/data/driver_stats.parquet",
        event_timestamp_column="event_timestamp",
        created_timestamp_column="created",
    )
    
    driver = Entity(name="driver_id", 
    								value_type=ValueType.INT64, 
    								description="driver id",)
    
    # Our parquet
    driver_hourly_stats_view = FeatureView(
    		name="driver_hourly_stats",
    		entities=["driver_id"],
    		ttl=Duration(seconds= 86400 * 1),
    		features=[
    			Feature(name="conv_rate", dtype=ValueType.FLOAT),
    			Feature(name="acc_rate", dtype=ValueType.FLOAT),
    			Feature(name="avg_daily_trips", dtype=ValueType.INT64),
    		],
    		online=True,
    		batch_source=driver_hourly_stats,
    		tags={},
    )
    ```
    
    - feature store 의 전반적인 아키텍처를 결정하는 key line 은 **provider** 임
    이는 raw data 의 위치와 online store 내 feature value 를 구체화하는데 사용됨
    - feature_store.yaml 에 provider 값에 유효한 옵션은 다음과 같음
        - `local`: use file source / SQLite
        - `gcp`: use BigQuery / Google Cloud Datastore
        - `aws`: use Redshift / DynamoDB
    - provider 를 customizing 하려면 custom provider 를 제작하여야 함

### **Step 3: Register feature definitions and deploy your feature store**

- `apply`  명령어를 사용하면 현재 디렉토리를 기준으로 정의된 feature view 와 entity 를 python script 에서 scan 하고, object 를 등록하고 인프라스트럭처를 배포함(?)
- 위의 [example.py](http://example.py) 같은 경우는 local 로 셋팅하면  [`example.py`](http://example.py) 를 읽고, SQLite online store table 에 셋업함

### **Step 4: Generating training data**

- model 을 학습하기 위해서, feature 나 label 이 필요함. 종종 label data 와 train data 를 각각 분리해서 저장함
- 사용자는 timestamp 가 있는 label table 을  query 하고 train data 생성을 위한 entity dataframe 으로 Feast 에 전달할 수 있음
- Feast 는 테이블들을 join 하여 관련 feature vector 들을 생성함

```python
from datetime import datetime, timedelta
import pandas as pd

from feast import FeatureStore

# The entity dataframe is the dataframe we want to enrich with feature values
entity_df = pd.DataFrame.from_dict(
    {
        "driver_id": [1001, 1002, 1003],
        "label_driver_reported_satisfaction": [1, 5, 3], 
        "event_timestamp": [
            datetime.now() - timedelta(minutes=11),
            datetime.now() - timedelta(minutes=36),
            datetime.now() - timedelta(minutes=73),
        ],
    }
)

store = FeatureStore(repo_path=".")

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
    ],
).to_df()

print("----- Feature schema -----\n")
print(training_df.info())

print()
print("----- Example features -----\n")
print(training_df.head())
```

```python
# output
----- Feature schema -----

<class 'pandas.core.frame.DataFrame'>
Int64Index: 3 entries, 0 to 2
Data columns (total 6 columns):
 #   Column                              Non-Null Count  Dtype              
---  ------                              --------------  -----              
 0   event_timestamp                     3 non-null      datetime64[ns, UTC]
 1   driver_id                           3 non-null      int64              
 2   label_driver_reported_satisfaction  3 non-null      int64              
 3   conv_rate                           3 non-null      float32            
 4   acc_rate                            3 non-null      float32            
 5   avg_daily_trips                     3 non-null      int32              
dtypes: datetime64[ns, UTC](1), float32(2), int32(1), int64(2)
memory usage: 132.0 bytes
None

----- Example features -----

                   event_timestamp  driver_id  ...  acc_rate  avg_daily_trips
0 2021-08-23 15:12:55.489091+00:00       1003  ...  0.120588              938
1 2021-08-23 15:49:55.489089+00:00       1002  ...  0.504881              635
2 2021-08-23 16:14:55.489075+00:00       1001  ...  0.138416              606

[3 rows x 6 columns]
```

### **Step 6: Fetching feature vectors for inference**

- 추론 할 때, `get_online_features()` 를 사용해서 different driver 를 위하여 최신 feature value 를 빠르게 읽어야 함. 그런 다음 feature vector 를 model 에 제공할 수 있음

```python
from pprint import pprint
from feast import FeatureStore

store = FeatureStore(repo_path=".")

feature_vector = store.get_online_features(
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
    ],
    entity_rows=[
        {"driver_id": 1004},
        {"driver_id": 1005},
    ],
).to_dict()

pprint(feature_vector)
```
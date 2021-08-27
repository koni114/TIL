# 좋은 데이터 로더의 조건
- 데이터의 형식에 따라, 양이 많고 적음에 따라, 사용할 프레임워크에 따라 항상 다르게 만들어 왔는데, 예를 들어 TensorFlow의 경우 빠른 로딩을 위해 tfrecord로 만들어 tf.data를 만들기도 하고 데이터 크기가 작은 경우에는 메모리에 업로드해 접근 하기도 함

## 15억 개의 쇼핑 데이터
- 네이버 쇼핑에서는 카테고리 분류의 경우 2천만 개의 데이터를 사용해서 머신러닝 모델을 학습하고 있음
- 천만건이 넘는 데이터를 처리하기 위해서 HDFS과 같은 분산 데이터베이스 사용
- 학습 데이터도 상당히 큰 용량을 차지하고, 주기적으로 데이터 변경이 일어나기 때문에 hive table 형태 또는 HDFS DB에 저장하고 있음
- '이 데이터를 어떻게 학습 환경에 가지고 올 것인지' 고민하는 것부터 시작됨
- 데이터가 원격 저장소에 보관되어 있기 때문에 그대로 사용하는 것은 네트워크 접근 속도가 병목이 될 확률이 큼. 즉 로컬 머신으로 데이터를 가지고 오는 것을 고려해야 함
- 원격 저장소에 보관되어 있는 데이터의 형식이 h5나 tfreccord 형태가 아니기 때문에 일반적으로 학습에 익숙한 형태로 변환할 것인지 생각해봐야 할 문제
- 예를 들어 10억 개의 데이터에 간단히 transform을 적용해서 새로운 저장 형식으로 만든다고 생각해보면, 적용하는 transform이 1밀리초가 소요되는 작은 작업이라도 30분의 시간이 필요하다는 사실

## Apache Parquet 
- hadoop 에코시스템에서 사용하는 columnar storage임
- Parquet의 디자인 목표는 다음과 같음
  - interperability(상호 운용성)
  - space efficiency
  - query efficiency 

### columnar storage의 의미
- 일반적인 관계형 데이터베이스 테이블에서는 각 행(row)마다 단일 레코드의 필드값이 저장됨
- row based storage는 한 행의 여러 열을 동시에 작업할 때 효율이 극대화됨
- 분석하는 열이 전체의 일부분이라면 row based stoage에서는 불필요한 다른 열까지 읽어야 하므로 비효율적인 연산이 발생
- columnar storage는 row based storage의 단점을 극복하기 위한 방법으로 많이 사용됨
- 다른 열에 영향을 주지 않고 특정 열의 값을 추가/삭제 할 수 있음
- 주로 같은 열에서는 데이터 타입이 동일하게 사용되기 때문에 행 기반일 때와 다른 압축 방식을 사용할 수 있고 공간 효율 또한 향상시킬 수 있는 장점이 있음
- 많은 메타 데이터를 다뤄야 하는 쇼핑의 특성상 columnar storage를 사용하면 데이터 처리 성능에 더 유리할 것임
- columnar 방식만의 장점이 있지만 단점 또한 생각해보아야 함. 10억 개의 상품명 데이터를 하나의 열에 보관해야 한다면 높은 압축률과 접근 용이성은 있지만 너무 큼
- 즉 이러한 경우에는 'Row group'이라는 개념을 통해 데이터를 분리하는 기법을 사용
- parquet에서는 1개의 파일은 n개의 group으로 구성할 수 있음. columnar 기반 스토리지이기 때문에 column 길이가 길면 길수록 빠르다는 것을 기억하면 row group 크기를 조절하는 데 좋은 참고가 될 수 있음
- block size가 128MB 인 경우 row group을 128MB보다 작으면서 가장 근접한 값으로 유지할 때 IO 비용을 최소화 할 수 있음
- 만약 block size가 128MB인데, 이보다 크게 row group size를 지정할 경우, 두 개의 block이 생성되며, 이는 불필요한 IO가 발생되므로 연산의 비효율이 발생할 수 있음
- <b>즉, row group 개수를 지정할 때 block size보다 작게 하는 것이 좋음</b>

### 좋은 데이터 로더의 조건
- 여러 파일로 쪼개져서 저장/읽기 가능
- 간단한 key, value 구조
- lazy data loading(메모리 보호)
- IO 병목을 막기 위한 데이터 캐시
- 데이터에 custom transform을 유연하게 적용 가능

### 여러 파일로 쪼개져서 저장/읽기 가능
- 분산 처리 DB에서는 데이터를 partition 또는 shard로 나누어 저장. 이는 병렬 처리에 유리한 구조이기 때문에 가급적 여러 파일 형태를 그대로 유지하는 것이 중요(repartition에도 비용 발생)
- 또한 data shuffle이 제공되어야 함

### 간단한 key, value 구조
- pandas, Spark, h5의 경우, column과 데이터 타입 조회가 쉬움. threcord는 직렬화되어 있기 때문에 feature key 값과 데이터 타입 조회가 어려움

### lazy data loading(메모리 보호)
- 메모리가 TB급이 아니라면 학습 데이터 전체를 한 서버에 로딩하는 것이 불가능함. 따라서 학습에 필요한 부분만 로드하는 기능이 필요

### IO 병목을 막기 위한 데이터 캐시
- 모든 데이터를 메모리에 로드하고 사용할 수 없기 때문에 반드시 학습 중간에 IO 로딩을 거쳐야 함
- 이 과정에서 IO 로딩 속도 문제로 병목이 발생하므로, IO 로딩 병렬화와 캐시 기능이 제공되어야 함

### 데이터에 custom transform을 유연하게 적용 가능
- 데이터 변형에는 문자열 형식의 label을 정수형인 index로 바꾸는 정적인 변환뿐만 아니라 image augmentation, NLP token masking 같은 동적인 변환도 존재함
- 데이터 로더를 만드는 과정에서 동적 변환이 쉽게 지원되도록 구현해야 함

## 데이터셋과 데이터 로더 관련 기술
- Google: Tensorflow - tfrecord, tf.data API
- Facebook: Pytorch - torch.utils.data API
- Uber: Petastorm
- Nvidia: Dali

### TensorFlow - tfrecord
- TensorFlow를 사용한다면 tfrecord를 사용하는 것이 좋은 방법
- 하지만 다음과 같은 불편한 점도 존재할 수 있음
  - 엄격한 포맷
  - parquet와의 상호 변환 문제 
  - Python object 타입이나 numpy 등을 자유롭게 사용하지 못하고 데이터 열람을 위해 뷰어나 변환 도구를 새로 만들어야 한다는 점이 불편

### Petastorm
- TB급의 parquet을 직접 다룰 수 있는 Petastorm 이라는 오픈소스를 발표함
- Petastorm은 Python 기반의 ML 프레임워크를 모두 지원함
- pure python
- 원격 저장소에서 직접 데이터를 읽어올 수 있도록 PySpark를 지원한다는 점
- Petastorm 시나리오를 보면 PySpark를 통해 읽은 원격 데이터셋을 Petastorm으로 읽어서 petastorm.Dataset으로 처리한 후 TensorFlow나 PyTorch의 dataloader로 변환하는 형태로 구성되어 있는 것을 확인할 수 있음
- 즉 다음과 같은 형태로 사용 가능
  - parquet(HDFS, 로컬)를 PySpark로 읽어서 전처리(column 선택 등)
  - Petastorm-PySpark dataframe 처리
    - PySpark dataframe → 로컬 캐시 디렉터리에 write
    - petastorm.reader 등의 형태로 로드
  - petastorm → pytorch dataloader
    - petastorm.spark.converter → petastorm.pytorch.dataloader : context manager
    - iterator 생성 (iter(petastorm.pytorch.dataloader))
  - batch = next(iter())
- 내부구조
  - ETL은 PySpark를 통해 parquet 파일을 읽고 데이터셋을 생성하는 기능을 제공
  - Unischema를 통해 지정된 data column, 데이터 타입을 Reader를 통해 읽음
  - 이때 Reader에서 사용하는 parquet backend는 PyArrow로 구현되어 있으며 데이터 로딩의 주요 엔진 기능을 수행
  - tf, PyTorch 데이터 로더에 대한 변환 역시 Reader에서 지원

### Petastorm의 특징과 데이터 로더 조건 비교
1. parallel execution strategy 지원
- 단일 프로세스로 아무리 노력해도 IO에서 병목인 상황이라면 학습이 느려지기 때문에 캐시와 더불어 병렬화 기능은 아주 중요
- Petastorm은 2가지 병렬화 실행 전략을 지원
  - thread pool
  - process pool
-  data row가 인코딩되어 있는 고차원 이미지 같은 경우 c++ 기반 패키지를 통해 디코딩할 수 있으므로 thread pool을 사용하는 것이 유리
- row 크기가 작은 데이터이면서 pure Python 코드로 접근해야 하는 경우는 process pool을 사용하는 것이 유리

2. shuffling
- Parquet 파일은 앞서 설명한 것처럼 row group 단위로 사용하기 떄문에 row group 단위로 메모리에 업로드 할 수 있음
- 이 구조를 그대로 사용한다면 같은 row group 내에 포함된 데이터끼리 상관(correlation)이 높아질 가능성이 커짐
- row group 0의 데이터로 학습을 진행한 후 row group 1을 학습하면 row group 0의 학습 정보가 소실될 문제가 생길 수도 있다. 이를 catastrophic forgetting 문제라고 함
- 이 문제를 해결하려면 학습 batch를 구성할 때 다양한 row group에서 샘플을 추출하면 된다. 하지만 row group 전체를 메모리에 로드하는 것이 불가능하므로 해당 기능을 구현하려면 높은 IO 비용을 부담하는 수 밖에 없음
- Petastorm과 tfrecord는 그림과 같은 shuffling 전략을 통해 문제를 해결한다. 전체 row group을 메모리에 업로드할 수 없으므로 row group들 중 일부를 random sampling을 통해 메모리에 캐싱함 
- 캐시된 row group 내에서 random sampling을 통해 모든 데이터가 적절히 추출되도록 조절함

3. local caching
- Petastorm에서는 원격 저장소의 데이터에 접근할 수 있도록 시나리오가 작성되어 있음
- PySpark를 사용해서 원격 저장소 데이터를 직접 사용할 수 있는 인터페이스가 열려있지만 사실 원격 저장소에 직접 접근하는 방법은 네트워크 접근 비용이 로컬 디스크의 IO 접근 비용보다 높기 때문에 학습에 용이한 방법은 아님
- 따라서 Petastorm은 Spark에서 처리된 column 데이터를 로컬 캐시 디렉터리에 저장하는 방법을 지원
- Spark에서 다루는 데이터 역시 columnar data이므로 Spark dataframe을 전처리로 사용하고 학습에 사용할 column data만 추출해서 캐시 디렉터리에 저장하는 방법을 사용
- 데이터는 학습의 1 epoch 때 로딩하는 과정에서 복제되고 2 epoch부터는 로컬 디렉터리에서 로딩이 이루어짐

4. 메모리 캐싱(단점)
- 3번에서 설명한 것처럼 원격 저장소에 있는 데이터를 로컬 디스크에 캐시하는 것도 중요하지만 실제 학습 속도를 빠르게 하기 위해서는 병렬적으로 전처리된 배치 데이터를 메모리에 queue 형식으로 보관하는 것이 중요

5. 사용 편의성(단점)
- Spark가 지원되는 것은 좋지만 Spark에서 데이터를 읽는 시간을 기다려야 한다
  - 300GB 기준 30분 정도 소요. 즉 학습 데이터를 한 번 로딩할 때 30분이 소요
  - 학습 서버에 HDFS 클라이언트와 PySpark를 세팅하는 다소 번거로운 과정을 거쳐야 하는 것도 단점으로 생각할 수 있을 것임
- 메모리 캐시와 멀티 프로세스 병렬 기능에 버그가 있다.

## 좋은 데이터 로더 만들기
- 앞서 각 데이터 로딩 방법이 데이터 로더로서의 기능을 제공하는 것을 확인해 봄
- 데이터 로더의 기능적인 측면이 중요하다는 것과 만들어진 툴에서 해당 기능을 충분히 지원하려는 것도 확인할 수 있었는데, 실질적으로 중요한 부분은 '지원되는 기능이 얼마나 편리하게 제공되는가'이다.
- 가장 먼저 확인해야 할 지표는 동등한 조건에서의 실행 시간이다.

### 순차 로딩에서의 실행 시간 비교
- 비교 조건은 다음과 같음
  - batch_size 100
  - 1000 iteration당 수행 시간 측정
  - 이미지, tokenized text, wordpiece id, label loading

## 출처 
- https://d2.naver.com/helloworld/3773258
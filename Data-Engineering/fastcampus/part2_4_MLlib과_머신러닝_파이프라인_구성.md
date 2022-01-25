## chapter04 Spark ML과 머신러닝 엔지니어링
### MLlib과 머신러닝 파이프라인 구성
- MLlib: Machine Learning Library 
  - ML을 쉽게 확장성 있게 적용하기 위해
  - 머신러닝 파이프라인 개발을 쉽게 하기 위해

#### Spark의 여러 컴포넌트
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_25.png)

- Spark SQL, Spark Streaming, MLlib, graphX 등의 컴포넌트들은 DataFrame API 위에서 돌아가고 있다는 사실을 기억하기

#### MLlib의 여러 컴포넌트
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_26.png)

- 파이프라인의 Persistence 는 모델이나 데이터를 저장하는데 쓰이게 됨

#### MLlib의 주요 컴포넌트
- DataFrame
- Transformer
  - 피처 변환과 학습된 모델을 추상화
  - 모든 Transformer는 `transform()` 함수를 가지고 있음
  - 데이터를 학습이 가능한 포멧으로 바꿈
  - DF를 받아 새로운 DF를 만드는데, 보통 하나 이상의 column을 더하게 됨
  - 예)
    - Data normalization
    - Tokenization
    - 카테고리컬 데이터 숫자로(one-hot encoding)  
- Estimator
  - 모델의 학습 과정을 추상화
  - 모든 Estimator는 `fit()` 함수를 갖고 있음
  - `fit()` 은 DataFrame을 받아 Model을 반환
  - fit을 한다는 것은 모델이 학습을 한다는 것과 비슷
  - 모델은 하나의 Transformer
  - 예)
    - `lr = LinearRegression()`
    - `model = lr.fit(data)`  
- Evaluator 
  - metric 기반으로 모델의 성능 평가
    - 예) Root mean squared error(RMSE)
  - 모델을 여러개 만들어서, 성능을 평가 후 가장 좋은 모델을 뽑는 방식으로 모델 튜닝을 자동화 할 수 있음
  - 예) 
    - BinaryClassificationEvaluator
    - CrossValidator 
- Pipeline
  - ML의 워크플로우
  - 여러 stage를 담고 있음
  - 저장될 수 있음(persist)  

### 첫 파이프라인 구축
- 간단하게 spark reference 에 나와 있는 sample data를 통해 logistic-regression 모델 학습을 수행해 보는 예제
~~~python
# logistic-regression.py
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local').appName("logistic-regression").getOrCreate()

from pyspark.ml.linalg import Vectors
from pyspark.ml.classification import LogisticRegression

training = spark.createDataFrame([
    (1.0, Vectors.dense([0.0, 1.1, 0.1])),
    (0.0, Vectors.dense([2.0, 1.0, -1.0])),
    (0.0, Vectors.dense([2.0, 1.3, 1.0])),
    (1.0, Vectors.dense([0.0, 1.2, -0.5]))], ['label', 'features'])

training.show()

lr = LogisticRegression(maxIter=30, regParam=0.01) # logistic instance 생성
model = lr.fit(training)

# model 평가를 위한 test dataset
test = spark.createDataFrame([
    (1.0, Vectors.dense([-1.0, 1.5, 1.3])),
    (0.0, Vectors.dense([3.0, 2.0, -0.1])),
    (1.0, Vectors.dense([0.0, 2.2, -1.5]))], ["label", "features"])

prediction = model.transform(test)

prediction.show()
~~~
~~~python
# pipeline.py
# MLlib pipeline
from pyspark.sql import SparkSession

spark = SparkSession.builder.master('local').appName("logistic-regression").getOrCreate()

from pyspark.ml.linalg import Vectors
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.feature import HashingTF, Tokenizer   # TF : Term Frequency

training = spark.createDataFrame([
    (0, "a b c d e spark", 1.0),
    (1, "b d", 0.0),
    (2, "spark f g h", 1.0),
    (3, "hadoop mapreduce", 0.0)], ["id", "text", "label"])

# spark 단어를 detect 하는 모델을 만들어 볼 것임
# tokenizer 를 통해 데이터를 토큰화

tokenizer = Tokenizer(inputCol="text", outputCol="words")
hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")

lr = LogisticRegression(maxIter=30, regParam=0.001)

# 파이프라인 생성
pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])

model = pipeline.fit(training)

# test dataset
test = spark.createDataFrame([
    (4, "spark i j k"),
    (5, "l m n"),
    (6, "spark hadoop spark"),
    (7, "apache hadoop")], ["id", "text"])

prediction = model.transform(test)
prediction.show()
~~~

### 추천 알고리즘 - 예제
- ALS: Alternating Least Sqaures
- movie lens 25m dataset라고 검색하여 데이터셋 다운로드
- ml-25m 이라는 directory 자체를 data 안에 넣어두자
- `links.csv`
- `ratings.csv` : 영화를 각각 rating 한 파일
- `movies.csv` : 영화의 이름을 각각 알 수 있는 파일

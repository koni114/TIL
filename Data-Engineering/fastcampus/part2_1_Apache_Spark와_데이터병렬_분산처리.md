## Part2 - Apache Spark와 데이터 병렬 - 분산처리
### 기초 환경 설정
- 필요한 환경 & 패키지
  - 파이썬
  - 주피터 노트북
  - 자바
  - Spark
  - Pyspark
- Anaconda 사이트에서 일괄적으로 설치가 가능

### 모빌리티 데이터 
- TLC Trip Record Data
  - 10+년 이상의 택시와 모딜리티 서비스 기록  
    2009년부터 2021년까지 모든 기록이 공개
- 매년 20GB씩 쌓이는 Dataset   
  승차와 하차 시간과 장소, 소요시간, 택시비와 같이 중요한 데이터를 포함
- 다운로드 URL  
  https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- 2020년도 3월 데이터 중 High Volume For-Hire Vehicle Trip Records (CSV) 데이터를 다운
- 해당 데이터는 Uber 등 대형 택시 운영 기업

#### 데이터 컬럼 확인
- `hvfhs_license_num` : high volume for hire service license
  - HV0002: Juno
  - HV0003: Uber
  - HV0004: Via
  - HV0005: Lyft
  - Uber 와 lyft 회사가 90% 이상임. Juno, via는 minor 함 
- `dispatching_base_num` : 어느 장소에서 dispatch 되는지
- `pickup_datatime` : 승객 승차 시간
- `dropoff_datetime` : 승객 하차 시간
- `PULocationID` : Pick Up Location ID
- `DOLocationID` : Drop off Location ID
- `SR_Flag` : Shared Riding 여부, 1.0 --> Yes, NaN(Not a Number) --> No
- mobility 데이터에 관심이 많은 경우는 Uber Movements Dataset 사용 권장  
  관공서나 연구를 위한 licence가 있음

#### 환경 셋팅
- [github.com/keon](https://github.com/keon/data-engineering) 에는 앞으로 사용할 코드들이 들어가 있음
- 해당 코드를 다운로드 받고, data-engineering 폴더에 data 폴더를 생성하고, 다운로드 받은 파일을 넣으면 됨

### 우버 트립수 세기
- 우버 택시의 일별 트립 수를 세보기
- 01-spark directory 로 이동하여 `count_trips.py` 파일 오픈
~~~python
# 패키지 가져오기
from pyspark import SparkConf, SparkContext
import pandas as pd

# Spark 설정
conf = SparkConf().setMaster("local").setAppName("uber-date-trips")
sc = SparkContext(conf=conf)

# 우리가 가져올 데이터가 있는 파일 디렉토리 지정
directory = "/Users/heojaehun/data-engineering/01-spark/data"
file_name = "fhvhv_tripdata_2020-03.csv"

# 데이터 파싱
lines = sc.textFile(f"file:///{directory}/{filename}")
header = lines.first()
filtered_lines = lines.filter(lambda row: row != header)

# 필요한 부분만 골라내서 세는 부분 -> countByValue 로 같은 날짜 등장하는 부분을 셈
dates = filtered_lines.map(lambda x: x.split(",")[2].split(" ")[0])
result = dates.countByValue()

# 아래는 Spark 코드가 아닌 파이썬 코드 
pd.Series(result, name='trips').to_csv("trips_date.csv")

# CSV File 로 저장
~~~
- 해당 script 를 terminal 에서 `spark-submit` 을 통해 실행할 수 있음
- <b>spark-submit 은 클러스터 매니저에게 작업을 제출하는 코드라고 생각하면 됨</b>
- `localhost:4040` 을 통해 Spark UI 화면에서 작업 내역을 확인할 수 있음
- 저장한 csv file data 를 간단한 plot 으로 확인
~~~python
import pandas as pd 
import matplotlib.pyplot as plt

trips = pd.read_csv("trips_date.csv")
trips.plot()
plt.show()
~~~

### Spark 간단 개요
- Spark 가 빠르다는 것은 쪼개서 In-memory 연산을 하기 때문
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_04.png)

- Spark 는 하나의 cluster 를 이루게 되는데, SpakContext 가 있는 <b>driver program</b> 과, <b>Cluster Manager</b>, <b>Worker Node</b>로 구성
- Driver program 은 쉽게 우리가 코드를 작성하는 컴퓨터라고 생각 할 수 있음(일거리 생산)
- 정의된 Task는 Cluster Manager로 넘어가 일거리를 분배함  
  Hadoop 은 Yarn, AWS 는 Elastic MapReduce 사용 가능
- 내 컴퓨터에서 Spark program 을 돌리면 왜 판다스보다 느릴까?   
  Spark 는 확장성을 고려해서 설계했기 때문

#### 1개의 노드에서 Pandas vs Spark 성능 비교
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_05.png)

- Y축은 소요시간이고, X축은 데이터 크기임
- Spark 는 속도가 느리지만, 계속 연산이 가능함
- 노드를 계속 증가시켜 가면서 확장할 수 있음을 말함
- 빅데이터 환경에서는 Spark가 굉장히 빠름  
  hadoop MapReduce 보다 메모리는 100배, 디스크 상에서는 10배 

#### Lazy Evaluation 
- 태스크를 정의할 때는 연산을 하지 않다가 결과가 필요할 때 연산
- 기다리면서 연산 과정을 최적화 할 수 있음

#### Resilient Distributed Dataset(RDD)
- 여러 분산 노드에 걸쳐서 저장
- 변경이 불가능
- 여러개의 파티션으로 분리

#### Pandas vs Spark
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_06.png)

### Spark는 어떻게 진화하고 있을까
#### Spark 1.0
- 2014년 정식 발표
- RDD를 이용한 인메모리 처리 방식
- DataFrame(V1.3)
- Project Tungsten - 엔진 업그레이드로 메모리와 CPU 효율 최적화

#### Spark 2.0
- 2016년 발표
- 단순화되고 성능 개선
- Structured Streaming
- Dataset 이라는 DataFrame 의 확장형 자료구조 등장
- Catalyst Optimizer 프로젝트 - 언어에 상관없이 동일한 성능 보장  
  - Scala, R, Python, Java 

#### Spark 3.0
- 2020년 발표
- MLlib 기능 추가
- Spark SQL 기능 추가
- Spark 2.4 보다 2배 빨라짐
  - Adaptive execution
  - Dynamic partition pruning
- PySpark 사용성 개선
- 딥러닝 지원 강화
  - GPU 노드 지원
  - 머신러닝 프레임워크와 연계 가능
- GraphX - 분산 그래프 연산
- Python 2 지원 끊김
- 쿠버네티스 지원 강화

#### Spark 구성
- Spark Core
- Spark SQL
- Spark Streaming
- MLlib
- GraphX

### RDD(Resilient Distributed Dataset)
- 탄력적인 분산 데이터셋
- 앞서 코드에서 `lines = sc.textFile(f"file:///{directory}/{filename}")` 에서 lines 가 RDD 객체임
- 다음은 RDD의 5가지 특징

#### 데이터 추상화
- RDD는 데이터를 추상화하는 특징을 가지고 있음  
  데이터는 클러스터에 흩어져있지만 하나의 파일인 것처럼 사용 가능

#### Resilient & immutable
- RDD는 탄력적이고 불변하는 성질이 있음
- 데이터가 여러군데서 연산하는데, 여러 노드중 하나가 망가진다면? 
- 생각보다 많이 일어남
  - 네트워크 장애
  - 하드웨어 / 메모리 문제
  - 알수없는 갖가지 이유 등 
- immutable
  - RDD1이 변환을 거치면 RDD1이 변하는게 아니라 새로운 RDD2가 만들어짐 
  - 즉, RDD의 변환 과정은 하나의 비순환 그래프(Acyclic Graph)로 그릴 수 있게 됨
  - 덕분에 문제가 생길 경우, 쉽게 전 RDD로 돌아갈 수 있음

#### Type safe
- 컴파일시 Type을 판별할 수 있어 문제를 일찍 발견할 수 있음
- Integer RDD, String RDD, Double RDD 등

#### Unstructured / Structured Data
- Structured / Unstructured 둘 다 담을 수 있음

#### Lazy
- 결과를 도출할 때까지 연산을 하지 않음
- Action 을 할 때까지 변환(Transformation)은 실행되지 않음

### 코드 한줄씩 파헤치기
- `count_trips.ipynb` 파일 참조
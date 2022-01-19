## Part 2. Apache Spark와 데이터 병렬-분산 처리
### Unstructured vs Unstructured 
- 다음과 같은 tickers 와 prices 라는 데이터가 있을 때, 미국의 2000$ 이상의 주식만 가져오기 위한 방법은 어떤 것들이 있을까?
~~~python
tickers = sc.parallelize([
    (1, ("Google", "GOOGL", "USA")),
    (2, ("Netflix", "NFLX", "USA")),
    (3, ("Amazon", "AMZN", "USA")),
    (4, ("Tesla", "TSLA", "USA")),
    (5, ("Samsung", "005930", "Korea")),
    (6, ("Kakao", "035720", "Korea"))
])

prices = sc.parallelize([
    (1, (2984, "USD")), (2, (645, "USD")),
    (3, (3518, "USD")), (4, (1222, "USD")),
    (5, (70600, "KRW")), (6, (125000, "KRW"))
])
~~~
- 첫 번째는 inner Join -> Filter by Country -> Filter by Currency
- 두 번째는 Filter by Country -> Filter by Currency -> inner join
~~~python
# CASE 1: join 먼저, filter 나중에
ticker_price = tickers.join(prices)
ticker_price.collect()
filtered_results = ticker_price.filter(lambda x: x[1][0][2] == "USA"
                                                 and x[1][1][0] > 2000).collect()

# CASE 2: filter 먼저, join 나중에
filtered_price = prices.filter(lambda x: x[1][0] > 2000)
filtered_tickers = tickers.filter(lambda x: x[1][2] == "USA")
filtered_tickers.join(filtered_price).collect()
~~~
- 결과적으로 두 번째 방법이 더 좋은데, 항상 개발자들이 이런 것들을 신경써 가면서 개발하기 어려울 수 있음
- <b>데이터가 구조화 되어있다면 자동으로 최적화가 가능</b>

#### 구조화한 데이터란
- Unstructured: free form
  - 로그 파일
  - 이미지 
- Semi Structured: 행과 열
  - CSV
  - JSON
  - XML 
- Structured: 행과 열 + 데이터 타입(스키마)
  - 데이터베이스 

#### Structured Data vs RDDs
- RDD에선
  - 데이터의 구조를 모르기 때문에 데이터를 다루는 것을 개발자에게 의존함
  - Map, flatMap, filter 등을 통해 유저가 만든 function 을 수행
- Structured Data 에선
  - 데이터의 구조를 이미 알고있으므로 어떤 테스크를 수행할것인지 정의만 하면 됨
  - 최적화도 자동으로 할 수 있음

#### 구조화된 데이터를 다루는 Spark SQL
- Spark SQL은 구조화된 데이터를 다를 수 있게 해줌
  - 유저가 일일이 function을 정의한 일 없이 작업 수행 가능
  - 자동으로 연산이 최적화 됨 

### Spark SQL 소개
#### Spark SQL의 목적
- 스파크 프로그래밍 내부에서 관계형 처리를 하기 위해
- 스키마의 정보를 이용해 자동으로 최적화를 하기 위해
- 외부 데이터셋을 사용하기 쉽게 하기 위해

#### Spark SQL 소개
- 스파크 위에 구현된 하나의 패키지
- 3개의 주요 API
  - SQL
  - DataFrame
  - Datasets
- 2개의 백엔드 컴포넌트
  - Catalyst - 쿼리 최적화 엔진
  - Tungsten - 시리얼라이저   

#### DataFrame
- Spark Core에 RDD가 있다면 Spark SQL엔 DataFrame이 있음
- DataFrame은 테이블 데이터셋이라고 보면 됨
- 개념적으로는 RDD에 스키마가 적용된 것이라고 보면 됨

#### SparkSession
- Spark Core에 Spark Context가 있다면 Spark SQL엔 SparkSession이 있음
~~~python
spark = SparkSession.builder.appName("test-app").getOrCreate()
~~~
- RDD에서 스키마를 정의한다음 변형을 하거나 CSV, JSON 등의 데이터를 받아오면 됨

#### RDD로부터 DataFrame 만들기
- Schema를 자동으로 유추해서 DataFrame 만들기
- Schema를 사용자가 정의하기
~~~python
# Schema 를 자동으로 유추해서 DataFrame 만들기
spark = SparkSession.builder.appName("test-app").getOrCreate()

lines = sc.textFile("example.csv")
data = lines.map(lambda x: x.split(","))
preprocessed = data.map(lambda x: Row(name=x[0], price=int(x[1])))

# Infer
df = spark.createDataFrame(preprocessed)

# Schema를 사용자가 정의하기
schema = StructType(
    [StructField("name", StringType(), True),
    StructField("price", StringType(), True)])

spark.createDataFrame(preprocessed, schema).show()
~~~

#### 파일로부터 DataFrame 만들기
~~~python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("test-app").getOrCreate()

df = spark.read.json('dataset/nyt2.json')
df_txt = spark.read.text('text_data.txt')
df_csv = spark.read.csv("csv_data.csv")
df_parquet = spark.read.load("parquet_data.parquet")
~~~

#### createOrReplaceTempView
- DataFrame을 하나의 데이터베이스 테이블처럼 사용하려면 `createOrReplaceTempView()` 함수로 temporary view 를 만들어 주어야함
~~~python
data.createOrReplaceTempView("mobility_data")
spark.sql("SELECT pickup_datetime FROM mobility_data LIMIT 5").show()
~~~

#### Spark 에서 사용할 수 있는 SQL문
- HIVE Query Language와 거의 동일
- Select, From, Where, Count, Having, Group By, Order By, Sort By, Distinct, Join

#### Python에서 Spark SQL 사용하기
- DataFrame 을 RDD로 변환해 사용 가능
- `rdd = df.rdd.map(tuple)`
- (하지만 RDD를 덜 사용하는 쪽이 좋음) 

#### DataFrame 의 이점
- MLLib이나 Spark Streaming 같은 다른 스파크 모듈들과 사용하기 편함
- 개발하기 편하고, 최적화도 알아서 됨

### SQL 기초
~~~python
from pyspark.sql import SparkSession

# spark instance 생성
spark = SparkSession.builder.master('local').appName("learn-sql").getOrCreate()

stocks = [
    ('Google', 'GOOGL', 'USA', 2984, 'USD'),
    ('Netflix', 'NFLX', 'USA', 645, 'USD'),
    ('Amazon', 'AMZN', 'USA', 3518, 'USD'),
    ('Tesla', 'TSLA', 'USA', 1222, 'USD'),
    ('Tencent', '0700', 'Hong Kong', 483, 'HKD'),
    ('Toyota', '7203', 'Japan', 2006, 'JPY'),
    ('Samsung', '005930', 'Korea', 70600, 'KRW'),
    ('Kakao', '035720', 'Korea', 125000, 'KRW'),
]

stockSchema = ["name", "ticker", "country", "price", "currency"]
df = spark.createDataFrame(data=stocks, schema=stockSchema)

# spark 가 내부적으로 어떻게 infer 했는지 확인 가능
print(df.dtypes)

df.show()

df.createOrReplaceTempView("stocks")

spark.sql("select name from stocks").show()
spark.sql("select name, price from stocks").show()
spark.sql("select name, price from stocks where country = 'Korea'").show()
spark.sql("select name, price from stocks where price > 2000").show()
spark.sql("select name, price from stocks where price > 2000 and country = 'USA'").show()

# string condition
spark.sql("select name, price from stocks where country like 'U%'").show()
spark.sql("select name, price from stocks where country like 'U%' and name not like '%e%'").show()
spark.sql("select name, price from stocks where price between 1000 and 10000").show()

spark.sql("select name, price, currency from stocks \
          where currency = 'USD' and \
          price > (select price from stocks where name = 'Tesla')").show()

spark.sql("select name, price from stocks order by length(name)").show()

# Join Example
# 회사가 버는 돈
earnings = [
    ('Google', 27.99, 'USD'),
    ('Netflix', 2.56, 'USD'),
    ('Amazon', 6.12, 'USD'),
    ('Tesla', 1.86, 'USD'),
    ('Tencent', 11.01, 'HKD'),
    ('Toyota', 224.82, 'JPY'),
    ('Samsung', 1780., 'KRW'),
    ('Kakao', 705., 'KRW')
]

from pyspark.sql.types import StringType, FloatType, StructType, StructField

earningSchema = StructType([
    StructField("name", StringType(), True),
    StructField("eps", StringType(), True),
    StructField("currency", StringType(), True),
])

earningsDF = spark.createDataFrame(data=earnings, schema=earningSchema)
earningsDF.createOrReplaceTempView("earnings")

earningsDF.select("*").show()
spark.sql("SELECT * from stocks join earnings on stocks.name = earnings.name").show()

# PER Price / EPS
spark.sql("select stocks.name, (stocks.price / earnings.eps) from stocks join earnings on stocks.name = earnings.name ").show()
~~~

### DataFrames
- DataFrame의 사용법
  - DataFrame의 데이터 타입
  - DataFrame의 가능한 연산들
  - DataFrame에서의 Aggregation 작업들  

#### DataFrame은 관계형 데이터
- DataFrame은 관계형 데이터셋: RDD + Relation
- RDD가 함수형 API를 가졌다면 DataFrame은 선언형 API
- 자동으로 최적화가 가능
- 타입이 없음

#### DataFrame: RDD의 확장판
- 지연 실행(Lazy Execution)
- 분산 저장
- Immutable
- 열 (Row) 객체가 있음
- SQL 쿼리를 실행할 수 있음
- 스키마를 가질 수 있고 이를 통해 성능을 더욱 최적화 시킬 수 있음
- CSV, JSON, Hive 등으로 읽어오거나 변환이 가능

#### DataFrame의 스키마를 확인하는 법
- `dtypes`
- `show()`
  - 테이블 형태로 데이터를 출력
  - 첫 20개의 열만 보여줌
- `printSchema()`
  - 스키마를 트리 형태로 볼 수 있음

#### 복잡한 DataTypes 들 
- ArrayType
- MapType
- StructType(== Object)

#### DataFrame Operations
- Select
- Where
- Limit
- OrderBy
- GroupBy
- Join
~~~python
# select function
df.select("*").collect()
df.select("name", "age").collect()
df.select(df.name, (df.age + 10).alias('age')).collect()

# agg function
df.agg({"age": "max"}).collect()
from pyspark.sql import function as F
df.agg(F.min(df.age)).collect()

# groupBy 
df.groupBy().avg().collect()
sorted(df.groupBy('name').agg({'age': 'mean'}).collect())
sorted(df.groupBy(df.name).avg().collect())
sorted(df.groupBy(['name', df.age]).count().collect())

# join
df.join(df2, 'name').select(df.name, df2.height).collect()
~~~

### Spark SQL 로 트립 수 세기
~~~python
## trip_count_sql
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("trip_count_sql").getOrCreate()

directory = "/Users/heojaehun/data-engineering/01-spark/data/"
file_name = "fhvhv_tripdata_2020-03.csv"

data = spark.read.csv(f"{directory}/{file_name}", inferSchema=True, header=True).cache()
data.show()

# Spark SQL 사용
data.createOrReplaceTempView("mobility_data")
spark.sql("SELECT * FROM mobility_data LIMIT 5").show()

spark.sql("SELECT pickup_datetime from mobility_data").show()

# split function 을 사용 가능
# pickup_date 별 group by로 count 계산
spark.sql("SELECT pickup_date, count(*) FROM (SELECT split(pickup_datetime, ' ')[0] as pickup_date FROM mobility_data) group by pickup_date").show()
~~~

### Spark SQL로 뉴욕의 각 행정구 별 데이터 추출하기
~~~python
## trip_count_sql
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("trip_count_sql").getOrCreate()

directory = "/Users/heojaehun/data-engineering/01-spark/data/"
trip_file = "fhvhv_tripdata_2020-03.csv"
zone_file = "taxi+_zone_lookup.csv"

trip_data = spark.read.csv(f"{directory}/{trip_file}", inferSchema=True, header=True).cache()
zone_data = spark.read.csv(f"{directory}/{zone_file}", inferSchema=True, header=True).cache()

# Spark SQL 사용
trip_data.show()
zone_data.show()

trip_data.createOrReplaceTempView("trip_data")
zone_data.createOrReplaceTempView("zone_data")


spark.sql("SELECT * FROM trip_data LIMIT 5").show()
spark.sql("SELECT * FROM zone_data LIMIT 5").show()

# 멘하탄에서 승차한 승객이 몇 명인지 구해보기
spark.sql("SELECT borough, count(*) as trips FROM (SELECT zone_data.Borough as borough \
          FROM trip_data join zone_data on trip_data.PULocationID = zone_data.locationID) \
          group by borough").show()

spark.sql("SELECT borough, count(*) as trips FROM (SELECT zone_data.Borough as borough \
          FROM trip_data join zone_data on trip_data.DOLocationID = zone_data.locationID) \
          group by borough").show()
~~~

### Catalyst optimizer 및 Tungsten Project 작동원리
- Spark Backend는 Catalyst 와 Tungsten 이라는 두 프로젝트로 최적화 됨

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_10.png)

#### Catalyst 
- SQL과 DataFrame이 구조가 있는 데이터를 다룰 수 있게 해주는 모듈
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_11.png)
- Catalyst 가 하는 일은 Logical Plan 을 Physical Plan 으로 바꾸는 일을 수행

#### Logical Plan
- Logical Plan 은 수행해야하는 모든 transformation 단계에 대한 추상화  
  데이터가 어떻게 변해야 하는지 정의하지만 실제 어디서 어떻게 동작하는지는 정의하지 않음  

#### Physical Plan
- Logical Plan 이 어떻게 클러스터 위에서 실행될지 정의
- 실행 전략을 만들고 Cost Model에 따라 최적화

#### Catalyst 가 하는 일
- Logical Plan을 Physical Plan으로 바꾸는 일
  - 1. 분석: DataFrame 객체의 relation을 계산, 칼럼의 타입과 이름을 확인 
  - 2. Logical Plan 최적화
    - 상수로 표현된 표현식을 Compile Time에 계산(runTime에서 하지 않음)  
      상수로 표현된 표현식은 컴파일 타임에서 미리 계산이 가능하기 때문
    - Predicate Pushdown: join & filter -> filter & join
    - Prejection Pruning: 연산에 필요한 칼럼만 가져오기
  - Physical Plan 만들기: Spark에서 실행 가능한 Plan으로 변환
  - 코드 제너레이션: 최적화된 Physical Plan 을 Java Bytecode 로 변환 
 ![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_12.png)
- Physical plan 은 간단하게 특정 클러스터에서 무슨 일을 수행할지를 정의함


#### Logical Plan 최적화
~~~python
SELECT zone_data.Zone, count(*) AS trips\
FROM trip_data JOIN zone_data \
ON trip_data.PULocationID = zone_data.LocationID \
WHERE trip_data.hvfhs_license_num = 'HV0003' \
GROUP BY zone_data.Zone order by trips desc
~~~
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_13.png)

- 위의 SQL 문을 다음과 같이 logical plan 으로 정의할 수 있는데,  
  왼쪽의 Plan을 오른쪽에 보이는 Plan으로 더 최적화해서 정의할 수 있음


#### Explain
- spark.sql(query).explain(True)
  - Parsed Logical Plan
  - Analyzed Logical Plan
  - Optimized Logical Plan
  - Physical Plan 
~~~python
spark.sql("SELECT zone_data.Zone, count(*) AS trips\
FROM trip_data JOIN zone_data \
ON trip_data.PULocationID = zone_data.LocationID \
WHERE trip_data.hvfhs_license_num = 'HV0003' \
GROUP BY zone_data.Zone order by trips desc").explain(True)
~~~

#### Tungsten
- Physical Plan이 선택되고 나면 분산 환경에서 실행될 Bytecode가 만들어지게 됨
- 이 프로세스를 Code Generation 이라고 부름
- 스파크 엔진의 성능 향상이 목적
  - 메모리 관리 최적화
  - 캐시 활용 연산
  - 코드 생성  

### user define function
~~~python
# user-defined functions
# SQL 문 안에서 쓸 수 있는 함수라고 보면 됨

from pyspark.sql import SparkSession
spark = SparkSession.builder.master('local').appName('udf').getOrCreate()

transactions = [
    ('찹쌀탕수육+짜장2', '2021-11-07 13:20:00', 22000, 'KRW'),
    ('등심탕수육+크립새우+짜장면', '2021-10-24 11:19:00', 21500, 'KRW'),
    ('월남 쌈 2인 세트', '2021-07-25 11:12:40', 42000, 'KRW'),
    ('콩국수+열무비빔국수', '2021-07-10 08:20:00', 21250, 'KRW'),
    ('장어소금+고추장구이', '2021-07-01 05:36:00', 68700, 'KRW'),
    ('족발', '2020-08-19 19:04:00', 32000, 'KRW'),
]

schema = ["name", "datetime", "price", "currency"]

df = spark.createDataFrame(transactions, schema=schema)

df.createOrReplaceTempView("transactions")

spark.sql("SELECT * FROM transactions LIMIT 5").show()

# UDF
def squared(n):
    return n ** 2

# 함수를 register 해야 함.
# 1. 등록하는 방법 1

spark.udf.register("squared", squared)

spark.sql("SELECT price, squared(price) FROM transactions").printSchema()
# root
# |-- price: long (nullable = true)
# |-- squared(price): string (nullable = true)
# 결괏값을 보면 타입이 string 인데, 이는 타입을 지정하지 않으면 string 으로 됨
# 다음과 같이 변경해야 함

from pyspark.sql.types import LongType
spark.udf.register("squared", squared, LongType())
spark.sql("SELECT price, squared(price) FROM transactions").printSchema()

# 2. 등록하는 방법 2
# decorator 를 방법
from pyspark.sql.functions import udf


@udf("long")
def squared(n):
    return n * n


def read_number(n):
    unit = ["", "십", "백", "천", "만"]
    num = "일이삼사오육칠팔구"
    result = []
    i = 0
    while n > 0:
        n, r = divmod(n, 10)
        if r > 0:
            result.append(num[r-1]+unit[i])
        i += 1

    return "".join(reversed(result))


print(read_number(21250))
print(read_number(68700))

spark.udf.register("read_number", read_number)

spark.sql("SELECT price, read_number(price) FROM transactions").show()


def get_weekday(d):
    import calendar
    return calendar.day_name[d.weekday()]


spark.udf.register("get_weekday", get_weekday)

query = """
SELECT 
    datetime,
    get_weekday(TO_DATE(datetime)) as day_of_week
FROM
    transactions
"""
spark.sql(query).show()
~~~
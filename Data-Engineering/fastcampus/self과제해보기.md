## self 과제 해보기
### spark 과제 
1. `restaurant_reviews.csv` 를 활용하여 카테코리(중식, 분식, 일식, 아시안, 패스트푸드) 별 가격 평균을 spark code 로 작성하여 만들어보세요. 다음과 같은 제약 조건을 만족해야 합니다.
  - Spark UI 에서 `category-review-average` 로 검색이 가능해야 합니다.
  - `map`, `mapValues`, `reduceByKey` 를 적절하게 사용하여 속도가 최적화 될 수 있도록 해야합니다.
  - 최종 결과는 `result` 변수에 담아야 하며, `collect` 함수를 통해 출력하세요.

2. 다음의 `tickers` 와 `prices` 데이터를 활용하여 미국의 2000$ 이상 주식을 보유한 기업을 선택하고, 이를 출력하세요
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

3. 다음의 데이터가 있을 때, Spark SQL 을 사용하여 다음의 데이터를 추출해 보세요.
~~~python
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
~~~
- 이름과 주식 보유액. 컬럼 데이터 선택하여 출력
- 가장 높은 주식 보유액을 가진 회사를 출력
- 나라별 평균 주식 값을 출력

4. Spark SQL을 활용하여, 날짜(일별)별 trip 수를 계산해보세요
~~~python
directory = "/Users/heojaehun/data-engineering/01-spark/data/"
file_name = "fhvhv_tripdata_2020-03.csv"
~~~

5. 숫자를 한글로 읽어주는 user define function 을 선언하고 이를 `price` 컬럼에 적용하여 출력해보세요.
- ex) 15,000  -> 만오천
- ex) 175,000 -> 십칠만오천
- ex) 250,000 -> 이십오만 

~~~python
transactions = [
    ('찹쌀탕수육+짜장2', '2021-11-07 13:20:00', 22000, 'KRW'),
    ('등심탕수육+크립새우+짜장면', '2021-10-24 11:19:00', 21500, 'KRW'),
    ('월남 쌈 2인 세트', '2021-07-25 11:12:40', 42000, 'KRW'),
    ('콩국수+열무비빔국수', '2021-07-10 08:20:00', 21250, 'KRW'),
    ('장어소금+고추장구이', '2021-07-01 05:36:00', 68700, 'KRW'),
    ('족발', '2020-08-19 19:04:00', 32000, 'KRW'),
]

schema = ["name", "datetime", "price", "currency"]
~~~

### kafka 과제
1. 2개의 consumer 와 2개의 producer 를 실행시킬 kafka server 를 실행시켜 보세요  
 이 때, 2개의 producer 에서 각각 message 를 post 할 때, 동시 2개의 consumer에 get 되어야 합니다.  
이러한 구조를 만들기 위해서 어떻게 옵션을 처리했으며, 그러한 이유가 무엇인지도 같이 설명해주세요


### spark 과제 해답

4. Spark SQL을 활용하여, 날짜(일별)별 trip 수를 계산해보세요
~~~python
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import Row, StructType, StringType, StructField, IntegerType

directory = "/Users/heojaehun/data-engineering/01-spark/data/"
file_name = "fhvhv_tripdata_2020-03.csv"

spark = SparkSession.builder.master('local').appName('trip-count-sql').getOrCreate()
df = spark.read.csv(f"{directory}/{file_name}", header=True)

df.createOrReplaceTempView("mobility_data")
spark.sql("SELECT * FROM mobility_data LIMIT 5").show()

query = """
    SELECT pickup_date, count(*) 
    FROM (SELECT 
            split(pickup_datetime, ' ')[0] as pickup_date
          FROM
            mobility_data)
    GROUP BY  pickup_date
"""
spark.sql(query).show()
~~~

### kafka 과제 답변
1. 2개의 consumer 와 2개의 producer 를 실행시킬 kafka server 를 실행시켜 보세요  
 이 때, 2개의 producer 에서 각각 message 를 post 할 때, 동시 2개의 consumer에 get 되어야 합니다.  
이러한 구조를 만들기 위해서 어떻게 옵션을 처리했으며, 그러한 이유가 무엇인지도 같이 설명해주세요
- 2개의 consumer 를 동일한 group으로 묶게되면 producer 가 message 를 해당 group 으로 post 했을 때, 하나의 consumer 에만 post 됨  
그 이유는 topic 이 가지고 있는 partition 이 하나만 있기 때문. 이 partition은 반드시 한 개의 consumer 와 매핑되기때문
- 따라서 이를 방지하기 위해 partition이 여러 개여야 함  
  partition 개수가 2인 second-topic 생성
~~~shell
# topic 생성.
# 이 때, partition 의 개수를 2개 이상해야 consumer group 내에 분산 처리됨
 ./bin/kafka-topics.sh --create --topic second-topic --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1
~~~
~~~shell
# producer_1
./bin/kafka-console-producer.sh --topic second-topic --bootstrap-server localhost:9092
~~~
~~~shell
# producer_2 --> producer_1 과 동일
./bin/kafka-console-producer.sh --topic second-topic --bootstrap-server localhost:9092
~~~
~~~shell
# consumer_1
./bin/kafka-console-consumer.sh --topic second-topic --bootstrap-server localhost:9092 --group second-group
~~~
~~~shell
# consumer_2
./bin/kafka-console-consumer.sh --topic second-topic --bootstrap-server localhost:9092 --group second-group
~~~
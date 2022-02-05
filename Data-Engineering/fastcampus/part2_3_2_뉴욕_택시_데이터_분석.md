## 뉴욕 택시 데이터 분석 실습
- 분석 데이터는 구글에서 TLC Trip Record Data 를 검색하여 2021년 1월 부터 7월까지의 Yellow _trip data 사용 
- yellow taxi는 시에서 직접 운영하는 택시 데이터로, 기존 uber data 보다 데이터가 많음 

~~~python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("taxi-analysis").getOrCreate()

# 파일 디렉토리 및 파일 명 지정
trip_files = "/Users/heojaehun/data-engineering/01-spark/data/trips/*"
zone_file = "/Users/heojaehun/data-engineering/01-spark/data/taxi+_zone_lookup.csv"

# 데이터 로딩
trips_df = spark.read.csv(f"file:///{trip_files}", inferSchema=True, header=True)
zone_df = spark.read.csv(f"file:///{zone_file}", inferSchema=True, header=True)

# 데이터 스키마 확인
trips_df.printSchema()
zone_df.printSchema()

# SQL 문으로 가공하기 위하여 Temporary View 에 등록
trips_df.createOrReplaceTempView("trips")
zone_df.createOrReplaceTempView("zone")

# 필요한 컬럼만 추려내기 위하여, JOIN 후 필요한 컬럼 추출
# 승차, 하차 시간 같은 경우는 날짜 / 시간(시, hour) 를 쪼개서 각 컬럼으로 만듬
# 고객이 지불한 금액 컬럼도 유용한 컬럼이므로 선택
query = """
    SELECT 
        t.VendorID as vender_id,
        TO_DATE(t.tpep_pickup_datetime) as pickup_date,
        TO_DATE(t.tpep_dropoff_datetime) as dropoff_date,
        HOUR(t.tpep_pickup_datetime) as pickup_time,
        HOUR(t.tpep_dropoff_datetime) as dropoff_time,
        t.passenger_count,
        t.trip_distance,
        t.fare_amount,
        t.tip_amount,
        t.tolls_amount,
        t.total_amount,
        t.payment_type,
        pz.Zone as pickup_zone,
        dz.Zone as dropoff_zone
    FROM 
        trips t
        LEFT JOIN 
            zone pz
        ON 
            t.PULocationID = pz.LocationID
        LEFT JOIN
            zone dz
        ON  t.DOLocationID = dz.LocationID
"""

comb_df = spark.sql(query)
comb_df.createOrReplaceTempView("comb")

comb_df.printSchema()

# 불필요한 데이터를 선별해 내기 위한 작업 수행
# - 2021년 데이터인데, 해당 년도가 아닌 데이터들은 제거 필요
#  (단, 2020.12.31 은 가능, 2021.01.01 에 하차 했을 수도 있기 때문)

# - 2009년 데이터도 있는 것을 확인 가능
spark.sql("SELECT pickup_date, pickup_time from comb WHERE pickup_date < '2020-12-31'").show()

# total_amount
# describe 함수 사용 시, 해당 컬럼 데이터의 statistics 확인
# min 은 음수가 나오고, max 는 39만 달러 이므로, 상식적으로 말이 안됨.
# --> 따라서 해당 데이터를 나중에 제거 필요
comb_df.select("total_amount").describe().show()

# trip_distance
# max 는 너무 커서 제거가 필요.
comb_df.select("trip_distance").describe().show()

# passenger_count
comb_df.select("passenger_count").describe().show()

# 사람들이 몇 년 몇 월에 탔는지 확인해보기
# 2021-08-01 이후의 데이터와 2020-12-01 이전의 데이터를 제거해 주면 좋다고 판단됨
query = """
    SELECT
        DATE_TRUNC('MM', c.pickup_date) AS month,
        COUNT(*) AS trips
    FROM
        comb c
    GROUP BY
        month
    ORDER BY
        month desc
"""
spark.sql(query).show()

# 데이터 클리닝 진행
query = """
    SELECT
        *
    FROM
        comb c
    WHERE
        c.total_amount < 5000 
        AND c.total_amount > 0
        AND c.trip_distance < 1000
        AND c.passenger_count < 4
        AND c.pickup_date >= '2021-01-01'
        AND c.pickup_date < '2021-08-01'
"""

cleaned_df = spark.sql(query)
cleaned_df.createOrReplaceTempView('cleaned')

# Visualization
# 필요한 package 로딩
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

query = """
SELECT
    c.pickup_date,
    COUNT(*) AS trips
FROM
    cleaned c
GROUP BY
    c.pickup_date
"""
pd_df = spark.sql(query).toPandas() # pandas 로 export

# graph
# 1월 부터 8월까지 택시 이용 수가 늘어나고 있음을 확인
fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(x="pickup_date", y="trips", data=pd_df)

# 요일별 데이터 확인
query = """
SELECT
    DATE_FORMAT(c.pickup_date, 'EEEE') AS day_of_week,
    COUNT(*) AS trips
FROM
    cleaned c
GROUP BY
    day_of_week
"""
pd2_df = spark.sql(query).toPandas() # pandas 로 export
data = pd2_df.groupby("day_of_week").trips.median().to_frame().reset_index()

# 일 -> 월 -> 화 .. 로 정렬을 위하여 preprocessing 수행
data["sort_dow"] = data["day_of_week"].replace({
    "Sunday": 0,
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6
})

data.sort_values(by="sort_dow", inplace=True)

fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(x="day_of_week", y="trips", data=data)


# get_weekday 함수를 직접 만들어 user define function 을 생성.
# 직접 사용해 보는 예제

def get_weekday(d):
    import calendar
    return calendar.day_name[(d.weekday())]


spark.udf.register("get_weekday", get_weekday)

query = """
SELECT
    c.pickup_date,
    get_weekday(c.pickup_date) AS day_of_week,
    COUNT(*) AS trips
FROM
    cleaned c
GROUP BY
    c.pickup_date,
    day_of_week
"""

pd3_df = spark.sql(query).toPandas()  # pandas 로 export

# udf 예제 2.
# payment type 컬럼을 한글로 변경해주는 udf 생성
payment_type_to_string = {
    1: "Credit Card",
    2: "Cash",
    3: "No Charge",
    4: "Dispute",
    5: "Unknown",
    6: "Voided Trip",
}


def parse_payment_type(payment_type):
    return payment_type_to_string[payment_type]


spark.udf.register("parse_payment_type", parse_payment_type)

query = """
SELECT
    parse_payment_type(payment_type),
    count(*) as trips,
    MEAN(fare_amount) as mean_fare_amount,
    STD(fare_amount) AS stdev_fare_amount
FROM
    cleaned
GROUP BY
    payment_type
"""

spark.sql(query).show()
~~~
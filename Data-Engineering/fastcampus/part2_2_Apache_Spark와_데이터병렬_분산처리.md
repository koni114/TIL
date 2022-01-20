## part2 - chapter 02. 병렬처리에서 분산처리까지

### 병렬처리와 분산처리
- Data-Parallel
  - `RDD.map(<task>)` 
  - 데이터를 여러개로 쪼개고, 여러 쓰레드에서 각자 task를 사용
  - 각자 만든 결과값을 합치는 과정 
- Distributed Data-Parallel
  - 데이터를 여러개로 쪼개서 여러 노드로 보냄
  - 여러 노드에서 각자 독립적으로 task를 적용
  - 각자 만든 결과값을 합치는 과정
  - 노드간 통신같이 신경써야될 것이 늘어남  
    Spark를 이용하면 분산된 환경에서도 일반적인 병렬처리를 하듯 코드를 짜는 것이 가능  
    --> RDD 의 데이터 추상화때문
- 그렇다고 Spark 가 알아서 모든 기능을 최적화 시켜주지 않음  
  그 이유는 노드간 통신 때문

### 분산처리와 Latency_1
- 분산처리로 넘어가면서 신경써야될 문제가 많아짐
  - 부분 실패 - 노드 몇개가 프로그램과 상관 없는 이유로 인해 실패
  - 속도 - 많은 네트워크 통신을 필요로 하는 작업은 속도가 저하 
- 예를 들어 두 코드를 비교해 보자
~~~python
RDD.map(A).filter(B).reduceByKey(C).take(100) #- 1
RDD.map(A).reduceByKey(C).filter(B).take(100) #- 2
~~~
- `reduceByKey` 연산은 네트워크 연산이 수행되므로 시간이 오래걸림  
  따라서 1번 코드가 시간이 훨씬 적게 걸림
- 수행 속도는 <b>메모리 > 디스크 > 네트워크 </b> 순으로 진행되며, 네트워크는 메모리 연산에 비해 100만배 정도 느림
- 즉, Spark의 작업 뒷단에서 어떻게 돌아갈지 상상하며 코딩해야 함

### Key-Value RDD
- Key-Value RDD란, (Key, Values) 쌍을 갖기 때문에 Pairs RDD라고도 불림
- Single Value RDD
  - ex) 텍스트에 등장하는 단어 수 세기(날짜)
- Key-Value RDD
  - ex) 넷플릭스 드라마가 받은 평균 별점(날짜, 승객수)
- `pairs = rdd.map(lambda x: (x, 1))`

#### Key-Value RDD
- `reduceByKey()` : 키값을 기준으로 테스크 처리
- `groupByKey()` : 키값을 기준으로 벨류를 묶음
- `sortByKey()` : 키값을 기준으로 정렬
- `keys()` : 키값 추출
- `values()` : 벨류값 추출
~~~python 
pairs = rdd.map(lambda x: (x, 1))
count = pairs.reduceByKey(lambda a, b, : a + b)
~~~

#### Key Value RDD로 할 수 있 는 것들 - JOIN
- `join`
- `rightOuterJoin`
- `leftOuterJoin`
- `subtractByKey`
- Key Value 데이터에서 Key를 바꾸지 않는 경우 map() 대신 value만 다루는 `mapValues()` 함수를 써주자
- Spark 내부에서 파티션을 유지할 수 있어 더욱 효율적
  - `mapValues()`
  - `flatMapValues()`
- Value만 다루는 연산들이지만 RDD에서는 key는 유지됨  

#### reduceByKey 연산 예제
~~~python
# reduceByKey 연산을 사용하여 key 별 평균값 계산하기

from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster('local').setAppName("category-review-average")
sc = SparkContext(conf=conf)

directory = '/Users/heojaehun/data-engineering/01-spark/data'
file_name = 'restaurant_reviews.csv'

# spark 는 action 이 수행되기 전까지는 실제 연산이 수행되지 않음을 기억
lines = sc.textFile(f'file:///{directory}/{file_name}')
lines.collect()  # collect 라는 action 을 수행하여 확인

header = lines.first()
filtered_lines = lines.filter(lambda row: row != header)

def parse(row):
    fields = row.split(",")
    category, reviews = fields[2], int(fields[3])
    return category, reviews


categoryReviews = filtered_lines.map(parse)
categoryReviewsCount = categoryReviews.mapValues(lambda x: (x,  1))


reduced = categoryReviewsCount.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
reduced.collect()

averages = reduced.mapValues(lambda x: x[0] / x[1])
averages.collect()
~~~

### RDD Transformation and Actions
- Spark Operation 은 Transformation 과 Action 으로 나눌 수 있음
- Transformations 는 결과값으로 새로운 RDD를 반환하고 lazy evaluation 연산
- Action 연산은 결괏값을 연산하여 출력하거나 저장하고 eager Execution 연산

#### Action 실습
~~~python
from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster('local').setAppName('transformations_actions')
sc = SparkContext(conf=conf)

# SparkContext 의 config 정보가 모두 알고 싶은 경우, getAll 함수 사용
sc.getConf().getAll()

# SparkContext 를 종료하고 싶은 경우, sc.stop 함수 사용
sc.stop()

# Actions function 알아보기
# RDD 만들어주기
# sc.parallelize 함수는 RDD 를 직접 만들어주는 함수
# parallelize 함수는 list 로 부터 RDD 를 만들어냄
foods = sc.parallelize(['짜장면', '마라탕', '짬뽕', '떡볶이', '쌀국수', '짬뽕',
                        '짜장면', '짜장면', '짜장면', '라면', '우동', '라면'])


# PythonRDD object 로 출력 되는 것을 확인 가능
print(foods)

# 1. collect action
# RDD 안에 있는 value 를 모두 가져다 확인 가능
# but, application 운영 시에는 절대 사용해서는 안됨
foods.collect()

# 2. countByValue action
# RDD 안에 있는 데이터의 각 객체 별 갯수 출력
foods.countByValue()

# 3. take action
# 몇 개의 element 만 뽑아보고 싶은 경우 사용
foods.take(3)

# 4. first action
# 첫 번째 값을 가져오고 싶은경우 사용
foods.first()

# 5. count action
# 데이터의 총 개수를 출력하고 싶은 경우
foods.count()

# 6. distinct action
# unique 한 데이터 개수 출력하고 싶은 경우
foods.distinct().count()

# 7. foreach action
# 해당 액션은 요소를 하나하나씩 꺼내서 함수를 적용하는데 사용
# ** 값을 리턴하지 않음(중요) why? 해당 함수는 worker node 에서 수행되는 함수이기 때문
# 위의 함수들은 driver program 에서 수행되는 함수들이지만, foreach 는 아님
foods.foreach(lambda x: print(x))
~~~

#### Transformations
- transformations 는 크게 narrow 와 wide 로 나뉨
- Narrow Transformation
  - 1:1 변환
  - `filter()`, `map()`, `flatmap()`, `sample()`, `union()`
  - 1열을 조작하기 위해 다른 열/파티션의 데이터를 쓸 수 없음 
  - 정렬이 필요하지 않은 경우 
- Wide Transformation
  - Shuffling
  - Intersection and join, distinct, cartesian, reduceByKey(), groupByKey()
  - 아웃풋 RDD의 파티션에 다른 파티션의 데이터가 들어갈 수 있음

#### transformation code
~~~python

# transformation
sc.parallelize([1, 2, 3]).map(lambda x: x + 2).collect()

#########################
# narrow transformation #
#########################
# 1. flatmap function
# list 의 요소들을 펼쳐서 볼 떄 사용

movies = [
    "그린 북",
    "매트릭스",
    "토이 스토리",
    "캐스트 어웨이",
    "포드 V 페라리",
    "보헤미안 랩소디",
    "백 투 더 퓨처",
    "반지의 제왕",
    "죽은 시인의 사회"
]

moviesRDD = sc.parallelize(movies)
flatMovies = moviesRDD.flatMap(lambda x: x.split(" "))
flatMovies.collect()

# 2. filter function
filterMovies = flatMovies.filter(lambda x: x != "매트릭스")

# 3.union, intersection, subtract function
num1 = sc.parallelize([1, 2, 3, 4])
num2 = sc.parallelize([4, 5, 6, 7, 8, 9, 10])

num1.intersection(num2).collect()
numUnion = num1.union(num2)
num1.subtract(num2).collect()

# 3. sample function
# - first parameter(boolean) : 복원, 비복원 여부
# - second parameter(double) : 샘플 비율
# - third parameter(integer) : seed 값 입력
numUnion.sample(True, .5).collect()
numUnion.sample(True, .3, seed=100).collect()

#######################
# wide transformation #
#######################
foods = sc.parallelize(['짜장면', '마라탕', '짬뽕', '떡볶이', '쌀국수', '짬뽕',
                        '짜장면', '짜장면', '짜장면', '라면', '우동', '라면'])

# 1. groupBy function
foodsGroup = foods.groupBy(lambda x: x[0]) # 첫 번째 값을 기준으로 요소들을 grouping
res = foodsGroup.collect()
for (k, v) in res:
    print(k, list(v))

nums = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
list(nums.groupBy(lambda x: x % 2 == 0).collect()[1][1])
~~~

### Cache & Persist
- 왜 Spark를 설계할 때, Transformation 과 action 으로 나누었을까?  
  - 메모리를 최대한 활용할 수 있음(디스크, 네트워크 연산을 최소화 할 수 있음)  
    지연 연산의 경우 최적화가 가능해짐
  - 데이터를 다루는 task는 반복되는 경우가 많음  
    ex) 머신러닝 학습 
- 반복될 때는 비효율이 발생할 수 있는데, 예를 들어 Task -> Disk -> Task -> Disk 처럼, Disk에 자주 들르게 된다면 비효율이 발생되게됨
- 이를 해결하기 위한 좋은 방법은 Task 에서 다른 Task 로 넘어갈 떄  in-memory 방식으로 주고 받으면 좀 더 좋아짐
- 어떤 데이터를 메모리에 남겨야 할지 알아야 가능한데, transformation 은 지연 실행되기 때문에 메모리에 저장해둘 수 있음
- 데이터를 메모리에 남겨두고 싶을 때 사용할 수 있는 함수로 `Cache()` 와 `Persist()` 함수가 있음
- 이는 데이터를 메모리에 저장해두고 사용이 가능해짐
~~~python
# 예제 1
# categoryReviews 는 result1 과 result2 를 만들면서 2번 만들어짐

categoryReviews = filtered_lines.map(parse)

result1 = categoryReviews.take(10)
result2 = categoryReviews.mapValues(lambda x: (x, 1)).collect()

# 예제 2 
# .persist() 를 추가하여 메모리에 저장해두고 쓸 수 있음
categoryReviews = filtered_lines.map(parse).persist()

result1 = categoryReviews.take(10)
result2 = categoryReviews.mapValues(lambda x: (x, 1)).collect()
~~~
- 또 다른 좋은 예로, Regression 함수의 기울기를 구할 때 사용할 수 있음
~~~python
# gradient 을 계산할 때 마다 point 를 매번 로딩할 필요없이, caching 해서 사용이 가능
points = sc.textFile("...").map(parsePoint)

for i in range(ITERATIONS):
  gradient = points.map(gradient_descent).reduce(lambda x, y : (x + y)) / n)
  w -= gradient * learning_rate
~~~


#### 여러 종류의 Storage Level
- MEMORY_ONLY : 메모리에만 저장
- MEMORY_AND_DISK : 메모리와 디스크 모두 저장하는데, 메모리에 데이터가 없을 경우, 디스크에 저장
- MEMORY_AND_SER : 메모리에만 저장하는데 serialization 수행
- MEMORY_AND_DISK_SER : 메모리나 디스크에 저장하는 과정에서 serialization 수행  
  용량을 아낄 수는 있지만, 메모리나 디스크에서 데이터를 가지고 올 때 deserialization 연산을 수행해야 하기 때문에 약간의 trade-off 가 있음
- Cache vs Persist
  - Cache : default Storage Level 사용
    - RDD: MEMORY ONLY
    - DataFrame: MEMORY_AND_DISK 
  - Persist : Storage Level 을 사용자가 원하는대로 지정 가능 


### Cluster Topology
- Spark는 Master Worker Topology 로 구성
- 즉 항상 데이터가 여러곳에 분산되어 있으며, 같은 연산이여도 여러 노드에 걸쳐 실행된다는 점
- Spark 구조는 다음과 같음

![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_07.png)

- Driver Program 은 SparkContext 가 있으며, 이는 새로운 RDD 를 생성하는 역할 수행
- `textfile`, `parallelize` 같은 함수들은 master driver node 에서 사용되는 것
- 즉 Driver Program 은 개발자나 사용자가 실제 프로그래밍을 통해 사용하는 노드이며, 실제 작업은 worker node에서 수행되게 됨
- driver program 은 실제 작업을 하지는 않지만, 조직하는 역할을 수행
- dirver program 과 worker node 는 cluster manager 를 통해 소통
- driver program 은 transformation 과 action 을 저장해두거나 worker node 에 전달
- worker node 는 내부에 executor가 연산을 수행하고, 데이터를 저장하고, Driver program 에 전송
- worker node 는 Task 를 수행하고, 수행된 결과를 driver program 에 전송하며, 데이터를 저장하기 위해 cache를 두고 있음
~~~python
foods = sc.parallelize(["짜장면", "마라탕", ...])
three = foods.take(3)
~~~
- 위의 코드를 수행하면, 3이라는 값 자체는 driver program 에서 가지고 있고, 실제 take computation은 worker node 에서 일어나게 됨 

### Reduction Operation
- Reduction 은 요소들을 모아서 하나로 합치는 작업을 의미
- 많은 Spark의 연산들이 reduction 연산을 수행

#### 병렬/분산된 환경에서의 reduction 작업
- Action은 어떻게 분산된 환경에서 작동할까?  
- 대부분의 Action 은 Reduction 인데, 여기서 말하는 reduction은 근접하는 요소들을 모아서 하나의 결과로 만드는 일
- 파일 저장, collect() 등과 같이 Reduction 이 아닌 액션도 있음

#### 병렬처리가 가능하려면 ? 
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_08.png)
![img](https://github.com/koni114/TIL/blob/master/Data-Engineering/fastcampus/img/DE_09.png)

- 대표적인 Reduction Actions
  - Reduce
  - Fold
  - Group
  - Aggregate

#### Reduction Operations code - reduce
~~~python
from operator import add
sc.paralleize([1, 2, 3, 4, 5]).reduce(add)

# 아래 코드를 보면, 결괏값이 달라지게 됨
# 분산된 파티션들의 연산과 합치는 부분을 나눠서 생각해야함 ** 중요
# paralleize 함수의 2번째 parameter 는 partition 개수
from operator import add
sc.paralleize([1, 2, 3, 4, 5]).reduce(lambda x,y: (x*2)+y)  # 26
sc.paralleize([1, 2, 3, 4], 1).reduce(lambda x,y: (x*2)+y)  # 26
sc.paralleize([1, 2, 3, 4], 2).reduce(lambda x,y: (x*2)+y)  # 18
sc.paralleize([1, 2, 3, 4], 3).reduce(lambda x,y: (x*2)+y)  # 18
sc.paralleize([1, 2, 3, 4], 3).reduce(lambda x,y: (x*2)+y)  # 26

# (1, 2, 3, 4) --> ((1*2 + 2)*2 + 3)*2 + 4 = 26
# (1,2) (3,4)  --> ((1*2+2)*2 + (3*2)+4) = 18
~~~
- 파티션이 어떻게 나뉠지 프로그래머가 정확하게 알기 어려움
- 연산의 순서와 상관 없이 결과값을 보장하려면 교환법칙과 결합법칙을 고려해서 코딩해야 함

#### Reduction Operations code - Fold
~~~python
# fold 의 첫번째 인자는 시작값을 의미함
# 즉 해당 파티션의 시작 값을 의미함. 
from operator import add
sc.parallelize([1, 2, 3, 4, 5]).fold(0, add) # 0 + 1 + 2 + 3 + 4 + 5 = 15

# 예제 1 reduce vs fold
rdd = sc.parallelize([2, 3, 4], 4)
rdd.reduce(lambda x, y: x*y)
rdd.fold(1, lambda x, y: x*y)

# reduce = (2*3*4) = 24
# fold   = (1*(1*2)*(1*3)*(1*4)) = 24

rdd = sc.parallelize([2, 3, 4], 4)
rdd.reduce(lambda x, y: x+y)
rdd.fold(1, lambda x, y: x+y)

# reduce = (0 + 2 + 3 + 4) = 9
# fold   = (1 + 1) + (1 + 2) + (1 + 3) + (1 + 4) = 14
~~~

#### Reduction Operations code - GroupBy
- RDD.groupBy(<기준 함수>)
~~~python
rdd = sc.parallelize([1, 1, 2, 3, 5, 8])
result = rdd.groupBy(lambda x: x % 2).collect()
sorted([(x, sorted(y)) for (x, y) in result])
#  [(0, [2, 8]), (1, [1, 1, 3, 5])]
~~~

####  Reduction Operations code - Aggregate
- RDD 데이터 타입과 Action 결과 타입이 다를 경우 사용
- 자주 쓰이는 reduction action
- 파티션 단위의 연산 결과를 합치는 과정을 거침
- `RDD.aggregate(zeroValue, seqOp, combOp)`
  - zeroValue: 각 파티션에서 누적할 시작 값
  - seqOp: 각 파티션별 reduction computation 수행 함수
  - combOp: 파티션 각각의 결과를 합치는 함수 
~~~python
seqOp = (lambda x, y: (x[0] + y, x[1] + 1))
combOp = (lambda x, y: (x[0] + y[0], x[1] + y[1]))
sc.parallelize([1, 2, 3, 4]).aggregate((0, 0), seqOp, combOp)

# x[0] = 0, x[1] = 0 (zeroValue)
# x[0] + y = (0 + 1), x[1] + 1 = (0 + 1) -> (1, 1)
# x[0] + y = (1 + 2), x[1] + 1 = (1 + 1) -> (3, 2)

# x[0] = 0, x[1] = 0 (zeroValue)
# x[0] + y = (0 + 3), x[1] + 1 = (0 + 1) -> (3, 1)
# x[0] + y = (3 + 4), x[1] + 1 = (1 + 1) -> (7, 2)
# (10, 4)
~~~

### Key-Value RDD Operations & Joins
- Key-value RDD 에 적용할 수 있는 Transformation & Action function
- Transformations
  - `groupBykey`
  - `reduceByKey`
  - `mapValues`
  - `keys`
  - `join (+ leftOuterJoin, rightOuterJoin)` 
- Actions
  - `countByKey`

#### groupByKey 
- `groupBy` : 주어진 함수를 기준으로 Group
- `groupByKey` : 주어지는 Key를 기준으로 Group

~~~python
# rdd --> a [1, 1], b [1]
rdd = sc.parallelize([("a",  1), ("b",  1), ("a",  1)]) 
sorted(rdd.groupByKey().mapValues(len).collect()) # [('a', 2), ('b', 1)]

x = sc.parallelize([
    ("MATH", 7), ("MATH", 2), ("ENGLISH", 7),
    ("SCIENCE", 7), ("ENGLISH", 4), ("ENGLISH", 9),
    ("MATH", 8), ("MATH", 3), ("ENGLISH", 4),
    ("SCIENCE", 6), ("SCIENCE", 9), ("SCIENCE", 5)], 3)

y = x.groupByKey()
print(y.getNumPartitions())
# 3

# 직접 partition 개수를 지정하고 싶은 경우, parameter 로 지정
y = x.groupByKey(2)
print(y.getNumPartitions())
# 2

for t in y.collect():
    print(t[0], list(t[1]))

# MATH [7, 2, 8, 3]
# ENGLISH [7, 4, 9, 4]
# SCIENCE [7, 6, 9, 5]
~~~

#### reduceByKey
- `reduce` : 주어지는 함수를 기준으로 요소들을 합침(action)
- `reduceByKey`: Key를 기준으로 그룹을 만들고 합침(trans)
~~~python
from operator import add
rdd = sc.parallelize([("a",  1), ("b",  1), ("a",  1)])
sorted(rdd.reduceByKey(add).collect())
~~~
- 개념적으로는 groupByKey + reduction 
- 하지만 groupByKey 보다 훨씬 빠름
~~~python
x = sc.parallelize([
    ("MATH", 7), ("MATH", 2), ("ENGLISH", 7),
    ("SCIENCE", 7), ("ENGLISH", 4), ("ENGLISH", 9),
    ("MATH", 8), ("MATH", 3), ("ENGLISH", 4),
    ("SCIENCE", 6), ("SCIENCE", 9), ("SCIENCE", 5)], 3)

x.reduceByKey(lambda a,b: a+b).collect()
# [('MATH', 20), ('ENGLISH', 24), ('SCIENCE', 27)]
~~~

#### mapValues
- 함수를 value에게만 적용됨
- 파티션과 키는 그대로. 이는 네트워크 cost를 줄일 수 있어 장점을 가지고 있음
~~~python
x = sc.parallelize([("a", ["apple", "banana", "lemon"]), ("b", ["grapes"])])
def f(x): return len(x)
x.mapValues(f).collect()
# [('a', 3), ('b', 1)]
~~~

#### countByKey
- 각 key가 가진 요소들을 셈
~~~python
rdd = sc.parallelize([("a",  1), ("b",  1), ("a",  1)])
sorted(rdd.countByKey().items())
~~~

#### keys
- Transformation
- 모든 Key를 가진 RDD 생성
~~~python
m = sc.parallelize([(1, 2), (3, 4)]).keys()
m.collect()
# [1, 3]
~~~

#### Joins
- Transformation
- 여러개의 RDD를 합치는데 사용
- 대표적으로 두 가지의 Join 방식이 존재  
  - Inner Join(join)
  - Outer Join(left outer, right outer)  
~~~python
rdd1 = sc.parallelize([("foo", 1), ("bar", 2), ("baz", 3)])
rdd2 = sc.parallelize([("foo", 4), ("bar",  5), ("bar", 6), ("zoo", 1)])

rdd1.join(rdd2).collect()
# [('foo', (1, 4)), ('bar', (2, 5)), ('bar', (2, 6))]

rdd1.leftOuterJoin(rdd2).collect()
# [('foo', (1, 4)), ('bar', (2, 5)), ('bar', (2, 6)), ('baz', (3, None))]

rdd1.rightOuterJoin(rdd2).collect()
# [('foo', (1, 4)), ('bar', (2, 5)), ('bar', (2, 6)), ('zoo', (None, 1))]
~~~

### Shuffing & Partitioning
- Shuffing 은 그룹핑시 데이터를 한 노드에서 다른노드로 옮길 때 성능을 많이 저하시킴
- 예를 들어 `groupByKey`를 수행하면 shuffling 이 발생됨
- Shuffling 을 일으킬 수 있는 작업들
  - `Join`, `leftOuterJoin`, `rightOuterJoin` 
  - `GroupByKey`
  - `ReduceByKey`
  - `CombineByKey`
  - `Distinct`
  - `Intersection`
  - `Repartition`
  - `Coalesce`
- Shuffle 은 결과로 나오는 RDD가 원본 RDD의 다른 요소를 참조하거나 다른 RDD를 참조할 때 발생함

#### GroupByKeys + Reduce
- reduce 를 하기전에 GroupBy를 수행함으로 성능 저하가 일어남

#### ReduceByKey
- 각각의 partition 에서 reduce 연산을 수행하고, 이를 groupBy 하게 되면 연산 수행 속도를 최적화 시킬 수 있음

#### Shuffle 최소화 방법
- 미리 파티션을 만들어 두고 캐싱 후 reduceByKey 실행
- 미리 파티션을 만들어 두고 캐싱 후 join 실행 
- 둘다 파티션과 캐싱을 조합해서 최대한 로컬환경에서 연산이 실행되도록 하는 방식
- 셔플을 최소화 해서 10배의 성능 향상이 가능 

#### GroupByKey vs groupByKey code 
~~~python
# reduceByKey
(textRDD
 .flatMap(lambda line: line.split())
 .map(lambda word: (word, 1))
 .reduceByKey(lambda a, b: a + b))

# groupByKey
# --> out-of-memory 등 문제가 발생할 여지가 있음
(textRDD
 .flatMap(lambda line: line.split())
 .map(lambda word: (word, 1))
 .groupByKey()
 .map(lambda (w, counts): (w, sum(counts))))
~~~

#### partition은 어떻게 결정될까? 
- 데이터가 어느 노드/파티션에 들어가는지는 어떻게 결정될까? 
- 데이터를 최대한 균일하게 퍼트리고 쿼리가 같이 되는 데이터를 최대한 옆에 두어 검색 성능을 향상 시키는 것
- partition을 잘하는 것은 일반 RDD에서는 의미가 없음  
  어차피 모든 데이터를 한번 scan 해야하기 때문
- paired-RDD에서 partition 을 잘하게 되는 것이 의미가 있음  
  예를 들어 hash 를 기준으로 partition 을 수행하면 key를 바로 찾을 수도 있음

#### Partition 특징
- RDD는 쪼개져서 여러 파티션에 저장됨
- 하나의 파티션은 하나의 노드(서버)에, 하나의 노드는 여러개의 파티션을 가질 수 있음
- 파티션의 크기와 배치는 자유롭게 설정 가능하며 성능에 큰 영향을 미침
- Key-Value RDD를 사용할 때만 의미가 있음

#### Partition 종류
- Hash Partitioning
  - 데이터를 여러 파티션에 균일하게 분배하는 방식
  - [극단적인 예] 2개의 파티션이 있는 상황에서:
    - 짝수의 key만 있는 데이터셋에 Hash 함수가 (x % 2) 라면?
    - 한쪽 파티션만 사용하게 될 것  
      Partition 1: [2, 4, 6, 8, 10, ...]
      Partition 2: []
  - dictionary와 매우 비슷
- Range Partitioning
  - 순서가 있는, 정렬된 파티셔닝
  - 키의 순서, 키의 집합의 순서에 따라 파티셔닝이 수행됨
  - 서비스의 쿼리 패턴이 날짜 위주면 일별 Range Partition 고려 

#### Memory & Disk Partition
- 디스크에서 파티션하기 
  - `partitionBy()` (trans)
- 메모리에서 파티션하기
  - `repartition()`
  - `coalesce()`
- 보통은 partitionBy를 많이 사용하게 될 것임

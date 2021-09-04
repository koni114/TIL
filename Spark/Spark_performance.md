## Spark 성능비교 정리
### 복잡한 쿼리 수행 후 DataFrame 생성 vs 간단한 쿼리를 통해 DataFrame 생성 후 filter, select를 통한 정제
- RDBMS(Oracle, MySQL, postgreSQL...)
  - spark는 RDBMS에서 데이터를 가져올 때 느림. 네트워크를 통해 최소의 데이터양으로 전송하는 것이 좋으므로, 복잡한 쿼리를 통해 최대한의 데이터를 fitlering 하는 것이 중요
- RedShift, snowflake
  - 쿼리를 클러스터 자체로 push down 하거나 , JDBC를 사용하여 데이터를 읽으려는 경우가 더 빠름
- file
  - 마찬가지로 cluster가 최소한의 작업을 수행할 수 있도록 push down 해야 함
- <b>결과적으로, spark 작업을 더 빠르게 하기 위해서는 source의 filter를 push down 해야 함</b>

### groupByKey vs reduceByKey
- 반드시 `reduceByKey`를 사용해야 함. spark에서 사실 가장 기피해야할 연산은 node 간의 random shuffling인데, `groupByKey`는 data shuffling이 모든 노드 사이에서 발생함
- `reduceBykey`도 마찬가지로 shuffling은 일어나지만, 두 함수의 가장 큰 차이점은 reduceByKey는 shuffle 하기 전에 먼저 reduce 연산을 수행해 네트워크를 타는 데이터를 현저하게 줄여줌

### Partitioning 전략
- 분산 클러스터링 기반 병렬 처리에서 중요한 것 중에 하나는 여러개의 executor node에 데이터가 고르게 분산되게 하는 것이 중요함
- 잘 쪼개지지 않는 데이터를 가지고 분산 처리를 수행하면, 한 노드에만 일이 몰리는 현상이 발생할 수도 있음(<b>이를 skew 되었다고 함</b>)
- `repartition`이나 `coalesce` 함수를 통해 repartition 할 수 있지만, 프로그래머가 통제할 수 없는 상황도 있음
- join과 같은 연산에서는 spark의 설정값인 `spark.sql.shuffle.partitions` 값으로 partition 개수가 정해짐. 따라서 해당 설정 값을 적절히 조절해주는 것으로 적당한 partition 개수를 유지할 수 있음

### coalesce vs repartition
- `coalesce`를 주로 사용하는 것이 좋음. `repartition`은 data의 shuffling이 일어나는 반면, `coalesce`는 partition 개수를 늘릴 수는 없지만, shuffling이 일어나지 않기 때문에 더 좋음

### local collection vs 분산처리
- 개발환경에서는 차이가 안날 수 있지만, 분산 환경에서는 collection 수행시, driver 노드에 데이터가 수집되어, out of memory 현상 등이 발생할 수 있어 주의해야 함

### dataFrame load 속도 향상
- csv --> parquet으로 변환하여 저장하면, dataFrame load 속도를 3~4배 향상 가능

### dataframe을 list 변환 속도 향상
- `df.collect()` --> `df.head(n)` 으로 변경시 변환 속도 향상

### executor core 할당 수
- `spark.executor.cores` --> 4 ~ 6
- 노드 별 여유 코어를 남기는 것이 좋음
- 코어를 5개 이하로 하는 것이 최적
- 테스트를 해보면 6개가 더 빠르긴 함

### executor 할당 메모리
- `spark.executor.memory` --> 16G ~ 24G
- 코어에 비례해서 메모리 설정
- 메모리 또한 여유 메모리를 남기는 것이 좋음

### 분산병렬처리를 위한 Task
- `spark.default.parallelism` --> 60
- 서버 코어 개수 * 2~3 설정 예시) 20(코어 수) * 3 = 60

### 데이터 저장/통신을 위한 serialization library 설정
- `spark.serializer org.apache.spark.serializer.KryoSerializer`
- 빠른 성능을 제공하는 Serialization library

### serialization library read/write max buffer 사이즈
- `spark.kryoserializer.buffer.max` --> 1024

### spark dataFrame <-> pandas dataFrame
- `spark.sql.execution.arrow.enabled` -> true
- 1G 파일 기준시, 20배 성능 향상 효과  

### File Format 최적화
- Parquet, ORC와 같은 columnar file 활용
- splittable file format(snappy, bzip2와 같은 compression format)
- 너무 많은 small file은 compaction 하자

### Parallelism
- 데이터 사이즈에 맞춘 스파크 파티션 생성
- 너무 적은 파티션 수는 executor를 idle하게 만들며, Executor out of memory 발생 우려가 있음
- 반대로 너무 많은 파티션은 task scheduling overhead, meta 정보의 과다로 성능이 떨어질 수 있음
- Executor 최소한 2~3개 이상의 코어를 할당해야 함
- `spark.sql.shuffle.partitions` 기본값 200은 빅데이터 프로덕션 환경에서는 너무 적을 수 있음. 따라서 기본적으로 튜닝이 필요

### Shuffle 줄이기
- shuffle은 네트워크와 disk I/O를 포함하는 노드간 데이터 이동을 불러일으키는 가장 비싼 연산
- 즉, <b>shuffle을 줄이는 것이 튜닝의 시작</b>
  - `spark.sql.shuffle.partitions` 을 튜닝하자
  - 각 task 사이즈가 너무 적지 않도록 input data를 파티셔닝함
  - 일반적으로 파티션당 100MB에서 200MB를 타겟팅 함 

### Filter/Reduce dataSet size
- partition된 데이터를 활용함
- 최대한 이른 stage에서 데이터를 Filter out함

### 적절한 cache의 사용
- pipeline에서 여러번 계산이 필요한 df에서 활용
- unpersist를 하자

### Join
- BroadcastHashJoin을 최대한 활용. 가장 성능이 빠른 Join

### Cluster Resource Tuning
- spark.driver.memory, executor-memory, num-executors, and executor-cores 튜닝

### 하드워에 Spec에 대한 이해
- Core count & speed
- Memory Per Core(메모리당 코어가 얼마나 되는가)
- Local disk type, count, size, speed
- network speed, topology
- cost / core / hour

### action 수행이 효과적인지 확인 필요
- Long Stages, Spills, Laggard Tasks
  - duration으로 sorting해서 가장 오래 돌고 있는 Stage를 파악하는 것부터 시작할 수 있음
  - disk spill(메모리에 공간이 없어 disk로 누수가 일어나는 현상)이 심하게 일어나고 있는 Stage인 경우를 찾음. 보통 가장 오래 도는 Job과 동일한 경우가 많음
- CPU Utilization
  - Ganglia / Yarn  
    CPU 활용률이 너무 낮다면, CPU 활용률이 70% 내외로 활용될 수 있도록 타겟으로 잡아볼 수 있음
   
### 데이터 스캔 최소화
- 간단하지만 가장 중요한 최적화 기법  
  lazy loading - 데이터 파티셔닝을 최대한 필터하고 로딩해서 사용
- Hive Partition  
  Partition pruning을 통한 스캔 대상 데이터 최소화(기본 default 값 True)


### Spark Paritions - Input/Shuffle/Output
- Spark Partition을 컨트롤하는 두 가지 핵심
- Spill을 피하도록 함
- 최대한의 Core를 활용할 수 있도록 함. 데이터의 Input 단계부터 Shuffle 단계, Output 단계로 나눠서 알아보자

#### Input
- Size를 컨트롤하자
  - `spark.sql.file.maxPartitionBytes` default value: 128MB
  - Increase Parallelism : 코어의 활용률을 병렬도를 더 올리기 위해 쪼개서 읽을 수 있음
- 예를들어 shuffle 이 없는 map job이라면 오직 read/write 속도에만 dependant한 task인데, 더 빠르게 처리하기 위해 maxPartitionSize를 core 수에 맞게 처리하면 속도를 크게 개선할 수 있음  
더 많은 코어가 나누어서 처리했기 때문 
- Heavily Nested/Repetitive Data 인 경우 메모리에서 풀어 냈을 때, 데이터가 커질 수 있으므로 더 작게 읽는 것이 필요할 수 있음
- Generating Data - Explode : 이 역시 새로운 데이터 컬럼을 만들면서 데이터가 메모리 상에서 커질 수 있음
- Source Structure is not optimal(upstream)
- UDFs

#### Shuffle
- Count를 컨트롤하자
- `spark.sql.shuffle.partitions` default value : 200
- 가장 큰 셔플 스테이지의 타겟 사이즈를 파티션당 200MB 이하로 잡는 것이 적절함  
  (target size <= 200 MB/partition)
- ex) shuffle Stage Input = 210GB  
  210000MB / 200MB = 1050 -> `spark.conf.set("sparks.sql.shuffle.partitions", 1050)`
- 하지만 만약 클러스터의 가용 코어가 2000 이라면 다 활용하면 더 좋음  
  -> `spark.conf.set("spark.sql.shuffle.partitions", 2000)`

### Output
- Count를 컨트롤하자
- coalesce(n) : 2000개의 partition이 Shuffle 하고 나서, write할 때 100개가 나눠서 할 수 있도록 
- Repartition(n) : partition을 증가시킬 때 사용. shuffle을 발생시키므로 곡 필요한 경우가 아니면 사용 X
- ex) 전체 160GB의 파일을 처리하는데 10개의 코어가 1.6GB를 처리할 때와 100개의 코어가 처리할 때의 차이는 아주 큼

### Skew Join Optimization
- 어떤 파티션이 다른 파티션보다 훨씬 큰 경우  
  ex) 어떤 키 하나에는 수백만개의 count가 몰려있고, 나머지 키에는 수십개 정도씩만 있다고 하자
  Salting 이라는 방법을 통해 해결해 볼 수 있음(노이즈 데이터를 뿌려넣는다는 의미)
- 0 부터 spark.sql.shuffle.partitions -1 사이의 random int를 가진 column을 양쪽 데이터에 생성
- Join 조건에 새로운 salting column을 포함함
- result 표출 시 salting column을 drop함

~~~scala
df.groupBy('city', 'state').agg(fuc).orderBy(co.desc)
val saltVal = random(0, spark.conf.get(org...shuffle.partitions) - 1)
df.withColumn("salt", lit(saltVal))
  .groupBy("city", "state", "salt")
  .agg(func)
  .drop("salt")
  .orderBy(col.desc)
~~~
- Spark3.0 부터는 join시 동적으로 splitting-replicating 등의 작업을 통해 재분배하는 조건이 생김
  - `spark.sql.adaptive.skewJoin.enabled` : default: true
  - `spark.sql.adaptive.skewJoin.skewedPartitionFactor` default: 10
  - `spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes` : default 256MB 

### Minimize Data Scans(Persistence)
- 반복 작업이 있는 경우에 `persist()` 사용
- 기본 `df.cache == df.persist(StorageLevel.MEMORY_AND_DISK)`
- 다른 타입들의 장단점에 대해서도 알아보자  
  - Default StorageLevel.MEMORY_AND_DISK  
    (deserialized)
  - deserialized = Faster = Bigger
  - serialized = Slower = Smaller
- `df.unpersist`를 잊지 말자 
  - cache memory 를 사용하는 만큼 working memory 가 줄어들 것임 

### Join Optimization
- `SortMerge Join` : 양쪽 데이터가 다 클때
- `Broardcast Join` : 한쪽 데이터가 작때
  - 옵티마이저에 자동으로 활성화됨(`spark.sql.autoBroadJoinThreshold`) 기본값은 10M.
  - Risk
    - Not Enough Driver Memory
    - DF > spark.driver.maxResultSize
    - DF > single executor avaliable working memory
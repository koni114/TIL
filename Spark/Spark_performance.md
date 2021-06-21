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



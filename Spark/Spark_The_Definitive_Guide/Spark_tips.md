## Spark Tips
- pyspark에서 pyspark.sql.functions 모듈에 있는 `col`, `columns` import 오류 발생하는 경우, pyspark-stubs 패키지 설치. 이 때 spark 버전과 동일해야 함  
ex) spark verison이 2.4.8인 경우, pyspark-stubs version이 2.4.0 post8 설치
- `pyspark.sql.dataframe.tail` 함수는 spark 3.0 이상부터 지원
- 현재 dataFrame의 파티션 개수 확인  
  `retail_df.rdd.getNumPartitions()`
- 
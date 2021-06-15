## 복잡한 쿼리 수행 후 DataFrame 생성 vs 간단한 쿼리를 통해 DataFrame 생성 후 filter, select를 통한 정제
1. RDBMS(Oracle, MySQL, postgreSQL...)
- spark는 RDBMS에서 데이터를 가져올 때 느림. 네트워크를 통해 최소의 데이터양으로 전송하는 것이 좋으므로, 복잡한 쿼리를 통해 최대한의 데이터를 fitlering 하는 것이 중요
2. RedShift, snowflake
- 쿼리를 클러스터 자체로 push down 하거나 , JDBC를 사용하여 데이터를 읽으려는 경우가 더 빠름
3. file
- 마찬가지로 cluster가 최소한의 작업을 수행할 수 있도록 push down 해야 함
- <b>결과적으로, spark 작업을 더 빠르게 하기 위해서는 source의 filter를 push down 해야 함</b>

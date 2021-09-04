## Spark- trouble shooting
### sql을 통한 RDBMS data select시, query error 발생 
- 항상 sql 쿼리를 통해 data select 수행시, ()를 주고, AS tablename으로 지정해 주어야 함

### std 계산시, 데이터가 1개인 경우 NaN
- 항상 표준편차 계산시, 데이터가 1개이면 NaN을 return 함.
- 이에 대한 처리가 반드시 필요함

## Window function 사용시 다음과 같은 warning 발생
- No Partition Defined for Window operation! Moving all data to a single partition, this can cause serious performance degradation
- `partitionBy` 함수를 통해 컬럼을 지정하여 window function 사용시 파티션이 생성되도록 해야함. 그렇지 않으면 driver local process에서 모든 데이터를 collect하여 계산하기 때문에 에러 발생 여지가 있음

## Spark data load시, microseconds truncate 문제
- S3 데이터를 csv format으로 export 한 뒤 가공하는 작업 수행
- MySQL에서 datatime(6)은 microsencond precision까지 지원
- S3에서 csv 파일을 읽게되면 microsecond는 truncate되고, millisecond만 남는 현상이 발생
  - ex) 2018-01-29 12:34:56.789  -> 2018-01-29 12:34:56.789 
  - ex) 2018-01-29 12:34:56.7890 -> 2018-01-29 12:35:03.890...
- 실제 Spark도 microseconds를 지원하는데 데이터를 로드 할 때는 microsecond를 못받아드림
- <b>이유는 Spark는 데이터를 로드하면서 timestamp를 파싱할 때 apache common의 FastDateFormat을 사용하는데, 이는 SimpleDataFormat의 thread-safe 버전으로, 이 클래스가 milliseconds 까지만 지원</b>
- 결과적으로 microseconds 단위까지 로드하고 싶다면, StringType으로 먼저 로드 후 Spark에서 timestamp로 casting 하는 작업이 필요

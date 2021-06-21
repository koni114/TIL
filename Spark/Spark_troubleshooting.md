## Spark- trouble shooting
### sql을 통한 RDBMS data select시, query error 발생 
- 항상 sql 쿼리를 통해 data select 수행시, ()를 주고, AS tablename으로 지정해 주어야 함

### std 계산시, 데이터가 1개인 경우 NaN
- 항상 표준편차 계산시, 데이터가 1개이면 NaN을 return 함.
- 이에 대한 처리가 반드시 필요함

## Window function 사용시 다음과 같은 warning 발생
- No Partition Defined for Window operation! Moving all data to a single partition, this can cause serious performance degradation
- `partitionBy` 함수를 통해 컬럼을 지정하여 window function 사용시 파티션이 생성되도록 해야함. 그렇지 않으면 driver local process에서 모든 데이터를 collect하여 계산하기 때문에 에러 발생 여지가 있음


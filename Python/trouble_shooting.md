## trouble shooting 정리
### terminal에서 python script 실행시, 'No module named' error 발생하는 경우
- IDE에서 해당 Script를 실행할 때와 terminal에서 해당 script를 실행할 때와 pythonPath가 달라서 생기는 문제. 따라서 `sys.path.append('path')` 를 통해 경로를 맞춰주자

### intellij에서 python script에서 JDBC driver directory path 설정 방법
-  `.config('spark.driver.extraClassPath', './lib/postgresql-9.4.1207.jar')`
  
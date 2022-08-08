## trouble shooting 정리
### terminal에서 python script 실행시, 'No module named' error 발생하는 경우
- IDE에서 해당 Script를 실행할 때와 terminal에서 해당 script를 실행할 때와 pythonPath가 달라서 생기는 문제. 따라서 `sys.path.append('path')` 를 통해 경로를 맞춰주자

### intellij에서 python script에서 JDBC driver directory path 설정 방법
-  `.config('spark.driver.extraClassPath', './lib/postgresql-9.4.1207.jar')`
  
### private 망에서 pip install 안되는 경우 해결 방법(intellij)
- 파이썬이 설치된 폴더에서 `session.py` python 파일을 찾아 `self.verify=False` 로 변경

### intellij 에서 import module 경로 인식 문제가 있는 경우
- File -> Project Structure -> Project Settings 에서 Modules -> Add Content Root 에서 변경







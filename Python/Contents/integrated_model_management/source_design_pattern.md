## 디자인 패턴
- m00s22
  - APP
  - PY_BATCH
  - PY_SERVER 
    - am_kpi_formula
    - appdata   
      - common
        - model_kpi_template
          - gen_hit_rate.py   --> 사용자가 template으로 사용할 적중률 template      
    - doc
    - input_data 
    - model       --> DB CRUD 등의 접근 수행
    - service     --> 필요한 로직 처리
    - view        --> app 과 python server를 routing 해주는 역할 수행 
    - test        --> test. pytest.
    - util        --> common function. 
  - ETC
    - git_push, git_commit 등을 위한 shell script   

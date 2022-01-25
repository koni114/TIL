## Chapter03 Airlfow 로 Spark 파이프라인 관리하기 - Airflow 와 Spark 같이쓰기
### airflow로 Spark 파이프airflow tasks test nft-pipeline store_nft 2021-01-23라인 관리하기 - Airflow 와 Spark 같이쓰기
- airflow 에 Spark 를 사용하려면 Spark provider 를 설치해야 함
~~~shell
pip --version 
pip install apache-airflow-providers-apache-spark 
~~~

#### airflow 상에서 spark 사용 예제
~~~python
# spark-example.py
from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_sql import SparkSqlOperator

default_args = {
    'start_date': datetime(2021, 1, 1)
}

with DAG(dag_id='spark-example',
         schedule_interval="@daily",
         default_args=default_args,
         tags=['spark'],
         catchup=False) as dag:

    sql_job = SparkSqlOperator(sql="SELECT * FROM foobar",
                               master='local',
                               task_id='sql_job')
~~~
- 다음과 같이 `airflow.providers.apache.spark.operators.spark_sql` 의  `SparkSqlOperator` 를 사용하면 Spark SQL 사용 가능
- 하지만 heavy 한 Spark Job 을 직접 airflow 내에서 사용하면 안됨
- airflow 내에서 spark-submit 을 실행하는 것이 더 좋음
~~~python
airflow tasks test spark-example submit_job 2021-01-24
~~~

### 택시비 예측 파이프라인 만들기 1

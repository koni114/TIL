import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator

dag=DAG(
    dag_id="print_dag_run_conf",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval=None,
)


def print_conf(**context):
    print(context["dag_run"].conf)


process = PythonOperator(
    task_id="process",
    python_callable=print_conf,
    dag=dag,
)


#!/usr/bin/env python
import datetime as dt
import os
import sys
from datetime import timedelta

from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.sensors.python import PythonSensor

SRC_HOME = os.path.dirname(os.path.realpath(__file__))
if SRC_HOME not in sys.path:
    sys.path.append(SRC_HOME)

from src.config import config as conf
from src.train_trigger import train_trigger

# exec(f"from repo.{proj_name}.src.config import config as conf")
# exec(f"from repo.{proj_name}.src.train_trigger import train_trigger")

with DAG(
    dag_id = f"{conf['proj_name']}-train-pipeline-trigger",
    default_args={
        "retries": 1,
        "retry_delay": dt.timedelta(minutes=2)
    },
    schedule_interval=conf["train_trigger_schedule_interval"],
    dagrun_timeout=timedelta(minutes=60),
    description=f"{conf['proj_name']} - train pipeline trigger by trigger rule",
    start_date = dt.datetime.strptime(conf["train_trigger_start_date"], conf["date_format"])
)as dag:

    check_trigger_rule_sensor = PythonSensor(
        task_id="check_trigger_rule",
        python_callable=train_trigger,
        op_kwargs=conf,
        timeout=60
    )

    start_train_pipeline_operator = TriggerDagRunOperator(
        task_id="start_train_pipeline",
        trigger_dag_id=f"{conf['proj_name']}-train-pipeline",
        wait_for_completion=True,
        poke_interval=10,
    )

    check_trigger_rule_sensor >> start_train_pipeline_operator
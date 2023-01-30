#!/usr/bin/env python
import datetime as dt
import os
import sys
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s

SRC_HOME = os.path.dirname(os.path.realpath(__file__))
if SRC_HOME not in sys.path:
    sys.path.append(SRC_HOME)

from src.config import config as conf
from src.config import get_src_home, set_env_minIO

with DAG(
    dag_id=f"{conf['proj_name']}-train-pipeline",
    default_args={
        "retries": 1,
        "retry_delay": dt.timedelta(minutes=2)
    },
    schedule_interval=conf["train_schedule_interval"],
    dagrun_timeout=timedelta(minutes=60),
    description=f"{conf['proj_name']} - train pipeline",
    start_date=dt.datetime.strptime(conf['train_start_date'], conf['date_format'])
) as dag:

    set_env_minIO(conf)

    train_operator = BashOperator(
        task_id="train",
        bash_command=f"python {os.path.join(get_src_home(), 'train.py')}",
        dag=dag,
    )

    k = KubernetesPodOperator(
        name="hello-dry-run",
        namespace="airflow",
        image="debian",
        cmds=["bash", "-cx"],
        arguments=["echo", "10"],
        labels={"foo": "bar"},
        task_id="dry_run_demo",
    )

    train_operator >> k

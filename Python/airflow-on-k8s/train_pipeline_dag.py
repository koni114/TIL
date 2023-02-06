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

    cloner = k8s.V1Container(
        name="clone-repo",
        image="k8s.gcr.io/git-sync/git-sync:v3.4.0",
        env=[
            # Problem: No templating occurs on this line.
            k8s.V1EnvVar(name="GIT_SYNC_REPO", value="{{ dag_run.conf['repo_url'] }}"),
            k8s.V1EnvVar(name="GIT_SYNC_SSH", value="true"),
        ],
    )

    build_container = KubernetesPodOperator(
        name="train-k8s",
        task_id="train-k8s",
        namespace="airflow",
        image="koni114/airflow:2.3.3-python3.8-12",
        init_containers=[cloner],
        is_delete_operator_pod=False,
        dag=dag,
        service_account_name="airflow-worker",
    )



    train_operator >> build_container

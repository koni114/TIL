import datetime as dt
import datetime

import pathlib
import os

import git
import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="git_daily_push",
    start_date=dt.datetime(2022, 6, 21),
    schedule_interval="@daily",
)


def git_push(repo_dir: str, commit_message: str):
    try:
        repo = git.Repo(repo_dir)
        repo.git.add(update=True)
        repo.index.commit(commit_message)
        origin = repo.remote(name="origin")
        origin.push()
    except Exception as e:
        print("Some Error occurred  while pushing the code")
        print(e)


git_push = PythonOperator(
        task_id="git_push",
        python_callable=git_push,
        op_kwargs={"repo_dir": "/Users/heojaehun/gitRepo/TIL",
                   "commit_message": f"git push {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"},
        dag=dag
)

git_push
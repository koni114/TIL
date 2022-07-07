import glob
import importlib.util
import os

import pytest
from airflow.models import DAG


# __file__
# --> 현재 수행중인 코드를 담고 있는 파일이 위치한 PATH 를 알려줌

DAG_PATH = os.path.join(
    os.path.dirname(__file__), "*.py"
)
print(f"DAG_PATH --> {DAG_PATH}")

# glob.glob
# 해당 패턴에 맞는 모든 파일 list 를 반환
DAG_FILES = glob.glob(DAG_PATH, recursive=True)
print(f"DAG_FILES --> {DAG_FILES}")


# dag_file = "2022-07-06.py"
# DAG_PATH = "*.py"
# os.path.splitext()
# 파일명과 확장자명을 분리시켜줌 ex) ["2022-07-06", ".py"]

@pytest.mark.parametrize("dag_file", DAG_FILES)
def test_dag_integrity(dag_file):
    module_name, _ = os.path.splitext(dag_file)     # ['2022-07-06', '.py']
    module_path = os.path.join(DAG_PATH, dag_file)  # '*.py/2022-07-06.py'
    mod_spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(module)

    dag_objects = [var for var in vars(module).values() if isinstance(var, DAG)]
    assert dag_objects

    for dag in dag_objects:
        dag.test_cycle()


from pathlib import Path
tmp_path = Path(".")
print(tmp_path / "input.json")
print(tmp_path / "output.csv")


# vars function
# --> python 내장함수로, 클래스 내 지역변수들을 dictionary 형태로 보여줌
#    __dict__ attribute 를 반환




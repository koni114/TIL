## 2022-04-27
# 특정 변수별 연속형 변수 통계값 만들기
import pandas as pd
import numpy as np
import os
os.getcwd()
pd.set_option("display.max_columns", 100)


df = pd.read_csv("/Users/heojaehun/gitRepo/TIL/Python/daily_Python/test_data/retail-data/all/online-retail-dataset.csv")
df.columns
df.head(5)
cal_var = "Quantity"
group_var = ["Country"]
except_var = ["InvoiceNo"]


def pos_cal_cpk(df: pd.DataFrame, cal_var: str, cpk_ucl_var: str, cpk_lcl_var: str):
    pass

def pos_cal_stat(df: pd.DataFrame, cal_var: str, except_var: list = None, group_var: list = None, ):

    # 제외할 컬럼이 dataframe 에 있는지 확인 후 제외
    ex_var = [v for v in except_var if v in df.columns]
    df.drop(ex_var, axis=1, inplace=True)

    # 통계값에 필요한 함수 선언
    def q1(x):
        return x.quantile(0.25)

    def q3(x):
        return x.quantile(0.75)

    def pct05(x):
        return x.quantile(0.05)

    def pct10(x):
        return x.quantile(0.10)

    def pct90(x):
        return x.quantile(0.90)

    def pct95(x):
        return x.quantile(0.95)

    # 통계 함수 계산을 위한 dict 생성
    stat_dict = {
        f"count_{cal_var}": 'count',
        f"mean_{cal_var}": 'mean',
        f"sd_{cal_var}": "std",
        f"min_{cal_var}": 'min',
        f"medi_{cal_var}": 'median',
        f"max_{cal_var}": 'max',
        f"q1_{cal_var}": q1,
        f"q3_{cal_var}": q3,
        f"pct05_{cal_var}": pct05,
        f"pct10_{cal_var}": pct10,
        f"pct90_{cal_var}": pct90,
        f"pct95_{cal_var}": pct95,
        f"var_{cal_var}": "var"
    }

    # 그룹 변수가 dataFrame 에 있는지 확인
    grp_var = [v for v in group_var if v in df.columns]
    if grp_var:
        return df.groupby(grp_var)[cal_var].agg(** stat_dict)  # 그룹 변수가 있는 경우,
    else:
        return df[[cal_var]].agg(list(stat_dict.values()))     # 그룹 변수가 없는 경우










# 파생변수 생성.
# - isMicro ? -- > True 면 rule21, False rule20
# - ds_id     -- >

import re
import pandas as pd
import numpy as np
from typing import List

df = pd.read_csv("test_data/iris.csv")
df["aggr_dt"] = "2022-06-06"
df["ctq_id"] = "C3671"
df["index"] = df.groupby("variety").cumcount()

derived_rule_df = pd.DataFrame([["C3671", "D1074", "N", "E", "new_col",
                                "Setosa + Virginica"]],
                               columns=["ds_id", "out_var_id", "out_var_tp", "tr_tp", "col_kor_nm", "expr"])

index_var_list = ["index", "aggr_dt", "ctq_id"]
col_var_list = ["variety"]
value_n_var = "petal.length"

class posCalDerivedVar:
    def __init__(self, df: pd.DataFrame, derived_rule_df: pd.DataFrame,
                 index_var_list: List, col_var_list: List, value_n_var: str, value_c_var: str):

        self.df = df
        self.derived_rule_df = derived_rule_df
        self.index_var_list = index_var_list
        self.col_var_list = col_var_list
        self.value_n_var = value_n_var
        self.value_c_var = value_c_var

    def get_derived_n_var(self):

        pivoted_df = pd.pivot_table(df,
                                    index=index_var_list,
                                    columns=col_var_list,
                                    values=value_n_var).reset_index()

        meta_col, derived_col = [], []
        meta_col.extend(index_var_list)
        meta_col.extend(col_var_list)
        meta_col.append(value_n_var)

        # idx, row = 0, derived_rule_df.loc[0, :]
        for idx, row in derived_rule_df.iterrows():

            expr_v = row.expr

            for col in pivoted_df.columns[~np.in1d(pivoted_df.columns, meta_col)]:
                if col in expr_v:
                    expr_v = expr_v.replace(col, "pivoted_df." + col)

            derived_col.append(row.col_kor_nm.strip())
            pivoted_df[row.col_kor_nm.strip()] = eval(expr_v)

        result_df = pd.melt(pivoted_df.loc[:, index_var_list + derived_col],
                            id_vars=index_var_list,
                            value_vars=derived_col,
                            value_name=value_n_var,
                            var_name=col_var_list)

        return result_df

import pandas as pd
d_df = pd.read_csv("test_data/iris.csv")

df = pd.DataFrame({'cust_id': ['c1', 'c1', 'c1', 'c2', 'c2', 'c2', 'c3', 'c3', 'c3'],
                   'prod_cd': ['p1', 'p2', 'p3', 'p1', 'p2', 'p3', 'p1', 'p2', 'p3'],
                   'grade': ['A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B'],
                   'pch_amt': [30, 10, 0, 40, 15, 30, 0, 0, 10]})

df.columns = ["가", '나', '다', '라']

data = pd.DataFrame({'cust_ID': ['C_001', 'C_001', 'C_002', 'C_002'],
                     'prd_CD': ['P_001', 'P_002', 'P_001', 'P_002'],
                     'pch_cnt': [1, 2, 3, 4],
                     'pch_amt': [100, 200, 300, 400]})

df_melt = pd.melt(data,
                  id_vars=['cust_ID', 'prd_CD'],
                  value_vars=['pch_cnt', 'pch_amt'],
                  value_name='pch_value',
                  var_name=['pch_CD'])


test_expr = "pch_new_col = pch_amt + pch_cnt"

test = pd.pivot_table(df_melt,
                      index=["cust_ID", "prd_CD"],
                      columns=["pch_CD"],
                      values=["pch_value"]).reset_index()

left_expr, right_expr = test_expr.split("=")
test[left_expr.strip()]









from typing import List


import pandas as pd
import numpy as np
from scipy import stats


df = pd.read_csv("test_data/iris.csv")
df = df.loc[np.in1d(df.variety, ["Setosa", "Virginica"]), :]
df["ctq_result"] = [0, 1] * (len(df) // 2)

x_var = "sepal.length"
y_var = "Species"
f_var = "variety"
bad_label = "Virginica"
good_label = "Setosa"

class posTestDiffTwoGroups:
    def __init__(self, df: pd.DataFrame, group_var: List,
                 x_var: str, y_var: str,  f_var: str, cut_off: float = 0.5,
                 conf_level: float = 0.95, good_label: str = "Setosa",
                 bad_label:str = "Virginica"):
        self.df = df
        self.group_var = group_var
        self.x_var = x_var
        self.y_var = y_var
        self.f_var = f_var
        self.cut_off = cut_off
        self.conf_level = conf_level
        self.good_label = good_label
        self.bad_label = bad_label

    def get_group_var_uniq_df(self):
        df_grp_var_uniq = self.df[self.group_var].drop_duplicates()
        return df_grp_var_uniq

    def cal_two_sample_ttest(self):

        df = self.df
        df.drop(df[x_var].isna(), inplace=True)

        if not len(df.groupby([f_var])[f_var].count()) == 2:
            return

        good_df = df.loc[df[f_var] == good_label, :]
        bad_df = df.loc[df[f_var] == bad_label, :]

        if not len(good_df) >= 2 and len(bad_df) >= 2:
            return

        # p_value --> TEST_MEAN
        ttest_result = stats.ttest_ind(good_df[x_var], bad_df[x_var], equal_var=True)

    def cal_feasibility_test(self):

        df = self.df
        df.drop(df[x_var].isna(), inplace=True)

        if not len(df.groupby([f_var])[f_var].count()) == 2:
            return

        good_df = df.loc[df[f_var] == good_label, :]
        bad_df = df.loc[df[f_var] == bad_label, :]

        if not len(good_df) >= 2 and len(bad_df) >= 2:
            return

        # A(평균 동일성 여부 지표) 계산
        A_v = ((np.mean(good_df[x_var]) - np.mean(bad_df[x_var])) ** 2) / (np.std(good_df[x_var]) ** 2)
        a_v = round(A_v, 8)

        # V(분산 동일성 여부 지표) 계산
        v_v = (np.std(bad_df[x_var]) ** 2) / (np.std(good_df[x_var]) ** 2)
        v_v = round(v_v, 8)
































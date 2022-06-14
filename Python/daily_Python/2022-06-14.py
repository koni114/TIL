# 2022-06-14.py
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

df = pd.read_csv("test_data/iris.csv")
df["ctq_result"] = [0, 1] * (len(df) // 2)

group_var = ["variety"]
x_var = "sepal.length"
y_var = "ctq_result"
f_var = "variety"
bad_label = 1
good_label = 0

result_df_columns = group_var + ["TEST_MEAN", "A", "V"]
result_df = pd.DataFrame(columns=result_df_columns)

for (grp, df_by_group_id) in df.groupby(group_var):
    good_df = df_by_group_id.loc[df[y_var] == good_label, :]
    bad_df = df_by_group_id.loc[df[y_var] == bad_label, :]
    ttest_result = ttest_ind(good_df[x_var], bad_df[x_var], equal_var=True)

    a_v = ((np.mean(good_df[x_var]) - np.mean(bad_df[x_var])) ** 2) / (np.std(good_df[x_var]) ** 2)
    # V(분산 동일성 여부 지표) 계산
    v_v = (np.std(bad_df[x_var]) ** 2) / (np.std(good_df[x_var]) ** 2)

    result_tmp_df = pd.DataFrame([[grp, ttest_result.pvalue, round(a_v, 8), round(v_v, 8)]], columns=result_df_columns)
    result_df = pd.concat([result_df, result_tmp_df])

result_df = pd.concat([result_df, result_df])
result_df["id"] = ["A", "A", "A", "B", "B", "B"]

result_df[["id", "variety", "TEST_MEAN", "A", "V"]]

# id 별로 variety 의 rank 를 계산한다.

# TEST_MEAN 컬럼 값이 0.05 보다 작거나 같은 경우, TEST_MEAN 이 작은 순서대로 rank 를 매긴다.
# TEST_MEAN 컬럼 값이 0.05 보다 작거나 같은 값이 없으면,
# A 컬럼이 1보다 크거나 같은 값이 있는 경우, A 컬럼 값이 큰 순서대로 rank 를 매긴다.
# A 컬럼 값이 1보다 크거나 같은 값이 없는 경우,
# V 컬럼 값이 큰 순서대로 rank 를 매긴다.

for (var, df_group_by_id) in result_df.groupby(group_var):
    if np.any(df_group_by_id["TEST_MEAN"] <= 0.05):
        df_group_by_id["cause_rank"] = df_group_by_id["TEST_MEAN"].rank(method="min", ascending=True).astype(int)
        df_group_by_id["cause_yn"] = np.where(df_group_by_id['TEST_MEAN'] <= 0.05, "Y", "N")
    elif np.any(result_df["A"] >= 1):
        df_group_by_id["cause_rank"] = df_group_by_id["A"].rank(method="min", ascending=False).astype(int)
        df_group_by_id["cause_yn"] = np.where(df_group_by_id['A'] >= 1, "Y", "N")
    else:
        df_group_by_id["cause_rank"] = df_group_by_id["V"].rank(method="min", ascending=False).astype(int)
        df_group_by_id["cause_yn"] = np.where(df_group_by_id['V'] >= 4, "Y", "N")



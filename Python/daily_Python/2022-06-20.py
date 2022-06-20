# 2022-06-20.py
# entropy, bg-ratio, chi-square 계산해보기

# 1. entropy.
# 1.1  범주형 변수의 entropy 계산하기


import pandas as pd
import numpy as np

lst = ["apple"] * 3 + ["orange"] * 2 + ["banana"] * 1
fruits = pd.Series(lst)
print(fruits)

probs = fruits.value_counts(normalize=True)
entropy_v = np.round(-1 * np.sum(np.log2(probs) * probs), 4)
print(f"entropy --> {entropy_v}")

# 1.2. 그룹별 entropy 계산하기
# 범주형 변수가 추가 되었을 때의 entropy 와 그렇지 않을 때의 entropy 를 계산하여
# information-gain 을 계산해보기

df = pd.DataFrame({"fac1": [1, 1, 1, 1, 2, 2, 2, 2],
                   "fac2": [1, 0, 1, 0, 1, 1, 1, 1]})

x = pd.Series([1, 0, 1, 0])
def cal_entropy(x):
    probs = x.value_counts(normalize=True)
    entropy = -1 * np.sum(np.log2(probs) * probs)
    return entropy

before_entropy_v = cal_entropy(df["fac2"])

# groupby 이후에 특정 컬럼명을 지정해주면, 계산값에 column 명이 지정되지 않음.
grouped_df = df.groupby(["fac1"])["fac2"].count().reset_index(name="count")
grouped_df["entropy"] = df.groupby(["fac1"])["fac2"].apply(cal_entropy).reset_index(drop=True)
grouped_df["prob"] = grouped_df["count"] / np.sum(grouped_df["count"])
after_entropy_v = np.sum(grouped_df["entropy"] * grouped_df["prob"])

print(f"information gain --> {round(before_entropy_v - after_entropy_v, 4)}")

# 2. bg-ratio.
def bg_ratio(x):
    x_len = len(x)
    x_value_counts = x.value_counts()
    if len(x_value_counts) == 1:
        return 1
    return abs(x_value_counts[0] / x_len) - (x_value_counts[1] / x_len)

bg_ratio_v = np.mean(df.groupby(["fac1"])["fac2"].apply(bg_ratio))
print(f"bg-ratio --> {bg_ratio_v}")

obs = pd.DataFrame({"당뇨": [10, 15], "정상": [10, 65]})
obs.index = ["비만체중", "정상체중"]
print(obs)

# 3. chi-square 의 독립성 검정
from scipy.stats import chi2_contingency
chi_result = chi2_contingency(pd.crosstab(df["fac1"], df["fac2"]), correction=False)
print(f"chi-square --> {np.round(chi_result[0], 4)}")
print(f"p-value --> {np.round(chi_result[1], 4)}")


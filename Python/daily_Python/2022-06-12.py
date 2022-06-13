# two-sample t-test 검정 예제

# 예제 수행을 위한 데이터 준비
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("test_data/iris.csv")
df = df.loc[np.in1d(df.variety, ["Setosa", "Virginica"]), :]
df["ctq_result"] = [0, 1] * (len(df) // 2)

x_var = "sepal.length"
y_var = "Species"
f_var = "ctq_result"

setosa_sepal_length = df.loc[df.variety == "Setosa", x_var]
virginica_sepal_length = df.loc[df.variety == "Virginica", x_var]

# 정규성 검정 결과
normal1 = stats.shapiro(setosa_sepal_length)
normal2 = stats.shapiro(virginica_sepal_length)
print(normal1)
print(normal2)

# 등분산성 검정(levene test)
levene = stats.levene(setosa_sepal_length, virginica_sepal_length)
print(levene)

# 독립 Two-sample T-TEST
# - 검정 통계량: -15.386195820079404
ttest_result = stats.ttest_ind(setosa_sepal_length, virginica_sepal_length, equal_var=True)
print(f"검정 통계량 --> {ttest_result.statistic}")
print(f"pvalue   --> {ttest_result.pvalue}")
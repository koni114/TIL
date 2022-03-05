# 동일 길이로 나누어서 범주 나누기: pd.cut()
# 동일 개수로 나누어서 범주 만들기: pd.qcut()

import numpy as np
import pandas as pd
np.random.seed(123)
df = pd.DataFrame({'col_1': np.random.randint(20, size=20),
                   'col_2': np.random.randn(20)})

df_col_1_factor = pd.cut(df.col_1, 4)

df_grouped = df.col_1.groupby(df_col_1_factor)
df_grouped.agg(['count', 'mean', 'std', 'min', 'max'])

def summary_func(grp):
    return {'count': grp.count(),
            'std': grp.mean(),
            'mean': grp.mean(),
            'min': grp.min(),
            'max': grp.max()}

df_grouped.apply(summary_func).unstack()
df_grouped.apply(summary_func)

# labels = np.arange(4, 0, -1) 로 지정하면 거꾸로 지정됨
bucket_qcut_label_col_2 = pd.qcut(df.col_2, 4, labels=np.arange(4, 0, -1))

# [4 < 3 < 2 < 1] 순서로 동일 개수로 나눈 4개의 그룹별 통계량
grouped = df.col_2.groupby(bucket_qcut_label_col_2)
grouped.apply(summary_func).unstack()


## (2). 그룹 별 변수 간 상관관계 분석
## Pearson Correlation Coefficient 을 구할 수 있는 corr(), corrwith() 함수를 제공
## 해당 함수를 groupby + apply 를 함께 사용함으로써 그룹 별 변수 간 상관계수를 구할 수 있음


import numpy as np
import pandas as pd
np.random.seed(123)
df = pd.DataFrame(np.random.randn(10, 4),
                  columns=['a', 'b', 'c', 'd'])
df['group'] = ['grp1'] * 5 + ['grp2'] * 5
df = df.set_index('group')
print(df)

# (2)-1 'd' 변수와 나머지 모든 변수 간 그룹별 상관계수 구하기: x.corrwith(x['d'])
corr_with_d = lambda x: x.corrwith(x['d'])
grouped = df.groupby('group')
grouped.apply(corr_with_d)

# (2)-2 'a' 변수와 'd' 변수 간 그룹 별 상관계수 구하기
# --> g['a'].corr[g['d']]

corr_a_d = lambda g: g['a'].corr(g['d'])
grouped = df.groupby('group')
grouped.apply(corr_a_d)

# (3) 그룹 별 선형회귀모형 적합하기(Group-wise Linear Regression)
# groupby + apply() 를 활용하여 그룹 별 선형회귀모형을 적합

import numpy as np
import pandas as pd
from sklearn import datasets, linear_model

# diabetes 데이터 load
diabetes = datasets.load_diabetes()
diabetes_Y = pd.DataFrame(diabetes.target, columns=['target'])
diabetes_X = pd.DataFrame(diabetes.data[:, 0:3],
                          columns=['age', 'sex', 'bmi'])

# GroupBy() + apply() --> UDF
diabetes_df = pd.concat([diabetes_Y, diabetes_X], axis=1)
diabetes_df['grp'] = np.where(diabetes_df['sex'] > 0, 'M', 'F')
diabetes_df.drop(columns=['sex'], inplace=True)
print(diabetes_df[:3])

# 선형회귀모형 UDF 정의
# 각 그룹별 age 와 bmi 변수의 회귀계수를 비교할 것이므로,
# 그룹별 회귀 모형의 회귀계수 + 절편을 결과로 반환

def lin_regress(data, y_var, x_vars):

    # output, input variables
    y = data[y_var]
    X = data[x_vars]

    lin_reg = linear_model.LinearRegression()
    model = lin_reg.fit(X, y)

    intercept = model.intercept_
    coef = model.coef_
    result = [intercept, coef]

    return result


grouped = diabetes_df.groupby('grp')
lin_reg_coef = grouped.apply(lin_regress, 'target', ['age', 'bmi'])

print(np.round(lin_reg_coef['M'], 3))
print(lin_reg_coef['F'])

# (4). 그룹 별 무작위 표본 추출(random sampling by group)
# np.random.permutation() 함수를 사용하여 순열을 무작위로 뒤 섞은 후에 n개 만큼 indexing
import numpy as np
import pandas as pd

# setting seed number for reproducibility
np.random.seed(123)

# Make a DataFrame
df = pd.DataFrame({'grp': ['grp_1']*10 + ['grp_2']*10,
                   'col_1': np.random.randint(20, size=20),
                   'col_2': np.random.randint(20, size=20)})

# 사용자가 지정한 샘플링 비율만큼 무작위 표본 추출을 해주는 UDF 정의
def sampling_func(data, sample_pct):
    np.random.seed(123)
    N = len(data)
    sample_n = int(N*sample_pct)
    sample = data.take(np.random.permutation(N)[:sample_n])
    return sample


sample_set = df.groupby('grp').apply(sampling_func, sample_pct=0.8)
sample_set.sort_index()

# 무작위 추출에서 group keys 를 없애려면 group_keys= False 설정
sample_set = df.groupby('grp', group_keys=False).apply(sampling_func, sample_pct=0.8)
sample_set.sort_index()

# 80% 무작위 샘플링이 된 sample_set 에 있는 데이터셋을 training_set 이라고 가정해보고
# sample_set 는 없지만 원래 데이터에는 있던 나머지 20% 데이터를 test set 으로 별도로 만들어보기
test_set = df.drop(df.index[sample_set.index])
print(test_set)

df.drop(sample_set.index)

# (5) 다수 그룹 별 다수의 변수 간 상관관계 분석
# (correlation coefficient with multiple columns by groups)
# 다수 그룹 별 다수의 변수 간 쌍을 이룬 상관계수 분석(paired correlation)

# 3개의 그룹 변수, 4개의 연속형 변수를 가진 예제 DataFrame 만들기
import numpy as np
import pandas as pd

group_1 = ['A', 'B'] * 20
group_2 = ['C', 'D', 'E', 'F'] * 10
group_3 = ['G', 'H', 'I', "J", 'K', 'L', 'M', 'N'] * 5

df = pd.DataFrame({'group_1': group_1,
                   'group_2': group_2,
                   'group_3': group_3,
                   'col_1': np.random.randn(40),
                   'col_2': np.random.randn(40),
                   'col_3': np.random.randn(40),
                   'col_4': np.random.randn(40)})

df.sort_values(by=['group_1', 'group_2', 'group_3'], axis=0)

# (2) 그룹별 두 개 변수 간 상관계수를 구하는 사용자 정의 함수
val_1 = 'col_1'
val_2 = 'col_2'
group_list = ['group_1']


def corr_group(df, var_1, var_2, group_list):
    corr_func = lambda g: g[var_1].corr(g[var_2])

    # GroupBy Operators
    grouped = df.groupby(group_list)

    corr_coef_df = pd.DataFrame(grouped.apply(corr_func), columns=['corr_coef'])

    corr_coef_df['var1'] = var_1
    corr_coef_df['var2'] = var_2

    return corr_coef_df

# (3) 다수 그룹별 다수 변수 간 두개 씩 쌍을 이루어 상관계수 구하기
# 'group_1', 'group_2', 'group_3' 의 3개의 그룹 변수로 만들어진 모든 경우의 수의 그룹 조합에
# 대해서, 'col_1', 'col_2', 'col_3', 'col_4'의 4개 연속형 변수 2개씩 쌍을 이루어 만들어진 모든 경우의 수
# 조합을 구해 조합별 상관계수 구하기

corr_coef_df_all = pd.DataFrame()
group_list = ['group_1', 'group_2', 'group_3']
col_list = ['col_1', 'col_2', 'col_3', 'col_4']

from itertools import combinations
comb = combinations(col_list, 2)

for var in list(comb):
    corr_tmp = corr_group(df, var[0], var[1], group_list)
    corr_coef_df_all = corr_coef_df_all.append(corr_tmp)

# result
print(corr_coef_df_all[['var1', 'var2', 'corr_coef']])
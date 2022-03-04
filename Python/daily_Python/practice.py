import numpy as np
import pandas as pd
pd.set_option('max_columns', 50)
pd.set_option('max_rows', 50)
np.random.seed(123)
df = pd.DataFrame({'col_1': np.random.randint(20, size=20),
                   'col_2': np.random.randn(20)})

df_col_1_factor = pd.cut(df.col_1, 4)
grouped = df.col_1.groupby(df_col_1_factor)

df_col_2_factor_by_count = pd.qcut(df.col_2, 4, labels=np.arange(4, 0, -1))

def stat_func(grp):
    return {'mean': grp.mean(),
            'std': grp.std(),
            'median': grp.median(),
            'sum': grp.sum()}


grouped.apply(stat_func).unstack()


from flask import Flask, url_for
app = Flask(__name__)

@app.route('/myapplication')
def index(): pass

@app.route('/login')
def login(): pass

@app.route('/user/<username>')
def profile(username): pass


with app.test_request_context():
    print(url_for("index"))
    print(url_for("login"))
    print(url_for("login", next="/"))
    print(url_for("profile", username="John Doe"))

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

# (5) 다수 그룹 별 다수의 변수 간 상관관계 분석(correlation coefficient with multiple columns by groups)


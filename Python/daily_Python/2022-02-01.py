# 이산형 변수를 One-Hot encoding 수행

# 범주형 변수의 이항변수화: sklearn.preprocessing.OneHotEncoder()
from sklearn.preprocessing import OneHotEncoder
import numpy as np
data_train = np.array([[0, 0, 0],
                       [0, 1, 1],
                       [0, 2, 2],
                       [1, 0, 3],
                       [1, 1, 4]])

print(data_train)

# OneHotEncoder() 로 범주형 변수의 이항변수화 적합시키기: enc.fit()
help(OneHotEncoder)

enc = OneHotEncoder(categories='auto',
                    drop=None,
                    sparse=True,
                    handle_unknown='ignore')
enc.fit(data_train)

enc.transform([["1", '0', '2']]).toarray()
enc.inverse_transform([[0., 1., 1., 0., 0., 0., 0., 1., 0., 0.]])
enc.get_feature_names()
enc.get_params()

# 연속형 변수의 이산형화(discretization)
import pandas as pd
import numpy as np
np.random.seed(10)
df = pd.DataFrame({'C1': np.random.randn(20),
                   'C2': ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a',
                          'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']})


# np.digitize() 함수를 활용한 이산형화
bins = np.linspace(df.C1.min(), df.C1.max(), 10)
df['C1_bin'] = np.digitize(df['C1'], bins)
print(df)

df.groupby('C1_bin')['C1'].size()
df.groupby('C1_bin')['C1'].mean()
df.groupby('C1_bin')['C1'].std()
df.groupby('C1_bin')['C2'].value_counts()

# pd.get_dummies() 를 이용해 가변수(dummy var) 만들기
pd.get_dummies(df['C1_bin'], prefix='C1')

# drop_first = True 옵션 설정 시, 가변수의 첫번째 변수를 자둥으로 삭제
# 가변수 함정(dummy trap) 을 피할 수 있게 해줌
pd.get_dummies(df['C1_bin'], prefix='C1', drop_first=True)

# (2) np.where(condition, factor1, factor2, ...) 를 이용한 연속형 변수의 이산형화
# - 조건절에 좀더 유연하게 조건을 부여해서 이산형화, 범주화를 할 수 있음
# - 연속형 변수 'C1' 의 `평균`을 기준을  평균 이상으로 'high', 평균 미만이면 'low' 로 이산형화 변수 생성
df['high_low'] = np.where(df['C1'] >= df['C1'].mean(), 'high', 'low')

df.groupby('high_low')['C1'].size()
df.groupby('high_low')['C1'].mean()
df.groupby('high_low')['C1'].std()

# Q1, Q3 를 기준으로 01_high, 02_medium, 03_low 로 구분하여 이산형화 변환 수행
Q1 = np.percentile(df['C1'], 25)
Q3 = np.percentile(df['C1'], 75)

df['h_m_l'] = np.where(df['C1'] >= Q3, '01_high',
                       np.where(df['C1'] >= Q1, '02_medium', '03_low'))

df.groupby('h_m_l')['C1'].size()
df.groupby('h_m_l')['C1'].mean()
df.groupby('h_m_l')['C1'].std()

# 다항차수 변환, 교호작용 변수 생성
# sklearn.preprocessing.PolynomialFeatures() 에 대해서 알아보자
# 해당 함수를 활용하면, 다항차수 변환, 교호작용 변수 생성이 가능

import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures

X = np.arange(6).reshape(3, 2)
poly = PolynomialFeatures(degree=2)

# (1, x1, x2, x1^2, x1*x2, x2^2)
poly.fit_transform(X)

# (2) 교호작용 변수만을 만들기 : interaction_only = True

X2 = np.arange(9).reshape(3, 3)
poly_d2 = PolynomialFeatures(degree=2, interaction_only=True)
poly_d3 = PolynomialFeatures(degree=3, interaction_only=True)

# (x1, x2, x3) --> (1, x1, x2, x3, x1*x2, x2*x3, x1*x3)
poly_d2.fit_transform(X2)

# transform from (x1, x2, x3) to (1, x1, x2, x3, x1*x2, x1*x3, x2*x3, x1*x2*x3)
poly_d3.fit_transform(X2)
print(poly_d3)



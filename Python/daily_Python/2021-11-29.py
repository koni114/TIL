## dataFrame 층별화
import os

import numpy as np
import seaborn as sns
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

df = sns.load_dataset('titanic')

# boolean indexing
mask1 = (df.age >= 10) & (df.age <= 20)
df_filtering = df.loc[mask1, :]
df_filtering.head()

mask2 = (df.age < 10) & (df.sex == 'female')
df_female_under10 = df.loc[mask2, :]
print(df_female_under10.head())

# contains + notna
mask3 = df["embark_town"].str.contains("F") | df['embark_town'].notna()

######################
## IQR 기준 이상치 제거 ##
######################


def outlier_treatment(data_column):
    if any(data_column.isna()):
        data_column = data_column[data_column.notna()]
    sorted(data_column)
    Q1, Q3 = np.percentile(data_column, [25, 75])
    IQR = Q3 - Q1
    lower_range = Q1 - (1.5 * IQR)
    upper_range = Q3 + (1.5 * IQR)
    return lower_range, upper_range


lower_bound, upper_bound = outlier_treatment(data_column=df.age)
df.drop(df[(df.age > upper_bound) | df.age < lower_bound].index, inplace=True)

##############
## 결측치 제거 ##
##############
# 결측치 사례 제거.
# - 수치형의 경우 평균이나 중앙치로 대체
# - 범주형인 경우, mode 값으로 대체
# 간단한 예측 모델로 대체하는 방식이 일반적

# fillna --> 결측치 채우기
# 연속형인 경우 Mean 이나 Median 을 이용

#- Missing Value 파악을 위해 df.info() 확인
#- np.nan 으로 적절히 missing value 로 불러왔다면 info() 이용 가능
#- 공백이나 다른 방식으로 처리되어 있다면, 모두 replace 처리해주어야 함
#  info()를 실행하였을 때, 누가봐도 float or int 이지만 object(string)으로 되어 있다면
#  이런 사례가 포함될 가능성이 높음

# NA와 Null 차이점
# - R 에서만 구분되면 개념
# - 파이썬에서는 numpy 의 NaN 만 이용. 가끔 pure python 에서 None 을 볼 수 있음
# - NA: Not Available
# - Null: empty(null) object
# - NaN: Not a Number (python)
# - reference
df.columns
df['age'] = df['age'].fillna(df.age.mean())
df['embarked'].value_counts()


# 만약 결측치가 문자열 스페이스('  ')로 되어 있다면, np.nan 으로 바꾸어
# Pandas 라이브러리가 인식할 수 있도록 변환
df.embarked = df.embarked.replace('', np.nan)

# 결측치를 제거하는 방법
df.dropna(how='all').head()  # 한 행이 모두 missing value 이면 제거
df.dropna(how='any').head()  # 한 행에서 하나라도 missing value 가 있으면 제거

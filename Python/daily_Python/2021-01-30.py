import pandas as pd
import numpy as np
ser = pd.Series([1, 2, 3, 4, np.nan])

ser.replace(2, 20)
ser.replace(np.nan, 5)
ser.replace([1, 2, 3, 4, np.nan], [6, 7, 8, 9, 10])


df = pd.DataFrame({'C1': ['a_old', 'b', 'c', 'd', 'e'],
                   'C2': [1, 2, 3, 4, 5],
                   'C3': [6, 7, 8, 9, np.nan]})


df.replace({'C1': 'a_old'}, {'C1': 'a_new'})
df.replace({'C3': np.nan}, {'C3': 10})

# 중복 여부 확인: pd.DataFrame.duplicated()
# 중복이 있으면 처음과 마지막 값 중 무엇을 남길 것인가?: keep = 'first', 'last', False
# 중복값 처리 : drop_duplicates()

import pandas as pd
data = {'key1': ['a', 'b', 'b', 'c', 'c'],
        'key2': ['v', 'w', 'w', 'x', 'y'],
        'col':  [1, 2, 3, 4, 5]}

df = pd.DataFrame(data)
df.duplicated(['key1'], keep=False)
df.duplicated(['key1', 'key2'])

df.drop_duplicates(['key1'], keep='first')
df.drop_duplicates(['key1'], keep='last')
df.drop_duplicates(['key1'], keep=False)

# 유일한 값 찾기 : pd.Series.unique()
# 유일한 값 별로 개수 세기 : pd.Series.value_counts()

import pandas as pd
import numpy as np
df = pd.DataFrame({'A': ['A1', 'A1', 'A2', 'A2', 'A3', 'A3'],
                   'B': ['B1', 'B1', 'B1', 'B1', 'B2', np.nan],
                   'C': [1, 1, 3, 4, 4, 4]})

df['A'].unique()
df['B'].unique()
df['C'].unique()

# 유일한 값별로 개수 세기: pd.Series.value_counts()
pd.Series.value_counts(normalize=False,   # False : 개수, True : 상대 비율
                       sort=True,         # True : 개수 기준정렬, False: 유일한 값 기준 정렬
                       ascending=False,   #
                       bins=None,
                       dropna=True)       # True: NaN 무시, False : NaN 포함


df['A'].value_counts()
df['B'].value_counts(dropna=False)
df['C'].value_counts()

# 표준정규분포 표준화
# 1. (x - mean()) / std()
# 2. ss.zscore
# 3. StandardScaler(data).fit_transform()

import numpy as np
data = np.random.randint(30, size=(6, 5))
data_standardized_np = (data - np.mean(data, axis=0)) / np.std(data, axis=0)

# 제대로 계산되었는지 확인
np.mean(data_standardized_np, axis=0)
np.std(data_standardized_np, axis=0)

import scipy.stats as ss
data_standardized_ss = ss.zscore(data)
data_standardized_ss

from sklearn.preprocessing import StandardScaler
data_standardized_skl = StandardScaler().fit_transform(data)
print(data_standardized_skl)
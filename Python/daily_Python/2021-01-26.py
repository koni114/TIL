import pandas as pd
df_left = pd.DataFrame({'KEY': ['K0', 'K1', 'K2', 'K3'],
                        'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': [0.5, 2.2, 3.6, 0.4]})

df_right = pd.DataFrame({'KEY': ['K2', 'K3', 'K4', 'K5'],
                         'C': ['C2', 'C3', 'C4', 'C5'],
                         'D': ['D2', 'D3', 'D4', 'D5']})

df_all = pd.merge(df_left, df_right,  how='outer', on='KEY')


df_all.isnull()
df_all.notnull()

df_all.loc[[0, 1], ['A', 'B']] = None
df_all[['A', 'B']].isnull()

# 컬럼별 결측값 개수 구하기: df.isnull().sum()
df_all.isnull().sum()
df_all['A'].isnull().sum()

# 컬럼별 결측값이 아닌 값의 개수를 구하려면, df.notnull().sum() 을 사용
df_all.notnull().sum()
df_all['NaN_cnt'] = df_all.isnull().sum(1)
df_all['NotNull_cnt'] = df_all.notnull().sum(1)
print(df_all)



## 결측값 채우기, 대체, 결측값 처리 : df.fillna()
import numpy as np
import pandas as pd
df = pd.DataFrame(np.random.randn(5, 3), columns=['C1', 'C2', 'C3'])

df.loc[0, 0] = None
df.loc[1, ['C1', 'C3']] = np.nan
df.loc[2, ['C2']] = np.nan
df.loc[3, ['C2']] = np.nan
df.loc[4, 'C3'] = np.nan

# 결측값을 특정 값으로 채우기 : df.fillna(0)
df_0 = df.fillna(0)
df_missing = df.fillna('missing')

# 결측값 앞 방향으로 채워나가는 경우, method = 'ffill', 'pad' 입력
df_ffill = df.fillna(method='ffill')
df_pad = df.fillna(method='pad')

# 결측값 뒷 방향으로 채워나가는 경우 method = 'bfill', method = 'backfill'
df_bfill = df.fillna(method='bfill')
df_backfill = df.fillna(method='backfill')
print(df_backfill)

# 앞/뒤 방향으로 결측값 채우는 횟수를 제한하기 : fillna(limit=number)
df.fillna(method='ffill', limit=1)
df.fillna(method='bfill', limit=1)

# 결측값을 변수별 평균으로 대체하기 : df.fillna(df.mean()),
#                            df.where(pd.notnull(df), df.mean(), axis='columns')
# df.where(Series 객체에 대한 조건문, 거짓 값에 대한 대체 값)

df.fillna(df.mean())
df.where(pd.notnull(df), df.mean(), axis='columns')

# 다음은 C1 컬럼의 평균을 가지고, C1, C2, C3 컬럼의 결측값 대체
df.mean()['C1']
df.fillna(df.mean()['C1'])

# 'C1' , 'C2' 컬럼에 대해서만 각 컬럼의 평균을 가지고, 각 컬럼에 있는 대체값을 대체하는 경우
df.mean()['C1':'C2']
df.fillna(df.mean()['C1':'C2'])

# 결측값을 다른 변수의 값으로 대체
# C2 컬럼에서 결측값이 없으면 'C2' 컬럼의 값을 그대로 사용,
# C2 컬럼에 결측값이 있으면 C1 컬럼의 값을 가져다가 결측값 채우기

df_2 = pd.DataFrame({'C1': [1, 2, 3, 4, 5],
                     'C2': [6, 7, 8, 9, 10]})

df_2.loc[[1, 3], ['C2']] = np.nan

df_2['C2_New'] = np.where(pd.notnull(df_2['C2']) == True, df_2['C2'], df_2['C1'])

# loop programming 으로 계산하는 경우, 동일한 결과를 반환하지만,
# np.where() 와 pd.notnull() 을 사용하는 것이 속도도 빠르고 코드도 짧음

# 결측값 있는 행 제거 : dropna(axis=0)
# 결측값 있는 열 제거 : dropna(axis=1)

import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.randn(5, 4), columns=['C1', 'C2', 'C3', 'C4'])
df.loc[[0, 1], 'C1'] = None
df.loc[2, 'C2'] = np.nan

# 결측값이 들어있는 행 전체 삭제
df.dropna(axis=0)

# 결측값이 들어있는 열 전체 삭제
df.dropna(axis=1)

# 특정 행 또는 열을 대상으로 결측값이 들어있으면 제거
df['C1'].dropna()
df[['C1', 'C2', 'C3']].dropna()
df[['C1', 'C2', 'C3']].dropna(axis=1)

# 결측값 보간(interpolation)하기.
# (1) 시계열 데이터의 값에 선형으로 비례하는 방식으로 결측값 보간
# (2) 시계열 날짜 index 기준으로 결측값 보간
# (3) DataFrame 값에 선형으로 비례하는 방식으로 결측값 보간
# (4) 결측값 보간 개수 제한

import pandas as pd
import numpy as np
from datetime import datetime

date_strs = ['2021-12-01', '2021-12-03', '2021-12-04', '2021-12-10']
dates = pd.to_datetime(date_strs)

ts = pd.Series([1, np.nan, np.nan, 10], index=dates)

ts_intp_linear = ts.interpolate()
print(ts_intp_linear)

# 시계열 날짜 index 기준으로 결측값 보간
ts_intp_time = ts.interpolate(method='time')
print(ts_intp_time)

# DataFrame 값에 선형으로 비례하는 방식으로 결측값 보간
df = pd.DataFrame({'C1': [1, 2, np.nan, np.nan, 5],
                   'C2': [6, 8, 10, np.nan, 20]})

df_intp_values = df.interpolate(method='values')
print(df_intp_values)

# 결측값 보간 개수 제한하기 : limit = 1
df.interpolate(method='values', limit=1)

# limit_direction = 'backward'
df.interpolate(method='values', limit=1, limit_direction='backward')

import pandas as pd
import numpy as np
df = pd.DataFrame(np.arange(10).reshape(5, 2),
                  index=['a', 'b', 'c', 'd', 'e'],
                  columns=['C1', 'C2'])

df.loc[['b', 'e'], ['C1']] = None
df.loc[['b', 'c'], ['C2']] = None


df = pd.DataFrame(np.random.randn(5, 3), columns=['C1', 'C2', 'C3'])
df.iloc[0, 0] = None
df.loc[1, ['C1', 'C3']] = np.nan
df.loc[2, 'C2'] = np.nan
df.loc[3, 'C2'] = np.nan
df.loc[4, 'C3'] = np.nan

df = pd.DataFrame(np.random.randn(5, 4),
                  columns=['C1', 'C2', 'C3', 'C4'])

df.loc[[0, 1], 'C1'] = None
df.loc[2, 'C2'] = np.nan

date_strs = ['2021-01-03', '2021-01-04', '2021-01-07', '2021-01-10']
dates = pd.to_datetime(date_strs)
ts = pd.Series([1, np.nan, np.nan, 10], index=dates)
print(ts)

df = pd.DataFrame({'C1': [1, 2, np.nan, np.nan, 5],
                   'C2': [6, 8, 10, np.nan, 20]})

df_intp_values = df.interpolate(method='values')
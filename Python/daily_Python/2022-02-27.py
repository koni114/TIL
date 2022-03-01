## 2022-02-27
import numpy as np
import pandas as pd
import urllib.request
import ssl

# 여러개의 칼럼에 대해 다른 함수를 적용 : groupby().apply(functions)
# --> dict 를 통해서도 각 컬럼별로 여러 함수 적용 가능하므로, 편한 것을 선택하면 됨

# (1) dataFrame 에서 여러개의 칼럼에 대해 다른 함수 적용: grouped.apply(function)

import numpy as np
import pandas as pd
df = pd.DataFrame({'grp_col_1': ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b'],
                   'grp_col_2': ['c', 'c', 'd', 'd', 'd', 'e', 'e', 'f', 'f', 'f'],
                   'val_1': np.arange(10),
                   'val_2': np.random.randn(10)})

# val_1 --> mean, std
# val_2 --> max, min, range





def stat_func(x):
    d = dict()
    d['val_1_mean'] = x['val_1'].mean()
    d['val_1_std'] = x['val_1'].std()
    d['val_2_max'] = x['val_2'].max()
    d['val_2_min'] = x['val_2'].min()
    d['val_2_range'] = x['val_2'].max() - x['val_2'].min()
    return pd.Series(d, index=['val_1_mean', 'val_1_std', 'val_2_max',
                               'val_2_min', 'val_2_range'])


df_return = df.groupby(['grp_col_1', 'grp_col_2']).apply(stat_func)

# 계층적 인덱스를 사용하고 싶지 않으면, reset_index 로 return
df_return.reset_index()
df_return.reset_index(level='grp_col_2')
df_return.reset_index(drop=True)

# 계층적 인덱스를 가진 데이터프레임의 여러개의 칼럼에 대해
# 다른 함수를 적용하여 Group By 집계하기
arrays = [['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b'],
          ['c', 'c', 'd', 'd', 'd', 'e', 'e', 'f', 'f', 'f']]

my_index = pd.MultiIndex.from_arrays(arrays, names=['grp_idx_1', 'grp_idx_2'])
df2 = pd.DataFrame({'val_1': np.arange(10),
                    'val_2': np.random.randn(10)},
                   index=my_index)

# 계층적 인덱스 --> Group By 집계.
# df2.groupby(level=[])
df2.groupby(level=['grp_idx_1', 'grp_idx_2']).apply(stat_func)

# (3). GroupBy 를 활용한 그룹 별 가중 평균 구하기
import pandas as pd
import numpy as np

df = pd.DataFrame({'grp_col': ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b'],
                   'val': np.arange(10)+1,
                   'weight': [0.0, 0.1, 0.2, 0.3, 0.4, 0.0, 0.1, 0.2, 0.3, 0.4]})


# (1) GroupBy 를 활용하여 그룹 별 가중 평균 구하기
grouped = df.groupby('grp_col')
weighted_avg_func = lambda g: np.average(g['val'], weights=g['weight'])
grouped.apply(weighted_avg_func)

# (2) 수작업으로 그룹 별 가중 평균 구하기(Split -> Apply -> Combine)
df_a = df[df['grp_col'] == 'a']
df_b = df[df['grp_col'] == 'b']

weighted_avg_a = np.sum(df_a['val'] * df_a['weight'] / np.sum(df_a['weight']))
weighted_avg_b = np.sum(df_b['val'] * df_b['weight'] / np.sum(df_b['weight']))

weighted_avg_ab = pd.DataFrame({'grp_col': ['a', 'b'],
                                'weighted_average': [weighted_avg_a, weighted_avg_b]})


# (4) 결측값을 그룹 평균값으로 채우기
# Fill missing values by Group means

import numpy as np
import pandas as pd

np.random.seed(123)
df = pd.DataFrame({'grp': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
                   'col_1': np.random.randn(8),
                   'col_2': np.random.randn(8)})

df.loc[[1, 6], ['col_1', 'col_2']] = np.nan
df.groupby('grp').mean()

fill_mean_func = lambda g: g.fillna(g.mean())
df.groupby('grp').apply(fill_mean_func)

fill_values = {'a': 1.0, 'b': 0.5}
fill_func = lambda d: d.fillna(fill_values[d.name])
df.groupby('grp').apply(fill_func)

# (5) dataFrame 에 그룹 단위로 통계량을 집계해서 컬럼 추가하기

import numpy as np
import pandas as pd
df = pd.DataFrame({'group_1': ['a', 'a', 'a', 'a', 'a',
                               'b', 'b', 'b', 'b', 'b',],
                  'group_2': ['c', 'c', 'c', 'd', 'd',
                              'e', 'e', 'e', 'f', 'f'],
                  'col': [1, 2, np.NaN, 4, np.NaN,
                          6, 7, np.NaN, 9, 10]})


df['sum_col'] = df.groupby(['group_1', 'group_2']).col.transform('sum')
df['max_col'] = df.groupby(['group_1', 'group_2']).col.transform('max')




# day 2 mission

import pandas as pd
import numpy as np

idx = ['r0', 'r1', 'r2', 'r3', 'r4']
df = pd.DataFrame({
    'c1': np.arange(5),
    'c2': np.random.randn(5)},
    index=idx)

re_idx = ['r0', 'r1', 'r2', 'r5', 'r6']
df_reindex = df.reindex(re_idx)
print(df_reindex)

# 다음의 결괏값이 나오도록 dataframe 을 만들어주세요
# 이 때, index 는 다음과 같은 시계열 데이터이여야 합니다.
date_str = pd.date_range(start='2022-01-25', end='2022-01-29', freq='D')
df = pd.DataFrame(np.arange(10, 60, 10), columns=['c1'], index=date_str)

add_date_str = pd.date_range(start='2022-01-20', end="2022-01-29", freq='D')
df = df.reindex(add_date_str, method='bfill')
print(df)

df_1 = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                     'B': ['B0', 'B1', 'B2'],
                     'C': ['C0', 'C1', 'C2'],
                     'D': ['D0', 'D1', 'D2']},
                    index=[0, 1, 2])

df_2 = pd.DataFrame({'A': ['A3', 'A4', 'A5'],
                     'B': ['B3', 'B4', 'B5'],
                     'C': ['C3', 'C4', 'C5'],
                     'D': ['D3', 'D4', 'D5']},
                    index=[3, 4, 5])

df_3 = pd.DataFrame({'E': ['A6', 'A7', 'A8'],
                     'F': ['B6', 'B7', 'B8'],
                     'G': ['C6', 'C7', 'C8'],
                     'H': ['D6', 'D7', 'D8']},
                    index=[0, 1, 2])

df_4 = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                     'B': ['B0', 'B1', 'B2'],
                     'C': ['C0', 'C1', 'C2'],
                     'E': ['E0', 'E1', 'E2']},
                    index=[0, 1, 3])

pd.concat([df_1, df_2], axis=0)
pd.concat([df_1, df_3], axis=1)
pd.concat([df_1, df_4], axis=0)
pd.concat([df_1, df_4], axis=0, join='inner')
pd.concat([df_1, df_4], axis=1)
pd.concat([df_1, df_4], axis=1, join='inner')
pd.concat([df_1, df_4], axis=1).reindex(df_1.index)

df_1 = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                     'B': ['B0', 'B1', 'B2'],
                     'C': ['C0', 'C1', 'C2'],
                     'D': ['D0', 'D1', 'D2']},
                    index=[0, 1, 2])

S = pd.Series(['S1', 'S2', 'S3'], index=[0, 1, 2], name='S')
pd.concat([df_1, S], axis=1)

S = pd.Series(['S1', 'S2', 'S3', 'S4'], index=['A', 'B', 'C', 'E'])
df_1.append(S, ignore_index=True)

# 과제 4
# 해당 데이터를 로드해 보세요
df_left = pd.DataFrame({'KEY': ['K0', 'K1', 'K2', 'K3'],
                        'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3']})

df_right = pd.DataFrame({'KEY': ['K2', 'K3', 'K4', 'K5'],
                         'C': ['C2', 'C3', 'C4', 'C5'],
                         'D': ['D2', 'D3', 'D4', 'D5']})








# 다음의 파일 3개를 로드하고(1), 각 파일의 행과 열의 개수를 출력(2)해보세요.
# 이 때, 파일의 구분자를 잘 확인하여 로드해보세요.
# test_csv_file.csv
# test_text_file.txt
# text_without_column_name.txt

import pandas as pd
import os
df = pd.read_csv('./rfriend-python-study/data/test_csv_file.csv')
df = pd.read_csv('./rfriend-python-study/data/test_text_file.txt', sep="|")
df = pd.read_csv('./rfriend-python-study/data/text_without_column_name.txt', sep="|", header=None)

# 다음의 파일을 로드하는데, 다음의 제약사항을 지켜 로드해보세요
# train.csv
# 첫번째 행은 빼고 상위 5개의 행(2, 3, 4, 5, 6)만 로드
# PassengerId 컬럼을 Index column 으로 지정
# 가장 상위 row 를 header 로 지정
# ?, ??, N/A, nan, NaN 을 결측값으로 지정

df = pd.read_csv('./rfriend-python-study/data/train.csv',
                 header=0,
                 skiprows=[1],
                 nrows=5,
                 index_col='PassengerId',
                 na_values=["?", "??", "N/A", "nan", "NaN"])


# 과제 2
# 다음의 데이터를 DataFrame 으로 생성 후 csv file 로 만들어 보세요
# 이 때, 아래의 제약조건을 to_csv 함수 내에서 설정하여 만들어 보세요
# 소수점은 둘째자리까지만 설정해주세요
# X3 컬럼은 빼주세요

data = {'ID': ['A1', 'A2', 'A3', 'A4', 'A5'],
        'X1': [1, 2, 3, 4, 5],
        'X2': [3.0132, 4.532, 3.2113, 4.023, 3.543],
        'X3': ['my', 'name', 'is', 'jaehun', 'heo']}


df = pd.DataFrame(data)
df.to_csv('/Users/heojaehun/gitRepo/TIL/Python/daily_Python/rfriend-python-study/data/test.csv',
          float_format="%0.2f",
          columns=['ID', 'X1', 'X2'])

# 위의 DataFrame 의 다음의 attribute 를 조회해 보세요
# transpose
print(df.transpose())

# 행과 열 이름
print(df.axes)

# dataFrame 의 데이터 형태
print(df.dtypes)

# 행과 열의 개수를 튜플로 반환
print(df.shape)

import numpy as np
df = pd.DataFrame({'class_1': ['a', 'a', 'b', 'b', 'c'],
                  'var_1': np.arange(5),
                  'var_2': np.random.randn(5)})

df.index = ['r0', 'r1', 'r2', 'r3', 'r4']
print(df.loc[['r0', 'r1']])
print(df.iloc[0:2])

print(df.loc[:, ['class_1', 'var_2']])


idx = ['r0', 'r1', 'r2', 'r3', 'r4']
df = pd.DataFrame({
    'c1': np.arange(5),
    'c2': np.random.randn(5)},
    index=idx)

slt_idx = ['r0', 'r1', 'r2', 'r5', 'r6']
df.reindex(slt_idx, fill_value=0)

date_idx = pd.date_range(start='2022-01-25',  end='2022-01-29', freq='D')
df = pd.DataFrame({'c1': np.arange(10, 60, 10)}, index=date_idx)
print(df)

# 위의 dataFrame 에서 2022-01-20 ~ 2022-01-24 날짜의 데이터를 추가하고
# 이 때 가장 최근(2022-01-25)의 데이터로 값을 채워주세요
re_idx = pd.date_range(start='2022-01-20', end='2022-01-29', freq='D')
df.reindex(re_idx, method='bfill')

# 위의 dataFrame 에서 2022-01-30 ~ 2022-01-31 날짜의 데이터를 추가하고
# 이 때 가장 최근(2022-01-29)의 데이터로 값을 채워주세요
re_idx = pd.date_range(start='2022-01-25', end='2022-01-30', freq='D')
df.reindex(re_idx, method='ffill')

# 과제 2
# 해당 데이터를 로드해 보세요
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

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 1)
concat_df_1_2 = pd.concat([df_1, df_2])
print(concat_df_1_2)

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 2)
concat_df_1_3 = pd.concat([df_1, df_3], axis=1)
print(concat_df_1_3)

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 3)
print(pd.concat([df_1, df_4], axis=0, join='outer'))

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 4)
print(pd.concat([df_1, df_4], axis=0, join='inner'))

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 5)
print(pd.concat([df_1, df_4], axis=1, join='outer'))

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 6)
print(pd.concat([df_1, df_4], axis=1, join='inner'))

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 7)
print(pd.concat([df_1, df_4], axis=1).reindex(df_1.index))
help(pd.concat)

df_1 = pd.DataFrame({'A': ['A0', 'A1', 'A2'],
                     'B': ['B0', 'B1', 'B2'],
                     'C': ['C0', 'C1', 'C2'],
                     'D': ['D0', 'D1', 'D2']},
                    index=[0, 1, 2])

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 1)
s = pd.Series(['D0', 'D1', 'D2'], name='S')
print(pd.concat([df_1, s], axis=1))

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 2)
s = pd.Series(['S1', 'S2', 'S3', 'S4'], index=['A', 'B', 'C', 'E'])
print(df_1.append(s, ignore_index=True))

# 과제 4
df_left = pd.DataFrame({'KEY': ['K0', 'K1', 'K2', 'K3'],
                        'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3']})

df_right = pd.DataFrame({'KEY': ['K2', 'K3', 'K4', 'K5'],
                         'C': ['C2', 'C3', 'C4', 'C5'],
                         'D': ['D2', 'D3', 'D4', 'D5']})

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 1)
pd.merge(df_left, df_right, how='left', on='KEY')

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 2)
pd.merge(df_left, df_right, how='right', on='KEY')

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 3)
pd.merge(df_left, df_right, how='inner', on='KEY')

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 4)
print(pd.merge(df_left, df_right, how='outer',
               on='KEY', indicator='indicator_info'))

# 과제 5
# 다음의 데이터를 로드하세요
df_left = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                        'B': ['B0', 'B1', 'B2', 'B3']},
                       index=['K0', 'K1', 'K2', 'K3'])

df_right = pd.DataFrame({'C': ['C2', 'C3', 'C4', 'C5'],
                         'D': ['D2', 'D3', 'D4', 'D5']},
                        index=['K2', 'K3', 'K4', 'K5'])

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 1)
pd.merge(df_left, df_right, left_index=True, right_index=True, how='left')

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 2)
pd.merge(df_left, df_right, left_index=True, right_index=True, how='right')

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 3)
pd.merge(df_left, df_right, left_index=True, right_index=True, how='inner')

# 위의 데이터를 활용하여 아래처럼 만들어보세요(-- 4)
pd.merge(df_left, df_right, left_index=True, right_index=True, how='outer')

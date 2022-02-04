############################
# 데이터 정렬(sort , arrange) #
############################
import pandas as pd
personnel_df = pd.DataFrame({'sequence': [1, 3, 2],
                             'name': ['park', 'lee', 'choi'],
                             'age': [30, 20, 40]})


# (1-1) 'sequence' 열을 기준으로 index(axis=0) 오름차순 정렬하기
personnel_df.sort_values(by=['sequence'], axis=0)

# (1-2) 내림차순으로 정렬하기 : ascending=False
personnel_df.sort_values(by=['sequence'], axis=0, ascending=False)

# (1-3) 열 이름을 정렬하기 : axis=1
personnel_df.sort_index(axis=1, ascending=True)
personnel_df.sort_index(axis=1, ascending=False)

# (1-4) DataFrame 자체 내에서 정렬된 상태로 다시 저장하기: inplace=True
personnel_df.sort_values(by=['sequence'], axis=0, inplace=True)
print(personnel_df)

# (1-5) 결측값을 처음에(na_position='first'), 혹은 마지막(na_position='last') 위치에 정렬
import numpy as np
personnel_df = pd.DataFrame({'sequence': [1, 3, np.nan],
                             'name': ['park', 'lee', 'choi'],
                             'age': [30, 20, 40]})

# na_position='first'
personnel_df.sort_values(by=['sequence'], axis=0, na_position='first')

# na_position='last'
personnel_df.sort_values(by=['sequence'], axis=0, na_position='last')

# (2) Tuple 정렬하기 : sorted(tuple, key) method
personnel_tuple = [(1, 'park', 30),
                   (3, 'lee', 20),
                   (2, 'choi', 40)]

# sorted by number
sorted(personnel_tuple, key=lambda x: x[0])

# sorted by name
sorted(personnel_tuple, key=lambda x: x[1])

# sorted ny age
sorted(personnel_tuple, key=lambda x: x[2])

# 내림차순으로 정렬하고 싶으면, reverse=True 설정

#######################################################
# Series, DataFrame 행, 열 생성(creation)                #
# 선택(selection, slicing, indexing), 삭제(drop, delete) #
########################################################

# (1-1) Series 생성 및 Series 원소 선택
import numpy as np
import pandas as pd

s = pd.Series([0, 1, 2, 3, 4])
print(s[0])
print(s[:3])
print(s[s >= s.mean()])
print(s[[4, 2, 0]])

# (1-2) index 에 label 을 할당해준 Series 를 만들어보고,
#     특정 index label 을 지정해서 indexing 을 해보자

s_ix = pd.Series([0, 1, 2, 3, 4], index=['a', 'b', 'c', 'd', 'e'])
print(s_ix[['a', 'b', 'c']])
print(s_ix.get(['a', 'b', 'e']))
s_ix['a'] = 100

# (1-3) 특정 index label 이 Series 에 들어있는지 확인해보자
print('a' in s_ix)
print('x' in s_ix)

# (2) DataFrame 행과 열 생성, 선택, 삭제
# creation, selection, drop of row and column

import pandas as pd
df = pd.DataFrame({'C1': [0, 1, 2, 3],
                   'C2': [4, 5, 6, 7],
                   'C3': [8, 9, 10, np.nan]},
                  index=['R1', 'R2', 'R3', 'R4'])

print(df.index)
print(df.columns)

# (2-1) pd.DataFrame(df, index=[], columns=[]) 형식으로 slicing
df_R1R3 = pd.DataFrame(df, index=['R1', 'R3'])
print(df_R1R3)

df_C1C3 = pd.DataFrame(df, columns=['C1', 'C3'])
print(df_C1C3)

df_R1R3_C1C3 = pd.DataFrame(df,  index=['R1', 'R3'], columns=['C1', 'C3'])
print(df_R1R3_C1C3)

# (2-2) df 에서 컬럼 이름을 직접 지정하여 선별
print(df[['C1', 'C2']])

# df 에 새로운 컬럼 만들기
# - 1. df['new_column'] = ...
df['C4'] = df['C1'] + df['C2']

# - 2. assign() method
df = df.assign(C5=df['C1'] + df['C2'])
df = df.assign(C5=lambda x: x.C1 * x.C2)

# (2-3) df 의 컬럼 삭제
# - 1 df.drop[xx, 1]
df_drop_C4C5 = df.drop(['C4', 'C5'], 1)
print(df_drop_C4C5)

# - 2 del function
del df['C4']
del df['C5']
print(df)

# (3) df 의 행(row) 와 열(column) 을 선택
# - 1. df.['xx'][0:2]
print(df['C1'])
print(df.C1)
print(df[0:2])
print(df['C1'][0:2])
print(df.C1[0:2])

# - 2. index label 가지고 행(row) 선택시, df.loc['xx'] 사용
print(df.loc['R1'])
print(df.loc[['R1', 'R2']])

# - 3. index 의 label 이 아니라 정수(integer) 로 indexing 을 하려면 df.iloc[int] 를 사용
print(df.iloc[0])
print(df.iloc[0:2])

# - 4. df 의 행(row) indexing 할 때, df[0:2] 처럼 행의 범위를 ':' 로 설정 해도 가능
# ** 주의 : df[0] 처럼 정수 값 지정 시, key error 발생
try:
    df[0]
except KeyError:
    print("Key Error 발생")

print(df[0:2])

# 조건을 부여해서 선택 가능
print(df[df['C1'] <= 1.0])

# 선택한 컬럼을 벡터 객체로 만들어 놓고, DataFrame 에서 벡터 객체에 들어있는 컬럼만 선별
df_col_selector = ['C1', 'C2']
print(df[df_col_selector])

###########################
## 다차원 배열 ndarray 만들기 ##
###########################






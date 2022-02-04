# 2022-02-02.py

import numpy as np
import pandas as pd
from pandas import DataFrame

data = DataFrame({'cust_id': ['c1', 'c1', 'c1', 'c2', 'c2', 'c2', 'c3', 'c3', 'c3'],
                  'prod_cd': ['p1', 'p2', 'p3', 'p1', 'p2', 'p3', 'p1', 'p2', 'p3'],
                  'grade' : ['A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B'],
                  'pch_amt': [30, 10, 0, 40, 15, 30, 0, 0, 10]})

# (1) 데이터 재구조화: data.pivot(index, columns, values)
# 위의 데이터를, 행에는 cust_id,
# 열(column) 에는 상품코드(prd_cd)
# 행과 열이 교차하는 칸에는 구매금액(pch_amt) 이 위치하도록 데이터 구조 변경

data_pivot = data.pivot(index='cust_id', columns='prod_cd', values='pch_amt')
print(data_pivot)

# (2) 데이터 재구조화: pd.pivot_table(data, index, columns, values, aggfunc)
pd.pivot_table(data, index='cust_id', columns='prod_cd', values='pch_amt')

# index 가 2개 이상인 경우
data.pivot(index=['cust_id', 'grade'], columns='prod_cd', values='pch_amt')
pd.pivot_table(data, index=['cust_id', 'grade'], columns='prod_cd', values='pch_amt')

# columns 가 2개 이상인 경우
data.pivot(index=['cust_id'], columns=['prod_cd', 'grade'], values='pch_amt')
pd.pivot_table(data, index=['cust_id'], columns=['prod_cd', 'grade'], values='pch_amt')

# Pivot() 함수는 중복값이 있는 경우, ValueError 를 반환
# 반면에 pd.pivot_table() 은 aggfunc=np.sum 혹은 aggfunc=np.mean 과 같이 집계

data.pivot(index='grade', columns='prod_cd', values='pch_amt')
pd.pivot_table(data, index='grade', columns='prod_cd',
               values='pch_amt', aggfunc=np.sum)

pd.pivot_table(data, index='grade', columns='prod_cd',
               values='pch_amt', aggfunc=np.mean)

# # pivot_table(aggfunc=np.mean), by default
pd.pivot_table(data, index='grade', columns='prod_cd',
               values='pch_amt', aggfunc=np.sum, margins=True)

################################################ ##
## 데이터 재구조화(reshaping data) :                 ##
##  pd.DataFrame.stack(), pd.DataFrame.unstack() ##
###################################################

import numpy as np
import pandas as pd
mul_index = pd.MultiIndex.from_tuples([('cust_1', '2015'), ('cust_1', '2016'),
                                       ('cust_2', '2015'), ('cust_2', '2106')])

df = pd.DataFrame(data=np.arange(16).reshape(4, 4),
                  index=mul_index,
                  columns=['prd_1', 'prd_2', 'prd_3', 'prd_4'],
                  dtype='int')

# 칼럼의 level 은 1개 밖에 없으므로 stack(level=-1) 을 별도로 명기하지 않아도 됩니다.
data_stacked = df.stack()
data_stacked['cust_2']['2015'][['prd_1', 'prd_2']]

# 결측값이 있는 데이터셋을 stack() 할 때, 결측값을 제거할지(dropna=True)
# 결측값을 NaN으로 유지할지, 설정할 수 있는 stack 확인
df.loc[['cust_2'], ['prd_4']] = np.nan

df.stack(dropna=False)
df.stack(dropna=True)

# unstack
# level 이 3개 있는 MultiIndex 임
# unstack(level=-1), unstack(level=0), unstack(level=1) 별로 어떤 level 이 컬럼으로 이동해서
# unstack() 되는지 유심히 살펴보기

data_stacked.unstack(level=-1)
data_stacked.unstack(level=0)
data_stacked.unstack(level=1)

#
data_stacked_unstacked = data_stacked.unstack(level=-1)
data_stacked_unstacked_df = data_stacked_unstacked.reset_index()

data_stacked_unstacked_df.rename(columns={'level_0': 'custID',
                                          'level_1': 'year'}, inplace=True)


#############
## pd.melt ##
#############

import numpy as np
import pandas as pd

data = pd.DataFrame({'cust_ID': ['C_001', 'C_001', 'C_002', 'C_002'],
                     'prd_CD': ['P_001', 'P_002', 'P_001', 'P_002'],
                     'pch_cnt': [1, 2, 3, 4],
                     'pch_amt': [100, 200, 300, 400]})

data_melt = pd.melt(data,
                    id_vars=['cust_ID', 'prd_CD'],
                    var_name='pch_CD',
                    value_name='pch_value')

data_melt_pivot = pd.pivot_table(data_melt,
                                 index=['cust_ID', 'prd_CD'],
                                 columns='pch_CD',
                                 values='pch_value',
                                 aggfunc=np.mean)

#######################
## pd.wide_to_long() ##
#######################
import numpy as np
import pandas as pd
np.random.seed(10)

data_wide = pd.DataFrame({"C1prd1": {0: "a", 1: "b", 2: "c"},
                          "C1prd2": {0: "d", 1: "e", 2: "f"},
                          "C2prd1": {0: 2.5, 1: 1.2, 2: .7},
                          "C2prd2": {0: 3.2, 1: 1.3, 2: .1},
                          "value": dict(zip(range(3), np.random.randn(3)))})

data_wide["seq_no"] = data_wide.index

df_wide_to_long = pd.wide_to_long(data_wide,
                                  stubnames=['C1', 'C2'],
                                  i=['seq_no'],
                                  j='prd')

print(df_wide_to_long.index)
print(df_wide_to_long.columns)


# pd.crosstab() 사용해 교차표(cross tabulation)
# 범주형 변수로 되어있는 요인(factors)별로 교차분석(cross tabulations) 해서,
# 행, 열 요인 기준 별로 빈도를 세어서 도수분포표(frequency table), 교차표(contingency table) 을 만들어줌

import pandas as pd
data = pd.DataFrame({'id': ['id1', 'id1', 'id1', 'id2', 'id2', 'id3'],
                     'fac_1': ['a', 'a', 'a', 'b', 'b', 'b'],
                     'fac_2': ['d', 'd', 'd', 'c', 'c', 'd']})

# pd.crosstab 의 행과 열에 위치에는 array 형식의 데이터가 들어감
# (1) 교차표 만들기 : pd.crosstab(index, columns)
pd.crosstab(data.fac_1, data.fac_2)
pd.crosstab(data.id, data.fac_1)
pd.crosstab(data.id, data.fac_2)

# (2) Multi-index, Multi-level 로 교차표 만들기 : pd.crosstab([id1, id2], [col1, col2])
pd.crosstab(data.id, [data.fac_1, data.fac_2])
pd.crosstab([data.fac_1, data.fac_2], data.id)

# (3) 교차표의 행 이름, 열 이름 부여 : pd.crosstab(rownames=['xx'], colnames=['aa'])
pd.crosstab(data.id, [data.fac_1, data.fac_2],
            rownames=['id_num'],
            colnames=['a_b', 'c_d'])

# (4) 교차표의 행 합, 열 합 추가하가ㅣ : pd.crosstab(margins=True)
pd.crosstab(data.id, [data.fac_1, data.fac_2], margins=True)

# (5) 구성비율로 교차표 만들기 : pd.crosstab(normalize=True)
pd.crosstab(data.id, [data.fac_1, data.fac_2])




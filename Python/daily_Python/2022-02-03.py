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
# NumPy 로 ndarray 라는 매우 빠르고 공간 효율적인 벡터 연산이 가능한 다차원 배열(n-dimentional array)를 만들 수 있음
# 선형 대수(Linear Algebra), 무작위 난수 생성 등에 NumPy 를 사용

import numpy as np

# array() 로 ndarray 만들기
arr1 = np.array([1, 2, 3, 4, 5])
print(arr1)

# list 객체 선언 후에 np.array() 를 사용해서 배열 변환 가능
data_list = [6, 7, 8, 9, 10]
arr2 = np.array(data_list)
print(arr2)

# 같은 길이의 여러개의 리스트(lists) 를 가지고 있는 리스트도
# np.array() 를 사용해서 배열 변환 가능
data_lists = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
arr12 = np.array(data_lists)
print(arr12)

# 다차원 배열의 차원과 그룹 안의 원소들의 크기를 확인할 때, array.shape 함수 사용
# array.dtype 함수 사용하여 데이터 유형 확인 가능
print(arr12.shape)
print(arr12.shape[0])
print(arr12.shape[1])
print(arr12.dtype)

# np.asarray() 를 사용해서 array 를 만들기도 함
a = [1, 2, 3, 4, 5]
type(a)
a = np.asarray(a)
print(type(a))

# ** np.asarray() 는 이미 ndarray 가 있다면, 복사(copy) 를 하지 않음
b = np.array([1, 2])
print(np.asarray(b) is b)

# 만약 데이터 형태(data type)이 이미 설정이 되어 있다면, np.asarray() 를 사용해서
# array 로 변환하려고 할 경우 데이터 형태가 다를 경우에만 복사(copy) 됨

c = np.array([1, 2], dtype=np.float32)
print(np.asarray(c, dtype=np.float32) is c) # True
print(np.asarray(c, dtype=np.float64) is c) # False

# float 데이터 형태의 원소를 가지는 배열을 만들고 싶은 경우,
# np.asfarray() 함수 사용

d = [6, 7, 8, 9, 10]
print(np.asfarray(d))

# np.asarray_chkfinite() 함수 사용시 배열로 만들려고 하는 데이터 input 에 결측값(NaN) 이나
# 무한수(infinite number) 가 들어있을 경우 'ValueError' 를 반환하게 할 수 있음
# np.nan 으로 결측값을 넣어보고, np.inf 로 무한수를 추가해서 확인

e = [11, 12, 13, 14, 15]
np.asarray_chkfinite(e, dtype=float)

e_2 = [11, 12, 13, np.nan, 15]
try:
    np.asarray_chkfinite(e_2, dtype=float)
except ValueError:
    print("Value Error 발생")


e_3 = [11, 12, 13, 14, np.inf]
try:
    np.asarray_chkfinite(e_3, dtype=float)
except ValueError:
    print("Value Error 발생")

# np.zeros(), np.ones(), np.empty() 함수는 괄호 안에 쓴 숫자 개수만큼 0, 1, 비어있는 배열 공간 생성
print(np.zeros(5))
print(np.ones(10))
print(np.empty(10))

# np.zeros(), np.ones(), np.empty() 안에 tuple 을 입력하면, 다차원 배열 만들 수 있음
np.zeros((2, 5))
np.ones((2, 5))
np.empty((4, 3))

# np.arange() 는 0 부터 괄호안의 숫자 만큼의 정수 배열 값을 '배열' 로 반환
f = np.arange(10)
print(f)

# np.zeros_like(), np.ones_like(), np.empty_like()
# 이미 있는 array 와 동일한 모양과 데이터 형태를 유지한 상태에서 각 '0', '1', '빈 배열' 반환
f_2_5 = f.reshape(2, 5)
np.zeros_like(f_2_5)
np.ones_like(f_2_5)
np.empty_like(f_2_5)

# np.identity(), np.eye() 함수를 사용하면
# 대각성분은 '1' 이고, 나머지 성분은 '0' 으로 구성된 정방행렬인 항등행렬(identity matrix) 혹은
# 단위 행렬을 만들 수 있음

np.identity(5)
np.eye(5)

###########################
## 무작위 표본 추출, 난수 만들기 ##
############################

# 개수가 5개인 무작위 샘플
import numpy as np
np.random.normal(size=5)
np.random.normal(size=5)  # array with different random numbers

# seed : 난수 생성 초기값 부여
np.random.seed(50)
np.random.normal(size=5)

np.random.seed(50)
np.random.normal(size=5)

# size = 샘플 생성(추출) 개수 및 array shape 설정
np.random.normal(size=2)
np.random.normal(size=(2, 3))

# 이항 분포로부터 무작위 표본 추출(Random sampling from Binomial Distribution)
np.random.binomial(n=1, p=0.5, size=20)

# 초기하분포에서 무작위 표본 추출(Random sampling from Hypergeometric distribution)
# good 이 5개, bad 가 20 개인 모집단에서 5개의 샘플을 무작위로 비복원추출 하는 것을 100번 시뮬레이션 한 후에
# 도수분포표를 구해서, 막대그래프로 나타내보자

np.random.seed(seed=100)
rand_hyp = np.random.hypergeometric(ngood=5, nbad=20, nsample=5, size=100)
unique, counts = np.unique(rand_hyp, return_counts=True)

print(np.asarray((unique, counts)).T)

import matplotlib.pyplot as plt
plt.bar(unique, counts, width=0.5, color='blue', align='center')

# (1-3) 포아송 분포로부터 무작위 표본 추출: np.random.poisson(lam, size)
# 일정한 단위 시간, 혹은 공간에서 무작위로 발생하는 사건의 평균 회수인 lambda 가 20 인 포아송 분포로부터
# 100개의 난수를 만들어보자
# 그 후에 도수를 계산하고, 막대그래프로 분포를 그려보자

np.random.seed(seed=100)
rand_pois = np.random.poisson(lam=20, size=100)
unique, counts = np.unique(rand_pois, return_counts=True)

print(np.asarray((unique, counts)).T)
plt.bar(unique, counts, width=0.5, color='red', align='center')

# (2) 연속형 확률분포(continuous probability distribution)
# (2-1) 정규분포로부터 무작위 표본 추출
np.random.seed(100)
mu, sigma = 0.0, 3.0
rand_norm = np.random.normal(mu, sigma, size=100)
np.mean(rand_norm)
np.std(rand_norm)

import matplotlib.pyplot as plt
plt.hist(rand_norm)

# (2-2) t-분포로 부터 무작위 표본 추출
np.random.seed(100)
rand_t = np.random.standard_t(df=3, size=100)
print(rand_t)

import matplotlib.pyplot as plt
plt.hist(rand_t, bins=20)

# (2-3) 균등 분포로부터 무작위 표본 추출 : np.random.uniform(low, high, size)

np.random.seed(100)
rand_unif = np.random.uniform(low=0.0, high=10.0, size=100)
plt.hist(rand_unif, bins=10)

# (2-4) 이산형 균등분포에서 정수형 무작위 표본 추출
np.random.seed(100)
rand_int = np.random.randint(low=0, high=10+1, size=100)
print(rand_int)

# (2-5) F-분포로 부터 무작위 표본 추출: np.random.f(dfnum, dfden, size)
# 자유도1이 5, 자유도2가 10인 F-분포로 부터 100개의 난수를 만들고,
# 히스토그램을 그려서 분포 확인

np.random.seed(100)
rand_f = np.random.f(dfnum=5, dfden=10, size=100)
print(rand_f)


import matplotlib.pyplot as plt
plt.hist(rand_f, bins=20)

# (2-6) 카이제곱분포로 부터 무작위 표본 추출 : np.random.chisquare(df, size)
# df : 자유도
rand_chisq = np.random.chisquare(df=2, size=100)

import matplotlib.pyplot as plt
plt.hist(rand_chisq, bins=20)

################################
## ndarray 데이터 형태 지정 및 변경 ##
################################
# (1) 데이터 형태의 종류(Data Type)
# 크게 숫자형과 문자형
# 숫자형 --> bool 자료형, 정수형, 부호 없는 정수형, 부동소수형, 복소수형

# (2) Numpy 데이터 형태 지정해주기
# (2-1) np.array([xx,xx], dtype=np.Type)
import numpy as np
x_float64 = np.array([1.4, 2.6, 3.0, 4.9, 5.32], dtype=np.float64)
print(x_float64.dtype)
print(x_float64)

# (2-2) np.array([xx, xx], dtype=np.'Type Code')
x_float64_1 = np.array([1.4, 2.6, 3.0, 4.9, 5.32], dtype='f8')
print(x_float64_1.dtype)

# (2-3) np.Type([xx, xx])
x_float64_1 = np.float64([1.4, 2.6, 3.0, 4.9, 5.32])
print(x_float64_1)

# (3) 데이터 형태 변환
# (3-1) float64 -> int64 : x_float64.astype(np.int64)
x_int64 = x_float64.astype(np.int64)
print(x_int64.dtype)
print(x_int64)

# (3-2) float64 -> int64 로 변환하기 : np.int64(x_float64)
x_int64_2 = np.int64(x_float64)
print(x_int64_2.dtype)
print(x_int64_2)

# (3-3) 부동소수형(float64) 를 문자열(string)으로 반환
x_string = x_float64.astype(np.string_)
print(x_string.dtype)
print(x_string)

# (3-4) 문자열(string) 을 부동소수형(float64)로 변환하기
x_string.astype(np.float64)

# (4) Python 의 int 와 NumPy 의 int64 비교
# methods, attribute 는 내장 python int 타입보다 NumPy int64 가 8배 정도 많음








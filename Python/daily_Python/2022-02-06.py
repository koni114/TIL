###########################
# 배열과 배열, 배열과 스칼라 연산 #
###########################
# 두 배열에 대해 vectorization 으로 빠르게 연산 가능
# 두 배열의 차원이 다른 경우, NumPy 는 BroadCasting 연산 수행

import numpy as np
x = np.array([1, 1, 2, 2])
y = np.array([1, 2, 3, 4])

# (1) 배열과 스칼라의 산술 연산
print(y + 1)
print(y - 1)
print(y / 2)
print(y // 2)
print(y ** 2)

# NumPy와 Pure python 의 속도 비교
# NumPy 가 Pure Python 과 비교했을 떄, 62.4배 더 빠름
a = np.arange(1000000)
# %timeit a + 1              # 559 µs ± 36 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
# %timeit [i+1 for i in a]   # 349 ms ± 16 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# 같은 크기 배열 간 산술 연산
# element-wise multiplication

print(x + y)
print(x - y)
print(y ** x)

# 배열 간 비교 연산
# 원소 단위로 비교 연산을 만족하면 True 반환, 만족하지 않으면 False 반환
# 배열 단위 비교 연산 --> np.array_equal(x, y)

x = np.array([1, 1, 2, 2], dtype='float64')
y = np.array([1, 2, 3, 4], dtype='float64')

np.equal(x, y)
np.not_equal(x, y)
np.greater(x, y) # x > y
np.greater_equal(x, y) # x >= y
np.less(x, y) # x < y
np.less_equal(x, y)
np.array_equal(x, y)

# 배열 간 할당 연산
m = np.array([1, 1, 2, 2])
n = np.array([1, 2, 3, 4])

m += n
print(m)

m = np.array([1, 1, 2, 2])
m -= n
print(m)

m **= n
print(m)

# 배열 간 논리 연산
# - np.logical_and(a, b) : 두 배열의 원소가 모두 0 이 아니면 True 반환
# - np.logical_or(a, b)  : 두 배열의 원소 중 하나라도 '0' 이 아니면 True 반환
# - np.logical_xor(a, b) : 두 배열의 원소가 서로 같지 않으면 True 반환

a = np.array([1, 1, 0, 0])
b = np.array([1, 0, 1, 0])

np.logical_and(a, b)
np.logical_or(a, b)
np.logical_xor(a, b)

# 소속 여부 판단 연산
p = "P"
q = np.array(["P", "Q"])
r = np.array(["R", "S"])

print(p in q)
print(p in r)
print(p not in q)

# 배열의 크기가 다른 경우에는 ValueError 발생
x4 = np.arange(4)
x5 = np.arange(5)

try:
    x4 + x5
except ValueError:
    print("x4 와 x5의 배열 길이가 맞지 않습니다.")

##########################################
## 다른 차원의 배열 간 산술연산 시 Broadcasting ##
##########################################

# 1. Broadcasting over axis 1 with a Scalar

import numpy as np
a_ar = np.array([1, 2, 3, 4], dtype='float64')
print(a_ar + 1)

# Pandas 의 DataFrame 도 Scalar 산술 연산 시에 Broadcasting 이 적용

import pandas as pd
a_df = pd.DataFrame({'x1': [1, 2, 3, 4],
                     'x2': [5, 6, 7, 8]})
print(a_df + 1)

# 2. Broadcasting over axis 0 with a 1-D array
b = np.arange(12).reshape((4, 3))
c = np.array([0, 1, 2])

print(b + c)

# BroadCasting 을 수행하려면 기준 축에 있는 원소의 크기가 서로 같아야 짝을 맞추어서 확산이 가능
# 맞지 않으면 다음과 같은 ValueError 발생
b = np.arange(12).reshape((4, 3))
d = np.array([0, 1, 2, 3])
try:
    b + d
except Exception as e:
    print(e)

# operands could not be broadcast together with shapes (4,3) (4,)

# 3. Broadcasting over axis 1 with a 2-D array
# 가로 방향으로 column 을 복사해가면서 broadcasting 하는 예

b = np.arange(12).reshape((4, 3))
e = np.array([0, 1, 2, 3]).reshape((4, 1))
print(b + e)

# 4. Broadcasting over axis 0 with a 3-D array

f = np.arange(24).reshape((2, 4, 3))
g = np.ones((4, 3))

print(f + g)

#########################
## NumPy 배열에 축 추가하기 ##
#########################
# NumPy Array 에 새로운 축 추가하는 2가지 방법
# (1) indexing 으로 길이가 1인 새로운 축 추가하기. arr(:, np.newaxis, :)
# ex) (3, 4) -> (3, 4, 1)
# ex) (3, )  -> (3, 1)

import numpy as np
a = np.array([1, 2, 3, 4])
print(a.shape)

a_4_1 = a[:, np.newaxis]
print(a_4_1.shape)

b = np.arange(12).reshape(3, 4)
print(b.shape)

b_3_4_1 = b[:, :, np.newaxis]
print(b_3_4_1.shape)

# (2) np.tile(arr, reps) method
# arr 에는 배열을, reps 에는 반복하고자 하는 회수를 넣어줌

A = np.array([0, 1, 2, 3])
print(A.shape)

A_8 = np.tile(A, 2)
print(A_8.shape)
print(A_8)

A_2_8 = np.tile(A, (2, 2))
print(A_2_8)
print(A_2_8.shape)

##########################################
## 행렬의 행과 열 바꾸기, 축 바꾸기, 전치행렬: a.T ##
## np.transpose(a), np.swapaxes(a, 0, 1) ##

# NumPy 의 행렬 전치를 위해 3가지 방법 사용 가능
# (1) a.T
# (2) np.transpose(a) method
# (3) np.swapaxes(a, 0, 1) method


import numpy as np
a = np.arange(15).reshape(3, 5)
print(a.T)
print(np.transpose(a))
print(np.swapaxes(a, 0, 1))

# 행렬 내적 (np.dot) 계산 a^T * a
print(np.dot(a.T, a))

# (2-1) Transposing 3D array : a.T attribute
b = np.arange(24).reshape(2, 3, 4)
print(b.T)
print(b.T.shape)

# (2-2) Transposing 3D array : np.transpose() method
b = np.arange(24).reshape(2, 3, 4)
b_T = np.transpose(b, (2, 1, 0))
print(b_T)
print(b_T.shape)

# (2-3) Transposing 3D array : np.swapaxes() method
b_T = np.swapaxes(b, 0, 2)
print(b_T.shape)
print(b_T)

#####################################
## 배열의 일부분 선택하기                ##
## indexing and slicing an ndarray ##
#####################################

# (1) Indexing a subset of 1D array : a[from : to]
import numpy as np
a = np.arange(10)

print(a[0])
print(a[0:5])

b_idx = a[0:5]
b_idx[0:3] = 10
print(b_idx)
print(a)

# (1-3) indexing 한 배열을 복사하기 : arr[0:5].copy()
a = np.arange(10)
b = a[0:5].copy()
b[0] = 100

print(b)
print(a)

# (2-1) Indexing and Slicing 2D array with comma ',' : d[0:3, 1:3]
d = np.arange(20).reshape(4, 5)
print(d[0])
print(d[0:2])
print(d[0, 4])
print(d[0:3, 1:3])

# (2-2) Indexing and Slicing 2D array with square bracket '[ ][ ]' : d[0:3][1:3]
# comma 를 사용해서 slicing 하는 것과 차이가 있음
# 대괄호 두개 '[][]' 는 첫 번째 대괄호 '[]' 에서 indexing 을 먼저 하고 나서,
# 그 결과를 가져다가 두번째 대괄호 '[]' 에서 한번 더 indexing 을 하게 됨

print(d[0][4])
print(d[0:3][1:3]) # 반드시 주의!!

# (3-1) Indexing and Slicing of 3D array : e[0, 0, 0:3]
e = np.arange(24).reshape(2, 3, 4)
e_idx_0 = e[0]
e_idx_0_0 = e[0, 0]
e_idx_0_0_2 = e[0, 0, 0:3]

# (3-2) 축 하나를 통째로 가져오기( indexing the entire axis by using colon ':')
print(e[0, :, 0:3])

################################################################
## [Python Numpy] Boolean 조건문으로 배열 인덱싱 (Boolean Indexing) ##
################################################################

import numpy as np
arr = np.arange(20).reshape(5, 4)

axis_ABC = np.array(['A', 'A', 'B', 'C', 'C'])
print(axis_ABC)

print(axis_ABC == 'A')
print(arr[axis_ABC == 'A'])
print(arr[axis_ABC == 'A', :2])

print(arr[(axis_ABC == 'A') | (axis_ABC == 'B')])
print(arr[(axis_ABC != 'A') & (axis_ABC != 'B')])


try:
    print(arr[(axis_ABC != 'A') and (axis_ABC != 'B')]) # error
except Exception as e:
    print("Value Error!")



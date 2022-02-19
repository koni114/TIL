# 다차원 배열을 1차원 배열로 평평하게 펴주는 ravel()
#                                 flatten()

import numpy as np
x = np.arange(12).reshape(3, 4)

# np.ravel(x, order='C') : C와 같은 순서로 인덱싱하여 평평하게 배열(default)
np.ravel(x, order='C')

# np.ravel(x, order='F') : Fortran 과 같은 순서로 인덱싱하여 평평하게 배열
# 아래의 결과는 세로로 평평하게 배열
np.ravel(x, order='F')

# np.ravel(x, order='K') : 메모리에서 발생하는 순서대로 인덱싱하여 평평하게 배열
np.ravel(x, order='K')

# 3차원 배열 같은 경우에는 order 매개변수 사용시 주의
# 아래에 2*3*2 의 3차원 배열에 대해서 축이 어떻게 설정되어있느냐에 따라 order='C' 와 order='K' 선택
y = np.arange(12).reshape(2, 3, 2)
np.ravel(y, order='C')
np.ravel(y, order='F')

z = np.arange(12).reshape(2, 3, 2).swapaxes(1, 2)

np.ravel(y, order='K')

# 배열을 옆으로, 위 아래로 붙이기
# np.r_, np.c_, np.hstack(), np.vstack()
# np.column_stack(), np.concatenate(axis=0), np.concatenate(axis=1)

# 두 배열을 왼쪽에서 오른쪽으로 붙이기
# np.r_[a, b]
# np.hstack([a, b]) --> horizontal
# np.concatenate((a, b), axis=0)

import numpy as np
import pandas as pd
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.r_[a, b])
print(np.hstack([a, b]))
print(np.concatenate((a, b), axis=0))

# 두 배열을 위에서 아래로 붙이기
# np.r_[[a], [b]]
# np.vstack([a, b]) --> Vertical
# np.concatenate((c, d), axis=1)
# --> 1D 배열은 AxisError 발생. 2D 이상 배열은 에러 없이 잘됨

print(np.r_[[a], [b]])
print(np.vstack([a, b]))
try:
    np.concatenate((a, b), axis=1)
except Exception as e:
    print(e)

c = np.array([[0, 1, 2], [3, 4, 5]])
d = np.array([[6, 7, 8], [9, 10, 11]])
np.concatenate((c, d), axis=1)

# 두 개의 1차원 배열을 칼럼으로 세로로 붙여서 2차원 배열 만들기
# np.c_[a, b]
# np.column_stack([a, b])
# np.concatenate((c.T, d.T), axis=1)
print(np.c_[a, b])
print(np.column_stack([a, b]))
print(np.concatenate((c.T, d.T), axis=1))

# numpy 집합함수(set functions)
# 한 개, 혹은 두 개의 1차원 ndarray 집합에 대해
# (1) unique(x) : 배열 내 중복된 원소 제거 후 유일한 원소를 정렬하여 반환
import numpy as np
x = np.array([1, 2, 3, 1, 2, 4])
np.unique(x)

# (2) intersect1d(x, y) : 두 개의 배열 x, y 의 교집합을 정렬하여 반환
x = np.array([1, 2, 3, 4])
y = np.array([3, 4, 5, 6])
np.intersect1d(x, y)

# (3) union1d(x, y) : 두 개의 배열 x, y의 합집합을 정렬하여 반환
np.union1d(x, y)

# (4) in1d(x, y) : 첫 번쨰 배열 x가 두 번째 배열 y의 원소를 포함하고 있는지 여부를 불리언 배열을 반환
np.in1d(x, y)

# (5) setdiff1d(x, y) : 첫 번째 배열 x로 부터 두 번째 배열 y를 뺸 차집합을 반환
np.setdiff1d(x, y)

# (6) setxor1d(x, y) : 두 배열 x, y의 합집합에서 교집합을 뺀 대칭차집합을 반환
np.setxor1d(x, y)

# numpy 최소, 최대, 조건 색인값 : np.argmin(), np.argmax(), np.where()
# (1) 최솟값(min), 최대값(max) : np.min(), np.max()

import numpy as np
x = np.array([5, 4, 3, 2, 1, 0])
print(x.min())
print(np.min(x))
print(x.max())
print(np.max(x))

# (2) 최소값, 최대값의 색인 위치: np.argmin(), np.argmax()
x.argmin()
np.argmin(x)
x.argmax()
np.argmax(x)

# (3) 조건에 맞는 값의 색인 위치: np.where()
np.where(x >= 3)

# (4) 조건에 맞는 값을 indexing 하기: x[np.where()]
print(x[np.where(x >= 3)])

# (5) 조건에 맞는 값을 특정 다른 값으로 변환하기
print(np.where(x >= 3, 3, x))

# numpy array 정렬, 거꾸로 정렬, 다차원 배열 정렬
# 1차원 배열 정렬: np.sort(x)

import numpy as np
x = np.array([4, 2, 6, 5, 1, 3, 0])
np.sort(x) # 원래 배열은 그대로, 정렬 결과 복사본 반환
x.sort()   # 배열 자체를 정렬

# 1차원 배열 거꾸로 정렬: np.sort(x)[::-1], x[np.argsort(-x)]
x = np.array([4, 2, 6, 5, 1, 3, 0])
x_reverse_1 = np.sort(x)[::-1]
print(x_reverse_1)

# 2차원 배열 열 축 기준으로 정렬: np.sort(x, axis=1)
x = np.array([4, 2, 6, 5, 1, 3, 0])
x_reverse_2 = x[np.argsort(-x)]
print(x_reverse_2)

# 2차원 배열 행 축 기준으로 정렬: np.sort(x, axis=0)
x2 = np.array([[2, 1, 6],
               [0, 7, 4],
               [5, 3, 2]])

x2_sort_axis_1 = np.sort(x2, axis=1)
print(x2_sort_axis_1)

# 2차원 배열 행 축 기준으로 거꾸로 정렬: np.sort(x, axis=0)[::-1]
x2 = np.array([[2, 1, 6],
               [0, 7, 4],
               [5, 3, 2]])

x2_sort_axis_0_reverse = np.sort(x2, axis=0)[::-1]
print(x2_sort_axis_0_reverse)


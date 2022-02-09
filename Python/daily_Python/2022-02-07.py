######################################
## 정수 배열을 사용해서 다차원 배열 인덱싱 하기 ##
######################################

# 정수 배열을 indexer 로 사용해서 다차원 배열로부터 Indexing 하는 방법
# Fancy Indexing 에 대해 알아보자
# Fancy Indexing 은 copy 를 만듬

# (1) 특정 순서로 다차원 배열의 행을 Fancy Indexing 하기
# `axis 0` 의 위에서부터 아래 방향으로 '1' 과 '2' 위치의 행 전체를 fancy indexing
import numpy as np
a = np.arange(15).reshape(5, 3)
print(a[[1, 2]])

# 'axis 0' 의 아래에서 위 방향으로 fancy indexing --> '-'
print(a[[-1, -2]])

# (2) 특정 순서로 다차원 배열의 행(row) 과 열(column) 을 Fancy Indexing 하기
print(a[[0, 2, 4]][:, [0, 2]])
print(a[np.ix_([0, 2, 4], [0, 2])])

# Fancy Indexing 은 View 가 아니라 copy 생성
a_copy = a[np.ix_([0, 2, 4], [0, 2])]
a_copy[0, :] = 100

print(a_copy)
print(a)

#################################
## 범용 함수(universal functions) ##
##################################
import numpy as np
a = np.array([-4.62, -2.19, 0, 1.57, 3.40, 4.06])

# np.round : N 소수점 자릿수까지 반올림
print(np.round(a, 1))
print(np.round(a))

# np.rint(a) : 가장 가까운 정수로 올림 혹은 내림
np.rint(a)

# np.fix(a) : 0 방향으로 가장 가까운 정수로 올림 혹은 내림
print(np.fix(a))

# np.ceil(a) : 올림
print(np.ceil(a))

# np.floor(a) : 내림
print(np.floor(a))

# np.trunc(a) : 각 원소의 소수점 부분은 잘라버리고 정수값만 남김
print(np.trunc(a))

b = np.array([1, 2, 3, 4])
c = np.array([[1, 2], [3, 4]])

# np.prod() : 배열 원소 간 곱 범용 함수
np.prod(b)
np.prod(c, axis=0)
np.prod(c, axis=1)

# np.sum()
np.sum(b)
np.sum(b, keepdims=True)
np.sum(c, axis=0)
np.sum(c, axis=1)

# np.nanprod() : NaN 을 '1' 로 간주하고 배열 원소 간 곱을 함
d = np.array([[1, 2], [3, np.nan]])
np.nanprod(d, axis=0)
np.nanprod(d, axis=1)

# np.nansum() : NaN 을 zero 로 간주하고 배열 원소 간 더하기
np.nansum(d, axis=0)
np.nansum(d, axis=1)

# np.cumprod() : 행, 열에서 배열 원소들을 누적으로 곱해나감
e = np.array([1, 2, 3, 4])
f = np.array([[1, 2, 3], [4, 5, 6]])
print(np.cumprod(e))
print(np.cumprod(f, axis=0))
print(np.cumprod(f, axis=1))

# np.cumsum() : 배열 원소 간 누적 합 구하기 범용 함수
np.cumsum(e)
np.cumsum(e, axis=0)

# np.diff() : 배열 원소 간 n차 차분 구하기
g = np.array([1, 2, 4, 10, 13, 20])
np.diff(g)
np.diff(g, n=2)
np.diff(g, n=3)

# 차분 결과를 1차원 배열(1 dimensional array)로 반환해주는 함수
np.ediff1d(g)
np.ediff1d(f)

# np.gradient() : 기울기 함수


arr = np.arange(20).reshape(5, 4)
axis_ABC = np.array(['A', 'A', 'B', 'C', 'C'])

arr = np.arange(20).reshape(5, 4)
axis_ABC = np.array(['A', 'A', 'B', 'C', 'C'])

a = np.arange(15).reshape(5, 3)
a_copy = a[[0, 2, 4]][:, [0, 2]]
a_copy[0, :] = 100
print(a)

b = np.array([1, 2, 3, 4])

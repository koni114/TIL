# 삼각함수 np.sin(), np.cos(), np.tan()
import numpy as np
np.sin(np.array((0, 30, 45, 60, 90)) * np.pi / 180.)
np.cos(np.array((0, 30, 45, 60, 90)) * np.pi / 180.)
np.tan(np.array((0, 30, 45, 60, 90)) * np.pi / 180.)

# 싸인 곡선 그리기
import matplotlib.pyplot as plt
x = np.arange(0, 2 * np.pi, 0.1)
y = np.sin(x)
plt.plot(x, y)

# 역삼각함수 : : np.arcsin(), np.arccos(), np.arctan
np.arcsin(1)
np.sin(np.arcsin(1))
np.sin(np.arcsin(1))

# degree 를 radian 으로 변환
# radian 을 degree 로 변환

np.deg2rad(180)
np.rad2deg(np.pi)

# 배열의 원소에 대한 논리 함수
# 배열에 NaN 포함 여부 확인 함수 : np.isnan(x)

# NINF : Negative INF
# PINF : Positive INF
import numpy as np
a = np.array([0, 1, 2, np.nan, 4, np.inf, np.NINF, np.PINF])
print(np.isnan(a))

# 배열에 유한수(finite number) 포함 여부 확인 함수
print(np.isfinite(a))

# 배열에 음의 무한수 포함 여부 : np.isneginf(x)
np.isneginf(a)

# 배열에 양의 무한수 포함 여부 : np.isposinf(x)
np.isposinf(a)

# 참 확인 논리 함수
arr = np.array([[True, False], [True, True]])
np.all(arr, axis=0)
np.all(arr, axis=1)

# 배열의 1개 이상의 원소가 참인지 평가하는 함수 : np.any()
arr = np.array([[True, False], [True, True]])
np.any(arr, axis=0)
np.any(arr, axis=1)

# 배열 원소가 조건을 만족하지 않는 경우 참 반환 : np.logical.not(condition)
b = np.array([0, 1, 2, 3, 4])
np.logical_not(b <= 2)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.set_printoptions(precision=2)

np.random.seed(100)
mu, sigma = 0, 1
x = pd.DataFrame(mu + sigma * np.random.randn(10000))
print(x[(np.abs(x) > 3).any(1)])

x[(np.abs(x) >= 3).any(1)] = np.sign(x) * 3

# reshape 에서 -1 에서 무슨 의미인가?


import numpy as np
x = np.arange(12).reshape(3, 4)
x.reshape(1, -1)




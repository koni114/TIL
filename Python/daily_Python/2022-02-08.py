## 삼각함수
# degree : 우리가 일반적으로 사용하는 것 처럼 0 ~ 360도 표기
# radian : 부채꼴의 호의 길이와 반지름의 길이가 같게 되는 각도를 1 radian
# 1 radian 은 각도로 환산하면, 57.2958.. 정도 됨
# 180 degree = Pi radian
# 1 degree = Pi radian / 180
# 1 radian = 180 degree / Pi

import numpy as np
np.sin(np.array([0, 30, 45, 60, 90]) * np.pi / 180)
np.cos(np.array([0, 30, 45, 60, 90]) * np.pi / 180)
np.tan(np.array([0, 30, 45, 60, 90]) * np.pi / 180)

# sin 곡선 그리기
import matplotlib.pyplot as plt
x = np.arange(0, 2 * np.pi, 0.1) # 0 ~ 2pi
y = np.sin(x)
plt.plot(x, y)

# 삼각함수의 역수
# cosecant, secant, cotangent 함수는 아래와 같이 정의

# 역삼각함수
# arcsin, arccos, arctan
np.arcsin(1)
np.sin(np.arcsin(1))

# degree -> radian
np.deg2rad(180)
np.rad2deg(np.pi)

# 절대값
test_value = [1, 2, -1, -2, 0.3, -0.9]
np.abs(test_value)
np.fabs(test_value)

# 제곱근
np.sqrt(test_value)

# 제곱값
np.square(test_value)

# 배열 원소의 정수와 소수점을 구분하여 2개의 배열 반환
split_value = np.modf(test_value)
print(split_value[0])  # 소수점
print(split_value[1])  # 정수

# 배열 원소의 부호 판별 함수
c = np.array([-2, -1, 0, 1, 2])
np.sign(c) # 1(positive), 0(zero), -1(negative)

# 배열에 NaN 포함 여부 확인 함수 : np.isnan(x)
import numpy as np
a = np.array([0, 1, 2, np.nan, 4, np.inf, np.NINF, np.PINF])
print(np.isnan(a))

# 배열에 유한수(finite number) 포함 여부 확인 함수 : np.isfinite(x)
print(np.isfinite(a))

# 배열에 무한수(infinite number) 포함 여부 확인 함수 : np.isinf(x)
print(np.isinf(a))

# 배열에 음의 무한수 포함 여부
np.isneginf(a)

# 배열에 양의 무한수 포함 여부
np.isposinf(a)

# 배열의 모든 원소가 참(True) 인지 평가하는 함수 : np.all()
import numpy as np

all_TF = [[True, False], [True, True]]

np.all(all_TF)
np.all(all_TF, axis=1)  # 가로
np.all(all_TF, axis=0)  # 세로

#  배열의 모든 원소가 참(True) 인지 평가하는 함수 : np.any()
np.any([[True, False], [True, True]])
np.any([[True, False], [True, True]], axis=0)
np.any([[True, False], [True, True]], axis=1)

# 배열 원소가 조건을 만족하지 않는 경우 참 반환 --> np.logical_not
b = np.array([0, 1, 2, 3, 4])
np.logical_not(b <= 2)

x = np.arange(12).reshape(3, 4)







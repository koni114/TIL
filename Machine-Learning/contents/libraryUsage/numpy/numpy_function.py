import numpy as np

#- np.argmin function
#- 가장 작은 값의 인덱스 return
np.argmin([1,2,3,4,5]) #- 0

#- np.random
#- randint, rand, randn
#- np.random.randint : 균일 분포의 정수 난수 1개 생성
#- np.random.rand    : 0부터 1사이의 균일 분포에서 난수 matrix array 생성
#- np.random.randn   : 가우시안 표준 정규 분포에서 난수 matrix array 생성

np.random.randint(6)      #- 0 ~ 5사이의 난수 1개 생성
np.random.randint(1, 20)  #- 1 ~ 20 사이의 난수 1개 생성
np.random.rand(6)         #- 0 ~ 1의 균일 분포 표준정규분포 난수 생성
np.random.rand(3, 2)      #- 3,2 matrix
np.random.randn(6)
np.random.randn(3, 2)

#- 공식 테스트를 위한 데이터 생성
#- 정규방정식을 통한 hat theta 계산
#- hat theta를 통한 예측값 생성
import numpy as np
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

X_b = np.c_[np.ones((100, 1)), X]
theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T.dot(y))
print(theta_best)

X_new = [[0], [2]]
X_new_b = np.c_[np.ones((2, 1)), X_new]
y_predict = X_new_b.dot(theta_best)
print(y_predict)

#- 2차원 배열에 대해 order="C", order="F", order="k" 별로 확인
#- np.ravel(x, order="C") : C와 같은 순서로 인덱싱하여 평평하게 배열
x = np.arange(12).reshape(3, 4)
x.ravel(order="C")
x.ravel(order="F") #- Fortran과 같은 순서로 인덱싱하여 평평하게 배열
x.ravel(order="k") #- 메모리에서 발생하는 순서대로 인덱싱하여 평평하게 배열

#- np.cumsum function
#- 행렬 식을 점점 누적해서 더해주는 function
np.cumsum([1, 2, 3, 4, 5])

#- np.array_split function
from sklearn.datasets import load_iris
X = load_iris().data
n_batch = 10
for X_batches in np.array_split(X, n_batch):
    print(f"X_batches shape : {X_batches.shape}")


#- np.percentile function
#- 분위수를 구해주는 함수.
np.percentile([1, 2, 3, 4, 5], 50)   #- 전체 numpy.array 의 50% 이므로, 3.0이 나옴
np.percentile([1, 2, 3, 4, 5], 100)  #- 전체 100% 위치 -> 5.0
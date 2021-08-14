import numpy as np
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1) #- randn : 가우시안 표준정규분포 난수

#- 정규방정식을 사용한 theta 값 계산
#- numpy 선혀앧수 모듈에 있는 inv() 함수를 사용해 역행렬을 계산
#- dot() 메서드를 사용해 행렬 곱셈을 함
x_b = np.c_[np.ones((100, 1)), X]  #- 모든 샘플에 x0 = 1을 추가
theta_best = np.linalg.inv(x_b.T.dot(x_b)).dot(x_b.T).dot(y) #- (X^T * X)^(-1) (X^T * y)
print(theta_best) #- 잡음 때문에 정확하게 예측하지는 못함

#- thata hat을 활용한 예측 수행
X_new = np.array([[0], [2]])
X_new_b = np.c_[np.ones((2, 1)), X_new]
y_predict = X_new_b.dot(theta_best)
print(y_predict)

#- 모델의 예측을 그래프에 나타내보기
import matplotlib.pyplot as plt
plt.plot(X_new, y_predict, "r-")
plt.plot(X, y, "b.")
plt.axis([0, 2, 0, 15])
plt.show()

#- scikit-learn에서 선형 회귀를 수행하는 것은 간단
#- scikit-learn은 가중치(coef_)와 편향(intercept_)를 분리하여 저장
from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(X, y)
print(lin_reg.intercept_, lin_reg.coef_)
lin_reg.predict(X_new)

#- LinearRegression class는 scipy.linalg.lstsq() 함수를 기반으로 함
#- 이 함수를 직접 호출할 수 있음
X_b = np.c_[np.ones((100, 1)), X]
theta_best_svd, residuals, rank, s = np.linalg.lstsq(X_b, y, rcond=1e-6)

#- np.linalg.lstsq 함수는 hat theta = X^(+)y를 계산
#- X+는 X의 유사역행렬
#- np.linalg.pinv() 함수를 사용해 유사역행렬을 직접 구할 수 있음
np.linalg.pinv(X_b).dot(y)

########################
## 경사 하강법 알고리즘 구현 ##
########################

eta = 0.1 #- 학습률
n_iterations = 1000
m = 100

theta = np.random.randn(2, 1)
for iteration in range(n_iterations):
    gradients = 2/m * X_b.T.dot(X_b.dot(theta) - y)
    theta = theta - eta * gradients

print(theta)

#- 간단한 학습 스케줄을 사용한 확률적 경사 하강법의 구현
n_epochs = 50
t0, t1 = 5, 50

def learning_schedule(t):
    return t0 / (t + t1)

theta = np.random.randn(2, 1)

for epoch in range(n_epochs):
    for i in range(m):
        random_index = np.random.randint(m)
        xi = X_b[random_index:random_index+1]
        yi = y[random_index:random_index+1]
        gradients = 2 * xi.T.dot(xi.dot(theta) - yi)
        eta = learning_schedule(epoch * m + i)
        theta = theta - eta * gradients

print(theta)

#- 사이킷런 SGD 방식의 선형 회귀 사용 예제
from sklearn.linear_model import SGDRegressor
sgd_reg = SGDRegressor(max_iter=1000, tol=1e-3, penalty=None, eta0=0.1)
sgd_reg.fit(X , y.ravel())
print(sgd_reg.intercept_, sgd_reg.coef_)

#- 다항 회귀
m = 100
X = 6 * np.random.rand(m, 1) - 3
y = 0.5 * X**2 + X + 2 + np.random.randn(m, 1)
plt.plot(X, y, 'b.')

from sklearn.preprocessing import PolynomialFeatures
#- include_bias --> True이면 편향을 위한 특성 x0인 1이 추가됨
poly_features =PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly_features.fit_transform(X)
print(X[0])
print(X_poly[0])

lin_reg = LinearRegression()
lin_reg.fit(X_poly, y)
print(lin_reg.intercept_, lin_reg.coef_)

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

def plot_learning_curve(model, X  ,y):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
    train_errors, val_errors = [], []
    for m in range(1, len(X_train)):
        model.fit(X_train[:m], y_train[:m])
        y_train_predict = model.predict(X_train[:m])
        y_val_predict = model.predict(X_val)
        train_errors.append(mean_squared_error(y_train[:m], y_train_predict))
        val_errors.append(mean_squared_error(y_val, y_val_predict))
    plt.plot(np.sqrt(train_errors), "r-+", linewidth=2, label="훈련 세트")
    plt.plot(np.sqrt(val_errors), "b-+", linewidth=2, label="검증 세트")

#- 단순 선형 회귀 모형 learning curve
lin_reg = LinearRegression()

plot_learning_curve(lin_reg, X, y)

#- 10차 다항 회귀 모형 learning curve
polynomial_regression = Pipeline([
    ("poly_features", PolynomialFeatures(degree=10, include_bias=False)),
    ('lin_reg', LinearRegression()),
])

plot_learning_curve(polynomial_regression, X, y)

#- Ridge Regression
from sklearn.linear_model import Ridge
ridge_reg = Ridge(alpha=1, solver='cholesky')
ridge_reg.fit(X, y)
ridge_reg.predict([[1.5]])

from sklearn.linear_model import SGDRegressor
sgd_reg = SGDRegressor(penalty='l2')
sgd_reg.fit(X, y.ravel())
sgd_reg.predict([[1.5]])

#- Lasso Regression


# Linear Regression
- 다항 회귀는 선형 회귀보다 파라미터가 많아 훈련 데이터에 과적합되기 쉬움

## 선형 회귀
- 선형 회귀를 훈련시키는 두 가지 방법
  - 직접 계산할 수 있는 공식을 사용하여 훈련 세트에 가장 잘 맞는 모델 파라미터(훈련 세트에 대해 비용 함수를 최소화하는 모델 파라미터를 해석적으로 구함
  - 경사 하강법(GD)이라 불리는 반복적인 최적화 방식을 사용하여 모델 파라미터를 조금씩 바꾸면서 비용 함수를 훈련 세트에 대해 최소화시킴 
    결국 위의 방법과 동일한 파라미터로 수렴함
- 선형 회귀는 입력 특성의 가중치(독립변수의 계수)와 편향(절편)이라는 상수를 더해 예측을 만듬
- 선형 회귀 모델 식은 다음과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\hat{y}&space;=&space;\theta_{0}&space;&plus;&space;\theta_{1}x_{1}&space;&plus;&space;\theta_{2}x_{2}&space;&plus;&space;...&space;&plus;&space;\theta_{n}x_{n}" /></p>

- yHat은 예측값  
- n은 특성의 수
- x(i)는 i번째 특성값
- theta(j)는 j번째 모델 파라미터(절편은 theta(0))
- 이 식은 [식 4-2]처럼 벡터 형태로 더 간단하게 쓸 수 있음

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\hat{y}&space;=&space;h_{\theta}(x)&space;=&space;\theta&space;\cdot&space;x" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{y}&space;=&space;h_{\theta}(x)&space;=&space;\theta&space;\cdot&space;x" title="\hat{y} = h_{\theta}(x) = \theta \cdot x" /></a></p>

- theta는 편향 theta_{0} 과 theta_{1}에서 theta_{n}까지의 특성 가중치를 담은 모델의 파라미터 벡터
- x는 x_{0}에서 x_{n}까지 담은 샘플의 특성 벡터임. x_{0}는 항상 1
- theta dot x 는 벡터 theta와 x의 점곱
- h_(theta)는 모델 파라미터 theta를 사용한 가설 함수 
- 선형 회귀 모델을 훈련시키려면 RMSE를 최소화하는 theta를 찾아야 함
- 실제로는 RMSE 보다 평균 제곱 오차(MSE)를 최소화하는 것이 같은 결과 값을 내면서 더 간단함
- <b>최종 모델을 평가하는 데 사용하는 성능 측정 지표 말고 학습 알고리즘이 다른 함수를 최적화하는 경우가 종종 있음</b>  
why? 보통 성능 지표에는 없는 유용한 미분 특성이 존재해 이런 함수가 더 계산하기 쉽거나, 훈련하는 동안 모델에 제약을 가하기 위해 사용(ex) ridge, Lasso 모형)
- 훈련 세트 X에 대한 선형 회귀 가설 h_{theta}의 MSE는 다음 처럼 계산함

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=MSE(X,&space;h_{\theta})&space;=&space;\frac{1}{m}&space;\sum_{i=1}^{m}(\theta^{T}X^{(i)}&space;-&space;y^{(i)})^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?MSE(X,&space;h_{\theta})&space;=&space;\frac{1}{m}&space;\sum_{i=1}^{m}(\theta^{T}X^{(i)}&space;-&space;y^{(i)})^{2}" title="MSE(X, h_{\theta}) = \frac{1}{m} \sum_{i=1}^{m}(\theta^{T}X^{(i)} - y^{(i)})^{2}" /></a></p>

### 정규방정식(normal equation)
- 비용 함수 MSE(theta)를 최소화 하는 함수 계수를 찾기 위한 해석적인 방법이 있음
- 다른 말로 하면 바로 결과를 얻을 수 있는 수학 공식이 존재
- 이를 <b>정규방정식(normal equation)</b>이라고 함
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\hat\theta&space;=&space;(X^{T}X)^{-1}X^{T}y" /></p>

- theta hat은 비용 함수를 최소화하는 theta 값
- y는 y(1) 부터 y(m)을 포함하는 타깃 벡터
- `LinearRegresssion` 클래스는 `scipy.linalg.lstsq()` 함수를 기반으로 함  
  이 함수를 직접 호출할 수 있음
- <b>중요한 것은 `LinearRegresssion` 은 theta hat = X^{+}y를 계산하는데, 여기서 X^{+}는 유사역행렬(pseudoinverse)라고 함</b>
- 유사역행렬 자체는 <b>특잇값 분해(sigular value decomposition, SVD)</b> 라고 부르는 표준 행렬 분해 기법을 사용해 계산
- R에서의 `lm()` 함수는 QR분해를 이용하여 선형 회귀를 계산함
~~~python 
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
~~~

#### 특잇값분해(singular value decomposition)
- 유사역행렬은 다음과 같은 식으로 계산됨 --> theta hat = X^{+} y 
- 중요한 것은 정규방정식은 극단적인 경우 계산할 수 없는 반면, 유사역행렬은 언제든지 구할 수 있음. 그래서 특잇값분해를 이용한 유사역행렬을 더 선호

#### 계산 복잡도
- 정규방정식의 계산 복잡도는 (n+1) * (n+1) 크기가 되는 X^{T} X를 계산
- 행렬을 계산하는 계산복잡도는 O(n^{2.4}) 에서 O(n^{3}) 사이임  
  특성이 두배 늘어날수록 계산 시간이 대략 5.3 ~ 8배 정도 늘어남
- `LinearRegression`이 사용하는 SVD 방법은 약 O(n^{2})임. 특성의 개수가 늘어나면 계산 속도는 약 4배 늘어나게 됨
- <b>특성의 개수가 늘어날수록 성능 저하가 심하게 일어남</b>
- 훈련 세트의 샘플 수에 대해서는 선형적으로 증가(O(m)). 따라서 메모리 공간이 허락된다면 큰 훈련 세트도 효율적으로 처리가 가능
- 또한 학습된 선형 회귀 모델은 예측이 매우 빠른데, 예측 계산 복잡도는 샘플 수와 특성 수에 선형적
- 다시 말해 예측하려는 샘플이 두 배로 늘어나면 걸리는 시간도 거의 두 배 증가


### 경사 하강법
- 특성이 너무 많고, 훈련 샘플이 너무 많아 메모리에 모두 담을 수 없을 때 사용
- 여러 종류의 문제에서 최적의 해법을 찾을 수 있는 일반적인 최적화 알고리즘
- 경사 하강법의 기본 아이디어는 비용 함수를 최소화하기 위해 반복해서 파라미터를 조정해 나가는 것
- 경사 하강법의 원리는 발바닥이 닿는 바닥의 기울기만 가지고 골짜기를 찾아가는 방법과 유사
- 파라미터 벡터 theta에 대해 비용 함수의 현재 그레이디언트를 계산  
  (그레디언트는 비용 함수의 미분값으로 포괄적으로 사용)
- 그리고 그레디언트가 감소하는 방향으로 진행. 그레디언트가 0이 되면 최솟값에 도달한 것
- theta를 임의의 값을 시작해서(무작위 초기화, random initialization) 한 번에 조금씩 비용 함수가 감소되는 방향으로 진행하여 알고리즘이 최솟값에 수렴할 때까지 점진적으로 향상시킴
- 그레디언트가 0이되면 최솟값에 도달한 것임
- <b>학습 스텝의 크기는 비용 함수의 기울기에 비례</b>. 따라서 파라미터가 최솟값에 가까워질수록 스텝 크기가 점진적으로 줄어듬
- 경사 하강법에서 중요한 파라미터는 스텝의 크기로, learning rate 하이퍼 파라미터로 결정
- 학습률이 너무 작으면 알고리즘이 수렴하기 위해 반복을 많이 진행해야 하므로, 시간이 오래 걸림
- 학습률이 너무 크면 골짜기를 가로질러 반대편으로 건너뛰게 되어 이전보다 더 높은 곳으로 올라가게 됨
- 모든 비용함수가 2차 볼록 함수 형태는 아님. 따라서 전역 최솟값(global minimum)이 아닌 지역 최솟값(local minimum)에 수렴할 수 있음
- <b>선형 회귀를 위한 MSE 비용 함수는 항상 2차 볼록함수이기 때문에 어디서 시작하던 전역 최솟값만 있고 기울기가 갑자기 변하지 않음(립시츠 연속)</b>
- 이 두 사실로부터 경사 하강법이 전역 최솟값에 가깝게 접근할 수 있음을 보장함
- 사실 비용 함수는 그릇 모양을 하고 있지만 <b>특성들의 스케일이 매우 다르면 길쭉한 모양일 수 있음</b>
- 왼쪽: 특성1과 특성2이 스케일이 같은 훈련 세트
- 오른쪽: 특성1이 특성2보다 더 작은 훈련 세트
- 특성1이 더 작기 때문에 비용함수에 영향을 주기 위해서는 특성1이 더 크게 바뀌어야 함. 그래서 특성1 축을 따라서 더 길쭉한 모양이 됨
![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/LM_scaling_versus.JPG)

- 위의 그림에서 보면, 왼쪽 그림은 scaling 처리가 되어 최솟값으로 곧장 진행하고 있어 빠르게 도달하는 반면, 오른쪽 그래프는 시간이 오래걸림
- <b>즉 스케일이 다르면 전역 최솟값에 도달하는 시간이 더 오래걸리므로, scale을 조정해 주어야 함</b>
- <b>앞의 그림은 모델 훈련이 비용 함수를 최소화하는 모델 파라미터의 조합을 찾는 일임을 보여줌. 이를 파라미터 공간(parameter space)에서 찾는다고 얘기함</b>


### 배치 경사 하강법
- 경사 하강법을 구현하려면 각 모델 파라미터 theta(j)에 대해 비용 함수의 그레디언트를 계산해야함
- 다시 말해 theta(j)가 조금 변경될 때 비용 함수가 얼마나 바뀌는지 계산해야함. 이를 <b>편도함수(partial derivative)</b>라고 함  
이는 "동쪽을 바라봤을 때 발밑에 느껴지는 산의 기울기는 얼마인가?"와 같은 질문 
- 이러한 같은 질문을 모든 차원에서 행함
- 다음의 식은 파라미터 theta(j)에 대한 비용 함수의 편도함수임
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\frac{\partial&space;}{\partial\theta_{j}}&space;MSE(\theta)&space;=&space;\frac{2}{m}&space;\sum_{i&space;=&space;1}^{m}(\theta^{T}x^{(i)}&space;-&space;y^{(i)})&space;(x_{j})^{(i)}" /></p>
- 위의 식을 이용해 편도 함수를 각각 계산할 수도 있지만, 선형 대수로 한꺼번에도 계산 가능
- 수식에 theta가 있기 때문에 매 경사 하강법 스텝에서 전체 훈련 세트 X에 대해 계산함
- 그래서 이 알고리즘을 <b>배치 경사 하강법(batch gradient descent)</b>라고 함
- 매 스텝에서 훈련 데이터 전체를 사용함(전체 경사 하강법이 더 적절한 이름 같음)
- 이런 이유로 매우 큰 훈련 세트에서는 아주 느림
- <b>그러나 경사 하강법은 특성 수에는 민감하지 않음</b>
- <b>위로 향하는 그레디언트 벡터가 구해지면, 반대 방향인 아래로 가야 함</b>
- 즉 theta에서 편도 함수의 값을 빼야한다는 의미. 여기서 학습률도 사용됨
- 다음은 경사 하강법의 스텝 식임
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\theta^{next&space;step}&space;=&space;\theta&space;-&space;\eta&space;\bigtriangledown_{\theta}&space;MSE(\theta)" /></p>

~~~python
eta = 0.1 #- 학습률
n_iterations = 1000
m = 100

theta = np.random.randn(2, 1)
for iteration in range(n_iterations):
    gradients = 2/m * X_b.T.dot(X_b.dot(theta) - y)
    theta = theta - eta * gradients

print(theta)
~~~
- 적절한 학습률을 찾으려면 그리드 탐색을 사용. 그리드 탐색에서 수렴하는 데 너무 오래 걸리는 모델을 막기 위해 반복 횟수를 제한해야 함
- 적절한 학습률의 반복 휫수를 찾으려면, 반복 횟수를 아주 크게 지정하고 그레디언트 벡터가 아주 작아지면 벡터의 노름이 허용 오차보다 작아지면 경사 하강법이 거의 최솟값에 도달한 것이므로 알고리즘을 중지시키는 방법이 있음
- 수렴율  
  - 비용함수의 모양에 따라 달라지겠지만 허용 오차 범위 안에서 최적의 솔루션에 도달하기 위해서는 O(1/허용오차)의 반복이 걸릴 수 있음
  - <b>허용 오차를 1/10으로 줄이면 알고리즘의 반복은 10배 늘어남</b>

### 확률적 경사 하강법
- 배치 경사 하강법의 가장 큰 문제는 매 스탭에서 전체 훈련 세트를 이용해 그레디언트를 계산 한다는 사실
- 훈련 세트가 커지면 매우 느려지게 됨
- <b>확률적 경사 하강법은 매 스텝에서 한 개의 샘플을 무작위로 선택하고 그 하나의 샘플에 대한 그레디언트를 계산함</b>
- 매 반복에서 다뤄야 할 데이터가 매우 적기 때문에 한 번에 하나의 샘플을 처리하면 알고리즘이 확실히 훨씬 빠름
- 반면 확률적(무작위)이기 때문에 이 알고리즘은 배치 경사 하강법보다 훨씬 불안정 함
- 비용 함수가 최솟값에 다다를 때까지 부드럽게 감소하지 않고 요동치면서 평균적으로 감소함
- 즉, 시간이 지나면 최솟값에 매우 근접하겠지만 요동이 지속되면서 최솟값에 안착하지 못할 것임
- 알고리즘이 멈출 때 좋은 파라미터가 구해지겠지만 최적치는 아님
- 무작위성은 지역 최솟값에서 탈출시켜줘서 좋지만 알고리즘을 전역 최솟값에 다다르지 못하게 한다는 점에서 좋지 않음
- 딜레마를 해결하는 한 가지 방법은 학습률을 점진적으로 감소시키는 것
  - 이는 담금질 기법(simulated annealing) 알고리즘과 유사
  - 매 반복에서 학습률을 결정하는 함수를 학습 스케줄(learning schedule, learning rate schedule)이라고 함
- 시작할 때는 학습률을 크게하지만 점차 작게 줄여서 알고리즘이 전역 최솟값에 도달하게 함
- 다음은 간단한 학습 스케줄을 사용한 확률적 경사 하강법의 구현
~~~python
n_epochs = 50
t0, t1 = 5, 50
m = 100 #- sample num

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
~~~
- 일반적으로 한 반복에서 m번(훈련 세트에 있는 샘플 수) 되풀이 되고, 이때 각 반복을 epoch라고 함
- 샘플은 무작위로 선택되기 때문에 한 샘플은 2번 이상 선택 될 수도 있고, 아예 선택받지 못할 수도 있음
- <b>따라서 알고리즘이 epoch마다 모든 샘플을 사용하게 하려면 훈련 세트를 섞은 후 차례대로 하나씩 선택하고 다음 에포크에서 다시 섞는 식의 방법을 사용할 수 있음</b>   
사이킷런의 `SGDClassifier`, `SGDRegressor` 에서 위의 방법을 사용
- 그러나 이렇게 하면 보통 더 늦게 수렴됨
- 확률적 경사 하강법을 사용할 때 훈련 샘플이 IID(independent and identically distributed)를 만족해야 평균적으로 파라미터가 전역 최적점을 향해 진행한다고 보장할 수 있음
- 이렇게 만드는 가장 간단한 방법은 훈련하는 동안 샘플을 섞는 것. 예를 들어 epoch 단위로 샘플을 섞는 것
- 레이블 순서대로 정렬된 샘플처럼 샘플을 섞지 않은 채로 사용하면 확률적 경사 하강법이 먼저 한 레이블에 최적화하고 그다음 두 번째 레이블을 최적화하는 방식으로 진행되므로, 이 모델은 결국 최적점에 가깝게 도달하지 못할 것임
- scikit-learn에서 SGD 방식으로 선형 회귀를 사용하려면 기본값으로 제곱 오차 비용 함수를 최적화하는 `SGDRegressor` 클래스를 사용
- 다음 코드는 최대 1000번 epoch 동안 실행됨(`max_iter=1000`). 또한 한 에포크에서 0.001보다 적게 손실이 줄어들 때까지 실행됨(`tol=1e-3`)
- 학습률 0.1(`eta0 = 0.1`)로 기본 학습 스케줄을 사용
- 기본 학습 스케줄의 기본 값은 'invscaling'으로, 반복 횟수 t, eta0, power_t 두 매개변수를 사용한 다음 공식으로 학습률을 계산 
- 회귀 : eta(t) = eta0 / t^(power_t), default: eta0 = 0.01, power_t = 0.25
- 분류 : 1 / alpha(t0 + t)
~~~python
#- 사이킷런 SGD 방식의 선형 회귀 사용 예제
from sklearn.linear_model import SGDRegressor
sgd_reg = SGDRegressor(max_iter=1000, tol=1e-3, penalty=None, eta0=0.1)
sgd_reg.fit(X , y.ravel())

print(sgd_reg.intercept_, sgd_reg.coef_)
~~~

### 미니배치 경사 하강법
- 전체 훈련 세트나 하나의 샘플을 기반으로 그레디언트를 계산하는 것이 아니라  
  미니배치라 부르는 임의의 작은 샘플 세트에 대해 그레디언트를 계산함
- 확률적 경사 하강법에 비해서 장점은 행렬 연산에 최적화된 하드웨어, 특히 GPU를 사용해서 얻는 성능 향상
- 미니배치를 어느정도 크게하면 덜 불규칙적이게 수렴
- 선형회귀가 아니라면 지역 최솟값에서 벗어나기 힘들지도 모름
![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/Linear_Regression.JPG)

## 다항 회귀
- 비선형 데이터를 학습하는 데 선형 모델을 사용할 수 있음
- 이렇게 하는 간단한 방법은 각 특성의 거듭제곱을 새로운 특성으로 추가하고, 이 확장된 특성을 포함한 데이터셋에 선형 모델을 훈련시키는 것. 이런 기법을 <b>다항 회귀(Polynomial Regression)</b>라고 함
~~~python
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
~~~
- 특성이 여러 개일 때 다항 회귀는 특성 사이의 관계를 찾을 수 있음(교호작용)
- `PolynomialFeatures`가 주어진 차수까지 특성 간의 모든 교차항을 추가하기 때문
- 예를 들어 두 개의 특성 a, b가 있을 때 `degree=3`으로 추가하면 a^2, b^2, a^3, b^3 뿐만 아니라 ab, ab^2, a^2b 도 특성으로 추가됨
- `PolynomialFeatures`를 이용해 다항 변수들을 생성해 낼 수 있는데, `interaction_only = True`로 지정하면 제곱항들은 제거
- 특성 a, b가 있을때 degree = 2이면, a^2, b^2, ab, a, b도 특성으로 추가함
- `PolynomialFeatures(degree=d)`는 특성이 n개의 배열을 특성이 (n + d)! / d!n! 개인 배열로 변환함

### 학습 곡선
- 고차 다항 회귀는 보통의 선형 회귀보다 훨씬 더 훈련 데이터에 잘 맞추려고 할 것임
- 보통 n차 다항 회귀는 n이 커질수록 점점 더 과대적합 될 확률이 높은데, 이 때 적절한 n의 값은 어떻게 찾을 수 있을까?
  - 모델의 일반화 성능을 추정하기 위해 교차 검증을 이용하여 평가  
    훈련 데이터의 성능이 좋은데, test Dataset의 성능이 좋지 않다면 과대적합 된 것  
    --> n의 값을 낮추어야 함
  - 만약 train/test Dataset에 대한 성능이 둘 다 좋지 못하다면 과소적합 된 것
  - <b>학습 곡선</b>을 살펴보는 것도 도움이 됨  
    이 그래프는 훈련 세트와 검증 세트의 모델 성능을 훈련 세트 크기의 함수로 나타냄  
    X = 훈련 세트 크기, y = RMSE를 각각 훈련/테스트 세트로 계산  
![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/underFitting_LearningCurve.JPG)

- 위의 학습 곡선은 과소 적합 되었을 때의 특징이 나타나는 학습 곡선  
  - 훈련 세트의 그래프와 검증 세트의 그래프의 오차가 거의 나지 않음 
  - 두 곡선이 수평한 곡선을 만듬
- 모델이 훈련 데이터에 과소 적합 되어 있다면 데이터를 더 추가하더라도 소용이 없음  
  더 복잡한 모델을 사용하거나 더 나은 특성을 사용해야 함  

![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/overFitting_LearningCurve.JPG)

- 다음은 10차 다항회귀 곡선
  - 훈련 데이터의 오차가 선형 회귀 모델보다 훨씬 낮음
  - 두 곡선 사이의 공간이 있음. 이 말은 훈련 데이터에서의 모델 성능이 검증 데이터에서보다 훨씬 낫다는 의미를 보여줌 --> 과대 적합의 특징
  - 더 큰 훈련세트를 사용하면 두 곡선이 점점 가까워짐 
- 과대적합 모델을 개선하는 한 가지 방법은 검증 오차가 훈련 오차에 근접할 때까지 더 많은 훈련 데이터를 추가하는 것
- 다음은 해당 곡선을 그리기 위한 코드
~~~python
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
~~~

#### 편향(bias)/분산(variance) 트레이드 오프
- 통계학과 머신러닝에서 나온 중요한 이론 하나는 모델의 일반화 오차는 세가지 다른 종류의 오차의 합으로 표현될 수 있다는 사실
  - 편향(bias)  
    잘못된 가정으로 인한 것. 예를 들어 데이터는 실제 2차인데 선형함수로 가정하는 경우,  
    편향이 큰 모델은 훈련 데이터에 과소적합되기 쉬움
  - 분산(variance)  
    분산은 훈련 데이터에 있는 작은 변동이 모델에 과도하게 민감해서 나타남  
    자유도가 높은 모델(예를 들어 고차 다항 회귀)이 높은 분산을 가지기 쉬워 훈련 데이터에 과대적합되는 경향이 있음 
  - 줄일 수 없는 오차  
    데이터 자체의 잡음 때문에 발생. 이 오차를 줄이려면 데이터 자체의 이상치 등을 제거해야함

## Ridge 회귀
- 규제가 추가된 회귀 버전
- 가중치 벡터 L2 노름을 사용
- 규제를 하는 이유는 모델의 오버피팅을 줄이기 위하여 규제를 수행
- 규제항 (theta)^2 의 합이 비용 함수에 추가됨
- 이는 학습 알고리즘을 데이터에 맞추는 것 뿐만 아니라 모델의 가중치가 가능한 한 작게 유지되도록 노력함
- <b>규제항은 학습하는 동안에만 비용 함수에 추가되고, 실제 모델 평가에는 규제항은 제외됨</b>
- 일반적으로 훈련하는 동안 사용되는 비용 함수와 테스트에서 사용되는 성능 지표는 다른데,  
  규제를 떠나서 이들이 다른 이유는 비용 함수는 미분 가능해야하고, 성능 지표는 최종 목표에 가능한 한 가까워야 함
- 하이퍼파라미터 alpha는 모델을 얼마나 규제할지를 결정함  
  alpha가 0이면 릿지 회귀는 선형 회귀와 같아짐
- alpha가 매우 커지면, 가중치가 거의 0에 가까워지고,  데이터의 평균선과 비슷해짐
- 다음은 릿지 회귀의 비용함수임
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?J(\theta)&space;=&space;MSE(\theta)&space;&plus;&space;\alpha\frac{1}{2}\sum_{i&space;=&space;1}^{n}\theta^{2}" /></p>

- 편향 theta(0)는 규제되지 않음
- 릿지 회귀는 입력 특성의 스케일에 민감하기 때문에 수행하기 전에 데이터의 스케일을 맞추는 것이 중요
- <b>규제가 있는 모델은 대부분 scaling을 해야함</b>
- alpha가 커질수록 직선에 가까워지며, 이는 편향은 커지고 분산은 줄어들게 됨
- 릿지 회귀도 마찬가지로 정규방정식을 사용할 수도 있고, 경사 하강법을 사용할 수도 있음

## Lasso 회귀
- Least absolute shrinkage and selection operator(LASSO)
- 가중치 벡터 L1 노름을 사용함
- 라쏘 회귀의 비용함수는 다음과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?J(\theta)&space;=&space;MSE(\theta)&space;&plus;&space;\alpha\frac{1}{2}\sum_{i&space;=&space;1}^{n}|\theta|" /></p>

- 라쏘 회귀의 중요한 특징은 덜 중요한 특성의 가중치를 제거하려고 하는 것(가중치의 값이 0이 됨)
- 라쏘 회귀는 자동으로 특성 선택을 하고 희소 모델(sparse model)을 만듬
- 라쏘를 사용할 때 경사 하강법이 최적점 근처에서 진동하는 것을 막으려면 훈련하는 동안 점진적으로 학습률을 감소시켜야 함
- Lasso 회귀에서 규제 함수는 absolute function이기 때문에 미분 불가능한 점에서 진동이 조금 있을 수 있음

## elasticNet 회귀
- 엘라스틱넷은 릿지 회귀와 라쏘 회귀를 절충한 모델
- 규제항은 릿지와 라소의 규제항을 단순히 더해서 사용하며, 혼합 정도는 혼합 비율 r을 사용해 조절
- r = 0이면 엘라스틱넷은 릿지 회귀와 같고, r = 1이면 lasso 회귀와 같음
- 엘라스틱넷의 비용함수는 다음과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?J(\theta)&space;=&space;MSE(\theta)&space;&plus;&space;r\alpha\sum_{i&space;=&space;1}^{n}|\theta|&space;&plus;&space;\frac{1-&space;r}{2}\alpha\sum_{i&space;=&space;1}^{n}\theta^{2}" /></p>

- 그렇다면 보통의 선형 회귀, 릿지, 라쏘, 엘라스틱넷을 언제 사용해야 할까요?  
  --> 적어도 규제가 약간은 있는 것이 대부분의 경우에 좋으므로 일반적으로 평범한 선형 회귀는 피해야 함  
- 릿지가 기본이 되지만 쓰이는 특성이 몇 개뿐이라고 의심되면 라쏘나 엘라스틱넷이 더 좋음
- 라쏘는 특성 수가 샘플 수(n)가 보다 많으면 최대 n개의 특성을 선택함
- 또한 여러 특성이 강하게 연관되어 있으면 이들 중 임의의 특성 하나를 선택함 
- 적절한 모델 학습 반복 횟수를 지정하기 위하여 early stopping을 하는 것이 좋음
- 확률 경사 하강법이나 미니배치 경사 하강법은 곡선이 그리 매끄럽지 않아 최솟값에 도달했는지 확인하기 어려울 수 있음. 한 가지 해결책은 일정 시간 동안 최솟값보다 클 때 학습을 멈추고 최솟값일 때의 모델 파라미터로 되돌리는 것

## 용어 정리
- 립시츠 연속
  - 어떤 함수의 도함수가 일정한 범위 안에서 변할 때 이 함수를 립시츠 연속이라고 함
- 희소 모델(sparse model)
  - 0이 아닌 특성의 가중치가 적은 모델
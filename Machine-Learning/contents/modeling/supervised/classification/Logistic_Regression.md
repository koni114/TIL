# 로지스틱 회귀
- 어떤 회귀 알고리즘은 분류에도 사용이 가능
- 로지스틱 회귀는 샘플이 특정 클래스에 속할 확률을 추정하는데 널리 사용됨
- 추정 확률이 50%가 넘으면 모델은 그 샘플이 해당 클래스에 속한다고 예측(레이블이 '1'인 양성 클래스)
- 아니면 클래스에 속하지 않는다고 예측(레이블이 '0'인 음성 클래스)
- 이를 <b>이진 분류기라고 함</b>

## 로지스틱 확률 추정
- 로지스틱도 선형 회귀와 마찬가지로 입력 특성의 가중치의 합을 계산함(그리고 편향을 더함)
- 대신 선형 회귀처럼 결과를 바로 출력하지 않고, 결괏값의 로지스틱을 출력
- 로지스틱 회귀 모델의 확률 추정 모형은 다음과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\hat{p}&space;=&space;h_{\theta}(x)&space;=&space;\sigma(\theta^{T}&space;x)" /></p>

- 로지스틱(sigma(.)로 표현)은 0과 1사이를 출력하는 시그모이드 함수임
- 로지스틱 함수는 다음과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\sigma(t)&space;=&space;\frac{1}{1&space;&plus;&space;exp(-t)}" /></p>
- 로지스틱 회귀 모델이 샘플 x가 양성 클래스에 속할 확률 hatP = h_(theta)(x) 를 추정하면 이에 대한 예측 hatY를 쉽게 구할 수 있음
- 로지스틱 회귀 모델 예측은 다음과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\hat{y}&space;=&space;\begin{pmatrix}&space;0&space;,&space;\hat{p}&space;<&space;0.5\\&space;1,&space;\hat{p}&space;>=&space;0.5&space;\end{pmatrix}" /></p>

- t < 0이면 sigma(t) < 0.5 이고, t >= 0 이면 sigma(t) >= 0.5 이므로, 로지스틱 회귀 모델은 theta^(t) * x가 양수일 때 1이라고 예측하고, 음수일 때 0이라고 예측
- t를 종종 <b>로짓(logit)</b> 이라고 부름. logit(p) = log(p / 1 - p) 로 정의 되는 로짓 함수가 로지스틱 함수의 역함수라는 사실에서 이름을 따옴
- 실제로 추정 확률 p의 로짓을 계산하면 t값을 얻을 수 있음
- 로짓을 <b>로그-오즈(log-odds)</b>라고도 부름. 로그-오즈는 양성 클래스 추정 확률과 음성 클래스 추정 확률 사이의 로그 비율이기 때문
- `LogisticRegression` 는 클래스 레이블을 반환하는 `predict()` 와 클래스에 속할 확률 값을 
반환하는 `predict_proba()`를 반환
- `predict()` 메서드는 theta^T * x 값이 0보다 클 때를 양성 클래스로 판단하여 결과를 반환하며 `predict_proba()` 메서드는 시그모이드 함수를 적용하여 계산한 확률을 반환

## 훈련과 비용 함수
- 그렇다면 해당 모형을 어떻게 훈련시킬까?
- 훈련의 목적은 양성 샘플(y = 1)에 대해서는 높은 확률을 추정하고, 음성 샘플(y = 0)에 대해서는 낮을 확률을 추정하는 모델의 파라미터 벡터 theta를 찾는 것
- 이러한 아이디어가 하나의 훈련 샘플 x에 대해 나타낸 비용 함수인 다음 식에 드러나 있음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?c(\theta)&space;=&space;\begin{pmatrix}&space;-log(\hat{p})),&space;y&space;=&space;1\\&space;-log(1-&space;\hat{p}),&space;y&space;=&space;0&space;\end{pmatrix}" /></p>

- 이 비용함수는 t가 0에 가까워지면 -log(t) 가 매우 커지므로 타당하다 할 수 있음
- 그러므로 모델이 양성 샘플을 0에 가까운 확률로 추정하면 비용이 크게 증가함
- 또한 음성 샘플을 1에 가까운 확률로 추정해도 비용이 크게 증가함
- 반면에 t가 1에 가까우면 -log(t)는 0에 가까워짐
- 따라서 기대한 대로 음성 샘플의 확률을 0에 가깝게 추정하거나 양성 샘플의 확률을 1에 가깝게 추정하면 비용은 0에 가까워질 것임
- <b>전체 훈련 세트에 대한 비용 함수는 모든 훈련 샘플의 비용을 평균한 것</b>  
  이를 <b>로그 손실(LogLoss)</b>이라고 부르며, 다음과 같이 하나의 식으로 쓸 수 있음
<p align = 'center'><img src="  https://latex.codecogs.com/gif.latex?j(\theta)&space;=&space;-\frac{1}{m}\sum_{m}^{i=1}[y^{(i)}log(\hat{p^{i}})&space;&plus;&space;(1&space;-&space;y^{(i)})log(1&space;-&space;\hat{p^{(i)}})]" /></p>

- 안타깝게도 이 비용 함수의 최솟값을 계산하는 알려진 해가 없음(정규방정식 같은 것이 없음)
- 하지만 이 비용 함수는 볼록 함수이므로 경사 하강법(또는 어떤 다른 최적화 알고리즘)이 전역 최솟값을 찾는 것을 보장함(학습률이 너무 크지 않고 충분히 기다릴 시간이 있다면)
- 이 비용 함수의 j번째 모델 파라미터 theta(j)에 대해 편미분을 하면 다음 식과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\frac{\sigma}{\sigma\theta}J(\theta)&space;=&space;\frac{1}{m}&space;\sum_{i&space;=&space;1}^{m}(\sigma(\theta^{T}x^{(i)})-&space;y^{(i)})&space;x_{j}^{(i)} " /></p>

- 각 샘플에 대해 예측 오차를 계산하고, j번쨰 특성값을 곱해서 모든 훈련 샘플에 대해 평균을 냄
- 모든 편도함수를 포함한 그레디언트 벡터를 만들면 경사 하강법 알고리즘을 사용할 수 있음
- 이 떄 확률적 경사 하강법과 미니배치 경사 하강법은 동일한 개념으로 적용됨
- 다른 선형 모델처럼 로지스틱 회귀 모델도 l1, l2 패널티를 사용하여 규제 가능
- 사이킷런의 LogisticRegression 모델의 규제 강도를 조절하는 하이퍼파라미터는 (다른 선형 모델처럼) alpha가 아니고 그 역수에 해당하는 C. C가 높을수록 모델의 규제가 줄어듬

### 로지스틱 회귀 예제
~~~python
#- logistic regression
#- iris data
#- petal : 꽃잎, sepal : 꽃받침
from sklearn import datasets
import numpy as np
import pandas as pd

iris = datasets.load_iris()
print(list(iris.keys()))

X = iris['data'][:, 3:]  #- 꽃잎의 너비
y = (iris['target'] == 2).astype(int)

#- 로지스틱 회귀 모형 훈련
from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression()
log_reg.fit(X, y)

#- 꽃잎의 너비가 0~3cm인 꽃에 대해 모델의 추정 확률 계산
import matplotlib.pyplot as plt
X_new = np.linspace(0, 3, 1000).reshape(-1, 1)
y_proba = log_reg.predict_proba(X_new)
plt.plot(X_new, y_proba[:, 1], 'g-', label="Iris virginica")
plt.plot(X_new, y_proba[:, 0], 'b--', label="Not Iris virginica")

#- 결과 해석
#- Iris-Verginica 의 꽃잎 너비는 1.4 ~ 2.5cm 사이에 분포
#- 반면 다른 붓꽃은 일반적으로 꽃잎 너비가 더 작아 0.1~1.8cm에 분포. 약간 중첩되는 부분은 존재
#- 양쪽 확률이 50%가 되는 1.6cm 근방에서 결정 경계가 만들어짐

log_reg.predict([[1.7], [1.5]])
~~~
- 다른 선형 모델처럼 로지스틱 회귀 모델도 l1, l2 패털티를 사용하여 규제 가능
- 사이킷런 패키지는 l2를 기본 패널티로함
- `LogisticRegression` 모델의 규제 강도를 조절하는 하이퍼파라미터는 alpha가 아니고 그 역수에 해당하는 C입니다. C가 높을수록 규제가 줄어듬


## 4.6.4 소프트맥스 회귀(다항 로지스틱 회귀)
- 로지스틱 회귀 모델은 여러 개의 이진 분류기를 훈련시켜 연결하지 않고 직접 다중 클래스를 지원하도록 일반화될 수 있음(y의 label이 여러개..)
- 이를 <b>소프트맥스 회귀</b>, <b>다항 로지스틱 회귀</b>라고 함
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=s_{k}(x)&space;=&space;(\theta^{k})^{T}x" target="_blank"><img src="https://latex.codecogs.com/gif.latex?s_{k}(x)&space;=&space;(\theta^{k})^{T}x" title="s_{k}(x) = (\theta^{k})^{T}x" /></a></p>

- 각 클래스는 자신만의 벡터 theta^{k}가 있음(이 theta는 (클래스 수, 특성 수)인 2차원 배열)
- 이 벡터들은 <b>파라미터 행렬(parameter matrix)</b>에 저장됨
- 개념은 매우 간단한데, 샘플 x가 주어지면 소프트맥스 회귀 모델이 각 클래스 k에 대한 점수 sk(x)를 계산하고, 그 점수에 소프트맥스 함수(정규화된 지수 함수 normalized exponential function)를 적용하여 각 클래스의 확률을 추정
- 소프트맥스 점수 계산 식은 다음과 같음
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\hat{p_{k}}&space;=&space;\sigma&space;(s(x))_{k}&space;=&space;\frac{exp(s_{k}(x))}{\sum_{j=1}^{K}exp(s_{j}(x))}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{p_{k}}&space;=&space;\sigma&space;(s(x))_{k}&space;=&space;\frac{exp(s_{k}(x))}{\sum_{j=1}^{K}exp(s_{j}(x))}" title="\hat{p_{k}} = \sigma (s(x))_{k} = \frac{exp(s_{k}(x))}{\sum_{j=1}^{K}exp(s_{j}(x))}" /></a></p>

- K는 클래스 수
- s(x)는 샘플 x에 대한 각 클래스의 점수를 담은 백터
- sigma(s(x))_k는 샘플 x에 대한 각 클래스가 주어졌을 때 이 샘플이 클래스 k에 속할 추정 확률
- 소프트맥스 회귀 분류기의 예측식은 다음과 같음

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\hat{y}&space;=&space;argmax(\sigma({s(x)}))_{k}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{y}&space;=&space;argmax(\sigma({s(x)}))_{k}" title="\hat{y} = argmax(\sigma({s(x)}))_{k}" /></a></p>

- argmax 연산은 함수를 최대화하는 변수의 값을 반환
- 소프트맥스 회귀 분류기는 한 번에 하나의 클래스만 예측하며, 하나의 사진에서 여러 사람의 얼굴을 인식하는 데는 사용할 수 없음
- 이러한 소프트맥스 회귀 모형을 훈련하는 비용함수는 크로스 엔트로피(cross-entropy)를 사용하면 적절함
- 크로스 엔트로피는 추정된 클래스의 확률이 타깃 클래스에 얼마나 잘 맞는지 측정하는 용도로 사용됨
- 크로스 엔트로피 비용함수는 다음과 같음

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=J(\theta)&space;=&space;-\frac{1}{m}\sum_{i=1}^{m}\sum_{k=1}^{K}&space;y_{k}^{(i)}log(\hat{p}_{k}^{(i)})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?J(\theta)&space;=&space;-\frac{1}{m}\sum_{i=1}^{m}\sum_{k=1}^{K}&space;y_{k}^{(i)}log(\hat{p}_{k}^{(i)})" title="J(\theta) = -\frac{1}{m}\sum_{i=1}^{m}\sum_{k=1}^{K} y_{k}^{(i)}log(\hat{p}_{k}^{(i)})" /></a></p>

- y_{k}^{(i)}는 i 번째 샘플이 k 클래스에 속할 확률임. 이는 보통 0 또는 1이 됨
- 딱 2개의 클래스가 있을 때(K = 2) 이 비용 함수는 로지스틱 회귀의 비용 함수와 같음
- 사이킷런의 `LogitsicRegression` 은 클래스가 둘 이상일 때 일대다(OvA) 전략을 사용  
  하지만 multi_class 매개변수를 multinomial로 바꾸면 소프트맥스 회귀를 사용할 수 있음



## 용어 정리
- 크로스 엔트로피
  - 원래 정보 이론에서 유래했는데, 매일 날씨 정보를 효율적으로 전달한다고 가정했을 때 8가지 정보가 있다면(맑음, 흐림 등 ..) 2^{3} = 8 이므로, 이 선택 사항을 3비트를 사용하여 인코딩 할 수 있음  
  - 거의 대부분의 날이 맑음이라면 '맑음'을 하나의 비트(0)로 인코딩하고 다른 7개의 선택 사항을 4비트로 표현하는 것이 효율적임
  - 크로스 엔트로피는 선택 사항마다 전송한 평균 비트 수를 측정
  - 날씨에 대한 가정이 완벽하면 크로스 엔트로피는 날씨 자체의 엔트로피와 동일
  - 하지만 이러한 가정이 틀렸다면 크로스 엔트로피는 <b>쿨백-라이블러 발산</b>이라 불리는 양만큼 커질 것임
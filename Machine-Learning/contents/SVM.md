# SVM(Support Vector Machine)
- SVM은 매우 강력하고 선형이나 비선형 분류, 회귀, 이상치 탐색에도 사용할 수 있는 다목적 ML 모델임
- 복잡한 분류 문제에 잘 들어맞으며 <b>작거나 중간 크기의 데이터 셋에 적합</b>

## 선형 SVM 분류
![img](https://github.com/koni114/Machine-Learning/blob/master/img/LargeMarginClassification.png)

- 위 그림에서 두 클래스가 직선으로 확실히 잘 나뉘어 있음
- 왼쪽 그래프에서 점선은 클래스를 잘 분류하지 못하고 있고, 다른 두 모델은 훈련 세트에 대해서 완벽하게 동작
- 하지만 결정 경계가 샘플에 너무 가까워 새로운 샘플에 대해서는 잘 작동하지 못할 것임
- 오른쪽 그래프의 실선은 SVM 분류기의 결정 경계
- <b>이 직선은 두 개의 클래스로 나누고 있을 뿐만 아니라 제일 가까운 훈련 샘플로부터 가능한 멀리 떨어져 있음</b>
- SVM 분류기를 클래스 사이에 가장 폭이 넓은 도로를 찾는 것으로 생각할 수 있음
- 그래서 <b>Large margin classification</b>이라고 함
- 오른쪽 그래프에서 도로 바깥쪽에 샘플을 더 추가해도 결정 경계에는 전혀 영향을 미치지 않음
- 도로 경계(점선)에 위치한 샘플에 의해 전적으로 결정됨. 이 샘플을 <b>Support Vector</b>라고 함
- <b>SVM은 특성 경계에 민감한데, </b> scale이 너무 좁게 되면 Support vector의 거리가 좁아질 수 있기 때문

### 선형 소프트 마진 분류
- 모든 샘플이 도로 바깥쪽에 올바르게 분류되어 있다면 이를 <b>hard margin classification</b>이라고 함
- 두가지 문제점이 있는데, 데이터가 선형으로 잘 구분되어 있어야하고, 이상치에 민감함  
  예를 들어 이상치 하나가 다른 label 집단에 들어가 있으면 하드 마진을 찾을 수 없음
- 이러한 문제를 피하려면 좀 더 유연한 모델이 필요한데, 도로의 폭을 가능한 한 넓게 유지하는 것과 <b>마진 오류(margin violation)</b>  사이에 적절한 균형을 잡아야 함. 이를 <b>소프트 마진 분류(soft margin classification)</b>이라고 함

![img](https://github.com/koni114/Machine-Learning/blob/master/img/SVM_2.JPG)

- 여러 하이퍼파라미터를 지정할 수 있는데, C(cost)는 이런 하이퍼파라미터 중에 하나임
- C를 <b>감소</b>시켜 모델을 규제 할 수 있음, 즉, C는 마진 오류 비용이라고 생각하면 됨  
(즉, 과대적합인 경우 C를 감소시키자)
- 왼쪽 모델에 마진 오류가 많지만 일반화가 더 잘 될 것 같음
- <b>SVM 분류기는 로지스틱 회귀 분류기와는 다르게 클래스에 대한 확률을 제공하지 않음</b>
- 사이킷런의 `LinearSVC`는 `predict_proba()` 메서드를 제공하지 않지만, `SVC` 모델은 `probability=True`로 매개변수를 지정하면 `predict_proba()` 메서드를 제공. 기본값은 False
- 사이킷런에서 SVC를 만들수 있는 방법 3가지
  - LinearSVC
  - SVC --> SVC(kernel = "linear", C = 1) 
  - SGDClassifier --> SGDClassifier(loss='hinge', alpha = 1/(m*C))  
    선형 SVM 분류기를 사용하기 위해 일반적인 확률적 경사 하강법을 사용. LinearSVC보다는 느리게 수렴하지만, 데이터가 많아 전부 메모리 적재가 어려울 때 유용
- LinearSVC는 SVC와 비교했을 때 규제에 편향이
 들어가기 때문에 SVC와 비교할때는 반드시 `StandardScaler()`를 수행해 주어야 함

## 비선형 SVM 분류
- 선형 SVM 분류기가 효율적이고, 많은 경우에 아주 잘 작동하지만, 선형적으로는 분류할 수 없는 데이터셋이 많음
- 비선형 데이터셋을 다루는 한 가지 방법은 다항 특성과 같은 특성을 더 추가하는 것
- 이렇게 하면 선형적으로 구분되는 데이터셋이 만들어질 수 있음

![img](https://github.com/koni114/Machine-Learning/blob/master/img/SVM_3.JPG)

- 위의 그림에서 왼쪽 그래프는 하나의 특성 x_{1} 만을 가진 간단한 데이터셋을 나타냄
- 그림에서 볼 수 있듯이 이 데이터셋은 선형적으로 구분이 안됨
- 하지만 두 번째 특성 x_{2} = (x1)^{2}을 추가하여 만들어진 2차원 데이터셋은 완벽하게 선형적으로 구분할 수 있음

### 다항식 커널
- 다항식 특성을 추가하는 것은 간단하고 모든 머신러닝 알고리즘에서 잘 작동함
- 낮은 차수 다항식은 매우 복잡한 데이터셋을 잘 표현하지 못하고 높은 차수의 다항식은 굉장히 많은 특성을 추가하므로 모델을 느리게 만듬
- SVM을 사용할 때 <b>커널 트릭(kernel trick)</b>이라는 수학적 기교를 적용할 수 있음
- 커널 트릭은 실제로는 특성을 추가하지 않으면서 다항식 특성을 많이 추가한 것과 같은 결과를 얻을 수 있음
- 어떤 특성도 추가하지 않기 때문에 엄청난 수의 특성 조합이 생기지 않음
- 파이썬에서는 다음과 같이 입력 가능
~~~python
from sklearn.svm import SVC
poly_kernel_svm_clf = Pipeline([
  ("scaler", StandardScaler()),
  ("svm_clf", SVC(kernel = "poly", degree = 3, coef0 = 1, C=5))
])
poly_kernel_svm_clf(X, y)
~~~

![img](https://github.com/koni114/Machine-Learning/blob/master/img/SVM_4.JPG)

- 이 코드는 3차 다항식 커널을 사용해 SVM 분류기를 훈련시킴
- 결과는 위의 그래프의 왼쪽과 같고, 오른쪽 그래프는 10차 다항식 커널을 사용한 또 다른 SVM 분류기 
- 모델이 과대적합이라면 다항식의 차수를 줄여야 함
- 반대로 과소적합이라면 차수를 늘려야 함. `coef0`는 모델이 높은 차수와 낮은 차수에 얼마나 영향을 받을지 조절함
- 적절한 하이퍼파라미터를 찾는 일반적인 방법은 grid search를 사용하는 것
- 처음에는 그리드 폭을 크게하고, 그다음에는 최적의 값을 찾기 위해 그리드를 세밀하게 검색함

### 유사도 특성
- 비선형 특성을 다루는 또 다른 기법은 각 샘플이 특정 <b>랜드마크(landmark)</b>와 얼마나 닮았는지 측정하는 <b>유사도 함수(similarity)</b>로 계산한 특성을 추가하는 것
- 예를 들어 앞에서 본 1차원 데이터셋에 두 개의 랜드마크 x1 = -2와 x1 = 1을 추가하자(위의 왼쪽 그래프)
- 그리고 gamma = 0.3인 가우시안 방사 기저 함수(radial basis function, RBF)를 유사도 함수로 정의하자
- 가우시안 RBF 식은 다음과 같음
<p align = 'center'><img src = "https://latex.codecogs.com/gif.latex?\phi_{\gamma&space;}(x,&space;l)&space;=&space;exp(-\gamma\left&space;\|&space;x&space;-&space;l&space;\right&space;\|^{2})"/></p>

- 'l'은 랜드마크 지점이며, r은 0보다 커야하며, 값이 작을수록 넓은 종모양이 됨 
- 이 함수의 값은 0부터 1까지 변화하며 종 모양으로 나타남 
- 이제 새로운 특성을 만들 준비가 되었음. 예를 들어 x1 = -1 샘플을 살펴보자. 이 샘플은 첫 번째 랜드마크에서 1만큼 떨어져 있고 두 번째 랜드마크에서 2만큼 떨어져 있음
- 그러므로 새로 만든 특성은 x2 = exp(-0.3 x (-1-(-2))^2) `= 0.74 와 x3 = exp(-0.3x(1-(-1))^2) = 0.30`임 위의 오른쪽 그래프는 변환된 데이터셋을 보여줌 
- 그림에서 볼 수 있듯이 이제 선형적으로 구분이 가능
- 랜드마크를 어떻게 선택하는지 궁금할 것임. 간단한 방법은 데이터셋에서 있는 모든 샘플 위치에 랜드마크를 설정하는 것
- 이렇게 하면 차원이 매우 커지고 따라서 변환된 훈련 세트가 선형적으로 구분될 가능성이 높음
- 단점은 훈련 세트에 있는 n개의 특성을 가진 m개의 샘플이, m개의 특성을 가진 m개의 샘플로 변환된다는 것. 훈련 세트가 매우 클 경우 동일한 크기의 아주 많은 특성들이 만들어짐

![img](https://github.com/koni114/Machine-Learning/blob/master/img/SVM_10.JPG)

### gamma, C(오류 비용) 간단 정리
- gamma, C(cost)는 커질수록 모델의 불규칙적이며, 과대적합될 우려가 있음
- gamma, C(cost)는 작아질수록 모델이 일반화되며, 과소적합될 우려가 있음

### 가우시안 RBF 커널
- <b>다항 특성 방식과 마찬가지로 유사도 특성 방식도 ML 알고리즘에 유용하게 사용될 수 있음</b>
- 추가 특성을 모두 계산하려면 연산 비용이 많이 드는데 특히 훈련 세트가 클 경우 더 그렇게 됨
- 여기서 커널 트릭이 한번 더 SVM의 마법을 만듬!
- 유사도 특성을 많이 추가하는 것과 비슷한 결과를 얻을 수 있음
- 가우시안 RBF 커널을 이용한 SVC 모델을 시도해보자
~~~python
rbf_kernel_svm_clf = Pipeline([
  ("scaler", StandardScaler()),
  ("svm_clf", SVC(kernel="rbf", gamma=5, C=0.001))
])
rbf_kernel_svm_clf.fit(X, y)
~~~
- 위의 python 모델이 하단 이미지의 왼쪽 아래에 나타나 있음
- 다른 그래프들은 gamma와 C의 값을 바꾸어서 훈련시킨 모델
- <b>gamma를 증가시키면 종 모양 그래프가 좁아져서</b> 각 샘플의 영향 범위가 작아짐
- 결정 경계가 조금 더 불규칙해지고 각 샘플을 따라 구불구불하게 휘어짐
- 반대로 작은 gamma 값은 넓은 종 모양 그래프를 만들며 각 샘플의 영향 범위에 걸쳐 영향을 주므로 결정 경계가 더 부드러워짐
- 결국 하이퍼파라미터 gamma가 규제의 역할을 함
- 모델이 과대적합일 경우엔 감소시켜야하고 과소적합일 경우엔 증가시켜야함(hyper-parameter C와 비슷)
 
![img](https://github.com/koni114/Machine-Learning/blob/master/img/SVM_5.JPG)

- 다른 커널도 있지만 거의 사용되지 않음. 어떤 커널은 특정 데이터 구조에 특화되어 있음
- <b>문자열 커널(string kernel)</b>이 가끔 텍스트 문서나 DNA 서열을 분류할 때 사용  
  (예를 들면 문자열 서브시퀀스 커널이나 레벤슈타인 거리기반의 커널)
- 여러 가지 커널 중 어떤 것을 사용해야 할까? 경험적으로 봤을 때 언제나 선형 커널을 가장 먼저 시도해 봐야함.  
<b>특히 훈련 세트가 아주 크거나 특성 수가 많을 경우에 그렇게 됨</b>
- 훈련 세트가 너무 크지 않다면 가우시안 RBF 커널도 시도해보자

### 계산 복잡도
- `LinearSVC` 파이썬 클래스는 선형 SVM을 위한 최적화된 알고리즘을 구현한 `liblinear` 라이브러리를 기반으로 하는데, 훈련 시간 복잡도는 O(m x n) 정도임
- 정밀도를 높이면 알고리즘 수행 시간이 길어짐. 이는 허용오차 하이퍼파라미터 입실론으로 조절함
- 대부분의 분류 문제는 허용오차를 기본값으로두면 잘 작동함
- python의 SVC는 커널 트릭 알고리즘을 구현한 libsvm 라이브러리를 기반으로 함  
  훈련의 시간 복잡도는 보통 O(m^2 x n)과 O(m^3 x n) 사이  
- 이는 훈련 샘플 수가 커지면 엄청나게 느려진다는 것을 의미함
- 복잡하지만 작거나 중간규모의 훈련 세트에 이 알고리즘이 잘 맞음
- 하지만 특성의 개수에는, 특히 희소 특성(sparse features, 각 샘플에 0이 아닌 특성이 몇 개 없는 경우)인 경우에는 잘 확장됨
- 이런 경우 알고리즘의 성능이 샘플이 가진 0이 아닌 특성의 평균 수에 비례함

## SVM 회귀
- 앞서 이야기한 것처럼 SVM 알고리즘은 다목적으로 사용할 수 있음
- 선형, 비선형 분류뿐만 아니라 선형, 비선형 회귀에도 사용 가능. SVM을 분류가 아니라 회귀에 적용하는 방법은 목표를 반대로 하는 것
- <b>제한된 마진 오류(도로 밖의 샘플) 안에서 도로 안에 가능한 한 많은 샘플이 들어가도록 학습</b>
- 도로의 폭은 하이퍼파라미터 입실론으로 조절함
- 아래 그래프는 무작위로 생성한 선형 데이터셋에 훈련시킨 두 개의 선형 SVM 회귀 모델을 보여줌
- 하나는 마진을 크게 하고(입실론 = 1.5) 다른 하나는 마진을 작게(입실론 = 0.5)하여 만듬

![img](https://github.com/koni114/Machine-Learning/blob/master/img/SVM_6.JPG)

- 마진 안에서는 훈련 샘플이 추가되어도 모델 예측에는 큰 영향이 없음. 그래서 이 모델을 <b>입실론에 민감하지 않다(epsilon-insentive)</b>고 말함
- 사이킷런의 `LinearSVR`을 사용해 선형 SVM 적용 가능
- 비선형 회귀 작업을 처리하려면 커널 SVM 모델을 사용하는데, 아래 그래프는 임의의 2차방정식 형태의 훈련 세트에 2차 다항 커널을 사용한 SVM 회귀를 보여줌
- 왼쪽 그래프는 규제가 거의 없고, 오른쪽 그래프는 규제가 훨씬 많음

![img](https://github.com/koni114/Machine-Learning/blob/master/img/SVM_7.JPG)

- 사이킷런에서 SVR은 SVC의 회귀 버전임, LinearSVR은 필요한 시간이 훈련 세트의 크기에 비례해서 선형적으로 늘어남
- 하지만 SVR은 훈련 세트가 커지면 훨씬 느려짐 

## SVM 이론
- 이 절에서 SVM의 이론은 어떻게 이뤄지는지, 그리고 SVM의 훈련 알고리즘이 어떻게 작동하는지 설명
- 먼저 선형 SVM 분류기부터 시작
- 먼저 표기법을 정리하자. 편향 theta(0)와 입력 특성의 가중치 theta(1) ~ theta(n)까지 모델 파라미터를 하나의 벡터 theta에 넣음
- 그리고 모든 샘플에 편향에 해당하는 입력값 x(0) = 1 을 추가
- 여기서는 SVM을 다룰 때 조금 더 편리한 표기법을 사용하겠음. 편향을 b라 하고 특성의 가중치 벡터를 w라 하겠음. 따라서 입력 특성 벡터에 편향을 위한 특성이 추가되지 않음

### 결정 함수와 예측
- 선형 SVM 분류기 모델은 단순히 결정 함수 w^(T)x + b = w1x1 + w1x2 + ... wnxn + b 를 계산해서 새로운 샘플 x의 클래스를 예측
- 결괏값이 0보다 크면 예측값은 양성, 0보다 작으면 예측값은 음성임
- 다음의 식을 가볍게 참조하자
<p align = 'center'><img src = "https://latex.codecogs.com/gif.latex?\hat{y}&space;=&space;\begin{Bmatrix}&space;0&space;&&space;w^{T}x&space;&plus;&space;b&space;<&space;0\\&space;1&space;&&space;w^{T}x&space;&plus;&space;b&space;\geq&space;0&space;\end{Bmatrix}"/></p>

![img](https://github.com/koni114/Machine-Learning/blob/master/img/SVM_2.JPG)

![img](https://github.com/koni114/Machine-Learning/blob/master/img/SVM_8.JPG)
  
- 위의 두 개의 이미지 중 첫번째 이미지의 오른쪽 그래프의 결정함수가 두 번째 이미지에 나타나 있음
- 특성이 2개인 데이터셋이기 때문에 2차원 평면임
- <b>결정 경계는 결정 함수의 값이 0인 값들로 이루어져 있음</b>
- 이는 두 평면의 교차점으로 직선임(굵은 실선)  
  (조금 더 일반적으로 말하면 n개의 특성이 있을 때 결정 함수는 n차원의 초평면(hyperplaine)이고 결정 경계는 n-1차원의 초평면
  )
- 점선은 결정 함수의 값이 -1 또는 1인 점들을 나타냄
- 이 선분은 결정 경계에 나란하고 일정한 거리만큼 떨어져서 마진을 형성하고 있음
- 선형 SVM 분류기를 훈련한다는 것은 마진 오류를 하나도 발생하지 않거나(하드 마진) 제한적인 마진 오류를 가지면서(소프트 마진) <b>가능한 한 마진을 크게 하는 w와 b를 찾는 것</b>

### 목적 함수
- 결정 함수의 기울기를 생각해보면 이는 가중치 벡터의 노름 ||w||와 같음  
  (그냥 기울기가 W다! 라는 의미)
- 이 기울기를 2로 나누면 결정 함수 값이 +-이 되는 점들이 결정 경계로부터 2배만큼 멀어짐  
  (결정 경계는 반드시 결정 함수 값이 -1, +1인 점 이므로)
- <b>즉 기울기를 2로 나누는 것은 마진에 2를 곱하는 것과 같음</b>
- 다음의 2차원 그래프를 보면 이해하기 쉬움. <b>가중치 벡터가 작을수록 경계는 커짐!</b>

![img](https://github.com/koni114/Machine-Learning/blob/master/img/SVM_9.JPG)

- 마진을 크게 하기 위해 ||W||를 최소화하려고 함
- 마진 오류를 하나도 만들지 않으려면, 결정 함수가 모든 양성 훈련 샘플에서는 1보다 커야 하고 음성 훈련 샘플에서는 -1보다 작아야 함
- 음성 샘플(y(i) = 0)일 때 t(i) = -1로, 양성 샘플(y(i) = 1)일 때 t(i) = 1로 정의하면 앞서 말한 제약 조건을 모든 샘플에서 다음의 식으로 표현 가능
<p align = 'center'><img src = "https://latex.codecogs.com/gif.latex?t^{(i)}(w^{T}x^{(i)}&space;&plus;&space;b)&space;\geq&space;1"/></p>

- 그러므로 하드 마진 선형 SVM 분류기의 목적 함수를 아래의 최적화(optimization) 문제로 표현할 수 있음
<p align = 'center'><img src = "https://latex.codecogs.com/gif.latex?\begin{pmatrix}&space;minimize,&space;\frac{1}{2}W^{T}W&&space;contraint,&space;t^{(i)}(w^{T}x^{(i)}&space;&plus;&space;b)&space;\geq&space;1&space;\end{pmatrix}"/></p>

- ||W||를 최소화하는 대신, (1/2) * ||W||^2 을 최소화함
- 그 이유는 후자가 깔끔하게 미분되기 때문. 반면 전자는 0에서 미분 불가능
- 최적화 알고리즘은 미분할 수 있는 함수에서 잘 작동
- 소프트 마진 분류기의 목적 함수를 구성하려면 각 샘플에 대해 slack variable `S >= 0`을 도입해야 함
- S(i)는 i번째 샘플이 얼마나 마진을 위반할지 정함
- 이 문제는 두 개의 상충되는 목표를 가지고 있음. 마진 오류를 최소화하기 위해 가능한 한 슬랙 변수의 값을 작게 만드는 것과 마진을 크게 하기 위해 (1/2)*W^(T)*W를 가능한 한 작게 만드는것  
- SVM 회귀를 위한 목적함수는 분류의 경우와 조금 다름. 회귀에서는 결정 경계의 양쪽으로 모든 샘플을 담기 위한 도로의 오차 폭을 두 개의 슬랙 변수 S, S*라고 할 때 다음 두 조건을 만족하는 목적 함수를 구성함
<p align = 'center'><img src = "https://latex.codecogs.com/gif.latex?\begin{pmatrix}&space;y^{(i)}&space;-(W^{T}&space;\cdot&space;X^{i}&space;&plus;&space;b)&space;\leq&space;\epsilon&space;&plus;&space;S^{(i)})&space;&&space;(W^{T}&space;\cdot&space;X^{i}&space;&plus;&space;b)&space;-&space;y^{(i)}&space;\leq&space;\epsilon&space;&plus;&space;S^{(i)})&space;\end{pmatrix}"/></p>

- <b>여기에 하이퍼파라미터 C(cost)가 등장함. 이 파라미터는 두 목표 사이의 트레이드오프를 정의함</b>
- 결국 밑에 있는 제약을 가진 최적화 문제가 됨

<p align = 'center'><img src = "https://latex.codecogs.com/gif.latex?\begin{pmatrix}&space;minimize&space;\frac{1}{2}&space;\cdot&space;W^{T}W&space;&plus;&space;C\sum_{i=1}^{m}S^{(i)}&space;\\&space;i&space;=&space;1,&space;2,&space;...,&space;m&space;\\&space;t^{(i)}(W^{T}x^{(i)}&space;&plus;&space;b)&space;\geq&space;1&space;-&space;S^{(i)},&space;S^{(i)}&space;\geq&space;0&space;\end{pmatrix}"/></p>

### 콰드라틱 프로그래밍
- 하드 마진과 소프트 마진 문제는 모두 선형적인 제약 조건이 있는 볼록 함수의 이차 최적화 문제 
- 이런 문제를 <b>콰드라틱 프로그래밍(QP)문제</b>라고 함
- 여러 가지 테크닉으로 QP 문제를 푸는 알고리즘이 많이 있지만 이 책의 범위를 벗어남

### 쌍대 문제
- 원문제(primal problem)이라는 제약이 있는 최적화 문제가 주어지면 <b>쌍대 문제(dual problem)</b>라고 하는 깊게 관련된 다른 문제로 표현할 수 있음
- 일반적으로 쌍대 문제 해는 원 문제 해의 하한값이지만, 목적 함수가 볼록 함수이고 부등식 제약조건이 연속 미분 가능하면서 볼록함수이면 원문제와 똑같은 해를 제공
- 중요한건 SVM 문제는 위의 조건을 만족함. 따라서 원문제 또는 쌍대 문제 중 하나를 선택해서 풀 수 있음
- 아래 식이 선형 SVM 목적 함수의 쌍대 형식임

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=minimize&space;\frac{1}{2}&space;\sum_{i=1}^{m}\sum_{j=1}^{m}&space;\alpha^{(i)}\alpha^{(j)}&space;t^{(i)}&space;t^{(j)}&space;x^{(i)^{T}}x^{j}&space;-&space;\sum_{i=1}^{m}\alpha^{(i)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?minimize&space;\frac{1}{2}&space;\sum_{i=1}^{m}\sum_{j=1}^{m}&space;\alpha^{(i)}\alpha^{(j)}&space;t^{(i)}&space;t^{(j)}&space;x^{(i)^{T}}x^{j}&space;-&space;\sum_{i=1}^{m}\alpha^{(i)}" title="minimize \frac{1}{2} \sum_{i=1}^{m}\sum_{j=1}^{m} \alpha^{(i)}\alpha^{(j)} t^{(i)} t^{(j)} x^{(i)^{T}}x^{j} - \sum_{i=1}^{m}\alpha^{(i)}" /></a></p>

- [조건] i = 1, 2, ..., m일때 alpha^{(i)} >= 0
- 이 식을 최소화하는 벡터 hat alpha를 찾았다면 아래 식을 사용해 원 문제의 식을 최소화하는 hat w , hat b를 계산할 수 있음

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\hat{W}&space;=&space;\sum_{i=1}^{m}\hat{\alpha}^{(i)}t^{(i)}x^{(i)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{W}&space;=&space;\sum_{i=1}^{m}\hat{\alpha}^{(i)}t^{(i)}x^{(i)}" title="\hat{W} = \sum_{i=1}^{m}\hat{\alpha}^{(i)}t^{(i)}x^{(i)}" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\hat{b}&space;=&space;\frac{1}{n_{s}}\sum_{i=1}^{m}(t^{(i)}&space;-&space;\hat{W}^{T}x^{(i)})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{b}&space;=&space;\frac{1}{n_{s}}\sum_{i=1}^{m}(t^{(i)}&space;-&space;\hat{W}^{T}x^{(i)})" title="\hat{b} = \frac{1}{n_{s}}\sum_{i=1}^{m}(t^{(i)} - \hat{W}^{T}x^{(i)})" /></a></p>

- 훈련 샘플 수가 특성 개수보다 작을 때 원 문제보다 쌍대 문제를 푸는 것이 더 빠름
- <b>더 중요한 것은 원 문제에서는 적용이 안되는 커널 트릭을 가능하게 함</b>

### 커널 SVM
- 예를 들어 2차원 데이터셋에 2차 다항식 변환을 적용하고 선형 SVM 분류기를 변환된 이 훈련 세트에 적용한다고 해보자
- 아래 식은 우리가 적용하고자 하는 2차 다항식 매핑함수 phi 임
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\phi(x)&space;=&space;\phi(\binom{x1}{x2})&space;=&space;\begin{pmatrix}&space;x_{1}^{2}\\&space;\sqrt{2}x1x2\\&space;x_{2}^{2}&space;\end{pmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\phi(x)&space;=&space;\phi(\binom{x1}{x2})&space;=&space;\begin{pmatrix}&space;x_{1}^{2}\\&space;\sqrt{2}x1x2\\&space;x_{2}^{2}&space;\end{pmatrix}" title="\phi(x) = \phi(\binom{x1}{x2}) = \begin{pmatrix} x_{1}^{2}\\ \sqrt{2}x1x2\\ x_{2}^{2} \end{pmatrix}" /></a></p>

- 변환된 벡터는 특성 차원이 2차원 -> 3차원이 됨
- 두 개의 2차원 벡터 a와 b에 2차 다항식 매핑을 적용한 다음 변환된 벡터로 점곱(dot product)을 하면 어떻게 되는지 살펴보자

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\phi(a)^{T}\phi(b)&space;=&space;\begin{pmatrix}&space;a_{1}^{2}\\&space;\sqrt{2}ab\\&space;b_{2}^{2}&space;\end{pmatrix}&space;\begin{pmatrix}&space;a_{1}^{2}\\&space;\sqrt{2}ab\\&space;b_{2}^{2}&space;\end{pmatrix}&space;=&space;a_{1}^{2}b_{1}^{2}&space;&plus;&space;2a_{1}b_{1}a_{2}b_{2}&space;&plus;&space;a_{2}^{2}b_{2}^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\phi(a)^{T}\phi(b)&space;=&space;\begin{pmatrix}&space;a_{1}^{2}\\&space;\sqrt{2}ab\\&space;b_{2}^{2}&space;\end{pmatrix}&space;\begin{pmatrix}&space;a_{1}^{2}\\&space;\sqrt{2}ab\\&space;b_{2}^{2}&space;\end{pmatrix}&space;=&space;a_{1}^{2}b_{1}^{2}&space;&plus;&space;2a_{1}b_{1}a_{2}b_{2}&space;&plus;&space;a_{2}^{2}b_{2}^{2}" title="\phi(a)^{T}\phi(b) = \begin{pmatrix} a_{1}^{2}\\ \sqrt{2}ab\\ b_{2}^{2} \end{pmatrix} \begin{pmatrix} a_{1}^{2}\\ \sqrt{2}ab\\ b_{2}^{2} \end{pmatrix} = a_{1}^{2}b_{1}^{2} + 2a_{1}b_{1}a_{2}b_{2} + a_{2}^{2}b_{2}^{2}" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex==&space;(a_{1}b_{1}&space;&plus;&space;a_{2}b_{2})^{2}&space;=&space;(\binom{a_{1}}{a_{2}}^{T}&space;\binom{b_{1}}{b_{2}})^{2}&space;=&space;(a^{T}b)^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;(a_{1}b_{1}&space;&plus;&space;a_{2}b_{2})^{2}&space;=&space;(\binom{a_{1}}{a_{2}}^{T}&space;\binom{b_{1}}{b_{2}})^{2}&space;=&space;(a^{T}b)^{2}" title="= (a_{1}b_{1} + a_{2}b_{2})^{2} = (\binom{a_{1}}{a_{2}}^{T} \binom{b_{1}}{b_{2}})^{2} = (a^{T}b)^{2}" /></a></p>

- <b>결과가 어떤가요? 변환된 벡터의 점곱이 원래 벡터의 점곱의 제곱과 같음</b>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\phi(a)^{T}\phi(b)&space;=&space;(a^{T}b)^2" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\phi(a)^{T}\phi(b)&space;=&space;(a^{T}b)^2" title="\phi(a)^{T}\phi(b) = (a^{T}b)^2" /></a>
</p>

- <b>핵심은 아래의 식으로 변환할 수 있다는 것!</b>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\phi(a)^{T}\phi(b)&space;=&space;(x^{(i)^{T}}x^{(j)})^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\phi(a)^{T}\phi(b)&space;=&space;(x^{(i)^{T}}x^{(j)})^{2}" title="\phi(a)^{T}\phi(b) = (x^{(i)^{T}}x^{(j)})^{2}" /></a></p>

- 그래서 실제로 훈련 샘플을 변환할 필요가 전혀 없음. 즉 쌍대 식에 있는 점곱을 제곱으로 바꾸기만 하면됨
- 결괏값은 실제로 훈련 샘플을 어렵게 변환해서 선형 SVM 알고리즘을 적용하는 것과 완전히 같음
- 하지만 이 기법이 전체 과정에서 필요한 계산량 측면에서 훨씬 효율적임
- 바로 이것이 커널 트릭!
- <b>함수 K(a, b) = (a^{T} b)^2 를 2차 다항식 커널이라고 부름</b>
- <b>머신러닝에서 커널은 변환 phi를 계산하지 않고 원래 벡터 a와 b에 기반하여 점곱 phi(a)^{T} phi(b)를 계산할 수 있는 함수</b>
- 다음은 가장 널리 사용되는 커널의 일부를 나열함

![img](https://github.com/koni114/Machine-Learning/blob/master/img/SVM_kernel.JPG)

### 온라인 SVM
- 온라인 SVM 분류기를 구현하는 한 가지 방법은 원 문제로부터 유도된 비용함수를 최소화하기 위한 경사 하강법을 사용하는 것
- 경사 하강법은 QP 기반 방법보다 훨씬 느리게 수렴
- 선형 SVM 분류기 비용 함수는 다음과 같음

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=J(W,&space;b)&space;=&space;\frac{1}{2}W^{T}W&space;&plus;&space;C\sum_{i=1}^{m}&space;max(0,&space;1&space;-&space;t^{(i)}(w^{T}x^{(i)}&space;&plus;&space;b))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?J(W,&space;b)&space;=&space;\frac{1}{2}W^{T}W&space;&plus;&space;C\sum_{i=1}^{m}&space;max(0,&space;1&space;-&space;t^{(i)}(w^{T}x^{(i)}&space;&plus;&space;b))" title="J(W, b) = \frac{1}{2}W^{T}W + C\sum_{i=1}^{m} max(0, 1 - t^{(i)}(w^{T}x^{(i)} + b))" /></a></p>

- 이 비용함수의 첫 번째 항은 모델이 작은 가중치 벡터 w를 가지도록 제약을 가해 마진을 크게 만듬
- 두 번째 항은 모든 마진 오류를 계산. 어떤 샘플이 도로에서 올바른 방향으로 벗어나 있다면 마진 오류는 0
- 그렇지 않다면 마진 오류는 올바른 방향의 도로 경계선까지의 거리에 비례
- 이 항을 최소화하면 마진 오류를 가능한 한 줄이고 크기도 작게 만듬

### 힌지 손실
- <b>max(0, 1 - t) 함수를 힌지 손실(hinge loss) 라고 함</b>
- t = 1에서 서브그레디언트를 사용해 경사 하강법 사용 가능

 ## 용어 정리
- 노름(Norm)
  - 벡터의 크기
- 기저 함수(basis function)
  - 비선형 함수를 만들어내려면 비선형 함수를 충분히 많이 생각해 낼 수 있어야 함
  - 이러한 고충을 덜기 위해 만들어진 것이 기저함수(basis function)임
  - 특정한 규칙에 따라 만들어진 <b>함수의 열(sequence)</b>로서 충분히 많은 수의 함수가 있으면 어떤 모양의 함수라도 흉내낼 수 있다는 것을 말함
  - <b>쉽게 얘기하면 여러 함수를 조합해서 만든 함수라고 생각하면 편할 듯!</b>
  - 다항 회귀는 다항 기저함수를 사용하는 기저 함수 모형임
- 커널 트릭(kernel trick)
  - 기존 특성에서 고차원의 특성들을 직접 추가하지 않아도 커넡 트릭을 이용해서 고차원의 특성을 추가한 것과 같은 효과를 가져올 수 있음
- 서브그레디언트
  - 미분 불가능한 점 주위의 그레디언트들의 중간 값 정도를 말함
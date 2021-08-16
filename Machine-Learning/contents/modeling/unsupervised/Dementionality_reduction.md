# 차원 축소(Dimension shrink)
## 차원 축소
- 많은 경우 ML 문제는 훈련 샘플 각각이 수천, 수백만 개의 특성을 가지고 있음
- 이런 많은 특성은 훈련을 느리게 할 뿐만 아니라 좋은 솔루션을 찾기 어렵게 만듬
- 이런 문제를 종종 <b>차원의 저주(cuse of dimensionality)</b>라고 함
- 차원을 축소시키면 일부 정보가 유실되며, 훈련 속도는 빨라질 수 있지만 시스템의 성능이  
  조금 나빠질 수 있음
- 그러므로 차원 축소를 하기 전에 훈련이 너무 느린지, 원본 데이터로 시스템을 훈련해봐야 함
- 어떤 경우에는 훈련 데이터의 차원을 축소시키면 잡음이나 불필요한 세부사항을 걸러내므로  
  성능을 높일 수 있음
- 차원 축소는 훈련 속도를 높이는 것과 데이터 시각화에도 아주 유용함
- 차원 수를 둘로 줄이면 고차원 훈련 세트를 하나의 압축된 그래프로 그릴 수 있고,  
  군집 같은 시각적인 패턴을 감지해 중요한 통찰을 얻는 경우가 많이 있음  

## 차원의 저주
- 우리는 3차원 세계에서 살고 있어 고차원 공간을 직관적으로 상상하기는 어려움
- 1,000차원 공간에서 휘어져 있는 200차원의 타원체는 고사하고 기본적인 4차원 초입방체 조차도  
  머릿속에 그리기가 어려움
- 단위 면적에서 임의의 두 점을 선택하면 두 점 사이의 거리는 평균적으로 대략 0.52가 됨
- 3차원 큐브에서 임의의 두 점을 선택하면 평균 거리는 대략 0.66
- 1,000,000 차원의 초입방체에서 두 점을 무작위로 선택하면 평균 거리는 428.25
- 고차원은 많은 공간을 가지고 있기 때문
- <b>이로 인해 고차원 데이터셋은 매우 희박할(Sparse) 위험이 있음</b> 
- 즉 대부분의 훈련 데이터가 서로 멀리 떨어져 있음. 이는 새로운 샘플도 훈련 샘플과 멀리 떨어져 있을 가능성이 높다는 의미
- 이 경우 예측을 위해서 훨씬 많은 외삽(extrapolation)을 해야하기 떄문에 저차원일 때보다 예측이 더 불안정함
- 간단히 말해 훈련 세트의 차원이 클수록 과대적합의 위험이 커짐
- 이론적으로 차원의 저주를 해결하는 해결책 하나는 훈련 샘플의 밀도가 충분히 높아질 때까지 훈련 세트의 크기를 키우는 것
- 불행하게도 일정 밀도에 도달하기 위해 필요한 샘플 수는 차원 수가 커짐에 따라 기하급수적으로 늘어남

## 차원 축소를 위한 접근 방법
- 차원을 감소시키는 두 가지 주요한 접근법인 투영(projection)과 매니폴드(manifold) 학습을 알아보자

### 투영(projection)
- 대부분의 실전 문제는 훈련 샘플이 모든 차원에 걸쳐 균일하게 퍼져 있지 않음
- 많은 특성들은 거의 변화가 없고, 다른 특성들은 서로 강하게 연관되어 있음
- 결과적으로 모든 훈련 샘플이 고차원 공간 안의 <b>저차원 부분 공간(subspace)</b>에 놓여 있음

### 매니폴드 학습
![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/dimensionality_reduction_2.png)
- 스위스 롤은 2D 매니폴드의 한 예 
- 간단히 말해 2D 매니폴드는 고차원 공간에서 휘어지거나 뒤틀린 2D 모양  
  (위의 그림에서 오른쪽 그림은 2D 매니폴드의 한 예)
- 더 일반적으로 d차원 매니폴드는 국부적으로 d차원 초평면으로 보일 수 있는 n차원 공간의 일부(d < n)
- 스위스 롤의 경우에는 d = 2이고, n = 3임
- 많은 차원 축소 알고리즘이 훈련 샘플이 놓여 있는 매니폴드를 모델링하는 식으로 작동  
  이를 <b>매니폴드 학습</b>이라고 함
- 이는 대부분 실제 고차원 데이터셋이 더 낮은 저차원 매니폴드에 가깝게 놓여 있다는 <b>매니폴드 가정(manifold assumption)</b> 또는 매니폴드 가설에 근거
- 여기서 MNIST로 생각해보자. 전체 손글씨 숫자 이미지는 어느 정도 비슷한 면이 있는데,  
  선으로 연결되어 있고 경계는 흰색이고 어느 정도 중앙에 위치함
- 무작위로 생성된 이미지라면 그중 아주 적은 일부만 손글씨 숫자처럼 보일 것임 
- 다시 말해 숫자 이미지를 만들 때 가능한 자유도는 아무 이미지나 생성할 때의 자유도보다 훨씬 낮음
- 이런 제약은 데이터셋을 저차원의 매니폴드로 압축할 수 있도록 도와줌
- 매니폴드 가정은 이 저차원의 매니폴드 공간에 표현되면 더 간단해 질 것 이라는 가정을 동반  
  하지만 항상 이 가정이 맞는 것은 아님.
- 당연히 차원을 늘렸을 때 더 간단하게 데이터를 분할 시킬 수 있는 경우가 있음!
- 결과적으로 무조건 차원 수를 낮춘다고 성능 향상이 되는 것은 아님

## PCA(principal component Analysis)
- 주성분 분석은 가장 인기 있는 차원 축소 기법 중 하나
- 먼저 데이터에 가장 가까운 초평면을 정의한 다음, 데이터를 이 평면에 투영 시킴

### 분산 보존
- 저차원의 초평면에 훈련 세트를 투영하기 전에 먼저 올바른 초평면을 선택해야 함
- 2D 데이터셋을 1차원 초평면에 투영시킬 때, 분산이 최대한 보존되는 축을 선택하는 것이 정보가 가장 적게  
  손실되므로 합리적으로 보임
- 이 선택을 다른 방식으로 설명하면, <b>원본 데이터셋과 투영된 것 사이의 평균 제곱 거리를 최소화 하는 축</b>
- 이 방식이 PCA를 더 간단하게 설명할 수 있음

### 주성분
- PCA는 훈련 세트에서 분산이 최대인 축을 찾음
- 또한 첫 번째 축에서 직교하고 남은 분산을 최대한 보존하는 두 번째 축을 찾음
- 고차원 데이터셋이라면 PCA는 이전의 두축에 직교하는 세 번째 축을 찾으며 데이터셋에 있는 차원의 수만큼 네 번째, 다섯 번째, ... n번째 축을 찾음
- i번째 축을 이 데이터의 i번째 주성분(Principle Component)라고 부름
- 첫번째 축에서 두번째 주성분은 첫번째 축의 수직, <b>세 번째 축은 이 첫번째 두번째 축이 만드는 평면에 수직</b> 
- 각 주성분을 위해 PCA는 주성분 방향을 가리키고 원점에 중앙이 맞춰진 단위 벡터를 찾음
- 하나의 축에 단위 벡터가 반대 방향으로 두 개이므로, PCA가 반환하는 단위 벡터의 방향을 일정하지 않음
- 즉, <b>주성분의 방향은 일치하지 않음</b>
- 훈련 세트를 조금 섞은 다음, 다시 PCA를 적용하면 새로운 PC 중 일부가 원래 방향과 반대 방향일 수 있음
- 그러나 일반적으로 같은 축에 놓여 있을 것임
- 어떤 경우에는 한 쌍의 PC가 회전하거나 서로 바뀔 수 있지만 보통은 같은 평면을 구성함
- 훈련 세트의 주성분을 어떻게 찾을 수 있을까?
- 다행히 특잇값 분해(singular value decomposition, SVD)라는 표준 행렬 분해 기술이 있어  
  훈련 세트 행렬 X를 세 개의 행렬의 행렬 곱셈인 U* Sigma(V^T)로 분해 할 수 있음
- 여기서 찾고자 하는 모든 주성분의 단위 벡터가 V과 같이 담겨 있음  
  - V = (C1 C2 ... Cn)
- 사이킷런의 PCA 파이썬 클래스는 데이터의 평균을 0으로 해주는 작업을 대신 해줌

### 주성분 축 계산 
- 일반적으로 고유값-분해(eigenvalue-decomposition)과 특이값 분해(Singular value-decomposition)을 이용해 계산 가능

### d차원으로 투영하기
- 주성분을 모두 추출해냈다면 처음 d개의 주성분으로 정의한 초평면에 투영하여 데이터셋의 차원을 d차원으로 축소 시킬 수 있음
- 이 초평면은 분산을 가능한 한 최대로 보존하는 투영임을 보장함
- 초평면에 훈련 세트를 투영하고, d차원으로 축소된 데이터셋 X를 얻기 위해서는 행렬 X와 V의 첫 d열로 구성된  
  행렬 W(d)를 행렬 곱셈하면 됨
- X(d-proj) = XW(d)

~~~python
#- 차원 축소(Dimensionality Reduction)
#- SVD(특잇값 분해)를 이용하여 주성분 뽑아내기
from sklearn.datasets import load_iris
import numpy as np
iris = load_iris()
X = iris.data
y = iris.target
X_centered = X - X.mean(axis=0)
U, s, Vt = np.linalg.svd(X_centered)

c1 = Vt.T[:, 0]
c2 = Vt.T[:, 1]

#- 2개의 주성분으로 정의된 평면에 데이터를 투영
W2 = Vt.T[:, :2]
X2D = X_centered.dot(W2)
~~~

### 사이킷런을 사용해서 주성분 구하기
- 사이킷런의 PCA 모델은 SVD 분해 방법을 사용하여 구현
- 다음은 PCA 모델을 사용해 데이터셋의 차원을 2로 줄이는 코드(사이킷런의 PCA 모델은 자동으로 데이터를 중앙에 맞춰줌)
~~~python
# 사이킷런을 이용해서 주성분 만들기
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X2D = pca.fit_transform(X)
print(X2D)
~~~
- `components_` 속성에 W^d의 전치가 담겨 있음(예를들어 첫 번째 주성분을 정의하는 단위 벡터는 `pca.components_.T[:0]` 입니다)

### 설명된 분산의 비율
- 설명된 분산의 비율(explained variance ratio)도 유용한 정보 중 하나
- `explained_variance_ratio_` 변수에 저장된 주성분의 설명된 분산의 비율(explained variance ratio)도 유용한 정보 중 하나
- 이 비율은 각 주성분의 축을 따라 잇는 데이터셋의 분산 비율을 나타냄
~~~python
print(pca.explained_variance_ratio_)
# [0.92461872 0.05306648]
~~~
- 이는 데이터셋의 분산의 92.4%가 첫 번째 PC를 따라 놓여 있고, 5.3%가 두 번째 PC를 따라 놓여 있음을 알려줌

### 적절한 차원 수 선택하기
- 축소할 차원 수를 임의로 정하기보다는 충분한 분산이 될 때까지 더해야 할 차원 수를 선택하는 것이 좋음
- 데이터 시각화를 위해 차원을 축소하는 경우 차원을 2개나 3개로 줄이는 것이 일반적임
- 아니면 설명된 분산을 차원 수에 대한 함수로 그려 적절한 변곡점을 찾아 주성분 수를 정함
- 보존하려는 분산의 비율을 `n_components`에 0.0에서 1.0 사이로 설정하는 편이 훨씬 낫다
- 또는 설명된 분산값을 그래프로 그리는 것도 하나의 방법(`cumsum`을 그래프로 그리면 됨)
~~~python
pca = PCA()
pca.fit(X, y)
cumsum = np.cumsum(pca.explained_variance_ratio_)
d = np.argmax(cumsum >= 0.95) + 1
print(f"분산 95% 이상 주성분 수 : {d}")

#- n_components를 0.0 ~ 1.0 사이로 지정하면 자동으로 주성분 수 계산
pca = PCA(n_components=0.95)
X_reduced = pca.fit_transform(X)
print(X_reduced)
~~~

### 압축을 위한 PCA
- 차원을 축소하고 난 후에는 훈련 세트의 크기가 줄어듬
- 예를 들어 MNIST 데이터셋에 분산의 95%를 유지하도록 PCA를 적용해보자
- 각 샘플은 원래 784개 특성이 아니라 150개 정도만 가지고 있음
- 대부분의 분산은 유지되었지만 데이터셋은 원본 크기의 20% 미만이 되었음
- 이는 상당한 압축률이고 이런 크기 축소는 (SVM 같은) 분류 알고리즘의 속도를 크게 높일 수 있음
- 또한 압축된 데이터셋에 PCA 투영의 변환을 반대로 적용하여 784개의 차원으로 되돌릴 수도 있음  
  투영에서 일정량의 정보를 잃어버렸기 때문에 이렇게 해도 원본 데이터셋을 얻을 수는 없음
- 원본 데이터와 재구성된 데이터 사이의 평균 제곱 거리를 <b>재구성 오차(recontruction error)</b> 라고 함
- 다음 코드는 MNIST 데이터셋을 154차원으로 압축하고, `inverse_transform()` 메서드를 이용해 784차원으로 복원
- 주성분의 Transpose 행렬인 V^T 가 `components_` 변수에 저장되어 있으므로, `inverse_transform()` 메서드에서는 압축된 데이터셋에 `components_`를 점곱하고 원본 데이터셋에서 구한 평균을 더함
- X_train의 크기가 (52500, 784)라고 하면 PCA 변환 후 X_reduced의 X_reduced의 크기는 (52500, 154)가 됨
- 주성분의 전치이니 components_의 크기는 (154, 784)임
- X_train의 크기가 (52500, 784)이므로 X_reduced와 components_ 의 점곱 결과는 (52500, 784)가 되어 원본 데이터셋의 차원으로 복원됨
~~~python
#- MNIST 데이터셋을 154차원으로 압축하고, inverse_transform() 메서드를 사용
pca = PCA(n_components = 154)
X_reduced = pca.fit_transform(X_train)
X_recovered = pca.inverse_transform(X_reduced)
~~~

### 랜덤 PCA
- `svd_solver` 매개변수를 "randomized"로 지정하면 사이킷런은 랜덤 PCA라 부르는 확률적 알고리즘을 사용해 처음 d개의 주성분에 대한 근사값을 빠르게 찾음
- 랜덤 PCA는 성분확률적 알고리즘을 사용해 처음 d개의 주에 대한 근사값을 빠르게 찾음
- 이 알고리즘의 계산 복잡도는 O(m x n^2) + O(n^3)이 아닌 O(m x d^2) + O(d^3)임
- 따라서 d가 n보다 많이 작으면 완전 SVD 보다 훨씬 빠름
~~~python
rnd_pca = PCA(n_components=154, svd_solver="randomized")
X_reduced = rnd_pca.fit_transform(X_train)
~~~
- `svd_solver`의 기본값은 "auto"임. m이나 n이 500보다 크고, d가 m이나 n의 80%보다 작으면 사이킷런은 자동으로 랜덤 PCA 알고리즘을 사용
- 만약 강제로 완전한 SVD방식을 사용하려면 `svd_solver = 'full'`로 지정

### 점진적 PCA
- Incremental PCA(IPCA)라고 함
- PCA 구현의 문제는 SVD 알고리즘을 실행하기 위해서 전체 훈련 세트를 메모리에 올려야 한다는 것
- 따라서 점진적 PCA는 훈련 세트를 미니 배치로 나눈 뒤, IPCA 알고리즘에 한 번에 하나씩 주입
- 이런 방식은 훈련 세트가 클 때 유용하고 온라인으로 PCA를 적용 할 수도 있음 
- `IncrementalPCA` 클래스에 주입해서 사용 가능. `partial_fit()`을 미니배치마다 호출해야 함
~~~python
for X_batch in np.array_split(X, n_batches):
    inc_pca.partial_fit(X_batch)
X_reduced = inc_pca.transform(X)
~~~
- 또 다른 방법은 넘파이의 `memmap` 파이썬 클래스를 사용하여 하드 디스크의 이진 파일에 저장된 매우 큰 배열을 메모리에 들어 있는 것처럼 다루는 것
- 이 파이썬 클래스는 필요할 때 데이터를 메모리에 적재함. IncrementalPCA는 특정 순간에 배열의 일부만 사용하기 때문에 메모리 부족 문제를 해결할 수 있음
- 다음 코드처럼 이 방식을 사용하면 일반적인 `fit()` 메서드를 사용할 수 있음
~~~python
X_mm = np.memmap(filename, dtype='float32', mode='readonly', shape=(m, n))
batch_size = m // n_batches
inc_pca = IncrementalPCA(n_components=154, batch_size=batch_size)
inc_pca.fit(X_mm)
~~~
- `IncrementalPCA`의 fit() 메서드는 batch_size 만큼 전체 훈련 데이터를 미니배치로 나누어 `partial_fit()` 메서드를 호출
- batch_size의 기본값은 특성 수의 5배임

### 커널 PCA
- 샘플을 매우 높은 고차원 공간으로 암묵적으로 매핑하여 SVM의 비선형 분류와 회귀를 가능하게 하는 수학적 기법인  
  커널 트릭에 대해서 이야기 함
- 고차원 특성 공간에서의 선형 결정 경계는 원본 공간에서는 복잡한 비선형 결정 경계에 해당하는 것을 배움
- 같은 기법을 PCA에 적용해 차원 축소를 위한 복잡한 비선형 투형을 수행할 수 있음. 이를 <b>커널 PCA</b> 라고 함
- 이 기법은 투영된 후에 샘플의 군집을 유지하거나 꼬인 매니폴드에 가까운 데이터셋을 펼칠 때도 유용
- 다음 코드는 사이킷런의 KernelPCA를 사용해 RBF 커널로 kPCA를 적용
~~~python
from sklearn.decomposition import KernelPCA
rbf_pca = KernelPCA(n_components=2, kernel="rbf", gamma=0.04)
X_reduced = rbf_pca.fit_transform(X)
print(X_reduced)
~~~
- kPCA는 비지도 학습이기 때문에 좋은 커널과 하이퍼파라미터를 선택하기 위한 명확한 성능 측정 기준이 없음  
- 하지만 차원 축소는 종종 지도 학습의 전처리 단계로 활용되므로, 그리드 탐색을 사용하여 주어진 문제에서 성능이 가장 좋은 커널과 하이퍼파라미터를 선택할 수 있음
- 다음 코드는 두 단계의 파이프라인을 만듬  
  먼저 kPCA를 사용해 차원을 2차원으로 축소하고, 분류를 위해 로지스틱 회귀를 적용  
  파이프라인 마지막 단계에서 좋은 분류 정확도를 얻기 위해 GridSearchCV를 사용해 kPCA의 가장 좋은 커널과 gamma 파라미터를 찾음 
- 가장 좋은 커널과 파라미터는 `best_params`에 저장
~~~python
from sklearn.decomposition import KernelPCA
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

clf = Pipeline([
    ("kpca", KernelPCA(n_components=2)),
    ("log_reg", LogisticRegression())
])

param_grid = [{
    "kpca__gamma": np.linspace(0.03, 0.05, 10),
    "kpca__kernel": ["rbf", "sigmoid"]
}]

grid_search = GridSearchCV(clf, param_grid, cv=3)
grid_search.fit(X, y)
print(f"best param: {grid_search.best_params_}")
~~~
- 완전한 비지도학습 방식으로, 가장 낮은 재구성 오차를 만드는 커널과 하이퍼파라미터를 선택하는 방식도 있음
- 하지만 재구성은 선형 PCA만큼 쉽지 않음
- 아래 그림은 스위스 롤의 원본 3D 데이터셋(왼쪽 위)과 RBF 커널의 kPCA를 적용한 2D 데이터셋을 보여줌
- 커널 트릭 덕분에 이 변환은 특성 맵(feature map)을 사용하여 훈련 세트를 무한 차원의 특성 공간에 매핑한 다음, 변환된 데이터셋을 선형 PCA를 사용해 2D로 투영한 것과 수학적으로 동일
![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/dimensionality_reduction_3.png)
- 축소된 공간에 있는 샘플에 대해서 선형 PCA를 역전시키면 재구성된 데이터 포인트는 원본 공간이 아닌 특성 공간에 놓이게 됨
- 이 특성 공간은 무한 차원이기 때문에 재구성된 포인트를 계산할 수 없고 재구성에 따른 실제 에러를 계산할 수 없음
- 다행히 재구성된 포인트에 가깝게 매핑된 원본 공간 포인트를 찾을 수 있고, 이를 <b>재구성 원상(pre-image)</b>이라고 함
- 이런 원상을 얻게 되면 원본 샘플과의 제곱 거리를 측정할 수 있음. 그래서 오차를 최소화하는 커널과 하이퍼파라미터를 선택할 수 있음
- 재구성하는 방법은 투영된 샘플을 학습 데이터로, 원본 샘플을 타깃으로 하는 지도학습 회귀 모델을 구현하는 것
- 사이킷런에서는 다음 코드와 같이 `fit_inverse_transform=True`로 지정하면 이를 자동으로 수행
~~~python
rbf_pca = KernelPCA(n_components=2, kernel='rbf', gamma= 0.433,
                    fit_inverse_transform=True)
X_reduced = rbf_pca.fit_transform(X)
X_preimage = rbf_pca.inverse_transform(X_reduced)
~~~
- `KernelPCA`는 `fit_inverse_transform=False`가 기본값이며, `inverse_transform()` 메서드를 가지고 있지 않음. 이 메서드는 `fit_inverse_transform=True`를 지정했을 때만 생성됨
- 그런다음 재구성 오차(recontruction error)를 계산할 수 있음
~~~python
from sklearn.metrics import mean_squared_error
mean_squared_error(X, X_preimage)
~~~

## LLE(Locally linear embedding)
- 또 다른 강력한 비선형 차원 축소(nonlinear dimensionallity reduction, NLDR) 기술
- 이전 알고리즘처럼 투영에 의존하지 않는 매니폴드 학습
- 간단히 말해 LLE는 먼저 각 훈련 샘플이 가장 가까운 이웃(closest neighbor(c.n.))에 얼마나 선형적으로 연관되어 있는지 측정
- 그런 다음 국부적인 관계가 가장 잘 보존되는 훈련 세트의 저차원 표현을 찾음
- <b>이 방법은 특히 잡음이 너무 많지 않은 경우 꼬인 매니폴드를 펼치는 데 작동</b>
- 다음 코드는 사이킷런의 LocallyLinearEmbedding을 사용해 스위스 롤을 펼침


### LLE 작동방식
- 먼저 알고리즘이 각 훈련 샘플 x(i)에 대해 가장 가까운 k개의 샘플을 찾음(위에서는 10)
- 그런 다음 이 이웃에 대한 선형 함수로 x(i)를 재구성함. 더 구체적으로 말하면 x(i)와 simga(m)(j=1)wi,jx(j)의 거리가 최소가 되는 wi,j를 찾는 것ㄴ
- 여기서 x(j)가 x(i)의 가장 가까운 k개 이웃 중 하나가 아닐 경우에는 wi,j=0이 됨
- 그러므로 LLE의 첫 단계는 아래와 같은 제한이 있는 최적화 문제가 됨
- 아래 W는 가중치 wi,j를 모두 담은 가중치 행렬
- 두 번째 제약은 각 훈련 샘플 x(i)에 대한 가중치를 단순히 정규화하는 것 

## 다른 차원 축소 기법
### 랜덤 투영(random projection)
- 랜덤한 선형 투영을 사용해 데이터를 저차원 공간으로 투영함

### 다차원 스케일링(multidimensional scaling, MDS)
- 샘플 간의 거리를 보존하면서 차원을 축소

### Isomap
- 각 샘플을 가장 가까운 이웃과 연결하는 식으로 그래프를 만듬
- 그런 다음 샘플 간의 지오데식 거리(geodesic distance)를 유지하면서 차원 축소

### t-SNE(t-distributed stochastic neighbor embedding)
- 비슷한 샘플은 가까이, 비슷하지 않는 샘플은 멀리 떨어지도록 하면서 차원을 축소
- 주로 시각화에 많이 사용되며 특히 고차원 공간의 있는 샘플의 군집을 시각화할 때 사용

### 선형판별분석(linear discriminant analysis, LDA)
- 사실 분류 알고리즘임. 훈련 과정에서 클래스 사이를 가장 잘 구분하는 축을 학습
- 이 축은 데이터가 투영되는 초평면을 정의하는 데 사용 가능
- 이 알고리즘의 장점은 투영을 통해 가능한 한 클래스를 멀리 떨어지게 유지시키므로 SVM 분류기 같은 다른 분류 알고리즘을  
  적용하기 전에 차원 축소에 좋음

![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/dimensionality_reduction_1.JPG)
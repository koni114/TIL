# 비지도 학습
- 군집(clustering)
  - 비슷한 샘플을 cluster로 모음. 군집은 데이터 분석, 고객 분류, 추천 시스템, 검색 엔진, 이미지 분할, 준지도 학습, 차원 축소 등에 사용할 수 있는 훌륭한 도구
- 이상치 탐지(outlier detection)
  - '정상' 데이터가 어떻게 보이는지를 학습하고, 비정상 샘플을 감지하는 데 사용됨
  - 예를 들면 제조 라인에서 결함 제품을 감지하거나, 시계열 데이터에서 새로운 트렌드를 찾음
- 밀도 추정(density estimation)
  - 데이터셋 생성 확률 과정(random process)의 PDF(probability density function)을 추정
  - 밀도 추정은 이상치 탐지에 널리 사용됨. 밀도가 매우 낮은 영역에 놓인 샘플이 이상치일 가능성이 높음  . 또한 데이터 분석과 시각화에도 유용함
    
    
## 군집(Clustering)
- 비슷한 샘플을 구별해 하나의 클러스터 또는 비슷한 샘플의 그룹으로 할당하는 작업
- 각 샘플은 하나의 군집에 할당됨
- 군집은 다음과 같은 다양한 애플리케이션에서 사용됨
  - 고객 분류  
    고객을 구매 이력이나 웹사이트 내 행동 등을 기반으로 클러스터로 모을 수 있음  
    이는 고객이 누구인지, 고객이 무엇을 원하는지 이해하는 데 도움이 됨  
    동일한 클러스터 내에 사용하는 좋아하는 컨텐츠를 추천하는 추천 시스템을 만들 수 있음
  - 데이터 분석  
    새로운 데이터셋을 분석할 때 군집 알고리즘을 수행하고 각 클러스터를 따로 분석하면 도움이 됨
  - 차원 축소 기법  
    한 데이터셋에 군집 알고리즘을 사용하면 각 클러스터에 대한 <b>샘플의 친화성(affinity)</b>를 측정할 수 있음  
    각 샘플의 특성 벡터 x는 클러스터 친화성의 벡터로 바꿀 수 있음  
    k개의 클러스터가 있다면, 이 벡터는 k차원이 됨
  - 이상치 탐지  
    모든 클러스터에 친화성이 낮은 샘플은 이상치일 가능성이 높음  
    웹사이트 내 행동을 기반으로 사용자의 클러스터를 만들었다면 초당 웹서버 요청을 비정상적으로 많이 하는 사용자를 감지할 수 있음  
    이상치 탐지는 특히 제조 분야에서 결함을 감지할 때 유용함. 또는 부정거래감지에 활용
  - 준지도 학습
  - 검색 엔진  
    일부 검색 엔진은 제시된 이미지와 비슷한 이미지를 찾아줌  
    이런 시스템을 구축하려면 먼저 데이터베이스에 있는 모든 이미지에 군집 알고리즘을 적용해야함
  - 이미지 분할  
    색을 기반으로 픽셀을 클러스터로 모음  
    그다음 각 픽셀의 색을 해당 클러스터의 평균 색으로 변경함  
    이는 이미지에 있는 색상의 종류를 크게 줄여, 물체의 윤곽을 감지하기 쉬워져 물체 탐지 및 추적 시스템에서 이미지 분할을 많이 활용
- 클러스터의 보편적인 정의는 없음
- 알고리즘이 다르면 다른 종류의 클러스터를 감지함
- 어떤 알고리즘은 센트로이드(centroid)라 부르는 특정 포인트를 중심으로 모인 샘플을 찾음
- 어떤 알고리즘은 샘플이 밀집되어 연속된 영역을 찾음
- 어떤 알고리즘은 계층적으로 클러스터의 클러스터를 찾음

## k-means
- k-평균은 반복 몇번으로 이런 종류의 데이터셋을 빠르고 효율적으로 클러스터로 묶을 수 있는 알고리즘
- 로이드-포지 알고리즘이라고 불리우기도 함
- 각 클러스터의 중심을 찾고, 가장 가까운 클러스터 샘플을 할당함
- 알고리즘이 찾을 클러스터 개수 k를 지정해야 함  
  적절한 k개의 개수를 찾는 것은 쉽지 않음
- 만약 k를 5로 지정하면 군집에서 각 샘플의 레이블은 알고리즘이 샘플에 할당한 클러스터의 인덱스
- `KMeans` 클래스의 인스턴스는 `labels_` 인스턴스 변수에 훈련된 샘플의 레이블을 가지고 있음
- `cluster_centers_`에 알고리즘이 찾은 센트로이드 다섯 개도 확인할 수 있음
- 새로운 샘플에 가장 가까운 센트로이드의 클러스터를 할당할 수 있음  
  <b>센트로이드를 구하면, 지도학습처럼 사용 가능하다는 의미</b>
- k-평균의 결정 경계를 그려보면 <b>보노로이 다이어그램(Voronoi diagram)</b>을 얻을 수 있음  
  보노로이 다이어그램은 평면을 특정 점까지의 가장 가까운 점의 집합으로 분할한 그림 
- 실제 k-평균은 <b>클러스터의 크기가 많이 다르면, 잘 작동하지 않음</b> 
- 샘플을 클러스터에 할당할 때 센트로이드까지 거리를 고려하는 것이 전부이기 때문
- <b>하드 군집(hard clustering)</b>이라는 샘플을 하나의 클러스터에 할당하는 것보다 샘플에 클러스터마다 점수를 부여하는 것이 유용할 수 있음. 이를 <b>소프트 군집(soft clustering)</b>이라고 함
- 이 점수는 샘플과 센트로이드 사이의 거리가 되거나, 반대로 가우시안 방사 기저 함수와 같은 유사도 점수(simularity score)가 될 수 있음
- `KMeans` 클래스의 `transform` 메서드는 샘플과 각 센트로이드 사이의 거리를 반환함
- 이러한 변환은 매우 효율적인 비선형 차원 축소 기법이 될 수 있음
~~~python
from sklearn.datasets import load_iris
X = load_iris().data
y = load_iris().target

from sklearn.cluster import KMeans
k = 5
kmeans = KMeans(n_clusters=5)
y_pred = kmeans.fit_predict(X)

#- KMeans 클래스의 인스턴스는 labels_ 인스턴스 변수에
#- 훈련된 샘플의 레이블을 가지고 있음
print(kmeans.labels_)          #- 훈련 샘플 레이블
print(kmeans.cluster_centers_) #- 이 알고리즘이 찾은 센트로이드

#- 새로운 샘플에 가장 가까운 센트로이드의 클러스터를 할당할 수 있음
import numpy as np
X_new = np.array([[0, 2, 3, 4], [3, 2, 4, 1], [-3, 3, 0, 0], [-3, 2.5, 3, 1]])
kmeans.predict(X_new)

#- KMeans 의 transform 함수는 샘플과 각 센트로이드 사이의 거리를 반환
#- 이러한 변환은 매우 효율적인 비선형 차원 축소 방법이 될 수 있음
kmeans.transform(X)
~~~

### k-means 알고리즘
- 레이블이나 센트로이드가 주어지지 않는다면 센트로이드를 랜덤하게 선정함(예를 들어 무작위로 k개의 샘플을 뽑아 그 위치를 센트로이드로 정함)
- 그리고 샘플에 레이블을 할당하고 센트로이드를 업데이트하는 작업을 센트로이드 변화가 없을 때까지 계속함
- <b>이 알고리즘은 제한된 횟수 안에 수렴하는 것을 보장함(일반적으로 이 횟수는 매우 작음)</b>
- 무한하게 반복되지 않는데, 샘플과 가장 가까운 센트로이드 사이의 평균 제곱 거리가 매 단계마다 작아질 수 밖에 없기 때문
- 이 알고리즘의 계산 복잡도는 일반적으로 샘플 개수 m, 클러스터의 개수 k, 차원 개수 n에 선형적임  
이는 데이터가 군집할 수 있는 구조를 가질 때 그러한데, 그렇지 않으면 최악의 경우 계산 복잡도는 샘플 갯수에 지수적으로 증가. 왠만하면 거의 그럴 일이 없음
- <b>일반적으로 k-means 알고리즘은 가장 빠른 군집 분석 알고리즘 중 하나</b>
- 이 알고리즘이 수렴하는 것을 보장하지만 적절한 솔루션으로 수렴하지 못할 수 있음(즉 지역 최적점으로 수렴할 수 있음)
- <b>이 여부는 센트로이드의 초기화에 달려 있음</b>
- 센트로이드 초기화를 개선하여 이런 위험을 줄일 수 있음

### 센트로이드 초기화 방법
- 예를 들어 또 다른 군집 알고리즘을 먼저 실행하거나 하는 방식으로 센트로이드의 위치를 근사하게 알 수 있다면 초기값 지정 할 수 있음 
- `init` 매개변수에 센트로이드 리스트를 담은 넘파이 배열을 지정하고 `n_init`를 1로 지정할 수 있음
- 다른 방법은 여러 번 수행해서 가장 좋은 솔루션을 선택하는 것
- `n_init` 매개변수로 랜덤 초기화 횟수를 지정함
- <b>최선의 솔루션을 알수 있는 성능 지표가 있는데, 이 값은 샘플과 가장 가까운 센트로이드 사이의 평균 제곱 거리이며 모델의 이너셔라고 부름</b>
- `inertia_` 인스턴스 변수로 모델의 이너셔를 확인 가능
- 따라서 해당 이너셔 값이 가장 작은 모델을 최적 솔루션으로 선택
- k-평균 알고리즘을 향상시킨 k-평균++도 있음
- 이 논문에서 다른 센트로이드와 거리가 먼 센트로이드를 선택하는 똑똑한 초기화 단계를 소개함
- 이 방법은 k-평균 알고리즘이 최적이 아닌 솔루션을 수렴할 가능성을 크게 낮춤
- k-평균++ 초기화 알고리즘은 다음과 같음
  - 데이터셋에서 무작위로 균등하게 하나의 센트로이드 c(1)을 선택
  - D(x^(i))^2 / sum(j = 1)(m)D(x^(j))^2 의 확률로 샘플 x(i)를 새로운 센트로이드 c(i)로 선택
  - D(x^(i))는 샘플 x(i)와 이미 선택된 가장 가까운 센트로이드까지 거리  
    여기서 D(x^(i))는 샘플 x^(i)와 가장 가까운 센트로이드까지의 거리임
  - 이 확률분포는 이미 선택한 센트로이드에서 멀리 떨어진 샘플을 다음 센트로이드까지 선택할 가능성을 높임
  - k개의 센트로이드가 나올 때까지 위의 단계를 반복함
- <b>`Kmeans` 클래스는 기본적으로 k-means++ 초기화 알고리즘을 사용함</b>  
  원래 방식을 사용하고 싶다면, `init` 매개변수를 `random`으로 지정

### K-평균 속도 개선과 미니배치 K-평균
#### k-평균 속도 개선
- 찰스 엘칸의 논문에서 k-평균 알고리즘에 대해 또 다른 중요한 개선을 제안했음
- 불필요한 거리 계산을 많이 피함으로서 알고리즘의 속도를 상당히 높일 수 있음
- 이를 위해 삼각 부등식을 사용함(AC <= BC + AB, 즉 두 점 사이의 직선은 가장 짧은 거리가 됨)
- 샘플과 센트로이드 사이의 상한선과 하한선을 유지함
- 이 알고리즘은 KMeans에서 기본으로 사용함

#### 미니배치 k-평균
- 데이비드 스컬리 논문에서 k-평균 알고리즘의 또 다른 중요한 변종이 제시되었음
- 전체 데이터셋을 사용하지 않고 이 알고리즘은 각 반복마다 미니배치를 사용해 센트로이드를 조금씩 이동시킴
- <b>일반적으로 알고리즘의 속도를 3배에서 4배 정도로 높임</b>
- 또한 메모리에 들어가지 않는 대량의 데이터셋에 군집 알고리즘을 적용할 수 있음
- 사이킷런은 `MiniBatchKMeans` 클래스에 해당 알고리즘을 구현함  
~~~python
#- mini-batch kmeans
from sklearn.cluster import MiniBatchKMeans
minibatch_kmeans = MiniBatchKMeans(n_clusters=5)
minibatch_kmeans.fit(X)
~~~
- 데이터셋이 메모리에 들어가지 않으면 가장 간단한 방법은 numpy의 `memmap` 클래스를 사용하는 것
- 또는 `MiniBatchMeans` 클래스의 `partial_fit()` 메서드를 한 번에 하나의 미니배치를 전달할 수 있음
- 미니배치 k-평균 알고리즘이 기존 k-평균 알고리즘보다 속도는 훨씬 빠르지만, 이너셔 자체는 조금 더 나쁨 특히 클러스터의 개수가 증가할 때 그러함


![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/kmeans_1.JPG)

- 위의 그림의 왼쪽 그래프를 보면 k가 증가함에 따라 두 곡선의 차이는 일정하게 유지되지만  
  이너셔의 값이 감소하므로 이 차이가 차지하는 비율은 점점 커짐
- 오른쪽 그래프에서 미니배치 k-평균이 일반 k-평균보다 훨씬 빠른 것을 확인 가능

### 최적의 클러스터 개수 찾기
- k를 너무 작거나 크게 지정하면 상당히 나쁜 모델이 만들어짐
- 가장 작은 이너셔를 가진 모델을 선택하면 안됨. 반드시 이너셔는 k가 증가함에 따라 작아지기 때문
- 방법은 이너셔 그래프를 클러스터 k의 함수로 그렸을 때 그래프에서 엘보(elow, 기울기가 확 완만해지는 지점)을 찾으면 됨
- 이보다 좋은 방법은 <b>실루엣 점수(silhouette score)</b>임(계산 시간이 오래걸림)
- 이 값은 모든 샘플에 대한 실루엣 계수의 평균
- 샘플의 실루엣 계수는 (b - a) / max(a, b)로 계산함
  - a : 동일한 클러스터에 있는 다른 샘플까지 평균 거리(클러스터 내부 평균 거리)
  - b : 다른 가장 가까운 클러스터까지 평균 거리(가장 가까운 클러스터의 샘플까지 평균 거리)
- 샘플과 가장 가까운 클러스터는 자신이 속한 클러스터는 제외
- 실루엣 계수는 -1 부터 1까지 바뀔 수 있음 
  - +1에 가까우면 자신의 클러스터 안에 잘 속해있고, 다른 클러스터와는 멀리 있다는 의미
  - -1에 가까우면 이 샘플이 잘못된 클러스터에 할당되었다는 의미
- 실루엣 점수를 계산하려면, `silhouette_score()` 함수를 사용. 데이터셋에 있는 모든 샘플과 할당된 레이블을 전달

#### 실루엣 계수
- 모든 샘플의 실루엣 계수를 할당된 클러스터와 계숫값으로 정렬하여 그리면 더 많은 정보가 있는 그래프를 얻을 수 있음. 이를 <b>실루엣 다이어그램</b>이라고 함 
- 클러스터마다 칼 모양의 그래프가 그려짐
- 이 그래프의 높이는 샘플의 개수를 의미하고, x축은 실루엣 계수를 나타냄(즉 클러스터 별 그래프의 면적이 넢을수록 좋음)
- 수직 파선은 각 클러스터의 개수에 해당하는 실루엣 점수를 나타냄
- 한 클러스터의 샘플 대부분이 이 점수보다 낮은 계수를 가지만 다른 클러스터와 너무 가깝다는 것을 의미하므로, 나쁜 클러스터임
- 좋은 k를 고르려면, 수직 파선보다 대부분 넘어가면서 실루엣 계수 값이 고르게 분포되어 있는 k를 고르는 것이 최적!

![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/kmeans_2.JPG)

### k-means의 한계
- k-means는 장점이 많은데, 속도가 빠르고 확장이 용이함
- 하지만 완벽한 것은 아닌데, 최적이 아닌 솔루션을 파하려면 알고리즘을 여러 번 실행 해야함
- 또한 클러스터 개수를 지정해야 함
- k-평균은 <b>클러스터의 크기나 밀집도가 서로 다르거나, 구형이 아닐 경우 잘 작동하지 않음</b>
- 예를 들어 타원형 모양으로 밀집도를 가지는 것들은 잘 구분해내지 못함
- <b>타원형 클러스터에는 가우시안 혼합 모델이 잘 작동함</b>
- k-평균을 실행하기 전에 스케일을 조정하는 것이 중요함. 완전히 보장되지는 않지만 스케일을 맞추면 좀 더 구형에 가까워짐

## 군집을 사용한 이미지 분할
- <b>이미지 분할(image segmentation)</b>은 이미지를 세그먼트 여러 개로 분할하는 작업
- <b>시멘틱 분할(semantic segmentation)</b>에서는 동일한 종류의 물체에 속한 모든 픽셀은 같은 세그먼트에 할당됨
- 예를 들어 자율 주행 자동차의 비전 시스템에서 보행자 이미지를 구성하는 모든 픽셀은 '보행자' 세그먼트에 할당될 것임
- 이 경우 각 보행자는 다른 세그먼트가 될 수 있음 (이런 분할을 인스턴스 분할이라고 함)
- 시맨틱 또는 인스턴스 분할에서 최고 수준의 성능을 내려면 합성곱 신경망을 사용한 복잡한 모델을 사용해야 함
- 여기서는 간단하게 색상 분할(colo segmentation)을 수행해보자  
  동일한 색상을 가진 픽셀을 같은 세그먼트에 할당할 것임
- 인공위성 사진을 분석하여 한 지역의 전체 산림 면적이 얼마나 되는지 측정하려면 색상 분할로 충분함
- RGB간의 색상의 긴 리스트로 변환한 다음, k-평균 알고리즘을 클러스터로 모음
- 예를 들어, 모든 초록색을 하나의 컬러 클러스터로 만들 수 있음
- 각 색상에 대해 그 픽셀의 컬러 클러스터의 평균을 찾음  
  예를 들어 초록 클러스터의 평균 색이 밝은 초록이라고 가정
- 마지막으로 이 긴 색상의 리스트를 원본 이미지가 동일한 크기로 바꿈
~~~python
from matplotlib.image import imread
import os
image = imread(os.path.join("images", "unsupervised_learning", "ladybug.png"))
print(f"image.shape : {image.shape}")

#- imread : 0.0 ~ 1.0 사이
#- imageio.imread : 0 ~ 255 사이
#- 어떤 이미지는 더 적은 채널을 가지고(흑백사진), 어떤 이미지는 더 많은 채널을 가짐(투명도를 위한 알파채널 추가)
#- 위성 이미지는 종종 여러 전자기파에 대한 채널을 포함함(ex) 적외선)

#- 다음 코드는 RGB 색상의 긴 리스트로 변환한 다음 k-means 알고리즘을 사용해 클러스터로 모음
#- 각 색상에 대해 그 픽셀의 컬러 클러스터의 평균 컬러를 찾음. 예를 들어 모든 초록색은 모두 밝은 초록색으로 바뀔 수 있음
#- 마지막으로 shape 기존의 image shape과 동일하게 변경
X = image.reshape(-1, 3)
kmeans = KMeans(n_clusters=8).fit(X)
segmented_img = kmeans.cluster_centers_[kmeans.labels_] #- 색상 클러스터링
segmented_img = segmented_img.reshape(image.shape)

#- 클러스터 개수를 조정하면 색상이 변경되는데, 무당벌레의 색상은 전체 이미지에서 조금 들어가있기 때문에
#- 다른 색과 합쳐지는 경향이 보임!
~~~
![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/clustering_1.png)

## 군집을 사용한 전처리
- 군집은 지도 학습 알고리즘을 사용하기 전 전처리 단계로 활용 가능
- 차원 축소에 군집을 활용하는 예를 위해서 숫자 데이터셋을 활용해보자
- 이 데이터셋은 MNIST와 비슷한 데이터셋으로 0에서 9까지의 숫자를 나타내는 8x8 크기 흑백 이미지 1,797개를 담고 있음. 
- 특히 지도 학습 알고리즘을 적용하기 전에 전처리 단계로 이용할 수 있음
- 예를 들어 8x8 의 차원을 가진 숫자 이미지 데이터를 로지스틱 회귀로 분류한다고 할 때,  
  cluster 개수가 50인 kmeans를 적용해 centroid로 변경하고, 이 값을 기반으로 로지스틱 회귀를 적용하면 더 개선될 수 있음
- 즉, 차원 수는 줄이면서 성능은 증가할 수 있는데, 그 이유는 로지스틱 회귀 같은 경우는 선형임을 가정한 모형이기 때문에 성능도 개선되면서 차원을 줄일 수 있음! 
- gridSearchCV를 이용해 최적의 클러스터 개수를 찾아볼 수 있음
- 다음은 군집을 사용한 전처리 전체 코드
~~~python
from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ("kmeans", KMeans(n_clusters=50)),
    ('log_reg', LogisticRegression(max_iter=100)),
])
pipeline.fit(X_train, y_train)
pipeline.score(X_test, y_test)

from sklearn.model_selection import GridSearchCV
param_grid = dict(kmeans__n_clusters=range(75, 100))
grid_clf = GridSearchCV(pipeline, param_grid, cv=3, verbose=2)
grid_clf.fit(X_train, y_train)

print(f"best params : {grid_clf.best_params_}")
grid_clf.score(X_test, y_test)
~~~

## 군집을 사용한 준지도 학습
- 군집을 사용하는 또 다른 사례는 준지도 학습
- 레이블이 없는 데이터가 많고 레이블이 있는 데이터는 적을 때 사용
- 숫자 데이터셋에서 레이블된 50개 샘플에 로지스틱 회귀 모델 훈련해보자
- 테스트 세트에서 모델의 성능은 매우 낮음  
  전체 데이터셋을 사용했을 때보다 낮은 정확도가 나온 것이 당연함

### 군집 분석을 이용한 개선 방법
- 먼저 훈련 세트를 50개의 클러스터로 모음
- 그다음 각 클러스터에서 센트로이드에 가장 가까운 이미지를 찾음  
  이런 이미지를 <b>대표 이미지(representative image)</b>라고 함
- 이미지를 보고 수동으로 레이블을 할당함
- 이제 레이블된 50개 샘플로 이루어진 데이터셋이 준비되었으니 이 데이터를 가지고 다시 로지스틱 회귀를 수행하면, 훨씬 더 성능이 좋아지는 것을 확인할 수 있음
- 레이블을 수작업으로 처리하게 되면 어려우므로, 무작위 샘플 대신 대표 샘플에 레이블을 할당하는 것이 좋은 방법
- 여기서 한단계 더 나아갈 수 있는데, 레이블을 동일한 클러스터에 있는 모든 샘플로 전파하면 어떨까?  
이를 <b>레이블전파(label propagation)</b>라고 함
~~~python
########################
## 군집을 사용한 준지도 학습 ##
########################
n_labels = 50
log_reg = LogisticRegression()
log_reg.fit(X_train[:n_labels], y_train[:n_labels])
log_reg.score(X_test, y_test) #- 0.86

#- 정확도가 훨씬 낮음
#- 이를 개선하기 위해 먼저 훈련 세트를 50개의 클러스터로 나눔
#- 그다음 각 클러스터에서 센트로이드에 가장 가까운 이미지를 찾음.
#- 이런 이미지를 대표 이미지(representative image)라고 함
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=50)
X_digits_dist = kmeans.fit_transform(X_train)
representative_digit_idx = np.argmin(X_digits_dist, axis=0)
X_representative_digits = X_train[representative_digit_idx]

plt.figure(figsize=(8, 2))
for index, X_representative_digit in enumerate(X_representative_digits):
    plt.subplot(n_labels // 10, 10, index + 1) #- 5x10 의 50개의 칸, index+1 위치에 이미지 삽입한다는 의미
    plt.imshow(X_representative_digit.reshape(8, 8), cmap="binary", interpolation="bilinear")
    plt.axis('off')

#- 이미지를 보고 수동으로 y 할당
y_representative_digits = np.array([6, 8, 4, 3, 1, 0, 1, 2, 2, 5, 4, 6, 3, 1, 7, 9, 4, 7, 8, 6,
                                    4, 1, 9, 2, 0, 2, 7, 9, 5, 3, 7, 5, 1, 6, 8, 2, 9, 7, 5, 2,
                                    0, 8, 0, 4, 1, 0, 8, 6, 1, 9])

#- 레이블된 50개 샘플로 이루어진 데이터셋이 준비됨
#- 하지만 무작위로 고른 샘플은 아니고 이미지들은 각 클러스터를 대표하는 이미지
#- 성능이 조금이라도 높은지 확인해보자
log_reg = LogisticRegression()
log_reg.fit(X_representative_digits, y_representative_digits)
print(log_reg.score(X_test, y_test))

#- 50개의 모델을 훈련했을 뿐인데, 83.3% -> 92.2%로 확 올라감
#- 샘플에 레이블을 부여하는 것은 많이 어렵기 때문에 대표 샘플에 레이블을 할당하고 label propagation 을 해보자

#- y_train_propagated : 앞선 수동 레이블을 기반으로, 같은 클러스터 데이터는 수동 레이블을 할당
y_train_propagated = np.empty(len(X_train), dtype=np.int32)
for i in range(n_labels):
    y_train_propagated[kmeans.labels_== i] = y_representative_digits[i]

#- LogisticRegression 재학습
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train_propagated)
log_reg.score(X_test, y_test)

#- 92% 정도의 정확도를 나타내는데, 이는 놀라울 정도는 아님.
#- 그 이유는 대표 샘플의 레이블을 동일한 클러스터의 모든 데이터에 전파했기 때문
#- 클러스터 경계에 가깝게 위치한 샘플이 포함되어 있고, 아마 잘못 레이블이 부여되었을 것임
#- 센트로이드와 가까운 샘플의 20%만 레이블을 전파해보고 어떻게 되는지 확인해보자

percentile_closest = 20
X_cluster_dist = X_digits_dist[np.arange(len(X_train)), kmeans.labels_]

for i in range(n_labels):
    in_cluster = (kmeans.labels_ == i)
    cluster_dist = X_cluster_dist[in_cluster]
    cutoff_distance = np.percentile(cluster_dist, percentile_closest) #- 각 클러스터별 20% 분위수 계산
    above_cutoff = (X_cluster_dist > cutoff_distance)
    X_cluster_dist[in_cluster & above_cutoff] = -1

partially_propagated = (X_cluster_dist != -1)
X_train_partially_propagated = X_train[partially_propagated]
y_train_partially_propagated = y_train_propagated[partially_propagated]

print(f"X_train_partially_propagated.shape : {X_train_partially_propagated.shape}")
print(f"y_train_partially_propagated.shape : {y_train_partially_propagated.shape}")

log_reg = LogisticRegression()
log_reg.fit(X_train_partially_propagated, y_train_partially_propagated)
log_reg.score(X_test, y_test)

#- 실제 label propagation 이 성능이 좋음
np.mean(y_train_partially_propagated == y_train[partially_propagated]
~~~

### 능동 학습(active learning)
- 모델과 훈련 세트를 지속적으로 향상하기 위해 다음 단계로 <b>능동 학습(active learning)</b>을 몇 번 반복할 수 있음
- 이 방법은 전문가가 학습 알고리즘과 상호작용하여 알고리즘이 요청할 때 특정 샘플의 레이블을 제공
- active learning에는 여러 다른 전략이 많음
- 하지만 가장 널리 사용되는 것 중에 하나는 불확실성 샘플링(uncertainty sampling)임
  - 지금까지 수집한 레이블된 샘플에서 모델을 훈련함. 이 모델을 사용해 레이블되지 않은 모든 샘플에 대한 예측을 만듬
  - 모델이 가장 불확실하게 예측한 샘플을 전문가에게 보내 레이블을 붙임
  - 레이블을 부여하는 노력만큼의 성능이 향상되지 않을 때까지 반복

## DBSCAN
- 이 알고리즘은 밀집된 연속된 지역을 클러스터로 정의. 작동방식은 다음과 같음
  - 알고리즘이 각 샘플에서 작은 거리인 입실론 내에 샘플이 몇 개 놓여있는지 셈  
    이 지역을 샘플의 입실론-이웃이라고 부름
  - 자기 자신을 포함해 입실론-이웃 내에 적어도 min_samples개 샘플이 있다면 이를 핵심 샘플로 간주
  - 핵심 샘플의 이웃에 있는 모든 샘플은 동일한 클러스터에 속함  
    이웃에는 다른 핵심 샘플이 포함될 수 있음. 핵심 샘플의 이웃은 계속해서 하나의 클러스터를 형성
  - 핵심 샘플이 아니고 이웃도 아닌 샘플은 이상치로 판단
- 이 알고리즘은 <b>모든 클러스터가 충분히 밀집되어 있고 밀집되지 않은 지역과 잘 구분될 때 좋은 성능을 냄</b>
- `sklearn.cluster` 의 `DBSCAN` class를 사용. `labels_`가 -1인 것들은 이상치로 간주하는 것들 
- 핵심 샘플의 인덱스는 인스턴스 변수 `core_sample_indices_`에서 확인 가능  
  핵심 샘플 자체는 `components_`에 저장되어 있음
- 이 알고리즘은 새로운 샘플에 대해 클러스터를 예측할 수 없음  
  즉 `predict` 메서드를 제공하지 않고 `fit_predict` 메서드만 제공  
  DBSCAN의 작동 방식을 생각하면 새로운 데이터에 대해 예측할 수 없음을 쉽게 이해할 수 있음  
  DBSCAN이 샘플에 클러스터 레이블을 할당하는 방식이 아님  
  가능한 방법은 기존 훈련 세트에서 테스트 샘플을 추가하여 다시 DBSCAN을 훈련하는 것
- 이런 구현 결정은 다른 알고리즘이 이런 작업을 좀 더 잘 수행할 수 있기 때문
- 따라서 사용자가 필요한 예측기를 선택하여 핵심 샘플만 학습하여 centroid를 계산하거나,  
  DBSCAN 결과의 전체 샘플 label를 학습할 수 있음(예를 들어 KNN으로 학습함.) 
- 간단히 말해 DBSCAN은 매우 간단하지만 강력한 알고리즘
- 클러스터의 모양과 개수에 상관없이 감지할 수 있는 능력이 있음
- 이상치에 안정적이고 하이퍼파라미터가 두 개 뿐(eps, min_sample)
- 하지만 <b>클러스터 간의 밀집도가 크게 다르면 모든 클러스터를 올바르게 잡아내는 것이 불가능함</b>
- 계산 복잡도는 대략 O(mlog m), 샘플 개수에 대해 거의 선형적으로 증가  
  하지만 사이킷런의 구현은 eps가 커지면 O(m^2) 만큼 메모리가 필요
~~~python
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons

X, y = make_moons(n_samples=1000, noise=0.05)
dbscan = DBSCAN(eps=0.05, min_samples=5)
dbscan.fit(X)

#- 모든 샘플의 레이블은 _labels 에 저장
print(dbscan.labels_) #- -1인 것들은 샘플의 이상치로 판단했다는 것
print(np.unique(dbscan.labels_)) #- 총 9개의 cluster 생성

#- core instance 확인
#- core_sample_indices_ --> core instance의 index
#- components_          --> core instance value
print(f"core instance 개수 : {len(dbscan.core_sample_indices_)}")
print(f"core instance : {dbscan.components_}")

#- 클러스터를 7개 만들었고, 많은 샘플을 이상치로 판단하였으므로,
#- eps 를 0.2로 늘리면 완벽한 군집을 얻을 수 있음

#- DBSCAN 은 predict 함수를 제공하지 않고, predict_fit 함수만 제공
#- 다시 말해 이 알고리즘은 새로운 데이터셋이 들어왔을 때 클러스터를 예측할 수 없음
#- 따라서 사용자가 필요한 예측기를 선택해야 함 --> 분류 모델을 학습해야 한다는 의미
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=50)
knn.fit(dbscan.components_, dbscan.labels_[dbscan.core_sample_indices_])

X_new = np.array([[-0.5, 0], [0, 0.5], [1, -0.1], [2, 1]])
knn.predict(X_new)
knn.predict_proba(X_new)

#- 이 분류기를 핵심 샘플만 학습할수도 있고, 모든 샘플에 대해서 학습할 수도 있음
#- 또는 이상치를 제외할 수도 있음. 선택은 최종 작업의 성능에 따라 결정됨

#- 훈련 세트에는 이상치가 없기 때문에 클러스터가 멀리 떨어져 있어도 분류기는 항상 클러스터로 분류함
#- 최대 거리를 사용하면 두 클러스터에서 멀리 떨어진 샘플을 이상치로 간단히 분류할 수 있음
#- KNeighborsClassifier의 kneighbors() 메서드 사용
#- 이 메서드에 샘플을 전달하면 훈련 세트에서 가장 가까운 k개 이웃의 거리와 인덱스를 반환

y_dist, y_pred_idx = knn.kneighbors(X_new, n_neighbors=1)
y_pred = dbscan.labels_[dbscan.core_sample_indices_][y_pred_idx]
y_pred[y_dist > 0.2] = -1
y_pred.ravel()
~~~

## 다른 군집 알고리즘
### 병합 군집(agglomerative clustering)
- 클러스터 계층을 밑바닥부터 위로 쌓아 구성함
- 물 위를 떠다니는 작은 물방울을 생각해보자. 물방울이 점차 불어 나중에는 하나의 커다란 방울이 됨
- 비슷하게 반복마다 병합 군집은 인접한 클러스터 쌍을 연결  
    (처음에는 샘플 하나에서 시작)
- 병합된 클러스터 쌍을 트리로 모두 그리면 클러스터의 이진 트리를 얻을 수 있음

### BIRCH(balanced interative reducing and clustering using hieracrchies)
- 대규모 데이터셋을 위해 고안됨
- 특성 개수가 너무 많지 않다면(20개 이하) 배치 k-평균보다 빠르고 비슷한 결과를 만듬 
- 훈련 과정에서 새로운 샘플을 클러스터에 빠르게 할당할 수 있는 정보를 담은 트리 구조를 만듬
- 이 트리에 모든 샘플을 저장하지 않음
- 제한된 메모리를 사용해 대용량 데이터셋을 다를 수 있음

### 평균-이동
- 이 알고리즘은 먼저 각 샘플을 중심으로 하는 원을 그림
- 그다음 원마다 안에 포함된 모든 샘플의 평균을 구함
- 그리고 원의 중심을 평균점으로 이동시킴
- 모든 원이 움직이지 않을때까지 이동-평균을 계속 함
- 평균-이동은 지역의 최대 밀도를 찾을 때까지 높은 쪽으로 원을 이동시킴
- 동일한 지역에 안착한 원에 있는 모든 샘플은 동일한 클러스터가 됨
- 평균-이동은 DBSCAN과 유사한 특징이 있음
- 모양이나 개수의 상관없이 클러스터를 찾을 수 있음
- 하이퍼파라미터도 매우 적음(bandwidth라고 부르는 원 반경 딱 하나)
- DBSCAN과는 달리 평균-이동은 클러스터 내부 밀집도가 불균형할 때 여러 개로 나누는 경향이 있음
- 아쉽지만 계산 복잡도는 O(m^2)임

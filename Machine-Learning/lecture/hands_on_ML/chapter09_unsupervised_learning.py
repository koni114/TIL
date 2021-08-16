IMAGES_PATH = "./images/unsupervised_learning"
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)

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
kmeans.transform(X)

## 센트로이드 초기화 방법
#- 센트로이드를 근사하게 알 수 있다면 init 매개변수에 센트로이드 리스트를 담은
#- 넘파이 배열을 지정하고 n_init = 1로 지정
good_init = np.array([[-3, 3], [-3, 2], [-3, 1], [-1, 2], [0, 2]])
kmeans = KMeans(n_clusters=5, init=good_init, n_init=10)

#- Kmeans 모델의 이너셔 확인
kmeans = KMeans(n_clusters=5)
kmeans.fit(X)
print(kmeans.inertia_)

#- mini-batch kmeans
from sklearn.cluster import MiniBatchKMeans
minibatch_kmeans = MiniBatchKMeans(n_clusters=5)
minibatch_kmeans.fit(X)

#- 실루엣 점수 계산.
from sklearn.metrics import silhouette_score
silhouette_score(X, kmeans.labels_)

###########################################
## 군집을 이용한 색상 분할(color segmentation) ##
###########################################
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

####################
## 군집을 사용한 전처리 ##
####################
from sklearn.datasets import load_digits
X_digits, y_digits = load_digits(return_X_y=True)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_digits, y_digits)

from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X_train, y_train)
round(log_reg.score(X_test, y_test), 4)

#- cluster k-means 를 활용하여 전처리
#- 파이프라인을 만들어 훈련 세트를 50개의 클러스터로 모음
#- 이미지 50개 클러스터까지 거리로 바꿈
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
np.mean(y_train_partially_propagated == y_train[partially_propagated])

############
## DBSCAN ##
############
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

#########
## GMM ##
#########
from sklearn.mixture import GaussianMixture
gm = GaussianMixture(n_components=3, n_init=10)
gm.fit(X)

#- 이 알고리즘이 추정한 파라미터를 확인해보자
#- 특성이 두개 이므로, 평균이 특성마다 하나씩 반환되었고, 공분산 행렬의 크기는 2x2
print(gm.weights_)      #- phi
print(gm.means_)        #- means
print(gm.covariances_)  #- covariance

#- 이 데이터를 생성하기 위해 사용한 가중치는 0.2, 0.4, 0.4임
#- 평균과 분산 행렬도 이 알고리즘이 찾은 것과 매우 비슷함.

#- 알고리즘이 수렴했는지 여부와 반복횟수 확인 가능
print(gm.converged_)
print(gm.n_iter_)

#- 새로운 데이터 투입시 값 예측
gm.predict(X)
gm.predict_proba(X)

#- 가우시안 모델은 generative model 이므로, 이 모델에서 새로운 샘플을 만들 수 있음
X_new, y_new = gm.sample(6)
print(X_new)
print(y_new)

gm_score_samples = gm.score_samples(X)

#- 4% 백분위수를 밀도 임곗값으로 사용하여 이상치를 구분
import numpy as np
densities = gm.score_samples(X)
density_threshold = np.percentile(densities, 4)
anomalies = X[densities < density_threshold]

#- bic(), aic() 사용하여 AIC, BIC를 계산
gm.bic(X)
gm.aic(X)
# randomForest
## randomForest 기법 설명
- 트리 기반의 대표적인 앙상블 모형
- 랜덤포레스트는 같은 데이터에 여러개의 의사결정모형을 생성하여 학습 성능을 높이는 앙상블 기법의 모형
- 동일한 데이터로부터 복원 추출(부트스트랩 샘플링)을 통해 n개 이상의 학습 데이터를 편성하고 각각의 데이터마다 의사결정모형을 생성해 결과를 취합하는 방식
- 여기서 각각의 나무들은 일부 변수만을 취해 학습하게 됨
- 개별 트리들이 데이터를 바라보는 관점을 다르게해 다양성을 높이고자 하는 시도
- <b>로테이션 포레스트</b>는 데이터에 PCA를 적용해 데이터 축을 회전한 후 학습한다는 점만 제외하고 나머지는 동일함
- `max_samples`를 훈련세트의 크기로 지정
- `BaggingClassifier`에 `DecisionTreeClassifier`를 넣어 만들 수도 있고, `RandomForestClassifier`를 사용 가능
- `RandomForestClassifier`는 몇 가지 예외가 있지만 DecisionTree Classifier의 매개변수와 앙상블 자체를 제어하는 데 필요한  
  `BaggingClassifier`의 매개변수를 모두 가지고 있음
- RF는 트리의 노드를 분할할 때 전체 특성 중에서 최선의 특성을 찾는 대신 무작위로 선택한 특성 후보 중에서 최적의 특성을 찾는 식으로 무작위성을 더 주입
- 이는 결국 트리를 더욱 다양하게 만들고, 편향을 손해보는 대신 분산을 낮추어 전체적으로 더 훌륭한 모델을 만들어냄
~~~python
from sklearn.ensemble import RandomForestClassifier
rnd_clf = RandomForestClassifier(n_estimators=500, max_leaf_nodes=16, n_jobs=-1)
rnd_clf.fit(X_train, y_train)
y_pred_rf = rnd_clf.predict(X_test)

#- baggingClassifier를 활용한 randomForest
from sklearn.ensemble import BaggingClassifier
BaggingClassifier(
    DecisionTreeClassifier(max_features="auto", max_leaf_nodes=16),
    n_estimators=500,
    max_samples=1.0,
    bootstrap=True,
    n_jobs=-1
)
~~~

## extra-tree
- 랜덤 포레스트는 트리를 더욱 무작위하게 만들기 위해 후보 특성을 사용해 무작위로 분할한 다음 그중에서 최상의 분할을 선택
- 이와 같이 극단적으로 무작위한 트리의 랜덤 포레스트를 <b>익스트림 랜덤 트리(extreme randomized trees)</b> 앙상블 이라고 함
- 편향이 늘어나지만 분산을 낮추는 효과를 가져옴
- 모든 노드에서 특성마다 가장 최적의 임곗값을 찾는 것이 가장 오래 걸리는 일이므로, 익스트라 트리는 성능이 훨씬 빠름
- `ExtraTreesClassifier` 사용, 사용법은 `RandomForestClassifier` 와 같음
- randomForestClassifier가 ExtraTreesClassifier 보다 좋을지 나쁠지는 예단하기 어려움  
  일반적으로 둘 다 시도해보고 교차 검증으로 비교해보는 것이 유일한 방법
- 엑스트라 트리의 무작위 분할을 단일 결정 트리에 적용한 모델은 `ExtraTreeClassifier`와 `ExtraTreeRegressor`임

## 특성 중요도
- 랜덤 포레스트는 특성의 상대적 중요도를 측정하기 쉬움  
- 결정트리기반의 모형들은 모두 특성 중요도를 제공하는데, `DecisionTreeClassifier`의 특성 중요도는 일부 특성을 모두 배제시키지만,  
  `randomForestClassifier`는 모든 특성에 대해 평가할 기회를 가짐
- <b>사이킷런은 어떤 특성을 사용한 노드가 평균적으로 불순도를 얼마나 감소시키는지 확인하여 특성의 중요도를 측정</b>  
  더 정확히 말하자면 가중치 평균이며 각 노드의 가중치는 연관된 훈련 샘플 수와 같음
- 사이킷런은 훈련이 끝난 뒤 특성마다 자동으로 이 점수를 계산하고 중요도의 전체 합이 1이 되도록 결괏값을 정규화함  
  `feature_importances_` 변수에 저장되어 있음
- 결정 트리의 중요도는 노드에 사용된 특성별로 <b>(현재 노드의 샘플 비율 x 불순도) - (왼쪽 자식 노드의 샘플 비율 x 불순도) - (오른쪽 자식 노드의 샘플 비율 x 불순도) 로 계산하여 더하고</b>  
  특성 중요도의 합이 1이 되도록 전체 합으로 나누어 정규화
- 여기서 샘플 비율은 트리 전체 샘플 수에 대한 비율. 랜덤 포레스트 특성 중요도는 각 결정 트리의 특성 중요도를 모두 계산하여 더한 후 트리 수로 나눈 것
~~~python 
from sklearn.datasets import load_iris
iris = load_iris()
rnd_clf = RandomForestClassifier(n_estimators=500, n_jobs=-1)
rnd_clf.fit(iris['data'], iris['target'])
for name, score in zip(iris['feature_names'], rnd_clf.feature_importances_):
    print(name, score

# sepal length (cm) 0.0934308966587885
# sepal width (cm) 0.024394066806035508
# petal length (cm) 0.4254620443696972
# petal width (cm) 0.4567129921654788
~~~

## R 기반 구현
- R에서 의사결정나무를 수행하는 패키지는 `rpart`임
- 의사결정나무는 범주(classification)을 예측할 경우 범주형, 연속형 값을 맞추는 회귀(Regression)모두 가능함
- 분류를 하고 싶다면, 아래 예제에서 `type = 'class'`를, 회귀를 하고 싶다면 `type = anova`를 지정하면 됨
- 이렇게 명시적으로 적어주지 않아도 Y 값의 타입이 범주형이면 분류를, 연속형이면 예측을 수행
~~~r
library(rpart)
Fit1 <- rpart(fomula, data, type=“anova”) # regression
Fit2 <- rpart(fomula, data, type=“class”) # classification
~~~
- 랜덤포레스트와 관련된 패키지명은 말 그대로 `randomForest`임
- rpart와 마찬가지로 Y의 자료형이 factor이면 분류, numeric이면 자동으로 분류와 회귀를 수행
- `mtry`  : 샘플링 할 시 랜덤으로 선택하는 독립 변수의 개수
- `ntree` : 앙상블을 수행할 의사결정나무의 개수
~~~r
library(randomForest)
Fit <- randomForest(formula, data, ntree, mtry, ...)
~~~

## 용어 정리
- bagging
  - 같은 알고리즘 모형에 훈련 데이터셋을 무작위로 구성(복원)하여 앙상블 하는 것
- pasting
  - 같은 알고리즘 모형에 훈련 데이터셋을 무작위로 구성(비복원)하여 앙상블 하는 것
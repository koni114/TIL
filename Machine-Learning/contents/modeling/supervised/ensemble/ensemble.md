# 앙상블(ensemble)
- 배깅, 부스팅, 스태킹 등 인기있는 앙상블 방법을 설명해 보겠음

## 투표 기반 분류기
- 다수결 투표로 정해지는 분류기를 hard voting 분류기라고 함
- 분류기가 약한 학습기(weak learner) 일지라도 충분하게 많고 다양하다면 앙상블은 강한 학습기(strong learner)가 될 수 있음  
  이 것이 어떻게 가능할까? --> 큰 수의 법칙(law of large numbers)로 설명 가능
- 즉, 51%의 정확도를 가진 1000개의 분류기로 앙상블 모델을 구축한다고 가정했을 때,   
  가장 많은 클래스를 예측으로 삼는다면 75%의 정확도를 기대할 수 있음
- 하지만 이러한 가정은 모든 분류기가 완벽하게 독립적이고 오차에 상관관계가 없어야 가능
- but 앙상블 모형은 같은 데이터로 훈련시키기 때문에 이런 가정이 맞지 않음
- 앙상블 방법은 예측기가 가능한 한 서로 독립적일 때 최고의 성능을 발휘함. 즉 다양한 분류기를 얻는 한 가지 방법은  
  각기 다른 알고리즘으로 학습시키는 것. 이렇게 하면 매우 다른 종류의 오차를 만들 가능성이 높기 때문에 앙상블 모델의 정확도를 향상시킴
- 모든 분류기가 클래스의 확률을 예측할 수 있으면(`predict_proba()` 메서드가 있으면) 개별 분류기의 예측을 평균 내어 확률이 가장 높은 클래스를 예측할 수 있음. 이를 soft voting라고 함
~~~python
#- votingClassifier example
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

log_clf = LogisticRegression()
rnd_clf = RandomForestClassifier()
svm_clf = SVC()

voting_clf = VotingClassifier(
    estimators=[('lr', log_clf), ('rf', rnd_clf), ('svc', svm_clf)],
    voting = 'hard'
)

#- 각 분류기의 정확도 확인
for clf in (voting_clf, log_clf, rnd_clf, svm_clf):
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(clf.__class__.__name__, round(accuracy_score(y_test, y_pred), 4))

# VotingClassifier 0.8222
# LogisticRegression 0.8444
# RandomForestClassifier 0.8667
# SVC 0.7
~~~


## bagging, pasting
- 훈련 세트를 중복을 허용하여 샘플링하는 방식을 bagging, 중복 허용을 안하는 방식을 pasting 이라고 함
- 모든 예측기가 훈련을 마치면 결과를 수집하는데, 해당 수집함수는 분류일 때는 통계적 최빈값, 회귀에서는 평균값으로 계산 
- 개별 예측기는 원본 훈련 세트로 훈련시킨 것보다 훨씬 크게 편향되어 있지만 수집 함수를 통과하면 편향과 분산 모두 감소
- 일반적으로 앙상블의 결과는 원본 데이터셋으로 하나의 예측기를 훈련시킬때와 비교해 편향은 비슷하지만 분산은 줄어듬  
  즉, <b>훈련 세트의 오차 수는 거의 비슷하지만, 결정 경계는 덜 불규칙하다는 의미</b>
- 해당 모델을 다른 CPU 코어나 서버에서 병렬로 훈련시킬 수 있어 인기가 많음
- `BaggingClassifier` 클래스는 기반이 되는 분류기가 결정 트리 분류기처럼 클래스 확률을 추정할 수 있으면 hard voting 대신 soft voting 수행
- <b>부트스트래핑은 각 예측기가 학습하는 서브셋에 다양성을 증가시키므로, 배깅이 페이스팅보다 편향이 좀 더 높고, 분산이 적어 더 선호됨</b>
- 시간과 여유가 있다면 교차 검증으로 둘 다 비교하는 것이 좋음
![img](https://github.com/koni114/TIL/tree/master/Machine-Learning/img/bagging_ensemble.JPG)
~~~python
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

bag_clf = BaggingClassifier(
    DecisionTreeClassifier(),
    n_estimators=500,
    max_samples=100,
    bootstrap=True,
    n_jobs=-1)

bag_clf.fit(X_train, y_train)
y_pred = bag_clf.predict(X_test)
print(bag_clf.__class__.__name__, round(accuracy_score(y_test, y_pred), 4))
~~~
- 단일 결정 트리와 500개의 결정 트리 앙상블 모형을 비교하면, 편향은 거의 비슷하지만 분산은 감소하는 것을 확인할 수 있음


### oob 평가
- 배깅을 사용하면 어떤 샘플은 선택되고, 어떤 샘플은 선택되지 않을 수 있음
- `BaggingClassifier`는 기본값으로 중복을 허용하여 훈련 세트 m개의 샘플을 선택하는데, 이는 평균적으로  
- 선택되지 않은 나머지 37%를 oob(out-of-bag) 샘플이라고 부름
- 앙상블의 평가는 각 예측기의 oob 평가를 평균하여 얻음
- `BaggingClassifier`를 만들 때 `oob_score = True`로 지정하면 훈련이 끝난 후 자동으로 oob 평가를 수행
- oob 샘플에 대한 결정 함수의 값도 `oob_decision_function_` 변수에서 확인할 수 있음  
  각 훈련 샘플의 클래스 확률을 반환  
~~~python
bag_clf = BaggingClassifier(
    DecisionTreeClassifier(),
    n_estimators=500,
    max_samples=100,
    bootstrap=True,
    n_jobs=-1,
    oob_score=True)

bag_clf.fit(X_train, y_train)
bag_clf.oob_score_

#- 0.8038277511961722

#- oob_test의 결정함수의 값 확인
bag_clf.oob_decision_function_
~~~

### 랜덤 패치와 랜덤 서브스페이스
- `BaggingClassifier`는 특성 샘플링도 지원.  
  `max_features`, `bootstrap_features` 두 매개변수로 조절됨
- 각 예측기는 무작위로 선택한 feature의 일부분으로 훈련됨
- 이미지와 같은 매우 고차원의 데이터를 다룰 때 유용
- 특성과 샘플을 모두 샘플링하는 방식을 <b>랜덤 패치 방식(random patches method)</b>이라고 함
- 훈련 샘플을 모두 사용하고(bootstrap=False, max_samples =1.0) 특성은 샘플링한는 것을 <b>랜덤 서브스페이스(random subspace method)</b>라고 함
- 특성 샘플링은 더 다양한 예측기를 만들며 편향을 늘리는 대신 분산을 낮춤

## 부스팅(boosting)
- 부스팅은 약한 학습기 여러개를 연결하여 강한 학습기를 만들어 내는 앙상블 기법
- 부스팅 방법의 아이디어는 앞의 모델을 보완해나가면서 일련의 예측기를 학습시키는 것
- 부스팅 방법에는 여러가지가 있지만 <b>에이다부스트(adaboost)와 그레디언트 부스트(gradient boost)</b>가 가장 인기 있음

### 에이다부스트(adaboost)
- adpative boosting의 준말
- 이전 모델이 과소적합했던 훈련 샘플의 가중치를 더 높이는 것
- 이렇게 하면 새로운 예측기는 학습하기 어려운 샘플에 점점 더 맞춰지게 됨  
  이것이 adaboost에서 사용하는 방식

1. 첫 번째 분류기(ex) decisionTree)를 훈련 세트에서 훈련시키고 예측을 만듬
2. 알고리즘이 잘못 분류된 훈련 샘플의 가중치를 상대적으로 높임
3. 두 번째 분류기는 업데이트된 가중치를 사용해 훈련 세트에서 훈련하고 다시 예측을 만듬 
4. 1 - 3 번을 반복

- 아래 그림은 moons 데이터셋에 훈련시킨 다섯 개의 연속된 예측기의 결정 경계

![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/adaBoost_1.JPG)

- 이런 연속된 학습 기법은 경사 하강법과 비슷한 측면이 있음  
  경사 하강법은 비용 함수를 최소화하기 위해 한 예측기의 모델 파라미터를 조정해가는 반면 에이다부스트는 점차 더 좋아지도록 앙상블에 예측기를 추가함
- <b>연속된 학습 기법의 가장 큰 단점은 병렬화 할 수 없다는 점이 있음</b>

### 에이다부스트 이론
- 샘플 가중치 W(i)는 초기에 1/m로 초기화됨
- 첫번째 예측기가 학습되고, 가중치가 적용된 에러율 r1이 훈련 세트에 대해 계산됨

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=r_{j}&space;=&space;\frac{\sum_{i=1}^{m}w^{(i)},&space;\hat{y}_{j}^{i}&space;\neq&space;y^{(i)}}{\sum_{i=1}^{m}w^{(i)}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?r_{j}&space;=&space;\frac{\sum_{i=1}^{m}w^{(i)},&space;\hat{y}_{j}^{i}&space;\neq&space;y^{(i)}}{\sum_{i=1}^{m}w^{(i)}}" title="r_{j} = \frac{\sum_{i=1}^{m}w^{(i)}, \hat{y}_{j}^{i} \neq y^{(i)}}{\sum_{i=1}^{m}w^{(i)}}" /></a></p>

- <b>예측기의 가중치</b> alpha(j)는 아래 식을 이용해 계산됨
- 여기서 eta는 학습률 파라미터이고 기본값은 1임
- 예측기가 정확할수록 예측기의 가중치가 더 높아지게 됨
- 만약 무작위로 예측하는 경우 가중치는 0에 가까워지고, 무작위보다 못하다면 음수가됨 

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\alpha_{j}&space;=&space;\eta&space;\cdot&space;log&space;\frac{1-&space;r_{j}}{r_{j}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\alpha_{j}&space;=&space;\eta&space;\cdot&space;log&space;\frac{1-&space;r_{j}}{r_{j}}" title="\alpha_{j} = \eta \cdot log \frac{1- r_{j}}{r_{j}}" /></a></p>

- 그다음 에이다부스트가 아래 식을 사용해 가중치를 업데이트함
- 즉 잘못 분류된 데이터의 가중치 값이 추가됨

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=w^{(i)}&space;\leftarrow&space;\begin{Bmatrix}&space;W^{(i)},&space;\hat{y}_{j}^{(i)}&space;=&space;y_{j}^{i}&space;\\&space;W^{(i)}&space;\cdot&space;exp(\alpha_{j}),&space;\hat{y}_{j}^{(i)}&space;\neq&space;y_{j}^{i}&space;\end{Bmatrix}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?w^{(i)}&space;\leftarrow&space;\begin{Bmatrix}&space;W^{(i)},&space;\hat{y}_{j}^{(i)}&space;=&space;y_{j}^{i}&space;\\&space;W^{(i)}&space;\cdot&space;exp(\alpha_{j}),&space;\hat{y}_{j}^{(i)}&space;\neq&space;y_{j}^{i}&space;\end{Bmatrix}" title="w^{(i)} \leftarrow \begin{Bmatrix} W^{(i)}, \hat{y}_{j}^{(i)} = y_{j}^{i} \\ W^{(i)} \cdot exp(\alpha_{j}), \hat{y}_{j}^{(i)} \neq y_{j}^{i} \end{Bmatrix}" /></a></p>

- 마지막으로 샘플의 가중치를 정규화하고, 해당 가중치가 부여된 데이터를 새 예측기가 학습하고 전체 과정이 반복됨
- 이 알고리즘은 지정된 예측기 수에 도달하거나, 완벽한 예측기가 만들어지면 종료됨
- <b>예측을 할 때 에이다부스트는 단순히 모든 예측기의 예측을 계산하고 예측기 가중치 alpha(j)를 더해 예측 결과를 만듬</b>
- 사이킷런은 SAMME라는 에이다부스트의 다중 클래스 버전을 사용. 클래스가 두 개뿐일 때는 SAMME가 에이다부스트와 동일
- 예측기가 클래스의 확률을 추정할 수 있다면 SAMME.R(Real) 이라는 변종을 사용
- `AdaBoostClassifier`의 기본 추정기는 `max_depth = 1`인 DT임
- `AdaBoostRegressor`는 `max_depth = 3`인 DT를 기본 추정기로 사용함
~~~python
from sklearn.ensemble import AdaBoostClassifier
ada_clf = AdaBoostClassifier(
    DecisionTreeClassifier(max_depth=1), n_estimators=200,
    algorithm="SAMME.R", learning_rate=0.5)
ada_clf.fit(X_train, y_train)
~~~

### 그레디언트 부스팅
- 앙상블에 이전까지의 오차를 보정하도록 예측기를 순차적으로 추가함
- <b>이전 예측기가 만든 잔여 오차(residual error)에 새로운 예측기를 학습시킴</b>
- 결정 트리를 기반 예측기로 사용하는 것을 <b>그레디언트 트리 부스팅, 그레디언트 부스티드 회귀 트리(GBRT)라고 함</b>
- `GradientBoostingRegressor` 를 사용하면 GBRT 앙상블을 간단하게 훈련시킬 수 있음
- 다음은 이전에 만든 것과 같은 앙상블을 만드는 코드
~~~python
from sklearn.ensemble import GradientBoostingRegressor
gbrt = GradientBoostingRegressor(max_depth=2, n_estimators=3, learning_rate=1.0)
gbrt.fit(X, y)
~~~
- `learning_rate` 매개변수가 각 트리의 기여 정도를 조절하는데, 즉 <b>잔차예측값 x 학습률</b>으로 사용됨
- learning_rate를 낮게 설정하면 그만큼의 많은 트리가 필요하지만 예측의 성능은 좋아지며, 이를 축소(shrinkage)라고 부르는 규제 방법 
- learning_rate가 크면 오차예측값의 반영률이 높으므로 과대적합될 우려가 있음
- 최적의 트리수를 찾기 위해서는 early stopping 사용
- 간단하게 사용하려면 `staged_predict()` 사용. 이 메서드는 훈련의 각 단계(트리 하나, 트리 둘)에서 앙상블에 의해 만들어진 예측기를 순회하는 iterator를 반환
- 다음 코드는 120개의 트리로 GBRT 앙상블을 훈련시키고, 최적의 트리 수를 찾기 위해 각 훈련 단계에서 검증 오차를 측정함
- 마지막에 최적의 트리 수를 사용해 새로운 GBRT 앙상블을 훈련시킴
~~~python
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

X_train, X_val, y_train, y_val = train_test_split(X, y)

gbrt = GradientBoostingRegressor(max_depth=2, n_estimators=120)
gbrt.fit(X_train, y_train)

errors = [mean_squared_error(y_val, y_pred)
          for y_pred in gbrt.staged_predict(X_val)]

bst_n_estimators = np.argmin(errors) + 1

gbrt_best = GradientBoostingRegressor(max_depth=2, n_estimators=bst_n_estimators)
gbrt_best.fit(X_train, y_train)
~~~
- 해당 함수는 많은 수의 트리 모형을 만들고, 최적의 트리 모형 개수를 찾아내는 방식
- 사이킷런 0.20 버전에서 그레디언트 부스팅에 early stopping 기능이 추가 되었음
- 훈련 데이터에서 `validation_fraction` 비율 만큼 떼내어 `n_iter_no_change` 반복 동안에 `tol` 값 이상 향상되지 않으면 훈련이 멈춤
- `GradientBoostingRegressor`는 `subsample` 파라미터도 지원
- 이렇게 subsampling한 데이터로 weak learner를 만들면 편향은 증가하면서 분산은 감소하고 속도 성능은 증가시킬 수 있음. 이런 기법을 <b>확률적 그레디언트 부스팅(stochastic gradient boosting)</b> 이라고 함
- 다음 예제는 grdient boosting 알고리즘을 만드는 예제. decisionTree 3개를 가지고 잔여 오차를 예측하여 각 모델을 앙상블한 것 
~~~python
#- 1. 먼저 DecisionTreeRegressor를 훈련 세트에 학습
from sklearn.tree import DecisionTreeRegressor
tree_reg1 = DecisionTreeRegressor(max_depth=2)
tree_reg1.fit(X, y)

#- 2. 첫번째 예측기에서 생긴 잔여 오차에 두번째 DecisionTreeRegressor를 훈련
y2 = y - tree_reg1.predict(X)
tree_reg2 = DecisionTreeRegressor(max_depth=2)
tree_reg2.fit(X, y2)

#- 3. 두번째 예측기에서 생긴 잔여 오차에 세번째 DecisionTreeRegressor를 훈련
y3 = y2 - tree_reg2.predict(X)
tree_reg3 = DecisionTreeRegressor(max_depth=2)
tree_reg3.fit(X, y3)

#- 4. 세 개의 트리를 포함하는 앙상블 모델을 통한 예측은 3개의 값을 합치면 됨
y_pred = sum(tree.predict(X_test) for tree in (tree_reg1, tree_reg2, tree_reg3))
~~~
- 최적화된 그레이디언트 부스팅 구현으로 XGBoost 파이썬 라이브러리가 유명함
~~~python
import xgboost
xgb_reg = xgboost.XGBRegressor()
xgb_reg.fit(X_train, y_train,
            eval_set=[(X_val, y_val)], early_stopping_rounds=2) #- 조기 종료 기능도 제공
y_pred = xgb_reg.predict(X_val)
~~~

## 스태킹(stacking)
- stacked generalization의 줄임말
- 앙상블에 속한 모든 예측기의 예측을 취합하는 간단한 함수를 사용하는 대신, 취합하는 모델을 훈련시키면 어떨까? 라는 아이디어에서 출발
- 마지막 취합하는 예측기를 <b>블랜더(blender), 메타 학습기(meta learner)라고 함</b>
- 블랜더를 학습시키는 일반적인 방법은 홀드 아웃 세트를 사용하는 것
1. 먼저 훈련 세트를 2개의 서브셋으로 나눔
2. 첫 번째 서브셋을 첫 번째 레이어의 예측을 훈련시키기 위해 사용
3. 첫 번째 레이어의 예측기를 사용해 두 번째 서브셋에 대한 예측값을 만듬
4. 해당 예측한 값을 특성으로 새로운 훈련세트를 만들고, 이 데이터를 가지고 블렌더를 훈련시킴
- 이런 방식으로 레이어를 증가시킬 수 있음
- 만약 2개의 layer가 필요하다면, 3개의 subset이 필요!
- 사이킷런 0.22 버전에서 `StackingClassifier`와 `StackingRegressor`가 추가됨 

## 용어 정리
- 큰 수의 법칙(law of large numbers)
  - 동전을 자꾸 던질수록 실제 확률에 점점 더 가까워 지는 것을 말함  
    예를 들어 앞면이 51%, 뒷면이 49%가 나오는 동전이 있다고 할때 동전을 점점 더 여러번 던질수록  
    해당 확률에 가까워짐을 의미함
  - 동전을 1000번 던진 후 앞면이 다수가 될 확률은 75%, 10,000번 던지면 확률이 97%까지 높아짐
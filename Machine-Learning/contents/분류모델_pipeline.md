# chapter03 분류
- 사이킷런에서 제공하는 여러 헬퍼 함수를 사용해 잘 알려진 데이터셋을 내려받을 수 있음
- 사이킷런에서 읽어 들인 데이터셋은 일반적으로 비슷한 딕셔너리 구조를 가지고 있음
  - 데이터셋을 설명하는 DESCR 키
  - 샘플이 하나의 행, 특성이 하나의 열로 구성된 data 키
  - 레이블 배열을 담은 target 키
- 확률적 경사 하강법(Stochastic Gradient Descent, SGD)은 한 번에 하나씩 훈련 샘플을 독립적으로 처리
- 시계열 데이터를 제외하고는 train/test를 층화 샘플링을 통해서 잘 나눠야 함

## 이진 분류기 훈련
- `SDGClasifier` 는 무작위로 데이터를 선택하기 때문에 필요하다면 `random_state` 값 지정 필요
- `model.predict()` 할 때, array 차원을 항상 조심. --> `model.predict([])`
- 특히 imbalanced한 데이터를 다룰 때 성능 지표로 accuracy는 좋지 않음  
  f1-score, precision, recall, AUC 등을 이용하자
- `cross_val_predict` 함수를 이용해서 수행시, cross-validation 시, validation set으로 예측했던 데이터의 예측값을 조합해 최종 pred를 return


## 정밀도(precision)과 재현율(recall)
- 재현율(recall)은 민감도(sensitivity)나 TPR(True Positive Rate) 진짜양성비율 이라고도 함
- 정밀도가 재현율 보다 중요한 경우  
  ex) 안전한 동영상을 걸러내는 분류기
- 재현율이 정밀도보다 중요한 경우  
  ex) 카메라를 통해 좀도둑을 잡아내는 모델 
- 이 둘을 모두 얻을 수는 없음 --> <b>정밀도/재현율 트레이드오프</b>라고 함

### precision-recall curve
![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/precision_recall_curve.jpg)

- 좋은 정밀도/재현율 트레이드오프를 선택하는 방법(적절한 임계값을 선택하는 방법)은 재현율에 대한 정밀도 곡선(X축: 임곗값, Y축: 정밀도, 재현율 곡선 2개)을 그리는 것 
- 해당 곡선에서 정밀도 곡선은 울퉁불퉁하게 나타나는데, 그 이유는 임곗값이 높아질 때 정밀도가 반드시 좋아지는 것은 아님. 하지만 재현율은 반드시 좋아짐   


### PR curve
![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/PR_Curve.jpg)

- 정밀도가 급격하게 떨어지는 지점이 보이는데, 이 지점을 정밀도/재현율 trade-off 지점으로 정하면 좋음
- 이런 선택은 프로젝트의 성격에 따라서 달라짐

## ROC 커브
![img](https://github.com/koni114/TIL/blob/master/Machine-Learning/img/ROC_Curve.JPG)

- receiver operating characteristic(ROC)
- <b>ROC 커브는 threshold가 가장 큰 값에서 점점 작아지는 방향으로 진행</b>
- <b>Y축 : 진짜 양성으로 잘 예측한 것들 / 양성 데이터</b>
- <b>X축 : 음성인데, 양성으로 잘못 예측한 것들 / 음성 데이터</b>
- AUC 값의 범위는 0.5 ~ 1
- ROC 커브의 가장 큰 단점은 양성의 수가 적을 때(ex) 불량의 개수가 매우 적을 때)는 X
- <b>상황에 따라 ROC Curve를 사용할지, PR(Precision/Reall) Curve를 사용할지 판단해야함</b>
  - 양성 클래스가 드물거나, 거짓 음성보다 거짓 양성이 중요할때 PR 곡선 사용  
    why? 양성 클래스가 드물때 ROC커브를 사용하게 되면, TPR(진짜양성으로 예측 / 양성데이터) 값이 왠만하면 커지게됨
  - 그렇지 않으면 ROC 커브 사용
- PR 커브는 분류기의 성능 개선 여지가 얼마나 되는지 잘 보여줌
- sklearn 분류기는 보통 `decision_function()` 또는 `predict_proba()` 메서드 둘 중 하나를 가지고 있음

## 다중 분류
- RF, SGD 분류기, NB 같은 일부 알고리즘은 여러 개의 클래스를 처리 가능
- 로지스틱 회귀, SVM 같은 모델은 이진 분류만 가능
- 이진 분류기를 여러개 사용해서 다중 분류를 하는 경우도 많이 있음
- 특정 숫자 하나만 구별하는 숫자별 이진 분류기 10개를 훈련시켜 클래스가 10개인 숫자 이미지 분류 시스템을 만들 수 있음 --> <b>OvA(Overall versus all) 전략, OvR(Overall versus the rest) 전략이라고 함</b>
- 다른 전략은 0과1 구별, 0과2 구별... 처럼 각 숫자의 조합마다 이진 분류기를 훈련 --> <b>OvO 전략이라고 함</b>  
가장 많이 양성으로 분류된 클래스를 선택함
- OvO 전략의 주요 장점은 각 분류기의 훈련에 전체 훈련 세트 중 구별할 두 클래스에 해당하는 샘플만 필요하다는 점
- <b>훈련 세트의 크기에 민감한 SVM 같은 모델들은 OvO를 선호, 하지만 대부분의 이진 분류 알고리즘들은 OvR을 선호</b>

## 에러 분석
- 모델에 대한 에러 분석시, confusion matrix에 대한 `matshow()` 함수를 사용한 히트맵 시각화를 하면 좋음
- 오차행렬의 시각화를 통해 잘못 예측하고 있는 특정 레이블을 찾아 해당 레이블의 데이터를 더 수집하거나 할 수 있음
- 또는 MNIST 같은 경우, 동심원의 수를 세는 특성을 추가할 수 있음(8 -> 2, 6 -> 1,  5 -> 0)

## 다중 레이블 분류(multilabel-classification)
- 분류기가 샘플마다 여러개의 레이블 클래스를 출력해야 할 수도 있음
- 얼굴 인식 분류기를 생각해보자. 같은 사진에 여러 사람이 등장한다면, 다중 레이블 분류가 필요  
  분류기가 엘리스, 밥, 찰리 세 얼굴을 인식하도록 훈련되었으면, [1, 0, 1] 와 같은 레이블이 출력되어야 함 
- `KNeighborClassifier`는 다중 레이어 분류를 지원하지만, 모든 분류기가 그런것은 아님
- 다중 레이블 분류기를 평가하는 방법은 많음. 적절한 지표는 프로젝트에 따라 다름  
  예를 들어 각 레이블의 F1 점수를 구하고 간단히 평균 계산을 할 수 있음
- 각 레이블마다의 가중치를 부여할 수 있는데, 예를 들어 지지도(타깃 레이블에 속한 샘플 수)를 가중치로 두는 것 --> `average = "weighted"`로 부여

## 다중 출력 분류(multioutput-classification)
- 다중 레이블 분류에서 한 레이블이 다중 클래스가 될 수 있도록 일반화한 것
(하나의 레이블이 여러개의 값을 가질 수 있음)
- ex) 이미지의 잡음을 제거하는 시스템.  
잡음이 많은 이미지를 입력으로 받아 깨끗한 숫자 이미지를 MNIST 이미지처럼 픽셀의 강도를 담은 배열로 출력
- 위의 예에서는 분류/회귀의 경계는 모호함
# Metrics
- 모델의 성능을 평가하는 지표를 지칭
- 분류/회귀 모형에서의 지표는 각각 다름

## 모델 종류별 Metric 종류
- classification
  - Precision-Recall
  - ROC-AUC
  - Accuracy
  - Log-Loss
  - F1-Score

- Regression
  - MAE
  - MSE
  - RMSE
  - MSPE
  - RMSLE
  - R Square
  - Adjusted R Square

- Unsupervised Model
  - Rand Index
  - Mutual
  - Information

- Others
  - CV Errors
  - Heuristic methods to find K
  - BLEU Scores(NLP)

## Classification Metrics(분류 메트릭)
### 정확도(Accuracy)
- 분류기의 성능을 측정할 때 가장 간단히 사용할 수 있음
- 사실상 가장 많이 쓰는 개념 중 하나로, Target 대비 정확히 예측한 비율을 말함
~~~r
Accuracy <- (TP + TN) / (TP + FP + TN + FN)
~~~

### 정밀도(Precision)
- 모델이 참(TRUE)으로 예측한 것들 중 실제로 TRUE인 것들의 비율
~~~r
precision <- TP / (TP + FP)
~~~

### 재현율(Recall)
- 실제값이 TRUE인 것들 중 모델이 TRUE로 예측한 비율
~~~r
recall <- TP / (TP + FN)
~~~

### LogLoss
- 모델이 예측한 확률 값을 직접적으로 반영한 것
- 확률이 낮을 때 더 큰 패널티를 부과하기 위한 지표
- 예를 들어 확률이 100%일 때 -log(1.0) = 0  이고, 확률이 80% 일 때 -log(0.8) = 0.22314 가됨
- -log_e()의 그래프를 생각할 때 값이 작아질수록 기하 급수적으로 증가함  
- 결과적으로 지표는 전체 샘플에 대한 예측 확률 값을 -log를 취해 모두 더하고 평균을 취함

### F1-Score
- Precision과 Recall의 조화평균. 즉, F1 socre가 높아야 성능이 좋음
- recall, precision중 둘 중에 하나라도 0에 가까우면 그것이 잘 반영되게끔 지표를 설정
- 조화 평균의 식은 다음과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?F1&space;Score&space;=&space;\frac{2&space;Precision&space;*&space;Recall}{Precision&space;&plus;&space;Recall}" /></p>

### Fall-out
- FPR(False Positive Rate)를 Fall-out이라고 지칭함
- 실제 False 값을 TRUE로 잘못 예측한 비율을 의미함

### ROC Curve(개념에 대한 자세한 설명 추가 필요)
- ROC 곡선은 이진 분류 시스템에 대한 성능 평가 기법임
- Cut Off를 조정해 가면서 P,N으로 예측할 확률에 대해서 계산
- 면적(AUC)의 크기로 더 큰 것이 좋다고 할 수 있음 
- x축 : FPR(False Positive Rate), y축 : TPR(True Positive Rate)

## Regression Metrics(예측 메트릭)
### MAE(Mean Absolute Error)
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?MAE&space;=&space;\frac{\sum|{Y}&space;-&space;\hat{Y}|&space;}{n}"/></p>

- 모델의 예측값과 실제값의 차이를 모두 더한다는 개념
- 절대값을 취하기 때문에 값에 대해 직관적으로 파악이 가능
- <b>MSE보다 특이치에 덜 민감함</b> 
- 절대값이기 때문에 모델이 underperformance 인지, overperformance인지 알 수 없음
  - underperformance: 모델이 실제 예측보다 낮은 값으로 예측
  - overperformance : 모델이 실제 예측보다 높은 값으로 예측

### MSE(Mean Square Error)
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?MSE&space;=&space;\frac{\sum({Y}&space;-&space;\hat{Y})^{2}}{n}"/></p>

- MAE와는 다르게 예측값과 실제값의 차이의 면적의 합
- 제곱을 하기 때문에 특이값(이상치)에 민감
- 모델이 non-Robust 한 경우 지표에 대한 성능이 떨어질 수 있음
- 특이치에 민감함

### RMSE(Root Mean Squared Error)
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?RMSE&space;=&space;\sqrt{\frac{\sum({Y}&space;-&space;\hat{Y})^{2}}{n}}"/></p>

- MSE에 Root를 씌운 것
  - RMSE를 사용하면 오류 지표를 실제 값과 유사한 단위로 다시 변경하기 때문에 해석을 쉽게 함 

### MAPE(Mean Absolute Percentage Error)
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?MAPE&space;=&space;\frac{\sum|\frac{Y&space;-&space;\hat{Y}}{Y}|}{n}*100%"/></p>

- MAPE는 MAE를 퍼센트로 변환한 것
- MAE와 마찬가지로 MSE보다 특이치에 robust 함
- MAE와 같은 단점을 가진다.
- 추가적으로 모델에 대한 편향이 존재한다.
  - 이 단점에 대응하기 위해 MPE도 추가로 확인하는게 좋다.
  - 0 근처의 값에서는 사용하기 어렵다.

### RMSLE(Root Mean Square Logarithmic Error)
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?RMSLE&space;=&space;\sqrt{\frac{1}{n}\sum_{i=1}^{n}(log(\hat{y}&plus;1)-&space;log(y&plus;1))^{2}}"/></p>


- RMSE에 로그를 취해 준 것
  - 아웃라이어에 robust 하다. RMSLE는 아웃라이어가 있더라도 값의 변동폭이 크지 않다.
  - log 함수의 특성 상 실제값 보다 예측값이 더 작을 수록 패널티가 더 크게 부여됨
  - 즉 overperformance인지, underperformance인지에 따라 상대적 error를 측정해줌

### R Square
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?R^{2}&space;=&space;\frac{SSR}{SST}"/></p>

- 예측 모델이 상대적으로 얼마나 성능이 나오는지를 측정한 지표
- 다른 성능 지표인 RMSE나 MAE는 데이터의 scale에 따라서 값이 천차만별이기 때문에 절대 값만 보고 바로 성능을 판단하기가 어려운데, 결정계수의 경우 상대적인 성능이기 때문에 이를 직관적으로 알 수 있음
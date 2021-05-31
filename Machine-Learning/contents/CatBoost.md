# CatBoost
- catBoost가 다른 gbm 보다 좋은 성능을 낼 수 있는 이유
  - <b>ordering-priciple</b> 개념을 대입하여 기존의 data-leakage로 인한 prediction-shift 문제 해결 
  - high cardinality를 가진 category 변수들에 대해서 전처리 문제들을 해결했다는 것
- 대부분의 GBM은 decision Tree를 base predictor로 삼는데, 이러한 DT는 수치형 변수에서는 편리하지만 범주형이 포함된 데이터셋에서는 수치형 변수로 전처리를 해준 후 훈련을 해야했기에 학습시간이 오래 걸렸음
- catboost에서는 이러한 문제점을 모델 훈련시간에 동시에 진행을 하면서 시간 단축함
- 기존의 일반적인 GBM은 스텝의 새로운 DT를 만들 때 현재 모델에서 쓰여진 data를 Gradient estimate를 하는데 다시 쓰여지기 때문에 overfitting에 취약한 문제점이 있었음
- 이를 해결하기 위해 기존의 재귀적 분할을 한 후 leaf value를 구하는 방식에서 역순으로 leaf value를 먼저 구하고, 재귀적 분할을 수행하는 ordered principle 개념을 적용해 해결함

## Categorical features
- 범주형 변수는 서로 비교가 불가능한 값을 가지고 있기 때문에 바로 Binary disicionTree와 같은 모형에 쓰일 수 없음
- 따라서 일반적으로 범주형변수를 수치형변수로 전처리 하는데, 일반적으로 낮은 level을 갖는 범주형 변수에 가장 많이 쓰이는 방법이 One-Hot encoding임
- 이러한 전처리 과정이 모형 훈련 전에 일어날 수도 있고 모형 학습 중간에 일어날수도 있는데 후자가 더 성능이 좋다는 것이 밝혀짐
- One-Hot-encoding 외에 수치형 변수로 변환할 수 있는 방법이 catboost 에서 쓰였는데, 해당 category의 level마다 y값의 평균으로 나타내는 방법. 이를 <b>Label encoding</b>이라고 함 
- 이 변환된 변수를 사용한다면 당연히 overfitting 될 것인데, 따라서 hold-out 기법을 사용해 한 part는 label encoding을 통한 수치 변환에 쓰이고, 나머지 part는 실제 모델을 훈련하는데 쓰임. 
- 이 방법을 <b>hold-out TS</b> 라고 하는데 이 방법은 overfitting을 줄일 수 있으나 훈련시키고 statistics을 얻을 수 있는 데이터의 양이 줄어들게 됨
- Catboost에서는 이 방식을 더 개선시켜 TS값을 오직 observed history(여태까지 관찰된 관측치까지만, 즉 4번째 값을 변환시킨다면, 1~3번째 까지의 row만)로 산출되도록 한 <b>ordered-TS</b> 방식을 사용함
- 이 개념은 사실 online learning에서 차용된 것인데, 이를 offline learning에 적용하기 위해서는 인공적인 시간을 만들어야 했고 이 역할을 훈련 데이터의 random permutation(무작위 배열)이 해줌
- 한가지 의문점은 첫 TS를 산출할 때 이전에 쓰인 관측치가 없어 값을 변환할 수 없게됨
- 이를 위해 <b>prior와 이에 대한 가중치 alpha를 도입함.</b> 
- 이 prior는 regression일때는 y값의 평균이며, binary classification에서는 y값이 positive인 사전 확률임
- 최적의 prior를 찾기 위해 같은 모형에 또 다른 permutation을 사용해야 하는데 이렇게 되면 Target Leakage가 발생해 사용할 수 없음
- 따라서 일단 여러개의 모형을 만든 뒤 각 모형에 따른 random permutation 데이터를 넣어 학습 한 뒤 tree structure를 정한 후, 다시 이 tree structure를 다른 모형에 적용시킨 후 다른 모형에서의 prior들의 평균을 구함
- 이렇게 되면 모형마다 다른 데이터를 사용했기 때문에 target leakage 문제가 해결됨

## feature combination
- 범주형 간의 상관관계가 있는 상태에서 수치형으로 변환하게 되면 중요한 정보를 잃을 수 있음
- 따라서 이러한 문제를 해결하기 위해 두 변수를 조합(feature combination)해 새로운 변수를 만듬 
- 이렇게되면 category가 많게 되면 데이터는 exponential하게 커질 것임
- 이러한 문제를 해결하기 위해 greedy한 방식으로 tree를 학습 시킴
- <b>즉 catboost에서는 예를 들어 두 번째 depth의 node에서 범주형 변수를 combination 시키고, 3번째 depth에서 해당 combination된 feature를 다시 다른 범주형 변수와 combination 시키는 방식으로 greedy 하게 진행됨</b> 
- combination은 information gain이 동일한 두 feature를 하나의 feature로 묶어버림

## ordered boosting(ordered TS)
- 기존의 부스팅 과정과 전체적인 양상은 비슷하되, 조금 다름
- 기존의 부스팅 모델이 일괄적으로 모든 훈련 데이터를 대상으로 잔차 계산을 했다면, Catboost는 일부만 가지고 잔차계산을 한 뒤, 이걸로 모델을 만들고, 그 뒤의 데이터 잔차는 이 모델로 예측한 값을 사용
- x1 ~ x10 이라는 데이터 sample이 있을 때, 
  - x1의 잔차만 계산하고, 이를 기반으로 모델을 만듬. 그리고 x2의 잔차를 예측
  - x1, x2의 잔차를 가지고 모델을 만듬. 이를 기반으로 x3, x4의 잔차를 모델로 예측
  - x1, x2, x3, x4의 잔차를 가지고 모델을 만듬. 이를 기반으로 x5, x6, x7, x8의 잔차 예측.
  - 반복...

## Level-wise Tree
- LightGBM과 다르게(--> leaf-wise) Level-wise 로 leaf node를 생성함

## 


## 용어 정리
- hold out 기법
  - 데이터를 train/test로 나누는 방법  
  - 여기서는 train dataset을 두 덩어리로 나누는 것을 의미함
- offline learning
  - batch learning 과 동일한 용어로, 가용한 모든 데이터를 사용해 학습시키는 경우를 말함
  - 이러한 방식은 시간과 자원을 많이 소모하여 일반적으로 오프라인에서 가동됨
  - 먼저 시스템을 훈련시키고 제품 시스템에 적용하면 더 이상의 학습 없이 수행됨
  - 새로운 데이터 추가시, 처음부터 다시 학습해야 함
- online learning 
  - 데이터를 순차적으로 한 개씩 또는 mini-batch로 주입하여 시스템을 학습시킴
  - 매 학습 단계가 빠르고, 비용이 적게들어 시스템은 데이터가 도착하는데로 바로바로 학습 가능
  - 온라인 학습 시스템에서 중요한 파라미터는 새로운 데이터에 얼마나 빠르게 적응할 것인지임  
    이를 학습률(learning rate)라고 함



## 블로그 참조
https://gentlej90.tistory.com/100
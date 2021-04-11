# 의사결정트리(DecisionTree)
## DecisionTree 이론 설명
- 분류, 회귀 작업, 다중출력 작업도 가능한 모델
- randomForest의 기본 구성 요소이기도 함
- 결정 트리의 여러 장점 중 하나는 <b>데이터 전처리가 거의 필요하지 않다는 점</b>
- 특성의 스케일을 맞추거나 평균을 원점에 맞추는 작업이 필요하지 않음
- 결정 트리는 직관적이고 결정 방식을 이해하기 쉬움(white box model)
- 회귀 트리의 최종 값은 해당 리프 노드에 있는 훈련 샘플의 평균 target 값이 예측 값이 됨
- 의사결정나무의 학습 과정은 입력 변수 영역을 두 개로 구분하는 재귀적 분기(recursive partitioning)와 자세하게 구분된 영역을 통합하는 가지치기(pruning) 두 가지 과정으로 요약

## 클래스 확률 추정
- 결정 트리는 한 샘플이 특정 클래스 k에 속할 확률을 추정할 수 있음
- 먼저 이 샘플에 대해 리프 노드를 찾기 위해 트리를 탐색하고 그 노드에 있는 클래스 k의 훈련 샘플의 비율 반환
- 예를 들어 길이가 5cm, 너비가 1.5cm인 꽃잎을 발견했다고 가정하자
- 이에 해당하는 리프 노드는 깊이 2에서 왼쪽 노드이므로 결정 트리는 그에 해당하는 확률 출력
- Setosa(0%, 0/54), Versicolor(90.7%,49/54), Virginica(9.3%, (5/54)) 임
- 이처럼 각 class 별 확률을 알 수 있음
- 사이킷런은 이진 트리만 만드는 CART 알고리즘을 사용. 예를들어 ID3 같은 알고리즘은 둘 이상의 자식 노드를 가진 결정 트리를 만들 수 있음


## 불순도(impurity)
- 기본적으로 지니 불순도가 사용되지만, `criterion` 매개변수를 `entropy` 로 지정하여 엔트로피 불순도를 사용할 수 있음
- 노드의 gini 속성은 불순도를 측정하는데, 한 노드의 모든 샘플이 같은 클래스에 속해 있다면, 이 노드를 순수(gini = 0) 이라고 함
- 즉 gini 불순도가 낮을수록 노드 분할이 잘 되었다고 판단이 가능
- entropy 불순도도 마찬가지로 엔트로피 값이 0이 되었을 때 잘 분할되었다고 판단 가능
- <b>수치 예측 모형같은 경우 불순도를 분산(variance)로 판단</b>
- 최적의 노드 분할을 찾을 때 분류 모델시 information gain(불순도의 차)이 가장 큰 값을 가지는 분기를 찾아 적용하고, 수치 예측 모델은 MSE(잔차제곱합평균)으로 최적의 분기를 찾음

### 1. Gini 불순도
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?G_{i}&space;=&space;1&space;-&space;\sum_{k&space;=&space;1}^{n}&space;P_{i,k}^{2}" /></p>

- 이 식에서 P(i, k)는 i번째 노드에 있는 훈련 샘플 중 클래스 k에 속한 샘플의 비율    
  ex) iris같은 경우, Setosa class의 비율은 (0/50)^2 이런 식으로 계산.. 

### 2. entropy 불순도
- 엔트로피는 원래 분자의 무질서함을 측정하는 것으로 원래 열역학의 개념
- 분자가 안정되고 질서 정연하면 0에 가까움
- <b>감소되는 엔트로피의 양을 보통 information gain 이라고 부름</b>
- 일반적으로 머신 러닝에서의 정보 이득을 말할때는 쿨백-라이블러 발산을 말함
- 여기서는 모든 메세지(class)가 동일할 때 엔트로피는 0이됨
- entropy 식은 다음과 같음(하단 식에서 마이너스 추가해야함!)
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?H_{i}&space;=&space;\sum_{k&space;=&space;1,&space;p_{i,&space;k&space;!=&space;0}}^{n}&space;P_{i,&space;k}*&space;log_{2}(P_{i,&space;k})" /></p>

- 지니 불순도와 엔트로피 중 어느 것을 사용해야 하나?
- 사실 실제로는 큰 차이는 없음. 즉 둘다 비슷한 트리를 생성해 냄
- 지니 불순도가 조금 더 계산이 빠르고, 가장 빈도 높은 클래스를 한쪽 가지로 고립시키는 경향이 있는 반면, 엔트로피는 조금 더 균형 잡힌 트리를 만듬

## CART(Classification and regression Tree) 훈련 알고리즘
- 트리를 성장(train)시키기 위한 알고리즘 중 하나
- 먼저 훈련 세트를 하나의 특성 k의 임곗값 t(k)를 사용해 두 개의 서브셋으로 만듬   
  (ex) 꽃잎의 길이, 2.45cm)
- k와 t(k)는 가장 순수한 서브셋으로 나눌 수 있는 (k, t(k))의 짝을 찾음
- 이 알고리즘이 최소화해야 하는 비용 함수는 다음과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?J(k,&space;t_{k})&space;=&space;\frac{m_{left}}{m}&space;G_{left}&space;&plus;&space;\frac{m_{right}}{m}&space;G_{right}" /></p>

- G(left/right)는 왼쪽/오른쪽 서브셋의 불순도
- M(left/right)는 왼쪽/오른쪽 서브셋의 샘플 수
- 회귀 트리에서의 CART 알고리즘 비용 function은 다음과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?J(k,&space;t_{k})&space;=&space;\frac{m_{left}}{m}&space;MSE_{left}&space;&plus;&space;\frac{m_{right}}{m}&space;MSE_{right}" /></p>

- CART 알고리즘이 훈련 세트를 성공적으로 둘로 나누었다면 같은 방식으로 서브셋을 또 나누고, 그 다음엔 서브셋의 서브셋을 나누고 이런 식으로 계속 분할 됨
- 이 과정은 최대 깊이가 되면 중지되거나, 더 이상 불순도를 줄이는 분할을 할 수 없을 때 멈추게 됨
- 다른 몇 개의 매개변수도 중지 조건에 관여함  
- <b>CART 알고리즘은 greedy algorithm임</b> 맨 위 루트 노드에서 최적의 분할을 찾으며 이어지는 각 단계에서 이 과정을 반복함
- 현재 단계의 분할이 몇 단계를 거쳐 가장 낮은 불순도로 이어질 수 있을지 없을지는 고려하지 않음

### CART TREE 계산 복잡도
- 예측을 하려면 결정 트리를 루트 노드에서부터 리프 노드까지 탐색해야 함
- 일반적으로 결정 트리는 거의 균형을 이루고 있으므로 결정 트리를 탐색하기 위해서는 O(log2(m)) 개의 노드를 거쳐야 함
- 각 노드는 하나의 특성값만 확인하기 때문에 예측에 필요한 전체 복잡도는 특성 수와 무관하게 O(log2(m)) 임
- 훈련 샘플의 모든 특성을 비교하는 경우, 특성의 수가 n일때 <b>O(n x mlog(m))</b> 임
- 사이킷런은 (present = True로 지정하면) 미리 데이터를 정렬하여 훈련 속도를 높일 수 있음. 하지만 훈련 세트가 클 경우에는 속도가 많이 느려짐

## 규제 매개변수
- 결정 트리는 훈련 데이터에 대한 제약 사항이 거의 없음  
  반면에 선형 모델은 데이터가 선형일 것이라 가정
- 제한을 두지 않으면 트리가 훈련 데이터에 아주 가깝게 맞추려고 해서 대부분 과대적합 되기 쉬움
- 결정 트리는 모델 파라미터가 전혀 없는 것이 아니라(보통 많음) 훈련되기 전에 파라미터 수가 결정되지 않기 때문에 이런 모델을 <b>비파라미터 모델(nonparameter-model)</b>이라고 부름
- 그래서 모델 구조가 데이터에 맞춰져서 고정되지 않고 자유로움
- 반면 선형 모델 같은 <b>파라미터 모델(parameter model)</b>은 미리 정의된 파라미터 수를 가지므로 자유도가 제한되고 과대적합될 위험이 줄어듬
- 결정 트리의 규제 매개변수는 다음과 같은 것들이 있음
  - max_depth(최대 깊이 수)
  - min_samples_split(분할되기 위해 노드가 가져야 하는 최소 샘플 수)
  - min_samples_leaf(리프 노드가 가지고 있어야 할 최소 샘플 수)
  - min_weight_fraction_leaf
  - max_leaf_nodes(리프 노드의 최대 수)
  - max_features(각 노드에서 분할해 사용할 특성의 최대 수)
- 제한 없이 결정 트리를 훈련시키고 불필요한 노드를 가지치기(pruning)하는 알고리즘도 있음
- 순도를 높이는 것이 <b>통계적으로 큰 효과가 없다면</b> 리프 노드 바로 위에 노드는 불필요할 수 있음
- 대표적으로 카이제곱 검정 같은 통계적 검정을 사용하여 우연히 향상된 것인지 추정
- 이 확률을 p-값이라고 부르며 어떤 임곗값보다 높으면 그 노드는 불필요한 것으로 간주되고 그 자식 노드는 삭제됨
- 어떤 임곗값(하이퍼파라미터로 조정 가능하지만 통상적으로 0.05)보다 높으면 그 노드는 불필요한 것으로 간주하고 그 자식 노드는 삭제됨

## decisionTree 불안정성
- decisionTree는 몇 가지 제약사항이 존재
- 결정 트리는 계단 모양의 결정 경계를 만듬(모든 분할은 축에 수직임)
- 그래서 훈련 세트의 회전에 민감  
  예를 들어 X축의 수직으로 완벽하게 구분할 수 있는 데이터가 있을때 이를 45도 회전시키면  
  몇개의 계단을 만들어 구분해야 함
- 이를 해결할 수 있는 방법 중 하나는 훈련 데이터를 더 좋은 방향으로 회전시키는 PCA 기법을 사용하는 것

![img](https://github.com/koni114/Machine-Learning/blob/master/img/decisionTree_rotation.JPG)

- decisionTree의 주된 문제는 훈련 데이터에 있는 작은 변화에도 매우 민감하다는 것
- 사이킷런에서 사용하는 의사결정트리 모형은 각 노드에서 평가할 후보 특성을 무작위로 선택하기 때문에 만들 때 마다 모형이 바뀔 수 있음 


##  Decision Tree 재귀적 분기
* 한 변수 기준으로 정렬
* 이후 가능한 모든 분기점에 대해 엔트로피/지니 계수를 구해 분기 전과 비교해 Information Gain을 계산
* 다른 변수도 위의 두 과정을 동일하게 진행
* 이 중에서 가장 Information Gain 값이 큰 분기점을 선택해 분기 수행
* 이러한 과정을 계속 반복(recursive)를 수행 해 분기를 수행
* 1회 분기를 위해 수행해야 하는 경우의 수 : 변수 v개, recode n개라고 하면, --> v(n-1) 번 만큼 수행

#### 가지치기
* 모든 terminal node의 순도가 100%인 tree를 Full Tree라고 하는데,  Full tree를 생성한 뒤 적절한 수준에서 terminal node를 결합해 주어야 함
* 가지치기의 비용함수(cost function)가 있는데, 이 비용함수를 최소로 하는 분기를 찾아내도록 학습됨 
* CC(T) : 의사결정나무의 비용 복잡도(= 오류가 적으면서, terminal node 수가 적은 단순한 모델일수록 작은 값)
* ERR(T) : 검증 데이터에 대한 오분류율
* L(T) : terminal node 수
* Alpha : ERR(T) 와 L(T) 를 결합하는 가중치(사용자에 의해 부여됨. 보통 0.1 ~ 0.01 사이의 값을 씀)
$$ CC(T)=Err(T)+\alpha \times L(T) $$ 


### 의사결정트리 종류
#### CTREE
* hyper parameter
  * min_split
    * 한 노드를 분할하기 위해서 필요한 데이터 개수 
    * default : 10
  * max_depth
    * 나무구조의 깊이 설정. 뿌리노드는 0, maxdepth = 5이면 나무구조는 뿌리구조에서 5단계 내려감. 
    * default : 10	
  * minbucket 
    * 최종 노드에 포함되어야 할 데이터의 최소 개수
  * cp 
    * 비용복잡함수의 벌점 모수. 노드를 분할 할 때 분할 전과 비교하여 오분류율이 cp값 이상으로  
    향상되지 않으면 더 이상 분할하지 않고 나무 구조 생성을 멈춤. 
    * default : 0.01  

#### CART:RPART
*  rpart 패키지에서는 cp값을 증가시켜가며 tree 크기를 감소시켜 x validation error(xerror)을 계산
* xerror이 최소로 하는 cp가 최적
* hyper parameter
  * min_split
    * 한 노드를 분할하기 위해서 필요한 데이터 최소 개수 
  * xval
    * 교차타당성의 fold 개수, 디폴트는 10 
  * cp
    *  비용복잡함수의 벌점모수. 노드를 분할할 때 분할 전과 비교하여 
     오분류율이 cp 값 이상으로 향상되지 않으면 더 이상 분할하지 않고 나무구조 생성을 멈춤. 디폴트는 0.01
  * nsplit 
    * 가지의 분기수. nsplist + 1 만큼의 leaf node 생성. 

#### C50
* hyper paramter
  *  Winnowing
     * 입력 필드에 대해서 사전에 필드가 유용한지 측정한 다음 유용하지 않는 경우 배제하고 모델링
  *  globalPrunning
     *  전역적 가지치기 여부를 결정
     * 전역적 가지치기는 전체적으로 만들어진 Tree 구조에서  
     가지치기를 수행하는데 강도가 약한 sub-tree자체를 삭제
  * earlyStopping
    * 성능이 더이상 좋아지지 않으면 modeling stop.


### Caret :: DecisionTree
#### CTREE
*  parameter : cp
   * The complexity parameter (cp) is used to control the size of the decision tree and to select the optimal tree size.
#### RPART
* parameter : mincriterion
  * the value of the test statistic (for testtype == "Teststatistic"),  
    or 1 - p-value (for other values of testtype) that must be exceeded in order to implement a split.
    mincriterion = 0.95
#### C50
* parameter  :  trials, model, winnow
  * model : 'tree', 'rules'

## 용어 정리
- 리프 노드
  - 자식 노드가 없는 노드를 말함
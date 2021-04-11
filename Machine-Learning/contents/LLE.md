# LLE(Locally Linear Embedding)
- 지역 선형 임베딩이라고 하는 LLE는 강력한 비선형 차원 축소(nonlinear dimensionally reduction) 기술
- 이전 알고리즘처럼 투영에 의존하지 않는 매니폴드 학습
- LLE는 각 훈련 샘플이 가장 가까운 이웃(closest neighbor, c.n)에 얼마나 선형적으로 연관되어 있는지 측정
- 그런 다음 국부적인 관계가 가장 잘 보존되는 훈련 세트의 저차원 표현을 찾음
- 특히 이 방법은 잡음이 너무 많지 않는 경우 꼬인 매니폴드를 펼치는 데 잘 작동함
- 사이킷런의 `LocallyLinearEmbedding`을 사용해 스위스 롤을 펼침
- 아래 그림처럼 펼칠 수 있음

![img](https://github.com/koni114/Machine-Learning/blob/master/img/LLE.JPG)

- 그림에서 볼 수 있듯이 스위스 롤이 완전히 펼쳐졌고 지역적으로는 샘플 간 거리가 잘 보존되어 있음
- 그러나 크게 보면 샘플 간 거리가 잘 유지되지 않음
- 그럼에도 불구하고 모델링하는 데 잘 작동함  

## LLE 이론
1. 먼저 알고리즘이 각 훈련 샘플 x^(i)에 대해 가장 가까운 k개의 샘플을 찾음  
   여기서의 k는 하이퍼파라미터 
2. 이 이웃에 대한 선형함수로 x^(i)를 재구성함  
   다시 말하면 x^(i)와 sum{j=1, m} w_{i,j} x^(j) 사이의 거리가 최소가 되는 w(ij)를 찾는 것  
   여기서 x^{(j)}는 이웃 k개의 샘플을 말함
3. 결과적으로 아래 식의 최적화 문제를 푸는 것. W는 w(ij)를 모두 담은 가중치 행렬  
   두 번째 제약은 각 훈련 샘플 x^(i)에 대한 가중치를 단순히 정규화하는 것

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\hat{W}&space;=&space;argmin&space;\sum_{i=1}^{m}(x^{(i)}&space;-&space;\sum_{j=1}^{m}w_{i,&space;j}&space;\cdot&space;x^{(j)})^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{W}&space;=&space;argmin&space;\sum_{i=1}^{m}(x^{(i)}&space;-&space;\sum_{j=1}^{m}w_{i,&space;j}&space;\cdot&space;x^{(j)})^{2}" title="\hat{W} = argmin \sum_{i=1}^{m}(x^{(i)} - \sum_{j=1}^{m}w_{i, j} \cdot x^{(j)})^{2}" /></a></p>

4. 가중치 행렬 W는 훈련 샘플 사이의 지역적 선형 관계를 담고 있음  
  가능한 한 이 관계가 보존되도록 훈련 샘플을 d차원 공간(d < n)으로 매핑
5. 만약 z^(i)가 d차원 공간에서 x^(i)의 상(image)라면 가능한 한  
   z^(i)와 sum_{j=1}^{m} \hat{W_{i, j}} z^(j) 사이의 거리가 최소화 되어야 함
- 첫 번째 단계와 비슷해 보이지만, 샘플을 고정하고 최적의 가중치를 찾는 첫 번째 단계와는 다르게  
  가중치를 고정하고 저차원의 공간에서 샘플 이미지의 최적 위치를 찾음
- Z는 모든 z^(i)를 포함하는 행렬임

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Z&space;=&space;argmin(z^{(i)}&space;-&space;\sum_{j=1}^{m}W_{i,j}z^{(j)})^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Z&space;=&space;argmin(z^{(i)}&space;-&space;\sum_{j=1}^{m}W_{i,j}z^{(j)})^{2}" title="Z = argmin(z^{(i)} - \sum_{j=1}^{m}W_{i,j}z^{(j)})^{2}" /></a></p>

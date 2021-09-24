## chapter04 협업 필터링

### 협업필터링의 개요
- 사용자의 구매 패턴이나 평점을 가지고 다른 사람들의 구매 패턴, 평점을 통해 추천을 하는 방법
- 나에 대해서 추천을 해줄 때, 내가 평점을 매긴 것과 비슷한 사용자들을 찾아 추천을 해주는 방법
- 종류 
  - 최근접 이웃기반
  - 잠재 요인기반 등

### Neighborhood based method
- 최근접 이웃기반 모델
- Neighborhood based Collaborative Filtering은 메모리 기반 알고리즘으로 협업 필터링을 위해 개발된 초기 알고리즘
- 알고리즘은 크게 2가지로 나눔
  - User-based collaborative filtering  
    사용자의 구매 패턴과 유사한 사용자를 찾아 추천 리스트 생성
  - item-based collaborative filtering  
     특정 사용자가 준 점수간의 유사한 상품을 찾아 추천 리스트 생성

### K Nearest Neighbors
- 가장 근접한 k 명의 Neighbors를 통해 예측하는 방법
- 해당 알고리즘도 추천에서 사용
- 데이터(Explicit Feedback -> 사용자가 직접 선호도를 작성한 데이터를 말함)

#### User Based Collaborative Filtering
- Explicit Feedback data를 통해 사용자간의 유사도를 계산(이 때 모르는 값은 계산 안함)
- 유사도 계산을 할 때, 평점 같은 경우 어떤 사람들은 평점을 높게 주고, 어떤 사람들은 평균을 낮게 주는 경향이 있으므로 이러한 bias를 제거하기 위해서 모든 데이터에서 자신의 평균 평점을 뺀 값에서 유사도를 계산
- 지금과 같은 User Based의 유사도는 rowise 기반으로 유사도를 계산

#### Item Based Collaborative Filtering
- 아이템 기반을 columize 기반으로 유사도를 계산한다고 보면 됨

### Neighborhood based method 장점
- 간단하고 직관적인 방식으로 구현 및 디버그가 쉬움
- 특정 Item을 추천하는 이유를 정당화하기 쉽고 Item 기반 방법의 해석 가능성이 두드러짐
- 추천 리스트에 새로운 Item과 user가 추가되어도 상대적으로 안정적

### Neighborhood based method 단점
- User 기반 방법의 시간, 속도, 메모리가 많이 필요
- 희소성 때문에 제한된 범위가 있음  
  - John의 Top-k만 관심이 있음
  - John과 비슷한 이웃 중에서 아무도 해리포터를 평가하지 않으면, John의 해리포터에 대한 등급 예측을 제공할 수 없음
- 추천 시스템의 가장 큰 문제는 빈익빈 부익부 현상 발생
- 따라서 이러한 문제를 해결하기 위해 컨텐츠 기반의 모델을 적절히 섞어서 사용하는 것이 좋음

### Neighborhood vs Latent Factor
- Neighborhood는 Item space내에 유사한 Item을 추천해 준다던지, User Space 안에서 유사한 User를 추천해 주는 방식이였다면, Latent Factor는 Item space의 Latent space와 User Space의 Latent space를 구하고, 그 두개의 곱을 통해서 계산하는 방식

### Latent Factor Collaborative Filtering 정의
- 잠재적 요인기반 추천 모델
- Rating Matrix에서 빈 공간을 채우기 위해 사용자와 상품을 잘 표현하는 차원(Latent Factor)를 찾는 방법
- 잘 알려진 행렬 분해는 추천 시스템에서 사용되는 협업 필터링 알고리즘의 한 종류
- 행렬 분해 알고리즘은 사용자-아이템 상호 작용 행렬을 두 개의 저차원 직사각형 행렬 곱으로 분해하여 작동
- Rating Matrix을 만들어내기 위해 2가지 matrix를 도입하는데, 첫 번째는 사용자 기반의 매트릭스와 두 번째는 아이템 기반의 매트릭스를 도입함
- 각각의 요인이 무엇을 의미하는지는 정확히 모르기 떄문에 잠재 기반의 협업 필터링이라고 함
- 사용자 기반의 latent matrix와 아이템 기반의 latent matrix를 곱했을 때 평점 매트릭스를 복원할 수 있다는 것

### Latent Factor Collaborative Filtering 원리
- 사용자의 잠재요인과 아이템의 잠재요인을 내적해서 평점 매트릭스를 계산
- R ~~ UV^(T)

### SGD
- 고유값 분해와 같은 행렬을 대각화하는 방법
- Minimize J = 1/2 * ||R - UV^T||^2  
  평점 매트릭스와 user latent matrix * item latent matrix 간의 차이를 최소화하려는 U, V를 찾겠다라는 것  
  딥러닝 모형이다 보니, U, V의 weight가 계속 update 됨  
- gradient 폭주를 막기 위해 regularization term을 추가

#### SGD 예시
- Explicit Feedback된 형태의 4명 유저에 대한 3개의 아이템 평점 Matrix
- 목표는 ?를 채우는 것은 user latent 와 item latent로 채우겠다는 것
~~~
Rating Matrix
?  3  2
5  1  2
4  2  1
2  ?  4
~~~
- SGD 계산 process는 다음과 같음
  - user latent와 item latent를 임의로 초기화함  
    - Rating matrix가 4x3이기 때문에 4xn, nx3으로 형성  
    - ALS 논문에서는 n을 20으로 setting 함
  - Grdent Descent를 진행
    - ?는 제외하고 나머지 값에 대해서 진행
  - 모든 평점에 대해서 반복(epoch 1)  
    - latent matrix가 계속 갱신됨
- 계산된 latent space를 통해서도 insight를 얻을 수 있음

#### SGD 장단점
- 매우 유연한 모델로 다른 Loss function 사용 가능
- parallelized 가능함
- 단점은 수렴까지 속도가 매우 느림

### ALS
- 기존의 SGD가 두 개의 행렬(User Latent, Item Latent)를 동시에 최적화하는 방법이라면 ALS는 두 행렬 중 하나를 고정시키고 다른 하나의 행렬을 순차적으로 반복하면서 최적화하는 방법
- 이렇게 하면 기존의 최적화 문제가 convex 형태로 바뀌기에 수렴된 행렬을 찾을 수 있는 장점이 있음

#### ALS 알고리즘
- 초기 아이템, 사용자 행렬을 초기화
- 아이템 행렬을 고정하고 사용자 행렬을 최적화
- 사용자 행렬을 고정하고 아이템 행렬을 최적화
- 위의 2, 3 과정을 반복

### 협업필터링 장단점
- 장점
  - 도메인 지식이 필요하지 않음
  - 사용자의 새로운 흥미를 발견하기 좋음
  - 시작단계의 모델로 선택하기 좋음(추가적인 문맥정보등의 필요가 없음)
- 단점
  - 새로운 아이템에 대해서 다루기가 힘듬(한번 더 학습 수행해야 함)
  - side features(고객의 개인정보, 아이템의 추가정보)를 포함시키기 어려움   
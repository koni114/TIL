
GAN(generative adversarial network)
실제로는 존재하지 않지만, 있을법한 데이터를 생성해내는 모델
컴퓨터가 어떻게 있을법한 데이터를 잘 만들어낼 수 있을까? 

확률분포
- 확률 변수가 특정한 값을 가질 확률을 나타내는 함수
주사위를 던져 나올 수 있는 수를 확률 변수라고 할 때, 각 사건이 나올 확률이 가지는 분포를 확률 분포라고 함

확률 분포는 이산확률분포, 연속확률분포로 나눌 수 있음
이산확률분포는 정확한 값으로 떨어질 수 있는 것들.          ex) 주사위 눈금이 나올 확률
연속확률분포는 정확한 값으로 나누어 떨어질 수 없는 것들. 즉 사건의 값이 연속적인 것들 ex) 키, 몸무게.. 등

이러한 확률 분포는 다양한 데이터를 표현할때 유의미 하게 사용됨
실제의 많은 데이터는 정규분포로 모델링 할 수 있음

이미지 또한 마찬가지로 벡터나 행렬로서 컴퓨터가 값을 가지고 있을 수 있고, 이를 다양한 확률 분포로 표현할 수 있음
이미지데이터는 다차원 특징  공간의 한 점으로 표현됨
이미지는 많은 픽셀, 3개의 채널을 가지고 있기 때문에 고차원의 한 점으로 표현될 수 있음
즉, 이미지도 고차원 점을 나타내는 확률 분포로 해당 데이터를 표현할 수 있음

사람의 얼굴에는 통계적인 평균치가 존재할 수 있음
모델은 이를 수치적으로 표현할 수 있게 됨

이미지 데이터에 대한 확률분포란, 이미지에서의 다양한 특징들의 각각의 확률 변수가 되는 분포를 말함
우리가 hidden layer에서 dimension을 2라고 설정했다면 두 개의 특징에 대한 값들이 캐치가 될 것임
예를 들어 코의 길이, 눈의 모양일 때 이 두가지 특성에 대한 확률 분포를 만들어 낼 수 있을 것임.
결과적으로 얼굴을 나타내는 이미지도 이보다 훨씬 고차원으로 표현된다는 것만 다른 것 뿐이지 결국은 이 고차원 데이터의 확률 분포를 학습하는 개념은 동일함

생성 모델(generative model)
생성 모델은 실존 하지는 않지만 있을 법한 이미지(더 크게는 데이터)를 생성할 수 있는 모델을 의미함
Discriminative model 은 decision boundary를 학습하는 형태인 반면, 생성 모델은 각각의 클래스에 대해서 적절한 분포를 학습하는 형태로 이해 가능

생성 모델은 joint probability distribution 의 통계적 모델로 표현할 수 있는 경우가 많으며
새로운 데이터 인스턴스를 만들어내는 아키텍처라고 이해할 수도 있음. 여기서 데이터 인스턴스는 예를 들어 이미지 1장을 의미함

만약 확률분포에서 확률 값이 높은 부분에서 데이터 샘플링을 한다면 굉장히 그럴싸한 이미지가 나오게 될 것이며,
낮은 부분은 덜 있음직한 데이터가 될 것임
즉, 확률 분포에서 가장 확률이 높은 부분에서부터 적절히 노이즈를 섞어가면서 샘플링을 해 간다면 굉장히 다양한 특성을 가진 있음 직한 데이터를 생성해 낼 수 있을 것임

생성 모델(generative model)의 목표
이미지 데이터의 근사하는 모델 G(generator)를 만드는 것이 생성 모델의 목표
모델 G가 잘 동작한다는 의미는 이미지들의 분포를 잘 모델링 할 수 있다는 것을 의미
  - 2014년 제안된 Generative Adversarial networks가 대표적임

모델 G는 원래 데이터의 분포를 근사할 수 있도록 학습됨
즉 시간이 지나면서 생성 모델 G가 원본 데이터의 분포를 학습함
학습이 잘 되었다면 통계적으로 평균적인 특징을 가지는 데이터를 쉽게 생성 가능

Generative Adversarial Networks(GAN)
- 생성자(generative)와 판별자(discriminator) 두 개의 네트워크를 학습
- 생성자는 우리가 나중에 학습이 된 이후에 사용하고자 하는 모델이며 판별자는 생성자가 잘 학습할 수 있도록 도와주는 네트워크

다음의 목적함수(objective function)을 통해 생성자는 이미지 분포를 학습할 수 있음

Min(G) Max(D) V(D, G) = Ex~pdata(x)[log(D(x))] + Ez~pz(z)[log(1 - D(G(z)))]

함수 V는 D와 G라는 함수로 구성되며, 이 목적함수는 G 함수는 V 함수를 작아지도록, D 함수는 V 함수를 커지도록 노력함
Pdata(x)는 원본 데이터의 distribution을 의미하며, x~pdata(x)는 이러한 원본 데이터의 distribution에서 
여러개의 데이터를 샘플링 해서 D에 넣고 log를 취하고 기대값을 취하겠다라는 의미가 왼쪽 Ex~pdata(x)[log(D(x))] 의 식

 Ez~pz(z)[log(1 - D(z))]
생성자의 개념이 포함되어 있음
생성자는 항상 노이즈 벡터로 부터 입력을 받아서 새로운 이미지를 만들어 낼 수 있음
pz(z)는 하나의 노이즈를 뽑을 수 있는 distribution이 되는 것임
마찬가지로 여러개의 노이즈 벡터를 뽑고 이를 가짜 이미지 생성을 위해 G 함수에 넣어 생성한 후 D에 넣은 값에 -를 붙이고 1를 더한 값에 log를 취하고 기댓값을 계산한 식

Generator G(z)는 하나의 노이즈 벡터 z를 받아 새로운 데이터를 만들어내는 함수이며
Discriminator D(x)는 실제 분포에서부터 온 샘플의 확률 값이며 이는 이 이미지가 얼마나 진짜 같은지에 대한 확률 값임
진짜 이미지 1, 가짜 이미지는 0으로 학습함. 출력값은 확률값으로 표현됨 

즉 다시 식을 해석해보자면
판별자는 
학습을 함에 있어서 원본 데이터에 대해서는 1로 분류할 수 있도록 학습이 되며, ( -> Ex~pdata(x)[log(D(x))])
가짜 이미지가 들어왔을 때는 0을 만들어 낼 수 있도록 학습하겠다!는 의미( Ez~pz(z)[log(1 - D(G(z)))])

생성자는
오른쪽에 해당하는 term만 사용하게되는데, 이 term을 minimize 하게 되는데, 즉 오른쪽 식을 minimize 한다는 것은
D(G(z)) 가 1이 나오게끔 하는 G를 만들어낸다는 의미이며, 이는 진짜 이미지처럼 만들어내는 G 를 학슴하겠다! 라는 의미로 해석이 가능

즉 동일한 V라는 식에서.D와 G가 다른 목적을 가지고 학습
일종의 min-max game, optimization 함수로 볼 수 있음
결과적으로 generative model은 그럴싸한 이미지를 만들어내는 모델이 될 것임을 주장

학습을 진행할 때 프로그래밍 상에서 D를 먼저 학습하고 G를 학습하거나 
G를 학습하고 D를 학습하는 식으로 진행함

미니배치마다 두개의 네트워크를 한번씩 학습하는 방법을 선택

GAN의 수렴 과정을 자세하게 확인해보자
어떻게 GAN이 목적 함수를 이용해서 잘 학습할 수 있는가를 알아보자 

공식의 목표는 생성자의 분포가 원본 학습 데이터의 분포를 잘 따를 수 있도록 만드는 것(Pg -> Pdata)
D(G(z)) -> 1/2 라는 것은 더이상 D는 가짜 이미지와 진짜 이미지를 구분할 수 없게 되는 것이 목표

위의 과정을 시간의 흐름에 따라서 표현한다면
Z 공간에서 매번 z를 샘플링해서 생성자에 넣는데 (z의 도메인에서 x의 도메인으로 매핑됨) 처음에는 생성자의 분포를 원본ㄷ ㅔ이터의 분포를 잘 학습하지
못하기 때문에 판별 모델이 이를 잘 구분할 수 있음

시간이 지남에 따라 생성 모델은 원본 데이터의 분포와 거의 비슷해서 판별 모델이 잘 구분하지 못하고 1/2로 수렴함

그렇다면 학습을 진행했을 때, 어떻게 생성자의 분포가 원본 데이터로 수렴할 수 있을까 ?

Pg -> Pdata로 수렴하는 과정의 증명
Global Optimality 
매 상황에 대해서 생성자와 판별자가 각각 어떤 포인트로 global optimal을 가지는지 설명

G가 고정된 시점에서 D의 optimal point는 Pdata(x) / (Pdata(x) + Pg(x)) 로 수렴
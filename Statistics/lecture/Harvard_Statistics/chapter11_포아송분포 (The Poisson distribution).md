# 11강- 포아송분포 (The Poisson distribution)

## 핵심 키워드
* 포아송분포(poisson distribution)  
* 포아송 근사(poisson approximation/ poisson paradigm)  
* 이산확률분포  
* Birthday Problem  


## distribution과 random variable의 차이(자주 하는 실수)

* 교수님은 distribution과 random varible를 헷갈리는 것을 sympathetic magic이라고 하심  
  * sympathetic magic : 모방 마술    
* 확률변수와 확률질량함수를 더하는 것의 차이를 알아야 함  
  * 기본적으로 PMF를 더하는 것은 의미가 없음  
  * distribution을 더한다? 의미 없음  

* P(X = x) + P(Y = y) 같은 덧셈은 하지 않음  
  * 두 개의 합이 1보다 클 수 있음  
  * 이는 공리에 의해 확률이 아님  
* random variables의 합인 X+Y는 할 수 있음. 우리는 이항 분포를 따르는 두 random variable의 합을 증명했었음  
* X^3도 할 수 있는데 중요한 것은 random variable 이 세제곱된다고 해서 PMF나 분포가 세제곱 되는 것은 아님  

<p align = "center"><b>Word is not the thing. the map is not the territory</b></p>

* random variable과 distribution을 설명하는 구절  
* 우리는 지도와 영토 자체를 헷갈리진 않는다(지도 = distribution, 영토 = random variable)  

* 더 좋은 비유는 <b>random variable은 "집" 이고 distribution은 "설계도"</b>인 것  
  * 설계도 하나를 가지고 더 좋은 '집'을 만들 수 있음  
  * 설계도는 문의 위치나 방의 구조를 얘기해주기 보다는  
특정 확률을 가지고 무작위로 문의 색을 파랑 or 빨강으로 정하는 것  
  * 설계도는 집을 지을 때 필요한 모든 확률을 알려주는 것  

## 포아송 분포(Poisson Distribution)
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?X&space;\sim&space;Pois(\lambda&space;)" title="X \sim Pois(\lambda )" /></p>

* 통계학에서 가장 중요한 분포 중 하나  
* 프랑스 수학자인 Poisson의 이름을 딴 분포  

##### (1) PMF
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=P(X&space;=&space;k)&space;=&space;\frac{e^{\lambda}&space;\dot&space;\lambda&space;^{k}}{k!}&space;,&space;k&space;=&space;0,&space;1,&space;2..." target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(X&space;=&space;k)&space;=&space;\frac{e^{\lambda}&space;\dot&space;\lambda&space;^{k}}{k!}&space;,&space;k&space;=&space;0,&space;1,&space;2..." title="P(X = k) = \frac{e^{\lambda} \dot \lambda ^{k}}{k!} , k = 0, 1, 2..." /></a></p>

* lambda 는 'rate parameter'  
* K는 음수가 아닌 정수  
* 이항분포에서는 K의 범위가 정해져 있지만, Poisson은 음수만 아니면 모든 정수 가능  
* lambda는 실제로 어떤 문자를 쓰던 상관 없음. 0보다 큰 상수  
* 왜 중요한지 알아보기 전에, PMF가 타당한지 알아보자  

##### (2) PMF의 타당성 증명
* 1. 모든 k에 대해서 PMF는 0보다 큼  
* 2. 다 더해서 1인지 계산해보자  
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?\sum_{k&space;=&space;0}^{\infty}\frac{&space;e^{-\lambda}&space;\cdot&space;\lambda^{k}}{k!}&space;=&space;e^{-\lambda}&space;\cdot&space;\sum_{k&space;=&space;0}^{\infty}&space;\frac{\cdot&space;\lambda^{k}}{k!}" title="\sum_{k = 0}^{\infty}\frac{ e^{-\lambda} \cdot \lambda^{k}}{k!} = e^{-\lambda} \cdot \sum_{k = 0}^{\infty} \frac{\cdot \lambda^{k}}{k!}" /></p>
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?\text{&space;by&space;taylor,}&space;\sum_{k&space;=&space;0}^{\infty}&space;\frac{&space;\lambda^{k}}{k!}&space;=&space;e^{\lambda}" title="\text{ by taylor,} \sum_{k = 0}^{\infty} \frac{ \lambda^{k}}{k!} = e^{\lambda}" /></p>
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?\sum_{k&space;=&space;0}^{\infty&space;}&space;\frac{&space;e^{-\lambda}\cdot&space;\lambda^{k}}{k!}&space;=&space;e^{-\lambda}\cdot&space;e^{\lambda}" title="\sum_{k = 0}^{\infty } \frac{ e^{-\lambda}\cdot \lambda^{k}}{k!} = e^{-\lambda}\cdot e^{\lambda}" /></p>
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?=&space;1" title="= 1" /></p>

##### (3) 포아송 분포를 따르는 확률 변수의 기댓값
* 기댓값은 값과 확률의 곱의 합  
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?E(X)&space;=&space;e^{-\lambda}&space;\cdot&space;\sum_{k&space;=&space;1}^{\infty}&space;\frac{k&space;\cdot&space;\lambda^{k}&space;}{k!}" title="E(X) = e^{\lambda} \cdot \sum_{k = 1}^{\infty} \frac{k \cdot \lambda^{k} }{k!}" /></p>
<p align = "center">k를 소거하면</p>
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?E(X)&space;=&space;e^{-\lambda}&space;\cdot&space;\sum_{k&space;=&space;1}^{\infty}&space;\frac{\lambda^{k}&space;}{(k-1)!}" title="E(X) = e^{\lambda} \cdot \sum_{k = 1}^{\infty} \frac{\lambda^{k} }{(k-1)!}" /></p>
<p align = "center">위의 테일러 급수 식과 비슷하게 만들어주자</p>
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?E(X)&space;=&space;\lambda\cdot&space;e^{-\lambda}&space;\cdot&space;\sum_{k&space;=&space;1}^{\infty}&space;\frac{\lambda^{k-1}&space;}{(k-1)!}" title="E(X) = \lambda\cdot e^{\lambda} \cdot \sum_{k = 1}^{\infty} \frac{\lambda^{k-1} }{(k-1)!}" /></p>
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?E(X)&space;=&space;\lambda\cdot&space;e^{-\lambda}&space;\cdot&space;e^{\lambda}" title="E(X) = \lambda\cdot e^{-\lambda} \cdot e^{\lambda}" /></p>
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?E(X)&space;=&space;\lambda" title="E(X) = \lambda" /></p>

* 평균이 lambda라는 것은 외우기 쉬움  

##### (4) 포아송이 쓰이는 예시
* 실제 Poisson은 이산형 Data의 Model로써 가장 많이 사용  
* 먼저 일반화해서 적으면, <b>수를 세는 응용</b>에서 쓰임  
  * why? k가 음수가 아닌 정수이기 때문  

* 다음과 같은 경우에 포아송 분포를 생각해 볼 수 있음(중요)  
  * 성공의 수를 세는 응용  
  * 많은 시도 필요(n의 크기가 커야 함)  
  * 각 시도에서 성공 확률은 낮아야 함(p의 크기는 작아야 함)  

* <b/>예시1 - 한시간 안에 받는 이메일의 개수</b>  
  
  * 정확히 포아송이 아닐 수도 있음. 시작점으로 한 번 해보는 것임  
  * 포아송인지, 아닌지는 직접 해보야 함  
  * 직접 이메일을 세는 것은 경험적인 문제지 수학적인 문제는 아님  
  * 왜 포아송일까?  
    * 1시간동안 나에게 이메일을 보낼 수 있는 사람은 많음(n이 큼)  
    * 주기적으로 주고 받는 사이가 아니면 특정 1시간 동안 나에게 email을 보낼 확률은 매우 작음  

* <b>예시2 - 초콜렛 칩 쿠키 안에 든 초콜릿 칩의 개수</b>  

  * 초콜렛 칩 자체는 많이 들어있지만(n이 큼), 각 쿠키의 조각에는 칩이 잘 없음(p는 작음)  

* <b>예시3  - 특정 지역에서의 1년간 지진 발생률</b>  
  
  * 중요한 것은 꼭 포아송 분포를 따르지 않을 수 있다는 점. 초기 추정으로 적절할 것으로 판단한 것  

* 실제 예시에서는 상한(upper bound)가 존재하지만, 이론에서는 무한대  
완벽한 pois는 찾기 어렵지만, 대부분에서는 꽤 적절함(추정하기 유용한 분포라는 점)  

* 이를 <b>poisson paradigm, poisson approximation </b> 라고 함  

## 포아송 근사(poisson paradigm)
<p align = "center">A1, A2, An.. 의 사건이 있을 때</p>
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?P(A_{j})&space;=&space;p_{j}&space;\begin{Bmatrix}&space;\text{n&space;is&space;large}&space;&&space;\\&space;p_{j}&space;\text{&space;is&space;small}&space;&&space;\end{Bmatrix}" title="P(A_{j}) = p_{j} \begin{Bmatrix} \text{n is large} & \\ p_{j} \text{ is small} & \end{Bmatrix}" /></p>

* 증명이 매우 어렵지만, 독립성 같은 경우 성립하면 문제를 푸는데 더 수월하지만, 약하게 dependent 하는 경우도 성립  

##### weak dependent
* A1의 실행여부가 A3에는 상관 없지만    
A1 와 A2가 실행되었을 때 A3가 실행에 영향을 미치는 경우  

* 결과적으로 위의 조건을 만족하는 경우 Aj의 발생 횟수가 pois에 근사한다고 할 수 있음  
* 지금까지 본 예제들은 독립적이고 P가 같기 때문에    
일어날 확률이 다 같은 X ~ Bern(p) 였음  

* 이 때 사건의 발생 수는 P 확률의 이항분포를 따른 다는 것을 알고 있음  
  X ~ Binomial(n, p)  

* 즉, 이항분포에서 n 이 커지고, p가 작아지면 pois(X)로 수렴하는 것을 증명할 수 있음  

## 이항분포에서 포아송으로 수렴 증명
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?X&space;~&space;Bin(n,&space;p),&space;\text{let&space;n&space;}->&space;\infty&space;,&space;p&space;->&space;0" title="X ~ Bin(n, p), \text{let n }-> \infty , p -> 0" /></p>

* 실제 응용에서는 n이 유한수이기 때문에 '근사'라는 말을 씀  
* n과 p의 극한 속도는 다를 수 있음. 그렇다면 우리는 이항분포와 포아송의 기댓값이 같다라는 것으로 자연스럽게 시작해보자  
* 이 때 기댓값이 같다고 하는 것은, lambda는 상수이므로, 자연스레 n -> 무한대, p -> 0으로 가는 속도는 동일하다는 것을 알 수 있음  

##### PMF 증명
<p align ="center"><img src="https://latex.codecogs.com/gif.latex?P(X&space;=&space;k)&space;=&space;\binom{n}{k}\cdot&space;p^{k}\cdot&space;(1-p)^{n-k}" title="P(X = k) = \binom{n}{k}\cdot p^{k}\cdot (1-p)^{n-k}" /></p>
<p align ="center">이 때 p를 n의 식으로 바꾸자</p>
<p align ="center"><img src="https://latex.codecogs.com/gif.latex?p&space;=&space;\frac{\lambda}{n}," title="p = \frac{\lambda}{n}," /></p>
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?P(X&space;=&space;k)&space;=&space;\frac{n(n-1)(n-2)&space;...&space;\cdot&space;\lambda^{k}}{k!&space;\cdot&space;n^{k}}&space;\cdot&space;(1&space;-&space;\frac{\lambda}{n})^{n}\cdot&space;(1&space;-\frac{\lambda}{n})^{k}" title="P(X = k) = \frac{n(n-1)(n-2) ... \cdot \lambda^{k}}{k! \cdot n^{k}} \cdot (1 - \frac{\lambda}{n})^{n}\cdot (1 -\frac{\lambda}{n})^{k}" /></p>
<p align ="center"><img src="https://latex.codecogs.com/gif.latex?\lim_{n&space;->&space;\infty&space;}&space;\frac{\lambda^{k}}{k!}\cdot&space;1&space;\cdot&space;e^{-\lambda}" title="\lim_{n -> \infty } \frac{\lambda^{k}}{k!}\cdot 1 \cdot e^{-\lambda}" /></p>
<p align ="center">이는 포아송 분포의 PMF 임을 알 수 있다</p>

## 떨어지는 빗방울의 수
##### Poisson 인가?
* 직사각형 종이, 수평으로 있다고 생각하자  
* 비가 오는 밖에 종이를 놔둔다  
* 1분에 빗방울이 몇 개 떨어지는지 알고 싶다  
* 직사각형에 원하는 만큼 수평, 수직선을 그린다 -> 몇천만개로 나눴다고 해보자  
* 각 사각형당 특정 시간동안 빗방울이 떨어지는 횟수를 셀 것임    
작은 사각형에 빗방울이 떨어짐. 이는 굉장히 낮을 확률  
* 큰 사각형에는 거의 떨어짐. 이 때 람다는 비가 얼마나 세게 오는지? 를 의미함  

##### 생각해보기 - 이항분포를 써야 할까?
* 모든 사각형이 맞을 빗방울이 독립적이라면, 다 같은 확률 P로 맞는다면 이항분포 써야 할 수 있음  
* 사각형의 상태가 반드시 0 or 1 둘 중에 하나여야 함  
* 이항분포가 맞다고 해도, 큰 n과 아주 작은 P의 이항분포는 어렵  
* 1000! 도 계산하기가 매우 어렵다  

## Birthday problem
* 3명의 생일이 겹치는 경우의 확률은 얼마나 되는가?  
* 근사만 구하면 된다고 생각하자(실제로 기대 값을 계산 할 수 있음)  
* 기존의 풀었던 방법으로 하려면 매우 어렵  

## poisson 근사가 적절한가?
* 일단 n은 적절히 커야 함. but 엄청 클 필요는 없음  
* n이 몇백일 필요는 없음. why? nC3 을 생각  
* n이 10의 자리 일 때 nC3은 충분히 커짐  
* 3명의 생일이 겹치는 경우는 매우 확률이 낮음  
* <b>즉, poisson 분포로 접근 가능함! </b>  

## 지시확률변수를 활용한 확률 계산
* 먼저 각 집단의 지시확률변수(indicator random variables)를 만듬  
<p align ="center"><a href="https://www.codecogs.com/eqnedit.php?latex=I_{ijk}&space;,&space;i&space;<&space;j&space;<&space;k" target="_blank"><img src="https://latex.codecogs.com/gif.latex?I_{ijk}&space;,&space;i&space;<&space;j&space;<&space;k" title="I_{ijk} , i < j < k" /></a></p>

##### 실제 기대값은 ?
* 첫번째 사람은 아무 생일이여도 상관 없고, 두번째, 세번째 사람은 첫번째 사람과 생일이 같을 확률은 1/365  
* n명중에 3명이 선택될 경우의 수 -> n C 3  
<p align ="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E&space;(triple&space;\&space;matches)&space;=&space;\binom{n}{3}\cdot&space;\frac{1}{365^{2}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E&space;(triple&space;\&space;matches)&space;=&space;\binom{n}{3}\cdot&space;\frac{1}{365^{2}}" title="E (triple \ matches) = \binom{n}{3}\cdot \frac{1}{365^{2}}" /></a></p>

##### Poisson 근사 값 구해보기
* X가 3명의 생일이 같을 경우의 수라고 하자  
* X는 완벽한 Pois 일 수 없음. -> <b> n이 무한대일 수 없기 때문 </b>  
*  3명이 같은 생일일 경우의 수가 3개의 집단의 개수보다 훨씬 작음 -> <b> P가 작음 </b>  
<p align ="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\lambda&space;=&space;\binom{n}{3}\cdot&space;\frac{1}{365^{2}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\lambda&space;=&space;\binom{n}{3}\cdot&space;\frac{1}{365^{2}}" title="\lambda = \binom{n}{3}\cdot \frac{1}{365^{2}}" /></a><p>

##### 왜 포아송 근사가 타당할까?    
* nC3은 충분히 큼 (충분히 큰 시행)  
* 각 시도당 성공 확률은 매우 작음  

* 독립성 - 완벽하지 않음  
why? I123 이면 I124가 1일 확률이 커짐  
일단 12가 같기 때문 ! (Weak dependent)

##### 포아송 PMF를 이용해서 계산하기
<p align ="center"><a href="https://www.codecogs.com/eqnedit.php?latex=P(X&space;\geq&space;1)&space;=&space;1&space;-&space;P(X&space;=&space;0)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(X&space;\geq&space;1)&space;=&space;1&space;-&space;P(X&space;=&space;0)" title="P(X \geq 1) = 1 - P(X = 0)" /></a></p>
<p align ="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;\frac{1&space;-&space;e^{-\lambda&space;\dot&space;\lambda&space;^{0}}}{0!}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;\frac{1&space;-&space;e^{-\lambda&space;\dot&space;\lambda&space;^{0}}}{0!}" title="= \frac{1 - e^{-\lambda \dot \lambda ^{0}}}{0!}" /></a></p>
<p align ="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;1&space;-&space;e^{\lambda}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;1&space;-&space;e^{\lambda}" title="= 1 - e^{\lambda}" /></a></p>

  
##### 포아송으로 생각하려면..  
* 처음에는 3명의 생일이 같을 확률 자체를 random variable로 생각하는 것이 key point이지 않나 생각한다  
* 즉, 포아송 근사로 가기 위한 핵심은 위에서 말한 3가지 인 것이다.  
  * weak dependent  
  * n은 무한대  
  * p는 0으로 수렴  
* 헷갈리기 쉽지만, 잘 생각해보면 알 수 있다는 점! 자꾸 자꾸 연습하자  

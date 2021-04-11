# 14강- 위치, 척도 및 무의식적인 통계학자의 법칙(Location, Scale, and LOTUS)

## 핵심 키워드  
* 적률(moment)  
* 정규분포  
  * 표준화  
  * 65-95-99.7% Rule  
* 이항분포    
* 포아송분포  
* 평균, 분산    
* 무의식적인 통계학자의 법칙(LOTUS)  


## 복습
* Z  ~ N(0, 1), CDF는 표현하기 어렵기 때문에  <a href="https://www.codecogs.com/eqnedit.php?latex=\Phi&space;(z)" target="_blank"><img src="https://latex.codecogs.com/png.latex?\Phi&space;(z)" title="\Phi (z)" /></a> 로 표현  
* <a href="https://www.codecogs.com/eqnedit.php?latex=E(z)&space;=&space;0,&space;Var(z)=&space;E(z^{2})&space;=&space;1" target="_blank"><img src="https://latex.codecogs.com/png.latex?E(z)&space;=&space;0,&space;Var(z)=&space;E(z^{2})&space;=&space;1" title="E(z) = 0, Var(z)= E(z^{2}) = 1" /></a>  
* E(z) : 1차적률, E(z^2) : 2차적률, E(z^3) : 3차적률  

## 정규분포의 대칭성(symmetry)
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\int_{-\infty}^{\infty}&space;\frac{1}{\sqrt{2\pi}}&space;\cdot&space;e^{\frac{-z^{2}}{2}}&space;dz&space;=&space;0" target="_blank"><img src="https://latex.codecogs.com/png.latex?\int_{-\infty}^{\infty}&space;\frac{1}{\sqrt{2\pi}}&space;\cdot&space;e^{\frac{-z^{2}}{2}}&space;dz&space;=&space;0" title="\int_{-\infty}^{\infty} \frac{1}{\sqrt{2\pi}} \cdot e^{\frac{-z^{2}}{2}} dz = 0" /></a></p>
* LOTUS에 의해  해당 식을 나타낼 수 있고, 기함수(odd function)이므로 0
* 지수가 홀수이면 똑같이 적용됨 = 3rd moment

* 대칭임을 표현하는 또다른 표현
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=-Z&space;\sim&space;N(0,&space;1)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?-Z&space;\sim&space;N(0,&space;1)" title="-Z \sim N(0, 1)" /></a></p>

* Z, -Z 둘다 표준정규분포. ~N(0, 1)를 따름 => 대칭성을 보여줌  
* 결국 r.v의 부호자체는 변하지만 분포자체는 변하지 않음  
  * 대칭임을 알아보고 계산을 시작하는 것이 유용  

## 정규분포에서 평균, 분산이 0, 1이 아닌 경우  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X&space;=&space;\mu&space;&plus;&space;\sigma&space;z,&space;\&space;\mu&space;\&space;\epsilon&space;\mathbb&space;\&space;{R}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;=&space;\mu&space;&plus;&space;\sigma&space;z,&space;\&space;\mu&space;\&space;\epsilon&space;\mathbb&space;\&space;{R}" title="X = \mu + \sigma z, \ \mu \ \epsilon \mathbb \ {R}" /></a></p>

* 상수 Mu를 더해 위치를 이동한다는 뜻  
* 밀도를 바꾸지 않고 Mu를 더해 좌우로 이동하는 것을 말함. (sigma > 0, 양수)  
* 항상 밀도함수의 넓이를 정규화 상수를 통해 넓거나 좁게 만들 수 있음  
  * <a href="https://www.codecogs.com/eqnedit.php?latex=X&space;\sim&space;N(\mu&space;,&space;\sigma&space;^{2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;\sim&space;N(\mu&space;,&space;\sigma&space;^{2})" title="X \sim N(\mu , \sigma ^{2})" /></a>

* 다른 책에서는 보통 PDF를 먼저 구함. but 표준정규분포를 알고 이를 통해 정규분포를 알면 더 쉽게 이해 가능  
  * 상수를 곱하거나 더하면 되기 때문!    

#### 기댓값
* 선형성에 의해 <a href="https://www.codecogs.com/eqnedit.php?latex=E(X)&space;=&space;\mu" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X)&space;=&space;\mu" title="E(X) = \mu" /></a>

#### 분산
* 2가지 계산 방법이 존재  
  * <a href="https://www.codecogs.com/eqnedit.php?latex=Var(X)&space;=&space;E((X&space;-&space;Ex)^{2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(X)&space;=&space;E((X&space;-&space;Ex)^{2})" title="Var(X) = E((X - Ex)^{2})" /></a>
  * <a href="https://www.codecogs.com/eqnedit.php?latex=Var(X)&space;=&space;E(x^{2})&space;-&space;Ex^{2&space;}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(X)&space;=&space;E(x^{2})&space;-&space;Ex^{2&space;}" title="Var(X) = E(x^{2}) - Ex^{2 }" /></a>

* Var(X + C) : 직관적으로 상수 하나 더한다고 퍼짐의 정도가 변하지 않음  
* Var(CX) : 위의 E((x - Ex)^2) 에서 C가 추가되었다고 생각하면 선형성에 의해 C가 C^2로 튀어나옴    
= C^2 Var(X)  

* 중요한 것은 적어도 분산이 (-)면 안됨  
* r.v가 모든 확률로 상수라면 Var(x) = 0    
나머지는 반드시 양수가 나와야 함  

* <b>중요한 것은 분산은 선형성이 아니다</b> 라는 것  
* Var(X + Y) != Var(X) + Var(Y)  
  * X,Y가 서로 independent한 경우 성립  

* 선형성이 아닌 예시  
  * Var(X + X) = Var(2X) = 4Var(X)  
  * 위의 선형성 식이 성립한다면, Var(X + X) = Var(X) + Var(X) = 2Var(X)  
  * 즉 dependent한 경우 성립 x  

* Var(2X)에서 2X = X + X로 풀 수 있는데, 이를 X1 + X로 하면 안됨  
  *  X1 + X2는 독립변수라는 얘기.  

* 즉 <b>independent와 dependent의 구분을 잘 해야 함</b>  
* Var(2X) = 4Var(X) 라는 식은 직관적으로 잘 맞음  
  * 만약 X끼리 독립적이라면 서로의 분산은 상관없기 때문에    
  더하면 되겠지만, 이는 극도로 종속적이기 때문에    
  X 하나의 분산이 커질수록 전체 분산이 극도(제곱형태)로 커짐  

<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=Var(\mu&space;&plus;&space;\sigma&space;z)&space;=&space;\sigma^{2}&space;Var(z)&space;=&space;\sigma^{2&space;}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(\mu&space;&plus;&space;\sigma&space;z)&space;=&space;\sigma^{2}&space;Var(z)&space;=&space;\sigma^{2&space;}" title="Var(\mu + \sigma z) = \sigma^{2} Var(z) = \sigma^{2 }" /></a></p>

* 정규분포가 있을 때마다 표준정규분포로 만들어 쓸 수 있다는 것  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X&space;=&space;\mu&space;&plus;&space;\sigma&space;z&space;,\&space;z&space;=&space;\frac{X&space;-&space;\mu}{\sigma&space;}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;=&space;\mu&space;&plus;&space;\sigma&space;z&space;,\&space;z&space;=&space;\frac{X&space;-&space;\mu}{\sigma&space;}" title="X = \mu + \sigma z ,\ z = \frac{X - \mu}{\sigma }" /></a></p>

*해당 변환 식을 <b>stndardization</b> 이라고 함  
  * 정규분포에서 표준정규분포로 가는 것을 말함  

## 일반정규분포의 PDF 구하기
* 그냥 공식을 아는 것은 크게 의미가 없음  
* 중요한 것은 표준정규분포의 PDF를 어떻게 활용하면 정규분포의 PDF로 쉽게 구하는지를 보고자 하는 것  
* 한 번 구해보자  
<p align="center"> 확률 변수 X가 정규분포 Mu, sigma 를 따를 때 CDF를 먼저 구하자</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=P(X&space;\leq&space;x)&space;=&space;P(\frac{X&space;-&space;\mu&space;}{\sigma}&space;\leq&space;\frac{x&space;-&space;\mu}{\sigma})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(X&space;\leq&space;x)&space;=&space;P(\frac{X&space;-&space;\mu&space;}{\sigma}&space;\leq&space;\frac{x&space;-&space;\mu}{\sigma})" title="P(X \leq x) = P(\frac{X - \mu }{\sigma} \leq \frac{x - \mu}{\sigma})" /></a></p>
<p align="center">항상 sigma는 양수이기 때문에 등호 변화는 없음</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;\Phi&space;(\frac{X&space;-&space;\mu&space;}{\sigma&space;})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;\Phi&space;(\frac{X&space;-&space;\mu&space;}{\sigma&space;})" title="= \Phi (\frac{X - \mu }{\sigma })" /></a></p>
<p align="center">chain rule을 적용하여 PDF를 구해보자</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;\frac{1}{\sigma}&space;\cdot&space;\frac{1}{\sqrt{2\pi}}&space;\cdot&space;e^{\frac{-(\frac{X&space;-&space;\mu&space;}{\sigma})^{2}}{2}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;\frac{1}{\sigma}&space;\cdot&space;\frac{1}{\sqrt{2\pi}}&space;\cdot&space;e^{\frac{-(\frac{X&space;-&space;\mu&space;}{\sigma})^{2}}{2}}" title="= \frac{1}{\sigma} \cdot \frac{1}{\sqrt{2\pi}} \cdot e^{\frac{-(\frac{X - \mu }{\sigma})^{2}}{2}}" /></a></p>

#### X -> -X로 바뀌면?  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=-X&space;=&space;-\mu&space;&plus;&space;\sigma(-z)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?-X&space;=&space;-\mu&space;&plus;&space;\sigma(-z)" title="-X = -\mu + \sigma(-z)" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;~&space;N(-\mu&space;,&space;\sigma^{2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;~&space;N(-\mu&space;,&space;\sigma^{2})" title="= ~ N(-\mu , \sigma^{2})" /></a></p>

* 직관적으로 (-)를 붙인다는 것은 평균은 (-)가 붙고, 분산은 음수가 될 수 없으니 그대로!  

#### M1 + M2?
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X_{j}&space;\sim&space;N(M_{j},&space;\sigma&space;_{j}^{2}),&space;\&space;indep" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X_{j}&space;\sim&space;N(M_{j},&space;\sigma&space;_{j}^{2}),&space;\&space;indep" title="X_{j} \sim N(M_{j}, \sigma _{j}^{2}), \ indep" /></a></p>
<p align="center">j가 1부터 2일 때,</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X_{1}&space;&plus;X_{2}&space;\sim&space;N(\mu_{1}&space;&plus;&space;\mu_{2},&space;\&space;\sigma_{1}^{2}&space;&plus;&space;\sigma_{2}^{2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X_{1}&space;&plus;X_{2}&space;\sim&space;N(\mu_{1}&space;&plus;&space;\mu_{2},&space;\&space;\sigma_{1}^{2}&space;&plus;&space;\sigma_{2}^{2})" title="X_{1} +X_{2} \sim N(\mu_{1} + \mu_{2}, \ \sigma_{1}^{2} + \sigma_{2}^{2})" /></a></p>
<p align="center">분산 값에 주의하자</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X_{1}&space;-&space;X_{2}&space;\sim&space;N(\mu_{1}&space;-&space;\mu_{2},&space;\&space;\sigma_{1}^{2}&space;&plus;&space;\sigma_{2}^{2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X_{1}&space;-&space;X_{2}&space;\sim&space;N(\mu_{1}&space;-&space;\mu_{2},&space;\&space;\sigma_{1}^{2}&space;&plus;&space;\sigma_{2}^{2})" title="X_{1} - X_{2} \sim N(\mu_{1} - \mu_{2}, \ \sigma_{1}^{2} + \sigma_{2}^{2})" /></a></p>
<p align="center">실수를 많이 하는데, -X2 라는 값을 더하는 것이기 때문에</p>
<p align="center">분산을 각각 더해준다고 생각하자</p>

##68 - 95 - 99.7 % Rule

* 세 숫자가 단순히 평균으로부터의 거리를 표준편차로 나타내었을 때    
정규분포 확률변수가 그 거리 안에 있을 확률을 나타내는 숫자  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X&space;\sim&space;N(\mu&space;,&space;\sigma^{2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;\sim&space;N(\mu&space;,&space;\sigma^{2})" title="X \sim N(\mu , \sigma^{2})" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=P(|X&space;-&space;\mu&space;|&space;\leq&space;\sigma)&space;\approx&space;0.68" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(|X&space;-&space;\mu&space;|&space;\leq&space;\sigma)&space;\approx&space;0.68" title="P(|X - \mu | \leq \sigma) \approx 0.68" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=P(|X&space;-&space;\mu&space;|&space;\leq&space;2\sigma)&space;\approx&space;0.95" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(|X&space;-&space;\mu&space;|&space;\leq&space;2\sigma)&space;\approx&space;0.95" title="P(|X - \mu | \leq 2\sigma) \approx 0.95" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=P(|X&space;-&space;\mu&space;|&space;\leq&space;3\sigma)&space;\approx&space;0.997" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(|X&space;-&space;\mu&space;|&space;\leq&space;3\sigma)&space;\approx&space;0.997" title="P(|X - \mu | \leq 3\sigma) \approx 0.997" /></a></p>

* 위의 문장들을 Phi 로 바꿀 수 있음  

## Poisson의 분산 구하기  
* 이를 통해 LOTUS가 성립하는지 직관적으로나마 이해할 수 있음  
#### Poisson을 통한 LOTUS의 직관적 이해  
<p align="center">r.v가 하나 있다고 하자(일반적인..)</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X&space;:&space;0,&space;1,&space;2,&space;3&space;\dots" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;:&space;0,&space;1,&space;2,&space;3&space;\dots" title="X : 0, 1, 2, 3 \dots" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=P&space;:&space;P_{0},&space;P_{1},&space;P_{2},&space;\dots" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P&space;:&space;P_{0},&space;P_{1},&space;P_{2},&space;\dots" title="P : P_{0}, P_{1}, P_{2}, \dots" /></a></p>
<p align="center">분산을 구하기 위해서는 X^2를 구해야 함</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X^{2}&space;:&space;0^{2},&space;1^{2},&space;2^{2},&space;\dots" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X^{2}&space;:&space;0^{2},&space;1^{2},&space;2^{2},&space;\dots" title="X^{2} : 0^{2}, 1^{2}, 2^{2}, \dots" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(X)&space;:&space;\sum_{x}^{&space;}&space;x&space;\cdot&space;P(X&space;=&space;x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X)&space;:&space;\sum_{x}^{&space;}&space;x&space;\cdot&space;P(X&space;=&space;x)" title="E(X) : \sum_{x}^{ } x \cdot P(X = x)" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(X^{2})&space;:&space;\sum_{x}^{&space;}&space;x^{2}P(X&space;=&space;x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X^{2})&space;:&space;\sum_{x}^{&space;}&space;x^{2}P(X&space;=&space;x)" title="E(X^{2}) : \sum_{x}^{ } x^{2}P(X = x)" /></a></p>
<p align="center">1^2, 2^2, 3^2 과 같은 확률 변수가 나올 확률은 그대로 p1, p2, p3 같은 확률</p>
<p align="center">이러한 CASE에서 LOTUS를 직관적으로 이해 가능</p>
<p align="center">까다로운 점은 이런 함수가 1:1이 아닌 경우</p>
<p align="center">앞선 직관으로 이해하기가 어렵다</p>
<p align="center">예를 들어</p>
<p align="center">(-1)^2 = 1, (-2)^2 = 4 ... 똑같은 결과가 나올 수 있음</p>
<p align="center">But LOTUS는 어떤 복잡한 함수여도 이러한 방법이 가능</p>

#### Poisson의 분산 계산하기
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X&space;\sim&space;Pois(\lambda&space;)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;\sim&space;Pois(\lambda&space;)" title="X \sim Pois(\lambda )" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(X^{2})&space;=&space;\sum_{k&space;=&space;0}^{\infty}&space;K^{2}&space;\cdot\frac{&space;e^{-\lambda&space;}\cdot&space;\lambda^{k}}{k!}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X^{2})&space;=&space;\sum_{k&space;=&space;0}^{\infty}&space;K^{2}&space;\cdot\frac{&space;e^{-\lambda&space;}\cdot&space;\lambda^{k}}{k!}" title="E(X^{2}) = \sum_{k = 0}^{\infty} K^{2} \cdot\frac{ e^{-\lambda }\cdot \lambda^{k}}{k!}" /></a></p>
<p align="center">위의 식은 흔히 쓰지 않는 수열의 합</p>
<p align="center">e^x의 테일러 급수를 이용하자</p>
<p align="center">중요한 것은 테일러의 급수식 자체로 k^2 형태가 나와야 함</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{k&space;=&space;0}^{\infty&space;}&space;\frac{\lambda&space;^{k}}{k!}&space;=&space;e^{\lambda}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{k&space;=&space;0}^{\infty&space;}&space;\frac{\lambda&space;^{k}}{k!}&space;=&space;e^{\lambda}" title="\sum_{k = 0}^{\infty } \frac{\lambda ^{k}}{k!} = e^{\lambda}" /></a></p>
<p align="center">람다로 양변 미분하면, </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;\frac{\lambda&space;^{k-1}}{k!}&space;=&space;e^{\lambda}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;\frac{\lambda&space;^{k-1}}{k!}&space;=&space;e^{\lambda}" title="\sum_{k = 0}^{\infty } k \cdot \frac{\lambda ^{k-1}}{k!} = e^{\lambda}" /></a></p>
<p align="center">다시 람다를 곱하면, </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;\frac{\lambda&space;^{k}}{k!}&space;=&space;\lambda&space;\cdot&space;e^{\lambda}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;\frac{\lambda&space;^{k}}{k!}&space;=&space;\lambda&space;\cdot&space;e^{\lambda}" title="\sum_{k = 0}^{\infty } k \cdot \frac{\lambda ^{k}}{k!} = \lambda \cdot e^{\lambda}" /></a></p>
<p align="center">다시 미분하면, </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{k&space;=&space;0}^{\infty&space;}&space;k^{2}&space;\cdot&space;\frac{\lambda&space;^{k-1}}{k!}&space;=&space;e^{\lambda}&space;\cdot&space;\lambda&space;&plus;&space;e^{\lambda}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{k&space;=&space;0}^{\infty&space;}&space;k^{2}&space;\cdot&space;\frac{\lambda&space;^{k-1}}{k!}&space;=&space;e^{\lambda}&space;\cdot&space;\lambda&space;&plus;&space;e^{\lambda}" title="\sum_{k = 0}^{\infty } k^{2} \cdot \frac{\lambda ^{k-1}}{k!} = e^{\lambda} \cdot \lambda + e^{\lambda}" /></a></p>
<p align="center">다시 람다를 곱하면</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{k&space;=&space;0}^{\infty&space;}&space;k^{2}&space;\cdot&space;\frac{\lambda&space;^{k}}{k!}&space;=&space;e^{\lambda}&space;\cdot&space;\lambda^{2}&plus;&space;e^{\lambda}&space;\cdot&space;\lambda" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{k&space;=&space;0}^{\infty&space;}&space;k^{2}&space;\cdot&space;\frac{\lambda&space;^{k}}{k!}&space;=&space;e^{\lambda}&space;\cdot&space;\lambda^{2}&plus;&space;e^{\lambda}&space;\cdot&space;\lambda" title="\sum_{k = 0}^{\infty } k^{2} \cdot \frac{\lambda ^{k}}{k!} = e^{\lambda} \cdot \lambda^{2}+ e^{\lambda} \cdot \lambda" /></a></p>
<p align="center">e^(-lambda)를 곱하면, </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{k&space;=&space;1}^{\infty&space;}&space;k^{2}&space;\cdot&space;\frac{\lambda&space;^{k}&space;\cdot&space;e^{-\lambda}}{k!}&space;=&space;e^{-\lambda}&space;\cdot&space;e^{\lambda}&space;\cdot&space;\lambda^{2}&plus;&space;e^{-\lambda}&space;\cdot&space;e^{\lambda}&space;\cdot&space;\lambda" target="_blank"><img src="https://latex.codecogs.com/
gif.latex?\sum_{k&space;=&space;1}^{\infty&space;}&space;k^{2}&space;\cdot&space;\frac{\lambda&space;^{k}&space;\cdot&space;e^{-\lambda}}{k!}&space;=&space;e^{-\lambda}&space;\cdot&space;e^{\lambda}&space;\cdot&space;\lambda^{2}&plus;&space;e^{-\lambda}&space;\cdot&space;e^{\lambda}&space;\cdot&space;\lambda" title="\sum_{k = 1}^{\infty } k^{2} \cdot \frac{\lambda ^{k} \cdot e^{-\lambda}}{k!} = e^{-\lambda} \cdot e^{\lambda} \cdot \lambda^{2}+ e^{-\lambda} \cdot e^{\lambda} \cdot \lambda" /></a></p>
<p align="center"><p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;\lambda(\lambda&space;&plus;&space;1)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;\lambda(\lambda&space;&plus;&space;1)" title="= \lambda(\lambda + 1)" /></a></p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Var(X)=&space;(\lambda^{2}&space;&plus;&space;\lambda)&space;-&space;\lambda^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(X)=&space;(\lambda^{2}&space;&plus;&space;\lambda)&space;-&space;\lambda^{2}" title="Var(X)= (\lambda^{2} + \lambda) - \lambda^{2}" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;\lambda" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;\lambda" title="= \lambda" /></a></p>
<p align = 'center'>포아송은 평균도 람다, 분산도 람다!</p>
<p align = 'center'>포아송은 단위가 없음. 표준정규분포도 마찬가지</p>

## 이항분포의 분산 구하기  
* 총 3가지 방법이 있음  

#### 가장 쉬운 방법  
* 두 독립변수의 합의 분산은 두 분산의 합임을 구함  
  *  아직 증명이 안되었으므로 생략  
* 이항분포는 서로 독립적인 베르누이 분포를 따르므로 저 방법 이용 가능  
  *  즉 <b>Bern(p)의 분산 x n</b> 이면 됨  

#### 두번 째 방법  
* 지시확률변수를 이용해서 구할 수 있다  
<p align = 'center'>X를 베르누이 확률변수 P에 대한 독립항등분포의 합으로 나타내자</p>  
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=X&space;=&space;I_{1}&space;&plus;&space;I_{2}&space;&plus;&space;I_{3}&space;&plus;&space;I_{4}&space;...&space;&plus;&space;I_{n}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;=&space;I_{1}&space;&plus;&space;I_{2}&space;&plus;&space;I_{3}&space;&plus;&space;I_{4}&space;...&space;&plus;&space;I_{n}" title="X = I_{1} + I_{2} + I_{3} + I_{4} ... + I_{n}" /></a></p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=X^{2}&space;=&space;I_{1}^{2}&space;&plus;&space;I_{2}^{2}&space;&plus;&space;I_{3}^{2}&space;&plus;&space;I_{4}^{2}&space;...&space;&plus;&space;I_{n}^{2}&space;&plus;&space;2I_{1}I_{2}&space;&plus;&space;2I_{2}I_{3}&space;&plus;&space;...&space;2I_{n-1}I_{n}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X^{2}&space;=&space;I_{1}^{2}&space;&plus;&space;I_{2}^{2}&space;&plus;&space;I_{3}^{2}&space;&plus;&space;I_{4}^{2}&space;...&space;&plus;&space;I_{n}^{2}&space;&plus;&space;2I_{1}I_{2}&space;&plus;&space;2I_{2}I_{3}&space;&plus;&space;...&space;2I_{n-1}I_{n}" title="X^{2} = I_{1}^{2} + I_{2}^{2} + I_{3}^{2} + I_{4}^{2} ... + I_{n}^{2} + 2I_{1}I_{2} + 2I_{2}I_{3} + ... 2I_{n-1}I_{n}" /></a></p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=E(X^{2})&space;=&space;n&space;\cdot&space;E(I_{1}^{2})&space;&plus;&space;2&space;\cdot&space;\binom{n}{2}&space;E(I_{1},&space;I_{2}&space;)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X^{2})&space;=&space;n&space;\cdot&space;E(I_{1}^{2})&space;&plus;&space;2&space;\cdot&space;\binom{n}{2}&space;E(I_{1},&space;I_{2}&space;)" title="E(X^{2}) = n \cdot E(I_{1}^{2}) + 2 \cdot \binom{n}{2} E(I_{1}, I_{2} )" /></a></p>
<p align = 'center'>I1은 0또는 1의 값을 가짐</p>
<p align = 'center'>I1^2 = I1이고</p>
<p align = 'center'>E(I1) = p </p>
<p align = 'center'>I1, I2는 지시확률변수의 곱셈
<p align = 'center'>이는 새로운 지시확률변수</p>
<p align = 'center'>첫번째와 두번째가 모두 성공했는지 나타내는 지시자</p>
<p align = 'center'>E(I1, I2) = p^2 </p>
<p align = 'center'> 따라서 해당 값을 대입하면, </p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=E(X^{2})&space;=&space;np&space;&plus;&space;n(n-1)p^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X^{2})&space;=&space;np&space;&plus;&space;n(n-1)p^{2}" title="E(X^{2}) = np + n(n-1)p^{2}" /></a></p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=E(X^{2})&space;=&space;np&space;&plus;&space;n^{2}p^{2}&space;-&space;np^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X^{2})&space;=&space;np&space;&plus;&space;n^{2}p^{2}&space;-&space;np^{2}" title="E(X^{2}) = np + n^{2}p^{2} - np^{2}" /></a></p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Var(X)&space;=&space;np&space;-&space;np^{2}&space;np(1-&space;p)&space;=&space;npq" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(X)&space;=&space;np&space;-&space;np^{2}&space;np(1-&space;p)&space;=&space;npq" title="Var(X) = np - np^{2} np(1- p) = npq" /></a></p>

## why is LOTUS is True ?
* 이산확률변수일 때  LOTUS를 증명해보자  
* 연속일때와 크게 다르지 않음. sigma -> integral로 변하는 정도  

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=E(g(x))&space;=&space;\sum_{x}^{&space;}g(x)P(X&space;=&space;x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(g(x))&space;=&space;\sum_{x}^{&space;}g(x)P(X&space;=&space;x)" title="E(g(x)) = \sum_{x}^{ }g(x)P(X = x)" /></a></p>
<p align = 'center'>선형성을 증명할 때 사용한 항등식을 다시 생각해보자</p>
<p align = 'center'>합을 계산할 때, 두 가지로 생각할 수 있음</p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=g(x)P(X&space;=&space;x)&space;=&space;\sum_{s&space;\epsilon&space;S}^{&space;}g(X(s))P({&space;s&space;}&space;)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?g(x)P(X&space;=&space;x)&space;=&space;\sum_{s&space;\epsilon&space;S}^{&space;}g(X(s))P({&space;s&space;}&space;)" title="g(x)P(X = x) = \sum_{s \epsilon S}^{ }g(X(s))P({ s } )" /></a></p>
<p align = 'center'>좌변은 grouped, 우변은 ungrouped 식 임을 상기하자</p>
<p align = 'center'>대수적으로 계산하고 싶으면, 이중합(double sum)을 가지고 할 수 있음</p>
<p align = 'center'>우변 식을 이중합을 사용해서 나타내면, </p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex==&space;\sum_{x}^{&space;}\sum_{s&space;:X(S)&space;=&space;x}^{&space;}g(X(s))P({&space;s&space;}&space;)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;\sum_{x}^{&space;}\sum_{s&space;:X(S)&space;=&space;x}^{&space;}g(X(s))P({&space;s&space;}&space;)" title="= \sum_{x}^{ }\sum_{s :X(S) = x}^{ }g(X(s))P({ s } )" /></a></p>
<p align = 'center'>위의 식은 먼저 X에 대한 합을 생각하고</p>
<p align = 'center'>X에 대한 각 합에 대해서 전체 자갈들의 합을 구하는 것으로 생각할 수 있다</p>
<p align = 'center'>안쪽 합에서 X(s) = X 이므로 </p>
<p align = 'center'>X(s) = X로 치환되고 </p>
<p align = 'center'>중요한 것은 g(x)는 S와는 무관하므로 </p>
<p align = 'center'> 밖으로 뺄 수 있음 </p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex==&space;\sum_{x&space;}^{&space;}g(x)\sum_{s:X(s)&space;=&space;x}^{&space;}&space;P(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;\sum_{x&space;}^{&space;}g(x)\sum_{s:X(s)&space;=&space;x}^{&space;}&space;P(s)" title="= \sum_{x }^{ }g(x)\sum_{s:X(s) = x}^{ } P(s)" /></a></p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex==&space;\sum_{x&space;}^{&space;}g(x)P(X&space;=&space;x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;\sum_{x&space;}^{&space;}g(x)P(X&space;=&space;x)" title="= \sum_{x }^{ }g(x)P(X = x)" /></a></p>

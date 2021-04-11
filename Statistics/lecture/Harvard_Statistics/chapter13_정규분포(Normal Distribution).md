# 13강- 정규분포 (Normal Distribution)

## 핵심 키워드
* 균등분포(Uniform Distribution)  
* 균등분포의 보편성, 대칭성, 선형변환  
* 독립  
* 정규분포(Normal Distribution)  
* 표준정규분포(Standard Normal Distribution)  

## Universality of Uniform Distribution
* F가 연속이고 강한 증가인 CDF  
* 확률 변수가 아닌 CDF에서부터 시작. 더 큰 범위에서 일반화 할 수 있지만, 쉽게 접근하기 위해서 가정  
* X = F-1(U)이고, U가 0에서 1까지의 균등분포이면 X의 CDF는 F가 됨  
* 즉 이론상으로는 0부터 1까지의 균등분포를 가지는 학률변수로 우리가 원하는 어떠한 형태의 분포를 가지는 X를 얻을 수 있음  
  * simulation 할 때 쓰임  

* F의 분포를 가진 제비뽑기를 모의로 실행할 때,  
다른 연속분포보다 만들기 쉬운 U를 이용해서 F의 역함수를 구하고 넣으면 됨  
* 대부분 F의 역함수를 찾는 것은 어려움  
* 사실 X = F-1(u) 라는 것이 CDF가 3가지 특징을 가지는 이유  

### 직관을 주는 예시
* 만약 r.v X가 F의 분포를 가질 때, F(x)를 계산하면 F(x) ~ unif(0, 1)가 나옴  
  * 확률 변수 X를 자기 자신의 누적분포에 넣음  
  * X라는 random variable가 있고 random variable의 함수도 r.v 라고 했음  
  * 즉 F도 r.v의 함수이기 때문에 F도 r.v와 일맥상통함  
    * 이 정리에 따르면 F는 ~unif(0.1)를 따름  

* 표기법에 주의  
  * CDF는 X가 x 이하일 확률. 만약 CDF에 x <- X를 집어넣으면 P(X <= X)가 되므로,  
  1이됨. 이는 잘못된 것임  
  * 그냥 CDF에 X를 넣으라는 의미. P(X <= X)가 아니라!  
  * Ex) F(x) = 1 - e^(-x), x > 0 여기 x에 X를 대입하라는 말    
  단순히 표기법의 문제임  

* 기본 개념은 X가 아주 복잡하거나 모르는 분포를 가질 때, 모델을 시험하고 싶을 때   
간단한 균등분포로 변경 가능하다는 것  
  * 여러가지를 해보고 균등분포가 아니라면 Model이 틀렸다는 것을 알 수 있음  

### Simulation 예시
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=Let&space;F(x)&space;=&space;1&space;-&space;e^{-x},&space;\&space;x&space;>&space;0&space;\&space;(Expo(1))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Let&space;F(x)&space;=&space;1&space;-&space;e^{-x},&space;\&space;x&space;>&space;0&space;\&space;(Expo(1))" title="Let F(x) = 1 - e^{-x}, \ x > 0 \ (Expo(1))" /></a></p>  

* 모수 1을 가지는 지수분포  
* U가 0에서 1까지의 균등분포를 가지고 있을 때(U ~ unif(0, 1))   
F(x)의 분포를 모의로 실행하고 싶음  
* X가 F의 분포를 가지는 시뮬레이션을 하고 싶음  
* 우리가 해야할 것은 F의 역함수를 찾고,   
0 ~ 1인 균등분포의 r.v 를 넣으면 우리가 원하는 F 분포를 가지게 됨  
 <p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=F^{-1}(u)&space;=&space;-ln(1-u)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?F^{-1}(u)&space;=&space;-ln(1-u)" title="F^{-1}(u) = -ln(1-u)" /></a></p>

* 컴퓨터로 10번의 제비뽑기를 하면 10개의 독립적이고 똑같은 균등분포를 만들게 되고,  
이를 -ln(1-U)에 대입하면 이 분포(1 - e^(-x)) 에서 독립적이고 똑같은 10번의 제비뽑기를 하게 됨  

### symmetry of uniform
* 1-U도 0 ~ 1까지의 균등분포  
* 만약 a,b가 상수인 a + bu가 있을 때, 이 값도 어느구간에서의 uniform 분포  
  *  0 ~ 1 x 10 -> 0 ~ 10 이런식  

* a + bu 처럼 선형과 달리 비선형 변환은 균등하기 않은 결과를 갖음  
* U^2이 0과 1 사이에 있다고해서 균등분포라 단정지으면 안됨    
CDF를 확인해야함  

## 다시 독립성  
* 이번에는 r.v 간의 독립성을 알아보자  
 <p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X_{1},&space;X_{2},&space;...&space;X_{n}&space;\&space;indep&space;\&space;if&space;\&space;P(X_{1}&space;\leq&space;x_{1},&space;X_{2}&space;\leq&space;x_{2},&space;...&space;,&space;X_{n}&space;\leq&space;x_{n})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X_{1},&space;X_{2},&space;...&space;X_{n}&space;\&space;indep&space;\&space;if&space;\&space;P(X_{1}&space;\leq&space;x_{1},&space;X_{2}&space;\leq&space;x_{2},&space;...&space;,&space;X_{n}&space;\leq&space;x_{n})" title="X_{1}, X_{2}, ... X_{n} \ indep \ if \ P(X_{1} \leq x_{1}, X_{2} \leq x_{2}, ... , X_{n} \leq x_{n})" /></a></p>

 * 하나의 사건이고, n가지 사건이 교차로 일어나는 것임  
 * 직관적으로 독립성을 적용하면 각 사건 확률의 곱  
  <p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=P(X_{1}&space;\leq&space;x_{1},&space;X_{2}&space;\leq&space;x_{2},&space;...&space;,&space;X_{n}&space;\leq&space;x_{n})&space;=&space;\\&space;P(X_{1}&space;\leq&space;x_{1})&space;\cdot&space;P(X_{2}&space;\leq&space;x_{2})&space;\cdot&space;P(X_{n}&space;\leq&space;x_{n})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(X_{1}&space;\leq&space;x_{1},&space;X_{2}&space;\leq&space;x_{2},&space;...&space;,&space;X_{n}&space;\leq&space;x_{n})&space;=&space;\\&space;P(X_{1}&space;\leq&space;x_{1})&space;\cdot&space;P(X_{2}&space;\leq&space;x_{2})&space;\cdot&space;P(X_{n}&space;\leq&space;x_{n})" title="P(X_{1} \leq x_{1}, X_{2} \leq x_{2}, ... , X_{n} \leq x_{n}) = \\ P(X_{1} \leq x_{1}) \cdot P(X_{2} \leq x_{2}) \cdot P(X_{n} \leq x_{n})" /></a></p>

* 좌변 식은 joint CDF가 됨  
여러가지 확률변수의 CDF가 한 확률을 계산하기 위해 공동으로 적용되기 때문  
* 우변 식은 CDF를 각각 따로 적음   
모든 x1, ... xn에 성립함  
이게 성립되면 확률변수가 독립적이라고 정의  
이것이 <b>일반적인 r.v의 독립성의 정의</b>  

#### 이산분포의 경우
  <p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=P(X_{1}&space;=&space;x,&space;X_{2}&space;=&space;x,&space;X_{3}&space;=&space;x,&space;...&space;X_{n}&space;=&space;x)&space;\\&space;=&space;P(X_{1}&space;=&space;x)&space;\cdot&space;P(X_{2}&space;=&space;x)&space;...&space;P(X_{n}&space;=&space;x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(X_{1}&space;=&space;x,&space;X_{2}&space;=&space;x,&space;X_{3}&space;=&space;x,&space;...&space;X_{n}&space;=&space;x)&space;\\&space;=&space;P(X_{1}&space;=&space;x)&space;\cdot&space;P(X_{2}&space;=&space;x)&space;...&space;P(X_{n}&space;=&space;x)" title="P(X_{1} = x, X_{2} = x, X_{3} = x, ... X_{n} = x) \\ = P(X_{1} = x) \cdot P(X_{2} = x) ... P(X_{n} = x)" /></a></p>

* CDF와 PDF를 통한 독립성 정의식이 같은 의미  
* 이를 full independent라고 부르는데, 쌍의 독립성이 아닌 어떤 확률 변수 조합의  
사건 실행 여부를 알아도 나머지에 대해 아무것도 모르는 것  

#### 쌍(Pair) 독립성은 되고 완전(Full) 독립성은 안되는 경우 - 예제
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=Ex)&space;X_{1},&space;X_{2}&space;\sim&space;Bern(p),&space;i.i.d" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Ex)&space;X_{1},&space;X_{2}&space;\sim&space;Bern(p),&space;i.i.d" title="Ex) X_{1}, X_{2} \sim Bern(p), i.i.d" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X_{3}&space;=&space;\left\{\begin{matrix}&space;1&space;\&space;if&space;\&space;X_{1}&space;=&space;X_{2}&space;&&space;\\&space;0&space;\&space;if&space;\&space;X_{1}&space;\neq&space;X_{2}&space;&&space;\end{matrix}\right." target="_blank"><img src="https://latex.codecogs.com/gif.latex?X_{3}&space;=&space;\left\{\begin{matrix}&space;1&space;\&space;if&space;\&space;X_{1}&space;=&space;X_{2}&space;&&space;\\&space;0&space;\&space;if&space;\&space;X_{1}&space;\neq&space;X_{2}&space;&&space;\end{matrix}\right." title="X_{3} = \left\{\begin{matrix} 1 \ if \ X_{1} = X_{2} & \\ 0 \ if \ X_{1} \neq X_{2} & \end{matrix}\right." /></a></p>

* X1, X2, X3의 각각 pair는 독립이지만,  Full independent는 아님.  
* why? X1, X2를 알면 X3는 자동으로 결정되기 때문(Full independent 성립 X)  
* but X1을 안다고 X3을 아는것에 아무것도 도움이 되지 않음(Pair independent 성립)  

## 정규 분포(Normal Distribution)
* 가우시안 분포라고도 부름  
* 가우시안이 처음 쓴게 아님. 다른데서 가우시안이라고 부르면 같은 것임  
* 정규분포는 통계학에서 가장 유명한 distribution  
  * 이유1 : central limit theorem    
  확률에서 가장 유명하고 중요한 정리    
  여러 개의 독립적이고 동일한 확률변수를 더했을 때   
  그 합의 분포가 "정규분포" 를 따라 갈 것이라는 의미    
  어떤 확률변수이든 더하면 정규분포를 따른 다는 것!  

### 표준정규분포
* N(0,1) 평균이 0, 분산이 1 이라는 의미  
* 평균과 분산 두 모수를 가짐  

#### PDF
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=f(z)&space;=&space;C&space;\cdot&space;e^{-(\frac{z^{2}}{2})}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f(z)&space;=&space;C&space;\cdot&space;e^{-(\frac{z^{2}}{2})}" title="f(z) = C \cdot e^{-(\frac{z^{2}}{2})}" /></a></p>

* 표준정규분포인 경우, 관습적으로 z를 씀  
* 미분을 통해 1차도함수, 2차도함수를 통해 그래프를 그려보면  
  종모양의 그래프가 나올 것임  
* 앞의 C는 정규화상수  
  * 이 상수는 그래프의 넓이가 1이 되도록 맞쳐줌  
* Z 를 -Z로 치환해도 같은 값이 나오기 때문에 대칭성을 가짐  
* Z의 제곱에다가 지수함수이므로 0으로 빨리 간다는 것을 알 수 있음  
* 먼저 정규화 상수인 C를 구해보자  

#### 정규화 상수 구하기
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\int_{-\infty}^{\infty}&space;e^{\frac{-z^{2}}{2}}&space;dz" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\int_{-\infty}^{\infty}&space;e^{\frac{-z^{2}}{2}}&space;dz" title="\int_{-\infty}^{\infty} e^{\frac{-z^{2}}{2}} dz" /></a></p>
<p align="center">이 식이 부정적분으로 적분하는게 불가능하다는 정리가 있음</p>
<p align="center">부정적분을 시도할 이유가 없음</p>
<p align="center">but 정적분을 이용해서 풀 수 있음</p>
<p align="center">이걸 테일러 급수로 쓴 후 도함수를 찾는 걸로 하는게 아니라</p>
<p align="center">e^x의 테일러 급수에 X대신 -Z^2/2를 넣음</p>
<p align="center">무한 급수의 각 항을 적분한게 이 적분을 대신할 수 있는 걸</p>
<p align="center">보일 수 있음</p>
<p align="center">하지만 여전히 무한급수. 이 적분이 가능하다고 했을 때</p>
<p align="center">초등함수(지수, 로그, .... 우리가 평소에 접하던 함수) 유한합인 닫힌 상태로는 못함</p>
<p align="center">그렇다면 넓이는 어떻게 구할까?</p>
<p align="center">똑같은 값을 한 번더 곱하는 방법을 이용</p>
<p align="center">두 개의 적분함수를 구하기 위해 z -> x, y 로 변환</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\int_{-\infty}^{\infty}&space;e^{\frac{-z^{2}}{2}}&space;dz&space;\cdot&space;\int_{-\infty}^{\infty}&space;e^{\frac{-z^{2}}{2}}&space;dz&space;=&space;\int_{-\infty}^{\infty}&space;e^{\frac{-x^{2}}{2}}&space;dx&space;\cdot&space;\int_{-\infty}^{\infty}&space;e^{\frac{-y^{2}}{2}}&space;dy" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\int_{-\infty}^{\infty}&space;e^{\frac{-z^{2}}{2}}&space;dz&space;\cdot&space;\int_{-\infty}^{\infty}&space;e^{\frac{-z^{2}}{2}}&space;dz&space;=&space;\int_{-\infty}^{\infty}&space;e^{\frac{-x^{2}}{2}}&space;dx&space;\cdot&space;\int_{-\infty}^{\infty}&space;e^{\frac{-y^{2}}{2}}&space;dy" title="\int_{-\infty}^{\infty} e^{\frac{-z^{2}}{2}} dz \cdot \int_{-\infty}^{\infty} e^{\frac{-z^{2}}{2}} dz = \int_{-\infty}^{\infty} e^{\frac{-x^{2}}{2}} dx \cdot \int_{-\infty}^{\infty} e^{\frac{-y^{2}}{2}} dy" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\int_{-\infty}^{\infty}&space;\int_{-\infty}^{\infty}&space;e^{\frac{-(x^{2}&space;&plus;&space;y^{2})}{2}}&space;dx&space;dy" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\int_{-\infty}^{\infty}&space;\int_{-\infty}^{\infty}&space;e^{\frac{-(x^{2}&space;&plus;&space;y^{2})}{2}}&space;dx&space;dy" title="\int_{-\infty}^{\infty} \int_{-\infty}^{\infty} e^{\frac{-(x^{2} + y^{2})}{2}} dx dy" /></a></p>
<p align="center">이를 x,y에서 r, theta(극좌표계)로 변경해보자 </p>
<p align="center">피타고라스 정리가 생각나야 하는데,</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=r^{2}&space;=&space;x^{2}&space;&plus;&space;y^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?r^{2}&space;=&space;x^{2}&space;&plus;&space;y^{2}" title="r^{2} = x^{2} + y^{2}" /></a></p>
<p align="center">를 응용하면 된다</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\int_{0}^{2\pi}&space;\int_{0}^{\infty&space;}&space;e^{\frac{r^{2}}{2}}&space;\cdot&space;r&space;\&space;dr&space;\&space;d\Theta" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\int_{0}^{2\pi}&space;\int_{0}^{\infty&space;}&space;e^{\frac{r^{2}}{2}}&space;\cdot&space;r&space;\&space;dr&space;\&space;d\Theta" title="\int_{0}^{2\pi} \int_{0}^{\infty } e^{\frac{r^{2}}{2}} \cdot r \ dr \ d\Theta" /></a></p>
<p align="center">2차원 이상에서 변수 변형을 하면 자코비안을 끝에 곱해주어야 함</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\int_{0}^{2\pi}&space;\int_{0}^{\infty&space;}&space;e^{-u}&space;\cdot&space;du" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\int_{0}^{2\pi}&space;\int_{0}^{\infty&space;}&space;e^{-u}&space;\cdot&space;du" title="\int_{0}^{2\pi} \int_{0}^{\infty } e^{-u} \cdot du" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=u&space;=&space;\frac{r^{2}}{2},&space;\&space;du&space;=&space;r&space;\cdot&space;dr" target="_blank"><img src="https://latex.codecogs.com/gif.latex?u&space;=&space;\frac{r^{2}}{2},&space;\&space;du&space;=&space;r&space;\cdot&space;dr" title="u = \frac{r^{2}}{2}, \ du = r \cdot dr" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=[-e^{-u}]\&space;\infty&space;\&space;to&space;\&space;0&space;=&space;1" target="_blank"><img src="https://latex.codecogs.com/gif.latex?[-e^{-u}]\&space;\infty&space;\&space;to&space;\&space;0&space;=&space;1" title="[-e^{-u}]\ \infty \ to \ 0 = 1" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\int_{0}^{2\pi}&space;1&space;\cdot&space;d\Theta" target="_blank"><img src="https://latex.codecogs.com/png.latex?\int_{0}^{2\pi}&space;1&space;\cdot&space;d\Theta" title="\int_{0}^{2\pi} 1 \cdot d\Theta" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sqrt{2\pi&space;}" target="_blank"><img src="https://latex.codecogs.com/png.latex?\sqrt{2\pi&space;}" title="\sqrt{2\pi }" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=c&space;=&space;\frac{1}{\sqrt{2\pi&space;}}" target="_blank"><img src="https://latex.codecogs.com/png.latex?c&space;=&space;\frac{1}{\sqrt{2\pi&space;}}" title="c = \frac{1}{\sqrt{2\pi }}" /></a></p>
<p align="center">정규화 상수에 갑자기 파이가 나오고 이상했는데, 이유는</p>
<p align="center"> 극 좌표계를 이용해서 정적분을 이용했기 때문!</p>

## 표준정규분포의 평균, 분산  
#### 평균 계산하기  
* 대칭성 때문에 평균은 0이다  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\frac{1}{\sqrt{2\pi}}&space;\int_{\infty}^{-\infty}&space;\cdot&space;z&space;\cdot&space;e^{\frac{-z^{2}}{2}}&space;\&space;dz&space;=&space;0" target="_blank"><img src="https://latex.codecogs.com/png.latex?\frac{1}{\sqrt{2\pi}}&space;\int_{\infty}^{-\infty}&space;\cdot&space;z&space;\cdot&space;e^{\frac{-z^{2}}{2}}&space;\&space;dz&space;=&space;0" title="\frac{1}{\sqrt{2\pi}} \int_{\infty}^{-\infty} \cdot z \cdot e^{\frac{-z^{2}}{2}} \ dz = 0" /></a></p>

* g(x) 가 기함수면 g(-x) = -g(x)  
* 따라서 g(x)를 대칭되게 적분하면,  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\int_{-a}^{a}&space;g(x)&space;dx&space;=&space;0" target="_blank"><img src="https://latex.codecogs.com/png.latex?\int_{-a}^{a}&space;g(x)&space;dx&space;=&space;0" title="\int_{-a}^{a} g(x) dx = 0" /></a></p>

* ex) sin x function  

#### 분산 계산하기
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=Var(z)&space;=&space;E(z^{2})&space;-&space;Ez^2&space;=&space;E(z^{2})" target="_blank"><img src="https://latex.codecogs.com/png.latex?Var(z)&space;=&space;E(z^{2})&space;-&space;Ez^2&space;=&space;E(z^{2})" title="Var(z) = E(z^{2}) - Ez^2 = E(z^{2})" /></a></p>

<p align="center">이때 LOTUS 필요</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\frac{1}{\sqrt{2\pi&space;}}\int_{-\infty}^{\infty}&space;z^{2}&space;\cdot&space;e&space;^{\frac{-z^{2}}{2}}&space;dz" target="_blank"><img src="https://latex.codecogs.com/png.latex?\frac{1}{\sqrt{2\pi&space;}}\int_{-\infty}^{\infty}&space;z^{2}&space;\cdot&space;e&space;^{\frac{-z^{2}}{2}}&space;dz" title="\frac{1}{\sqrt{2\pi }}\int_{-\infty}^{\infty} z^{2} \cdot e ^{\frac{-z^{2}}{2}} dz" /></a></p>
<p align="center">해당 식은 우함수 이기 때문에(even function)</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;\frac{2}{\sqrt{2\pi&space;}}\int_{0}^{\infty}&space;z^{2}&space;\cdot&space;e&space;^{\frac{-z^{2}}{2}}&space;dz" target="_blank"><img src="https://latex.codecogs.com/png.latex?=&space;\frac{2}{\sqrt{2\pi&space;}}\int_{0}^{\infty}&space;z^{2}&space;\cdot&space;e&space;^{\frac{-z^{2}}{2}}&space;dz" title="= \frac{2}{\sqrt{2\pi }}\int_{0}^{\infty} z^{2} \cdot e ^{\frac{-z^{2}}{2}} dz" /></a></p>
<p align="center">부분적분하자. 하나는 미분하기 쉬운걸로, 하나는 적분하기 쉬운걸로</p>
<p align="center">기억을 상기해보면, 두 개의 식으로 나누는게 중요!</p>
<p align="center">z 와 나머지 식으로 나눈다</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\begin{Bmatrix}&space;u&space;=&space;z&space;&&space;&&space;dv&space;=&space;z&space;\cdot&space;e^{\frac{-z^{2}}{2}}&space;&&space;\\&space;du&space;=&space;dz&space;&&space;&&space;v&space;=&space;-&space;e^{\frac{-z^{2}}{2}}&space;&&space;\end{Bmatrix}" target="_blank"><img src="https://latex.codecogs.com/png.latex?\begin{Bmatrix}&space;u&space;=&space;z&space;&&space;&&space;dv&space;=&space;z&space;\cdot&space;e^{\frac{-z^{2}}{2}}&space;&&space;\\&space;du&space;=&space;dz&space;&&space;&&space;v&space;=&space;-&space;e^{\frac{-z^{2}}{2}}&space;&&space;\end{Bmatrix}" title="\begin{Bmatrix} u = z & & dv = z \cdot e^{\frac{-z^{2}}{2}} & \\ du = dz & & v = - e^{\frac{-z^{2}}{2}} & \end{Bmatrix}" /></a></p>

<p align="center">위의 식을 이용해 부분적분으로 나타내면, </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\frac{2}{\sqrt{2\pi}}&space;((uv)|_{\infty&space;}^{0}\textrm{}&space;&plus;&space;\int&space;e^&space;\frac{-z^2}{2}&space;dz&space;)" target="_blank"><img src="https://latex.codecogs.com/png.latex?\frac{2}{\sqrt{2\pi}}&space;((uv)|_{\infty&space;}^{0}\textrm{}&space;&plus;&space;\int&space;e^&space;\frac{-z^2}{2}&space;dz&space;)" title="\frac{2}{\sqrt{2\pi}} ((uv)|_{\infty }^{0}\textrm{} + \int e^ \frac{-z^2}{2} dz )" /></a></p>

<p align="center">첫번째 항은 0, 두번째 항은 앞서 했던 계산 방법을 이용</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\frac{2}{\sqrt{2\pi&space;}}&space;\cdot&space;\frac{\sqrt{2\pi}}{2}&space;=&space;1" target="_blank"><img src="https://latex.codecogs.com/png.latex?\frac{2}{\sqrt{2\pi&space;}}&space;\cdot&space;\frac{\sqrt{2\pi}}{2}&space;=&space;1" title="\frac{2}{\sqrt{2\pi }} \cdot \frac{\sqrt{2\pi}}{2} = 1" /></a></p>

### 표기법
* <a href="https://www.codecogs.com/eqnedit.php?latex=\Phi" target="_blank"><img src="https://latex.codecogs.com/png.latex?\Phi" title="\Phi" /></a> : 표준정규분포의 누적분포함수  
* <a href="https://www.codecogs.com/eqnedit.php?latex=\Phi(z)&space;=&space;\frac{1}{\sqrt{2&space;\pi}}&space;\int_{\infty}^{z}&space;e^{\frac{-t^{2}}{2}}&space;dt&space;,&space;\&space;CDF" target="_blank"><img src="https://latex.codecogs.com/png.latex?\Phi(z)&space;=&space;\frac{1}{\sqrt{2&space;\pi}}&space;\int_{\infty}^{z}&space;e^{\frac{-t^{2}}{2}}&space;dt&space;,&space;\&space;CDF" title="\Phi(z) = \frac{1}{\sqrt{2 \pi}} \int_{\infty}^{z} e^{\frac{-t^{2}}{2}} dt , \ CDF" /></a>  
* <a href="https://www.codecogs.com/eqnedit.php?latex=\Phi&space;(-z)&space;=&space;\Phi&space;(z)" target="_blank"><img src="https://latex.codecogs.com/png.latex?\Phi&space;(-z)&space;=&space;\Phi&space;(z)" title="\Phi (-z) = \Phi (z)" /></a> : 대칭성  

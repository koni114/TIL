# 12강- 이산, 연속, 균등분포 (Discrete vs. Continuous, the Uniform)

## 핵심 키워드
* 연속확률변수  
* 확률밀도함수(Probability Density Function = PDF)  
* 기댓값, 분산  
* 균등분포(Uniform Distribution)  
* 무의식적인 통계학자의 법칙(Law of the unconscious statistician = LOTUS)  
* 균등분포의 보편성(University of the Uniform)  

## 연속분포(Continuous Distribution)
* 이산분포는 연속분포에 비해서 훨씬 간단  
* 적분을 할 것임. 적분을 하지 못하는 경우에는 분리해서 계산  
* 그전에 연속분포와 이산분포의 차이를 정확하게 볼 줄 알아야 함!  

#### 이산분포 vs연속분포  
##### 이산분포
* random variable ->  X로 표현  
* PMF를 활용. P(X = x) 즉 확률 변수 X가 x일 확률을 나타냄  
함수의 정의역(x)이 양수인 정수이면, X도 양수인 정수이어야 함  
why? 이산이기 때문  
* 누적분포함수 CDF는  F(x) = P(X <= x)  
  이산에서의 CDF는 계단 형태를 가지기 때문에 계산이 까다로웠음  

##### 연속분포
* random variable -> X로 표현  
* PDF를 활용. PMF를 사용하지 않는 이유는     
<b> 특정한 random variable의 확률은 0을 가지기 때문! </b>  
why? 특정 실수사이에서는 무수히 많은 실수가 존재하기 때문에 어떤 실수 하나의 값을 가질 확률은 '0'  

* 누적분포함수 CDF는 F(x) = P(X <= x)  
적분으로 계산할 수 있기 때문에 훨씬 더 활용도가 높고 보편적임  


## PDF(Probability Density Function)
* 연속분포를 설명할 때 가장 자주 쓰는 분포  
* 자주하는 실수 중 하나는 "확률"이 아니라 "확률 분포"라는 점  
* PDF에서는 더 이상 조약돌을 생각 할 수 없음  
바닥에 깔려있는 진흙을 생각  

##### Defn
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Defn&space;:&space;R.V&space;\&space;X&space;\&space;has&space;\&space;PDF&space;\&space;f(x)&space;\if&space;\&space;P(a&space;\leq&space;X&space;\leq&space;b)&space;=&space;\int_{a}^{b}&space;f(x)&space;dx" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Defn&space;:&space;R.V&space;\&space;X&space;\&space;has&space;\&space;PDF&space;\&space;f(x)&space;\if&space;\&space;P(a&space;\leq&space;X&space;\leq&space;b)&space;=&space;\int_{a}^{b}&space;f(x)&space;dx" title="Defn : R.V \ X \ has \ PDF \ f(x) \if \ P(a \leq X \leq b) = \int_{a}^{b} f(x) dx" /></a></p>  

* random variable인 X가 PDF인 f(x)를 가질 때,  
X가 a와 b사이에 있을 확률은 해당 적분 값과 같다

##### properties
* a = b이면, 적분 값이 0 -> 특정 값에서 확률 값은 0
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=a&space;=&space;b,&space;\int_{a}^{a}&space;f(x)&space;dx&space;=&space;0" target="_blank"><img src="https://latex.codecogs.com/gif.latex?a&space;=&space;b,&space;\int_{a}^{a}&space;f(x)&space;dx&space;=&space;0" title="a = b, \int_{a}^{a} f(x) dx = 0" /></a></p>  

* 음수여선 안되고, 전체 적분을 했을 때 1이어야 함  
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=f(x)&space;\geq&space;0,&space;\&space;\int_{-&space;\infty&space;}^{\infty}&space;f(x)&space;dx&space;=&space;1" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f(x)&space;\geq&space;0,&space;\&space;\int_{-&space;\infty&space;}^{\infty}&space;f(x)&space;dx&space;=&space;1" title="f(x) \geq 0, \ \int_{- \infty }^{\infty} f(x) dx = 1" /></a></p>

##### 확률 밀도 함수의 예시(중요)
![img](https://github.com/koni114/Harvard_Statistics/blob/master/image/%ED%99%95%EB%A5%A0%EB%B0%80%EB%8F%84%ED%95%A8%EC%88%98.JPG)

* 총넓이는 1. 꼬불꼬불 할 수도 있고, 음수가 아니고 합이 1이기만 하면 됨  

* 확률 밀도(Probability Density -> f(x))가 뜻하는 것은 무엇일까?  
  * 일단 '확률'은 아니다. f(x0) 를 생각해보자  
  * 이 값이 a라고 했을 때, 1보다 클 수 있다. 때문에 절대 '확률'은 아님  

##### 입실론을 이용한 확률 밀도의 직관적 이해
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=f(x_{0})&space;\cdot&space;\epsilon&space;\approx&space;P(X&space;\in&space;(X_{0}&space;-&space;\frac{\epsilon}{2}&space;,&space;\&space;X_{0}&space;&plus;&space;\frac{\epsilon}{2}))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f(x_{0})&space;\cdot&space;\epsilon&space;\approx&space;P(X&space;\in&space;(X_{0}&space;-&space;\frac{\epsilon}{2}&space;,&space;\&space;X_{0}&space;&plus;&space;\frac{\epsilon}{2}))" title="f(x_{0}) \cdot \epsilon \approx P(X \in (X_{0} - \frac{\epsilon}{2} , \ X_{0} + \frac{\epsilon}{2}))" /></a></p>

* X가 정확하게 X0일 확률은 0  
* 하지만 입실론이 굉장히 작은 수 일 때,   
X0를 포함한 아주 작은 입실론 크기의 범위에 확률변수 X가 들어갈 확률이  
X가 정확히 X0일 확률에 근사하고,  
결국 <b> 확률밀도 x 범위 </b> 값의 길이가 됨(여기서의 x는 곱하기!)  
* 중요한 관점은 입실론을 곱하면서 '확률 밀도' 차원에서 '확률' 차원으로 곱하게 됨  
* 확률밀도를 직관적으로 생각하기 좋은 방법!  

## CDF(Cumulative Density Function)
##### Defn
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=if&space;\&space;X&space;\&space;has&space;\&space;PDF&space;\&space;f,&space;\&space;the&space;\&space;CDF&space;\&space;is&space;\&space;F(x)&space;=&space;P(X&space;\leq&space;x)&space;=&space;\int_{-\infty&space;}^{x}&space;f(t)&space;dt" target="_blank"><img src="https://latex.codecogs.com/gif.latex?if&space;\&space;X&space;\&space;has&space;\&space;PDF&space;\&space;f,&space;\&space;the&space;\&space;CDF&space;\&space;is&space;\&space;F(x)&space;=&space;P(X&space;\leq&space;x)&space;=&space;\int_{-\infty&space;}^{x}&space;f(t)&space;dt" title="if \ X \ has \ PDF \ f, \ the \ CDF \ is \ F(x) = P(X \leq x) = \int_{-\infty }^{x} f(t) dt" /></a></p>

* t를 쓴 이유는, x를 두번 쓰면 안되니 t를 쓴 것. 큰 의미는 없음  

##### CDF에서 PDF 구하는 방법
* 이때 F(x) 는 미분 가능해야 함  
연속분포는 F가 연속적이라는 것보다 확률변수 X가 특정 값 뿐만 아니라  
무한적으로 연속적인 값을 가질 수 있다는 것을 의미 함  
* 이 때 다음과 같은 식이 성립(Fundamental theorem calculus에 의거)  
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=f(x)&space;=&space;F^{'}(x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f(x)&space;=&space;F^{'}(x)" title="f(x) = F^{'}(x)" /></a></p>  

##### 특정 범위의 PDF의 값을 CDF로 표현하기
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=P(a&space;<&space;X&space;<&space;b)&space;=&space;\int_{a}^{b}&space;f(x)&space;dx&space;=&space;F(b)&space;-&space;F(a)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(a&space;<&space;X&space;<&space;b)&space;=&space;\int_{a}^{b}&space;f(x)&space;dx&space;=&space;F(b)&space;-&space;F(a)" title="P(a < X < b) = \int_{a}^{b} f(x) dx = F(b) - F(a)" /></a></p>  

* 이산 분포에서는 등호 포함여부가 중요했지만 연속분포에서는 필요 없음  
* 전 구간에서 미분가능하다고 가정해야 함. 아니면 굉장히 복잡해짐  

## 분산(Variance)
* 평균만으로는 데이터의 특성을 알기 어렵  
* 데이터의 분포나 퍼짐 정도를 알 필요성이 있음  
* 차근차근 생각하면서 분산에 대해서 접근해보자  
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Var(X)&space;=&space;E(X&space;-&space;E(X))&space;?" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(X)&space;=&space;E(X&space;-&space;E(X))&space;?" title="Var(X) = E(X - E(X)) ?" /></a></p>

<p align = 'center'> 이렇게 하면 항상 0이다(선형성에 의해..)</p>
<p align = 'center'>그렇다면 절대 값을 씌우면? </p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Var(X)&space;=&space;E(|X&space;-&space;E(X)|)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(X)&space;=&space;E(|X&space;-&space;E(X)|)" title="Var(X) = E(|X - E(X)|)" /></a></p>
<p align = 'center'>이렇게는 안한다</p>
<p align = 'center'>두 가지 이유가 있는데, 첫 번째는 절대값 그래프는 첨점이 생겨 미분 불가능하고, </p>
<p align = 'center'>기하학적인 접근이 어렵다</p>
<p align = 'center'>결과적으로 분산은 제곱을 이용한다</p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Var(X)&space;=&space;E((X&space;-&space;E(X))^{2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(X)&space;=&space;E((X&space;-&space;E(X))^{2})" title="Var(X) = E((X - E(X))^{2})" /></a></p>

* 분산 계산시 제곱 사용  
  *  기하학적인 접근이 가능. (ex) 피타고라스 정리, 유클리디안 거리 등 ...)  
  *  한 가지 단점은 단위가 바뀐다는 점  
  *  따라서 이때는 Standard deviation(표준편차)를 사용함  
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Standard&space;\&space;deviation&space;:&space;SD(x)&space;=&space;\sqrt{Var(x)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Standard&space;\&space;deviation&space;:&space;SD(x)&space;=&space;\sqrt{Var(x)}" title="Standard \ deviation : SD(x) = \sqrt{Var(x)}" /></a></p>

* E라는 표기법은 매우 유용  
연속이던, 이산이던 일반적인 기대값을 나타낼 수 있음  

##### 분산을 계산하는 다른 방법
* 제곱을 인수 분해해서 간단하게 만들 수 있음  
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Var(X)&space;=&space;E(X^{2}&space;-&space;2E(X)&space;\cdot&space;X&space;&plus;&space;(E(X))^{2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(X)&space;=&space;E(X^{2}&space;-&space;2E(X)&space;\cdot&space;X&space;&plus;&space;(E(X))^{2})" title="Var(X) = E(X^{2} - 2E(X) \cdot X + (E(X))^{2})" /></a></p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Var(X)&space;=&space;E(X^{2})-&space;2&space;\cdot&space;E(X)&space;\cdot&space;E(X)&space;&plus;&space;(E(X))^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(X)&space;=&space;E(X^{2})-&space;2&space;\cdot&space;E(X)&space;\cdot&space;E(X)&space;&plus;&space;(E(X))^{2}" title="Var(X) = E(X^{2})- 2 \cdot E(X) \cdot E(X) + (E(X))^{2}" /></a></p>

<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Var(X)&space;=&space;E(X^{2})-&space;(E(X))^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(X)&space;=&space;E(X^{2})-&space;(E(X))^{2}"  title="Var(X) = E(X^{2})- (E(X))^{2}" /></a></p>

* Notation. 표기법을 주의하자! 다음의 식은 같은 의미로 사용된다  
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Ex^{2}&space;=&space;E(x^{2})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Ex^{2}&space;=&space;E(x^{2})" title="Ex^{2} = E(x^{2})" /></a></p>

## 균등분포(Uniform Distribution)  
* 가장 간단한 연속분포 ~ Unif(a, b)  
* a,b점 사이의 random point  
* random의 의미  
  * 확률 변수가 있다는 것을 뜻함  
* completely random의 의미  
  *  어느 특정한 두 점의 확률이 같다고 하는 것은 의미가 없음  
  * 어차피 특정 point의 확률은 0  
  * a,b의 중점을 기준으로 앞의 반이 뽑힐 확률이 뒤의 반이 뽑힐확률과 같다는 뜻  
* 우리가 원하는 것은 치중하지 않는 분포  
* 균등분포는 특정 범위가 뽑힐 확률이 그 범위의 크기게 비례하는 것을 뜻함  

#### PDF
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=\left\{\begin{matrix}&space;C,&space;if&space;\&space;a&space;\leq&space;x&space;\leq&space;b&space;&&space;\\&space;0,&space;otherwise&space;&&space;\end{matrix}\right." target="_blank"><img src="https://latex.codecogs.com/gif.latex?\left\{\begin{matrix}&space;C,&space;if&space;\&space;a&space;\leq&space;x&space;\leq&space;b&space;&&space;\\&space;0,&space;otherwise&space;&&space;\end{matrix}\right." title="\left\{\begin{matrix} C, if \ a \leq x \leq b & \\ 0, otherwise & \end{matrix}\right." /></a></p>

* a,b 범위 바깥이면 0이어야 하고, a <= x <= b 이면 상수  
* PDF를 적분했을 때 1이 나와야 하므로, C = 1/(b-a)  

#### CDF
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=F(x)&space;=&space;\int_{-\infty}^{x}f(t)&space;dt&space;=&space;\int_{a}^{x}f(t)dt&space;=&space;\left\{\begin{matrix}&space;0,&space;\&space;if&space;\&space;x&space;<&space;a&space;&&space;\\&space;\frac{x-a}{b-a},&space;\&space;if&space;\&space;a&space;\leq&space;x&space;\leq&space;b&space;&&space;\\&space;1,\&space;if&space;\&space;x&space;>&space;b&space;&&space;\end{matrix}\right." target="_blank"><img src="https://latex.codecogs.com/gif.latex?F(x)&space;=&space;\int_{-\infty}^{x}f(t)&space;dt&space;=&space;\int_{a}^{x}f(t)dt&space;=&space;\left\{\begin{matrix}&space;0,&space;\&space;if&space;\&space;x&space;<&space;a&space;&&space;\\&space;\frac{x-a}{b-a},&space;\&space;if&space;\&space;a&space;\leq&space;x&space;\leq&space;b&space;&&space;\\&space;1,\&space;if&space;\&space;x&space;>&space;b&space;&&space;\end{matrix}\right." title="F(x) = \int_{-\infty}^{x}f(t) dt = \int_{a}^{x}f(t)dt = \left\{\begin{matrix} 0, \ if \ x < a & \\ \frac{x-a}{b-a}, \ if \ a \leq x \leq b & \\ 1,\ if \ x > b & \end{matrix}\right." /></a></p>

* x가 a보다 크거나 같고 b보다 작거나 같은 경우는 해당 적분 식을 적분해서 대입하면 나옴  
* 해당 함수는 1차 함수. 확률이 x에 비례해서 커짐  

#### 기대값
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=&space;\int_{b}^{a}&space;\frac{x}{b-a}&space;dx&space;=&space;\frac{a&plus;b}{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=&space;\int_{b}^{a}&space;\frac{x}{b-a}&space;dx&space;=&space;\frac{a&plus;b}{2}" title="E(x) = \int_{b}^{a} \frac{x}{b-a} dx = \frac{a+b}{2}" /></a></p>
* 균등 분포의 기대값이니, 당연히 a,b의 중간 값(직관적으로 이해 가능)  

#### 분산
* Var(x) = E(x^2) - (E(x))^2 를 이용  
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=E(X^{2})&space;=&space;E(Y)&space;=&space;\int_{-\infty&space;}^{\infty}&space;x^2&space;f_{x}(X)dx" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X^{2})&space;=&space;E(Y)&space;=&space;\int_{-\infty&space;}^{\infty}&space;x^2&space;f_{x}(X)dx" title="E(X^{2}) = E(Y) = \int_{-\infty }^{\infty} x^2 f_{x}(X)dx" /></a></p>

* 위의 식이 맞는가?  
* 얼핏 보면 X -> X^2 이므로 저런식으로의 접근이 맞는듯 하다  
<b>무의식적인 통계학자의 법칙(Law of the unconscious statistician)</b>이라고 함  
* 실제로 이런식으로 접근하는 것은 실수!  
생각도 안해보고 대충 X -> X^2 으로 변경해서 계산하는 것을 지칭  
but 실제로는 참!  
* 원래는 X^2의 PDF를 직접 구해야한다. 하지만 LOTUS를 이용해서 쉽게 풀 수 있음  
* 줄여서 LOTUS 라고 함. LOTUS는 다음과 같이 나타낼 수 있음  
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=E(g(X))&space;=&space;\int_{-\infty&space;}^{\infty}&space;g(x)&space;f_{x}(x)&space;dx" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(g(X))&space;=&space;\int_{-\infty&space;}^{\infty}&space;g(x)&space;f_{x}(x)&space;dx" title="E(g(X)) = \int_{-\infty }^{\infty} g(x) f_{x}(x) dx" /></a></p>

* LOTUS를 이용해서 분산을 구하면,  
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Let&space;\&space;U&space;\sim&space;Unif(0,&space;1),&space;\&space;E(U)&space;=&space;\frac{1}{2},&space;\&space;E(U^{2})&space;=&space;\int_{1}^{0}&space;U^{2}&space;\cdot&space;f_{u}(u)&space;du" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Let&space;\&space;U&space;\sim&space;Unif(0,&space;1),&space;\&space;E(U)&space;=&space;\frac{1}{2},&space;\&space;E(U^{2})&space;=&space;\int_{1}^{0}&space;U^{2}&space;\cdot&space;f_{u}(u)&space;du" title="Let \ U \sim Unif(0, 1), \ E(U) = \frac{1}{2}, \ E(U^{2}) = \int_{1}^{0} U^{2} \cdot f_{u}(u) du" /></a></p>
<p align = 'center'>이 때, fu(u)는 1(1/(b-a) = 1 이므로)</p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=E(U^{2})&space;=&space;\int_{0}^{1}&space;U^{2}&space;\cdot&space;f_{u}(u)&space;du" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(U^{2})&space;=&space;\int_{0}^{1}&space;U^{2}&space;\cdot&space;f_{u}(u)&space;du" title="E(U^{2}) = \int_{0}^{1} U^{2} \cdot f_{u}(u) du" /></a></p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=E(U^{2})&space;=&space;\int_{0}^{1}&space;U^{2}&space;\cdot&space;1&space;du&space;=&space;\frac{1}{3}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(U^{2})&space;=&space;\int_{0}^{1}&space;U^{2}&space;\cdot&space;1&space;du&space;=&space;\frac{1}{3}" title="E(U^{2}) = \int_{0}^{1} U^{2} \cdot 1 du = \frac{1}{3}" /></a></p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Var(U)&space;=&space;E(U^2)&space;-EU^{2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(U)&space;=&space;E(U^2)&space;-EU^{2}" title="Var(U) = E(U^2) -EU^{2}" /></a></p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=Var(U)&space;=&space;\frac{1}{3}&space;-&space;\frac{1}{4}&space;=&space;\frac{1}{12}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Var(U)&space;=&space;\frac{1}{3}&space;-&space;\frac{1}{4}&space;=&space;\frac{1}{12}" title="Var(U) = \frac{1}{3} - \frac{1}{4} = \frac{1}{12}" /></a></p>

* 결과적으로는 LOTUS 방법을 사용하여 훨씬 쉬워짐  
* 균등분포가 연속붙포에서는 제일 쉬운 듯 보임  
  *  PDF가 상수  
  * a,b의 범위가 존재해야함.   
  a,b를 모든 상수라고 해버리면 적분시 1이 되는 값을 찾지 못함  

#### Universality of Uniform Distribution
* 0~1까지의 균등분포를 가질 때, 균등분포에서 어떠한 분포로도 전환이 가능하다는 의미  
*  0과 1 사이의 수를 뽑을 때 어떠한 분포든지 균등분포에서 그 분포로 전환 가능  
* F가 엄청 복잡한 분포여도 상관 없음  
* F를 우리가 원하는 CDF 중 하나라고 할 때, 이 CDF를 가지는 r.v를 만들고 싶을 때 활용  

#### Universality of Uniform Distribution 증명
* 가정  
  * F는 강한 증가  
  * 연속함수  

* 다음과 같은 가정을 하는 이유는 역함수를 구하려고 하기 때문  
* 차근차근 생각해보면서 증명해보자  

<p align = 'center'>우선 다음과 같은 식을 만족한다고 가정해보자</p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=X&space;=&space;F^{-1}(U),&space;\&space;then,&space;\&space;X&space;\sim&space;F" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;=&space;F^{-1}(U),&space;\&space;then,&space;\&space;X&space;\sim&space;F" title="X = F^{-1}(U), \ then, \ X \sim F" /></a></p>
<p align = 'center'> 말로 풀어보면, 원하는 CDF의 역함수를 구하고, uniform random variable를 넣으면</p>
<p align = 'center'>원하는 random variable이 나온다는 의미</p>
<p align = 'center'>좌변의 식이 X ~ F가 되는지 확인하면 됨</p>
<p align = 'center'>CDF만 잘 이해하면 되는데, </p>
<p align = 'center'>X의 CDF를 계산하면 됨 </p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=P(X&space;\leq&space;x)&space;=&space;P(F^{-1}(U)&space;\leq&space;x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(X&space;\leq&space;x)&space;=&space;P(F^{-1}(U)&space;\leq&space;x)" title="P(X \leq x) = P(F^{-1}(U) \leq x)" /></a></p>
<p align = 'center'>F를 씌우자</p>
<p align = 'center'>만약 단순증가가 아니였다면 (-)를 붙여주어야 함</p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex==&space;P(U&space;\leq&space;F(x))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;P(U&space;\leq&space;F(x))" title="= P(U \leq F(x))" /></a></p>
<p align = 'center'>U는 0에서 1까지 균등분포를 따르는 확률 변수</p>
<p align = 'center'>F(x)는 확률변수이기 때문에 0과 1 사이의 수</p>
<p align = 'center'>균등분포에서는 확률이 범위의 크기에 비례</p>
<p align = 'center'>0 ~ 1 이므로 특정범위의 확률은 그냥 F(x)가 됨</p>
<p align = 'center'><a href="https://www.codecogs.com/eqnedit.php?latex=P(X&space;\leq&space;x)&space;=&space;F(x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(X&space;\leq&space;x)&space;=&space;F(x)" title="P(X \leq x) = F(x)" /></a></p>

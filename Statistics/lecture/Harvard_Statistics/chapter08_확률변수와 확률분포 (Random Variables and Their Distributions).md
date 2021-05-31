# 8강- 확률변수와 확률분포 (Random Variables and Their Distributions)

## 핵심 키워드  
* 확률분포(random variables)  
* 모수  
* 확률질량함수(PMF)  
* 지시확률변수  
* 누적분포함수(CDF)  
* 이항분포  
* 초기하분포  

## 이항 분포(Binomial distribution)
* Bin(n, p) 으로 표시. n과 p는 파라미터로 다른 문자로 표기가 가능  
* X ~ Bin(n, p)라고 표기를 많이 하는데, 이는 <b> X가 이항분포를 가지는 확률 변수</b>라는 뜻  

#### 3가지 관점의 이항분포 해석
#####  (1) Story 해석
* X : n번의 독립적인 베르누이 시행(P)에서 성공한 횟수  
* 일반적으로 동전던지기를 생각하면 된다. 예를 들어 동전을 던졌을 때 총 n번 중 성공이라고 판단(앞면 또는 뒷면이겠지..?)되는 횟수를 X, 확률 변수라고 함  

##### (2) 합의 꼴을 가지는 지시확률변수(indicator random variables)
<p align="center"><img src="https://latex.codecogs.com/gif.latex?X&space;=&space;X_{1}&space;&plus;&space;X_{2}&space;&plus;&space;X_{3}&space;\dots&space;X_{n}&space;,&space;X_{j}" title="X = X_{1} + X_{2} + X_{3} \dots X_{n} , X_{j}" /></p>

* Xj 가 1일 때, j번째 실행이 성공일 때, Xj가 0일 때 j번 째 실행이 실패일 때를 의미
* indicator라고 하는 이유는  j번째 시행이 성공인지, 실패인지 알려주기 때문!  
* Xj ( 1 < = j <= n ) 은 i.i.d(independent identically distributed Ber(p))  
  * independent : 시행 자체가 서로 독립적이라는 의미  
  * identically : 각 X가 동일한 분포를 가진다는 의미 -> 여기서는 베르누이 분포   

* <b> random variables VS distribution </b>
  * random variables : 수학적으로 함수를 의미. 즉 X = X1 + X2 + ... Xn 처럼!  
  * distribution : X가 어떻게 다르게 행동할지에 대한 확률  
  * 같은 분포를 가지는 random variables는 여러 개일 수 있다!  


##### (3) 확률질량함수(PMF : Probability mass function)
* X가 특정 값을 가질 확률  
* 이항분포는 다음과 같이 나타낼 수 있음  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(X&space;=&space;k)&space;=&space;\binom{n}{k}&space;p^k&space;q^{n-k},&space;(p&space;=&space;1-q)" title="P(X = k) = \binom{n}{k} p^k q^{n-k}, (p = 1-q)" /></p>  

## 확률 분포 추가 설명
* 확률 분포(random variables)는 무엇인가?  
* R.V.S(Random Variables 의 약자)  
* 표본공간 S가 있다고 하자. 표본공간은 매우 복잡할 수 있고, 고차원이며 무한대 일 수 있다.  
* 표본공간에 있는 조약돌 예시를 생각해 보았을 때, 확률 변수는 <b>조약돌 안에 숫자를 배정하는 함수</b>로 정의할 수 있음  
* <b>X = 7</b> 이라는 것은 단순히 사건을 의미함. X에다가 7을 대입하라는 의미가 아님   

## CDF(Cumulative distribution function)
* 앞선 이항분포도 CDF로 작성이 가능하다  
* X = x도 사건이지만, X <= x도 사건으로 생각할 수 있음  
<p align = "center"><img src="https://latex.codecogs.com/gif.latex?F(x)&space;=&space;P(X&space;\leq&space;x)" title="F(x) = P(X \leq x)" /></p>

* 이 때의 F(x)를 CDF라고 한다!  

##### CDF가 중요한 이유  

* 항상 확률변수는 숫자를 부여한다(Sample space가 복잡하던 말던!)  
* F(x) = P(X <= x) 에서 X <= x 는 사건이지만 실험을 하기 전까지 X의 값이 무엇인지 알 수 없음  
* 실험한 후에는 확인 할 수 있음  
  * ex) X = 7 이라는 것을 관찰하고 x 가 9였다면, 사건이 일어났다고 할 수 있음  
* 즉 CDF는 분포를 나타내는 방법 중 하나! (이 말은 다른 방법으로도 나타낼 수 있다는 말)  
* Why? X에 대한 모든 가능한 확률을 결정할 수 있는 방법이기 때문  
* ex) X가 1와 3사이에 있는 확률, X가 5 ~ 7 사이에 있는 확률 등..  
* 핵심은 우리가 F(x)를 통해 위와 같은 질문에 답을 할 수 있다는 것!  
* 일반적으로 PMF보다 CDF를 더 많이 사용하는데, 이유는 모든 확률변수에 사용할 수 있다는 이유 때문이다  

## PMF 추가 설명
* PMF는 이산확률변수(discrete random variables)에 대해서만 정의됨  

##### ** discrete random variables VS continuous random variables
* discrete random variables  
  * 변수(X)가 '이산적'이다 라는 의미  
  * 예를 들어 이항분포에서 X는 이산적이다(사건이 1,2,3 ... 5 이렇게 나타나기 때문)  
  * 이 때 정수일 필요는 없음. 유한 배열이거나 무한 배열일 수도 있다는 의미  
* continuous random variables   
  * 특정 구간에 있는 실수를 가짐. 특정한 값이여도 상관없음!  
* 어떤 확률변수는 이산확률변수 + 연속확률변수를 동시에 가질 수도 있음!  
* 그렇다면, PMF는 어떻게 생각할 수 있을까?  
  * 모든 j에 대해서 X = aj일 확률! 이 때 j는 사건이 발생한 건 수라고 생각하면 되고, aj는 사건이라고 생각하면 됨  
  * P(X = aj) 는 X라는 확률 변수가 aj라는 사건이 일어날 확률(P)이라고 해석이 가능하다  
  * 앞선 생각들에 의해서 2가지 조건을 만족해야 한다는 것을 생각할 수 있는데,  
    * 1. 모든 P(aj) >= 0  
    * 2. P(X = aj) 의 합 = 1     
* 이산확률변수는 CDF보다 PMF에 쓰는것이 더 편함!  
* 만약 분포를 찾으려고 했을 때 PMF를 찾는 것이 더 쉬움  

## 이항분포에서의 PMF가 유효한지 확인해보기
* 앞서 썼던 PMF가 진짜 유효한지 확인하려면 2가지 조건을 만족하는지 확인하면 된다.  
* 먼저 이항분포의 PMF를 보자  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(X&space;=&space;k)&space;=&space;\binom{n}{k}&space;p^k&space;q^{n-k},&space;(p&space;=&space;1-q)" title="P(X = k) = \binom{n}{k} p^k q^{n-k}, (p = 1-q)" /></p>

* 1. 모든 P(aj)가 0보다 큰가?  
  * nCk, p, q는 모두 0보다 크므로, P(aj)는 항상 0보다 큰 값을 만족  
* 2. P(X = aj) 의 합이 1인가?  
  * <b>이항정리</b>에 따르면 해당식은 (p + q)^n 임  
  * q = 1-p 이므로, 1을 만족한다  

## X+Y ~ Bin(m+n, p) 증명해보기
* 전 chapter에서 X ~ Bin(n, p), Y ~ Bin(m, p) 이면, X+Y ~ Bin(n+m, p)를 3가지 관점에서 생각해보자  

##### (1) Story 관점
* 각 시행은 베르누이 분포를 따르는 이항분포의 시행들을 각각 더하면 X+Y ~ Bin(m+n, p) 가 나오는 것을 이해할 수 있음  
* 예를 들어 동전을 n,m번 던지는 이항분포를 따르는 시행이 있다고 할 때, 각각 던지나, 같이 생각해서 던지나  
확률 값은 같다는 것을 생각할 수 있음  
* <b>** X + Y의 의미</b>
  * 항상 강조하지만, X, Y는 "function" 이다  
  * 두 함수를 더하려면, 두 함수가 같은 정의역을 가지고 있어야 함  -> 같은 Sample space를 가짐  
  * 따라서 해당 X, Y의 두 함수를 제곱해서 더하던, 세제곱해서 더하던 상관 없다는 말!(ex) X^2 + Y.... )  

##### (2) 지시확률변수 관점
<p align="center"><img src="https://latex.codecogs.com/gif.latex?X&space;=&space;X_{1}&space;&plus;&space;X_{2}&space;&plus;&space;X_{3}&space;\dots&space;X_{n}" title="X = X_{1} + X_{2} + X_{3} \dots X_{n}" /></p>
<p align="center"><img src="https://latex.codecogs.com/gif.latex?Y&space;=&space;Y_{1}&space;&plus;&space;Y_{2}&space;&plus;&space;Y_{3}&space;\dots&space;Y_{n}" title="Y = Y_{1} + Y_{2} + Y_{3} \dots Y_{n}" /></p>
<p align="center"><img src="https://latex.codecogs.com/gif.latex?X&space;&plus;&space;Y&space;=&space;\sum_{&space;}^{n}&space;X_{j}&space;&plus;&space;\sum_{&space;}^{n}&space;Y_{j}" title="X + Y = \sum_{ }^{n} X_{j} + \sum_{ }^{n} Y_{j}" /></p>

##### (3) PMF 관점
* 전확률정리와 조건부확률을 사용해서 증명해보자!  
* 문제를 쉽게 풀기 위해 X값을 안다고 가정해보자(전확률정리 이용)  
* 또한 X에 대한 조건부확률을 통해 계산해보자  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(X&plus;Y&space;=&space;k)&space;=&space;\sum_{j&space;=&space;0}^{k}&space;P(X&space;&plus;&space;Y&space;=&space;k&space;|&space;X&space;=&space;j)&space;P(X&space;=&space;j)" title="P(X+Y = k) = \sum_{j = 0}^{k} P(X + Y = k | X = j) P(X = j)" /></p>
<p align="center">X는 j이면 X에 상관없이 Y는 자연스레 k-j가 되고, <p>
<p align="center">P(X = j) 는 PMF로 나타낼 수 있으므로, </p>
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(X&plus;Y&space;=&space;k)&space;=&space;\sum_{j&space;=&space;0}^{k}&space;P(Y&space;=&space;k-j&space;|&space;X&space;=&space;j)\binom{n}{j}&space;P^{j}&space;q^{n-j}" title="P(X+Y = k) = \sum_{j = 0}^{k} P(Y = k-j | X = j)\binom{n}{j} P^{j} q^{n-j}" /></p>
<p align="center">X와 Y는 서로 독립이므로, X = j 일 때, Y = k-j일 확률이나,   <p>
<p align="center">그냥 Y = k-j일 확률이나 같으므로, 분모의 P(X = j)를 지울 수 있다  <p>
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(X&plus;Y&space;=&space;k)&space;=&space;\sum_{j&space;=&space;0}^{k}&space;P(Y&space;=&space;k-j)\binom{n}{j}&space;P^{j}&space;q^{n-j}" title="P(X+Y = k) = \sum_{j = 0}^{k} P(Y = k-j)\binom{n}{j} P^{j} q^{n-j}" /></p>
<p align="center"> P(Y = k-j) 도 PMF로 나타낼 수 있으므로,  <p>
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(X&plus;Y&space;=&space;k)&space;=&space;\sum_{j&space;=&space;0}^{k}&space;\binom{m}{k-j}&space;P^{k-j}&space;q^{m&plus;k-j}\binom{n}{j}&space;P^{j}&space;q^{n-j}" title="P(X+Y = k) = \sum_{j = 0}^{k} \binom{m}{k-j} P^{k-j} q^{m+k-j}\binom{n}{j} P^{j} q^{n-j}" /></p>
<p align="center"> 살짝 정리해주면,  <p>
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(X&plus;Y&space;=&space;k)&space;=&space;\sum_{j&space;=&space;0}^{k}&space;\binom{m}{k-j}&space;\binom{n}{j}&space;P^{k}&space;q^{m&plus;n-k}" title="P(X+Y = k) = \sum_{j = 0}^{k} \binom{m}{k-j} \binom{n}{j} P^{k} q^{m+n-k}" /></p>
<p align="center"> 여기서 막힐 수 있는데, 방데르몽드의 항등식을 이용하자!  <p>
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(X&plus;Y&space;=&space;k)&space;=&space;\binom{m&plus;n}{k}&space;P^{k}&space;q^{m&plus;n-k}" title="P(X+Y = k) = \binom{m+n}{k} P^{k} q^{m+n-k}" /></p>

## 이항분포가 아닌데, 이항분포라고 생각하는 경우
* 항상 이항분포에서 생각해야 할 점은, <b>시행이 독립적인가? </b> 와 <b>성공확률이 동일한가? </b> 이다  

##### ex 1) 52개의 카드 덱에서 5개를 뽑았을 때, 꺼낸 카드에서 에이스 카드 개수의 확률분포?
* 크기 5의 모든 부분 집합은 동등한 확률로 분포(52 C 5의 경우의 수는 항상 동일한 확률이라는 뜻)  
* 에이스 카드를 뽑는 사건은 <b>'이산적'</b>이다. 즉, PMF를 구하는 것이 편리하다  
* Let X = # aces  
* P(X = k) = k가 0,1,2,3,4가 아니라면 확률은 0  
  * 이런 문제를 풀 때, 경우의 수를 전부 다 나열하는 것도 도움이 됨  
* 보통 PMF를 구할 때 실수하는 것은 도합 1이 되지 않는 PMF를 구하거나, 불가능 한 값을 포함시키는 경우가 많음  
* 결과적으로 이항분포가 아니다. why? <b>시행이 독립적이지 않기 때문!</b>  
  * 첫 번째 카드가 ace면, 뒤로 가는 시행일수록 ace 카드가 나올 확률이 줄어든다!  
* 그렇다면 이 문제의 확률변수의 PMF는?  
<p align="center"> <img src="https://latex.codecogs.com/gif.latex?P(X&space;=&space;k)&space;=&space;\frac{\binom{4}{k}&space;\binom{48}{5-k}&space;}{\binom{52}{5}}" title="P(X = k) = \frac{\binom{4}{k} \binom{48}{5-k} }{\binom{52}{5}}" /></p>

* 이 문제와 같은 확률 변수의 분포는 초기하분포(Hypergeometric distribution) 이라고 함  
* 52개의 카드가 10만장으로 늘어나고 5개의 ace카드를 뽑는 경우의 수의 확률이라면?  
  * 잘 생각해보자. 이는 이항분포로 점점 수렴해간다!!!!  

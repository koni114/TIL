# 9강- 기댓값, 지시확률변수와 선형성 (Expectation, Indicator Random Variables, Linearity)
* 평균 어떻게 구할 것인가?  
* 평균의 뜻? 확률 변수의 평균은?  

## 핵심 키워드  
* 누적분포함수(CDF)  
* 독립 확률변수  
* 기댓값(expectation)  
* 지시확률변수  
* 선형성(linearity)  
* 기하분포  

## Cumulative Density Function(CDF)
* 누적분포함수라고 함  
* 모든 확률변수에 대해서 성립. 꼭 이산확률변수에만 성립되는 것이 아님  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=CDF&space;=&space;F(x)&space;=&space;P(X&space;\leq&space;x),&space;as&space;\&space;a&space;\&space;function&space;\&space;of&space;\&space;real" target="_blank"><img src="https://latex.codecogs.com/gif.latex?CDF&space;=&space;F(x)&space;=&space;P(X&space;\leq&space;x),&space;as&space;\&space;a&space;\&space;function&space;\&space;of&space;\&space;real" title="CDF = F(x) = P(X \leq x), as \ a \ function \ of \ real" /></a></p>

### CDF의 그래프 특성  
* discrete할 경우 CDF의 예시를 그려보자  
 ![img](https://github.com/koni114/Harvard_Statistics/blob/master/image/CDF%EC%98%88%EC%8B%9C.png)  
* 계단형을 가짐. 이번 예시는 0, 1, 2, 3으로 하지만 무한대 일 수 있음  
* 1,2,3 일때 좌극한의 값은 취하지 않음. 1일 때 값이 커지기 때문  
* 만약 CDF에서 PDF의 값을 알고 싶으면 jump size를 알아야 함  
* jump의 크기를 모두 더하면 1  

* F(x)를 이용해서 P(1 <= X <= 3 ) 을 구해보자  
  * P(X <= 3) - P(X <= 1) 은 틀린 정답. 부등호를 조심해야 함  
  * P(X <= 1) + P(1 < X <= 3) = P(X <= 3)    
  * P(1 < X <= 3) = F(3) - F(1)  
  * PMF를 계산하는 경우 부등호의 여부에 따라 계산식이 달라지므로 주의  

## CDF의 3가지 특성  
* (1). increasing  
  * F(x) = P(X <= x) 라는 식을 보면    
  X가 커질수록 당연히 포함되는 사건이 커지므로 True  

* (2) right continuous  
  *  우연속 계단함수는 연속적일 수 있음  
  * 그래프 자체는 비연속적이지만 우연속!  
  * 아까 그래프에서 우극한을 생각해보면  오른쪽에서 접하면 continuous 하지만   
  좌극한은 성립하지 않음  
  예를들어 3일때는 왼쪽으로 접근하면 3일 때 값이 jump  

* (3) F(x) 의 극한 성질  
  * x가 -무한대이면, 0으로 도달  
  * x가 +무한대이면, 1로 도달  

*  <b>3가지 속성과 CDF는 등가교환</b>   
discrete이든, continuous든 CDF의 3가지 속성 존재  

## 확률변수의 독립성  
확률변수의 독립성에 대한 정의  
* X, Y 확률변수가 독립성을 가진다고 해보자  
* 개념은 확률변수를 사건들에 관련시키는 것  
* P(X <= x, Y <= y) = P(X <= x) * P(Y <= y) 등식이 성립할 때   
확률 변수 X,Y가 독립이라고 할 수 있음  
  * 이 때 좌변을 joint CDF라고 함  
  * X, Y에 대한 확률을 동시에 보라는 것인데, X,Y가 독립적이라면 단순히 각각의 확률을 곱하는 값이 됨  
* 이산인 경우  
P(X = x, Y = y) = P(X = x) * P(Y = y)  

## 평균 (Averages, Means, Expected Value..)  
* 만약 아무설명 없이 평균을 말한다면 Means를 의미  
* 또는 Expected Value(기대값)이라고 통용  

### 확률변수의 평균  
* 매우 중요  
* r.v는 직접 실험하기 전에는 모른다는 것을 기억해야함  
그전에 평균이 무엇인지 예측해보고자 하는 것  
* 사실은 <b>분포의 중간</b>이라는 의미가 더 중요  
  *  평균이 분포의 중간이라는 것을 알려줌  
* 복잡한 분포를 <b>하나의 값</b>으로 알려준다  

### 평균 구하는 방법
* (1) 다 더해서 나누기  
  * ex) 1, 2, 3, 4, 5, 6 의 평균?   
  1+2+3+4+5+6 / 6 = 3.5  
* (2) 가중평균(weighted average)으로 구하기  
  * ex) 1,1,1,1,1,3,3,5 의 평균?   
   5/8 * 1 + 2/8 * 3 + 1/8  * 5 = 2  
   * 이 가중평균 계산식의 확률변수의 평균을 구하는 것과 동일  
   * 다음과 같은 이론을 확률변수에 확장  

## 확률변수의 기댓값 정의  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=&space;\sum_{x}^{&space;}&space;x&space;\cdot&space;P(X&space;=&space;x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=&space;\sum_{x}^{&space;}&space;x&space;\cdot&space;P(X&space;=&space;x)" title="E(x) = \sum_{x}^{ } x \cdot P(X = x)" /></a></p>

* E(x) : 통계에서의 표준 표기법. Expected Value의 줄임말  
* 위의 식은 기대값을 나타내기 가장 좋은 방법 중 하나. 실제로는 다른 방법도 있음  
* 양수 P(X = x)일 때 실수 X에 대한 합을 구하는 것  

### 기댓값 예시 - 베르누이의 기댓값
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X&space;\sim&space;Bern(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;\sim&space;Bern(p)" title="X \sim Bern(p)" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=&space;1&space;\cdot&space;P(X&space;=&space;1)&space;&plus;&space;0&space;\cdot&space;P(X&space;=&space;0)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=&space;1&space;\cdot&space;P(X&space;=&space;1)&space;&plus;&space;0&space;\cdot&space;P(X&space;=&space;0)" title="E(x) = 1 \cdot P(X = 1) + 0 \cdot P(X = 0)" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=&space;1&space;\cdot&space;P(X&space;=&space;1)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=&space;1&space;\cdot&space;P(X&space;=&space;1)" title="E(x) = 1 \cdot P(X = 1)" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=&space;p" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=&space;p" title="E(x) = p" /></a></p>

* 사실은 좀 더 깊은 뜻을 가지고 있음  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X&space;=&space;\left\{\begin{matrix}&space;1,&space;\&space;occur&space;\&space;event&space;\&space;P&space;&&space;\\&space;0,&space;\&space;not&space;\&space;occur&space;\&space;event&space;\&space;P&space;&&space;\end{matrix}\right." target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;=&space;\left\{\begin{matrix}&space;1,&space;\&space;occur&space;\&space;event&space;\&space;P&space;&&space;\\&space;0,&space;\&space;not&space;\&space;occur&space;\&space;event&space;\&space;P&space;&&space;\end{matrix}\right." title="X = \left\{\begin{matrix} 1, \ occur \ event \ P & \\ 0, \ not \ occur \ event \ P & \end{matrix}\right." /></a></p>
<p align="center">E(x) = P(A) 인데, 이를 지시확률변수로 생각해 볼 수 있음</p>
<p align="center">지시확률변수는 사건이 일어나면 1, 아니면 0</p>
<p align="center">정의에 의해 이는 Bern임을 알 수 있음</p>
<p align="center">지시확률변수가 1일 확률은 A사건이 일어날 확률과 같음</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=&space;P(A)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=&space;P(A)" title="E(x) = P(A)" /></a></p>
<p align="center">지시의 기대값 = A사건이 일어날 확률</p>
<p align="center">이는 기대값과 확률을 연결 시켜 줌</p>
<p align="center">교수님은 이를 fundamental bridge라고 함</p>

### 기댓값 예시 - 이항확률변수의 기댓값
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=&space;\sum_{k&space;=&space;0}^{n}&space;k&space;\cdot&space;\binom{n}{k}&space;\cdot&space;p^{k}&space;q^{n-k}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=&space;\sum_{k&space;=&space;0}^{n}&space;k&space;\cdot&space;\binom{n}{k}&space;\cdot&space;p^{k}&space;q^{n-k}" title="E(x) = \sum_{k = 0}^{n} k \cdot \binom{n}{k} \cdot p^{k} q^{n-k}" /></a></p>
<p align="center">3장에서 story proof 2번째 공식을 이용하면</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=&space;\sum_{k&space;=&space;0}^{n}&space;n&space;\cdot&space;\binom{n-1}{k-1}&space;\cdot&space;p^{k}&space;q^{n-k}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=&space;\sum_{k&space;=&space;0}^{n}&space;n&space;\cdot&space;\binom{n-1}{k-1}&space;\cdot&space;p^{k}&space;q^{n-k}" title="E(x) = \sum_{k = 0}^{n} n \cdot \binom{n-1}{k-1} \cdot p^{k} q^{n-k}" /></a></p>
<p align="center">위의 식으로 변형한 이유는 k가 번거롭기 때문</p>
<p align="center">n을 밖으로 빼자</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=n&space;\cdot&space;\sum_{k&space;=&space;0}^{n}&space;\binom{n-1}{k-1}&space;\cdot&space;p^{k}&space;q^{n-k}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=n&space;\cdot&space;\sum_{k&space;=&space;0}^{n}&space;\binom{n-1}{k-1}&space;\cdot&space;p^{k}&space;q^{n-k}" title="E(x) =n \cdot \sum_{k = 0}^{n} \binom{n-1}{k-1} \cdot p^{k} q^{n-k}" /></a></p>
<p align="center">이항 정리를 이용하기 위해  j = k-1 로 치환하면 </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=np&space;\cdot&space;\sum_{k&space;=&space;0}^{n}&space;\binom{n-1}{j}&space;\cdot&space;p^{j}&space;q^{n-j-1}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=np&space;\cdot&space;\sum_{k&space;=&space;0}^{n}&space;\binom{n-1}{j}&space;\cdot&space;p^{j}&space;q^{n-j-1}" title="E(x) =np \cdot \sum_{k = 0}^{n} \binom{n-1}{j} \cdot p^{j} q^{n-j-1}" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=np" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=np" title="E(x) =np" /></a></p>

### 기댓값의 선형성을 이용한 이항분포의 기댓값 계산
* 이항분포는 독립적이고 동일하게 분포된 Bern(p)의 n개의 합이라는 것을 이용  
* Bern(p)는 기대값 p를 가지고 있고 n개가 있으므로, = np  

### 초기하확률변수의 기댓값 계산  
* 예시를 통해 기대값 계산 방법을 접근해보자  
<p align="center">5개의 카드를 뽑을 때, Ace카드가 나올 사건을 </p>
<p align="center">지시확률변수의 관점에서 생각해보자</p>
<p align="center">E(x)는 무엇일까? </p>
<p align="center">Xj를 j번째 카드가 Aces 일 때의 지시확률이라고 해보자</p>
<p align="center">이 때 5개의 카드에 순서를 부여해보자</p>
<p align="center">문제에서는 제시되지 않았지만 그렇게 생각해도 무방</p>
<p align="center">5개의 지시확률이 있을때의 기댓값은 </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(X_{1})&space;&plus;&space;E(X_{2})&space;&plus;&space;E(X_{3})&space;&plus;&space;E(X_{4})&space;&plus;&space;E(X_{5&space;})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X_{1})&space;&plus;&space;E(X_{2})&space;&plus;&space;E(X_{3})&space;&plus;&space;E(X_{4})&space;&plus;&space;E(X_{5&space;})" title="E(X_{1}) + E(X_{2}) + E(X_{3}) + E(X_{4}) + E(X_{5 })" /></a></p>
<p align="center">5개의 기댓값들은 선형성에 의해 모두 동일하다 </p>
<p align="center">왜 그럴까? </p>
<p align="center">우선적으로 지시확률끼리 의존적이여도 기댓값은 같고</p>
<p align="center">다른 분포가 아니고 같은 분포이기 때문이다</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;5E(X_{1})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;5E(X_{1})" title="= 5E(X_{1})" /></a></p>
<p align="center">fundamental bridge에 의해 </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;5&space;\cdot&space;P(1st\&space;Ace)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;5&space;\cdot&space;P(1st\&space;Ace)" title="= 5 \cdot P(1st\ Ace)" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;5&space;\cdot&space;\frac{1}{13}&space;=&space;\frac{5}{13}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;5&space;\cdot&space;\frac{1}{13}&space;=&space;\frac{5}{13}" title="= 5 \cdot \frac{1}{13} = \frac{5}{13}" /></a></p>
<p align="center">이 식은 초기하의 기대값 계산과 동일하다 </p>

## Geometric DIstribution(기하 분포)
* X ~ Geom(p) : 여러번의 Bern(p) 시행에서 첫 성공까지의 실패 수 X  
* 매개변수 p가 있는 기하분포  
* hypergeometic과는 크게 관련이 없음  
* 실제로 geometric sequence(등비수열)에서의 등비의 뜻  
* '첫 성공' 전에 얼마나 많은 실패가 있는지 알려줌  
* 특정 교과서에서는 성공을 세지 않음  
  * 성공 포함 여부를 조심!    

### 기하확률변수의 PMF  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=P(X&space;=&space;k)&space;=&space;q^{k}\cdot&space;p,&space;\&space;k&space;\&space;\epsilon&space;\&space;(0,&space;1,&space;2,&space;3...)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(X&space;=&space;k)&space;=&space;q^{k}\cdot&space;p,&space;\&space;k&space;\&space;\epsilon&space;\&space;(0,&space;1,&space;2,&space;3...)" title="P(X = k) = q^{k}\cdot p, \ k \ \epsilon \ (0, 1, 2, 3...)" /></a></p>

* 이항확률변수는 n이 정해져 있지만, 기하분포에서는 성공할때 까지 계속함  
* ex) FFFFFS (F : 실패, S : 성공). P(X = 5), = q^5 * p

### 기하확률변수 PMF 의 유효성 검증
* 모든 확률의 합이 1이되는지 확인하자.  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{k&space;=1}^{\infty}&space;pq^{k}&space;=&space;p&space;\cdot&space;\sum_{k&space;=1}^{\infty}&space;q^{k}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{k&space;=1}^{\infty}&space;pq^{k}&space;=&space;p&space;\cdot&space;\sum_{k&space;=1}^{\infty}&space;q^{k}" title="\sum_{k =1}^{\infty} pq^{k} = p \cdot \sum_{k =1}^{\infty} q^{k}" /></a></p>
<p align="center">이 때, 등비수열의 무한급수를 이용하면 </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;p&space;\cdot&space;\frac{1}{1-q}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;p&space;\cdot&space;\frac{1}{1-q}" title="= p \cdot \frac{1}{1-q}" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;1" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;1" title="= 1" /></a></p>
<p align="center">여기서 등비수열을 사용했기 때문에 </p>
<p align="center">geometric function이라고 함</p>

### 기하확률변수의 기댓값 계산  
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=X&space;\sim&space;Geom(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;\sim&space;Geom(p)" title="X \sim Geom(p)" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=&space;\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;pq^{k}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=&space;\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;pq^{k}" title="E(x) = \sum_{k = 0}^{\infty } k \cdot pq^{k}" /></a></p>
<p align="center">먼저 p를 바깥으로 빼면 </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=&space;p&space;\cdot&space;\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;q^{k}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=&space;p&space;\cdot&space;\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;q^{k}" title="E(x) = p \cdot \sum_{k = 0}^{\infty } k \cdot q^{k}" /></a></p>
<p align="center">여기서 k를 없애는 것이 중요 </p>
<p align="center">우리가 알고있는 사실은 등비수열이라는 것</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{k&space;=&space;0}^{\infty&space;}&space;q^{k}&space;=&space;\frac{1}{1-q}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{k&space;=&space;0}^{\infty&space;}&space;q^{k}&space;=&space;\frac{1}{1-q}" title="\sum_{k = 0}^{\infty } q^{k} = \frac{1}{1-q}" /></a></p>
<p align="center">이를 미분해서 k를 앞으로 빼내자</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;q^{k-1}&space;=&space;\frac{1}{(1-q)^{2}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;q^{k-1}&space;=&space;\frac{1}{(1-q)^{2}}" title="\sum_{k = 0}^{\infty } k \cdot q^{k-1} = \frac{1}{(1-q)^{2}}" /></a></p>
<p align="center">pq를 곱하면 </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=p&space;\cdot&space;\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;q^{k}&space;=&space;\frac{pq&space;}{(1-q)^{2}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?p&space;\cdot&space;\sum_{k&space;=&space;0}^{\infty&space;}&space;k&space;\cdot&space;q^{k}&space;=&space;\frac{pq&space;}{(1-q)^{2}}" title="p \cdot \sum_{k = 0}^{\infty } k \cdot q^{k} = \frac{pq }{(1-q)^{2}}" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex==&space;\frac{q}{p}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?=&space;\frac{q}{p}" title="= \frac{q}{p}" /></a></p>

### 기하확률변수의 기댓값(story proof + 선형성 이용)
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=C&space;=&space;E(x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?C&space;=&space;E(x)" title="C = E(x)" /></a></p>
<p align="center">앞면이 나올 확률이 p인 동전을 앞면이 나올때까지</p>
<p align="center">계속 뒤집는다고 하자</p>
<p align="center">성공한 경우 = (현재 - 1) 실패한횟수 x p</p>
<p align="center">실패한 경우 = (현재 실패한횟수 + E(x)) x q </p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=C&space;=&space;0&space;\cdot&space;p&space;&plus;&space;(1&space;&plus;&space;C)&space;\cdot&space;q" target="_blank"><img src="https://latex.codecogs.com/gif.latex?C&space;=&space;0&space;\cdot&space;p&space;&plus;&space;(1&space;&plus;&space;C)&space;\cdot&space;q" title="C = 0 \cdot p + (1 + C) \cdot q" /></a></p>
<p align="center">한 번 실패했을때, 1이고</p>
<p align="center">다시 반복한다는 것이 핵심</p>
<p align="center">1 + C 가 된다</p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=C&space;=&space;q&space;&plus;&space;Cq" target="_blank"><img src="https://latex.codecogs.com/gif.latex?C&space;=&space;q&space;&plus;&space;Cq" title="C = q + Cq" /></a></p>
<p align="center"><a href="https://www.codecogs.com/eqnedit.php?latex=C&space;=&space;\frac{q}{p}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?C&space;=&space;\frac{q}{p}" title="C = \frac{q}{p}" /></a></p>

# 10강 - 기댓값(Expectation Continued)

## 핵심 키워드
* 선형성  
* 음이항분포(negative binomial)  
* First success  



## 교수님만의 기대값 선형성 증명

* 전 수업 때 평균 구하는 2가지 방법에 대해 이야기함  
  * 다 더해서 나눔  
  * 가중 평균 계산  

* 위의 두가지 방법을 이용해서 증명을 진행해보자  

<p align = "center">두 확률변수의 합이 있다고 해보자</p>
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=T&space;=&space;X&space;&plus;&space;Y" target="_blank"><img src="https://latex.codecogs.com/gif.latex?T&space;=&space;X&space;&plus;&space;Y" title="T = X + Y" /></a></p>
<p align = "center">이 식이 E(X) + E(Y)임을 보이면 됨</p>
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(T)&space;=&space;E(X)&space;&plus;&space;E(Y)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(T)&space;=&space;E(X)&space;&plus;&space;E(Y)" title="E(T) = E(X) + E(Y)" /></a></p>
<p align = "center">증명을 2가지 방법으로 해볼텐데, 먼저 정의를 이용해보자</p>
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{t}^{&space;}&space;t\cdot&space;P(T&space;=&space;t)&space;=&space;\sum_{x}^{&space;}&space;x&space;\cdot&space;P(X&space;=&space;x)&space;&plus;&space;\sum_{y}^{&space;}&space;y&space;\cdot&space;P(Y&space;=&space;y)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{t}^{&space;}&space;t\cdot&space;P(T&space;=&space;t)&space;=&space;\sum_{x}^{&space;}&space;x&space;\cdot&space;P(X&space;=&space;x)&space;&plus;&space;\sum_{y}^{&space;}&space;y&space;\cdot&space;P(Y&space;=&space;y)" title="\sum_{t}^{ } t\cdot P(T = t) = \sum_{x}^{ } x \cdot P(X = x) + \sum_{y}^{ } y \cdot P(Y = y)" /></a></p>
<p align = "center">이 식을 어떻게 풀 것인지 전략을 생각해야 하는데,</p>
<p align = "center">1. 왼쪽 식을 풀어 오른쪽 식과 같게 하거나, </p>
<p align = "center">2. 오른쪽 식을 풀어 왼쪽 식과 같게 할 수 있음</p>
<p align = "center"><b>조건부 확률</b>을 활용해 1번 전략으로 풀어보자 </p>
<p align = "center">좌변 식을 조건부 확률로 풀어 쓰면, </p>
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{t}^{&space;}&space;P(T&space;=&space;t)&space;=&space;\sum_{x}^{&space;}&space;P(T&space;=&space;t|X&space;=&space;x)&space;\cdot&space;P(X&space;=&space;x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{t}^{&space;}&space;P(T&space;=&space;t)&space;=&space;\sum_{x}^{&space;}&space;P(T&space;=&space;t|X&space;=&space;x)&space;\cdot&space;P(X&space;=&space;x)" title="\sum_{t}^{ } P(T = t) = \sum_{x}^{ } P(T = t|X = x) \cdot P(X = x)" /></a></p>
<p align = "center">만약 X, Y가 독립적이라면 간단하게 가능</p>
<p align = "center">How? 이 전에 X+Y ~ Bin(m+n, k)처럼.. </p>
<p align = "center">하지만 dependent 하다면 P(T = t|X = x) 를 풀어낼 수 없음 </p>
<p align = "center">다른 방식으로 접근해보자</p>


### 조약돌 예시  


* X가 4개의 가능한 값 들이 있다고 하고, 표본 공간을 열로 배열  
* 확률변수는 Sample Space에서 mapping 이라는 것을 상기하자  
* 표본공간은 실제 조약돌들의 집합  
이때 조약돌들을 배열한다고 가정하자  
* X는 이 4가지 가능한 값들을 가지고 있다고 가정하면 이는 이산확률변수에도 성립  
ex) 어떤 시행(experiment)을 했는데, 이는 다양(조약돌 각각을 의미)하지만, 4개 중 하나로 grouping해서 확률변수 X로 나타내겠다! 라는 의미인 듯  
* 즉, <b> 각각 가중 평균의 합(0,1,2,3) = 전체 더한 것의 합 </b> 으로 나타낼 수 있음  
* 그러면 어떻게 합을 구할지 관찰해보자  

<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(x)&space;=&space;\sum_{x}^{&space;}&space;X&space;\cdot&space;P(X=&space;x)&space;=&space;\sum_{s}^{&space;}&space;X(s)&space;\cdot&space;P(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(x)&space;=&space;\sum_{x}^{&space;}&space;X&space;\cdot&space;P(X=&space;x)&space;=&space;\sum_{s}^{&space;}&space;X(s)&space;\cdot&space;P(s)" title="E(x) = \sum_{x}^{ } X \cdot P(X= x) = \sum_{s}^{ } X(s) \cdot P(s)" /></a></p>

<p align = "center">좌변은 가중 평균의 합,  우변은 전체 값의 합의 평균을 의미</p>
<p align = "center">P(s)는 조약돌 각각 마다의 질량을 의미할 것이고,</p>
<p align = "center">X(s)는 각 조약돌마다 mapping되는 X 값. X는 함수를 의미함</p>
<p align = "center">이 방법을 잘 생각해보면 꽤 명백하다</p>
<p align = "center">좌변 - 우변이 grouped - ungrouped 임을 알 수 있음</p>
<p align = "center">조약돌에 대한 합을 구하는 것은 각각의 조약돌은 어떤 값(0,1,2,3)에 지정되어 있고 </p>
<p align = "center">이들을 한 번에 평균을 구하는 것(우변)</p>
<p align = "center">우변식도 가중평균이긴하다. 각 조약돌은 서로 확률(질량)을 가지고 있기 때문</p>
<p align = "center">하지만 전체의 평균을 구하는 느낌임을 알 수 있음</p>

<p align = "center">grouped 같은 경우는</p>
<p align = "center">엄청나게 큰 조약돌 덩어리로 뭉쳐 함께 붙이면 </p>
<p align = "center">큰 조약돌은 질량들의 합과 같은 질량을 가지고 있다고 생각할 수 있음 </p>
<p align = "center">다시 돌아와서 이산인 경우의 선형성을 증명해보자</p>

### 이산인 경우 선형성 증명
<p align = "center">X 대신 T에 대한 같은 특성을 사용</p>
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(X)&space;=&space;\sum_{s}^{&space;}&space;(X&plus;Y)(s)&space;\cdot&space;P(s)" target="_blank"><a href="https://www.codecogs.com/eqnedit.php?latex=E(T)&space;=&space;\sum_{s}^{&space;}&space;(X&plus;Y)(s)&space;\cdot&space;P(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(T)&space;=&space;\sum_{s}^{&space;}&space;(X&plus;Y)(s)&space;\cdot&space;P(s)" title="E(T) = \sum_{s}^{ } (X+Y)(s) \cdot P(s)" /></a></p>
<p align = "center">여기서 X+Y는 두 함수를 더한다는 의미</p>
<p align = "center">즉 함수를 2개 더하고 난 후의 값과 각 함수의 값을 각각 더한 값은 같음</p>
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=\sum_{s}^{&space;}(X&plus;Y)(s)&space;=&space;\sum_{s}^{&space;}X(s)&space;&plus;&space;\sum_{s}^{&space;}Y(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\sum_{s}^{&space;}(X&plus;Y)(s)&space;=&space;\sum_{s}^{&space;}X(s)&space;&plus;&space;\sum_{s}^{&space;}Y(s)" title="\sum_{s}^{ }(X+Y)(s) = \sum_{s}^{ }X(s) + \sum_{s}^{ }Y(s)" /></a></p>
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(T)&space;=&space;(\sum_{s}^{&space;}X(s)&space;&plus;&space;\sum_{s}^{&space;}Y(s))\cdot&space;P(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(T)&space;=&space;(\sum_{s}^{&space;}X(s)&space;&plus;&space;\sum_{s}^{&space;}Y(s))\cdot&space;P(s)" title="E(T) = (\sum_{s}^{ }X(s) + \sum_{s}^{ }Y(s))\cdot P(s)" /></a></p>
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(T)&space;=&space;\sum_{s}^{&space;}(X(s))&space;P(s)&space;&plus;&space;\sum_{s}^{&space;}(Y(s))P(s)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(T)&space;=&space;\sum_{s}^{&space;}(X(s))&space;P(s)&space;&plus;&space;\sum_{s}^{&space;}(Y(s))P(s)" title="E(T) = \sum_{s}^{ }(X(s)) P(s) + \sum_{s}^{ }(Y(s))P(s)" /></a></p>
<p align = "center">위의 정리된 식에 의해</p>
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(X&plus;Y)&space;=&space;E(X)&space;&plus;&space;E(Y)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X&plus;Y)&space;=&space;E(X)&space;&plus;&space;E(Y)" title="E(X+Y) = E(X) + E(Y)" /></a></p>

### 상수 곱에 대한 선형성 확인
* 기대값에 상수를 곱할 수 있음
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(cx)&space;=&space;c&space;\cdot&space;E(x)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(cx)&space;=&space;c&space;\cdot&space;E(x)" title="E(cx) = c \cdot E(x)" /></a></p>
<p align = "center">실제로 이 식이 좀 더 직관적일 수 있음</p>
<p align = "center">예를 들어, 모든 숫자에 3을 곱하면 이는 기대 값에 3을 곱한 결과와 같기 때문</p>
<p align = "center">이 것이 종속적이여도 성립하는지 이해하는데 도움이 됨</p>
<p align = "center">why? 극단적인 경우에서 보는 것이 굉장히 유용하기 때문</p>
<p align = "center">극단적인 케이스인 X = Y 인 경우 생각해보자 </p>
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=E(X&space;&plus;&space;Y)&space;=&space;E(2X)&space;=&space;2&space;\cdot&space;E(X)&space;=&space;E(X&space;&plus;&space;Y)&space;=&space;E(X)&space;&plus;&space;E(Y)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?E(X&space;&plus;&space;Y)&space;=&space;E(2X)&space;=&space;2&space;\cdot&space;E(X)&space;=&space;E(X&space;&plus;&space;Y)&space;=&space;E(X)&space;&plus;&space;E(Y)" title="E(X + Y) = E(2X) = 2 \cdot E(X) = E(X + Y) = E(X) + E(Y)" /></a></p>
<p align = "center">이러한 접근은 선형성의 증명은 아니지만</p>
<p align = "center">극한의 경우 성립한다는 것을 확인할 수 있음</p>

### 앞으로..
<p align = "center">앞으로 우리는 15개 정도의 분포를 배운다</p>
<p align = "center">굉장히 많은 분포들이 있지만 중요한 이유는 유용한 story를 담고 있다는 점에서 차이가 있음</p>

## 음이항분포(Negative Binomial Distribution)

* 틀린 용어지만, 표준 용어이다  
* 실제로 음수도 아니고, 이항도 아니다  
* 실제로는 기하 분포의 일반화 분포!  
* 2개의 변수가 있음 -> (r, p)  
r개의 성공을 원하는 경우의 연장선  
* 독립적인 베르누이 p가 있고, r번째 성공 전의 실패 횟수를 알고 싶음  

### PMF  
* 간단한 그림을 그려 접근  
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=PMF&space;:&space;\binom{n&plus;r-1}{r-1}&space;P^{r}(1-P)^{n}&space;,&space;n&space;=&space;0,&space;1,&space;2,&space;..." target="_blank"><img src="https://latex.codecogs.com/gif.latex?PMF&space;:&space;\binom{n&plus;r-1}{r-1}&space;P^{r}(1-P)^{n}&space;,&space;n&space;=&space;0,&space;1,&space;2,&space;..." title="PMF : \binom{n+r-1}{r-1} P^{r}(1-P)^{n} , n = 0, 1, 2, ..." /></a></p>  

* 총 성공 실패를 합친 개수 중, 실패 또는 성공의 개수 만큼 뽑기. r은 성공의 수, n은 실패의 수  
* 그렇다면 왜 음이항(Negative Binomial) 이라고 할까?  
실제로 이항정리에서의 음수승과 관련이 있기 때문  

### 기대값
* 극단적인 경우를 생각하자(r = 1)  
geometric 이고, 기대값이 q/p 였음  

* 전략 : r번의 성공을 첫번째 성공 기다리고.. 두번째 성공 기다리고.. 세번째 성공 기다리고.. 처럼 각각의 독립 시행 처럼 생각할 수 있음  
* E(X) = E(X1 + X2 + X3 + X4 ... Xr) = E(X1) + E(X2) + E(X3) ... + E(Xr) = r x (q/p)  
  * Xj는 실패의 횟수일 때  
  X1은 첫번째 성공까지의 실패 횟수  
  X2는 첫 번째 성공과 두 번째 성공 사이의 횟수  
  * Xj ~ Geom(p)  

### 기하와 음이항의 convention에 대해 조심하기
* 성공의 개수를 1부터 시작하는지, 0부터 시작하는지 생각해야함  
* 둘 다 흔한 경우이므로 조심하자  
  * 데구르트(?) : 0부터 시작  
  * 로스 : 1부터 시작  


## 성공분포(First Success distribution)
<p align = "center"><a href="https://www.codecogs.com/eqnedit.php?latex=X&space;\sim&space;FS(p)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X&space;\sim&space;FS(p)" title="X \sim FS(p)" /></a></p>

* 첫 성공까지 걸리는 시간, 성공의 개수를 셈  
* 우리는 Y = X-1로 치환할 수 있고, Y ~ Geom(P)  
* E(X) = E(Y) + 1 = (q/p) + 1 = 1/p  
  * 첫 성공의 기대 값으로는 단순해 보이는데, 실제로 굉장히 직관적임  
  * 예를 들어 성공의 확률이 0.1이면, 평균 10번의 시행이 있어야 성공한다는 뜻  

### 기대값에 대한 예시
* putnam Exam 설명  
  * 1부터 n까지의 임의의 순열이 있고, 순열 배치는 random(확률은 같음). n은 적어도 2  
  * 문제는 극댓값의 개수의 기대값을 찾는 문제  
  * 극대값 :  
    * 중간에 있는 수는 양쪽에 있는 수보다 커야 함  
    * 양쪽에 있는 수는 그 옆에 있는 수보다 커야 함  
 * 이 문제는 세계에서 가장 어려운 경시 대회 문제 중 가장 어려운 문제 중 하나였는데,  
 대수학이 아닌 확률로 계산하면 쉽게 접근이 가능!  
 * 문제 풀이  
   * 지시확률변수를 생각해보자  
   * Ij가 자리 j에 대한 극대값의 지시확률변수라고 하자  
   * E(I1 + I2 + I3 ... In ) = E(I1) + E(I2) + E(I3) ... E(In) = ( n-2 /3 )  + (2/2) = (n+1) / 3  
     * (n-2)/3 = 중간에 있는 숫자 개수 n-2 * 가운데 있는 숫자가 양쪽 숫자보다 높을 확률 1/3  
     * (2/2) = 양 끝에 있는 숫자 개수 2 * 양 끝에 있는 숫자가 클 확률 1/2  
   * 가운데 있는 숫자가 양쪽 숫자보다 높을 확률 = 2/6  
= (가운데 있는 숫자가 양쪽보다 높을 확률 = 3번 중 1번) / (3개의 숫자가 배열 될 확률)  

* 많이 실수 하는 것  
  * 1/4라고 생각하기 쉽다  
  why?  a b c 의 숫자가 배열되어 있을 때,  
  b가 a보다 클 확률 1/2  
  b가 c보다 클 확률 1/2  
 따라서 1/2 * 1/2 = 1/4 라고 생각한다  
 but 이것은 틀린 풀이! -> 각각의 사건이 독립이 아니기 때문이다  

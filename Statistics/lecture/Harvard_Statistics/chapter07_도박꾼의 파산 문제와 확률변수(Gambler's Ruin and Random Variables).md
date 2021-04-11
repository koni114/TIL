# 7강- 도박꾼의 파산 문제와 확률변수 (Gambler's Ruin and Random Variables)

## 핵심 키워드
* Gambler's Ruin(도박꾼의 파산)  
* 계차방정식  
* 확률변수  
* 확률분포  
* 확률질량함수

## 도박꾼의 파산 문제(Gambler's Ruin)  

* A와 B 두 명의 도박꾼이 매 라운드 $1씩 걸고 도박을 함  
* 이긴 사람은 상대방의 $1을 가져가고, 둘 중 한 명이 가지고 온 돈이 바닥날 때까지 이 과정을 반복함  
* 사건 정의  
  * p = A가 특정 라운드를 이길 확률, P(A win)  
  * q = 1-p  

* A는 i 달러, B는 N-i 달러를 가지고 게임을 시작 할 때, A를 기준으로 보면 다음과 같음  

![img](https://github.com/koni114/Harvard_Statistics/blob/master/image/%EB%8F%84%EB%B0%95%EA%BE%BC%ED%8C%8C%EC%82%B0.JPG)    

* p의 확률로 A가 1달러를 얻고, q의 확률로 1달러를 잃음  
* 0과 N은 흡수 상태(absorbing state)라고 하며, 게임 종료를 나타냄  

<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P_{i}&space;=&space;P*P_{i&plus;1}&space;&plus;&space;q*P_{i-1}" title="P_{i} = P*P_{i+1} + q*P_{i-1}" /></p>  

* 사건 정의  
  * Pi = A가 i달러를 가지고 있을 때 게임을 이길 확률  
  * 1 <= i <= N-1 (i기 0과 N이면 게임은 종료된다)  
  * P0 = 0, Pn = 1  

* 이를 <b>계차방정식(difference equation)</b>이라고 함. (미분방정식의 이산 형태)  

##### 추측을 통한 문제 접근  
* Pi 가 특정 값을 가진다고 추측하여 방정식의 해를 생각해 보는 것  
* 실제로 해를 찾을 수는 없다. 하지만 유용한 정보를 제공!  

* Pi = X^i 라고 추측  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P_{i}&space;=&space;x^{i},&space;x^{i}&space;=&space;px^{i&plus;1}&space;&plus;&space;qx^{i-1}" title="P_{i} = x^{i}, x^{i} = px^{i+1} + qx^{i-1}" /></p>
<p align = 'center'>x는 0이 아니므로, </p>  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?px^{2}&space;-x&space;&plus;&space;q&space;=&space;0" title="px^{2} -x + q = 0" /></p>  
<p align = 'center'>근의 공식을 이용하여 해를 나타내면, </p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?x&space;=&space;\frac{1&space;\pm&space;\sqrt{1&space;-&space;4pq}}{2p}" title="x = \frac{1 \pm \sqrt{1 - 4pq}}{2p}" /></p>
<p align = 'center'>이 때, p = 1-q 를 이용하면 식을 간단하게 변형 가능하다 </p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?1&space;-&space;4pq&space;=&space;(2p&space;-1)^{2}" title="1 - 4pq = (2p -1)^{2}" /></p>
<p align = 'center'>따라서, 둘 중 하나의 값을 가진다</p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\begin{cases}&space;&&space;x=&space;1\\&space;&&space;x=&space;\frac{(1-p)}{p}&space;=&space;\frac{q}{p}&space;\end{cases}" title="\begin{cases} & x= 1\\ & x= \frac{(1-p)}{p} = \frac{q}{p} \end{cases}" /></p>
<p align = 'center'>결과적으로 이 식은 조건을 만족하지만, 경계 조건을 만족하지 않는다.</p>
<p align = 'center'>경계 조건은 P0 = 0, Pn = 1 을 말한다</p>

##### 일반해 찾기  
* 위의 두 해에 대한 일반식은 다음과 같다  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P_{i}&space;=&space;A&space;\cdot&space;I^{i}&space;&plus;&space;B&space;\cdot&space;(\frac{q}{p})^i" title="P_{i} = A \cdot I^{i} + B \cdot (\frac{q}{p})^i" /></p>

* 일반적으로 계차 방정식의 추측해를 대입하고 조건에 해당하지 않고  
그 두 해가 서로 다르다면 일반해는 그 해의 선형 결합으로 나타낼 수 있음  
(두 해가 같다면(=중근) 더 복잡해짐)  
* n개의 해가 있다면, 그 n개의 해의 선형 결합으로 나타낼 수 있음  

<p align = 'center'>위의 식에서 P0 = 0을 대입하면 </p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P_{0}&space;=&space;A&space;&plus;&space;B&space;,&space;A&space;=&space;-B" title="P_{0} = A + B , A = -B" />
<p align = 'center'>위의 식에서 Pn = 1을 대입하면 </p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?1&space;=&space;A&space;&plus;&space;B&space;\cdot&space;(\frac{q}{p})&space;^&space;{n}" title="1 = A + B \cdot (\frac{q}{p}) ^ {n}" /></p>
<p align = 'center'>이 때 A = -B를 다시 대입하면 </p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?1&space;=&space;A&space;-&space;A&space;\cdot&space;(\frac{q}{p})&space;^&space;{n}" title="1 = A - A \cdot (\frac{q}{p}) ^ {n}" /></p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?1&space;=&space;A(1&space;-&space;(\frac{q}{p})&space;^&space;{n})" title="1 = A(1 - (\frac{q}{p}) ^ {n})" /></p>
<p align = 'center'> A를 남기고 좌변으로 넘기면  </p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?A&space;=&space;\frac{1}{(1&space;-&space;(\frac{q}{p})&space;^&space;{n})}" title="A = \frac{1}{(1 - (\frac{q}{p}) ^ {n})}" /></p>


<p align = 'center'>다시 일반해로 돌아와서 A, B에 해당 값을 대입하면</p>
<p align = 'center'><p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P_{i}&space;=&space;A&space;&plus;&space;B&space;\cdot&space;(\frac{q}{p})^{i}" title="P_{i} = A + B \cdot (\frac{q}{p})^{i}" /></p></p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P_{i}&space;=&space;A&space;\cdot&space;(1&space;-&space;(\frac{q}{p})^{i})" title="P_{i} = A \cdot (1 - (\frac{q}{p})^{i})" /></p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P_{i}&space;=&space;\frac{1&space;-&space;(\frac{q}{p})^{i}}{1&space;-&space;(\frac{q}{p})^{n}},&space;p&space;\neq&space;q" title="P_{i} = \frac{1 - (\frac{q}{p})^{i}}{1 - (\frac{q}{p})^{n}}, p \neq q" /></p>
<p align = 'center'></p>

##### p = q 일때의 일반해 구하기
* p = q 이면 계차방정식의 일반해를 구하는 방법이 어려워 지므로, 극한으로 접근  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?X&space;=&space;\frac{q}{p}" title="X = \frac{q}{p}" /></p>
<p align = 'center'>앞서 구한 Pi 방정식에 X를 대입하면 </p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\lim_{x&space;\mapsto&space;1&space;}&space;\frac{1&space;-&space;X^{i}}{1&space;-&space;X^{n}}" title="\lim_{x \mapsto 1 } \frac{1 - X^{i}}{1 - X^{n}}" /></p>
<p align = 'center'>로피탈의 정리를 이용하면(분자, 분모 미분) </p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\lim_{x&space;\mapsto&space;1&space;}&space;\frac{i&space;\cdot&space;X^{i}}{N&space;\cdot&space;X^{n}}&space;=&space;\frac{i}{N}" title="\lim_{x \mapsto 1 } \frac{i \cdot X^{i}}{N \cdot X^{n}} = \frac{i}{N}" /></p>
<p align = 'center'>이는 게임에서 A와 B가 이길 확률이 50:50 일 때, </p>
<p align = 'center'>A가 이길 확률은 A가 가지고 있는 자산 i / 총 자산 이라는 것을 의미한다.</p>

##### 불공평한 경우
* i = N-i(같은 돈을 가지고 시작 할 경우),  p = 0.49, q = 0.51  
  * N = 20 일 때, A가 이길 확률 40%  
  * N = 100 일 때, A가 이길 확률 12%  
  * N = 200 일 때, A가 이길 확률 2%  

##### 게임이 무한정 반복 될 때?
* 사실은 배제하고 계산함  
* why ? A가 이기고 B가 파산할 확률과 B가 이기고 A가 파산할 확률의 합은 1이기 때문    
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\frac{i}{N}&space;&plus;&space;\frac{N&space;-&space;i}{N}&space;=&space;1" title="\frac{i}{N} + \frac{N - i}{N} = 1" /></p>

## 확률 변수(random variables)
* 위키피디아에서 random variables를 <b>'임의의 값을 가지는 변수'</b> 라고 하지만  
전혀 확률 변수에 대한 직관적인 이해가 어렵다  
* 지금까지 확률은 사건에 대해 많이 정의해 보았는데, 특히 A, B와 같은 표기법으로 많이 정의해 보았음  
  * ex1) A가 $를 가지고 시작하는 사건  
  * ex2) 시간이 7일 때 A가 i달러를 가지고 있는 사건 ...    
* 이보다 더 많은 조건들을 표기하기 위해서는 또 더 많은 사건을 정의해야하고.. 표기법은 금방 부족해질 것임  
* 수학에서는 수와 변수에 대해 많이 생각하는 것처럼 통계에서도 r.v가 필요한데, 정의하는 것은 매우 까다로움  

##### 확률변수(random variables)?
* 위키피디아 정의는, <b>"확률 변수는 무작위하고 특정한 분포를 따르는 변수이다"</b> 라고 되어 있음  
* 분포가 뭔지도 모르는데 분포를 따른다고 되어 있음  
* 분포가 뭔지 안다고 해도 확률변수가 뭔지는 알려주지 않음  
* 위키피디아의 두 번째 정의는 <b>"함수"</b> 라고 되어 있음(구간이 정해져 있고 가측인..)  
  * 실제로 정확하지만  측도론과 실해석학을 모르면 이해할 수 없음  

##### 확률 변수에서 변수(variables)란?
* 우리가 자주 사용하는 변수(variables)란 무엇일까? (ex) x + 2 = 9)  
* 실제로 x는 상수에 가깝다. 예를 들어 x + 2 = 9 에서 x = 7이라는 것을 알기 때문이다  
* x는 어떤 한 수를 뜻하는 기호이지만, 변할 수는 없다는 점. 상수를 뜻하는 기호일 뿐..    
만약 시간에 따라 변하는 값을 표현하고 싶으면 함수로 해야함  
* 즉, 확률 변수에서 변수의 의미는 없다. Why? 함수이기 때문  

##### 확률 변수(random variables)에서 무작위성(random)란?
* 함수는 결정되어 있는데, 왜 무작위성이라는 단어가 붙은 것일까?
* 무작위성이라는 단어가 붙은 이유는, S라고 불렀던 sample space의 함수인데, <b>실수에 대한 확률 시행(random experience)</b>가 있다는 것을 말함  
* 입력 값으로 S를 가지는데, random exprience에 의해 특정 실수를 가지고, 이 때 Mapping 해주는 함수가 확률 변수(random variables)인 것이다!  
* 즉 확률 변수란, <b>표본 공간에서 실수로 가는 함수</b>를 의미함  

##### 그래서 확률 변수(random variables)가 뭐라고..?
* 거두절미하고 <b>"수치적인 요약(numerical summary)"</b>라고 하자  
  이때의 요약은 전체의 random experience를 요약하는 것이 아니라 일부분을 의미한다  
* 즉 무작위성은 exprience에서 오는 것이다!  
random exprience는 다른 결과에 대해 다른 확률을 부여했음. 전체 sample space의 확률을 1로 했을 때 다른 사건은 다른 확률을 가짐  
* 확률 시행이 끝난 후에는 특정한 결과를 관찰하게 됨    
s라고 하는 결과를 시행 후에 관측하는 것    
s는 자체로써 굉장히 추상적일 수 있지만, 이를 실수로 대응 시킨 것이 random variables임  
무한대의 s가 있는데 이를 실수에 대응시킨 것!  

## 베르누이(Bernoulli) 확률 변수
* X가 0 또는 1 두개의 값만 가질 수 있음  

* P(X = 1) = p, P(X = 0) = 1-p 일 때, X는 bernoulli(p) 분포를 따른다고 함  

## 이항(Binomial) 확률 변수
* n번의 독립적인 베르누이(p) 시행에서 성공 횟수의 분포는 Bin(n,p)Bin(n,p) 를 따른다고 함  
* 이항확률변수의 확률질량함수(PMF) 는,  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(X&space;=&space;k)&space;=&space;\binom{n}{k}p^{k}q^{n-k}" title="P(X = k) = \binom{n}{k}p^{k}q^{n-k}" /><p>

* 이항확률변수의 특징  
  *  X ~ Bin(n,p),  Y ~ Bin(m,p) 일 때     
X+Y ~ Bin(n+m,p) 를 따름  

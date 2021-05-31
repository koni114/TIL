
# Birthday Problem과 확률의 특성 (Birthday Problem, Properties of Probability)

## 핵심 키워드  
* Birthday problem
* 확률의 non-naïve한 정의의 공리
* 확률의 특성
* 포함배제의 원리

## Birthday problem

#### 문제 설명
* 어떤 파티에서 사람들의 그룹이 있을 때, 두 명의 생일이 같을 확률이 최소한 50%이 넘으려면 몇명이 있어야 할까?
* 일반적으로 K명이 있을 때 2명이 생일이 같을 확률을 찾아보자

#### 문제 가정
* 윤년은 제외(2월 29일)
* 365일이 모두 동일한 확률을 가진다고 가정
		* 이는 옳은 가정일까? -> NO. 통계 조사에 의하면 계절적 특성에 따라 더 많이 태어난 월이 있음
* 각각 독립하다고 가정(출생에 대한 독립성 가정)
ex) K명의 그룹에서 쌍둥이가 많다면 확률 계산이 달라질 수 있음

#### 문제 풀이
* K가 365보다 크다면 확률은 1이된다
why? 상자가 365개 있을 때, 상자보다 점의 개수가 많으면 여러 개의 점이 들어간 상자가 1개는 생긴다
(비둘기 집의 원리)
* K가 365보다 작은 경우?
보통 K 값을 100보다 큰 수로 생각
* 정답은 23명. K = 23일 때 50.7% 정도의 확률을 가짐
	* 여사건을 생각하자. K = n명일 때, 여사건을 생각하는 것이다.
	* <img src="https://latex.codecogs.com/gif.latex?P(no&space;Match)&space;=&space;\frac{365&space;*&space;364&space;*&space;363&space;*&space;...&space;(365&space;-&space;n&space;&plus;&space;1)}{365^{n}}" title="P(no Match) = \frac{365 * 364 * 363 * ... (365 - n + 1)}{365^{n}}" />
* 즉, 1 - P(no match) >= 0.5인 n 값을 구하면 23이 나온다

#### 직관적인 이해 방법
*  k개 중에서 2개를 선택하는 경우의 수를 생각해보자
* <img src="https://latex.codecogs.com/gif.latex?\binom{k}{2}" title="\binom{k}{2}" />  인데,
k = 23 일때 252라는 경우의 수가 나오며, 이 값이 365의 절반 비스무리 하므로, 23이 50%에 근접 할 것이다! 라고 추측 할 수 있음

#### 생일이 같거나, 1 day 차이 나는 경우의 확률이 50%가 넘기 위한 K 개수는?
* 14로 줄어들게 됨!

##  확률의 정의

#### 복습
* 확률에서 P라는 함수로 정의함
* P 함수는 앞선 chapter에서 말한 2가지 공리를 만족하면 확률을 표현한다고 할 수 있음

* 공리
  * <img src="https://latex.codecogs.com/gif.latex?P(\phi)&space;=&space;0,&space;P(S)&space;=&space;1" title="P(\phi) = 0, P(S) = 1" />
  * <img src="https://latex.codecogs.com/gif.latex?P(\bigcup_{n=1}^{\infty&space;}&space;A_{n})&space;=&space;\sum_{n&space;=&space;1}^{\infty}&space;P(A_{n})" title="P(\bigcup_{n=1}^{\infty } A_{n}) = \sum_{n = 1}^{\infty} P(A_{n})" />
* 두 가지 공리를 이용해서 대부분의 속성들(properties)을 확인해보자

#### 확률의 간단한 속성 정리(Property)
* <img src="https://latex.codecogs.com/gif.latex?p(A^{c})&space;=&space;1&space;-&space;P(A)" title="p(A^{c}) = 1 - P(A)" />
* A 사건이 B 사건에 포함되면(부분집합), P(A)는 P(B) 보다 작다
<img src="https://latex.codecogs.com/gif.latex?B&space;=&space;A&space;\cup&space;P(B&space;\cap&space;A^{c})" title="B = A \cup P(B \cap A^{c})" /> 로 표현할 수 있는데,  확률은 0보다 작은 값이 나올 수 없으므로, P(B) >= P(A) 이 성립
* <img src="https://latex.codecogs.com/gif.latex?P(A&space;\cup&space;B&space;)&space;=&space;P(A)&space;&plus;&space;P(A^{c}&space;\cap&space;B)" title="P(A \cup B ) = P(A) + P(A^{c} \cap B)" />
* <img src="https://latex.codecogs.com/gif.latex?P(A&space;\cup&space;B)&space;=&space;P(A)&space;&plus;&space;P(B)&space;-&space;P(A&space;\cap&space;B)" title="P(A \cup B) = P(A) + P(B) - P(A \cap B)" />
* <img src="https://latex.codecogs.com/gif.latex?P(A&space;\cap&space;B)&space;&plus;&space;P(B&space;\cap&space;A^{c})&space;=&space;P(B)" title="P(A \cap B) + P(B \cap A^{c}) = P(B)" />

## inclusion-exclusion principle (포함-배제 원리)

#### 공식
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(A_{1}&space;\cup&space;A_{2}&space;...\cup&space;A_{n})&space;=&space;\sum_{j&space;=&space;1}^{n}&space;P(A_{j})&space;-&space;\sum_{i&space;<&space;j&space;}^{}P(A_{i}&space;\cap&space;A_{j})&space;&plus;&space;\sum_{i&space;<&space;j&space;<&space;k}^{}P(A_{i}&space;\cap&space;A_{j}\cap&space;A_{k})&space;..." title="P(A_{1} \cup A_{2} ...\cup A_{n}) = \sum_{j = 1}^{n} P(A_{j}) - \sum_{i < j }^{}P(A_{i} \cap A_{j}) + \sum_{i < j < k}^{}P(A_{i} \cap A_{j}\cap A_{k}) ..." /></p>

#### 포함-배제 원리 예제 - 드 몽모르트 문제(deMontomrt's problem 1713, matching problem)
* 52개의 카드 중 n번째에 n 숫자 카드가 나올 확률
-> 이를 포함-배제 원리를 이용하여 풀 수 있음
* Aj :  카드 j가 j번째에 놓이는 사건
* <img src="https://latex.codecogs.com/gif.latex?P(Aj)&space;=&space;\frac{1}{n}" title="P(Aj) = \frac{1}{n}" />
-> 이러한 사건이 n가지 발생할 수 있음
 * <img src="https://latex.codecogs.com/gif.latex?P(Ai&space;\cap&space;Aj)&space;=&space;\frac{(n-2)!}{n!}&space;=&space;\frac{1}{n(n-1)!}" title="P(Ai \cap Aj) = \frac{(n-2)!}{n!} = \frac{1}{n(n-1)!}" />
 -> nC2 이므로 n(n-1) /2 가지 만큼 발생
* <img src="https://latex.codecogs.com/gif.latex?P(A_{1}&space;\cap&space;A_{2}&space;\cap&space;A_{3}...&space;\cap&space;A_{n})&space;=&space;\frac{(n-k)!}{n!}" title="P(A_{1} \cap A_{2} \cap A_{3}... \cap A_{n}) = \frac{(n-k)!}{n!}" />
-> 1가지 발생

* 따라서 구하고자 하는 확률인 P(A1 U A2 U ... U An) 는
<img src="https://latex.codecogs.com/gif.latex?=&space;P(A_{1})&space;&plus;&space;P(A_{2})&space;&plus;&space;...&space;&plus;&space;P(A_{n})&space;-&space;P(A_{1}&space;\cup&space;A_{2})&space;-&space;...&space;&plus;&space;P(A_{1}&space;\cup&space;A_{2}&space;\cup&space;A_{3})&space;&plus;&space;..." title="= P(A_{1}) + P(A_{2}) + ... + P(A_{n}) - P(A_{1} \cup A_{2}) - ... + P(A_{1} \cup A_{2} \cup A_{3}) + ..." />
<img src="https://latex.codecogs.com/gif.latex?=&space;n\frac{1}{n}&space;-&space;\frac{n(n-1)}{2!}\frac{1}{n(n-1)}&space;&plus;&space;\frac{n(n-1)(n-2)}{3!}&space;\frac{1}{n(n-1)(n-2)}&space;..." title="= n\frac{1}{n} - \frac{n(n-1)}{2!}\frac{1}{n(n-1)} + \frac{n(n-1)(n-2)}{3!} \frac{1}{n(n-1)(n-2)} ..." />
<img src="https://latex.codecogs.com/gif.latex?=&space;1&space;-&space;\frac{1}{2!}&space;&plus;&space;\frac{1}{3!}&space;-&space;...&space;&plus;&space;(-1)^{n-1}\frac{1}{n!}" title="= 1 - \frac{1}{2!} + \frac{1}{3!} - ... + (-1)^{n-1}\frac{1}{n!}" />
<img src="https://latex.codecogs.com/gif.latex?\approx&space;1-&space;\frac{1}{e}" title="\approx 1- \frac{1}{e}" />

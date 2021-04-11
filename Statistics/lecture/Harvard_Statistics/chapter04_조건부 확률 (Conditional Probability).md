# 4강- 조건부 확률 (Conditional Probability)

## 핵심 키워드
* 독립(independence)  
* 쌍으로 독립(Pair independence)  
* Newton-pepys Problem  
* 조건부 확률(conditional probability)  
* 베이즈의 정리(Bayes’ Theorem)  

## 몽모르트 문제 복습

* 문제 : 카드중 j번째 카드에 j숫자가 나올 확률을 구하는 문제  
* 이 문제를 inclusion-exclusion 방법으로 쉽게 풀 수 있었던 이유는 대칭성 때문  
* n개의 카드가 해당 숫자 j번째에 나올 확률은,  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A_{1}&space;\cap&space;A_{2}&space;\cap&space;A_{3}...&space;\cap&space;A_{n})&space;=&space;\frac{(n-k)!}{n!}" title="P(A_{1} \cap A_{2} \cap A_{3}... \cap A_{n}) = \frac{(n-k)!}{n!}" /></p>  

* 1~n개는 항상 같은 위치에 나와야 하기 때문에 고정되고 나머지 숫자들은 아무대나 나와도 상관 없으므로 위와 같은 식이 성립  
* 포함 배제 원리를 이용한 유도식은 생략하고 최종 식만 보면,  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?=&space;1&space;-&space;\frac{1}{2!}&space;&plus;&space;\frac{1}{3!}&space;-&space;...&space;&plus;&space;(-1)^{n-1}\frac{1}{n!}" title="= 1 - \frac{1}{2!} + \frac{1}{3!} - ... + (-1)^{n-1}\frac{1}{n!}" /></p>  

* 짝이 하나도 맞지 않을 확률은 위의 식을 1에서 빼면 됨  
* 결과적으로 테일러 급수를 이용하면 1 - 1/e 라는 결과 값을 가질 수 있는데, 뜬금포이긴 하다  
* why? 1/e는 미분방정식에서나 나올만 한데 갑자기 확률 계산 결과 값이 1/e 이기 때문  
어떻게 생각할  수 있을까?  
##### 1/e 의 비밀
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\frac{(-1)&space;^&space;{n-1}}{n!}" title="\frac{(-1) ^ {n-1}}{n!}" /></p>  

* 해당 식이 무한대로 가면 어떻게 될까?  
* 직관적으로 생각하면, n 이 커지므로, j번째에 j 카드가 올 확률은 낮아지지만, 시행 자체는 많아지므로, 어디론가 수렴할 것 같은 생각이 든다.  
* 결과적으로 이러한 접점이 1/e이 되는 것이다!  

## 독립(independence)
* 식은 간단하지만, 정의에 대한 확실한 이해는 어려울 수 있다.  
* 다양한 방법, 예제로 직관적으로 이해하려고 노력해보자! (항상 헷갈린다)  

<p align = 'center'><b> Defn : Events A,B and independent if P(AnB) = P(A) * P(B) </b></p>

* 배반(disjoint)과 혼동하지 말자!  
  * A와 B가 배반이라고 하면, A가 일어나면 B가 일어나지 않는 것을 의미한다  
  * 독립은 이와는 다르게, A가 발생할 때, 이는 B의 발생에 아무런 영향을 주지 못하는 것을 의미한다  

##### A, B, C가 독립인 경우

* 먼저 각 쌍들이 독립이어야 한다(교집합 기호를 보통 comma로 쓰기도 한다)  
* 다음과 같은 식 3개를 만족한다  
 <p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A,&space;B)&space;=&space;P(A)P(B)" title="P(A, B) = P(A)P(B)" /></p>  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A,&space;C)&space;=&space;P(A)P(C)" title="P(A, C) = P(A)P(C)" /></p>  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(B,&space;C)&space;=&space;P(B)P(C)" title="P(B, C) = P(B)P(C)" /></p>  

* 생각해보자. 이 세가지 식을 만족하면 되는 것일까? -> NO! 한 개의 식이 더 필요하다  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A,&space;B,&space;C)&space;=&space;P(A)P(B)P(C)" title="P(A, B, C) = P(A)P(B)P(C)" /></p>  

* 처음 3개의 식을 만족한다고 해서 위의 식을 만족하지 않는다는 것을 기억하자  
* 즉 총 4개의 식을 모두 만족해야 A,B,C가 독립이라고 할 수 있다  


## Newton-Pepys Problem(1693)
* 새뮤얼 피프스는 유명한 일기 작가  
* 문제 : 주사위가 있는데, 1 ~ 6까지 있고 각 면이 나올 확률은 동일  
* 다음 3가지 경우 중 어떤 것이 가장 확률이 높을까?  
  * A1 : 6개의 주사위 중 적어도 하나의 주사위가 6이 나올 사건  
  * A2 : 12개의 주사위로 적어도 2개의 6이 나올 사건  
  * A3 : 18개의 주사위로 적어도 3개의 6이 나올 사건  

* 답은 다음과 같다  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A_{1})&space;=&space;1&space;-&space;(\frac{5}{6})^{6}" title="P(A_{1}) = 1 - (\frac{5}{6})^{6}" /> </p>  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A_{2})&space;=&space;1&space;-&space;(\frac{5}{6})^{12}&space;-&space;(\frac{5}{6})^{11}&space;\frac{1}{6}&space;*&space;12" title="P(A_{2}) = 1 - (\frac{5}{6})^{12} - (\frac{5}{6})^{11} \frac{1}{6} * 12" /></p>  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A_{3})&space;=&space;1&space;-&space;\sum_{k&space;=&space;0}^{2}&space;\binom{18}{k}(\frac{1}{6})^{k}(\frac{5}{6})^&space;{18&space;-&space;k}" title="P(A_{3}) = 1 - \sum_{k = 0}^{2} \binom{18}{k}(\frac{1}{6})^{k}(\frac{5}{6})^ {18 - k}" /></p>  

* 계산해보면, A1의 확률이 가장 높다!(그냥 그렇다고..)    

##  조건부 확률(conditioning probability)  
* 통계는 불확실성에 대한 학문  
* 대부분의 일상적인 일 들은 100% 확실한 것은 잘 없다. 항상 불확실성이 존재  
* 내가 알고 있는 사실이 있음. 이러한 사실을 믿고 있을 때, 이러한 믿음은 어떻게 갱신할 수 있을까?  
* 우리는 통계적으로, 수학적으로 갱신해야 한다.  
* 교수님 왈, "Conditioning is the soul of statistics."  결과적으로 조건부 확률을 잘 알라고 하는 것이다  

##### Defn
* P(A|B) : B라는 사건이 일어났을 때, A의 사건이 일어날 확률(다음과 같이 |로 표시)  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A|B)" title="P(A|B)" /></p>  

* B라는 사건이 일어났을 때, A의 사건이 일어날 확률(다음과 같이 |로 표시)  
* 만약 A와 B가 독립적이라면, 조건부 확률은 의미가 없음  
  * B가 일어났을 때 A가 일어날 확률과 단순히 A가 일어날 확률이 같기 때문. but 독립이 아니라면 가치있는 정보가 될 것임  

<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A|B)&space;=&space;\frac{P(A,&space;B)}{P(B)},&space;if&space;P(B)&space;>&space;0" title="P(A|B) = \frac{P(A, B)}{P(B)}, if P(B) > 0" /></p>  

* 위의 식은 엄청 간단해 보이지만, 정말 다양한 예제에서 사용되게 될 것  

##  조건부 확률에 대한 2가지 직관적 해석  
* 사실 조건부 확률 식만 가지고 해석하기에는 어려움이 있음  
* 따라서 어떠한 현상에서 조건을 붙일 때, 합리적인 방식이라고 생각할 수 있으면 좋음   
  * 따라서 다음의 두 가지 직관적 해석을 기억해보자  

##### (1) 조약돌 세계(Pebble world)  
![img](https://github.com/koni114/Harvard_Statistics/blob/master/image/%EC%A1%B0%EC%95%BD%EB%8F%8C%EC%84%B8%EA%B3%84.JPG)  


* S : 표본공간  
* 우리가 통상적으로 쓰는 확률의 단순한 정의를 넘어서 생각해보자  
* 유한개의 가능한 결과가 있는데, 이는 각각 다른 확률로 표현될 수 있음  

* 1,2,4,5번 돌을 묶은 공간(space)가 사건 B라고 하자  
* 사건 B는 조약돌의 집합이고 P(A | B)를 구하고 싶다고 해보자  
* 이 것이 의미하는 것은 B가 이미 일어났다고 해석하면 됨. 즉 B 공간 안에 조약돌이 선택되었다고 가정하므로
* B 밖에 있는 5개는 관련이 없게 됨  
* 네 개의 조약돌만 남음! 쉽게 말하면 원래 S라고 하는 우주가 있었는데, B라고 하는 공간을 우리의 우주로 한정시킨 것  

* 평소에 하던데로 확률의 법칙을 적용하면 됨  
* 따라서 A의 사건이 조약돌 5,6,8,9가 선택될 확률 이라고 하면 결과적으로 5번 조약돌이 선택될 확률이라는 것  
  * --> P(A n B)  

* 이 때, 우리는 공간을 B의 사건으로( = 우리의 우주, 공간)으로 한정시켰기 때문에, B 사건이 일어날 확률의 공간을 1로 맞추어 주어야 함 = <b>재정규화(renormalization)</b>  
* 따라서 P(B)로 나눠 주는 것  

* 정리하자면 P(A|B)  
  *  1. get rid of pebble B^c  
  * 2. renormalize space  


##### (2) 빈도학파 세계(frequentist world)  
* 실험을 여러번 반복  
* 철학적인 문제가 있긴 하지만, 정확히 같은 실험을 여러 번 반복할 수 있다고 하자  
* 여기서의 포인트는 확률을 보는 관점이 '빈도'라는 것  
* 예를 들어 1000번을 던졌을 때, 앞면이 512번이 나온다면 확률을 512 / 1000으로 보겠다는 의미  
* 쉬운 예제로 유한한 이진 데이터를 만들어 낸다고 생각해보자  

![img](https://github.com/koni114/Harvard_Statistics/blob/master/image/%EC%9D%B4%EC%A7%84%EB%8D%B0%EC%9D%B4%ED%84%B0.JPG)  

* 다음과 같은 이진 데이터가 있다고 할 때, B의 사건 중, 사건 A 또한 발생한 것의 비율은 ?  
* 이도 마찬가지로, 조건부 확률 P(A|B) 인 것을 알 수 있고, 또한 위의 조약돌 예시와 일맥상통하는 면이 있다는 점!  

##  조건부 확률을 이용한 간단한 정리  
* 다음의 정리들은 앞으로 많이 사용되고 응용되므로, 꼭 기억하도록 하자  

##### (1) 정리1  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A,&space;B)&space;=&space;P(B)P(A|B)&space;=&space;P(A)P(B|A)" title="P(A, B) = P(B)P(A|B) = P(A)P(B|A)" ></p>  

* 식 자체는 굉장히 단순해 보일 수 있는데, 굉장히 활용도가 높다  
* 이때 독립이라면, P(A n B) = P(A)P(B) 인데, P(B)P(A|B) 라는 식에서  
P(A|B)는 P(A)로 바뀐다는 것  


##### (2) 정리2  
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A_{1},&space;A_{2},&space;A_{3}\dots&space;A_{n})&space;=&space;P(A_{1})&space;P(A_{2}|A_{1})P(A_{3}|A_{1},A_{2})P(A_{4}&space;|&space;A_{1},&space;A_{2},&space;A_{3}..)" title="P(A_{1}, A_{2}, A_{3}\dots A_{n}) = P(A_{1}) P(A_{2}|A_{1})P(A_{3}|A_{1},A_{2})P(A_{4} | A_{1}, A_{2}, A_{3}..)" /></p>  

##### (3) Bayes' Rule   
* 베이즈는 목사이자 통계를 공부한 사람  
* P(A | B) 라는 식과 P(B | A)라는 식을 연결 짓고 싶음  
* 위의 식에서 P(B)P(A|B) = P(A)P(B|A) 라는 식을 응용해보자  
* 양변을 P(B)로 나누면,   
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?P(A|B)&space;=&space;\frac{P(B|A)P(A)}{P(B)}" title="P(A|B) = \frac{P(B|A)P(A)}{P(B)}" /></p>  

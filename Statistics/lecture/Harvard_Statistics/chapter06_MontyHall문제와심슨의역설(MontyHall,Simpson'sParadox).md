#  Monty Hall 문제와 심슨의 역설 (Monty Hall, Simpson's Paradox)

## 핵심 키워드
* Monty Hall  
 * 전체 확률의 법칙  
 * 심슨의 역설(Simpson's Paradox)  

## Monty Hall 문제  
사람들이 많이 틀리는 문제 중에 하나로, 이해했다고들 생각하지만, 조금만 응용해서 다시 내면 다시 틀림..   

 #### 문제 설명
 * 총 3개의 문이 있음  문 뒤에는 자동차가 1개, 염소가 2개 있다.  
* 우리는 문 뒤에 무엇이 있는지 모른다.  
* Monty Hall이 우리에게 문을 하나 선택하라고 한다.
* Monty Hall만이 어느 문에 자동차가 있고, 염소가 있는지 알고 있다.  
* 먼저 우리는 문을 하나 선택해야 함.
* Monty Hall은 우리가 선택하지 않는 나머지 문 2개 중 하나를 여는데, 반드시 염소가 있는 문을 하나 연다.
* 다음에 Monty Hall은 우리에게 바꿀 수 있는 기회를 주는데,   
바꾸는 것이 좋을까? 그대로 있는 것이 좋을까? 아니면 바꾸나, 바꾸지 않나 똑같을까?  

#### 가정
 * 우리는 염소가 아닌 자동차를 원한다  
 * Monty Hall는 항상 문을 열고, 문을 연 곳에는 염소가 있음  
 * 만약 Monty Hall이 어떤 문을 열지 선택할 수 있다면 동일한 확률로 결정을 내릴 것임  
 -> 이 경우는 처음 우리가 자동차를 선택했을때 해당됨. 나머지 두 문을 열 확률은 동일하다는 의미  

#### 정답
 바꾸는 것이 유리하다.  
 처음 그대로 있을 때 자동차가 있을 확률 : 1/3   
 바꾸었을 때 자동차가 있을 확률 :  2/3
#### 생각해보기
##### 1. 50-50 확률 아닌가?
* Monty Hall이 연 뒤 남은 문은 2개이므로 자동차를 고를확률은 어디 위치든 50%아닌가? 라고 생각할 수 있다.  

* 잘 생각해보면, Monty Hall이 염소가 있는 문을 열었다라는 증거가 있다는 가정 하에 같은 확률인지는 생각해보아야 함.  

* <b>중요한 사실은 Monty Hall이 A번째 문을 열었다는 사실.</b> 이에 입각하여 조건화 해야한다.

##### 2. 조건부 확률 + 수형도를 이용한 풀이
* 복잡도를 최소화하기 위해서 게임 참가자가 1번 문을 선택했다고 가정
* Monty Hall이 어떤 문을 여느냐에 따라서 다음 가지가 결정됨
* 수형도에서 두 가지 생각해볼 점  
    - 어떤 문에 자동차가 있느냐?
    - 몬티가 어떤 문을 열었느냐?

* 첫 번쨰로는 어떤 문에 자동차가 있는지, 그리고 몬티가 어떤 문을 열었는지를 가지고 수형도를 그려보자.

 ![img](https://github.com/koni114/TIL/blob/master/Statistics/lecture/Harvard_Statistics/image/MontyHall%EC%88%98%ED%98%95%EB%8F%84.JPG)  

* 예를 들어 Monty Hall이 2번 문을 열었다고 가정(조건)해보자.
* 동그라미 친 부분에 해당되고, 이 때 각각의 확률은 1/6, 1/3이 나오며,   
이를 renormalize 해주면 1/3, 2/3이 나온다(조건부 확률에서는 조약돌을 생각하자)  
* 즉 자동차가 있는 문 3번을 선택하게되면 2/3 확률로 차를 얻게 되는 것을 확인 할 수 있다.

* <b>P(바꿨을 때 성공확률 | Monty Hall이 2번 문 Open) = 2/3</b>

##### 3. 조건부 확률을 이용한 풀이
* 전체 확률의 법칙을 이용하여 풀어보자.
* 우리는 자동차가 어디 있는지 알고 싶어한다.
* 먼저 사건을 정의해야함.
  - S  : 우리가 성공하는 사건(항상 문을 바꾸는 전략)
  * Dj : 문 j 뒤에 자동차가 있는 사건(j = 1, 2, 3)

<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(S)&space;=&space;\frac{P(S|D1)}{3}&space;&plus;&space;\frac{P(S|D2)}{3}&space;&plus;&space;\frac{P(S|D3)}{3}" title="P(S) = \frac{P(S|D1)}{3} + \frac{P(S|D2)}{3} + \frac{P(S|D3)}{3}" /></p>

* <b> 여기서 생각해야 할 점은, 분모의 3은 P(D1), P(D2), P(D3)이 사전 확률이기 때문에 붙는다!   </b>
* 해당 값을 대입하여 계산하면 2/3이 나온다.
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(S)&space;=&space;0&space;&plus;&space;1*\frac{1}{3}&space;&plus;&space;1*\frac{1}{3}" title="P(S) = 0 + 1*\frac{1}{3} + 1*\frac{1}{3}" /></p>

* 또한 Monty Hall이 문을 열기전에 확률은 같으므로(대칭성), 조건부 일 때(ex)Monty Hall이 2번 문을 열었을 때 바꿨을 때 자동차가 있을 확률)도 마찬가지로 2/3 확률을 갖는다.

##### 4. 특이한 접근을 통한 문제 풀이
* 문이 3개가 아니라 100만개라면?


## 심슨의 역설(Simpson's paradox)
* 실제 역설은 존재하지 않음

##### 1. 심슨의 역설 문제 설명 - 두 의사
* 두 의사가 있는데,  두 의사는 총 합쳐서 100번의 수술만 함
* 첫 번째 의사 히버트  
    * 모든 가능한 수술 종류에서 두 번째 의사 보다 수술을 잘 할 확률이 높음.  
    * 마을에서 존경 받는 의사    
* 두 번째 의사 닉  
    * 모든 가능한 수술 종류에서 첫 번째 의사 보다 수술을 잘 할 확률이 낮음.  
    * 모든 수술을 129.99$에 해주는 돌팔이 의사  
* 이러한 두 가지 조건에서 <b>전체 수술을 잘 할 확률이 두 번째 의사가 첫 번째 의사보다 잘 할 확률이 높을 수 있다!</b> 라는 것이 심슨의 역설  

##### 2. 심슨의 역설 문제 두 의사의 수술 성공 확률 표
* 수술의 종류가 2개일 때 성공 확률을 표로 확인해보자  
* 히버트 의사 수술 성공 확률  

||  심장 수술 | 붕대 풀어주기
---|:---:|:---:|
|성공   |70  | 10  |
|실패   | 20  | 0  |

* 닉 의사 수술 성공 확률  

||  심장 수술 | 붕대 풀어주기
---|:---:|:---:|
|성공   |2  | 81  |
|실패   | 8  | 9  |

* 전체 수술 성공 확률
    - 히버트 : 80%
    - 닉   : 83%

* 확인해보면, 각 수술의 성공 확률은 히버트가 닉보다 성공 확률이 높지만, 전체 수술 확률은 닉이 더 높은 것을 확인할 수 있음

##### 3. 두 의사 예제 - 해석
* 결과적으로 조건부이냐, 비조건부이냐로 바라보는 관점에서 확률이 달라짐
* 상대적으로 수술 성공이 쉬운 수술만 절대적으로 많이 한다면, 전체 확률은 올라갈 수 밖에 없음
* <b>문제가 완벽히 같더라도 다른 표현과 환경을 제시한다면 결과는 달라질 수 있는 것이 통계</b>

##### 4. 심슨의 역설 - 이론적 접근

* A : 수술이 성공하는 사건
* B : 닉 의사가 수술을 집도하는 사건
* C : 심장 수술을 받는 사건
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(A|B,C)&space;<&space;P(A&space;|B^{c},&space;C)" title="P(A|B,C) < P(A |B^{c}, C)" /></p>
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(A|B,C^{c})&space;<&space;P(A&space;|B^{c},&space;C^{c})" title="P(A|B,C^{c}) < P(A |B^{c}, C^{c})" /></p>
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(A|B)&space;>&space;P(A&space;|B^{c})" title="P(A|B) > P(A |B^{c})" /></p>

* 해당 이론식을 통해 알 수 있는건, Dr. 히버트가 각 수술 조건별로 수술 성공 확률은 더 높지만,  
전체 수술 확률은 Dr. 닉이 더 높을 수 있다는 것을 의미한다.

* 여기서 C(심장 수술을 받는 사건)은 <b>교란 변수(confounder)</b> 라고 하며, 적절한 교란 변수를 찾아서 조건부 확률로 계산하지 않으면 오판할 수 있음을 의미

##### 5. 전체 확률의 법칙(LOTP)을 통한 심슨의 역설 판단

<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(A|B)&space;=&space;P(A|B,C)P(C|B)&space;&plus;&space;P(A|B,C^{c})P(C^{c}&space;|B)" title="P(A|B) = P(A|B,C)P(C|B) + P(A|B,C^{c})P(C^{c} |B)" /></p>
<p align="center"><img src="https://latex.codecogs.com/gif.latex?P(A|B^{c})&space;=&space;P(A|B^{c},C)P(C|B^{c})&space;&plus;&space;P(A|B^{c},C^{c})P(C^{c}&space;|B^{c})" title="P(A|B^{c}) = P(A|B^{c},C)P(C|B^{c}) + P(A|B^{c},C^{c})P(C^{c} |B^{c})" /></p>

* 두 식에서 P(C|B), P(C|B^c), P(C| B^c), P(C^c | B^c) 에 대한 가중치(비율)이 어떻게 setting 하느냐에 따라 제 각각 이므로, 해당 식이 틀렸는지, 맞는지 증명 할 수 없음을 의미한다.

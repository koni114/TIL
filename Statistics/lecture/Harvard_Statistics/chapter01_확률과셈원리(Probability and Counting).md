
# 확률과 셈 원리 ( Probability and Counting)
-----
## 핵심 키워드 및 학습내용 예습
* 확률론의 활용영역  
유전학, 물리학, 계량경제학, 금융, 역사학, 정치  
인문학, 사회과학계에서도 중요도와 활용이 늘어나고 있음  
도박과 게임 - 통계에서 여러 번 연구된 주제  
인생 전반 : 수학이 확실성에 대한 학문이라면, 확률은 불확실성을 계량화 하는 것을 가능하게 해줌.  
집단 간 분산 / 집단 내 분산 값으로 계산  

* 표본공간(sample space) : 시행에서 발생 가능한 모든 경우의 집합  
* 사건(event) : 표본공간의 부분집합  
* 셈 원리(곱의 법칙)  
* 이항계수  
   
## 확률의 Naive한 정의
P(x) = 사건X가 발생하는 경우의 수 /  발생 가능한 모든 경우의 수                          
* 내포하고 있는 가정  
모든 사건이 발생할 확률은 같음  
유한한 표본 공간  
항상 이 가정이 만족되는 것은 아니기에 적용 불가한 경우들이 존재  

## 셈 원리(Counting Principle)
* 곱의 법칙(Multiplication Rule) : 발생 가능한 수가 n1, n2, n3... nr 가지인  
1,2,3,.... r번의 시행에서 발생 가능한 모든 경우의 수는 n1 x n2 x n3 x nr 임  

## 이항계수(Binomial Coefficient)
<p align="center"><img src="https://latex.codecogs.com/gif.latex?\binom{n}{k}&space;=&space;\frac{n!}{(n-k)!k!}" title="\binom{n}{k} = \frac{n!}{(n-k)!k!}" /></p>

> 크기 n인 집합에서 만들 수 있는 크기 k인 부분집합의 수(순서 상관 없이)  

### 표본 추출을 정리한 표(Sampling Table) : n개 중에서 K개 뽑기
> |                                     |  순서 상관 있음 | 순서 상관 없음
> |---|:---:|:---:|
>  | 복원 |<img src="https://latex.codecogs.com/gif.latex?\dpi{150}&space;\large&space;n^{k}" title="\large n^{k}" />| <img src="https://latex.codecogs.com/gif.latex?\dpi{150}&space;\binom{n&space;&plus;&space;k&space;-&space;1}{k}" title="\binom{n + k - 1}{k}" />|   
>  | 비복원 | <img src="https://latex.codecogs.com/gif.latex?\dpi{150}&space;n(n-1)(n-2)(n-3)\cdot\cdot\cdot(n&space;-&space;k&space;&plus;&space;1)" title="n(n-1)(n-2)(n-3)\cdot\cdot\cdot(n - k + 1)" />| <img src="https://latex.codecogs.com/gif.latex?\dpi{150}&space;\binom{n}{k}" title="\binom{n}{k}" />||   

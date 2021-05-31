# 해석을 통한 문제풀이 및 확률의 공리

## 핵심 키워드
* 확률의 naive한 정의
* Story proof
* 확률의 non-naive한 정의의 공리

## 문제를 통한 통계의 이해

#### 10명 중 6명과 4명의 집단을 만들고 싶을 때, 경우의 수는?
* 10명 중 4명을 고르는 방법. 나머지 6명은 자동으로 나눠지기 때문
<p align="center"><img src="https://latex.codecogs.com/gif.latex?\binom{10}{6}&space;=&space;\binom{10}{4}" title="\binom{10}{6} = \binom{10}{4}" /></p>

#### 10명 중 5명 씩 두 그룹을 만들고 싶을 때, 경우의 수는?

 * 10명 중 5명을 선택하는 경우의 수
 * 이 때 5명이라는 그룹은 서로 구분이 불가하므로, 2로 나누어 주어야 함
 * 순서가 있는지, 없는지를 생각하는 것이 굉장히 중요함. 지금의 경우는 순서가 없으므로, 2로 나누어 주어야 함.

##  sampling table에 대한 논의

#### 복습

> |                                     |  순서 상관 있음 | 순서 상관 없음
> |---|:---:|:---:|
>  | 복원 |<img src="https://latex.codecogs.com/gif.latex?\dpi{150}&space;\large&space;n^{c}" title="\large n^{c}" />| <img src="https://latex.codecogs.com/gif.latex?\binom{n&plus;k-1}{c}" title="\binom{n + k - 1}{k}" />|
>  | 비복원 | <img src="https://latex.codecogs.com/gif.latex?\dpi{150}&space;n(n-1)(n-2)(n-3)\cdot\cdot\cdot(n&space;-&space;k&space;&plus;&space;1)" title="n(n-1)(n-2)(n-3)\cdot\cdot\cdot(n - k + 1)" />| <img src="https://latex.codecogs.com/gif.latex?\dpi{150}&space;\binom{n}{k}" title="\binom{n}{k}" />||

* 순서가 상관 없고, 복원인 경우를 제외한 3가지 Case는 곱의 법칙으로 설명 됨

#### 순서가 없으면서 복원 추출인 CASE - 증명
* 식은 다음과 같다. 다양하게 생각하면서 접근해보자
<p align="center"><img src="https://latex.codecogs.com/gif.latex?\binom{n&space;&plus;&space;k&space;-&space;1}{&space;k&space;}" title="\binom{n + k - 1}{ k }" /></p>


#### 극단적인 CASE를 통한 접근
* 간단하면서 중요한데, 극단적인 CASE를 보거나, 간단하지만 평범하지 않는 CASE를 풀어보면서 예시를 보는 것이 굉장히 중요하다

  -  k = 0 인 경우
  경우의 수는 1이다. 0개를 선택하는 방법은 1개. 이는 0!와도 같은 접근 방법이다.
  - k = 1 인 경우
  n개중에 1개를 뽑는 경우의 수 이므로 n개.
  - n = 2 인 경우
  여기서의 접근 방법이 굉장히 중요한데, n개의 상자에 k개의 공을 담은 경우의 수라고 생각해보자.
  즉 n = 2이므로 2개의 상자에 구분하지 못하는 k개의 공을 넣는 방법이므로,
  K+1이라는 경우의 수를 구할 수 있다
  이러한 연습은 굉장히 중요한데, 다른 것 같이 보이는 예제가 같음을 생각할 수 있기 때문이다!
  <p align="center">  <img src="https://latex.codecogs.com/gif.latex?\binom{k&space;&plus;&space;1}{&space;k&space;}&space;=&space;\binom{k&space;&plus;&space;1}{1}&space;=&space;k&space;&plus;&space;1" title="\binom{k + 1}{ k } = \binom{k + 1}{1} = k + 1" /></p>



#### K개의 구별 불가능한 입자들을 n개의 구별 가능한 박스에 넣는 경우의 수?
##### 상자 4개에 구슬 k개를 넣는 경우의 수를 생각해보자
![img](https://github.com/koni114/Harvard_Statistics/blob/master/image/4%EA%B0%9C%EC%83%81%EC%9E%90k%EA%B0%9C%EA%B5%AC%EC%8A%AC.JPG)


* 이는 K개의 구슬과 n-1개의 | 를 배열하는 경우의 수와 같다!
* 작대기 n-1 를 배열한 위치에 따라서 구슬의 배치가 달라지기 때문
* 따라서 다음과 같은 식을 가진다는 것을 직관적으로 판단할 수 있다
  <p align="center"><img src="https://latex.codecogs.com/gif.latex?\binom{n&space;&plus;&space;k&space;-&space;1}{&space;k&space;}&space;=&space;\binom{n&space;&plus;&space;k&space;-&space;1}{n&space;-&space;1}" title="\binom{n + k - 1}{ k } = \binom{n + k - 1}{n - 1}" /></p>

#### 증명을 통해 생각해볼 점

* 구슬과 같이 실물이 있는 물체는 labeling이 가능하므로, 서로 구별이 가능하다. 따라서 확률의 naive한 정의로 정의가 가능
* 하지만 물리학, counting problem 에서의 경우는 항상 구별 가능한 것이 아니기 때문에 이와 같은 접근은 어렵다.

## story proof
* 증명이긴 한데, 대수적 증명이 아닌 예시를 통한 직관적인 증명

#### 예시1
<p align="center"><img src="https://latex.codecogs.com/gif.latex?\binom{n&space;}{&space;k&space;}&space;=&space;\binom{n&space;}{n&space;-&space;k}" title="\binom{n }{ k } = \binom{n }{n - k}" /></p>

* n개중에 k개를 고르고, n-k개를 고르는 방법
* 위의 두 개의 식은 동일 함을 직관적으로 이해할 수 있다

#### 예시2
<p align="center"><img src="https://latex.codecogs.com/gif.latex?n&space;\binom{n&space;-1&space;}{k&space;-&space;1}&space;=&space;k&space;\binom{n&space;}{k}" title="n \binom{n -1 }{k - 1} = k \binom{n }{k}" /></p>

*  n - 1개 중 k -1 를 고르는 경우의 수에 n을 곱한 수는 n개 중 k개를 고르는 경우의 수에 k를 곱한 값과 같다.
* k명이 구성된 동아리와 동아리 내에서 대표 1명을 뽑는다고 하면 직관적으로 증명이 가능
    - 좌변 : 대표 한 명(n가지 경우의 수)을 뽑고, 나머지 n-1명 중 k-1명을 뽑는 경우의 수
    - 우변 : k명의 동아리 구성원을 뽑고, k명 중에서 대표 한 명(k가지 경우의 수)를 뽑는 경우의 수

#### 예시3
<p align="center"><img src="https://latex.codecogs.com/gif.latex?\binom{m&space;&plus;&space;n&space;}{k}&space;=&space;\sum_{j&space;=&space;0}^{k}&space;\binom{m}{j}\binom{n}{k&space;-&space;j}" title="\binom{m + n }{k} = \sum_{j = 0}^{k} \binom{m}{j}\binom{n}{k - j}" /></p>

* 방데르몽드 항등식이라고 불림(수학에서 유명한 항등식)
* 대수적으로 증명하는 것은 굉장히 어려움
* m+n개에서 k개를 뽑는 경우의 수는 m 그룹, n그룹에서 각각 j개, k-j개를 뽑아 이를  0=< j  <= k 개 만큼 더해주면 됨
![img](https://github.com/koni114/Harvard_Statistics/blob/master/image/%EB%B0%A9%EB%8D%B0%EB%A5%B4%EB%AA%BD%EB%93%9C.JPG)

## Non-naïve definition of probability
#### 확률 공간(sample space)
* 확률 공간에는 2개의 성분이 있음(S, P)
* S는 표본 공간(sample space) : 가능한 모든 경우의 수 공간
* P는 어떤 함수. P의 정의역은 S의 부분 집합
* P(A)는 [0, 1] 사이의 확률 -> 이것이 출력이 됨

#### 공리
* <img src="https://latex.codecogs.com/gif.latex?P(\phi)&space;=&space;0,&space;P(S)&space;=&space;1" title="P(\phi) = 0, P(S) = 1" />
* <img src="https://latex.codecogs.com/gif.latex?P(\bigcup_{n=1}^{\infty&space;}&space;A_{n})&space;=&space;\sum_{n&space;=&space;1}^{\infty}&space;P(A_{n})" title="P(\bigcup_{n=1}^{\infty } A_{n}) = \sum_{n = 1}^{\infty} P(A_{n})" />

* 두 가지 공리로부터 대부분의 식을 유도할 수 있음

* **공리: 논리학이나 수학 등의 이론체계에서 가장 가장 기초적인 근거가 되는 명제

# ANOVA(Analysis of variance)
- 비교하고자 하는 집단이 3개 이상인 경우 ANOVA 분석을 수행
- 독립변수는 범주형 자료이어야 하며, 종속변수는 연속형 자료이어야 함
- ANOVA 분석은 분산의 개념을 이용하는 방법으로서 각 집단들의 편차에 제곱합을 자유도로 나누어서 얻게되는 값을 이용하여 수준평균들 간의 차이가 있는지를 검정함
- ANOVA 분석은 영국의 통계학자 fisher가 고안해낸 방법
- 3개 집단에 대한 비교 시, 모집단이 정규분포를 따르지 않으면 다른 기법을 이용해야함  
  --> shapiro.wilk, qq-plot 등과 같은 정규성 검정을 통해 정규성 검정 확인
- 분산분석은 요인의 수에 따라 
  - 요인(factor)가 1개인 경우 --> 일원분산분석(one-way-anova)
  - 요인(factor)가 2개인 경우 --> 이원분산분석(two-way anova)

## 일원분산분석(one-way anova)
- 일원분산분석 모형은 다음과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?Y_{ij}&space;=&space;\mu_{i}&space;&plus;&space;\varepsilon_{ij}" /></p>

- Y(ij) : i번째 수준에서 j번째 값
- M(i)  : i번쨰 수준의 평균값
- E(ij) : i번째 수준에서 j번째 값의 오차. 서로 독립이며, 정규분포를 따름
- 분산분석은 측정된 자료값들의 전체 변동을 요인 수준간에 차이에서 발생하는 변동과, 그밖의 요인들에 의해서 발생하는 변동들을 기반으로 설명하는 것이 되겠음
- 분산 분석의 기본 원리는 다음과 같음

<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?Y_{ij}&space;-&space;\bar{Y}&space;=&space;(\bar{Y_{i}}&space;-&space;\
bar{Y})&space;&plus;&space;(\bar{Y_{ij}}&space;-&space;\bar{Y_{i}})" /></p>

- 각각의 측정값과 전체 측정값의 평균은, (각각의 수준별 평균 - 전체 평균) + (각각의 측정값 - 수준별 평균) 으로 구분할 수 있음
- 위의 식의 양변을 제곱하여 정리하면 다음과 같은 식으로 재편성됨
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?\sum_{i&space;=&space;1}^{r}\sum_{j&space;=&space;1}^{n}(Y_{ij}&space;-&space;\bar{Y})^{2}&space;=&space;\sum_{i&space;=&space;1}^{r}\sum_{j&space;=&space;1}^{n}(\bar{Y_{i}}&space;-&space;\bar{Y})^{2}&space;&plus;&space;\sum_{i&space;=&space;1}^{r}\sum_{j&space;=&space;1}^{n}(\bar{Y_{ij}}&space;-&space;\bar{Y_{i}})^{2}" /></p>

<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?SST&space;=&space;SSTR&space;&plus;&space;SSE" /></p>

- SST  : 총제곱합(Total sum of sqaure)
- SSTR : 처리제곱합(Treatment sum of square)
- SSE  : 오차제곱합(Error sum of square)
- SST, SSTR, SSE 간의 기본원리를 이용하여 통계량을 계산할 수 있음
- 검정통계량 <b>F(0) = MSTR/MSE</b>
  - MSTR --> SSTR / r - 1(r은 수준 개수)
  - MSE  --> SSE /  nr - r(n은 샘플 개수, r은 수준 개수)
- 위의 F(0) 통계량 값을 이용하여 전체 수준들 간의 평균이 같은지 아니면 다른지를 검정함
- 즉 수준간의 평균 차이가 클수록, 수준내 오차가 작을수록 통계량 값은 커짐

### 검정과 p-value
- 다음과 같이 가설을 세울 수 있음
  - 귀무가설 : 각 수준별 평균의 차이는 없다
  - 대립가설 : 각 수준별 평균의 차이는 있음
- 표본으로부터 계산된 검정통계량 F(0)가 유의수준(significance level) alpha에서 기각 채택 여부를 파악할 수 있음

### 등분산성 가정
- 오차의 등분산성 가정에 대해서는 Bartlett 검정 수행할 수 있음

## 사후 검정
- 일원분산분석 이후에 하게되는 다중비교(multiple comparison)
- 만약 대립가설(각 수준별로 유의미한 차이가 있다)를 채택하였을 경우, 수준별로 집단 간의 어디가 차이가 생겼는지를 알기 위한 다중비교를 의미함
- <b>예를 들어 일원분산분석에서 수준의 개수가 2개인 경우, T-Test를 진행하면 되지만, 수준의 개수가 3개 이상인 경우는 T-TEST를 진행하면 안됨!</b>  
그 이유는 두 수준간의 짝 별로 T-TEST를 진행하게 될 때 제 1종 오류(참을 거짓으로 판정할 오류)가 애초에 정한 유의 수준보다 훨씬 커지기 때문
- 만약, 수준 10개의 요인을 각각 T-TEST를 진행했을 경우, 1종 오류가 생길 확률은 1 - (0.95)^10 =0.40 정도가 됨. 약 8배가 커짐!
- 이러한 오류를 피하기 위하여 고안된 방법인 <b>Tukey's HSD</b>와 <b>ducan's LSR(least significance range)</b> 가 있음 
- <b>샤페 검정법(Scheffe test)</b>은 수준 별 샘플의 크기가 다른 경우와 세 개 이상의 수준에서 평균들을 비교할때도 사용가능한 방법

## 이원분산분석(two-way ANOVA)
- 2개의 요인(factor)내 각각의 조합별을 각 집단으로 판단하고 집단별 차이를 계산하는 방법
- 이원분산분석은 관측값이 하나인 경우와 관측값이 두 개 이상인 경우

### 관측값이 하나인 경우
- 즉, 다음과 같은 식으로 나타낼 수 있음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?SST&space;=&space;SSA&space;&plus;&space;SSB&space;&plus;&space;SSE" /></p>

- 검정통계량으로는 F통계량(요인 A효과검정 = MSA/MSE, 요인 B효과검정 = MSB/MSE)을 사용하며, 각각의 식들은 일원분산분석 방법과 동일

### 관측값이 두 개 이상인 경우
- 관측값이 두 개 이상인 경우의 이원분산분석을 알아보자
- 이 때 각 집단내 관측의 개수는 동일함
- 관측값이 여러 개인 경우, 두 요인이 상호간에 영향을 주고 받으면서 생기는 반응효과인 <b>교호작용</b>이 추가로 분석됨
- 식은 다음과 같음
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?SSTotal&space;=&space;SSA&space;&plus;&space;SSB&space;&plus;&space;SSAB&space;&plus;SSE" /></p>
<p align = 'center'><img src="https://latex.codecogs.com/gif.latex?SSAB&space;=&space;\bar{Y}_{ij.}&space;-&space;\bar{Y}_{i..}&space;-&space;\bar{Y}_{.j.}&space;&plus;&space;\bar{Y}_{...}" /></p>

### 이원분산분석 통계량 계산
- 요인 A : SSA / a-1 / MSA 
- 요인 B : SSB / b-1 / MSB
- 교호작용 AB : SAB / (a-1)(b-1) / MSAB
- 잔차 : SSE / ab(n-1) / MSE


## 용어 정리
- 제1종오류, 제2종오류
  - 제1종오류 : 귀무가설이 참인데 거짓으로 판별
  - 제2종오류 : 대립가설이 참인데 거짓으로 판별
  - 제1종오류가 제2종오류 보다 더 위험함. why? 일반적으로 가설을 검정할 때는 보편적인 사실을 귀무가설에 세워두고 실험을 통해 파악하고자, 의심스러운 상황을 대립가설로 세워두고 검정을 수행  
  ex) 탈모약의 효능을 파악하기 위하여 대립가설에는 효능이 있음을 세워둠  
  - 따라서 제1종오류를 최대한 줄이는 방향에서 제2종오류도 줄이려고 하는 것이 보편적임  
  - 제1종오류 --> 0.01, 0.05 같은 유의수준을 통해서 우선적으로 검토함 
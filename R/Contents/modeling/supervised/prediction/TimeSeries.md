# Times Series
## 시계열 분석
- 시간의 흐름에 따라 관찰된 값을 시계열 자료라고 함
- 많은 연구자들이 시계열 정보를 크게 2가지로 쪼개어 규칙성을 가지는 패턴과 불규칙한 패턴의 결합이라고 여겨왔음
- 따라서 시계열 모형은 전통적으로 이 두가지를 나누어서 개발되어 왔는데, 규칙성을 만드는 패턴을 또한 두가지로 쪼개어 이전의 결과과 이후의 결과 사이에서 발생하는 자기상관성(Autocorrelativeness)과 이전에 생긴 불규칙한 사건이 이후의 결과에 편향성을 초래하는 이동평균(Moving average)현상으로 구분하고 있음

### A. 자기상관모형(Autocorrelation) - AR모형
- 자기 상관이란 어떠한 Random Variable에 대해서 이전의 값이 이후의 값에 영향을 미치고 있는 상황을 이야기 함
- 예를 들면 이전에 값이 크면 이후에는 낮은 값이 나온다거나 하는 경향 따위를 말함
- 이러한 자기 상관은 바로 이전의 결과에 영향을 받을 수도 있지만, 드물게는 Delay가 발생하기도 함
- 우리가 실생활에서 가장 많이 발견하는 평균으로 돌아가려는 경향을 지닌 것들임. 예를 들면 용수철을 원래 길이보다 길게 잡아당기면 이후는 반드시 용수철은 줄어드는 방향으로 반발하는 움직임을 보여 궁극적으로 원래 길이로 돌아가려고 함
- 자기상관성을 시계열 모형으로 구성한 것을 AR 모형이라고 부르는데, 가장 간단한 형태가 바로 직전 데이터가 다음 데이터에 영향을 준다고 가정한 AR(1)모형임
- X(t) = {a*X(t-1) + c} + u*e(t) 
- 좀 쉽게 서술하자면, 시점 t에서 얻게 될 X(t)의 평균값은 시점 t-1에서 얻었던 X(t-1)의 값에 a를 곱하고 c를 더한 것과 같다는 뜻
- e(t)는 white noise라고 부르며, 평균이 0이고 분산이 1인 정규분포에서 도출된 random 값
- 즉 X(t) 값은 평균이 a*X(t-1) + c이며 분산이 u인 정규 분포에서 도출되는 임의의 값이라는 뜻
- 더 이전의 시점(P)를 모델에 넣고자 한다면 AR(P) 모형이 되는 셈

### B. 이동평균(Moving Average) - MA모형
- 시간이 지날수록 어떠한 Random Variable의 평균값이 지속적으로 증가하거나 감소하는 경향이 있을 수 있음
- 예를 들어 봄에서 여름이 될 수록 일반적으로 가계 전기 수요량은 증가하는 경향이 있고, 여름에서 겨울로 갈수록 감소하는 경향이 있음
- 이동평균을 시계열 모형으로 구성한 것을 MA 모형이라고 부르는데, 가장 간단한 형태가 바로 직전 데이터가 다음 데이터에 영향을 준다고 가정한 MA(1)모형임
- X(t) = {a*e(t-1) + c} + u*e(t)
- 시점 t에서 얻게 될 x(t)의 평균값은 시점 t-1에서 발생한 error e(t-1)의 값에 a를 곱하고 c를 더한 것과 같다는 뜻임
- 여기서 즉, X(t) 값은 평균이 a*e(t-1)이며, 분산이 u인 정규분포에서 도출되는 임의의 값이라는 뜼
- AR(1)과 가장 큰 차이는 이전에 발생한 error가 중요한 것이지 결과적으로 X(t-1)가 무슨 값인지는 중요하지 않다는 점
- 더 이전의 시점을 모델에 넣고자 한다면 MA(P)가 됨

### C. ARMA 모형
- ARMA는 AR모형과 MA모형을 합친 것임
- 가장 단순한 형태인 ARMA(1, 1)모형은 다음과 같음
- X(t) = {a*X(t-1)} + b{b*e(t-1)} + c + u*e(t) 
- ARMA(2, 2) 모형은 다음과 같음
- X(t) = {a1*X(t-1) + a2*X(t-2)} + {b1*e(t-1) + b2*e(t-2)} + c + u*e(t)
- 예를 들어 아래 그림과 같이 여론조사결과(X)와 실제 발생량의 차이(e)가 가지는 패턴을 이용해서 보다 나은 추정을 할 수 있지 않을까 생각해 볼 수 있음. 그래프에서 보면 조금 더 나아 보이긴 함
![img](ts_05.JPG)

### D. ARIMA 모형 
- ARIMA모형은 Autoregressive Integrated Moving Average 라는 뜻으로, ARMA 모형이 과거의 데이터들을 사용하는 것에 반해 ARIMA 모형은 이것을 넘어서서 과거의 데이터가 지니고 있던 '추세(Momentum)'까지 반영하게 됨
- 즉, Correlation 뿐 아니라 Cointegration까지 고려한 모델
- Cointegration은 Correlation보다 설명하기가 어려운데, 갖아 단순하게 설명하자고 하면 Correlation은 서로간에 선형관계를 설명하는 것이라면 Cointegration은 추세관계를 설명함. 즉 Cointegration은 시점이 고려되지 않으면 성립하지 않기 때문에 시계열 데이터에만 쓰이는 개념
- 선형관계
  - 두 변수 X-Y간의 correlation이 0보다 크면 X가 큰 값이 나올 때 Y값도 큰 값을 가진다
  - 두 변수 X-Y간의 correlation이 0보다 작으면 X가 큰 값이 나올 때 Y값은 작은 값을 가짐 
- 추세관계
  - 두 변수 X-Y간에 Cointegration이 0보다 크면 X의 값이 이전 값보다 증가하면 Y값도 증가함
  - 두 변수 X-Y간에 Cointegration이 0보다 작으면 X의 값이 이전 값보다 증가하면 Y값은 감소함
- 추가적인 example
  - 만약 Correlation이 0보다 작고 cointegration은 0보다 큰 관계라면, X가 큰 값이며 증가하는 추세에 있는 경우 Y는 현재 작은 값이나 빠르게 증가하는 추세로 반응하게 됨   
- 두가지 개념이 혼동스럽지만, 현재의 관계와 추세의 관계라는 요소로 분리해서 생각하면아주 어렵게 이해되진 않으리라 생각함
- 어쨋든, ARIMA 모형은 추세 또한 고려할 수 있기 때문에 momentum을 중요하게 보는 분석가들에게 아주 유용
- 가장 단순한 형태인 ARIMA(1, 1, 1)모형은 다음과 같음
- a*{X(t)-X(t-1)} = {b*X(t-1)} + {c*e(t-1)} + d + u*e(t)
- 위의 식은 ARMA(1,1)와 크게 다를 바가 없음. 그래서 보통 ARIMA(1, 1, 1)은 잘 쓰이지 않음
- 더 복잡한 모델인 ARIMA(1, 2, 1)를 소개하도록 하겠음
- a*[{X(t) - X(t-1)} - {X(t-1) - X(t-2)}] = {b*X(t-1)} + {c*e(t-1)} + d + u*e(t) 
- 이는 X를 2차 미분한 값에 대한 모델임. 데이터가 확실하게 모멘텀 성향을 지닌다고 가정했을 때 모멘텀의 변화를 모델링한 것이라고 보는 것이 맞겠음. 즉 이 모델은 모멘텀의 변화는 X의 이전 값과 이전에 발생한 white noise에 의해 결정된다는 것을 표현 한 것

- 시계열 분석을 통해 미래의 값을 예측하고 경향, 주기, 계절성 등을 파악하여 활용
- 시계열 분석을 위해서는 기본적으로 아래의 정상성(Stationary)를 만족해야 함
  - 평균이 일정
  - 분산이 시점에 의존하지 않음
  - 공분산은 단지 시차에만 의존하고, 시점 자체에는 의존하지 않음
![img](ts_01.JPG)
- 위의 3가지 중 하나라도 만족하지 못한다면, 비정상 시계열이라고 부름
- 실제 현실의 시계열 데이터는 비정상 시계열이 대부분이며, 비정상성 시계열 자료는 
  - 평균이 일정하지 않다면, 차분(Difference)를 통해
  - 분산이 일정하지 않다면, 변환(Transformation)을 통해 가공하여 정상 시계열 자료로 만들어 주어야 함

## R 시계열 분석 - ARIMA
### 정상성
 - 대부분의 시계열 자료는 다루기 어려운 비정상성 시계열 자료이기 때문에 분석하기 쉬운 정상성 시계열 자료로 변환
   - 평균이 일정해야 함: 모든 시점에 대해 일정한 평균을 가져야 함
   - 평균이 일정하지 않은 시계열은 차분(difference)을 통해 정상화
   - 차분은 현시점 자료에서 이전 시점 자료를 빼는 것
 - 분산도 시점에 의존하지 않아야 함
   - 분산이 일정하지 않은 시계열은 변환(transformation)을 통해 정상화
  - 공분산도 시차에만 의존할 뿐, 특정 시점에는 의존하지 않아야 함

### 시계열 모형
- 자기회귀모형(AR)
  - P시점 이전의 자료가 현재 자료에 영향을 줌
  - 오차항 = 백색잡음과정(white noise process)
  - 자기상관함수(ACF) : k기간 떨어진 값들의 상관계수
  - 부분자기상관함수(PACF) : 서로 다른 두 시점의 중간에 있는 값들의 영향을 제외시킨 상관계수
  - ACF는 빠르게 감소하면서, PACF는 어느 시점에서 절단점을 가지는 위치를 찾아야 함
  - PACF가 2 시점에서 절단점을 가지면, AR(1) 모형
- 이동평균모형(MA)
  - 유한한 개수의 백색잡음 결합이므로, 항상 정상성을 만족함
  - ACF가 절단점을 갖고, PACF는 빠르게 감소하는 위치를 찾아야 함
  - ex) ACF가 2부터 점선 안에 존재하면, --> MA(1)   
- 자기회귀누적이동평균 모형(Autoregressive integrated moving average model, ARIMA)
  - 비정상 시계열 모형
  - 차분이나 변환을 통해 AR, MA, 또는 이 둘을 합한 ARMA 모형으로 정상화
  - ARIMA(p, d, q) --> d : 차분 차수, p : AR 모형 차수, q : MA 모형 차수    
- 분해 시계열
  - 시계열에 영향을 주는 일반적인 요인을 시계열에서 분리해 분석해주는 방법
  - 시계열 요인, 순한 요인, 추세 요인, 불규칙 요인 

### R 분석 source code
~~~r
# 1) 소스 데이터를 시계열 데이터로 변환
ts(data, frequency = n, start = c(시작년도, 월))

# 2) 시계열 데이터를 x, trend, seasonal, random 값으로 분해
decompose(data)

# 3) 시계열 데이터를 이동평균한 값 생성
SMA(data, n = 이동평균수)

# 4) 시계열 데이터를 차분
diff(data, differences = 차분횟수)

# 5) ACF 값과 그래프를 통해 래그 절단값을 확인
acf(data, lag.max = 래그수)

# 6) PACF 값과 그래프를 통해 래그 절단값을 확인
pacf(data, lag.max = 래그수)

# 7) 데이터를 활용하여 최적의 ARIMA 모형을 선택
auto.arima(data)

# 8) 선정된 ARIMA 모형으로 데이터를 보정(fitting)
arima(data, order = c(p, d, q))

# 9) ARIMA 모형에 의해 보정된 데이터를 통해 미래값을 예측
forecast.Arima(fittedData, h = 미래예측수)

# 10) 시계열 데이터를 그래프로 표현
plot.ts(시계열데이터)

# 11) 예측된 시계열 데이터를 그래프로 표현
plot.forecast(예측된시계열데이터)

# Decompose non-seasonal data
# 영국왕들의 사망시 나이
library(TTR)
library(forecast)
kings <- scan("http://robjhyndman.com/tsdldata/misc/kings.dat", skip = 3)
kings

# 시계열 데이터로 변환
kings_ts <- ts(kings)
kings_ts

plot.ts(kings_ts)

# 이동평균
kings_sma3 <- SMA(kings_ts, n = 3)
kings_sma8 <- SMA(kings_ts, n = 8)
kings_sma12 <- SMA(kings_ts, n = 12)

par(mfrow = c(2,2))

plot.ts(kings_ts)
plot.ts(kings_sma3)
plot.ts(kings_sma8)
plot.ts(kings_sma12)

# 차분을 통해 데이터 정상화
kings_diff1 <- diff(kings_ts, differences = 1)
kings_diff2 <- diff(kings_ts, differences = 2)
kings_diff3 <- diff(kings_ts, differences = 3)

plot.ts(kings_ts)
plot.ts(kings_diff1)    # 1차 차분만 해도 어느정도 정상화 패턴을 보임
plot.ts(kings_diff2)
plot.ts(kings_diff3)

par(mfrow = c(1,1))
mean(kings_diff1); sd(kings_diff1)

# 1차 차분한 데이터로 ARIMA 모형 확인
# --> ARIMA(3,1,1) 최종 선택 가능
acf(kings_diff1, lag.max = 20)      # lag 2부터 점선 안에 존재. lag 절단값 = 2. --> MA(1)
pacf(kings_diff1, lag.max = 20)     # lag 4에서 절단값 --> AR(3)

# 자동으로 ARIMA 모형 확인
auto.arima(kings)   # --> ARIMA(0,1,1)

# 예측
kings_arima <- arima(kings_ts, order = c(3,1,1))    # 차분통해 확인한 값 적용
kings_arima

kings_fcast <- forecast(kings_arima, h = 5)
kings_fcast

forecast::autoplot(kings_fcast)

kings_arima1 <- arima(kings_ts, order = c(0,1,1))   # auto.arima 추천값 적용
kings_arima1

kings_fcast1 <- forecast.Arima(kings_arima1, h = 5)
kings_fcast1

plot.forecast(kings_fcast1)

# Decompose seasonal data
# 1946년 1월부터 1959년 12월까지 뉴욕의 월별 출생자 수 데이터
data <- scan("http://robjhyndman.com/tsdldata/data/nybirths.dat")
birth <- ts(data, frequency = 12, start = c(1946, 1))
birth

plot.ts(birth, main = "뉴욕 월별 출생자 수")

# 데이터 분해 - trend, seasonal, random 데이터 추세 확인
birth_comp <- decompose(birth)
plot(birth_comp)

birth_comp$trend
birth_comp$seasonal

# 시계열 데이터에서 계절성 요인 제거
birth_adjusted <- birth - birth_comp$seasonal
plot.ts(birth_adjusted, main = "birth - seasonal factor")

# 차분을 통해 정상성 확인
birth_diff1 <- diff(birth_adjusted, differences = 1)
plot.ts(birth_diff1, main = "1차 차분")       # --> 분산의 변동성이 크다

acf(birth_diff1, lag.max = 20)
pacf(birth_diff1, lag.max = 20)

# PACF 절단값이 명확하지 않아 ARIMA 모형 확정이 어렵다.
# ---> Auto.Arima 함수 사용
auto.arima(birth)             # ARIMA(2,1,2)(1,1,1)[12]
birth_arima <- arima(birth, 
                     order    = c(2,1,2), 
                     seasonal = list(order = c(1,1,1), period = 12))
birth_arima

birth_fcast <- forecast(birth_arima)
birth_fcast
plot(birth_fcast, main = "Forecasts 1960 & 1961")

# 1987년 1월부터 1993년 12월까지 리조트 기념품매장 매출액
data <- scan("http://robjhyndman.com/tsdldata/data/fancy.dat")
fancy <- ts(data, frequency = 12, start = c(1987, 1))
fancy
plot.ts(fancy)   # 분산이 증가하는 경향 --> log 변환으로 분산 조정
fancy_log <- log(fancy)
plot.ts(fancy_log)
fancy_diff <- diff(fancy_log, differences = 1)
plot.ts(fancy_diff)   

# 평균은 어느정도 일정하지만 특정 시기에 분산이 크다 
# --> ARIMA 보다는 다른 모형 적용 추천
acf(fancy_diff, lag.max = 100)
pacf(fancy_diff, lag.max = 100)
auto.arima(fancy)   # ARIMA(1,1,1)(0,1,1)[12]

fancy_arima <- arima(fancy, order = c(1,1,1), seasonal = list(order = c(0,1,1), period = 12))
fancy_fcast <- forecast(fancy_arima)
plot(fancy_fcast)

# 1500년부터 1969년까지 화산폭발 먼지량
data <- scan("http://robjhyndman.com/tsdldata/annual/dvi.dat", skip = 1)
dust <- ts(data, start = c(1500))
dust
plot.ts(dust)  # 한두개 데이터를 제외하고는 평균과 분산이 어느정도 일정하다 --> 차분 안함.
acf(dust, lag.max = 20)     # lag = 4 : MA(3)
pacf(dust, lag.max = 20)    # lag = 3 : AR(2)
auto.arima(dust)            # ARIMA(1,0,2)

# d = 0 이므로 AR(2) / MA(3) / ARIMA(2,0,3) 중 선택해서 적용 가능.
# 모수가 가장 적은 모형을 선택하는 것을 추천 --> AR(2) 적용
dust_arima <- arima(dust, order = c(2,0,0))
dust_fcast <- forecast.Arima(dust_arima, h = 30)
plot.forecast(dust_fcast)
~~~

## ADP 기출 문제 / 예제 실습
~~~r
library(TTR)
library(forecast)
library(tseries)
kings <- scan("http://robjhyndman.com/tsdldata/misc/kings.dat", skip = 3)
kings
king.ts <- ts(kings)
plot(king.ts)

#- 1. 정상성 확인(10점)
# 위의 시계열 그래프를 보면 평균 시간에 따라 일정치 않은 모습을 보이므로 비정상 시계열임

#- 2. ARIMA 모델 3가지 제시(10점)
# ARIMA 모델은 정상성 시계열에 한해 사용하므로,
# 비정상 시계열 자료는 차분을 통해 정상 시계열로 만들어줌
king.diff <- diff(king.ts, difference = 1)
plot(king.diff)

# 1차 차분 결과에서 평균과 분산이 시간에 따라
# 의존하지 않음을 알 수 있음
# ARIMA(p,1,q) 모델이며, 차분을 1회 해야 정상성을 만족
# 정상성을 만족한 시계열로 만들었으면, ACF와 PCAF를 통하여 적합한 ARIMA 모델을 결정

#- ACF
# lag는 0부터 값을 갖는데, 너무 많은 구간을설정하면 그래프 판단이 어려우니 20으로 설정
# ACF값이 lag1인 지점을 제외하고 모두 점선 구간 안에 있으므로, lag2에서 절단점을 가짐
# --> MA(1)
acf(king.diff, lag.max = 20)

#- PACF
#- PACF 값이 lag 1, 2, 3에서 점선 구간을 초과하고 나머지는 점선 안에 있으므로, lag4에서 절단점을 가짐
#- AR(3)
pacf(king.diff, lag.max = 20)

#- auto.arima
#- forecast package 내장된 auto.arima() 함수 이용
#- 영국 왕들의 사망 나이 데이터의 적절한 ARIMA 모델은 ARIMA(0, 1, 1)
auto.arima(king.ts)

#- 결과적으로 초기 분석에 의해 생성된 ARIMA 모델 후보는 다음 3가지
#- AR(3) --> ARIMA(3, 1, 0) 
#- MA(1) --> ARIMA(0, 1, 1) * auto.arima와 동일
#- ARMA(3,1) --> ARIMA(3, 1, 1)

#- 한가지 모델을 최종 선택하고 이유를 서술 
#- 위의 3가지 모델들의 AICc 값을 아래와 같이 계산하여 비교해봄
#- 가장 작은 값을 가지는 모델이 가장 좋은 모델로 판별 가능 
Arima(king.ts, order = c(3, 1, 0))
Arima(king.ts, order = c(0, 1, 1))
Arima(king.ts, order = c(3, 1, 1))

#- 최종 예측을 하고, 실제 결과와 비교하고 그 평가 방법을 사용한 이유를 서술
#- 일반적으로 실제 결과와 비교하려면 testDataset을 통한 실제 결과를 만들어 냄
train <- subset(king.ts, end = length(king.ts) - 9) 
test  <- subset(king.ts, start = length(king.ts) - 8)
plot(train)

train.diff <- diff(train, differences = 1)
plot(train.diff)

acf(train.diff)  # 절단점 2 --> MA(1)
Fit1 <- Arima(train.diff, order = c(0,1,1))
Fit1 %>% forecast(h = 8) %>% autoplot() 

pacf(train.diff) # 절단점 4, AR(3)
Fit2 <- Arima(train.diff, order = c(3,1,0))
Fit2 %>% forecast(h = 8) %>% autoplot()

Fit3 <- auto.arima(train.diff)
Fit3 %>% forecast(h=8) %>%  autoplot() 

king.test1 <- Arima(test, model = Fit1)
king.test2 <- Arima(test, model = Fit2)
king.test3 <- Arima(test, model = Fit3)

accuracy(king.test1)
accuracy(king.test2)
accuracy(king.test3)
~~~
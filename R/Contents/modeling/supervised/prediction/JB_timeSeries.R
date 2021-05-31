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

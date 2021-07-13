library(TTR)
library(forecast)

kings <- scan("http://robjhyndman.com/tsdldata/misc/kings.dat", skip = 3)
kings
king.ts <- ts(kings)
plot(king.ts)

king.diff <- diff(king.ts, difference = 1)
plot(king.diff)

train <- subset(king.ts, end = length(king.ts) - 9) 
test  <- subset(king.ts, start = length(king.ts) - 8)
train.diff <- diff(train, differences = 1)
plot(train.diff)

acf(train.diff)  # 절단점 2 --> MA(1)
Fit1 <- Arima(train.diff, order = c(0,1,1))
Fit1 %>% forecast(h = 8) %>% autoplot() 

Fit3 <- auto.arima(train.diff)
Fit3 %>% forecast(h=8) %>%  autoplot() 

king.test1 <- Arima(test, model = Fit1)
king.test2 <- Arima(test, model = Fit2)
king.test3 <- Arima(test, model = Fit3)

accuracy(king.test1)
accuracy(king.test2)
accuracy(king.test3)

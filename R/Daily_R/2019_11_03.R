## 2019_11_03.R
## anomaly detection 개념 정리
## forecast, FBN package를 이용한 시계열 합분해, 곱분해 예시 수행
## 

## anomaly detection 

#' 시계열 분해는 시계열을 계절적(seasonal) 시계열, 트랜드 시계열, 랜덤 잔여 시계열로 나눔.
#' 트렌드와 랜덤 시계열은 둘 다 비정상을 감지하는데 사용할 수 있음
#' 그러나 이미 비정상적인 시계열에서 비정상(anomaly)를 탐지하는 것은 쉽지 않음

#' 비정상적인 시계열로 작업하기
#' 이동 평균 분해를 통한 이상 탐지는 작동 X
#' 이동 중앙값 분해를 통한 이상 탐지는 작동함

#' 1. 이동 평균을 이용한 분해를 사용하여 비정상 감지
#' 2. 이동 중앙값을 사용한 분해를 사용하여 비정상 감지

#' Dataset : webTraffic.csv 는 103주(2년) 동안 일별 페이지 뷰 기록.
#'           재미를 더하기 위해 랜덤성을 추가할 것임
#'           시계열을 보면 주말 트래픽이 적기 때문에 7일의 주기적 계절성을 명확하게 볼 수 있음
#'           계절 시계열을 분해하려면 계절성 시간주기가 필요
#'           우리는 7일이라는 것을 알고 있음
#'           푸리에 변환을 통해 미리 알 수 없는 경우에도 시계열의 계절성을 구할 수 있음
#'           시계열 분해가 가산적인지, 곱셈인지를 알아야함. 


#' Tip
#' 시계열 성분
#' 추세-주기 성분, 계절성 성분, (시계열의 나머지 요소를 포함하는) 나머지(remainder) 성분으로 나뉨
#' 덧셈 분해(additive decomposition)
#' yt = St + Tt + Rt,

#' 계열에서 전환점을 살펴보는 것과 어떤 방향으로의 변화를 해석하려는 것이 목적이라면, 
#' 계절성으로 조정된 데이터보다는 추세-주기 성분을 사용하는 것이 더 낫습니다.

#' 이동 평균 평활
#' 즉, k기간 안의 시계열 값을 평균하여 시간 t의 추세-주기를 측정
#' 차수  m의 이동 평균이라는 의미에서 “ m-MA” 라고 부릅니다.

install.packages("forecast")
library(forecast)



movingAvrDetec <- function(df,  Xvar = NA, intervals = 5, sigma = 3, decomp = "additive"){
  
  require(FBN);require(ggplot2)
  if(is.na(Xvar))stop("독립변수를 입력하세요!")
  
  real <- df[,Xvar]
  decomposed_days = decompose(ts(real, frequency = intervals), decomp)
  
  trend_data <- decomposed_days[['trend']]
  
  min = mean(trend_data, na.rm = T) - sigma*sd(trend_data, na.rm = T)
  min = ifelse(min < 0, 0, min)
  max = mean(trend_data, na.rm = T) + sigma*sd(trend_data, na.rm = T)
  
  plot(as.ts(as.vector(trend_data)), ylim = c(min-0.5,max+0.5))
  abline(h=max, col="#e15f3f", lwd=2)
  abline(h=min, col="#e15f3f", lwd=2)
  
  # 이상 위치 detect point 찍어주기
  position = data.frame(id=seq(1, length(random)), value=random)
  
  anomalyH = position[position$value > max, ]
  anomalyH = anomalyH[!is.na(anomalyH$value), ]
  
  anomalyL = position[position$value < min, ]
  anomalyL = anomalyL[!is.na(anomalyL$value), ]
  
  anomaly = data.frame(id=c(anomalyH$id, anomalyL$id), value=c(anomalyH$value, anomalyL$value))
  anomaly = anomaly[!is.na(anomaly$value), ]
  
  realAnomaly = real[anomaly$id, ]
}




set.seed(4)
data <- read.csv("webTraffic.csv", sep = ",", header = T)
days = as.numeric(data$Visite)

# 무작위 잡음을 넣은 데이터
# runif function을 통해 무작위 잡음을 추가

for (i in 1:45) {
  pos = floor(runif(1, 1, 50))
  days[i*15+pos] = days[i*15+pos]^1.2
}

days[510+pos] = 0
plot(as.ts(days))



## 1. 이동 평균값(moving average)를 이용한 anomaly detection 수행

# 시계열이 비정상적(anomalous)이기 때문에 분해를 통해 구해진 추세(trend) 또한 완전히 잘못 나옴
# 실제로 비정상요소들이 평균에 포함

install.packages("FBN")
decomposed_days = decompose(ts(days, frequency = 7), "additive")
ggplot(decomposed_days)

# 랜덤 잡음에서 비정상을 검출하기 위해 정규 분포를 적용 할 수 있습니다. 표준 편차의 4배 밖의 값을 이상치(outlier)로 간주

random = decomposed_days$random

min = mean(random, na.rm = T) - 4*sd(random, na.rm = T)
max = mean(random, na.rm = T) + 4*sd(random, na.rm = T)

plot(as.ts(as.vector(random)), ylim = c(-0.5,2.5))
abline(h=max, col="#e15f3f", lwd=2)
abline(h=min, col="#e15f3f", lwd=2)

#find anomaly

position = data.frame(id=seq(1, length(random)), value=random)
anomalyH = position[position$value > max, ]
anomalyH = anomalyH[!is.na(anomalyH$value), ]
anomalyL = position[position$value < min, ]
anomalyL = anomalyL[!is.na(anomalyL$value), ]
anomaly = data.frame(id=c(anomalyH$id, anomalyL$id), value=c(anomalyH$value, anomalyL$value))
anomaly = anomaly[!is.na(anomaly$value), ]

plot(as.ts(days))

real = data.frame(id=seq(1, length(days)), value=days)
realAnomaly = real[anomaly$id, ]
points(x = realAnomaly$id, y =realAnomaly$value, col="#e15f3f")

## 2. 이동 중앙값(moving median)을 이용한 anomaly detection 수행
library(forecast)
library(stats)

trend = runmed(days, 7) # 7일치의 중앙값 계산
plot(as.ts(trend))      # ploting 

# 분해 공식에서 알 수 있듯이, 원 시계열에서 추세와 계절성을 제거하면 랜덤 노이즈만 남음.
# 랜덤 노이즈는 정규적으로 분포할 것이므로, 정규 분포를 적용하여 이상을 탐지 할 수 있습니다
# 정규 분포에서 표준편차 4배 밖의 값은 이상치로 간주될 수 있음.
# 무작위 시계열에는 여전히 비정상치가 포함되어 있으므로 비정상치는 빼고 표준 편차를 추정해야 함

detrend = days / as.vector(trend)             # 기존 중앙값으로 row data를 나눠줌
m = t(matrix(data = detrend, nrow = 7))       # 7일씩 구성될 수 있도록 matrix 구성
seasonal = colMeans(m, na.rm = T)             # 계절성을 제외하기 위해서 주기 평균 계산
random = days / (trend * seasonal)            # 기존 데이터에 trend, seasonal 를 나누어 줌
rm_random = runmed(random[!is.na(random)], 3) # 다시 해당 데이터의 중앙 값을 계산 

min = mean(rm_random, na.rm = T) - 4*sd(rm_random, na.rm = T)
max = mean(rm_random, na.rm = T) + 4*sd(rm_random, na.rm = T)

plot(as.ts(random))
abline(h=max, col="#e15f3f", lwd=2)
abline(h=min, col="#e15f3f", lwd=2)
######################
### 혼합 분포 군집 ###
######################
#' 혼합분포군집은 모형 기반의 군집방법
#' 데이터가 k개의 모수적 모형의 가중합으로 표현되는 모집단 모형으로부터 나왔다는 가정하에서 
#' 모수와 함께 가중치를 자료로부터 추정하는 방법 사용
#' k개의 각 모형은 군집을 의미
#' 각 데이터는 추정된 k개의 모형 중 어느 모형으로부터 나왔을 확률이 높은지에 따라 군집의 분류가 이루어짐

#' R에서 정규혼합분포의 추정과 군집화는 패키지 mixtools, mclust, nor1mix, HDclassif, EMcluster


############
## 예제 1 ##
############
#' 예제 1는 R 패키지 mixtools의 normalmixEM() 함수를 통해 혼합분포군집을 수행한 예제

library(mixtools)
data(faithful)

#- faithful 자료에 대한 히스토그램은 다음과 같음
hist(faithful$waiting, 
     main = "Time between Old Faithful eruptions", 
     xlab = "Minutes", 
     ylab = "", 
     cex.main = 1.5, 
     cex.lab = 1.5, 
     cex.axis = 1.4)


#- EM 알고리즘을 이용한 정규혼합분포의 추정결과는 다음과 같음
wait1 <- normalmixEM(faithful$waiting, lambda = .5, mu = c(55, 80), sigma = 5)
summary(wait1)

#- 추정된 정규혼합분포를 시각화 하면 다음과 같음
plot(wait1, density = T, cex.axis = 1.4, cex.lab = 1.4, cex.main = 1.8,
     main2 = "Time between Old Faithful eruptions", xlab2 = "Minutes")

#- EM 알고리즘을 통해 모수를 추정하는 과정에서 
#- 반복횟수 2회 만에 로그-가능도 함수가 최대가 됨을 알 수 있음

############
## 예제 2 ##
############
#- R 패키지 {mnist}의 Mclust() 함수를 통한 혼합분포군집을 수행한 예제
#- iris 자료에 대해 Mclust() 함수를 통해 군집 분석을 수행하면 다음과 같음
#- 혼합분포의 모수추정치와 함께, 각 군집별 해당 자료에 대한 요약 결과를 제공
library(mclust)
mc <- Mclust(iris[,1:4], G = 3)
summary(mc, parameters = TRUE)
plot.Mclust(mc)

#- 각 개체가 어느 그룹으로 분류되었는지는 다음을 통해 알 수 있음
str(mc)
mc$classification

#- 새로운 자료에 대한 분류는 predict()를 사용
predict(mc, data = iris)

mc$classification
mc_pred <- predict(mc, data=iris)
mc_pred$classification

str(mc)
mc$classification
predict(mc, data = iris)

#- plot.Mclust() 함수는 다양한 방식으로 군집 결과를 시각화 함
plot.Mclust(mc)

library(ggplot2)
library(dplyr)
options(scipen = 999)
p <- ggplot(faithful, aes(x = waiting)) + geom_density()
p

p + geom_vline(xintercept = 53, col = "red", size = 2) + geom_vline(xintercept = 80, col = "blue", size = 2)

library("mixtools")
set.seed(1)

#' Plot a Mixture Component
#' @param x Input data
#' @param mu Mean of component
#' @param sigma Standard deviation of component
#' @param lam Mixture weight of component
plot_mix_comps <- function(x, mu, sigma, lam){
   lam * dnorm(x, mu, sigma)
}

wait   <- faithful$waiting
mixmdl <- normalmixEM(wait, k = 2)

mixmdl$mu
mixmdl$sigma

post.df <- as.data.frame(cbind(x = mixmdl$x, mixmdl$posterior))

post.df %>%
  mutate(label = ifelse(comp.1 > 0.3, 1, 2)) %>% 
  ggplot(aes(x = factor(label))) +
  geom_bar() +
  xlab("Component") +
  ylab("Number of Data Points")


wait1 <- normalmixEM(faithful$waiting, lambda = .5, mu = c(55,80), sigma = 5)
plot(wait1, density = TRUE, cex.axis=1.4, cex.lab=1.4, cex.main=1.8, main2="Time between Old faithful eruptions", xlab2="Minutes")

install.packages("mclust")

library(mclust)
mc <- Mclust(iris[,1:4], G = 3)
summary(mc, parameters = TRUE)
plot.Mclust(mc)

mc$classification
mc_pred <- predict(mc, data=iris)
mc_pred$classification

str(mc)
mc$classification
predict(mc, data = iris)


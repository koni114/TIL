## 2019_10_30.R

## 1. 수치형으로 변환가능한지 확인하는 방법.
## package를 이용하면 더 좋은 것들이 있긴 할텐데.. 
## idea : as.numeric function으로 변경했을 때, 수치형이 아닌 것들은 NA로 return 됨
##        따라서 NA가 있는 경우 수치형으로 변환 할 수 없으므로, 이때는 변경 X, 전부 TRUE인 경우는 수치형으로 변환

test <- (test = c('1', '2', 'b'))
suppressWarnings(all(!is.na(as.numeric(as.character(col)))))

## 2. factor형인 vector에서 level의 값을 1, 0 으로 변환하고 싶을 때,
##    labels param을 사용하여 지정하면 levels <-> labels 를 mapping시켜서 데이터를 변환 시켜줌!

test <- c('a', 'b')
test <- as.factor(test)
test <- factor(test, levels = levels(test), labels = c(0, 1))


## 3. combinat package
## Combination, permuation에 대한 조합을 계산해주는 package(매우 편리)
## 실제 구현하려면 back tracking을 이용해서 알고리즘을 짜야 하므로, 시간이 걸리는데 이를 package로 풀어내줌!
## 아마 permutation, combination, multibinomial 등을 return

# install.packages("combinat")
library(combinat)
Xvar <- c('a', 'b', 'c', 'd')    # 
combn(Xvar, 2)                   # nC2 경우의 수의 조합을 matrix로 return 시켜줌!

## 4. 교호작용에 대해서 헷갈리지 말자!
#' Logistic Regression : Y : 범주, X : 연속 + 범주, 독립변수에 대한 교호작용 check 
#' GLM                 : Y : 연속, X : 연속 + 범주, 독립변수에 대한 교호작용 check
#' ANOVA               : Y : 연속, X : 범주, 독립변수(범주임을 잊지말자!)에 대한 교호작용 check


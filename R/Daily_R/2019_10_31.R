# 2019_10_31.R

## 들어가기 전에 생각하기! 
## ** 교호작용도(interaction plot)

#  교호작용도의 선이 평행으로 나타나면 교호작용이 없다고 판단할 수 있음.
#  교호작용도가 평행하다고 해서 통계적으로 의미 없다는 뜻은 아니다.

## 교호작용도는 도대체 어떤 변수들의 작용 관계를 확인하는 것인가? 
#  중요한 것은, 종속변수와 독립변수 한개를 각각 X, Y축에 두고(일반적으로 X축에 범주 OR 수치, Y축에 수치로 둔다) group 변수로 또다른 독립변수를 둬서 
#  교호작용도를 그린다! **** 헷갈리지 말아야 할 점.

## 1. 두 범주형 값 + 한개의 수치형 변수에 대한 교호작용도 그리기 ----

install.packages("psych")
library(plyr)
library(psych)
library(ggplot2)

# ToothGrowth : 데이터는 정확히 모르겠지만, supp, dose는 범주형.
#               len -> 수치형.

# 각 그룹별 평균값 계산.
toothInt <- ddply(ToothGrowth,.(dose, supp), summarise, val = mean(len))

# ggplot 생성.
# boxplot은 기존 데이터를 가지고 그리고, point와 line은 toothInt dataFrame을 통해 그림.

ggplot(ToothGrowth, aes(x = factor(dose), y = len, colour = supp)) + 
  geom_boxplot() + 
  geom_point(data = toothInt, aes(y = val)) +
  geom_line(data = toothInt, aes(y = val, group = supp)) + 
  theme_bw()


## 2. 두 연속형 + 한개의 범주형 변수에 대한 교호작용도 그리기 ----
library(reshape2)

# tips dataset <- reshape2 package 내장 data


# 두 그룹간의 lm을 만들어서, 이 두 선의 교호작용을 확인하는 개념으로 접근할 수 있다
##  두개의 연속형 변수의 상호작용이 있는 경우,
# mtcars 데이터를 이용

# mpg                      -> Y
# Wt(공차중량), hp(마력수) -> X

## 회귀 모형 만들기
fit2 = lm(mpg~wt*hp,data=mtcars)
summary(fit2)

# hp와 mpg 간의 회귀공식은 wt의 값에 따라 달라짐.
# wt 값의 사분위수를 확인해보자

summary(mtcars$wt)

# 즉, mtcars 데이터에 있는 자동차들 중 가장 가벼운 차는 1.153, 
# 가장 무거운 차는 5.424임을 알 수 있음.
# wt와 mpg 사이의 회귀공식은 hp에 따라 달라짐.
# 즉 회귀 계수를 소수점 두자리에서 반올림하면 다음과 같은 회귀식을 얻을 수 있음.

# interaction 시각화 해보기

# 1. 평균-표준편차, wt의 평균, wt + 표준편차를 이용하여 상호작용 시각화
#    즉 wt의 값이 3개로 주어졌을 때의 mpg = X1 * hp 식 3개를 구하고, 이를 그리는 방식

A      <- c(2.2,3.2,4.2)       # wt의 구간별 값..
coef   <- fit2$coef            # 회귀 계수, 1: intercept, 2: wt, 3:hp, 4:wt:hp
labels <- as.character(A)      # 문자열로 바꾸어야 matrix 곱이 되는듯
intercept <- coef[1] + coef[2]*A # 
slope     <- coef[3] + coef[4]*A

colour= rainbow(length(A))
df1   = data.frame(A,intercept,slope,colour)   

p <- ggplot(data=mtcars,aes(x=hp,y=mpg))+geom_point()
p <- p + geom_abline(data = df1, aes(slope=slope, intercept=intercept, colour=colour))
p <- p + scale_colour_discrete(labels=labels)+labs(colour="wt")
p








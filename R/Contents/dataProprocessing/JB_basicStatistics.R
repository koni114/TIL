#- 기술 통계량 구해주는 유용한 함수들
summary(iris$Sepal.Length)

by(iris$Sepal.Length, iris$Species, mean)


#- n : 개수
#- kurtosis : 첨도, 0보다 클수록 뾰족함
#- skew : 왜도, 대칭인 분포면 왜도가 0임 
#-        skew > 0 이면, 오른쪽으로 긴 꼬리를 가짐
#-        skew < 0 이면, 왼쪽으로 긴 꼬리를 가짐

library(psych)
psych::describe(iris)


#- dplyr -> summarise를 활용
library(dplyr)
iris %>%  group_by(Species) %>% summarise_all()


x <- 100
if(x >= 10){
  print("check")
}else if(x>= 5 && x <= 10){
  print("Hello")
}else{
  print("helloss")
}



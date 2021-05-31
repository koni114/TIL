# ** 특정 데이터의 신뢰구간과 백분율은 어떻게 다른가?
#   
# ** 신뢰구간(confidence Level)
# 구간 내에 실제 모수가 존재할 것으로 예측되는 구간으로 정의.
# 90%, 95%, 99% 등 다양한 정도의 구간추청이 가능.
# 
# 모평균의 95% 신뢰구간. = X + 1.96 X ( s / sqrt(n)  )
# 
# 표본들의 평균과 표준편차가 비슷하다면, 95% 신뢰구간의 폭은 표본수에 영향을 줌.
# 
# * 백분율은
# 전체 모집단 데이터에서, 데이터의 비율 값

# 기본적으로 작용하는 for문을 apply 계열로 변경하기. ----

library(data.table)
test <- as.data.frame(rbindlist(lapply(split(iris[1:5,], rownames(iris[1:5,])), function(x){
  x$Petal.Width <- 100000
  x
})))

# dplyr::mutate function 을 이용하여 이상치 처리 방법.
# 기본적으로 mutate function은 파생 변수를 만드는 함수이지만, 기존에 있는 변수 명으로 덮어쓰면,
# 해당 변수 값을 바꿀 수 있음!
library(dplyr)
library(rlang)

df_tmp <- iris
xVar <- "Sepal.Length"

# iris의 특정 변수 값의 이상치라고 판단되는 변수를 처리하는 경우,
# ** !!xVar := 는 변수안에 있는 문자열을 변수로 인식하게 하고 싶을 때!

df_tmp %>% mutate(!!xVar := ifelse(!!sym(xVar) >= 6.0
                                   , 100
                                   , ifelse(!!sym(xVar) <= 4.5
                                            , -100
                                            , !!sym(xVar)
                                   )
)
)
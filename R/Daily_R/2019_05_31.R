# ** R에서의 전역 변수
#' R에서 지역함수에서 전역 변수 접근하거나
#' 전역 변수의 값을 변경하고 싶을 때,
#' get, assign function + parent.frame 사용

# ex) vSubs 전역 변수를 test 지역 함수에서 변경 및, 호출하고 싶을때
# 호촐 같은 경우에는 가능. but python 과는 다르게 변경은 불가
# -> parent.frame parameter를 통해 setting

vSubs <- "hello"

test <- function(x){
  # vSubs = get("vSubs", parent.frame(n = 1)) 
  print(vSubs)
  vSubs <- x
  # assign("vSubs", vSubs, parent.frame(n = 1))
}

test("world")
print(vSubs)

# type convert function
# -> 문자형 컬럼을 자동으로 인식해서 수치형 컬럼으로 변경해주는 function
#    굉장히 유용!
# but, 문자형인 경우에만 인식한다. 수치형 컬럼이 있어서는 안됨
# 다음과 같이 점검 해주는 것이 좋음

if(sum(is.na(as.numeric(df[, cc]))) == 0){
  df[, cc] <- type.convert(df[, cc], na.strings = 'NA', as.is = T)
}


# plyr::revalue function
# 요인(factor) 형태의 데이터의 라벨을 변경하는 방법으로, plyr 패키지 안에 있는 revalue() 함수를 이용
#  revalue(요인 데이터, replace("기존라벨" = "새로운 라벨"))
smoke = factor(c(1, 2, 1, 1, 2))
levels(smoke)  # 결과물 : 1, 2

# 1 -> Smoking, 2 -> No Smoking 으로 변경
install.packages("plyr")
library(plyr)
smoke = revalue(smoke, replace = c("1" = "Smoking", "2" = "No Smoking"))
levels(smoke)

# step function 성능 이슈
# 기본적으로 step 함수는 굉장히 느린 성능 이슈가 존재한다(특히 로지스틱 범주 모델)
# stackoverFlow 내 30개의 변수를 stepwise 하는데 6 시간 정도 걸린다고 되어 있음.

# kable function
# 데이터를 표형식으로 보여주는 함수
# dataFrame를 넣으면, 표형식으로 return









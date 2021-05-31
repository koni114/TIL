# 일표본 T-TEST 검정

# input Data
# 1. df
# 2. 독립변수(수치형)
# 가설 검정 수행시,
# 3 .신뢰수준 입력
# 4. 모평균 입력
# 5. 대립가설 선택(평균 < 가설평균, 평균 > 가설평균, 평균 != 가설평균)

# dplyr을 이용한 특정 유형 타입 선택
# iris를 이용한 예시
library(dplyr)
xVar <- names(iris %>% select_if(is.numeric))

# 사소한 Tip
# 크롬에서 cashe 지우는 방법 -> F12 -> network -> disabled cashe 체크 -> F5 누르면 캐쉬가 지워짐 

# ** foreach 완벽 정복
# 루프(loop)와 lapply() 함수를 융합한 것으로 R의 병렬처리에 있어 매우 인기가 많음
# foreach 함수의 .combine 속성은 결과를 어떻게 결합시킬지를 정의
# .combine 속성 정리
# 1. .combine = c : vector 
# 2. .combine = rbind : matrix, cbind : 컬럼 결합 형태
# 3. .combine = list : list 형태로 return

# 외부에서 정의된 변수는 foreach문 내에서 사용 가능
# 외부 함수를 사용하고 싶으면, .export  = "함수명" 을 선언함으로써 사용 가능

# iris -> 4개 수치형 컬럼에 대한 일표본 t-test 결과 값을 dataFrame 형태로 저장
library(foreach)
numeric.name <- names(iris %>% select_if(is.numeric))
ttt <- unique(iris[,5])

result.table <- data.frame( variable = character(0)
                            , t.value = character(0) 
                            , alternative = character(0)
                            , p.value = character(0)
                            , confidence.level = character(0)
)


ave(iris, iris[,5], FUN =function(x){
  print(x[1,])
})

tt <- foreach(xVar = numeric.name, .combine = function(a,b){dplyr::bind_rows(a,b)}) %do% {
  ave(iris[,xVar], iris[,ttt], FUN = function(x){
    tmp.TTest <- t.test(iris[,xVar]
                        , y = NULL
                        , alternative = c("two.sided")
                        , mu = 0
                        , paired = F
                        , var.equal = F
                        , conf.level = 0.95
    )
    d0 <- data.frame(variable = xVar
                     , t.value = tmp.TTest$statistic
                     , alternative = tmp.TTest$alternative
                     , p.value = tmp.TTest$p.value
                     , confidence.level = paste0("(",tmp.TTest$conf.int[1] , " , ",tmp.TTest$conf.int[2],") ")
                     , stringsAsFactors = F)
    d0
    result.table <- rbind(result.table, tt)
  })
}




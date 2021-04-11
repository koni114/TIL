# getMode function
# R에는 최빈값을 구하는 function이 없음
# 따라서 다음과 같이 응용하여 사용할 수 있음
# ** tabulate function : vector에 있는 값을 table 화 시켜줌

getMode <- function(v){
  uniq  <- unique(v)
  uniqv[which.max(tabulate(match(v, uniq)))]
}

# getMode 내부 TEST 예제

test      <- c(1,2,1,1,3,4,6,NA)
uniq.test <- unique(test)
match(test, uniq.test) # test와 uniq.test가 mapping 되는 uniq.test 의 index 가 return 됨

# match function
# match(찾고 싶은 값, vector) -> vector와 매칭되는 vector index(찾고 싶은 값 index가 아니라 vector index) 반환
# 사용 예시
test <- c(1,2,1,1,3,4,6,NA)
uniq.test <- unique(test)
match(test, uniq.test)

# parent.frame() function 
# the parent function , parent.frame() in r 알아보기
# 부르는 입장인 함수를 parent function 이라 한다.
# f가 h를 부른다. (return 문에서!)
# 이렇게 부르는 입장인 함수를 parent function 이라 한다.
rm(list = ls())

f <- function(y) {
  d <- 8
  print(ls())
  print(ls(envir=parent.frame(n=1)))
  return(h(d,y))
}

h <- function(dee, yyy){
  print(ls())
  print(ls(envir=parent.frame(n=1)))
  return(dee*(w+yyy))
}


ls()
A <- 1
ls()
f(2)

# f(2) 실행 로직에 대한 풀이
# 1. f의 모수 출력 : "d" "y"
# 2. f의 parent function 출력 : "A"  "f" "h"
# 3. return h 함수의 모수 출력 : dee, yyy
# 4. h의 parent function 출력(f의 모수) : "d" "y"
# 만약, h함수에서  print(ls(envir=parent.frame(n=1))) ->  print(ls(envir=parent.frame(n=2)))
# 로 변경하면, R 전체의 객체가 출력

# beforeNa function
# 이전 값으로 대체하는 로직
# -> 이전 값이 없는 경우, 앞의 값으로 대체 하기 위한 로직
# 나중에 이전 값으로 대체해야 하는 경우, 해당 로직을 응용하자

beforeNa <- function(x){
  L <- !is.na(x)                                 
  x <- unlist(list(x[L][1], x[L]))[cumsum(L) + 1] 
  x
}

x <- c(NA,NA,6,NA,5)
beforeNa(x)

# zoo::na.approx fucntion
# zoo::na.approx
# NA 기준 앞 뒤의 평균 값을 계산하여 추가
# 일반적으로 앞 뒤의 평균 값을 계산하여 추가하고, 만약 앞 뒤 값이 없는 경우는
# beforeNa 함수를 이용하여 결측 처리

require(zoo)
x <- c(NA,NA,6,NA,5)
na.approx(x, na.rm = FALSE)

# type.convert function 
# type.convert : 자동으로 type convert 해주는 함수 **
# 반드시 문자형, 범주형인 경우에 가능
# 문자형 -> Logical, numeric, integer.. 등으로 변환하고 싶을 때 사용
# as.is param : TRUE 인 경우 factor -> character

tt <- type.convert("abcd", na.strings = 'NA')

# Hmisc::impute function
# 해당 vector 에 특정 값으로 대체해주는 함수(평균, 최빈값, 최소 값 등.. 결측에 해당 값을 대체)
# is.imputed 함수를 이용하면, 대체된 값의 T,F 를 알 수 있음 : 결측치 비율 등을 계산할 때 사용 가능
install.packages("Hmisc")
library(Hmisc)
x <- c(NA,NA,6,NA,5)
x.NAs <- impute(x, mean(x, na.rm = T)) # x vector 에 mean 으로 대체

# zip package in zip function
# file을 zip으로 만들어주는 함수
install.packages("zip")
require(zip)
zip_files <- list.files(path = "path입력", pattern = "패턴 입력") # 특정 패턴을 가진 파일의 list를 출력
zip::zip(zipfile = "경로+zipfile명", files = paste0("해당 파일 path", '/', Zip_Files))
file.remove(paste0(PLOT.DIR, '/', zip_files))

# fMultivar::rnorm2d function
# 특정 수치의 상관을 갖는 관측치를 랜덤으로 추출할 수 있음
install.packages("fMultivar")
library(fMultivar)
df <- fMultivar::rnorm2d(1000,rho=.5) # 0.5의 상관을 갖는 1000개의 관측치 생성


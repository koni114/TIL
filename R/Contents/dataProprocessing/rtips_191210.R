##########
## 목차 ##
##########
# 1. 여러개의 dataFrame을 리스트로 묶기 
# 2. list에 있는 객체 slicing 하기 
# 3.  문자열을 특정 길이로 만들고, 빈 자리는 '0'으로 채우는 방법
# 4. 소수 자리 수를 지정해주기
# 5.  JSON data -> RDataframe 형태로 저장 : jsonlite package : fromJSON

# 1. 여러개의 dataFrame을 리스트로 묶기 ----
# 1.1. R environment 상의 존재하는 여러 개의 DataFrame 중에서 특정 조건을 만족하는 DataFrame을 선별 : ls(pattern = "xx") 
# 1.2. 하나의 List로 묶는 방법 : mget()
# 1.3. List로 부터 특정 DataFrame을 Indexing 하는 방법 : list[[1]], list[["name"]]

install.packages('curl')
library(data.table)
library(jsonlite)
library(curl)
library(dplyr)

getwd()
rm(list = ls())  # Environment 에 있는 data 삭제 명령어.
cat("\014")  # console 에 있는 글귀 삭제 명령어.

# dataFrame 생성 : 예제 수행을 위한 DF 생성
data_1 <- data.frame(var1 = c(1, 2), var2 = c(3, 4))
data_2 <- data.frame(var1 = c('a', 'b'), var2 = c('c', 'd'))
data_3 <- data.frame(var1 = c(TRUE, TRUE), var2 = c(FALSE, TRUE))
file_1 <- data.frame(var1 = c(1, 2), var2 = c(3, 4))
file_2 <- data.frame(var1 = c('a', 'b'), var2 = c('c', 'd'))
file_3 <- data.frame(var1 = c(TRUE, TRUE), var2 = c(FALSE, TRUE))

# environment 에 생성된 객체 확인 : ls() ----
ls()

# 특정 문자열을 포한한 environment 객체 확인 ----
ls(pattern = "data_")

# 특정 문자열(ex) data_ )을 포함한 DF 객체를 list로 묶기 : mget() ----
mget.data_ <- mget(ls(pattern = "data_"))
mget.file_ <- mget(ls(pattern = "file_"))

# list에 있는 객체 slicing 하기 ----
mget.data_[[1]]
mget.data_[["data_1"]]

# 2. 문자열을 특정 길이로 만들고, 빈 자리는 '0'으로 채우는 방법 : sprintf {base}
# 데이터가 특정 형식으로 고정되어 있을 때, 주로 사용

# dataFrame 만들기
df <- data.frame(var1 = c(1, 11, 111, 1111))

# sprintf 를 이용하여 빈 자리수에 0 채우기 : 이때 factor type으로 전환
# ex) sprintf("%01d", var1) : 1자리수 문자열을 만들되, 1자리수가 되지 않으면 0으로 채움.
#    -> 이 때 1자리수보다 크면, 적용되지 않음

df <- transform(df,
                var1_01d = sprintf("%01d", var1),
                var1_02d = sprintf("%02d", var1),
                var1_03d = sprintf("%03d", var1)
)

# ** 주의! : data type 이 factor 형으로 변환 됨 
class(df[,2]) # factor로 변환

# 3. 소수 자리 수를 지정해주기 ----
# 3.1. 소수점 자리수 지정 : sprintf(".5f", var) ----
e <- c(3.141592)
sprintf("%.1f", e)  # 소수점 1째자리 수까지 지정
sprintf("%.2f", e)  # 소수점 2째자리 수까지 지정

# 3.2. 숫자 자리수 지정 : sprint("1.1f", e) ----
sprintf("%1.1f", e)
sprintf("%10.1f", e)  # 숫자 자리수가 변경 됨을 확인 -> 숫자 부분 : 10자리

# 4. 대용량 데이터 빠르게 읽어오는 방법 : fread() ----
library(data.table)

var1 <- rnorm(n = 1000000, mean = 1)
var2 <- rnorm(n = 1000000, mean = 2)
df.test <- data.frame(var1 = var1, var2 = var2)

write.table(df.test, file = "test.txt")

# system.time function을 이용해 시간 측정 시, 훨씬 빠름을 확인 가능
# fread() 로 호출 시, data.table, data.frame type 으로 저장

system.time(test2 <- read.table(file = "test.txt",
                                header = TRUE,
                                stringsAsFactors = F
            ))

system.time(test3 <- fread("test.txt",
                           header = TRUE,
                           stringsAsFactors = F
                           ))

# 5. JSON data -> RDataframe 형태로 저장 : jsonlite package : fromJSON ----
# JSON Data 형태의 data 호출

library(jsonlite)  # jsonlite library 호출(package가 없다면, 설치)
df_repos <- fromJSON("https://api.github.com/users/hadley/repos")  # fromJSON 함수를 이용하여 RDataFrame 로 저장
head(df_repos)  # 잘 저장됨을 확인

# 6. '#' 과 같은 특수 문자가 속해있는 문자를 가져오고 싶을 때, comment.char = "" ----
# read.table, read.csv 등 file을 가져올 때, parameter 로 comment.char = "" 를 넣어주면 됨



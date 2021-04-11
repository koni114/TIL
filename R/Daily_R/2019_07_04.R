# 2019_07_04
# lubricate package :: parse_date_time function
# 아무렇게 막 입력하는 날짜형을 예쁘게 변경 할 수 있는 방법
# -> 어떤 형식으로 Date format이 들어오던, ex) 2019-03-05, 201903-05, 2019/03/05 ..
#    날짜 형식이 아니지만 않으면(ex) 2019-33-33) 자동으로 Date format으로 변경해주는 함수

# gsub 함수와 병행해서 사용하면 combo ~
library(lubridate)

FromDate <- "2019-04_01"

if(!is.na(FromDate)){
  if(is.na(parse_date_time(FromDate, orders = "ymd")))stop("시작날짜 입력 형식을 확인하세요(yyyymmdd)")
  FromDate <- parse_date_time(FromDate, orders = "ymd")
  FromDate <- gsub("-", "", as.character(FromDate))
}

cat("FromDate :", FromDate)

test <- c(1,2,2,3,4)
df <- data.frame("cc" = test)
sum(is.na(as.numeric(df[, cc]))) == 0

sum(is.na(as.numeric(df[, "cc"]))) == 0 && !is.numeric(df[,"cc"])

# strptime() milesecond 표현 문제.
# 일반적으로 제조 데이터는 milsecond 단위의 데이터를 많이 다룬다. 
# 그렇다면 어떤 형식으로 데이터가 올라올까? 

# 다음과 같은 형식이다. -> 20190111002012812(%Y%m%d%H%M%OS)
# 그렇다면, 그냥 strptime 함수를 이용해서, 변환해주면 되지 않을까? 
# 하고 했더니.. 뒤에 milesecond 단위가 짤린다 

# 확인해보자 
as.POSIXct(strptime("20110327013000812", "%Y%m%d%H%M%OS"))

# 이에대한 해결방법은 ..? 
# -> 뒤에 3자리를 인식해서 .(comma)를 붙여주어야 한다.
as.POSIXct(strptime("20110327013000.812", "%Y%m%d%H%M%OS"))

# 그래도 혹시 뜨지 않는다면,
# getOption("digits.secs") 의 값이 3으로 setting이 되어있는지 확인해보자.

getOption("digits.secs")
options(digits.secs = 3)

# ** 주의해야 할 점.
# ms 단위의 숫자, 문자를 strptime() 함수를 이용하여 바꿀 때, 
# ms 끝자리 숫자가 1개씩 down되는 현상이 있음
# 따라서 문자형인 경우에는 paste0(time, '1')를 통해 붙여주여야 하고,
#        수치형인 경우에는 + 0.0001를 해주어야 함!!
# 2019_06_05, HJH
# 정규화 변환 Study
# -> 지수승, 로그, 제곱근, Box-Cox
# 등분산 검정
# levene, barlett, F-test

# 1. 지수승 변환
# 왼쪽으로 꼬리가 생긴 경우, -> 지수승 변환 ex) x^2, x^3
install.packages("UsingR")
install.packages("cluster")
library(UsingR)
library(Hmisc)
library(dplyr)

data(cfb)
summary(cfb$INCOME)
str(cfb)

hist(cfb$EDUC, breaks=500, freq=TRUE)                  # 그래프 자체가 왼쪽으로 많이 치우쳐져 있음
cfb <- cfb %>% mutate(INCOME_POW = (INCOME**2))        # 기존변수 + 파생변수 저장
hist(cfb$INCOME_POW, breaks=500, freq=TRUE)   

# 2. 로그 변환
# 
# 값에 0이 있을 시 에러 발생 -> 어떻게 할 것인가
# log의 역할은 큰 수를 같은 비율의 작은 수로 바꿔 주는 것이다.

# 값 중 0보다 작거나 같은 값이 있을 경우 log 변환은 불가해야 하는가?
# 아니면 최소 값을 + 해주어서 출력 해주어야 하는가?
# 밑을 입력 받게 할 것인가? 
# 더 세밀한 정규 변환이 필요한 경우, 파생변수 컴포넌트 이용
# -> 경고를 해주거나, +(-크기만큼 +해주어서 출력)

hist(cfb$INCOME, breaks=500, freq=TRUE)                  # 그래프 자체가 왼쪽으로 많이 치우쳐져 있음
cfb <- cfb %>% mutate(INCOME_LOG =log(INCOME+1, exp(1))) # 기존변수 + 파생변수 저장

cfb <- cfb %>% mutate(INCOME_LOG =log(INCOME+1, -10)) 
hist(cfb$INCOME_LOG, breaks=500, freq=TRUE)    

# 3. 제곱근, 세제곱근 변환
# 마찬가지로 큰 값을 더 작게 만들어주는 효과가 있음

hist(cfb$INCOME, breaks=500, freq=TRUE)                    # 그래프 자체가 왼쪽으로 많이 치우쳐져 있음
cfb <- cfb %>% mutate(INCOME_SQRT = (INCOME**(1/2)))       # 기존변수 + 파생변수 저장
hist(cfb$INCOME_SQRT, breaks=500, freq=TRUE)    

# 4. Box-cox 변환
# 정규분포가 아닌 자료를 정규분포로 변환하기 위하여 사용
# y(람다) = y^(람다) - 1 / 람다
# 여러가지 람다 값을 시도하여 가장 정규성을 높여주는 값을 찾아서 사용
library(caret)
hist(cfb$INCOME, breaks=500, freq=TRUE)                    # 그래프 자체가 왼쪽으로 많이 치우쳐져 있음
test <- caret::BoxCoxTrans(cfb$INCOME)
z    <- predict(test, cfb$INCOME)

# Box-Cox 변환 example
data(BloodBrain)
ratio <- exp(logBBB)
hist(ratio, breaks=500, freq=TRUE)      
bc <- BoxCoxTrans(ratio)
bc$lambda
predict(bc, ratio)
hist(predict(bc, ratio), breaks=500, freq=TRUE)  

# tip function
# 인간적으로 이제 tryCatch문은 알아서 좀 잘해보자
# tryCatch function
tryCatch({
  
}, error = function(err){print(err)})

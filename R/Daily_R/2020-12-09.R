# 2020-12-09
# lapply, data.table::rbindlist function을 이용하여
# group 별로 특정함수를 적용하고, 
# return된 data.frame을 기존의 idx 정렬로 return 시키는 방법

# 쉽게 하려다 보니, data.frame의 특정 컬럼의 그룹별로  
# 특정 로직을 적용하고 다시 재정렬시켜야 하는 경우가 발생한다.

#  다시 재정렬 한다는 말은 무슨말일까?
# 다음의 예시를 살펴보자

library(dplyr)
test <- data.frame(a = c(1,2,3,4,5), b = c("a",'b','a','b','c'))
grpByTest <- test %>% group_by(b)
do(grpByTest, .["a"])

# group_by 함수를 적용하면, a,b,c별로 그룹이 생성되고, do function을 통해  
# 적절한 조치를 취할 수 있다.
# 이번 경우는 아무것도 하지 않고 b컬럼의 값을 return 했는데, 순서가 a,b,c 로 정렬돼서 나온 것을 알 수 있다.
# 기존의 정렬 순서 그대로 return 시키려면 어떻게 해야 할까?

# lapply, rbindlist, data.table를 이용하여 data.frame을 정렬시킬 수 있다.
# 예를 들어, group 별로 각각 knnImpation function을 적용시키고 싶은 경우를 생각해보자.
# 이 때 그룹 dataframe 마다 knn 알고리즘을 적용시키지 못하는 경우도 발생할 것이다.
# 이럴 때는 기존 값 그대로 return해보자.

##########
## 예시 ##
##########

# iris data에서 Sepal.Length 컬럼 값을 난수 생성으로 50개 NA를 발생시켜, 
# 이를 Species별로 각각 결측을 대체하는 case를 구현해보자
require(DMwR);require(dplyr);require(data.table);

#- iris data 의 Sepal.Length 컬럼에 랜덤으로 50개의 결측 생성
test <- iris
test[sample(1:nrow(iris), 50), "Sepal.Length"] <- NA

#- Species 별로 각각 knnImputation 적용
#- 이 때 return 값은 list로 되어 있음
treatNaDf <- lapply(split(test, test$Species), function(df_tmp){
    x <- df_tmp[,"Sepal.Length"]  
    tryCatch({
     x <-  DMwR::knnImputation(df_tmp, k = sqrt(nrow(df_tmp)))["Sepal.Length"]
    }, error = function(x){
    x
    })
})

#- unlist, lapply function을 통해 rn이라는 컬럼에 ron_number를 저장하고, 해당 rn 컬럼으로 재정렬함 
rbList <- data.table::rbindlist(treatNaDf) 
rbList[, rn := as.numeric(unlist(lapply(treatNaDf, rownames)))] %>%  arrange(rn)


#- dplyr 연습
library(dplyr)
library(stringr)
library(psych)
library(fbasics)
library(caret)
titanic <- titanic %>% data.frame
#- 1. Sepal.Length < 5.0 인 값을 추출
#- 2. 5, 10, 15, 20행 추출
#- 3. Sepal로 시작하는 컬럼을 선택
#- 4. Length로 끝나는 문자열 선택
#- 5. 특정 문자열이 포함되는 컬럼 선택
#- 6. 정규표현식을 활용해보기 -> titanic의 Name에서 Mr, Mrs, Miss, 찾아보기
#- 7. 컬럼명을 변경해보기
#- 8. level 추출해보기
#- 9. dplyr에서 sampling 해보기(값/비율로 추출해보기)
#- 10. Species별 층화 추출 해보기
#- 11. 파생변수 생성해보기(특정 조건에 해당하는 컬럼, 사칙연산을 이용한 파생변수)
#- 12. 요약통계 계산해보기(평균, 중위, 1분위수, 3분위수, 최소, 최대, 첨도, 왜도)
#- 13. 열결합, 행결합 수행
#- 14. 그룹별로 조건을 확인 후, slicing을 하고 싶을 때, 어떻게 해야하지 ? 
#-     예를 들어 Species 조건별로 Sepal.Length 값이 평균 값 이상인 것들만 추출
#- 15. Species 그룹 별로,  Sepal.Length 값이 하나라도 음수가 있으면 해당 그룹을 제거
#- 16. Species 그룹 별로,  Sepal.Length 값이 한 개라도 10이 넘는 그룹이 있다면, 해당 그룹 데이터 전부를 포함
#- 17. ** 특정 값을 누적해 가면서 값 반환
#- 18. titanic.csv를 loading 해오기
#- 19. 오늘 날짜를 반환하여 %Y, %Y-%m-%d 형태로 변환해보기 
#- 20. 날짜형에서 monday, tuesday 등을 추출해보기.
#- 21. 만약 50개의 sequence data에서 2021-01-01 부터 날짜를 추가한 파생변수를 추가하려면 ? 
#- 22. 2021-01-01 ~ 오늘까지의 sequence data를 만들어 보아라
#- 23. 어떤 날짜는 20210101, 어떤 날짜는 2021-01-01로 구성되어 있으면 어떻게 해결?
#- 24. 년, 월, 일의 사칙연산은 어떻게 할 것 인가?
#- 25. label encoding시 어떻게 할 것인가? one-hot encoding은 어떻게 할 것인가? 
#- 26. 만약 ranking을 매기고 싶을 때,  tie인 경우 min으로 하고 싶다면?
#- 27. MASS library에 있는 Cars93 data 중 Type, Origin, MPG.city, MPG.highway 컬럼을 선택하고, Compact, Van만 filtering
#-     Compact, Van에 대한 데이터를 MPG.city, MPG.highway -> rowise로 변환
#- 28. 27번에서 melt한 데이터를 다시 columize 시켜 보시오
#- 29. 정규표현식에서 대소문자 구분하는 메타문자는?
#- 30. 데이터를 단순임의추출하기 위한 방법은?
#- 31. 종속변수에 대한 층화임의추출을 하기 위한 방법은?
#- 32. data shift를 하고 싶다. 선행 이동, 후행 이동을 하려면 어떻게 해야하는가? 
#- 33. iris 데이터를 Species 별로 data.frame으로 쪼개기
#- 34. 문자열의 길이를 알고싶은 경우는 어떻게 해야 하는가?
#- 35. 다음과 같은 data.frame 이 있을 때, 하나의 컬럼을 두 개의 컬럼으로 쪼개는 작업을 수행하시오.
#- 36. 데이터 표준화는 2가지 방법이 있다(표준화, 정규화) 어떻게 계산할 것인가? 
#- 37. 결측치가 발생한 행을 제거하시오
#- 38. 컬럼별로 결측치가 발생 비율이 50$% 이상은 컬럼을 제거
#- 39. 결측치가 발생한 행에서, 수치형이면 평균값으로, 범주형이면 최빈값으로 대체하시오
#- 40. 전체 데이터의 10%, 90% 는 어떻게 구할 수 있을까? 
#- 41. 5 간격으로의 이동 평균을 계산하시오

library(MASS)
library(reshape2)

########
# 해답 #
########
#- 1
iris %>% filter(Sepal.Length < 5.0)

#- 2
iris %>% slice(c(5, 10, 15, 20))


#- 3
iris %>% dplyr::select(starts_with('Sepal'))

#- 4
iris %>% dplyr::select(ends_with('Length'))

#- 5
iris %>% dplyr::select(contains('S'))

#- 6
colnames(titanic)
titanic <- titanic %>% dplyr::mutate('isMerried' = stringr::str_extract(Name, 'Mrs|Mr|Miss'))

#- 7
iris %>% dplyr::rename(hello = Species)

#- 8
iris %>% dplyr::select(Species) %>% distinct() %>% unlist %>% as.character

#- 9.
iris %>% sample_n(10, replace = F) %>% nrow
iris %>% sample_frac(0.5, replace = F) %>% nrow

#- 10.
iris %>% group_by(Species) %>% sample_n(10) %>% nrow
 
#- 11.
summary(iris)
iris %>% mutate('sum' = Sepal.Length + Sepal.Width + Petal.Length + Petal.Width) 
iris %>% mutate('기상 조건' = case_when(
  Sepal.Length >= 5.8 ~ sqrt(Sepal.Length),
  TRUE ~ Sepal.Length
))

#- 12.
iris %>% dplyr::select(is.numeric) %>% summarise_all(~mean(., na.rm = T))
iris %>% dplyr::select(is.numeric) %>% summarise_all(~median(., na.rm = T))
iris %>% dplyr::select(is.numeric) %>% summarise_all(~quantile(., na.rm = T)[2])
iris %>% dplyr::select(is.numeric) %>% summarise_all(~quantile(., na.rm = T)[4])
iris %>% dplyr::select(is.numeric) %>% summarise_all(~skew(., na.rm = T))

#- 13
dplyr::bind_rows(iris, iris) %>% nrow
test1 <- iris %>% select(c(1,2,5))
test2 <- iris %>% select(c(1,3,5))

dplyr::left_join(test1, test2, by=c('Species'))

#- 14
iris %>% group_by(Species) %>% filter(Sepal.Length >= mean(Sepal.Length)) %>% data.frame

#- 15
iris %>% group_by(Species) %>% filter(cumall(Sepal.Length >= 0)) %>% nrow()

#- 16
iris %>% group_by(Species) %>% arrange(Sepal.Length) %>% filter(cumany(Sepal.Length >= 7)) %>% nrow()

#- 17
iris %>% group_by(Species) %>% mutate(cummean.Sepal.Length = cummean(Sepal.Length)) %>% data.frame

#- 18.
titanic <- data.table::fread('~/R/data/titanic.csv',
                  header = T,
                  stringsAsFactors = F,
                  na.strings = c('NA', ''))


#- 19, 20
today <- Sys.Date()
format(today, '%Y')
format(today, '%Y-%m')
format(today, '%A')
format(today, '%y-%m-%d %H:%M:%S')

#- 21.
length(seq(as.Date('2021-01-01'), as.Date('2021-02-19'), 1))

#- 22.
lubridate::interval('2021-01-01', lubridate::today()) %>% as.period()

#- 23.
str(lubridate::ymd('2021-01-01', '20210102'))


#- 24. 
today <- Sys.Date()
today + lubridate::years(1)  #- 년 추가
today + lubridate::month(1)  #- 월 추가
today + lubridate::days(1)   #- 일 추가

#- 25.
#- label encoding --> case when 
iris %>% dplyr::select(Species) %>%  distinct()
iris %>% mutate('Species_encoding' = case_when(
  Species == 'setosa' ~ 1,
  Species == 'versicolor' ~ 2,
  Species == 'virginica' ~ 3
))

#- one-hot encoding --> caret::dummyVars
pred <- caret::dummyVars(~ Species, data = iris)
oneHot_df <- predict(pred, iris[,5, drop = F])
new_df <- cbind(iris, oneHot_df)

#- 26.
test <- c(1,4,4,4,4,3,2,5,10,9)
rank(test,ties.method = c('min'))

#- 27.
Cars93_filter <- Cars93 %>% dplyr::select(Type, Origin, MPG.city, MPG.highway) %>% filter(Type %in% c("Compact", "Van"))
Cars93_filter_melt <- reshape2::melt(Cars93_filter, 
                                     id.vars = c('Type', 'Origin'),
                                     measure.vars = c('MPG.city','MPG.highway'))

Cars93_filter_melt_add_id <- Cars93_filter_melt %>% group_by(variable) %>% mutate(id = row_number())
reshape2::dcast(Cars93_filter_melt_add_id, 'Type + Origin + id ~ variable', value.var = c('value'))

#- 30.
trainIdx <- sample(1:nrow(iris), nrow(iris) * 0.7)
train <- iris[trainIdx,  ]
test  <- iris[-trainIdx, ]

#- 31.
trainIdx <- caret::createDataPartition(iris[,c('Species')], p=0.7, list=F)
train    <- iris[trainIdx,  ]
test     <- iris[-trainIdx, ]

nrow(train)
nrow(test)

#- 32.
windowSize <- 2
iris_numeric_window <- iris %>% select_if(is.numeric) %>% mutate_all(~lag(., windowSize)) %>% rename(Sepal.Length.window = Sepal.Length,
                                                                              Sepal.Width.window = Sepal.Width,
                                                                              Petal.Length.window = Petal.Length,
                                                                              Petal.Width.window = Petal.Width)
dplyr::bind_cols(iris, iris_numeric_window)

#- 33.
iris_split_list <- split(iris, iris$Species)
iris_split_list$setosa
iris_split_list$versicolor
iris_split_list$virginica

#- 34.
iris %>% mutate('Species_nchar' = nchar(as.character(Species)))
substr(c('hello', 'world', 'my', 'name', 'is', 'HJH'), 0, 1)
stringr::str_split("hello world! my name is HJH", " ")[[1]]

#- 35. 
test <- data.frame(ID = c(1:3), name = c("Chulsu/Kim", "Younghei/Lee", "Dongho/Choi"))
do.call('rbind', strsplit(test$name, '/')) %>% data.frame

#- 36.
min_max_scaler <- function(x){
  round((max(x) - x) / (max(x) - min(x)), 3)
}
iris %>% select_if(is.numeric) %>% mutate_all(~min_max_scaler(.))

#- 38.
titanic %>% nrow()
titanic %>% filter_all(~!is.na(.)) %>% nrow()  #- 행제거
checkNaRatio <- function(x){
  sum(is.na(x)) / length(x) < 0.5
}
str(titanic)
titanic %>% select_if(checkNaRatio) %>% ncol
titanic %>% select_if(is.numeric) %>%  mutate_all(~ifelse(is.na(.x), mode(.x, na.rm =T), .x))
titanic %>% select_if(is.character) %>%  mutate_all(~ifelse(is.na(.x), mode(.x, na.rm =T), .x))

(titanic$Cabin)

#- 40
quantile(iris$Sepal.Length, 0.9, na.rm = T)
quantile(iris$Sepal.Length, 0.1, na.rm = T)

#- 41. zoo::rollapply


#- 정규표현식 test
#- 대소문자 구분 안한다는 메타 문자는? 
#- 문자 개수 지정 방법은?
#- 1개 이상, 0개 이상, 0또는 1
#- 다음의 text 중 "<html><head><Title>제목</head></html>" 에서 <> 를 split 하려면 어떻게 해야하는가?
iris %>% filter(grepl('^s.', Species))
stringr::str_extract(c('010-9119-7025 입니다. 전화주세요!', '제 전화번호는 01091197025입니다.'), '(010)(\\D?\\d{4}){2}')



